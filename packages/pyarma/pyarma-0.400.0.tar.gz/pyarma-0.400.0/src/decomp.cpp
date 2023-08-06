// Copyright 2020-2021 Jason Rumengan
// Copyright 2020-2021 Data61/CSIRO
// 
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
// http://www.apache.org/licenses/LICENSE-2.0
// 
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
// ------------------------------------------------------------------------

#include "pybind11/pybind11.h"
#include "armadillo"
#include <type_traits>
#include "pybind11/complex.h"

namespace py = pybind11;
using namespace pybind11::literals;

namespace pyarma {
    // TODO: test implicit conversion from submatrices to actual matrices
    /* Defining functions and methods that only work on real types 
       (double, float, and their complex forms)
       This includes inverses and decompositions */
    template<typename T>
    typename std::enable_if<!(arma::is_supported_blas_type<typename T::elem_type>::value)>::type
    expose_decomp(py::module &) { }

    template<typename T>
    typename std::enable_if<arma::is_supported_blas_type<typename T::elem_type>::value>::type
    expose_decomp(py::module &m) {
        using Type = typename T::elem_type;
        using Matrix = arma::Mat<Type>;
        using PodType = typename arma::get_pod_type<Type>::result;
        using CxType = typename std::conditional<arma::is_cx<Type>::value, Type, std::complex<Type>>::type;
        // Expose decompositions
        m.def("chol", [](const T &matrix, std::string layout = "upper") {
            Matrix temp;
            chol(temp, matrix, layout.c_str());
            return temp;
        }, "matrix"_a, "layout"_a = "upper")
        .def("chol", [](Matrix &R, const T &matrix, std::string layout = "upper") {
            return chol(R, matrix, layout.c_str());
        }, "R"_a, "matrix"_a, "layout"_a = "upper")

        .def("eig_sym", [](arma::Mat<PodType> &eigval, const T &matrix) {
            arma::Col<PodType> temp_eigval;
            bool result = eig_sym(temp_eigval, matrix);
            eigval = temp_eigval;
            return result;
        }, "eigval"_a, "matrix"_a)
        .def("eig_sym", [](arma::Mat<PodType> &eigval, Matrix &eigvec, const T &matrix) {
            arma::Col<PodType> temp_eigval;
            bool result = eig_sym(temp_eigval, eigvec, matrix);
            eigval = temp_eigval;
            return result;
        }, "eigval"_a, "eigvec"_a, "matrix"_a)
        .def("eig_sym", [](const T &matrix) { 
            arma::Col<PodType> eigval;
            Matrix eigvec;
            eig_sym(eigval, eigvec, matrix);
            return std::make_tuple(arma::Mat<PodType>(eigval), eigvec);
        })

        .def("eig_gen", [](const T &matrix, std::string bal = "nobalance") {
            // If it's already complex, the class is OK.
            // If it isn't, convert to complex. Funny, this is the reverse of the last one.
            arma::Col<CxType> eigval;
            arma::Mat<CxType> leigvec, reigvec;
            eig_gen(eigval, leigvec, reigvec, matrix, bal.c_str());
            return std::make_tuple(arma::Mat<CxType>(eigval), leigvec, reigvec);
        }, "matrix"_a, "bal"_a = "nobalance")
        .def("eig_gen", [](arma::Mat<CxType> &eigval, const T &matrix, std::string bal = "nobalance") {
            arma::Col<CxType> temp_eigval;
            bool result = eig_gen(temp_eigval, matrix, bal.c_str());
            eigval = temp_eigval;
            return result;
        }, "eigval"_a, "matrix"_a, "bal"_a = "nobalance")
        .def("eig_gen", [](arma::Mat<CxType> &eigval, arma::Mat<CxType> &eigvec, const T &matrix, std::string bal = "nobalance") {
            arma::Col<CxType> temp_eigval;
            bool result = eig_gen(temp_eigval, eigvec, matrix, bal.c_str());
            eigval = temp_eigval;
            return result;
        }, "eigval"_a, "eigvec"_a, "matrix"_a, "bal"_a = "nobalance")
        .def("eig_gen", [](arma::Mat<CxType> &eigval, arma::Mat<CxType> &leigvec, arma::Mat<CxType> &reigvec, const T &matrix, std::string bal = "nobalance") {
            arma::Col<CxType> temp_eigval;
            bool result = eig_gen(temp_eigval, leigvec, reigvec, matrix, bal.c_str());
            eigval = temp_eigval;
            return result;
        }, "eigval"_a, "leigvec"_a, "reigvec"_a, "matrix"_a, "bal"_a = "nobalance")

        .def("eig_pair", [](const T &a, const T &b) {
            // If it's already complex, the class is OK.
            // If it isn't, convert to complex. Funny, this is the reverse of the last one.
            arma::Col<CxType> eigval;
            arma::Mat<CxType> leigvec, reigvec;
            eig_pair(eigval, leigvec, reigvec, a, b);
            return std::make_tuple(arma::Mat<CxType>(eigval), leigvec, reigvec);
        })
        .def("eig_pair", [](arma::Mat<CxType> &eigval, const T &a, const T &b) {
            arma::Col<CxType> temp_eigval;
            bool result = eig_pair(temp_eigval, a, b);
            eigval = temp_eigval;
            return result;
        })
        .def("eig_pair", [](arma::Mat<CxType> &eigval, arma::Mat<CxType> &eigvec, const T &a, const T &b) {
            arma::Col<CxType> temp_eigval;
            bool result = eig_pair(temp_eigval, eigvec, a, b);
            eigval = temp_eigval;
            return result;
        })
        .def("eig_pair", [](arma::Mat<CxType> &eigval, arma::Mat<CxType> &leigvec, arma::Mat<CxType> &reigvec, const T &a, const T &b) {
            arma::Col<CxType> temp_eigval;
            bool result = eig_pair(temp_eigval, leigvec, reigvec, a, b);
            eigval = temp_eigval;
            return result;
        })

        // Sig1: U,H = hess(X)
        // Sig2: bool = hess(H,X)
        // Sig3: bool = hess(U,H,X)
        .def("hess", [](const T &matrix) {
            Matrix hess_vec, hess_mat;
            hess(hess_vec, hess_mat, matrix);
            return std::make_tuple(hess_vec, hess_mat, matrix);
        })
        .def("hess", [](Matrix &hess_mat, const T &matrix) { return hess(hess_mat, matrix); })
        .def("hess", [](Matrix &hess_vec, Matrix &hess_mat, const T &matrix) { return hess(hess_vec, hess_mat, matrix); })
        
        .def("inv", [](const T &matrix) { 
            Matrix inverse;
            inv(inverse, matrix);
            return inverse;     
        })
        .def("inv", [](Matrix &inverse, const T &matrix) { return inv(inverse, matrix); })
        
        .def("inv_sympd", [](const T &matrix) {
            Matrix inverse;
            inv_sympd(inverse, matrix);
            return inverse;
        })
        .def("inv_sympd", [](Matrix &inverse, const T &matrix) { return inv_sympd(inverse, matrix); })
        
        .def("lu", [](Matrix &l, Matrix &u, Matrix &p, const T &matrix) { return lu(l, u, p, matrix); })
        .def("lu", [](Matrix &l, Matrix &u, const T &matrix) { return lu(l, u, matrix); })
        
        .def("null", [](const T &matrix) {
            Matrix result;
            null(result, matrix);
            return result;
        })
        .def("null", [](Matrix &result, const T &matrix) { return null(result, matrix); })
        .def("null", [](const T &matrix, const PodType &tolerance) {
            Matrix result;
            null(result, matrix, tolerance);
            return result;
        })
        .def("null", [](Matrix &result, const T &matrix, const PodType &tolerance) { return null(result, matrix, tolerance); })
        
        .def("orth", [](const T &matrix) {
            Matrix result;
            orth(result, matrix);
            return result;
        })
        .def("orth", [](Matrix &result, const T &matrix) { return orth(result, matrix); })
        .def("orth", [](const T &matrix, const PodType &tolerance) {
            Matrix result;
            orth(result, matrix, tolerance);
            return result;
        })
        .def("orth", [](Matrix &result, const T &matrix, const PodType &tolerance) { return orth(result, matrix, tolerance); })
        
        .def("pinv", [](const T &matrix) {
            Matrix result;
            pinv(result, matrix);
            return result;
        })
        .def("pinv", [](Matrix &result, const T &matrix) { return pinv(result, matrix); })
        .def("pinv", [](const T &matrix, const PodType &tolerance) {
            Matrix result;
            pinv(result, matrix, tolerance);
            return result;
        })
        .def("pinv", [](Matrix &result, const T &matrix, const PodType &tolerance) { return pinv(result, matrix, tolerance); })
        
        // Q: QR, QZ, SVD_ECON, QR_ECON all have the same "side-effecting" signature. Should I implement a "return" signature?
        .def("qr", [](Matrix &q, Matrix &r, const T &matrix) { return qr(q, r, matrix); })
        .def("qr", [](Matrix &q, Matrix &r, arma::Mat<arma::uword> &p, const T &matrix, const std::string &p_type) { return qr(q, r, p, matrix, p_type.c_str()); })
        
        .def("qr_econ", [](Matrix &q, Matrix &r, const T &matrix) { return qr_econ(q, r, matrix); })
        
        .def("qz", [](Matrix &aa, Matrix &bb, Matrix &q, Matrix &z, const T &a, const T &b, std::string select = "none") {
            return qz(aa, bb, q, z, a, b, select.c_str());
        }, "aa"_a, "bb"_a, "q"_a, "z"_a, "a"_a, "b"_a, "select"_a = "none")
        
        .def("schur", [](const T &matrix) {
            Matrix schur_vec, schur_form;
            schur(schur_vec, schur_form, matrix);
            return std::make_tuple(schur_vec, schur_form);
        })
        .def("schur", [](Matrix &s, const T &matrix) { return schur(s, matrix); })
        .def("schur", [](Matrix &u, Matrix &s, const T &matrix) { return schur(u, s, matrix); })
        
        .def("solve", [](const T &a, const T &b, arma::solve_opts::opts settings = arma::solve_opts::none) {
            Matrix result;
            solve(result, a, b, settings);
            return result;
        }, "a"_a, "b"_a, "settings"_a = arma::solve_opts::none)
        .def("solve", [](Matrix &result, const T &a, const T &b, arma::solve_opts::opts settings = arma::solve_opts::none) {
            return solve(result, a, b, settings);
        }, "result"_a, "a"_a, "b"_a, "settings"_a = arma::solve_opts::none)

        // So let me get this straight.
        // If svd(X) where X is real, return reals.
        // If it's complex, return complex.
        // That's actually easy, because the input is always gonna be different anyway.
        // So the return types can differ. Great!
        // Sig1: U, s, V = svd(X)
        // Sig2: svd(s, X)
        // Sig3: svd(U,s,V,X)
        .def("svd", [](const T &matrix) {
            Matrix U, V;
            arma::Col<PodType> s;
            svd(U, s, V, matrix);
            return std::make_tuple(U, arma::Mat<PodType>(s), V);
        })
        .def("svd", [](arma::Mat<PodType> &s, const T &matrix) { 
            arma::Col<PodType> temp_s;
            bool result = svd(temp_s, matrix);
            s = temp_s; 
            return result;
        })
        .def("svd", [](Matrix &U, arma::Mat<PodType> &s, Matrix &V, const T &matrix) { 
            arma::Col<PodType> temp_s;
            bool result = svd(U, temp_s, V, matrix); 
            s = temp_s;
            return result;
        })
        
        .def("svd_econ", [](Matrix &U, arma::Mat<PodType> &s, Matrix &V, const T &matrix, std::string mode = "both") {
            arma::Col<PodType> temp_s;
            bool result = svd_econ(U, temp_s, V, matrix, mode.c_str());
            s = temp_s;
            return result;
        }, "U"_a, "s"_a, "V"_a, "matrix"_a, "mode"_a = "both")
        .def("syl", [](const T &a, const T &b, const T &c) {
            Matrix X;
            syl(X, a, b, c);
            return X;
        })
        .def("syl", [](Matrix &X, const T &a, const T &b, const T &c) { return syl(X, a, b, c); });
    }

