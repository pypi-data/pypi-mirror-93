#include <pythonic/core.hpp>
#include <pythonic/python/core.hpp>
#include <pythonic/types/bool.hpp>
#include <pythonic/types/int.hpp>
#ifdef _OPENMP
#include <omp.h>
#endif
#include <pythonic/include/types/ndarray.hpp>
#include <pythonic/include/types/float64.hpp>
#include <pythonic/types/float64.hpp>
#include <pythonic/types/ndarray.hpp>
#include <pythonic/include/builtins/tuple.hpp>
#include <pythonic/include/operator_/mul.hpp>
#include <pythonic/include/operator_/sub.hpp>
#include <pythonic/include/types/slice.hpp>
#include <pythonic/include/types/str.hpp>
#include <pythonic/builtins/tuple.hpp>
#include <pythonic/operator_/mul.hpp>
#include <pythonic/operator_/sub.hpp>
#include <pythonic/types/slice.hpp>
#include <pythonic/types/str.hpp>
namespace __pythran_forcing
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
  struct compute_watu_coriolis_forcing_component
  {
    typedef void callable;
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 , typename argument_type5 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type0;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type1;
      typedef decltype(pythonic::operator_::mul(std::declval<__type0>(), std::declval<__type1>())) __type2;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type3;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type3>::type>::type __type4;
      typedef decltype(pythonic::operator_::mul(std::declval<__type3>(), std::declval<__type4>())) __type5;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type4>::type>::type __type6;
      typedef decltype(pythonic::operator_::sub(std::declval<__type5>(), std::declval<__type6>())) __type7;
      typedef decltype(pythonic::operator_::mul(std::declval<__type2>(), std::declval<__type7>())) __type8;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type5>::type>::type __type9;
      typedef __type8 __ptype0;
      typedef typename pythonic::returnable<typename __combined<__type9,__type8>::type>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 , typename argument_type5 >
    typename type<argument_type0, argument_type1, argument_type2, argument_type3, argument_type4, argument_type5>::result_type operator()(argument_type0&& sigma, argument_type1&& mask, argument_type2&& coef_forcing_time, argument_type3&& target, argument_type4&& velocity, argument_type5&& out) const
    ;
  }  ;
  typename __transonic__::type::result_type __transonic__::operator()() const
  {
    {
      static typename __transonic__::type::result_type tmp_global = pythonic::types::make_tuple(pythonic::types::str("0.4.7"));
      return tmp_global;
    }
  }
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 , typename argument_type5 >
  typename compute_watu_coriolis_forcing_component::type<argument_type0, argument_type1, argument_type2, argument_type3, argument_type4, argument_type5>::result_type compute_watu_coriolis_forcing_component::operator()(argument_type0&& sigma, argument_type1&& mask, argument_type2&& coef_forcing_time, argument_type3&& target, argument_type4&& velocity, argument_type5&& out) const
  {
    out[pythonic::types::contiguous_slice(pythonic::builtins::None,pythonic::builtins::None)] = pythonic::operator_::mul(pythonic::operator_::mul(sigma, mask), pythonic::operator_::sub(pythonic::operator_::mul(coef_forcing_time, target), velocity));
    return out;
  }
}
#include <pythonic/python/exception_handler.hpp>
#ifdef ENABLE_PYTHON_MODULE
static PyObject* __transonic__ = to_python(__pythran_forcing::__transonic__()());
typename __pythran_forcing::compute_watu_coriolis_forcing_component::type<double, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>, double, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>::result_type compute_watu_coriolis_forcing_component0(double&& sigma, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>&& mask, double&& coef_forcing_time, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>&& target, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>&& velocity, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>&& out) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_forcing::compute_watu_coriolis_forcing_component()(sigma, mask, coef_forcing_time, target, velocity, out);
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
__pythran_wrap_compute_watu_coriolis_forcing_component0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[6+1];
    char const* keywords[] = {"sigma", "mask", "coef_forcing_time", "target", "velocity", "out",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4], &args_obj[5]))
        return nullptr;
    if(is_convertible<double>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[1]) && is_convertible<double>(args_obj[2]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[3]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[4]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[5]))
        return to_python(compute_watu_coriolis_forcing_component0(from_python<double>(args_obj[0]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[1]), from_python<double>(args_obj[2]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[3]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[4]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[5])));
    else {
        return nullptr;
    }
}

            static PyObject *
            __pythran_wrapall_compute_watu_coriolis_forcing_component(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap_compute_watu_coriolis_forcing_component0(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "compute_watu_coriolis_forcing_component", "\n""    - compute_watu_coriolis_forcing_component(float64, float64[:,:,:], float64, float64[:,:,:], float64[:,:,:], float64[:,:,:])", args, kw);
                });
            }


static PyMethodDef Methods[] = {
    {
    "compute_watu_coriolis_forcing_component",
    (PyCFunction)__pythran_wrapall_compute_watu_coriolis_forcing_component,
    METH_VARARGS | METH_KEYWORDS,
    "Supported prototypes:\n""\n""    - compute_watu_coriolis_forcing_component(float64, float64[:,:,:], float64, float64[:,:,:], float64[:,:,:], float64[:,:,:])"},
    {NULL, NULL, 0, NULL}
};


#if PY_MAJOR_VERSION >= 3
  static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "forcing",            /* m_name */
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
PYTHRAN_MODULE_INIT(forcing)(void)
#ifndef _WIN32
__attribute__ ((visibility("default")))
__attribute__ ((externally_visible))
#endif
;
PyMODINIT_FUNC
PYTHRAN_MODULE_INIT(forcing)(void) {
    import_array()
    #if PY_MAJOR_VERSION >= 3
    PyObject* theModule = PyModule_Create(&moduledef);
    #else
    PyObject* theModule = Py_InitModule3("forcing",
                                         Methods,
                                         ""
    );
    #endif
    if(! theModule)
        PYTHRAN_RETURN;
    PyObject * theDoc = Py_BuildValue("(sss)",
                                      "0.9.8.post2",
                                      "2021-02-02 13:34:56.123187",
                                      "e8dae1d4bfc21588c5ad551edcee29de29ea99a00f6f0bf52d79ae2394951dec");
    if(! theDoc)
        PYTHRAN_RETURN;
    PyModule_AddObject(theModule,
                       "__pythran__",
                       theDoc);

    PyModule_AddObject(theModule, "__transonic__", __transonic__);
    PYTHRAN_RETURN;
}

#endif