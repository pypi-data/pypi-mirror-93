from pyarma import *

m = cube(2,3,4,fill_randu)

m.print()

# Testing get_element
print(m[0,0,0])

print(m[0])

print(m[0:1,0:1,0:1][0])

print(m[0:1,0:1,0:1][0,0,0])

# Testing set_element
m[0,0,0] = 1
print(m[0,0,0])
m[0] = 2
print(m[0])
m[0:1,0:1,0:1][0] = 3
print(m[0:1,0:1,0:1][0])
m[0:1,0:1,0:1][0,0,0] = 4
print(m[0:1,0:1,0:1][0,0,0])

# Testing get_row
m[0,:,:].print()
m[:,:,:][0,:,:].print()

# Testing get_col
m[:,:,0].print()
m[:,:,:][:,:,0].print()

# Testing get_submatrix
m[:,:,:].print()
m[:,:,:][0:1,0:1,0:1].print()

print("testing set_row\n")
# Testing set_row (set using cube, subview_cube)
n = cube(3,3,3,fill_ones)
m.print()
m[0,:,:] = cube(1,3,4,fill_ones)
m.print()
m[0,:,:] = m[1,:,:]
m.print()

m[:,:,:][0,:,:] = cube(1,3,4,fill_ones)
m.print()
m[:,:,:][0,:,:] = m[1,:,:]
m.print()

print("testing set_col\n")
# Testing set_col
m.print()
m[:,0,:] = cube(2,1,4,fill_ones)
m.print()
m[:,0,:] = m[:,1,:]
m.print()

m[:,:,:][:,0,:] = cube(2,1,4,fill_ones)
m.print()
m[:,:,:][:,0,:] = m[:,1,:]
m.print()

print("testing set_slice\n")
# Testing set_slice
m.print()
m[:,:,0] = cube(2,3,1,fill_ones)
m.print()
m[:,:,0] = m[:,:,1]
m.print()

m[:,:,:][:,:,0] = cube(2,3,1,fill_ones)
m.print()
m[:,:,:][:,:,0] = m[:,:,1]
m.print()

print("testing set_subcube\n")
# Testing set_subcube
o = cube(2,3,4,fill_zeros)
m.print()
m[:,:,:] = cube(2,3,4,fill_ones)
m.print()
m[:,:,:] = o[:,:,:]
m.print()

m[:,:,:][:,:,:] = cube(2,3,4,fill_ones)
m.print()
m[:,:,:][:,:,:] = o[:,:,:]
m.print()