    template void expose_decomp<arma::mat>(py::module &m);
    // template void expose_decomp<arma::subview<double>>(py::module &m);
    // template void expose_decomp<arma::diagview<double>>(py::module &m);
    // template void expose_decomp<arma::subview_elem1<double, arma::umat>>(py::module &m);
    // template void expose_decomp<arma::subview_elem2<double, arma::umat, arma::umat>>(py::module &m);

    template void expose_decomp<arma::Mat<float>>(py::module &m);
    // template void expose_decomp<arma::subview<float>>(py::module &m);
    // template void expose_decomp<arma::diagview<float>>(py::module &m);
    // template void expose_decomp<arma::subview_elem1<float, arma::umat>>(py::module &m);
    // template void expose_decomp<arma::subview_elem2<float, arma::umat, arma::umat>>(py::module &m);

    template void expose_decomp<arma::Mat<arma::cx_double>>(py::module &m);
    // template void expose_decomp<arma::subview<arma::cx_double>>(py::module &m);
    // template void expose_decomp<arma::diagview<arma::cx_double>>(py::module &m);
    // template void expose_decomp<arma::subview_elem1<arma::cx_double, arma::umat>>(py::module &m);
    // template void expose_decomp<arma::subview_elem2<arma::cx_double, arma::umat, arma::umat>>(py::module &m);
 
