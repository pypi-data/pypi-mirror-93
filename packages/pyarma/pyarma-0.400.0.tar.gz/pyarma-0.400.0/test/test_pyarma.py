from pyarma import *
import math
import builtins

# Working as of PyArma extrasensory

# Testing matrix initialisation
# m = mat(4,5,fill_none)
# m.print("This should contain garbage.")
# print()
# m = mat(4,5,fill_eye)
# m.print("This should be an identity matrix.")
# print()
# m = mat(4,5,fill_zeros)
# m.print("This should be full of zeros.")
# print()
# m = mat(4,5,fill_ones)
# m.print("This should be full of ones.")
# print()
# m = mat(4,5,fill_randn)
# m.print("This should be random (Gaussian distribution).")
# print()
m = mat(4,5,fill_randu)
m.print("This should be random (uniformly distributed).")
print()
# # Testing submatrixing
# # m[:,:] should return everything
# m[:,:].print()
# print()
# # m[:, :y1], where cols go from 0..y1
# m[:, :2].print("This prints columns 0..2")
# m[:, :2,fill(0.0)]
# m[:, :2,fill_randu]
# m[:, :2].print("The columns should now contain a different set of random numbers.")
# print()
# # m[:, y0:], cols from y0..end
# m[:, 2:].print()
# print()
# # m[:, y0:y1]
# m[:, 1:3].print()
# print()
# # m[:x1, :], rows from 0..x1
# m[:2, :].print()
# print()
# # m[:x1, :y1], rows from 0..x1, cols 0..y1
# m[:2, :2].print()
# print()
# # m[:x1, y0:], rows 0..x1, cols y0..end
# m[:2, 2:].print()
# print()
# # m[:x1, y0:y1], rows 0..x1, cols y0..y1
# m[:2, 1:3].print()
# print()
# # m[x0:, :], rows x0..end
# m[2:, :].print()
# print()
# # m[x0:, :y1], rows x0..end, cols 0..y1
# m[2:, :2].print()
# print()
# # m[x0:, y0:], rows x0..end, cols y0..end
# m[2:, 2:].print()
# print()
# # m[x0:, y0:y1], rows x0..end, cols y0..y1
# m[2:, 1:3].print()
# print()
# # m[x0:x1, :], rows x0..x1
# m[1:3, :].print()
# print()
# # m[x0:x1, :y1], rows x0..x1, cols 0..y1
# m[1:3, :2].print()
# print()
# # m[x0:x1, y0:], rows x0..x1, cols y0..end
# m[1:3, 2:].print()
# print()
# # m[x0:x1, y0:y1], rows x0..x1, cols y0..y1
# m[1:3, 1:3].print()
# print()

# Testing diagonal access
m[diag, 0].print("This is the 0th diagonal.")
m[diag, 0].randu()
print()
m[diag, 0].print("It should now have different values.")
m.print()

# Testing row access
m[1,:].print("This should be the second row.")
m[1,1:].print("From the second column onward.")
m[1,1:3].print("Second column to fourth.")
m[1,:3].print("Up to the fourth.")


# Testing column access
m[:,1].print("This should be the second column.")
m[1:,1].print("From the second row onward.")
m[1:3,1].print("Second row to fourth.")
m[:3,1].print("Up to the fourth.")


# for i in range(2):
#     for j in range(3):
#         print(str(i) + ", " + str(j) + ": " + str(m[i,j]))

m = mat(5,5,fill_randu)
n = mat(0,1)
o = mat(1,0)
p = mat(0,0)

matrices = [m,n,o,p]

m.print()

for matrix in matrices:
    sum(matrix)
    sum(matrix,1)
    sum(sum(matrix,1))
    sum(sum(matrix,1),1)
    sum(matrix,0)
    sum(sum(matrix,0))
    sum(sum(matrix,0),0)  
    sum(sum(matrix))
    min(matrix)
    min(matrix,0)
    min(matrix,1)
    min(min(matrix))
    min(min(matrix,0))
    min(min(matrix,1))
    min(min(matrix,0),0)
    min(min(matrix,1),1)
    min(min(matrix,0),1)
    min(min(matrix,1),0)
    max(matrix)
    max(matrix,0)
    max(matrix,1)
    max(max(matrix))
    max(max(matrix,0))
    max(max(matrix,1))
    max(max(matrix,0),0)
    max(max(matrix,1),1)
    max(max(matrix,0),1)
    max(max(matrix,1),0)

n = mat(5,5,fill_randu)
# n.print()
m = m + n
# m.print()
o = mat(1,5,fill_randu)
# o.print()
m = m + o
# m.print()
p = mat(5,1,fill_randu)
# p.print()
m = m + p
# m.print()
q = mat(1,1,fill_ones)
m = m + q
# m.print()
m = m + 5
# m.print()

