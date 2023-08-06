#define SHAREDATA_MAIN_C_FILE
#include "common.h"
#include "PNUMPY.h"
//extern "C" void** PyArray_API;
PyTypeObject* pPyArray_Type = NULL;

/*
 * Some C++ compilers do not like mixin non-designated-initializers
 * like PyModuleDef_HEAD_INIT with designated-initializers like
 * .m_doc, so break this part out into a C file
 */
  

extern "C" PyObject* oldinit(PyObject *self, PyObject *args, PyObject *kwargs);
extern "C" PyObject* newinit(PyObject* self, PyObject* args, PyObject* kwargs);
extern "C" PyObject* atop_enable(PyObject * self, PyObject * args);
extern "C" PyObject* atop_disable(PyObject * self, PyObject * args);
extern "C" PyObject* atop_isenabled(PyObject * self, PyObject * args);
extern "C" PyObject* atop_info(PyObject * self, PyObject * args);
extern "C" PyObject* atop_setworkers(PyObject * self, PyObject * args);
extern "C" PyObject* thread_enable(PyObject * self, PyObject * args);
extern "C" PyObject* thread_disable(PyObject * self, PyObject * args);
extern "C" PyObject* thread_isenabled(PyObject * self, PyObject * args);
extern "C" PyObject* thread_getworkers(PyObject * self, PyObject * args);
extern "C" PyObject* thread_setworkers(PyObject * self, PyObject * args);
extern "C" PyObject* thread_zigzag(PyObject * self, PyObject * args);

// ledger.cpp
extern "C" PyObject* ledger_enable(PyObject * self, PyObject * args);
extern "C" PyObject* ledger_disable(PyObject * self, PyObject * args);
extern "C" PyObject* ledger_isenabled(PyObject * self, PyObject * args);
extern "C" PyObject* ledger_info(PyObject * self, PyObject * args);

// recycler.cpp
extern "C" PyObject* recycler_enable(PyObject * self, PyObject * args);
extern "C" PyObject* recycler_disable(PyObject * self, PyObject * args);
extern "C" PyObject* recycler_isenabled(PyObject * self, PyObject * args);
extern "C" PyObject* recycler_info(PyObject * self, PyObject * args);

extern "C" PyObject * hook_enable(PyObject * self, PyObject * args);
extern "C" PyObject * hook_disable(PyObject * self, PyObject * args);

extern "C" PyObject* timer_gettsc(PyObject * self, PyObject * args);
extern "C" PyObject* timer_getutc(PyObject * self, PyObject * args);
extern "C" PyObject* cpustring(PyObject * self, PyObject * args);
extern "C" PyObject * getitem(PyObject * self, PyObject * args);
extern "C" PyObject * lexsort32(PyObject * self, PyObject * args, PyObject * kwargs);
extern "C" PyObject * lexsort64(PyObject * self, PyObject * args, PyObject * kwargs);
extern "C" PyObject * sort(PyObject * self, PyObject * args, PyObject * kwargs);

// conversions.cpp
extern "C" PyObject* recarray_to_colmajor(PyObject* self, PyObject* args);

static char m_doc[] = "Provide methods to override NumPy ufuncs";


PyDoc_STRVAR(oldinit_doc,
     "oldinit(ufunc_name:");

