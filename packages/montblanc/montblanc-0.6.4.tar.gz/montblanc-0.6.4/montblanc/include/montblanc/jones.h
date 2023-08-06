#ifndef _MONTBLANC_JONES_H
#define _MONTBLANC_JONES_H


template <typename T>
void multiply_complex_in_place(std::complex<T> & lhs,
	                           const std::complex<T> & rhs)
{
	std::complex<T> tmp = lhs;

	lhs.real(lhs.real() * rhs.real());
	lhs.imag(tmp.real() * rhs.imag());
	lhs.real(lhs.real() - tmp.imag() * rhs.imag());
	lhs.imag(lhs.imag() + tmp.imag() * rhs.real());
}

template <typename T>
void multiply_complex_conjugate_in_place(std::complex<T> & lhs,
										 const std::complex<T> & rhs)
{
    std::complex<T> tmp = lhs;

    lhs.real(lhs.real() * rhs.real());
    lhs.imag(tmp.real() * rhs.real());
    lhs.real(lhs.real() + tmp.imag() * rhs.imag());
    lhs.imag(lhs.imag() - tmp.real() * rhs.imag());
}

#endif
