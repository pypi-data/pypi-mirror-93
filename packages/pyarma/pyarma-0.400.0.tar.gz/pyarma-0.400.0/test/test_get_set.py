from pyarma import *

m = mat(2,3,fill_randu)

m.print()

# Testing get_element
print(m[0,0])

print(m[0])

print(m[0:1,0:1][0])

print(m[0:1,0:1][0,0])

print(m[diag][0])

print(m[diag][0,0])

# Testing set_element
m[0,0] = 1
print(m[0,0])
m[0] = 2
print(m[0])
m[0:1,0:1][0] = 3
print(m[0:1,0:1][0])
m[0:1,0:1][0,0] = 4
print(m[0:1,0:1][0,0])
m[diag][0] = 5
print(m[diag][0])
m[diag][0,0] = 6
print(m[diag][0,0])

# Testing get_row
m[0,:].print()
m[:,:][0,:].print()

# Testing get_col
m[:,0].print()
m[:,:][:,0].print()

# Testing get_submatrix
m[:,:].print()
m[:,:][0:1,0:1].print()

print("testing set_row\n")
# Testing set_row (set using mat, subview or diagview)
n = mat(3,3,fill_ones)
m.print()
m[0,:] = mat(1,3,fill_ones)
m.print()
m[0,:] = m[1,:]
m.print()
m[0,:] = n[diag].as_row()
m.print()

m[:,:][0,:] = mat(1,3,fill_ones)
m.print()
m[:,:][0,:] = m[1,:]
m.print()
m[:,:][0,:] = n[diag].as_row()
m.print()

print("testing set_col\n")
# Testing set_col
m.print()
m[:,0] = mat(2,1,fill_ones)
m.print()
m[:,0] = m[:,1]
m.print()
m[:,0] = m[diag]
m.print()

m[:,:][:,0] = mat(2,1,fill_ones)
m.print()
m[:,:][:,0] = m[:,1]
m.print()
m[:,:][:,0] = m[diag]
m.print()

print("testing set_submatrix\n")
# Testing set_submatrix
o = mat(2,3,fill_zeros)
m.print()
m[:,:] = mat(2,3,fill_ones)
m.print()
m[:,:] = o[:,:]
m.print()
m[0:0, 0:2] = n[diag].as_row()
m.print()

m[:,:][:,:] = mat(2,3,fill_ones)
m.print()
m[:,:][:,:] = o[:,:]
m.print()
m[:,:][0:0, 0:2] = n[diag].as_row()
m.print()