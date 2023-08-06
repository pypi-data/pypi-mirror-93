#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include "utils.hpp"

#define HTTP_101 "HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: Upgrade\r\n"

struct Buffer {
    int size;
    uint8_t * data;

    void push(const void * data, int size) {
        if (size) {
            int new_size = this->size + size;
            this->data = (uint8_t *)realloc(this->data, new_size);
            if (data) {
                memcpy(this->data + this->size, data, size);
            }
            this->size += size;
        }
    }

    void pop(int size) {
        int new_size = this->size - size;
        if (new_size) {
            memcpy(this->data, this->data + size, new_size);
            this->data = (uint8_t *)realloc(this->data, new_size);
        } else {
            free(this->data);
            this->data = NULL;
        }
        this->size -= size;
    }
};

struct ModuleState {
    Socket sock;
    Buffer input;
    Buffer output;
    PyObject * json;
};

void disconnected(ModuleState * state) {
    PyErr_Format(PyExc_RuntimeError, "disconnected");
    state->input.pop(state->input.size);
    state->output.pop(state->output.size);
    sock_close(state->sock);
    state->sock = 0;
}

PyObject * webqueue_meth_init(PyObject * self, PyObject * args, PyObject * kwargs) {
    ModuleState * state = (ModuleState *)PyModule_GetState(self);

    const char * keywords[] = {"host", "port", NULL};
    const char * host = "0.0.0.0";
    int port = 5000;
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "|si", (char **)keywords, &host, &port)) {
        return NULL;
    }

    Socket listener = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    sockaddr_in address = {AF_INET, htons(port)};
    address.sin_addr.s_addr = inet_addr(host);
    socklen_t address_size = sizeof(address);
    sock_reuse(listener);
    bind(listener, (sockaddr *)&address, address_size);
    getsockname(listener, (sockaddr *)&address, &address_size);
    listen(listener, 1);
    state->sock = accept(listener, (sockaddr *)&address, &address_size);
    sock_close(listener);
    char request[4096] = {};
    sock_read(state->sock, request, 4000);
    char * key = strstr(request, "Sec-WebSocket-Key");
    char response[] = HTTP_101 "Sec-WebSocket-Accept: ____________________________\r\n\r\n";
    sec_websocket_accept(key + 19, response + 97);
    sock_write(state->sock, response, 129);
    sock_blocking(state->sock, false);
    Py_RETURN_NONE;
}

PyObject * webqueue_meth_flush(PyObject * self) {
    ModuleState * state = (ModuleState *)PyModule_GetState(self);
    if (state->output.size) {
        int chunk = sock_write(state->sock, state->output.data, state->output.size);
        if (chunk < 0 && !sock_would_block()) {
            disconnected(state);
            return NULL;
        }
        if (chunk > 0) {
            state->output.pop(chunk);
        }
    }
    Py_RETURN_NONE;
}

PyObject * webqueue_meth_update(PyObject * self) {
    ModuleState * state = (ModuleState *)PyModule_GetState(self);
    PyObject * flush = webqueue_meth_flush(self);
    if (!flush) {
        return NULL;
    }
    Py_DECREF(flush);
    PyObject * res = PyList_New(0);
    while (true) {
        char buffer[65536];
        int chunk = sock_read(state->sock, buffer, 65536);
        if ((chunk < 0 && !sock_would_block()) || !chunk) {
            disconnected(state);
            return NULL;
        }
        if (chunk > 0) {
            state->input.push(buffer, chunk);
        }
        if (chunk == 65536) {
            continue;
        }
        break;
    }
    while (true) {
        uint8_t * data = state->input.data;
        int head = (state->input.size < 2 ? 2 : data[1] == 255 ? 10 : data[1] == 254 ? 4 : 2) + 4;
        if (state->input.size < head) {
            break;
        }
        int temp = *(int *)(data + 2) & 0x7fffffff;
        int size = data[1] == 255 ? temp : data[1] == 254 ? temp & 0xffff : data[1] - 128;
        if (state->input.size < size) {
            break;
        }
        uint8_t opcode = data[0] & 15;
        if (opcode == 8) {
            disconnected(state);
            return NULL;
        }
        if (opcode == 9) {
            data[0] ^= 3;
            state->output.push(data, head + size);
            state->input.pop(head + size);
            continue;
        }
        if (opcode == 10) {
            state->input.pop(head + size);
            continue;
        }
        uint8_t * mask = data + head - 4;
        uint8_t * payload = data + head;
        for (int i = 0; i < size; ++i) {
            payload[i] ^= mask[i & 3];
        }
        PyObject * msg = PyBytes_FromStringAndSize((char *)payload, size);
        msg = PyObject_CallMethod(state->json, "loads", "N", msg);
        if (!msg) {
            return NULL;
        }
        PyList_Append(res, msg);
        Py_DECREF(msg);
        state->input.pop(head + size);
    }
    return res;
}

