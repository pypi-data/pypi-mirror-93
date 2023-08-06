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

namespace py = pybind11;

namespace pyarma {
    // Expose logmat functions
    template<typename T>
    void expose_logmat(py::module &m) {
        using Class = arma::Mat<T>;
        using CxType = typename std::conditional<arma::is_cx<T>::value, T, std::complex<T>>::type;

        m.def("logmat", [](const Class &matrix) { 
            arma::Mat<CxType> temp;
            arma::logmat(temp, matrix);
            return temp;
        })
        .def("logmat", [](arma::Mat<CxType> &matrix, const Class &logmat_of) { return arma::logmat(matrix, logmat_of); })
        .def("logmat_sympd", [](const Class &matrix) {
             Class temp;
             arma::logmat_sympd(temp, matrix);
             return temp;
        })
        .def("logmat_sympd", [](Class &matrix, const Class &logmat_sympd_of) { return arma::logmat_sympd(matrix, logmat_sympd_of); });
    }

    template void expose_logmat<double>(py::module &m);
    template void expose_logmat<float>(py::module &m);
    template void expose_logmat<arma::cx_double>(py::module &m);
    template void expose_logmat<arma::cx_float>(py::module &m);
}