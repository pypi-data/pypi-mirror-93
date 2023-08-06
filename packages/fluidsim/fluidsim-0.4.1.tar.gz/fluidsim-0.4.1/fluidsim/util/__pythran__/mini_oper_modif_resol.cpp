#include <pythonic/core.hpp>
#include <pythonic/python/core.hpp>
#include <pythonic/types/bool.hpp>
#include <pythonic/types/int.hpp>
#ifdef _OPENMP
#include <omp.h>
#endif
#include <pythonic/include/types/complex128.hpp>
#include <pythonic/include/types/ndarray.hpp>
#include <pythonic/types/ndarray.hpp>
#include <pythonic/types/complex128.hpp>
#include <pythonic/include/builtins/None.hpp>
#include <pythonic/include/builtins/getattr.hpp>
#include <pythonic/include/builtins/min.hpp>
#include <pythonic/include/builtins/pythran/and_.hpp>
#include <pythonic/include/builtins/range.hpp>
#include <pythonic/include/builtins/tuple.hpp>
#include <pythonic/include/operator_/add.hpp>
#include <pythonic/include/operator_/floordiv.hpp>
#include <pythonic/include/operator_/gt.hpp>
#include <pythonic/include/operator_/lt.hpp>
#include <pythonic/include/operator_/neg.hpp>
#include <pythonic/include/types/str.hpp>
#include <pythonic/builtins/None.hpp>
#include <pythonic/builtins/getattr.hpp>
#include <pythonic/builtins/min.hpp>
#include <pythonic/builtins/pythran/and_.hpp>
#include <pythonic/builtins/range.hpp>
#include <pythonic/builtins/tuple.hpp>
#include <pythonic/operator_/add.hpp>
#include <pythonic/operator_/floordiv.hpp>
#include <pythonic/operator_/gt.hpp>
#include <pythonic/operator_/lt.hpp>
#include <pythonic/operator_/neg.hpp>
#include <pythonic/types/str.hpp>
namespace __pythran_mini_oper_modif_resol
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
  struct fill_field_fft_3d
  {
    typedef void callable;
    ;
    template <typename argument_type0 , typename argument_type1 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type0;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type1;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::min{})>::type>::type __type2;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type3;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type3>())) __type4;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type4>::type>::type __type5;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type0>())) __type6;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type6>::type>::type __type7;
      typedef typename pythonic::assignable<decltype(std::declval<__type2>()(std::declval<__type5>(), std::declval<__type7>()))>::type __type8;
      typedef long __type9;
      typedef decltype(pythonic::operator_::functor::floordiv()(std::declval<__type8>(), std::declval<__type9>())) __type10;
      typedef decltype(pythonic::operator_::add(std::declval<__type10>(), std::declval<__type9>())) __type11;
      typedef decltype(std::declval<__type1>()(std::declval<__type11>())) __type12;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type12>::type::iterator>::value_type>::type __type13;
      typedef typename std::tuple_element<1,typename std::remove_reference<__type4>::type>::type __type14;
      typedef typename std::tuple_element<1,typename std::remove_reference<__type6>::type>::type __type15;
      typedef typename pythonic::assignable<decltype(std::declval<__type2>()(std::declval<__type14>(), std::declval<__type15>()))>::type __type16;
      typedef decltype(pythonic::operator_::functor::floordiv()(std::declval<__type16>(), std::declval<__type9>())) __type17;
      typedef decltype(pythonic::operator_::add(std::declval<__type17>(), std::declval<__type9>())) __type18;
      typedef decltype(std::declval<__type1>()(std::declval<__type18>())) __type19;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type19>::type::iterator>::value_type>::type __type20;
      typedef typename std::tuple_element<2,typename std::remove_reference<__type4>::type>::type __type21;
      typedef typename std::tuple_element<2,typename std::remove_reference<__type6>::type>::type __type22;
      typedef decltype(std::declval<__type2>()(std::declval<__type21>(), std::declval<__type22>())) __type23;
      typedef typename pythonic::lazy<__type23>::type __type24;
      typedef decltype(std::declval<__type1>()(std::declval<__type24>())) __type25;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type25>::type::iterator>::value_type>::type __type26;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type13>(), std::declval<__type20>(), std::declval<__type26>())) __type27;
      typedef decltype(std::declval<__type0>()[std::declval<__type27>()]) __type28;
      typedef __type28 __ptype0;
      typedef __type27 __ptype1;
      typedef typename pythonic::returnable<pythonic::types::none_type>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 >
    typename type<argument_type0, argument_type1>::result_type operator()(argument_type0&& field_fft_in, argument_type1&& field_fft_out) const
    ;
  }  ;
  typename __transonic__::type::result_type __transonic__::operator()() const
  {
    {
      static typename __transonic__::type::result_type tmp_global = pythonic::types::make_tuple(pythonic::types::str("0.4.7"));
      return tmp_global;
    }
  }
  template <typename argument_type0 , typename argument_type1 >
  typename fill_field_fft_3d::type<argument_type0, argument_type1>::result_type fill_field_fft_3d::operator()(argument_type0&& field_fft_in, argument_type1&& field_fft_out) const
  {
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type0;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::min{})>::type>::type __type1;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type2;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type2>())) __type3;
    typedef typename std::tuple_element<1,typename std::remove_reference<__type3>::type>::type __type4;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type5;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type5>())) __type6;
    typedef typename std::tuple_element<1,typename std::remove_reference<__type6>::type>::type __type7;
    typedef typename pythonic::assignable<decltype(std::declval<__type1>()(std::declval<__type4>(), std::declval<__type7>()))>::type __type8;
    typedef long __type9;
    typedef decltype(pythonic::operator_::functor::floordiv()(std::declval<__type8>(), std::declval<__type9>())) __type10;
    typedef decltype(pythonic::operator_::add(std::declval<__type10>(), std::declval<__type9>())) __type11;
    typedef decltype(std::declval<__type0>()(std::declval<__type11>())) __type12;
    typedef typename std::tuple_element<2,typename std::remove_reference<__type3>::type>::type __type13;
    typedef typename std::tuple_element<2,typename std::remove_reference<__type6>::type>::type __type14;
    typedef decltype(std::declval<__type1>()(std::declval<__type13>(), std::declval<__type14>())) __type15;
    typedef typename pythonic::lazy<__type15>::type __type16;
    typedef decltype(std::declval<__type0>()(std::declval<__type16>())) __type17;
    typedef typename std::tuple_element<0,typename std::remove_reference<__type3>::type>::type __type18;
    typedef typename std::tuple_element<0,typename std::remove_reference<__type6>::type>::type __type19;
    typedef typename pythonic::assignable<decltype(std::declval<__type1>()(std::declval<__type18>(), std::declval<__type19>()))>::type __type20;
    typedef decltype(pythonic::operator_::functor::floordiv()(std::declval<__type20>(), std::declval<__type9>())) __type21;
    typedef decltype(pythonic::operator_::add(std::declval<__type21>(), std::declval<__type9>())) __type22;
    typedef decltype(std::declval<__type0>()(std::declval<__type22>())) __type23;
    typename pythonic::assignable<typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type12>::type::iterator>::value_type>::type>::type ik1;
    typename pythonic::assignable<typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type17>::type::iterator>::value_type>::type>::type ik2;
    typename pythonic::assignable<typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type23>::type::iterator>::value_type>::type>::type ik0;
    typename pythonic::assignable_noescape<decltype(pythonic::builtins::functor::min{}(std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, field_fft_out)), std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, field_fft_in))))>::type nk0_min = pythonic::builtins::functor::min{}(std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, field_fft_out)), std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, field_fft_in)));
    typename pythonic::assignable_noescape<decltype(pythonic::builtins::functor::min{}(std::get<1>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, field_fft_out)), std::get<1>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, field_fft_in))))>::type nk1_min = pythonic::builtins::functor::min{}(std::get<1>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, field_fft_out)), std::get<1>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, field_fft_in)));
    typename pythonic::lazy<decltype(pythonic::builtins::functor::min{}(std::get<2>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, field_fft_out)), std::get<2>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, field_fft_in))))>::type nk2_min = pythonic::builtins::functor::min{}(std::get<2>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, field_fft_out)), std::get<2>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, field_fft_in)));
    {
      long  __target140423954266816 = pythonic::operator_::add(pythonic::operator_::functor::floordiv()(nk0_min, 2L), 1L);
      for (long  ik0=0L; ik0 < __target140423954266816; ik0 += 1L)
      {
        {
          long  __target140423952905360 = pythonic::operator_::add(pythonic::operator_::functor::floordiv()(nk1_min, 2L), 1L);
          for (long  ik1=0L; ik1 < __target140423952905360; ik1 += 1L)
          {
            {
              long  __target140423952906416 = nk2_min;
              for (long  ik2=0L; ik2 < __target140423952906416; ik2 += 1L)
              {
                field_fft_out.fast(pythonic::types::make_tuple(ik0, ik1, ik2)) = field_fft_in.fast(pythonic::types::make_tuple(ik0, ik1, ik2));
                if (pythonic::builtins::pythran::and_([&] () { return pythonic::operator_::gt(ik0, 0L); }, [&] () { return pythonic::operator_::lt(ik0, pythonic::operator_::functor::floordiv()(nk0_min, 2L)); }))
                {
                  field_fft_out[pythonic::types::make_tuple(pythonic::operator_::neg(ik0), ik1, ik2)] = field_fft_in[pythonic::types::make_tuple(pythonic::operator_::neg(ik0), ik1, ik2)];
                  if (pythonic::builtins::pythran::and_([&] () { return pythonic::operator_::gt(ik1, 0L); }, [&] () { return pythonic::operator_::lt(ik1, pythonic::operator_::functor::floordiv()(nk1_min, 2L)); }))
                  {
                    field_fft_out[pythonic::types::make_tuple(pythonic::operator_::neg(ik0), pythonic::operator_::neg(ik1), ik2)] = field_fft_in[pythonic::types::make_tuple(pythonic::operator_::neg(ik0), pythonic::operator_::neg(ik1), ik2)];
                  }
                }
                if (pythonic::builtins::pythran::and_([&] () { return pythonic::operator_::gt(ik1, 0L); }, [&] () { return pythonic::operator_::lt(ik1, pythonic::operator_::functor::floordiv()(nk1_min, 2L)); }))
                {
                  field_fft_out[pythonic::types::make_tuple(ik0, pythonic::operator_::neg(ik1), ik2)] = field_fft_in[pythonic::types::make_tuple(ik0, pythonic::operator_::neg(ik1), ik2)];
                }
              }
            }
          }
        }
      }
    }
    return pythonic::builtins::None;
  }
}
#include <pythonic/python/exception_handler.hpp>
#ifdef ENABLE_PYTHON_MODULE
static PyObject* __transonic__ = to_python(__pythran_mini_oper_modif_resol::__transonic__()());
typename __pythran_mini_oper_modif_resol::fill_field_fft_3d::type<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>::result_type fill_field_fft_3d0(pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>&& field_fft_in, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>&& field_fft_out) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_mini_oper_modif_resol::fill_field_fft_3d()(field_fft_in, field_fft_out);
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
__pythran_wrap_fill_field_fft_3d0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[2+1];
    char const* keywords[] = {"field_fft_in", "field_fft_out",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OO",
                                     (char**)keywords , &args_obj[0], &args_obj[1]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[1]))
        return to_python(fill_field_fft_3d0(from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[0]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[1])));
    else {
        return nullptr;
    }
}

            static PyObject *
            __pythran_wrapall_fill_field_fft_3d(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap_fill_field_fft_3d0(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "fill_field_fft_3d", "\n""    - fill_field_fft_3d(complex128[:,:,:], complex128[:,:,:])", args, kw);
                });
            }


