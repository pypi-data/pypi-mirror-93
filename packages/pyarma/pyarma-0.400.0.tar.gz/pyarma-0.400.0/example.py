import pyarma
from pyarma import *
import os

def main():
    print("PyArmadillo: " + pyarma.__doc__ + "\n")
    print("This program is located in: " + os.path.abspath(__file__) + "\n")

    A = mat(2,3) # directly specify the matrix size (elements are uninitialised)

    print("A.n_rows: " + str(A.n_rows)) # .n_rows and .n_cols are read only
    print("A.n_cols: " + str(A.n_cols))

    A[1,2] = 456.0 # directly access an element (indexing starts at 0)
    A.print("A:")

    A.set_size(4,5) # change the size (data is not preserved)

    A.fill(5.0) # set all elements to a particular value
    A.print("A:")

    A = mat([ [ 0.165300, 0.454037, 0.995795, 0.124098, 0.047084 ],
            [ 0.688782, 0.036549, 0.552848, 0.937664, 0.866401 ],
            [ 0.348740, 0.479388, 0.506228, 0.145673, 0.491547 ],
            [ 0.148678, 0.682258, 0.571154, 0.874724, 0.444632 ],
            [ 0.245726, 0.595218, 0.409327, 0.367827, 0.385736 ] ])

    A.print("A:")

    # determinant
    print("det(A): " + str(det(A)))

    # inverse
    inv(A).print("inv(A): ")

    # save matrix as a text file
    A.save("A.txt", raw_ascii)

    # load from file
    B = mat()
    B.load("A.txt")

    # submatrices
    B[ 0:2, 3:4 ].print("B[ 0:2, 3:4 ]:")

    B[ 0,3, size(3,2) ].print("B[ 0,3, size(3,2) ]:")

    B[0, :].print("B[0, :]: ")

    B[:, 0].print("B[:, 0]: ")

    # transpose
    B.t().print("B.t(): ")

    # maximum from each column (traverse along rows)
    max(B).print("max(B): ")

    # maximum from each row (traverse along columns)
    max(B,1).print("max(B,1): ")

    # maximum value in B
    print("max(max(B)) = " + str(as_scalar(max(max(B)))))

    # sum of each column (traverse along rows)
    sum(B).print("sum(B): ")

    # sum of each row (traverse along columns)
    sum(B,1).print("sum(B,1): ")

    # sum of all elements
    print("accu(B): " + str(accu(B)))

    # trace = sum along diagonal
    print("trace(B): " + str(trace(B)))

    # generate the identity matrix
    C = mat(4,4,fill_eye)

    # random matrix with values uniformly distributed in the [0,1] interval
    D = mat(4,4,fill_randu)
    D.print("D:")

    # row vectors are matrices with one row
    r = mat([ 0.59119, 0.77321, 0.60275, 0.35887, 0.51683 ])
    r = r.t()
    r.print("r:")

    # column vectors are matrices with one column
    q = mat([ 0.14333, 0.59478, 0.14481, 0.58558, 0.60809 ])
    q.print("q:")

    # convert matrix to vector; data in matrices is stored column-by-column
    v = vectorise(A)
    v.print("v:")

    # dot or inner product
    print("as_scalar(r*q): " + str(as_scalar(r*q)))

    # outer product
    (q*r).print("q*r: ")

    # multiply-and-accumulate operation
    print("accu(A @ B) = " + str(accu(A @ B)))

    # example of a compound operation
    B += 2.0 * A.t()
    B.print("B:")

    # imat specifies an integer matrix
    AA = imat([ [ 1, 2, 3 ],
                [ 4, 5, 6 ],
                [ 7, 8, 9 ] ])

    BB = imat([ [ 3, 2, 1 ],
                [ 6, 5, 4 ],
                [ 9, 8, 7 ] ])

    # comparison of matrices (element-wise); output of a relational operator is a umat
    ZZ = (AA >= BB)
    ZZ.print("ZZ:")

    # cubes ("3D matrices")
    Q = cube( B.n_rows, B.n_cols, 2 )
  
    Q[:, :, 0] = B
    Q[:, :, 1] = 2.0 * B
  
    Q.print("Q:")

