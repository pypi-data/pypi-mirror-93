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
#include "pybind11/complex.h"
#include "armadillo"

namespace py = pybind11;
using namespace pybind11::literals;

template<typename... Args>
using overload_cast_ = pybind11::detail::overload_cast_impl<Args...>;

namespace pyarma {
    // Expose running_stat_vec
    template<typename T>
    void expose_running_stat_vec(py::module &m, const std::string typestr) {
        using Class = arma::running_stat_vec<T>;
        
        py::class_<arma::running_stat_vec<T>>(m, typestr.c_str())
            .def(py::init<bool>(), "calc_cov"_a = false)
            .def("__call__", [](Class &rsv, const T &matrix) { rsv(matrix); })
            .def("min", &arma::running_stat_vec<T>::min)
            .def("max", &arma::running_stat_vec<T>::max)
            .def("range", &arma::running_stat_vec<T>::range)
            .def("mean", &arma::running_stat_vec<T>::mean)
            .def("var", &arma::running_stat_vec<T>::var, "norm_type"_a = 0)
            .def("stddev", &arma::running_stat_vec<T>::stddev, "norm_type"_a = 0)
            .def("cov", &arma::running_stat_vec<T>::cov, "norm_type"_a = 0)
            .def("reset", &arma::running_stat_vec<T>::reset)
            .def("count", &arma::running_stat_vec<T>::count);
    }

    template void expose_running_stat_vec<arma::mat>(py::module &m, const std::string typestr);
    template void expose_running_stat_vec<arma::fmat>(py::module &m, const std::string typestr);
    template void expose_running_stat_vec<arma::cx_mat>(py::module &m, const std::string typestr);
    template void expose_running_stat_vec<arma::cx_fmat>(py::module &m, const std::string typestr);
}