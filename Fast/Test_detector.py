import numpy as np
import scipy as sp
import scipy.signal as sg
import matplotlib.pyplot as plt
import imageio as imio
import ShowCorners as sc
import Fast_detector as Fd
import Appariement as app
import Homographie as Hmg

##Test ShowCorners
colored_image = imio.imread('set1-1.png')
gray_image = np.sum(colored_image*[0.2989, 0.5870 ,0.1140,0],axis=-1)
colored_image2 = imio.imread('set1-2.png')
gray_image2 = np.sum(colored_image2*[0.2989, 0.5870 ,0.1140,0],axis=-1)

##colored_image = imio.imread('chat2.png')
##gray_image = np.sum(colored_image*[0.2989, 0.5870 ,0.1140],axis=-1)
##gray_image2 = np.sum(colored_image*[0.2989, 0.5870 ,0.1140],axis=-1)

##colored_image = imio.imread('testfig.jpg')
##gray_image = np.sum(colored_image*[ 0.2989, 0.5870 ,0.1140],axis=-1)
##gray_image2 = np.sum(colored_image*[ 0.2989, 0.5870 ,0.1140],axis=-1)
##idr,idc,cornersR,cornersC=Fd.Fast_detector(gray_image)
##print(len(idr)," ", len(cornersC))
##Fast = sc.ShowCorners(cornersR,cornersC,gray_image);
##plt.imshow(Fast)
##plt.title('Algo Fast');



##sub_img = colored_image[::5,::5,:]

##colored_image = imio.imread('testfig.jpg')
##gray_image = np.sum(colored_image*[ 0.2989, 0.5870 ,0.1140],axis=-1)

print(colored_image.shape)
##print(np.where(gray_image>0))

idr_app1,idc_app1,idr_app2,idc_app2 = app.Appariement(gray_image,gray_image2)
print(len(idr_app1), "  " , len(idc_app2))
#print(idr_app1,idc_app1)
# si app(im1,im2) -> hmg(idr1,idc1,idr2,idc2,colimg1,colimg2)
# si app(im2,im1) -> hmg(idr2,idc2,idr1,idc1,colimg1,colimg2)
img_homographie = Hmg.Homographie(idr_app1,idc_app1,idr_app2,idc_app2,colored_image,colored_image2)


##idr_app1,idc_app1,idr_app2,idc_app2 = app.Appariement(gray_image2,gray_image)
##img_homographie = Hmg.Homographie(idr_app2,idc_app2,idr_app1,idc_app1,colored_image,colored_image2)

##plt.show()


##plt.figure(figsize = (5,5))
##plt.title("Gray image")
##plt.imshow(gray_image)
idr,idc,cornersR,cornersC=Fd.Fast_detector(gray_image)
##
plt.figure(figsize = (5,5))
plt.gray()
plt.subplot(1,2,1);
Fast = sc.ShowCorners(cornersR,cornersC,gray_image);
print(len(cornersR))
plt.imshow(Fast)
plt.title('Algo Fast');
plt.subplot(1,2,2);
Nmax = sc.ShowCorners(idr,idc,gray_image);
print(len(idr))
plt.title('Algo Fast - Elimination des non maximum');
plt.imshow(Nmax)
plt.show()


##print(gray_image.shape[0])
##print(gray_image.shape[1])

