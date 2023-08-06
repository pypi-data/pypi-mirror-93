#include <pythonic/core.hpp>
#include <pythonic/python/core.hpp>
#include <pythonic/types/bool.hpp>
#include <pythonic/types/int.hpp>
#ifdef _OPENMP
#include <omp.h>
#endif
#include <pythonic/include/types/uint8.hpp>
#include <pythonic/include/types/complex128.hpp>
#include <pythonic/include/types/ndarray.hpp>
#include <pythonic/include/types/float64.hpp>
#include <pythonic/types/float64.hpp>
#include <pythonic/types/ndarray.hpp>
#include <pythonic/types/uint8.hpp>
#include <pythonic/types/complex128.hpp>
#include <pythonic/include/builtins/None.hpp>
#include <pythonic/include/builtins/getattr.hpp>
#include <pythonic/include/builtins/map.hpp>
#include <pythonic/include/builtins/pythran/abssqr.hpp>
#include <pythonic/include/builtins/range.hpp>
#include <pythonic/include/builtins/tuple.hpp>
#include <pythonic/include/numpy/square.hpp>
#include <pythonic/include/operator_/add.hpp>
#include <pythonic/include/operator_/div.hpp>
#include <pythonic/include/operator_/eq.hpp>
#include <pythonic/include/operator_/lt.hpp>
#include <pythonic/include/operator_/mul.hpp>
#include <pythonic/include/operator_/sub.hpp>
#include <pythonic/include/random/uniform.hpp>
#include <pythonic/include/types/complex.hpp>
#include <pythonic/include/types/str.hpp>
#include <pythonic/builtins/None.hpp>
#include <pythonic/builtins/getattr.hpp>
#include <pythonic/builtins/map.hpp>
#include <pythonic/builtins/pythran/abssqr.hpp>
#include <pythonic/builtins/range.hpp>
#include <pythonic/builtins/tuple.hpp>
#include <pythonic/numpy/square.hpp>
#include <pythonic/operator_/add.hpp>
#include <pythonic/operator_/div.hpp>
#include <pythonic/operator_/eq.hpp>
#include <pythonic/operator_/lt.hpp>
#include <pythonic/operator_/mul.hpp>
#include <pythonic/operator_/sub.hpp>
#include <pythonic/random/uniform.hpp>
#include <pythonic/types/complex.hpp>
#include <pythonic/types/str.hpp>
namespace __pythran_operators3d
{
  struct __for_method__OperatorsPseudoSpectral3D__get_phases_random_lambda0
  {
    typedef void callable;
    ;
    template <typename argument_type0 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::random::functor::uniform{})>::type>::type __type0;
      typedef double __type1;
      typedef typename pythonic::returnable<decltype(std::declval<__type0>()(std::declval<__type1>(), std::declval<__type1>()))>::type result_type;
    }  
    ;
    template <typename argument_type0 >
    typename type<argument_type0>::result_type operator()(argument_type0&& _) const
    ;
  }  ;
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
  struct __code_new_method__OperatorsPseudoSpectral3D__get_phases_random
  {
    typedef void callable;
    typedef void pure;
    struct type
    {
      typedef typename pythonic::returnable<pythonic::types::str>::type result_type;
    }  ;
    typename type::result_type operator()() const;
    ;
  }  ;
  struct __code_new_method__OperatorsPseudoSpectral3D__vxvyfft_from_rotzfft
  {
    typedef void callable;
    typedef void pure;
    struct type
    {
      typedef typename pythonic::returnable<pythonic::types::str>::type result_type;
    }  ;
    typename type::result_type operator()() const;
    ;
  }  ;
  struct __for_method__OperatorsPseudoSpectral3D__vxvyfft_from_rotzfft
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
    struct type
    {
      typedef std::complex<double> __type0;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type1;
      typedef decltype(pythonic::operator_::mul(std::declval<__type0>(), std::declval<__type1>())) __type2;
      typedef long __type3;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::square{})>::type>::type __type4;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type5;
      typedef decltype(std::declval<__type4>()(std::declval<__type5>())) __type6;
      typedef decltype(std::declval<__type4>()(std::declval<__type1>())) __type7;
      typedef typename pythonic::assignable<decltype(pythonic::operator_::add(std::declval<__type6>(), std::declval<__type7>()))>::type __type8;
      typedef double __type9;
      typedef container<typename std::remove_reference<__type9>::type> __type10;
      typedef typename __combined<__type8,__type10>::type __type11;
      typedef decltype(pythonic::operator_::eq(std::declval<__type11>(), std::declval<__type3>())) __type12;
      typedef indexable<__type12> __type13;
      typedef typename __combined<__type8,__type13>::type __type14;
      typedef typename __combined<__type14,__type10>::type __type15;
      typedef typename pythonic::assignable<decltype(pythonic::operator_::div(std::declval<__type3>(), std::declval<__type15>()))>::type __type16;
      typedef decltype(pythonic::operator_::mul(std::declval<__type2>(), std::declval<__type16>())) __type17;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type18;
      typedef decltype(pythonic::operator_::mul(std::declval<__type17>(), std::declval<__type18>())) __type19;
      typedef decltype(pythonic::operator_::mul(std::declval<__type0>(), std::declval<__type5>())) __type20;
      typedef decltype(pythonic::operator_::mul(std::declval<__type20>(), std::declval<__type16>())) __type21;
      typedef decltype(pythonic::operator_::mul(std::declval<__type21>(), std::declval<__type18>())) __type22;
      typedef typename pythonic::returnable<decltype(pythonic::types::make_tuple(std::declval<__type19>(), std::declval<__type22>()))>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
    typename type<argument_type0, argument_type1, argument_type2>::result_type operator()(argument_type0&& self_Kx, argument_type1&& self_Ky, argument_type2&& rotz_fft) const
    ;
  }  ;
  struct __code_new_method__OperatorsPseudoSpectral3D__divhfft_from_vxvyfft
  {
    typedef void callable;
    typedef void pure;
    struct type
    {
      typedef typename pythonic::returnable<pythonic::types::str>::type result_type;
    }  ;
    typename type::result_type operator()() const;
    ;
  }  ;
  struct __for_method__OperatorsPseudoSpectral3D__divhfft_from_vxvyfft
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 >
    struct type
    {
      typedef std::complex<double> __type0;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type1;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type2;
      typedef decltype(pythonic::operator_::mul(std::declval<__type1>(), std::declval<__type2>())) __type3;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type4;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type3>::type>::type __type5;
      typedef decltype(pythonic::operator_::mul(std::declval<__type4>(), std::declval<__type5>())) __type6;
      typedef decltype(pythonic::operator_::add(std::declval<__type3>(), std::declval<__type6>())) __type7;
      typedef typename pythonic::returnable<decltype(pythonic::operator_::mul(std::declval<__type0>(), std::declval<__type7>()))>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 >
    typename type<argument_type0, argument_type1, argument_type2, argument_type3>::result_type operator()(argument_type0&& self_Kx, argument_type1&& self_Ky, argument_type2&& vx_fft, argument_type3&& vy_fft) const
    ;
  }  ;
  struct __code_new_method__OperatorsPseudoSpectral3D__urudfft_from_vxvyfft
  {
    typedef void callable;
    typedef void pure;
    struct type
    {
      typedef typename pythonic::returnable<pythonic::types::str>::type result_type;
    }  ;
    typename type::result_type operator()() const;
    ;
  }  ;
  struct __for_method__OperatorsPseudoSpectral3D__urudfft_from_vxvyfft
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type0;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type1;
      typedef decltype(pythonic::operator_::mul(std::declval<__type1>(), std::declval<__type0>())) __type2;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type3;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type3>::type>::type __type4;
      typedef decltype(pythonic::operator_::mul(std::declval<__type3>(), std::declval<__type4>())) __type5;
      typedef typename pythonic::assignable<decltype(pythonic::operator_::add(std::declval<__type2>(), std::declval<__type5>()))>::type __type6;
      typedef decltype(pythonic::operator_::mul(std::declval<__type6>(), std::declval<__type1>())) __type7;
      typedef long __type8;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::square{})>::type>::type __type9;
      typedef decltype(std::declval<__type9>()(std::declval<__type1>())) __type10;
      typedef decltype(std::declval<__type9>()(std::declval<__type3>())) __type11;
      typedef typename pythonic::assignable<decltype(pythonic::operator_::add(std::declval<__type10>(), std::declval<__type11>()))>::type __type12;
      typedef double __type13;
      typedef container<typename std::remove_reference<__type13>::type> __type14;
      typedef typename __combined<__type12,__type14>::type __type15;
      typedef decltype(pythonic::operator_::eq(std::declval<__type15>(), std::declval<__type8>())) __type16;
      typedef indexable<__type16> __type17;
      typedef typename __combined<__type12,__type17>::type __type18;
      typedef typename __combined<__type18,__type14>::type __type19;
      typedef typename pythonic::assignable<decltype(pythonic::operator_::div(std::declval<__type8>(), std::declval<__type19>()))>::type __type20;
      typedef typename pythonic::assignable<decltype(pythonic::operator_::mul(std::declval<__type7>(), std::declval<__type20>()))>::type __type21;
      typedef decltype(pythonic::operator_::sub(std::declval<__type0>(), std::declval<__type21>())) __type22;
      typedef decltype(pythonic::operator_::mul(std::declval<__type6>(), std::declval<__type3>())) __type23;
      typedef typename pythonic::assignable<decltype(pythonic::operator_::mul(std::declval<__type23>(), std::declval<__type20>()))>::type __type24;
      typedef decltype(pythonic::operator_::sub(std::declval<__type4>(), std::declval<__type24>())) __type25;
      typedef typename pythonic::returnable<decltype(pythonic::types::make_tuple(std::declval<__type22>(), std::declval<__type25>(), std::declval<__type21>(), std::declval<__type24>()))>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 >
    typename type<argument_type0, argument_type1, argument_type2, argument_type3>::result_type operator()(argument_type0&& self_Kx, argument_type1&& self_Ky, argument_type2&& vx_fft, argument_type3&& vy_fft) const
    ;
  }  ;
  struct compute_energy_from_3fields
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
    struct type
    {
      typedef double __type0;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::pythran::functor::abssqr{})>::type>::type __type1;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type2;
      typedef decltype(std::declval<__type1>()(std::declval<__type2>())) __type3;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type4;
      typedef decltype(std::declval<__type1>()(std::declval<__type4>())) __type5;
      typedef decltype(pythonic::operator_::add(std::declval<__type3>(), std::declval<__type5>())) __type6;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type7;
      typedef decltype(std::declval<__type1>()(std::declval<__type7>())) __type8;
      typedef decltype(pythonic::operator_::add(std::declval<__type6>(), std::declval<__type8>())) __type9;
      typedef typename pythonic::returnable<decltype(pythonic::operator_::mul(std::declval<__type0>(), std::declval<__type9>()))>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
    typename type<argument_type0, argument_type1, argument_type2>::result_type operator()(argument_type0&& vx, argument_type1&& vy, argument_type2&& vz) const
    ;
  }  ;
  struct compute_energy_from_2fields
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 >
    struct type
    {
      typedef double __type0;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::pythran::functor::abssqr{})>::type>::type __type1;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type2;
      typedef decltype(std::declval<__type1>()(std::declval<__type2>())) __type3;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type4;
      typedef decltype(std::declval<__type1>()(std::declval<__type4>())) __type5;
      typedef decltype(pythonic::operator_::add(std::declval<__type3>(), std::declval<__type5>())) __type6;
      typedef typename pythonic::returnable<decltype(pythonic::operator_::mul(std::declval<__type0>(), std::declval<__type6>()))>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 >
    typename type<argument_type0, argument_type1>::result_type operator()(argument_type0&& vx, argument_type1&& vy) const
    ;
  }  ;
  struct compute_energy_from_1field_with_coef
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 >
    struct type
    {
      typedef double __type0;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type1;
      typedef decltype(pythonic::operator_::mul(std::declval<__type0>(), std::declval<__type1>())) __type2;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::pythran::functor::abssqr{})>::type>::type __type3;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type4;
      typedef decltype(std::declval<__type3>()(std::declval<__type4>())) __type5;
      typedef typename pythonic::returnable<decltype(pythonic::operator_::mul(std::declval<__type2>(), std::declval<__type5>()))>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 >
    typename type<argument_type0, argument_type1>::result_type operator()(argument_type0&& arr, argument_type1&& coef) const
    ;
  }  ;
  struct compute_energy_from_1field
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 >
    struct type
    {
      typedef double __type0;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::pythran::functor::abssqr{})>::type>::type __type1;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type2;
      typedef decltype(std::declval<__type1>()(std::declval<__type2>())) __type3;
      typedef typename pythonic::returnable<decltype(pythonic::operator_::mul(std::declval<__type0>(), std::declval<__type3>()))>::type result_type;
    }  
    ;
    template <typename argument_type0 >
    typename type<argument_type0>::result_type operator()(argument_type0&& arr) const
    ;
  }  ;
  struct dealiasing_variable
  {
    typedef void callable;
    ;
    template <typename argument_type0 , typename argument_type1 >
    struct type
    {
      typedef double __type0;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type1;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type2;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type2>())) __type3;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type3>::type>::type __type4;
      typedef typename pythonic::lazy<__type4>::type __type5;
      typedef decltype(std::declval<__type1>()(std::declval<__type5>())) __type6;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type6>::type::iterator>::value_type>::type __type7;
      typedef typename std::tuple_element<1,typename std::remove_reference<__type3>::type>::type __type8;
      typedef typename pythonic::lazy<__type8>::type __type9;
      typedef decltype(std::declval<__type1>()(std::declval<__type9>())) __type10;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type10>::type::iterator>::value_type>::type __type11;
      typedef typename std::tuple_element<2,typename std::remove_reference<__type3>::type>::type __type12;
      typedef typename pythonic::lazy<__type12>::type __type13;
      typedef decltype(std::declval<__type1>()(std::declval<__type13>())) __type14;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type14>::type::iterator>::value_type>::type __type15;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type7>(), std::declval<__type11>(), std::declval<__type15>())) __type16;
      typedef __type0 __ptype0;
      typedef __type16 __ptype1;
      typedef typename pythonic::returnable<pythonic::types::none_type>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 >
    typename type<argument_type0, argument_type1>::result_type operator()(argument_type0&& ff_fft, argument_type1&& where_dealiased) const
    ;
  }  ;
  struct dealiasing_setofvar
  {
    typedef void callable;
    ;
    template <typename argument_type0 , typename argument_type1 >
    struct type
    {
      typedef double __type0;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type1;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type2;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type2>())) __type3;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type3>::type>::type __type4;
      typedef typename pythonic::lazy<__type4>::type __type5;
      typedef decltype(std::declval<__type1>()(std::declval<__type5>())) __type6;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type6>::type::iterator>::value_type>::type __type7;
      typedef typename std::tuple_element<1,typename std::remove_reference<__type3>::type>::type __type8;
      typedef typename pythonic::lazy<__type8>::type __type9;
      typedef decltype(std::declval<__type1>()(std::declval<__type9>())) __type10;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type10>::type::iterator>::value_type>::type __type11;
      typedef typename std::tuple_element<2,typename std::remove_reference<__type3>::type>::type __type12;
      typedef typename pythonic::lazy<__type12>::type __type13;
      typedef decltype(std::declval<__type1>()(std::declval<__type13>())) __type14;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type14>::type::iterator>::value_type>::type __type15;
      typedef typename std::tuple_element<3,typename std::remove_reference<__type3>::type>::type __type16;
      typedef typename pythonic::lazy<__type16>::type __type17;
      typedef decltype(std::declval<__type1>()(std::declval<__type17>())) __type18;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type18>::type::iterator>::value_type>::type __type19;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type7>(), std::declval<__type11>(), std::declval<__type15>(), std::declval<__type19>())) __type20;
      typedef __type0 __ptype4;
      typedef __type20 __ptype5;
      typedef typename pythonic::returnable<pythonic::types::none_type>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 >
    typename type<argument_type0, argument_type1>::result_type operator()(argument_type0&& sov, argument_type1&& where_dealiased) const
    ;
  }  ;
  struct __for_method__OperatorsPseudoSpectral3D__get_phases_random
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 , typename argument_type5 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::tuple{})>::type>::type __type0;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::map{})>::type>::type __type1;
      typedef __for_method__OperatorsPseudoSpectral3D__get_phases_random_lambda0 __type2;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type3;
      typedef long __type4;
      typedef decltype(std::declval<__type3>()(std::declval<__type4>())) __type5;
      typedef decltype(std::declval<__type1>()(std::declval<__type2>(), std::declval<__type5>())) __type6;
      typedef typename pythonic::assignable<decltype(std::declval<__type0>()(std::declval<__type6>()))>::type __type7;
      typedef typename pythonic::assignable<typename std::tuple_element<0,typename std::remove_reference<__type7>::type>::type>::type __type8;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type3>::type>::type __type9;
      typedef decltype(pythonic::operator_::mul(std::declval<__type8>(), std::declval<__type9>())) __type10;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type11;
      typedef decltype(pythonic::operator_::mul(std::declval<__type10>(), std::declval<__type11>())) __type12;
      typedef typename pythonic::assignable<typename std::tuple_element<1,typename std::remove_reference<__type7>::type>::type>::type __type13;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type4>::type>::type __type14;
      typedef decltype(pythonic::operator_::mul(std::declval<__type13>(), std::declval<__type14>())) __type15;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type16;
      typedef decltype(pythonic::operator_::mul(std::declval<__type15>(), std::declval<__type16>())) __type17;
      typedef decltype(pythonic::operator_::add(std::declval<__type12>(), std::declval<__type17>())) __type18;
      typedef typename pythonic::assignable<typename std::tuple_element<2,typename std::remove_reference<__type7>::type>::type>::type __type19;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type5>::type>::type __type20;
      typedef decltype(pythonic::operator_::mul(std::declval<__type19>(), std::declval<__type20>())) __type21;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type22;
      typedef decltype(pythonic::operator_::mul(std::declval<__type21>(), std::declval<__type22>())) __type23;
      typedef decltype(pythonic::operator_::add(std::declval<__type18>(), std::declval<__type23>())) __type24;
      typedef double __type25;
      typedef decltype(pythonic::operator_::add(std::declval<__type8>(), std::declval<__type25>())) __type26;
      typedef decltype(pythonic::operator_::sub(std::declval<__type8>(), std::declval<__type25>())) __type27;
      typedef typename __combined<__type26,__type27>::type __type28;
      typedef decltype(pythonic::operator_::mul(std::declval<__type28>(), std::declval<__type9>())) __type29;
      typedef decltype(pythonic::operator_::mul(std::declval<__type29>(), std::declval<__type11>())) __type30;
      typedef decltype(pythonic::operator_::add(std::declval<__type13>(), std::declval<__type25>())) __type31;
      typedef decltype(pythonic::operator_::sub(std::declval<__type13>(), std::declval<__type25>())) __type32;
      typedef typename __combined<__type31,__type32>::type __type33;
      typedef decltype(pythonic::operator_::mul(std::declval<__type33>(), std::declval<__type14>())) __type34;
      typedef decltype(pythonic::operator_::mul(std::declval<__type34>(), std::declval<__type16>())) __type35;
      typedef decltype(pythonic::operator_::add(std::declval<__type30>(), std::declval<__type35>())) __type36;
      typedef decltype(pythonic::operator_::add(std::declval<__type19>(), std::declval<__type25>())) __type37;
      typedef decltype(pythonic::operator_::sub(std::declval<__type19>(), std::declval<__type25>())) __type38;
      typedef typename __combined<__type37,__type38>::type __type39;
      typedef decltype(pythonic::operator_::mul(std::declval<__type39>(), std::declval<__type20>())) __type40;
      typedef decltype(pythonic::operator_::mul(std::declval<__type40>(), std::declval<__type22>())) __type41;
      typedef decltype(pythonic::operator_::add(std::declval<__type36>(), std::declval<__type41>())) __type42;
      typedef typename pythonic::returnable<decltype(pythonic::types::make_tuple(std::declval<__type24>(), std::declval<__type42>()))>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 , typename argument_type5 >
    typename type<argument_type0, argument_type1, argument_type2, argument_type3, argument_type4, argument_type5>::result_type operator()(argument_type0&& self_Kx, argument_type1&& self_Ky, argument_type2&& self_Kz, argument_type3&& self_deltax, argument_type4&& self_deltay, argument_type5&& self_deltaz) const
    ;
  }  ;
  template <typename argument_type0 >
  typename __for_method__OperatorsPseudoSpectral3D__get_phases_random_lambda0::type<argument_type0>::result_type __for_method__OperatorsPseudoSpectral3D__get_phases_random_lambda0::operator()(argument_type0&& _) const
  {
    return pythonic::random::functor::uniform{}(-0.5, 0.5);
  }
  typename __transonic__::type::result_type __transonic__::operator()() const
  {
    {
      static typename __transonic__::type::result_type tmp_global = pythonic::types::make_tuple(pythonic::types::str("0.4.7"));
      return tmp_global;
    }
  }
  typename __code_new_method__OperatorsPseudoSpectral3D__get_phases_random::type::result_type __code_new_method__OperatorsPseudoSpectral3D__get_phases_random::operator()() const
  {
    {
      static typename __code_new_method__OperatorsPseudoSpectral3D__get_phases_random::type::result_type tmp_global = pythonic::types::str("\n"
"\n"
"def new_method(self, ):\n"
"    return backend_func(self.Kx, self.Ky, self.Kz, self.deltax, self.deltay, self.deltaz, )\n"
"\n"
"");
      return tmp_global;
    }
  }
  typename __code_new_method__OperatorsPseudoSpectral3D__vxvyfft_from_rotzfft::type::result_type __code_new_method__OperatorsPseudoSpectral3D__vxvyfft_from_rotzfft::operator()() const
  {
    {
      static typename __code_new_method__OperatorsPseudoSpectral3D__vxvyfft_from_rotzfft::type::result_type tmp_global = pythonic::types::str("\n"
"\n"
"def new_method(self, rotz_fft):\n"
"    return backend_func(self.Kx, self.Ky, rotz_fft)\n"
"\n"
"");
      return tmp_global;
    }
  }
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
  typename __for_method__OperatorsPseudoSpectral3D__vxvyfft_from_rotzfft::type<argument_type0, argument_type1, argument_type2>::result_type __for_method__OperatorsPseudoSpectral3D__vxvyfft_from_rotzfft::operator()(argument_type0&& self_Kx, argument_type1&& self_Ky, argument_type2&& rotz_fft) const
  {
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::square{})>::type>::type __type0;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type1;
    typedef decltype(std::declval<__type0>()(std::declval<__type1>())) __type2;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type3;
    typedef decltype(std::declval<__type0>()(std::declval<__type3>())) __type4;
    typedef typename pythonic::assignable<decltype(pythonic::operator_::add(std::declval<__type2>(), std::declval<__type4>()))>::type __type5;
    typedef double __type6;
    typedef container<typename std::remove_reference<__type6>::type> __type7;
    typedef typename __combined<__type5,__type7>::type __type8;
    typedef long __type9;
    typedef decltype(pythonic::operator_::eq(std::declval<__type8>(), std::declval<__type9>())) __type10;
    typedef indexable<__type10> __type11;
    typedef typename __combined<__type5,__type11>::type __type12;
    typedef typename __combined<__type12,__type7>::type __type13;
    typename pythonic::assignable<typename __combined<__type13,__type11>::type>::type inv_Kh_square_nozero = pythonic::operator_::add(pythonic::numpy::functor::square{}(self_Kx), pythonic::numpy::functor::square{}(self_Ky));
    inv_Kh_square_nozero.fast(pythonic::operator_::eq(inv_Kh_square_nozero, 0L)) = 1e-14;
    typename pythonic::assignable<typename pythonic::assignable<decltype(pythonic::operator_::div(std::declval<__type9>(), std::declval<__type13>()))>::type>::type inv_Kh_square_nozero_ = pythonic::operator_::div(1L, inv_Kh_square_nozero);
    return pythonic::types::make_tuple(pythonic::operator_::mul(pythonic::operator_::mul(pythonic::operator_::mul(std::complex<double>(0.0, 1.0), self_Ky), inv_Kh_square_nozero_), rotz_fft), pythonic::operator_::mul(pythonic::operator_::mul(pythonic::operator_::mul(std::complex<double>(-0.0, -1.0), self_Kx), inv_Kh_square_nozero_), rotz_fft));
  }
  typename __code_new_method__OperatorsPseudoSpectral3D__divhfft_from_vxvyfft::type::result_type __code_new_method__OperatorsPseudoSpectral3D__divhfft_from_vxvyfft::operator()() const
  {
    {
      static typename __code_new_method__OperatorsPseudoSpectral3D__divhfft_from_vxvyfft::type::result_type tmp_global = pythonic::types::str("\n"
"\n"
"def new_method(self, vx_fft, vy_fft):\n"
"    return backend_func(self.Kx, self.Ky, vx_fft, vy_fft)\n"
"\n"
"");
      return tmp_global;
    }
  }
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 >
  typename __for_method__OperatorsPseudoSpectral3D__divhfft_from_vxvyfft::type<argument_type0, argument_type1, argument_type2, argument_type3>::result_type __for_method__OperatorsPseudoSpectral3D__divhfft_from_vxvyfft::operator()(argument_type0&& self_Kx, argument_type1&& self_Ky, argument_type2&& vx_fft, argument_type3&& vy_fft) const
  {
    return pythonic::operator_::mul(std::complex<double>(0.0, 1.0), pythonic::operator_::add(pythonic::operator_::mul(self_Kx, vx_fft), pythonic::operator_::mul(self_Ky, vy_fft)));
  }
  typename __code_new_method__OperatorsPseudoSpectral3D__urudfft_from_vxvyfft::type::result_type __code_new_method__OperatorsPseudoSpectral3D__urudfft_from_vxvyfft::operator()() const
  {
    {
      static typename __code_new_method__OperatorsPseudoSpectral3D__urudfft_from_vxvyfft::type::result_type tmp_global = pythonic::types::str("\n"
"\n"
"def new_method(self, vx_fft, vy_fft):\n"
"    return backend_func(self.Kx, self.Ky, vx_fft, vy_fft)\n"
"\n"
"");
      return tmp_global;
    }
  }
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 >
  typename __for_method__OperatorsPseudoSpectral3D__urudfft_from_vxvyfft::type<argument_type0, argument_type1, argument_type2, argument_type3>::result_type __for_method__OperatorsPseudoSpectral3D__urudfft_from_vxvyfft::operator()(argument_type0&& self_Kx, argument_type1&& self_Ky, argument_type2&& vx_fft, argument_type3&& vy_fft) const
  {
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::square{})>::type>::type __type0;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type1;
    typedef decltype(std::declval<__type0>()(std::declval<__type1>())) __type2;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type3;
    typedef decltype(std::declval<__type0>()(std::declval<__type3>())) __type4;
    typedef typename pythonic::assignable<decltype(pythonic::operator_::add(std::declval<__type2>(), std::declval<__type4>()))>::type __type5;
    typedef double __type6;
    typedef container<typename std::remove_reference<__type6>::type> __type7;
    typedef typename __combined<__type5,__type7>::type __type8;
    typedef long __type9;
    typedef decltype(pythonic::operator_::eq(std::declval<__type8>(), std::declval<__type9>())) __type10;
    typedef indexable<__type10> __type11;
    typedef typename __combined<__type5,__type11>::type __type12;
    typedef typename __combined<__type12,__type7>::type __type13;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type14;
    typedef decltype(pythonic::operator_::mul(std::declval<__type1>(), std::declval<__type14>())) __type15;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type3>::type>::type __type16;
    typedef decltype(pythonic::operator_::mul(std::declval<__type3>(), std::declval<__type16>())) __type17;
    typedef typename pythonic::assignable<decltype(pythonic::operator_::add(std::declval<__type15>(), std::declval<__type17>()))>::type __type18;
    typedef decltype(pythonic::operator_::mul(std::declval<__type18>(), std::declval<__type1>())) __type19;
    typedef typename pythonic::assignable<decltype(pythonic::operator_::div(std::declval<__type9>(), std::declval<__type13>()))>::type __type20;
    typedef decltype(pythonic::operator_::mul(std::declval<__type18>(), std::declval<__type3>())) __type21;
    typename pythonic::assignable<typename __combined<__type13,__type11>::type>::type inv_Kh_square_nozero = pythonic::operator_::add(pythonic::numpy::functor::square{}(self_Kx), pythonic::numpy::functor::square{}(self_Ky));
    inv_Kh_square_nozero.fast(pythonic::operator_::eq(inv_Kh_square_nozero, 0L)) = 1e-14;
    typename pythonic::assignable<typename pythonic::assignable<decltype(pythonic::operator_::div(std::declval<__type9>(), std::declval<__type13>()))>::type>::type inv_Kh_square_nozero_ = pythonic::operator_::div(1L, inv_Kh_square_nozero);
    typename pythonic::assignable_noescape<decltype(pythonic::operator_::add(pythonic::operator_::mul(self_Kx, vx_fft), pythonic::operator_::mul(self_Ky, vy_fft)))>::type kdotu_fft = pythonic::operator_::add(pythonic::operator_::mul(self_Kx, vx_fft), pythonic::operator_::mul(self_Ky, vy_fft));
    typename pythonic::assignable<typename pythonic::assignable<decltype(pythonic::operator_::mul(std::declval<__type19>(), std::declval<__type20>()))>::type>::type udx_fft = pythonic::operator_::mul(pythonic::operator_::mul(kdotu_fft, self_Kx), inv_Kh_square_nozero_);
    typename pythonic::assignable<typename pythonic::assignable<decltype(pythonic::operator_::mul(std::declval<__type21>(), std::declval<__type20>()))>::type>::type udy_fft = pythonic::operator_::mul(pythonic::operator_::mul(kdotu_fft, self_Ky), inv_Kh_square_nozero_);
    return pythonic::types::make_tuple(pythonic::operator_::sub(vx_fft, udx_fft), pythonic::operator_::sub(vy_fft, udy_fft), udx_fft, udy_fft);
  }
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
  typename compute_energy_from_3fields::type<argument_type0, argument_type1, argument_type2>::result_type compute_energy_from_3fields::operator()(argument_type0&& vx, argument_type1&& vy, argument_type2&& vz) const
  {
    return pythonic::operator_::mul(0.5, pythonic::operator_::add(pythonic::operator_::add(pythonic::builtins::pythran::functor::abssqr{}(vx), pythonic::builtins::pythran::functor::abssqr{}(vy)), pythonic::builtins::pythran::functor::abssqr{}(vz)));
  }
  template <typename argument_type0 , typename argument_type1 >
  typename compute_energy_from_2fields::type<argument_type0, argument_type1>::result_type compute_energy_from_2fields::operator()(argument_type0&& vx, argument_type1&& vy) const
  {
    return pythonic::operator_::mul(0.5, pythonic::operator_::add(pythonic::builtins::pythran::functor::abssqr{}(vx), pythonic::builtins::pythran::functor::abssqr{}(vy)));
  }
  template <typename argument_type0 , typename argument_type1 >
  typename compute_energy_from_1field_with_coef::type<argument_type0, argument_type1>::result_type compute_energy_from_1field_with_coef::operator()(argument_type0&& arr, argument_type1&& coef) const
  {
    return pythonic::operator_::mul(pythonic::operator_::mul(0.5, coef), pythonic::builtins::pythran::functor::abssqr{}(arr));
  }
  template <typename argument_type0 >
  typename compute_energy_from_1field::type<argument_type0>::result_type compute_energy_from_1field::operator()(argument_type0&& arr) const
  {
    return pythonic::operator_::mul(0.5, pythonic::builtins::pythran::functor::abssqr{}(arr));
  }
  template <typename argument_type0 , typename argument_type1 >
  typename dealiasing_variable::type<argument_type0, argument_type1>::result_type dealiasing_variable::operator()(argument_type0&& ff_fft, argument_type1&& where_dealiased) const
  {
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type0;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type1;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type1>())) __type2;
    typedef typename std::tuple_element<0,typename std::remove_reference<__type2>::type>::type __type3;
    typedef typename pythonic::lazy<__type3>::type __type4;
    typedef decltype(std::declval<__type0>()(std::declval<__type4>())) __type5;
    typedef typename std::tuple_element<2,typename std::remove_reference<__type2>::type>::type __type6;
    typedef typename pythonic::lazy<__type6>::type __type7;
    typedef decltype(std::declval<__type0>()(std::declval<__type7>())) __type8;
    typedef typename std::tuple_element<1,typename std::remove_reference<__type2>::type>::type __type9;
    typedef typename pythonic::lazy<__type9>::type __type10;
    typedef decltype(std::declval<__type0>()(std::declval<__type10>())) __type11;
    typename pythonic::assignable<typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type5>::type::iterator>::value_type>::type>::type i0;
    typename pythonic::assignable<typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type8>::type::iterator>::value_type>::type>::type i2;
    typename pythonic::assignable<typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type11>::type::iterator>::value_type>::type>::type i1;
    typename pythonic::lazy<decltype(std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, ff_fft)))>::type n0 = std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, ff_fft));
    typename pythonic::lazy<decltype(std::get<1>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, ff_fft)))>::type n1 = std::get<1>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, ff_fft));
    typename pythonic::lazy<decltype(std::get<2>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, ff_fft)))>::type n2 = std::get<2>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, ff_fft));
    {
      long  __target140423951287152 = n0;
      for (long  i0=0L; i0 < __target140423951287152; i0 += 1L)
      {
        {
          long  __target140423951324304 = n1;
          for (long  i1=0L; i1 < __target140423951324304; i1 += 1L)
          {
            {
              long  __target140423951325024 = n2;
              for (long  i2=0L; i2 < __target140423951325024; i2 += 1L)
              {
                if (where_dealiased.fast(pythonic::types::make_tuple(i0, i1, i2)))
                {
                  ff_fft.fast(pythonic::types::make_tuple(i0, i1, i2)) = 0.0;
                }
              }
            }
          }
        }
      }
    }
    return pythonic::builtins::None;
  }
  template <typename argument_type0 , typename argument_type1 >
  typename dealiasing_setofvar::type<argument_type0, argument_type1>::result_type dealiasing_setofvar::operator()(argument_type0&& sov, argument_type1&& where_dealiased) const
  {
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type0;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type1;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type1>())) __type2;
    typedef typename std::tuple_element<1,typename std::remove_reference<__type2>::type>::type __type3;
    typedef typename pythonic::lazy<__type3>::type __type4;
    typedef decltype(std::declval<__type0>()(std::declval<__type4>())) __type5;
    typedef typename std::tuple_element<3,typename std::remove_reference<__type2>::type>::type __type6;
    typedef typename pythonic::lazy<__type6>::type __type7;
    typedef decltype(std::declval<__type0>()(std::declval<__type7>())) __type8;
    typedef typename std::tuple_element<0,typename std::remove_reference<__type2>::type>::type __type9;
    typedef typename pythonic::lazy<__type9>::type __type10;
    typedef decltype(std::declval<__type0>()(std::declval<__type10>())) __type11;
    typedef typename std::tuple_element<2,typename std::remove_reference<__type2>::type>::type __type12;
    typedef typename pythonic::lazy<__type12>::type __type13;
    typedef decltype(std::declval<__type0>()(std::declval<__type13>())) __type14;
    typename pythonic::assignable<typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type5>::type::iterator>::value_type>::type>::type i0;
    typename pythonic::assignable<typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type8>::type::iterator>::value_type>::type>::type i2;
    typename pythonic::assignable<typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type11>::type::iterator>::value_type>::type>::type ik;
    typename pythonic::assignable<typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type14>::type::iterator>::value_type>::type>::type i1;
    typename pythonic::lazy<decltype(std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, sov)))>::type nk = std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, sov));
    typename pythonic::lazy<decltype(std::get<1>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, sov)))>::type n0 = std::get<1>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, sov));
    typename pythonic::lazy<decltype(std::get<2>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, sov)))>::type n1 = std::get<2>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, sov));
    typename pythonic::lazy<decltype(std::get<3>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, sov)))>::type n2 = std::get<3>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, sov));
    {
      long  __target140423951321120 = n0;
      for (long  i0=0L; i0 < __target140423951321120; i0 += 1L)
      {
        {
          long  __target140423951322752 = n1;
          for (long  i1=0L; i1 < __target140423951322752; i1 += 1L)
          {
            {
              long  __target140423951286672 = n2;
              for (long  i2=0L; i2 < __target140423951286672; i2 += 1L)
              {
                if (where_dealiased.fast(pythonic::types::make_tuple(i0, i1, i2)))
                {
                  {
                    long  __target140423951288112 = nk;
                    for (long  ik=0L; ik < __target140423951288112; ik += 1L)
                    {
                      sov.fast(pythonic::types::make_tuple(ik, i0, i1, i2)) = 0.0;
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
    return pythonic::builtins::None;
  }
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 , typename argument_type5 >
  typename __for_method__OperatorsPseudoSpectral3D__get_phases_random::type<argument_type0, argument_type1, argument_type2, argument_type3, argument_type4, argument_type5>::result_type __for_method__OperatorsPseudoSpectral3D__get_phases_random::operator()(argument_type0&& self_Kx, argument_type1&& self_Ky, argument_type2&& self_Kz, argument_type3&& self_deltax, argument_type4&& self_deltay, argument_type5&& self_deltaz) const
  {
    typename pythonic::assignable_noescape<decltype(pythonic::builtins::functor::tuple{}(pythonic::builtins::functor::map{}(__for_method__OperatorsPseudoSpectral3D__get_phases_random_lambda0(), pythonic::builtins::functor::range{}(3L))))>::type __tuple0 = pythonic::builtins::functor::tuple{}(pythonic::builtins::functor::map{}(__for_method__OperatorsPseudoSpectral3D__get_phases_random_lambda0(), pythonic::builtins::functor::range{}(3L)));
    typename pythonic::assignable_noescape<decltype(std::get<0>(__tuple0))>::type alpha_x = std::get<0>(__tuple0);
    typename pythonic::assignable_noescape<decltype(std::get<1>(__tuple0))>::type alpha_y = std::get<1>(__tuple0);
    typename pythonic::assignable_noescape<decltype(std::get<2>(__tuple0))>::type alpha_z = std::get<2>(__tuple0);
    return pythonic::types::make_tuple(pythonic::operator_::add(pythonic::operator_::add(pythonic::operator_::mul(pythonic::operator_::mul(alpha_x, self_deltax), self_Kx), pythonic::operator_::mul(pythonic::operator_::mul(alpha_y, self_deltay), self_Ky)), pythonic::operator_::mul(pythonic::operator_::mul(alpha_z, self_deltaz), self_Kz)), pythonic::operator_::add(pythonic::operator_::add(pythonic::operator_::mul(pythonic::operator_::mul((((bool)pythonic::operator_::lt(alpha_x, 0L)) ? typename __combined<decltype(pythonic::operator_::add(alpha_x, 0.5)), decltype(pythonic::operator_::sub(alpha_x, 0.5))>::type(pythonic::operator_::add(alpha_x, 0.5)) : typename __combined<decltype(pythonic::operator_::add(alpha_x, 0.5)), decltype(pythonic::operator_::sub(alpha_x, 0.5))>::type(pythonic::operator_::sub(alpha_x, 0.5))), self_deltax), self_Kx), pythonic::operator_::mul(pythonic::operator_::mul((((bool)pythonic::operator_::lt(alpha_y, 0L)) ? typename __combined<decltype(pythonic::operator_::add(alpha_y, 0.5)), decltype(pythonic::operator_::sub(alpha_y, 0.5))>::type(pythonic::operator_::add(alpha_y, 0.5)) : typename __combined<decltype(pythonic::operator_::add(alpha_y, 0.5)), decltype(pythonic::operator_::sub(alpha_y, 0.5))>::type(pythonic::operator_::sub(alpha_y, 0.5))), self_deltay), self_Ky)), pythonic::operator_::mul(pythonic::operator_::mul((((bool)pythonic::operator_::lt(alpha_z, 0L)) ? typename __combined<decltype(pythonic::operator_::add(alpha_z, 0.5)), decltype(pythonic::operator_::sub(alpha_z, 0.5))>::type(pythonic::operator_::add(alpha_z, 0.5)) : typename __combined<decltype(pythonic::operator_::add(alpha_z, 0.5)), decltype(pythonic::operator_::sub(alpha_z, 0.5))>::type(pythonic::operator_::sub(alpha_z, 0.5))), self_deltaz), self_Kz)));
  }
}
#include <pythonic/python/exception_handler.hpp>
#ifdef ENABLE_PYTHON_MODULE
static PyObject* __transonic__ = to_python(__pythran_operators3d::__transonic__()());
static PyObject* __code_new_method__OperatorsPseudoSpectral3D__get_phases_random = to_python(__pythran_operators3d::__code_new_method__OperatorsPseudoSpectral3D__get_phases_random()());
typename __pythran_operators3d::__for_method__OperatorsPseudoSpectral3D__get_phases_random::type<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>, double, double, double>::result_type __for_method__OperatorsPseudoSpectral3D__get_phases_random0(pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>&& self_Kx, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>&& self_Ky, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>&& self_Kz, double&& self_deltax, double&& self_deltay, double&& self_deltaz) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_operators3d::__for_method__OperatorsPseudoSpectral3D__get_phases_random()(self_Kx, self_Ky, self_Kz, self_deltax, self_deltay, self_deltaz);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
static PyObject* __code_new_method__OperatorsPseudoSpectral3D__vxvyfft_from_rotzfft = to_python(__pythran_operators3d::__code_new_method__OperatorsPseudoSpectral3D__vxvyfft_from_rotzfft()());
typename __pythran_operators3d::__for_method__OperatorsPseudoSpectral3D__vxvyfft_from_rotzfft::type<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>::result_type __for_method__OperatorsPseudoSpectral3D__vxvyfft_from_rotzfft0(pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>&& self_Kx, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>&& self_Ky, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>&& rotz_fft) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_operators3d::__for_method__OperatorsPseudoSpectral3D__vxvyfft_from_rotzfft()(self_Kx, self_Ky, rotz_fft);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
static PyObject* __code_new_method__OperatorsPseudoSpectral3D__divhfft_from_vxvyfft = to_python(__pythran_operators3d::__code_new_method__OperatorsPseudoSpectral3D__divhfft_from_vxvyfft()());
typename __pythran_operators3d::__for_method__OperatorsPseudoSpectral3D__divhfft_from_vxvyfft::type<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>::result_type __for_method__OperatorsPseudoSpectral3D__divhfft_from_vxvyfft0(pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>&& self_Kx, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>&& self_Ky, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>&& vx_fft, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>&& vy_fft) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_operators3d::__for_method__OperatorsPseudoSpectral3D__divhfft_from_vxvyfft()(self_Kx, self_Ky, vx_fft, vy_fft);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
static PyObject* __code_new_method__OperatorsPseudoSpectral3D__urudfft_from_vxvyfft = to_python(__pythran_operators3d::__code_new_method__OperatorsPseudoSpectral3D__urudfft_from_vxvyfft()());
typename __pythran_operators3d::__for_method__OperatorsPseudoSpectral3D__urudfft_from_vxvyfft::type<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>::result_type __for_method__OperatorsPseudoSpectral3D__urudfft_from_vxvyfft0(pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>&& self_Kx, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>&& self_Ky, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>&& vx_fft, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>&& vy_fft) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_operators3d::__for_method__OperatorsPseudoSpectral3D__urudfft_from_vxvyfft()(self_Kx, self_Ky, vx_fft, vy_fft);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_operators3d::compute_energy_from_3fields::type<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>::result_type compute_energy_from_3fields0(pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>&& vx, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>&& vy, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>&& vz) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_operators3d::compute_energy_from_3fields()(vx, vy, vz);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_operators3d::compute_energy_from_2fields::type<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>::result_type compute_energy_from_2fields0(pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>&& vx, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>&& vy) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_operators3d::compute_energy_from_2fields()(vx, vy);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_operators3d::compute_energy_from_1field_with_coef::type<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>, double>::result_type compute_energy_from_1field_with_coef0(pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>&& arr, double&& coef) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_operators3d::compute_energy_from_1field_with_coef()(arr, coef);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_operators3d::compute_energy_from_1field::type<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>::result_type compute_energy_from_1field0(pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>&& arr) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_operators3d::compute_energy_from_1field()(arr);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_operators3d::dealiasing_variable::type<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<npy_uint8,pythonic::types::pshape<long,long,long>>>::result_type dealiasing_variable0(pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>&& ff_fft, pythonic::types::ndarray<npy_uint8,pythonic::types::pshape<long,long,long>>&& where_dealiased) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_operators3d::dealiasing_variable()(ff_fft, where_dealiased);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_operators3d::dealiasing_setofvar::type<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long,long>>, pythonic::types::ndarray<npy_uint8,pythonic::types::pshape<long,long,long>>>::result_type dealiasing_setofvar0(pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long,long>>&& sov, pythonic::types::ndarray<npy_uint8,pythonic::types::pshape<long,long,long>>&& where_dealiased) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_operators3d::dealiasing_setofvar()(sov, where_dealiased);
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
__pythran_wrap___for_method__OperatorsPseudoSpectral3D__get_phases_random0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[6+1];
    char const* keywords[] = {"self_Kx", "self_Ky", "self_Kz", "self_deltax", "self_deltay", "self_deltaz",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4], &args_obj[5]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[2]) && is_convertible<double>(args_obj[3]) && is_convertible<double>(args_obj[4]) && is_convertible<double>(args_obj[5]))
        return to_python(__for_method__OperatorsPseudoSpectral3D__get_phases_random0(from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[0]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[1]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[2]), from_python<double>(args_obj[3]), from_python<double>(args_obj[4]), from_python<double>(args_obj[5])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap___for_method__OperatorsPseudoSpectral3D__vxvyfft_from_rotzfft0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    char const* keywords[] = {"self_Kx", "self_Ky", "rotz_fft",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[2]))
        return to_python(__for_method__OperatorsPseudoSpectral3D__vxvyfft_from_rotzfft0(from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[0]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[1]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap___for_method__OperatorsPseudoSpectral3D__divhfft_from_vxvyfft0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    char const* keywords[] = {"self_Kx", "self_Ky", "vx_fft", "vy_fft",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[2]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[3]))
        return to_python(__for_method__OperatorsPseudoSpectral3D__divhfft_from_vxvyfft0(from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[0]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[1]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[2]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap___for_method__OperatorsPseudoSpectral3D__urudfft_from_vxvyfft0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    char const* keywords[] = {"self_Kx", "self_Ky", "vx_fft", "vy_fft",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[2]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[3]))
        return to_python(__for_method__OperatorsPseudoSpectral3D__urudfft_from_vxvyfft0(from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[0]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[1]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[2]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_compute_energy_from_3fields0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    char const* keywords[] = {"vx", "vy", "vz",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[2]))
        return to_python(compute_energy_from_3fields0(from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[0]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[1]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_compute_energy_from_2fields0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[2+1];
    char const* keywords[] = {"vx", "vy",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OO",
                                     (char**)keywords , &args_obj[0], &args_obj[1]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[1]))
        return to_python(compute_energy_from_2fields0(from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[0]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[1])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_compute_energy_from_1field_with_coef0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[2+1];
    char const* keywords[] = {"arr", "coef",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OO",
                                     (char**)keywords , &args_obj[0], &args_obj[1]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[0]) && is_convertible<double>(args_obj[1]))
        return to_python(compute_energy_from_1field_with_coef0(from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[0]), from_python<double>(args_obj[1])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_compute_energy_from_1field0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[1+1];
    char const* keywords[] = {"arr",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "O",
                                     (char**)keywords , &args_obj[0]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[0]))
        return to_python(compute_energy_from_1field0(from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[0])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_dealiasing_variable0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[2+1];
    char const* keywords[] = {"ff_fft", "where_dealiased",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OO",
                                     (char**)keywords , &args_obj[0], &args_obj[1]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<npy_uint8,pythonic::types::pshape<long,long,long>>>(args_obj[1]))
        return to_python(dealiasing_variable0(from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[0]), from_python<pythonic::types::ndarray<npy_uint8,pythonic::types::pshape<long,long,long>>>(args_obj[1])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_dealiasing_setofvar0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[2+1];
    char const* keywords[] = {"sov", "where_dealiased",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OO",
                                     (char**)keywords , &args_obj[0], &args_obj[1]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long,long>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<npy_uint8,pythonic::types::pshape<long,long,long>>>(args_obj[1]))
        return to_python(dealiasing_setofvar0(from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long,long>>>(args_obj[0]), from_python<pythonic::types::ndarray<npy_uint8,pythonic::types::pshape<long,long,long>>>(args_obj[1])));
    else {
        return nullptr;
    }
}

            static PyObject *
            __pythran_wrapall___for_method__OperatorsPseudoSpectral3D__get_phases_random(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap___for_method__OperatorsPseudoSpectral3D__get_phases_random0(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "__for_method__OperatorsPseudoSpectral3D__get_phases_random", "\n""    - __for_method__OperatorsPseudoSpectral3D__get_phases_random(float64[:,:,:], float64[:,:,:], float64[:,:,:], float64, float64, float64)", args, kw);
                });
            }


            static PyObject *
            __pythran_wrapall___for_method__OperatorsPseudoSpectral3D__vxvyfft_from_rotzfft(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap___for_method__OperatorsPseudoSpectral3D__vxvyfft_from_rotzfft0(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "__for_method__OperatorsPseudoSpectral3D__vxvyfft_from_rotzfft", "\n""    - __for_method__OperatorsPseudoSpectral3D__vxvyfft_from_rotzfft(float64[:,:,:], float64[:,:,:], complex128[:,:,:])", args, kw);
                });
            }


            static PyObject *
            __pythran_wrapall___for_method__OperatorsPseudoSpectral3D__divhfft_from_vxvyfft(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap___for_method__OperatorsPseudoSpectral3D__divhfft_from_vxvyfft0(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "__for_method__OperatorsPseudoSpectral3D__divhfft_from_vxvyfft", "\n""    - __for_method__OperatorsPseudoSpectral3D__divhfft_from_vxvyfft(float64[:,:,:], float64[:,:,:], complex128[:,:,:], complex128[:,:,:])", args, kw);
                });
            }


            static PyObject *
            __pythran_wrapall___for_method__OperatorsPseudoSpectral3D__urudfft_from_vxvyfft(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap___for_method__OperatorsPseudoSpectral3D__urudfft_from_vxvyfft0(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "__for_method__OperatorsPseudoSpectral3D__urudfft_from_vxvyfft", "\n""    - __for_method__OperatorsPseudoSpectral3D__urudfft_from_vxvyfft(float64[:,:,:], float64[:,:,:], complex128[:,:,:], complex128[:,:,:])", args, kw);
                });
            }


            static PyObject *
            __pythran_wrapall_compute_energy_from_3fields(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap_compute_energy_from_3fields0(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "compute_energy_from_3fields", "\n""    - compute_energy_from_3fields(complex128[:,:,:], complex128[:,:,:], complex128[:,:,:])", args, kw);
                });
            }


            static PyObject *
            __pythran_wrapall_compute_energy_from_2fields(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap_compute_energy_from_2fields0(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "compute_energy_from_2fields", "\n""    - compute_energy_from_2fields(complex128[:,:,:], complex128[:,:,:])", args, kw);
                });
            }


            static PyObject *
            __pythran_wrapall_compute_energy_from_1field_with_coef(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap_compute_energy_from_1field_with_coef0(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "compute_energy_from_1field_with_coef", "\n""    - compute_energy_from_1field_with_coef(complex128[:,:,:], float64)", args, kw);
                });
            }


            static PyObject *
            __pythran_wrapall_compute_energy_from_1field(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap_compute_energy_from_1field0(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "compute_energy_from_1field", "\n""    - compute_energy_from_1field(complex128[:,:,:])", args, kw);
                });
            }


            static PyObject *
            __pythran_wrapall_dealiasing_variable(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap_dealiasing_variable0(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "dealiasing_variable", "\n""    - dealiasing_variable(complex128[:,:,:], uint8[:,:,:])", args, kw);
                });
            }


            static PyObject *
            __pythran_wrapall_dealiasing_setofvar(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap_dealiasing_setofvar0(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "dealiasing_setofvar", "\n""    - dealiasing_setofvar(complex128[:,:,:,:], uint8[:,:,:])", args, kw);
                });
            }


