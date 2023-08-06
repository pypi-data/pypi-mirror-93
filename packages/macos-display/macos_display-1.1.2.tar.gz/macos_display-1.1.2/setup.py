from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
from distutils.errors import CompileError

import sys
import platform


class get_pybind_include:
    """Helper class to determine the pybind11 include path
    The purpose of this class is to postpone importing pybind11
    until it is actually installed, so that the ``get_include()``
    method can be invoked. """

    def __init__(self, user=False):
        self.user = user

    def __str__(self):
        import pybind11
        return pybind11.get_include(self.user)


if platform.system() != 'Darwin':
    print("The macos_display package can only be installed on macOS", file=sys.stderr)
    sys.exit(1)

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


# As of Python 3.6, CCompiler has a `has_flag` method.
# cf http://bugs.python.org/issue26689
def has_flag(compiler, flagname):
    """Return a boolean indicating whether a flag name is supported on
    the specified compiler.
    """
    import tempfile
    with tempfile.NamedTemporaryFile('w', suffix='.cpp') as f:
        f.write('int main (int argc, char **argv) { return 0; }')
        try:
            compiler.compile([f.name], extra_postargs=[flagname])
        except CompileError:
            return False
    return True


def cpp_flag(compiler):
    """Return the -std=c++[11/14] compiler flag.
    The c++14 is prefered over c++11 (when it is available).
    """
    if has_flag(compiler, '-std=c++14'):
        return '-std=c++14'
    elif has_flag(compiler, '-std=c++11'):
        return '-std=c++11'
    else:
        raise RuntimeError('Unsupported compiler -- at least C++11 support '
                           'is needed!')


class BuildExt(build_ext):
    """A custom build extension for adding compiler-specific options."""
    def build_extensions(self):
        opts = ['-stdlib=libc++', '-mmacosx-version-min=10.7']
        opts.append('-DVERSION_INFO="%s"' % self.distribution.get_version())
        opts.append(cpp_flag(self.compiler))
        if has_flag(self.compiler, '-fvisibility=hidden'):
            opts.append('-fvisibility=hidden')
        for ext in self.extensions:
            ext.extra_compile_args = opts
        build_ext.build_extensions(self)


ext_modules = [
    Extension(
        'macos_display.display',
        ['macos_display/display_module.cpp', 
         'macos_display/display.cpp'],
        extra_link_args=[
            '-framework', 'IOKit',
            '-framework', 'CoreFoundation',
            '-framework', 'ApplicationServices'
        ],
        include_dirs=[
            get_pybind_include(),
            get_pybind_include(user=True)
        ],
        language='c++'
    ),
]

setup(
    name='macos_display',
    author='rob@sixty-north.com',
    author_email="rob@sixty-north.com",
    description="Retrieve information about macOS displays",
    long_description=long_description,
    long_description_content_type='text/x-rst',
    version='1.1.2',
    url="https://github.com/sixty-north/macos-display",
    packages=['macos_display'],
    ext_modules=ext_modules,
    cmdclass={'build_ext': BuildExt},
    install_requires=[
        'pybind11',  # This is needed if users have to build from source
    ],
    extras_require={
        'dev': ['bump2version', 'pybind11'],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: zlib/libpng License',
    ]
)
