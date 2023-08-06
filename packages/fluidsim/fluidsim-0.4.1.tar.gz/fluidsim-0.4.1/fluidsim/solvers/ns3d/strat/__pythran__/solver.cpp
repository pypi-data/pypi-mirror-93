#include <pythonic/core.hpp>
#include <pythonic/python/core.hpp>
#include <pythonic/types/bool.hpp>
#include <pythonic/types/int.hpp>
#ifdef _OPENMP
#include <omp.h>
#endif
#include <pythonic/include/types/complex128.hpp>
#include <pythonic/include/types/ndarray.hpp>
#include <pythonic/include/types/float64.hpp>
#include <pythonic/types/float64.hpp>
#include <pythonic/types/ndarray.hpp>
#include <pythonic/types/complex128.hpp>
#include <pythonic/include/builtins/tuple.hpp>
#include <pythonic/include/numpy/square.hpp>
#include <pythonic/include/operator_/mul.hpp>
#include <pythonic/include/operator_/neg.hpp>
#include <pythonic/include/operator_/sub.hpp>
#include <pythonic/include/types/slice.hpp>
#include <pythonic/include/types/str.hpp>
#include <pythonic/builtins/tuple.hpp>
#include <pythonic/numpy/square.hpp>
#include <pythonic/operator_/mul.hpp>
#include <pythonic/operator_/neg.hpp>
#include <pythonic/operator_/sub.hpp>
#include <pythonic/types/slice.hpp>
#include <pythonic/types/str.hpp>
namespace __pythran_solver
{
  struct __transonic__
  {
    typedef void callable;
    typedef void pure;
    struct type
    {
      typedef pythonic::types::str __type0;
      typedef typename pythonic::returnable<decltype(pythonic::types::make_tuple(std::declval<__type0>()))>::type result_type;
    }  ;
    typename type::result_type operator()() const;
    ;
  }  ;
  struct compute_fb_fft
  {
    typedef void callable;
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type0;
      typedef typename pythonic::assignable<typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type>::type __type1;
      typedef decltype(pythonic::operator_::neg(std::declval<__type0>())) __type2;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::square{})>::type>::type __type3;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type4;
      typedef decltype(std::declval<__type3>()(std::declval<__type4>())) __type5;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type6;
      typedef decltype(pythonic::operator_::mul(std::declval<__type5>(), std::declval<__type6>())) __type7;
      typedef decltype(pythonic::operator_::sub(std::declval<__type2>(), std::declval<__type7>())) __type8;
      typedef __type0 __ptype0;
      typedef typename pythonic::returnable<typename __combined<__type1,__type8>::type>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
    typename type<argument_type0, argument_type1, argument_type2>::result_type operator()(argument_type0&& div_vb_fft, argument_type1&& N, argument_type2&& vz_fft) const
    ;
  }  ;
  typename __transonic__::type::result_type __transonic__::operator()() const
  {
    {
      static typename __transonic__::type::result_type tmp_global = pythonic::types::make_tuple(pythonic::types::str("0.4.7"));
      return tmp_global;
    }
  }
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
  typename compute_fb_fft::type<argument_type0, argument_type1, argument_type2>::result_type compute_fb_fft::operator()(argument_type0&& div_vb_fft, argument_type1&& N, argument_type2&& vz_fft) const
  {
    typedef typename pythonic::assignable<typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type>::type __type0;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type1;
    typedef decltype(pythonic::operator_::neg(std::declval<__type1>())) __type2;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::square{})>::type>::type __type3;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type4;
    typedef decltype(std::declval<__type3>()(std::declval<__type4>())) __type5;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type6;
    typedef decltype(pythonic::operator_::mul(std::declval<__type5>(), std::declval<__type6>())) __type7;
    typedef decltype(pythonic::operator_::sub(std::declval<__type2>(), std::declval<__type7>())) __type8;
    typename pythonic::assignable<typename __combined<__type0,__type8>::type>::type fb_fft = div_vb_fft;
    fb_fft[pythonic::types::contiguous_slice(pythonic::builtins::None,pythonic::builtins::None)] = pythonic::operator_::sub(pythonic::operator_::neg(div_vb_fft), pythonic::operator_::mul(pythonic::numpy::functor::square{}(N), vz_fft));
    return fb_fft;
  }
}
#include <pythonic/python/exception_handler.hpp>
#ifdef ENABLE_PYTHON_MODULE
static PyObject* __transonic__ = to_python(__pythran_solver::__transonic__()());
typename __pythran_solver::compute_fb_fft::type<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>, double, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>::result_type compute_fb_fft0(pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>&& div_vb_fft, double&& N, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>&& vz_fft) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_solver::compute_fb_fft()(div_vb_fft, N, vz_fft);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}

static PyObject *
__pythran_wrap_compute_fb_fft0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    char const* keywords[] = {"div_vb_fft", "N", "vz_fft",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[0]) && is_convertible<double>(args_obj[1]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[2]))
        return to_python(compute_fb_fft0(from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[0]), from_python<double>(args_obj[1]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[2])));
    else {
        return nullptr;
    }
}

            static PyObject *
            __pythran_wrapall_compute_fb_fft(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap_compute_fb_fft0(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "compute_fb_fft", "\n""    - compute_fb_fft(complex128[:,:,:], float64, complex128[:,:,:])", args, kw);
                });
            }


static PyMethodDef Methods[] = {
    {
    "compute_fb_fft",
    (PyCFunction)__pythran_wrapall_compute_fb_fft,
    METH_VARARGS | METH_KEYWORDS,
    "Supported prototypes:\n""\n""    - compute_fb_fft(complex128[:,:,:], float64, complex128[:,:,:])"},
    {NULL, NULL, 0, NULL}
};


#if PY_MAJOR_VERSION >= 3
  static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "solver",            /* m_name */
    "",         /* m_doc */
    -1,                  /* m_size */
    Methods,             /* m_methods */
    NULL,                /* m_reload */
    NULL,                /* m_traverse */
    NULL,                /* m_clear */
    NULL,                /* m_free */
  };
#define PYTHRAN_RETURN return theModule
#define PYTHRAN_MODULE_INIT(s) PyInit_##s
#else
#define PYTHRAN_RETURN return
#define PYTHRAN_MODULE_INIT(s) init##s
#endif
PyMODINIT_FUNC
PYTHRAN_MODULE_INIT(solver)(void)
#ifndef _WIN32
__attribute__ ((visibility("default")))
__attribute__ ((externally_visible))
#endif
;
PyMODINIT_FUNC
PYTHRAN_MODULE_INIT(solver)(void) {
    import_array()
    #if PY_MAJOR_VERSION >= 3
    PyObject* theModule = PyModule_Create(&moduledef);
    #else
    PyObject* theModule = Py_InitModule3("solver",
                                         Methods,
                                         ""
    );
    #endif
    if(! theModule)
        PYTHRAN_RETURN;
    PyObject * theDoc = Py_BuildValue("(sss)",
                                      "0.9.8.post2",
                                      "2021-02-02 13:34:56.225094",
                                      "8572a368c4bb09a0b34a7ac63c0b097bb7675bd4bf9572a73f360b1766b6fdae");
    if(! theDoc)
        PYTHRAN_RETURN;
    PyModule_AddObject(theModule,
                       "__pythran__",
                       theDoc);

    PyModule_AddObject(theModule, "__transonic__", __transonic__);
    PYTHRAN_RETURN;
}

#endif