static PyMethodDef Methods[] = {
    {
    "__for_method__OperatorsPseudoSpectral3D__get_phases_random",
    (PyCFunction)__pythran_wrapall___for_method__OperatorsPseudoSpectral3D__get_phases_random,
    METH_VARARGS | METH_KEYWORDS,
    "Supported prototypes:\n""\n""    - __for_method__OperatorsPseudoSpectral3D__get_phases_random(float64[:,:,:], float64[:,:,:], float64[:,:,:], float64, float64, float64)"},{
    "__for_method__OperatorsPseudoSpectral3D__vxvyfft_from_rotzfft",
    (PyCFunction)__pythran_wrapall___for_method__OperatorsPseudoSpectral3D__vxvyfft_from_rotzfft,
    METH_VARARGS | METH_KEYWORDS,
    "Supported prototypes:\n""\n""    - __for_method__OperatorsPseudoSpectral3D__vxvyfft_from_rotzfft(float64[:,:,:], float64[:,:,:], complex128[:,:,:])"},{
    "__for_method__OperatorsPseudoSpectral3D__divhfft_from_vxvyfft",
    (PyCFunction)__pythran_wrapall___for_method__OperatorsPseudoSpectral3D__divhfft_from_vxvyfft,
    METH_VARARGS | METH_KEYWORDS,
    "Compute the horizontal divergence in spectral space.\n""\n""    Supported prototypes:\n""\n""    - __for_method__OperatorsPseudoSpectral3D__divhfft_from_vxvyfft(float64[:,:,:], float64[:,:,:], complex128[:,:,:], complex128[:,:,:])"},{
    "__for_method__OperatorsPseudoSpectral3D__urudfft_from_vxvyfft",
    (PyCFunction)__pythran_wrapall___for_method__OperatorsPseudoSpectral3D__urudfft_from_vxvyfft,
    METH_VARARGS | METH_KEYWORDS,
    "Compute toroidal and poloidal horizontal velocities.\n""\n""    Supported prototypes:\n""\n""    - __for_method__OperatorsPseudoSpectral3D__urudfft_from_vxvyfft(float64[:,:,:], float64[:,:,:], complex128[:,:,:], complex128[:,:,:])\n""\n""        urx_fft, ury_fft contain shear modes!\n""\n"""},{
    "compute_energy_from_3fields",
    (PyCFunction)__pythran_wrapall_compute_energy_from_3fields,
    METH_VARARGS | METH_KEYWORDS,
    "Supported prototypes:\n""\n""    - compute_energy_from_3fields(complex128[:,:,:], complex128[:,:,:], complex128[:,:,:])"},{
    "compute_energy_from_2fields",
    (PyCFunction)__pythran_wrapall_compute_energy_from_2fields,
    METH_VARARGS | METH_KEYWORDS,
    "Supported prototypes:\n""\n""    - compute_energy_from_2fields(complex128[:,:,:], complex128[:,:,:])"},{
    "compute_energy_from_1field_with_coef",
    (PyCFunction)__pythran_wrapall_compute_energy_from_1field_with_coef,
    METH_VARARGS | METH_KEYWORDS,
    "Supported prototypes:\n""\n""    - compute_energy_from_1field_with_coef(complex128[:,:,:], float64)"},{
    "compute_energy_from_1field",
    (PyCFunction)__pythran_wrapall_compute_energy_from_1field,
    METH_VARARGS | METH_KEYWORDS,
    "Supported prototypes:\n""\n""    - compute_energy_from_1field(complex128[:,:,:])"},{
    "dealiasing_variable",
    (PyCFunction)__pythran_wrapall_dealiasing_variable,
    METH_VARARGS | METH_KEYWORDS,
    "Dealiasing 3d array\n""\n""    Supported prototypes:\n""\n""    - dealiasing_variable(complex128[:,:,:], uint8[:,:,:])"},{
    "dealiasing_setofvar",
    (PyCFunction)__pythran_wrapall_dealiasing_setofvar,
    METH_VARARGS | METH_KEYWORDS,
    "Dealiasing 3d setofvar object.\n""\n""    Supported prototypes:\n""\n""    - dealiasing_setofvar(complex128[:,:,:,:], uint8[:,:,:])\n""\n""    Parameters\n""    ----------\n""\n""    sov : 4d ndarray\n""        A set of variables array.\n""\n""    where_dealiased : 3d ndarray\n""        A 3d array of \"booleans\" (actually uint8).\n""\n"""},
    {NULL, NULL, 0, NULL}
};


            #if PY_MAJOR_VERSION >= 3
              static struct PyModuleDef moduledef = {
                PyModuleDef_HEAD_INIT,
                "operators3d",            /* m_name */
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
            PYTHRAN_MODULE_INIT(operators3d)(void)
            #ifndef _WIN32
            __attribute__ ((visibility("default")))
            __attribute__ ((externally_visible))
            #endif
            ;
            PyMODINIT_FUNC
            PYTHRAN_MODULE_INIT(operators3d)(void) {
                import_array()
                #if PY_MAJOR_VERSION >= 3
                PyObject* theModule = PyModule_Create(&moduledef);
                #else
                PyObject* theModule = Py_InitModule3("operators3d",
                                                     Methods,
                                                     ""
                );
                #endif
                if(! theModule)
                    PYTHRAN_RETURN;
                PyObject * theDoc = Py_BuildValue("(sss)",
                                                  "0.9.8.post2",
                                                  "2021-02-02 13:34:55.028322",
                                                  "df6845d51849a552b537224476c6a99b53ea1cd595d15188ad0cb57d226d5fd9");
                if(! theDoc)
                    PYTHRAN_RETURN;
                PyModule_AddObject(theModule,
                                   "__pythran__",
                                   theDoc);

                PyModule_AddObject(theModule, "__transonic__", __transonic__);
PyModule_AddObject(theModule, "__code_new_method__OperatorsPseudoSpectral3D__get_phases_random", __code_new_method__OperatorsPseudoSpectral3D__get_phases_random);
PyModule_AddObject(theModule, "__code_new_method__OperatorsPseudoSpectral3D__vxvyfft_from_rotzfft", __code_new_method__OperatorsPseudoSpectral3D__vxvyfft_from_rotzfft);
PyModule_AddObject(theModule, "__code_new_method__OperatorsPseudoSpectral3D__divhfft_from_vxvyfft", __code_new_method__OperatorsPseudoSpectral3D__divhfft_from_vxvyfft);
PyModule_AddObject(theModule, "__code_new_method__OperatorsPseudoSpectral3D__urudfft_from_vxvyfft", __code_new_method__OperatorsPseudoSpectral3D__urudfft_from_vxvyfft);
                PYTHRAN_RETURN;
            }

#endif