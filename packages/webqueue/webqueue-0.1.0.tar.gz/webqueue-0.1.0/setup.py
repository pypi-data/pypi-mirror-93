import platform
from setuptools import Extension, setup

libraries = ['ws2_32'] if platform.system().lower().startswith('windows') else []

ext = Extension(
    name='webqueue',
    sources=['./webqueue.cpp'],
    libraries=libraries,
    define_macros=[('Py_LIMITED_API', '0x03050000')],
    py_limited_api=True,
)

setup(
    name='webqueue',
    version='0.1.0',
    ext_modules=[ext],
)