m = mat(3,3, fill_zeros)
m[0,1] = 5
m[0,2] = 5
m[1,2] = 5
m[diag] = mat(3, 1, fill_randu)
m.print()
#print(m.is_trimatu())
m = mat(3,3, fill_zeros)
m[1,0] = 5
m[2,0] = 5
m[2,1] = 5
m[diag] = mat(3, 1, fill_randu)
m.print()
#print(m.is_trimatl())
m = mat(3,3,fill_zeros)
m[diag] = mat(3,1,fill_randu)
m.print()
#print(m.is_diagmat())
#print(m.is_square())
m = mat(4,3,fill_randu)
#print(m.is_square())
#print(m.is_diagmat())
#print(m.is_trimatl())
#print(m.is_trimatu())
m = mat(5,5,fill_randu)
n = m.t() * m
m.print()
n.print()
#print(m.is_symmetric())
#print(n.is_symmetric())
#print(m.is_hermitian())
#print(n.is_hermitian())
#print(n.is_finite())
#print(n.has_inf())
n[0,0] = math.inf
#print(n.is_finite())
#print(n.has_inf())
#print(n.has_nan())
n[1,1] = math.nan
#print(n.has_nan())

m = mat(5,5,fill_randu)
m.print()
m.clean(0.1)
m.print()

# index_min(m).print()
# index_min(m,0).print()
# index_min(m,1).print()
# index_min(index_min(m)).print()
# index_min(index_min(m,0)).print()
# index_min(index_min(m,1)).print()

# m = mat(5,5,fill_randu)
# m.save("rmat.txt", raw_ascii)
# n = mat(5,5,fill_randu)
# o = mat(5,5,fill_eye)
# m.print()
# (m > 0.5).print()
# n.print()
# o.print()
# find(m > n).print()
# find(o).print()
# find((m > 0.5), 3, "last").print()
# find(m > n, 3, "last").print()

m = mat(5,5,fill_randu)
m.print()
u = umat(5,1)
for i in builtins.range(5):
    u[i,0] = i
u.print()
m[u].print()
m[u] = mat(5,1, fill_ones)
m.print()

m = mat(5,5,fill_randu)
m.print()
u = umat(3,1)
i = 0
for j in builtins.range(0, 5, 2):
    u[i,0] = j
    i += 1
u.print()
m[:,u].print()
m[:,u] = mat(5,3,fill_ones)
m.print()

m = mat(5,5,fill_randu)
m.print()
u = umat(3,1)
i = 0
for j in builtins.range(0, 5, 2):
    u[i,0] = j
    i += 1
u.print()
m[u,:].print()
m[u,:] = mat(3,5,fill_ones)
m.print()

m = mat(5,5,fill_randu)
m.print()
u = umat(3,1)
i = 0
for j in builtins.range(0, 5, 2):
    u[i,0] = j
    i += 1
v = u
u.print()
v.print()
m[u,v].print()
m[u,v] = mat(3,3,fill_ones)
m.print()

# m = mat(5,5,fill_randu)
# n = m.t() * m
# print(m.is_sympd())
# print(n.is_sympd())

# m = mat(5,5,fill_randu)
# m.print()
# m = m / 0.1
# m.print()

# m = mat(5,5,fill_randu)
# m.print()
# print(m.is_sorted())

# v = mat(5,1)
# for i in range(5):
#     v[i,0] = i
# v.print()
# print(v.is_sorted())

# cm = cx_mat(5,5,fill_randu)
# m = mat(5,5,fill_ones)
# n = mat(5,5,fill_zeros)
# cm.print()
# cm.set_imag(m)
# cm.print()
# cm.set_real(n)
# cm.print()

# m = mat(5,5,fill_randu)
# n = mat(3,5,fill_ones)
# m.print()
# m.insert_rows(2, n)
# m.print()
# m.insert_rows(0, 2)
# m.print()
# m.insert_rows(0, 2, False)
# m.print()
# m.shed_row(0)
# m.print()
# m.shed_rows(0,2)
# m.print()
# v = umat(3,1)
# i = 0
# for j in range(0,5,2):
#     v[i,0] = j
#     i += 1
# v.print()
# m.shed_rows(v)
# m.print()

# m = mat(5,5,fill_randu)
# n = mat(5,3,fill_ones)
# m.print()
# m.insert_cols(2, n)
# m.print()
# m.insert_cols(0, 2)
# m.print()
# m.insert_cols(0, 2, False)
# m.print()
# m.shed_col(0)
# m.print()
# m.shed_cols(0,2)
# m.print()
# v = umat(3,1)
# i = 0
# for j in range(0,5,2):
#     v[i,0] = j
#     i += 1
# v.print()
# m.shed_cols(v)
# m.print()

# m = mat(5,5,fill_randu)
# m.print()
# print(m.size())
# print(m.front())
# print(m.back())
# print(m.empty())
# m.clear()
# print(m.empty())

m = mat(5,5,fill_randu)
m.print()
n = m
n.print()
inplace_trans(m)
m.print()
n.print()

n = mat(5,5,fill_randu)
n = n.t() * n

eigval, eigvec = eig_sym(n)

eigval.print()
eigvec.print()

eigval = mat()
eigvec = mat()

eig_sym(eigval, eigvec, n)