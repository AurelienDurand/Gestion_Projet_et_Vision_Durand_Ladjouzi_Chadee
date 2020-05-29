import numpy as np
import scipy as sp
import scipy.signal as sg
import matplotlib.pyplot as plt
import imageio as imio
import ShowCorners as sc
import Fast_detector as Fd
import Appariement as app
from numpy.linalg import inv


# nearest neighbors interpolation
def nearest_neighbors(i, j, M, T_inv,h,minX,minY):
    ##w = i*h[6] + j*h[7] + h[8]
    x_max, y_max = M.shape[0] - 1, M.shape[1] - 1
    xw, yw, zw = T_inv @ np.array([i,j,1])
   ## print(zw)
    x = xw/zw
    y = yw/zw
    
    if np.floor(x) == x and np.floor(y) == y:
        x, y = int(x), int(y)
        return M[x, y]
    if np.abs(np.floor(x) - x) < np.abs(np.ceil(x) - x):
        x = int(np.floor(x))
    else:
        x = int(np.ceil(x))
    if np.abs(np.floor(y) - y) < np.abs(np.ceil(y) - y):
        y = int(np.floor(y))
    else:
        y = int(np.ceil(y))
    if x > x_max or y > y_max or x < 0 or y < 0:
        return 0.0

    return M[x, y]

idr =[128, 132, 165, 166, 166, 169, 179, 181, 196, 205, 206, 214, 218, 219, 225, 244, 251, 260, 267, 276, 288, 289, 318, 318, 352, 368]
idc = [321, 384, 235, 343, 403, 381, 473, 312, 223, 413, 266, 258, 441, 254, 438, 368, 484, 239, 244, 377, 485, 265, 500, 503, 238, 405]
idr2 = [141, 149, 174, 180, 183, 185, 198, 194, 206, 221, 218, 226, 234, 231, 241, 258, 266, 274, 281, 290, 301, 304, 329, 329, 371, 380]
idc2 = [173, 234, 82, 193, 251, 230, 314, 162, 67, 259, 114, 104, 284, 100, 282, 215, 322, 82, 87, 223, 322, 109, 334, 337, 77, 247]


n1 =0
n2 =4
X1 = idr[n1:n2]
print(X1)
Y1 = idc[n1:n2]
X2 = idr2[n1:n2]
Y2 = idc2[n1:n2]
colored_image = imio.imread('set1-1.png')
gray_image = np.sum(colored_image*[0.2989, 0.5870 ,0.1140,0],axis=-1)

colored_image2 = imio.imread('set1-2.png')
gray_image2 = np.sum(colored_image2*[0.2989, 0.5870 ,0.1140,0],axis=-1)

MatA= np.array([[X1[0],Y1[0],1,0,0,0,-X2[0]*X1[0],-X2[0]*Y1[0]],
               [0,0,0 ,X1[0],Y1[0],1,-Y2[0]*X1[0],-Y2[0]*Y1[0]],
               [X1[1],Y1[1],1,0,0,0,-X2[1]*X1[1],-X2[1]*Y1[1]],
               [0,0,0 ,X1[1],Y1[1],1,-Y2[1]*X1[1],-Y2[1]*Y1[1]],
               [X1[2],Y1[2],1,0,0,0,-X2[2]*X1[2],-X2[2]*Y1[2]],
               [0,0,0 ,X1[2],Y1[2],1,-Y2[2]*X1[2],-Y2[2]*Y1[2]],
               [X1[3],Y1[3],1,0,0,0,-X2[3]*X1[3],-X2[3]*Y1[3]],
               [0,0,0 ,X1[3],Y1[3],1,-Y2[3]*X1[3],-Y2[3]*Y1[3]]])

U, D, Vt = np.linalg.svd(MatA,full_matrices=True)
b = [X2[0],Y2[0],X2[1],Y2[1],X2[2],Y2[2],X2[3],Y2[3]]
bprim= np.dot(U.transpose(),b)

