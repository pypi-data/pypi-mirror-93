// Copyright 2020-2021 Jason Rumengan, Terry Yue Zhuo
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

#pragma once
#include "armadillo"

/* This contains dummy functions that force Armadillo to instantiate certain classes.
   This is done, as some Base<T, Derived> definitions rely on uninstantiated Derived classes.
   These functions must be defined here, as these classes are only
   instantiated (for a given source file) if these functions are compiled on the same file. */
namespace pyarma_junk {
    // arma_cold inline arma::fcube fcubefoo() {
    //     return arma::fcube();
    // }

    arma_cold inline arma::subview_cube<double> scubefoo() { 
        arma::cube bar(5,5,5,arma::fill::none);
        return bar(arma::span::all, arma::span::all, arma::span::all); 
    }

    arma_cold inline arma::subview_cube<arma::cx_double> scubecxfoo() { 
        arma::cx_cube bar(5,5,5,arma::fill::none);
        return bar(arma::span::all, arma::span::all, arma::span::all); 
    }
}
