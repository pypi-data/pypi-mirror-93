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

def test_fn_any_1():

    A =  pa.mat(5, 6, pa.fill_zeros)
    B = pa.mat(5, 6, pa.fill_zeros)
    B[0,0] = 1.0
    C = pa.mat(5, 6, pa.fill_ones )

    assert pa.any(pa.vectorise(A))[0] == False
    assert pa.any(pa.vectorise(B))[0] == True
    assert pa.any(pa.vectorise(C))[0] == True 

    assert pa.any(pa.vectorise(A[pa.span_all,pa.span_all]))[0] == False
    assert pa.any(pa.vectorise(B[pa.span_all,pa.span_all]))[0] == True
    assert pa.any(pa.vectorise(C[pa.span_all,pa.span_all]))[0] == True 

    assert pa.any(pa.vectorise(  C -  C))[0] == False
    assert pa.any(pa.vectorise(2*C -2*C))[0] == False

    assert pa.any(pa.vectorise(C) < 0.5)[0] == False
    assert pa.any(pa.vectorise(C) > 0.5)[0] == True

# def test_fn_any_2():

#     A = pa.mat(5, 6, pa.fill_zeros)
#     B = pa.mat(5, 6, pa.fill_zeros)
#     B[0,0] = 1.0
#     C = pa.mat(5, 6, pa.fill_ones )
#     D = pa.mat(5, 6, pa.fill_ones )
#     D[0,0] = 0.0

#     assert pa.accu(pa.any(A)   == pa.urowvec({0, 0, 0, 0, 0, 0}) ) == 6
#     assert pa.accu(pa.any(A,0) == pa.urowvec({0, 0, 0, 0, 0, 0}) ) == 6
#     assert pa.accu(pa.any(A,1) == pa.uvec   ({0, 0, 0, 0, 0}   ) ) == 5

#     assert pa.accu(pa.any(B)   == pa.urowvec({0, 0, 0, 0, 0, 0}) ) == 6
#     assert pa.accu(pa.any(B,0) == pa.urowvec({0, 0, 0, 0, 0, 0}) ) == 6
#     assert pa.accu(pa.any(B,1) == pa.uvec   ({0, 0, 0, 0, 0}   ) ) == 5

#     assert pa.accu(pa.any(C)   == pa.urowvec({1, 1, 1, 1, 1, 1}) ) == 6
#     assert pa.accu(pa.any(C,0) == pa.urowvec({1, 1, 1, 1, 1, 1}) ) == 6
#     assert pa.accu(pa.any(C,1) == pa.uvec   ({1, 1, 1, 1, 1}   ) ) == 5

#     assert pa.accu(pa.any(D)   == pa.urowvec({0, 1, 1, 1, 1, 1}) ) == 6
#     assert pa.accu(pa.any(D,0) == pa.urowvec({0, 1, 1, 1, 1, 1}) ) == 6
#     assert pa.accu(pa.any(D,1) == pa.uvec   ({0, 1, 1, 1, 1}   ) ) == 5