static PyMethodDef module_functions[] = {
    {"initialize",       (PyCFunction)newinit, METH_VARARGS | METH_KEYWORDS, INITIALIZE_DOC},
    {"atop_enable",      (PyCFunction)atop_enable, METH_VARARGS, ATOP_ENABLE_DOC},
    {"atop_disable",     (PyCFunction)atop_disable, METH_VARARGS, ATOP_DISABLE_DOC},
    {"atop_isenabled",   (PyCFunction)atop_isenabled, METH_VARARGS, ATOP_ISENABLED_DOC},
    {"atop_info",        (PyCFunction)atop_info, METH_VARARGS, "return dict"},
    {"atop_setworkers",  (PyCFunction)atop_setworkers, METH_VARARGS, "set workers for a func"},
    {"thread_enable",    (PyCFunction)thread_enable, METH_VARARGS, THREAD_ENABLE_DOC},
    {"thread_disable",   (PyCFunction)thread_disable, METH_VARARGS, THREAD_DISABLE_DOC},
    {"thread_isenabled", (PyCFunction)thread_isenabled, METH_VARARGS, THREAD_ISENABLED_DOC},
    {"thread_getworkers",(PyCFunction)thread_getworkers, METH_VARARGS, THREAD_GETWORKERS_DOC},
    {"thread_setworkers",(PyCFunction)thread_setworkers, METH_VARARGS, THREAD_SETWORKERS_DOC},
    {"thread_zigzag",      (PyCFunction)thread_zigzag,  METH_VARARGS, "toggle zigzag mode"},
    {"timer_gettsc",     (PyCFunction)timer_gettsc, METH_VARARGS, TIMER_GETTSC_DOC},
    {"timer_getutc",     (PyCFunction)timer_getutc, METH_VARARGS, TIMER_GETUTC_DOC},
    {"hook_enable",      (PyCFunction)hook_enable, METH_VARARGS, "Enable hook for numpy array __getitem__ for fancy and bool indexing"},
    {"hook_disable",     (PyCFunction)hook_disable, METH_VARARGS, "Disable hook for numpy array __getitem__ for fancy and bool indexing"},
    {"ledger_enable",    (PyCFunction)ledger_enable,  METH_VARARGS, LEDGER_ENABLE_DOC},
    {"ledger_disable",   (PyCFunction)ledger_disable,  METH_VARARGS, LEDGER_DISABLE_DOC},
    {"ledger_isenabled", (PyCFunction)ledger_isenabled,  METH_VARARGS, LEDGER_ISENABLED_DOC},
    {"ledger_info",      (PyCFunction)ledger_info,  METH_VARARGS, LEDGER_INFO_DOC},
    {"recycler_enable",    (PyCFunction)recycler_enable,  METH_VARARGS, RECYCLER_ENABLE_DOC},
    {"recycler_disable",   (PyCFunction)recycler_disable,  METH_VARARGS, RECYCLER_DISABLE_DOC},
    {"recycler_isenabled", (PyCFunction)recycler_isenabled,  METH_VARARGS, RECYCLER_ISENABLED_DOC},
    {"recycler_info",      (PyCFunction)recycler_info,  METH_VARARGS, RECYCLER_INFO_DOC},
    {"cpustring",        (PyCFunction)cpustring, METH_VARARGS, CPUSTRING_DOC},
    {"oldinit",          (PyCFunction)oldinit, METH_VARARGS | METH_KEYWORDS, OLDINIT_DOC},
    {"recarray_to_colmajor",    (PyCFunction)recarray_to_colmajor,  METH_VARARGS, "convert record array to col major"},
    {"getitem",          (PyCFunction)getitem, METH_VARARGS | METH_KEYWORDS, "alternative to fancy index or boolean index"},
    {"lexsort32",        (PyCFunction)lexsort32, METH_VARARGS | METH_KEYWORDS, "lexigraphical sort returning int32 fancy indexing"},
    {"lexsort64",        (PyCFunction)lexsort64, METH_VARARGS | METH_KEYWORDS, "lexigraphical sort returning int64 fancy indexing"},
    {"sort",             (PyCFunction)sort, METH_VARARGS | METH_KEYWORDS, "parallel inplace quicksort, followed by mergesort"},
    {NULL, NULL, 0,  NULL}
};


static PyModuleDef moduledef = {
   PyModuleDef_HEAD_INIT,
   "pnumpy._pnumpy",                  // Module name
   m_doc,  // Module description
   0,
   module_functions,                     // Structure that defines the methods
   NULL,                                 // slots
   NULL,                                 // GC traverse
   NULL,                                 // GC
   NULL                                  // freefunc
};

PyMODINIT_FUNC PyInit__pnumpy(void) {
    PyObject *module;

    module = PyModule_Create(&moduledef);

    if (module == NULL)
        return NULL;

    // Load numpy for PyArray_Type
    import_array();
    pPyArray_Type = &PyArray_Type;

    atop_init();
    LedgerInit();

    return module;
}