PyObject * webqueue_meth_block(PyObject * self) {
    ModuleState * state = (ModuleState *)PyModule_GetState(self);
    sock_blocking(state->sock, true);
    while (state->output.size) {
        PyObject * flush = webqueue_meth_flush(self);
        if (!flush) {
            return NULL;
        }
        Py_DECREF(flush);
    }
    while (true) {
        PyObject * res = webqueue_meth_update(self);
        if (!res) {
            return NULL;
        }
        if (PyList_Size(res)) {
            sock_blocking(state->sock, false);
            return res;
        }
        Py_DECREF(res);
    }
}

PyObject * webqueue_meth_send(PyObject * self, PyObject * arg) {
    ModuleState * state = (ModuleState *)PyModule_GetState(self);
    PyObject * dump = PyObject_CallMethod(state->json, "dumps", "O", arg);
    if (!dump) {
        return NULL;
    }
    PyObject * bytes = PyObject_CallMethod(dump, "encode", NULL);
    if (!bytes) {
        return NULL;
    }
    int size = (int)PyBytes_Size(bytes);
    const char * str = PyBytes_AsString(bytes);
    int head = size < 126 ? 2 : size < 65536 ? 4 : 10;
    state->output.push(NULL, (int)(head + size));
    state->output.data[state->output.size - size - head] = 129;
    state->output.data[state->output.size - size - head + 1] = size < 126 ? size : size < 65536 ? 126 : 127;
    memcpy(state->output.data + state->output.size - size - head + 2, &size, size < 126 ? 0 : size < 65536 ? 2 : 8);
    memcpy(state->output.data + state->output.size - size, str, size);
    Py_DECREF(bytes);
    Py_DECREF(dump);
    Py_RETURN_NONE;
}

PyMethodDef module_methods[] = {
    {"init", (PyCFunction)webqueue_meth_init, METH_VARARGS | METH_KEYWORDS, NULL},
    {"flush", (PyCFunction)webqueue_meth_flush, METH_NOARGS, NULL},
    {"update", (PyCFunction)webqueue_meth_update, METH_NOARGS, NULL},
    {"block", (PyCFunction)webqueue_meth_block, METH_NOARGS, NULL},
    {"send", (PyCFunction)webqueue_meth_send, METH_O, NULL},
    {},
};

int module_exec(PyObject * self) {
    ModuleState * state = (ModuleState *)PyModule_GetState(self);
    #if defined(_WIN32) || defined(_WIN64)
    WSADATA wsa_data;
    WSAStartup(MAKEWORD(2, 2), &wsa_data);
    #endif
    state->json = PyImport_ImportModule("json");
    if (!state->json) {
        return -1;
    }
    PyModule_AddObject(self, "json", state->json);
    Py_DECREF(state->json);
    return 0;
}

static PyModuleDef_Slot module_slots[] = {
    {Py_mod_exec, (void *)module_exec},
    {},
};

PyModuleDef module_def = {PyModuleDef_HEAD_INIT, "webqueue", NULL, sizeof(ModuleState), module_methods, module_slots};

extern "C" PyObject * PyInit_webqueue() {
    return PyModuleDef_Init(&module_def);
}
