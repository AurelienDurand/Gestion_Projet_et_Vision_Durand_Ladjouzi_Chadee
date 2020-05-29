import numpy as np
import scipy as sp
import scipy.signal as sg
import matplotlib.pyplot as plt
import imageio as imio
import ShowCorners as sc
## posr & posc == list des coordonnée des pixels coin ex:[100,105,145] [88,99,156]
# Donc de même taille

def ShowCorners(posr, posc, im):

    if len(im.shape)==3:
        print("Must be a gray image - colored given")
        return 

    imResult =  np.stack( (im,)*3, axis=-1) 

    for i in range(0,len(posr)):
        r = posr[i];
##        print(r)
        c = posc[i];
##        print(c)
        for j in range(r-1,r+2):
            imResult[j][c][0]=255
            imResult[j][c][1]=0
            imResult[j][c][2]=0
        for j in range(c-1,c+2):
            imResult[r][j][0]=255
            imResult[r][j][1]=0
            imResult[r][j][2]=0
    return imResult.astype(np.uint8)

########## Test #########

##colored_image = imio.imread('Moire.jpg')
##sub_defense = colored_image[::5,::5,:]
##gray_image = np.sum(colored_image*[ 0.21, 0.72 ,0.07],axis=-1)
##R=[100,102]
##C=[100,102]
##imcroix = ShowCorner(R,C,gray_image)
##plt.figure(figsize = (5,5))
##plt.title("Corner image")
##plt.imshow(imcroix)
##plt.show()
