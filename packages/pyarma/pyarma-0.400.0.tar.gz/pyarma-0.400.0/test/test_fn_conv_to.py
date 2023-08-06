# Copyright 2020 Terry Yue Zhuo
# Copyright 2020 Data61/CSIRO

# Licensed under the Apache License, Version 2.0 (the "License"
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------------

import sys
import math
import pytest
import pyarma as pa

# def test_fn_conv_to_1():

# A = pa.mat(5,6)
# A.fill(0.1)

# uA = conv_to<umat>::from(A)
# iA = conv_to<imat>::from(A)

# assert (uA.n_rows - A.n_rows) == 0
# assert (iA.n_rows - A.n_rows) == 0

# assert (uA.n_cols - A.n_cols) == 0
# assert (iA.n_cols - A.n_cols) == 0

# assert pa.any(pa.vectorise(uA)) == False
# assert pa.any(pa.vectorise(iA)) == False

# def test_fn_conv_to_2():

# mat A(5,6) A.fill(1.0)

# umat uA = conv_to<umat>::from(A)
# imat iA = conv_to<imat>::from(A)

# assert all(vectorise(uA)) == true)
# assert all(vectorise(iA)) == true)

# def test_fn_conv_to_4():

# A =   pa.linspace<rowvec>(1,5,6)
# B = 2*pa.linspace<colvec>(1,5,6)
# C = randu<mat>(5,6)

# assert math.isclose(pa.as_scalar( conv_to<rowvec>::from(A) * conv_to<colvec>::from(B), 130.40, abs_tol=0.0001) == True

# assert math.isclose(pa.conv_to<double>::from(A * B, 130.40, abs_tol=0.0001) == True

# with pytest.raises(RuntimeError)
#     REQUIRE_THROWS( conv_to<colvec>::from(C) )