y = np.divide(bprim,D)
h = np.dot(Vt.transpose(),y)

h = np.append(h,1)
print("h: \n",h)
H = h.reshape(3,3)

print("H:\n", H)

newimage = gray_image;
row = gray_image.shape[0]
col = gray_image.shape[1]


#x'= h00x+h01y+h02 / h20x+h21y+h22
#y'= h10x+h11y+h12 / h20x+h21y+h22
zerosMat  = np.zeros((row,col))
print(zerosMat.shape)
print(gray_image.shape)
findpos = np.where(zerosMat == 0);
idr= findpos[0]
print(idr)
idc= findpos[1]
print(h)
for i  in range(0,len(idr)):
    xprim= (h[0]*idr[i]  +  h[1]*idc[i]  + h[2] ) / (h[6]*idr[i]   +  h[7]*idc[i]   + h[8] )
    yprim= (h[3]*idr[i]  +  h[4]*idc[i]  + h[5] ) / (h[6]*idr[i]   +  h[7]*idc[i]   + h[8] )
    idr[i] = xprim
    idc[i] = yprim


print("max idr: ",np.max(idr))
print("min idr: ",np.min(idr))
print("max idc: ",np.max(idc))
print("min idc: ",np.min(idc))

nbx = np.abs(np.maximum(np.max(idr),row))+np.abs(np.minimum(np.min(idr),0))
nby = np.abs(np.maximum(np.max(idc),col))+np.abs(np.minimum(np.min(idc),0))
print("nbx= ",nbx)
print("nby= ",nby)
newShape = np.zeros((nbx,nby))
img_T = np.zeros((nbx,nby))

duplicateMat = np.zeros((nbx,nby))
minY = np.abs(np.minimum(np.min(idc),0))
minY_1 = int(np.minimum(np.min(idc),0))
maxY = np.abs(np.maximum(np.max(idc),col))
minX = np.abs(np.minimum(np.min(idr),0))
minX_1 = int(np.minimum(np.min(idr),0))
maxX = np.abs(np.maximum(np.max(idr),row))

if(np.min(idr)< 0):
    idr = idr + minX -1
else:
    idr = idr + minX
if(np.min(idc)< 0):   
    idc = idc + minY -1
else:
    idc = idc + minY 
print(len(idr))

row2 = gray_image2.shape[0]
col2 = gray_image2.shape[1]
for i  in range(0,row2):
    for j in range(0,col2):
        #print(i*col2+j)
        newShape[idr[i*col2+j]][idc[i*col2+j]] =   gray_image[i][j]
        img_T[idr[i*col2+j]][idc[i*col2+j]] = gray_image[i][j]
for i  in range(0,row):
    for j in range(0,col):
        newShape[i+minX][j+minY] = gray_image2[i][j]
        
##Backward Transform
T = np.array(H)
T_inv = np.linalg.inv(T)
print("H :\n",H)
print("H_inv :\n",T_inv)
img_nn = np.empty((img_T.shape[0], img_T.shape[1], 3), dtype=np.uint8)
for i, row in enumerate(img_T):
    for j, col in enumerate(row):
        img_nn[i, j, :] = nearest_neighbors(i+minX_1, j+minY_1, gray_image, T_inv,h,minX,minY)

for i, row in enumerate(gray_image2):
    for j, col in enumerate(row):
        img_nn[i-minX_1, j-minY_1, :] = gray_image2[i][j]
        
        
plt.figure(figsize=(5, 5))
plt.imshow(img_nn)


plt.figure()
plt.gray()
plt.imshow(img_T)
plt.figure()
plt.gray()

plt.subplot(2,2,3)
plt.imshow(newShape)
plt.subplot(2,2,4)
plt.imshow(img_nn)
plt.subplot(2,2,1)
plt.imshow(gray_image)
plt.subplot(2,2,2)
plt.imshow(gray_image2)

plt.show()

