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
    // Expose fill types
    arma_cold void expose_fill_types(py::module &m) {
        py::class_<arma::fill::fill_class<arma::fill::fill_randu>>(m, "fill_randu");
        m.attr("fill_randu") = py::cast(arma::fill::randu);

        py::class_<arma::fill::fill_class<arma::fill::fill_zeros>>(m, "fill_zeros");
        m.attr("fill_zeros") = py::cast(arma::fill::zeros);

        py::class_<arma::fill::fill_class<arma::fill::fill_ones>>(m, "fill_ones");
        m.attr("fill_ones") = py::cast(arma::fill::ones);
        
        py::class_<arma::fill::fill_class<arma::fill::fill_eye>>(m, "fill_eye");
        m.attr("fill_eye") = py::cast(arma::fill::eye);

        py::class_<arma::fill::fill_class<arma::fill::fill_randn>>(m, "fill_randn");
        m.attr("fill_randn") = py::cast(arma::fill::randn);

        py::class_<arma::fill::fill_class<arma::fill::fill_none>>(m, "fill_none");
        m.attr("fill_none") = py::cast(arma::fill::none);
    }
}