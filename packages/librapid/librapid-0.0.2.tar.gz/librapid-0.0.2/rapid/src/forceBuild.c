// This file simply means that setup.py must be run before installation,
// hence running the buildExtensions function and compiling the CUDA code.
// Without this file, python assumes there are no external files to
// compile, and will create a pure-python wheel which is then installed,
// meaning the CUDA dlls are not created and the code will not work.

#include <Python.h>

static PyMethodDef matrixFunctionMethods[] = {
        {NULL}
};

static PyModuleDef matrixCoreModule = {
        PyModuleDef_HEAD_INIT,
        .m_name = "forceBuild",
        .m_doc = "Force rapid/setup.py to run",
        .m_size = -1,
        matrixFunctionMethods
};

PyMODINIT_FUNC
PyInit_forceBuild(void) {
    PyObject *m;
    m = PyModule_Create(&matrixCoreModule);
    if (m == NULL)
        return NULL;

    return m;
}