    template void expose_decomp<arma::Mat<arma::cx_float>>(py::module &m);
    // template void expose_decomp<arma::subview<arma::cx_float>>(py::module &m);
    // template void expose_decomp<arma::diagview<arma::cx_float>>(py::module &m);
    // template void expose_decomp<arma::subview_elem1<arma::cx_float, arma::umat>>(py::module &m);
    // template void expose_decomp<arma::subview_elem2<arma::cx_float, arma::umat, arma::umat>>(py::module &m);

    template void expose_decomp<arma::Mat<arma::uword>>(py::module &m);
    // template void expose_decomp<arma::subview<arma::uword>>(py::module &m);
    // template void expose_decomp<arma::diagview<arma::uword>>(py::module &m);
    // template void expose_decomp<arma::subview_elem1<arma::uword, arma::umat>>(py::module &m);
    // template void expose_decomp<arma::subview_elem2<arma::uword, arma::umat, arma::umat>>(py::module &m);

    template void expose_decomp<arma::Mat<arma::sword>>(py::module &m);
    // template void expose_decomp<arma::subview<arma::sword>>(py::module &m);
    // template void expose_decomp<arma::diagview<arma::sword>>(py::module &m);
    // template void expose_decomp<arma::subview_elem1<arma::sword, arma::umat>>(py::module &m);
    // template void expose_decomp<arma::subview_elem2<arma::sword, arma::umat, arma::umat>>(py::module &m);
}