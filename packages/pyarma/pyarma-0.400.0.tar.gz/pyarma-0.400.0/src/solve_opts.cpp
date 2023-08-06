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
    // Expose solve options
    arma_cold void expose_solve_opts(py::module &m) {
        py::class_<arma::solve_opts::opts>(m, "solve_opts").def_readonly("flags", &arma::solve_opts::opts::flags)
            .def("__add__", [](const arma::solve_opts::opts &left, const arma::solve_opts::opts &right) {
                return left + right;
            });

        // Expose solve_opts
        py::class_<arma::solve_opts::opts_none, arma::solve_opts::opts>(m, "solve_opts_none");
        py::class_<arma::solve_opts::opts_fast, arma::solve_opts::opts>(m, "solve_opts_fast");
        py::class_<arma::solve_opts::opts_refine, arma::solve_opts::opts>(m, "solve_opts_refine");
        py::class_<arma::solve_opts::opts_equilibrate, arma::solve_opts::opts>(m, "solve_opts_equilibrate");
        py::class_<arma::solve_opts::opts_likely_sympd, arma::solve_opts::opts>(m, "solve_opts_likely_sympd");
        py::class_<arma::solve_opts::opts_allow_ugly, arma::solve_opts::opts>(m, "solve_opts_allow_sympd");
        py::class_<arma::solve_opts::opts_no_approx, arma::solve_opts::opts>(m, "solve_opts_no_approx");
        py::class_<arma::solve_opts::opts_no_band, arma::solve_opts::opts>(m, "solve_opts_no_band");
        py::class_<arma::solve_opts::opts_no_trimat, arma::solve_opts::opts>(m, "solve_opts_no_trimat");
        py::class_<arma::solve_opts::opts_no_sympd, arma::solve_opts::opts>(m, "solve_opts_no_sympd");

        // Expose as attributes, so solve_opts() is unnecessary
        m.attr("solve_opts_fast") = py::cast(arma::solve_opts::fast);
        m.attr("solve_opts_refine") = py::cast(arma::solve_opts::refine);
        m.attr("solve_opts_equilibrate") = py::cast(arma::solve_opts::equilibrate);
        m.attr("solve_opts_likely_sympd") = py::cast(arma::solve_opts::likely_sympd);
        m.attr("solve_opts_allow_ugly") = py::cast(arma::solve_opts::allow_ugly);
        m.attr("solve_opts_no_approx") = py::cast(arma::solve_opts::no_approx);
        m.attr("solve_opts_no_band") = py::cast(arma::solve_opts::no_band);
        m.attr("solve_opts_no_trimat") = py::cast(arma::solve_opts::no_trimat);
        m.attr("solve_opts_no_sympd") = py::cast(arma::solve_opts::no_sympd);
    }
}