static PyMethodDef Methods[] = {
    {
    "fill_field_fft_3d",
    (PyCFunction)__pythran_wrapall_fill_field_fft_3d,
    METH_VARARGS | METH_KEYWORDS,
    "Fill the values from field_fft_in in field_fft_out\n""\n""    Supported prototypes:\n""\n""    - fill_field_fft_3d(complex128[:,:,:], complex128[:,:,:])\n""\n""    This function is specialized for FFTW3DReal2Complex (no MPI).\n"""},
    {NULL, NULL, 0, NULL}
};


#if PY_MAJOR_VERSION >= 3
  static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "mini_oper_modif_resol",            /* m_name */
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
PYTHRAN_MODULE_INIT(mini_oper_modif_resol)(void)
#ifndef _WIN32
__attribute__ ((visibility("default")))
__attribute__ ((externally_visible))
#endif
;
PyMODINIT_FUNC
PYTHRAN_MODULE_INIT(mini_oper_modif_resol)(void) {
    import_array()
    #if PY_MAJOR_VERSION >= 3
    PyObject* theModule = PyModule_Create(&moduledef);
    #else
    PyObject* theModule = Py_InitModule3("mini_oper_modif_resol",
                                         Methods,
                                         ""
    );
    #endif
    if(! theModule)
        PYTHRAN_RETURN;
    PyObject * theDoc = Py_BuildValue("(sss)",
                                      "0.9.8.post2",
                                      "2021-02-02 13:34:55.913029",
                                      "dc8eac918a4067f893c2002fe2e3e943fa37c55a0ecb80964437574156596316");
    if(! theDoc)
        PYTHRAN_RETURN;
    PyModule_AddObject(theModule,
                       "__pythran__",
                       theDoc);

    PyModule_AddObject(theModule, "__transonic__", __transonic__);
    PYTHRAN_RETURN;
}

#endif