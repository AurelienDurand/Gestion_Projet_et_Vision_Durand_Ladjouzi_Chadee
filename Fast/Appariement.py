import numpy as np
import scipy as sp
import scipy.signal as sg
import matplotlib.pyplot as plt
import Fast_detector as Fd
import ShowCorners as sc
import imageio as imio

def Appariement(Im1,Im2):

##    # Show corners
##    Fast1 = sc.ShowCorners(idr1,idc1,Im1);
##    Fast2 = sc.ShowCorners(idr2,idc2,Im2);
    #Find match
    
    # Passage Im1 vers Im2 
    posr1,posc1,bestr,bestc = match(Im1,Im2)
    # Passage Im2 vers Im1
    posr2,posc2,bestr2,bestc2 = match(Im2,Im1)
    
    idr_app1 = []
    idc_app1 = []
    idr_app2 = []
    idc_app2 = []

    for i in range(0,len(posr1)):
        for j in range(0,len(posr2)):
            if posr1[i]== bestr2[j] and posc1[i]== bestc2[j] and bestr[i]== posr2[j] and bestc[i]== posc2[j]:
                   idr_app1.append(posr1[i])
                   idc_app1.append(posc1[i])
                   idr_app2.append(bestr[i])
                   idc_app2.append(bestc[i])
                
    showMatches(Im1,Im2,posr1,posc1,bestr,bestc)
    showMatches(Im2,Im1,posr2,posc2,bestr2,bestc2)
    showMatches(Im1,Im2,idr_app1,idc_app1,idr_app2,idc_app2)
    print(len(posr1),len(posr2),len(idr_app1))

    return idr_app1,idc_app1,idr_app2,idc_app2
    
def match(Im1,Im2):
    # Détection des coins
    idr1,idc1,cornersR1,cornersC1=Fd.Fast_detector(Im1)
    idr2,idc2,cornersR2,cornersC2=Fd.Fast_detector(Im2)
    plt.figure()
    plt.subplot(1,2,1)
    plt.imshow(sc.ShowCorners(idr1,idc1,Im1))
    plt.subplot(1,2,2)
    plt.imshow(sc.ShowCorners(idr2,idc2,Im2))
    
    size_r1= Im1.shape[0];
    size_c1= Im1.shape[1];
    size_r2= Im2.shape[0];
    size_c2= Im2.shape[1];
    bestr=[];
    bestc=[];
    posr1=[];
    posc1=[];
    N=2

    for i in range(0,len(idr1)):
        allZMSSD=[]
        row1=idr1[i]
        col1=idc1[i]
        if row1>N and col1>N and row1< size_r1-N and col1< size_c1-N:
            # test des effets de bords
            mask1=[]
            #mask1=[Im1(row1,col1) Im1(row1-1,col1-1) Im1(row1-1,col1) Im1(row1-1,col1+1) Im1(row1,col1+1) Im1(row1+1,col1+1) Im1(row1+1,col1) Im1(row1+1,col1-1) Im1(row1,col1-1)];
            for ii in range(-N,N+1):
                  for jj in range(-N,N+1):
                     mask1.append(Im1[row1+ii][col1+jj])

            mu1=np.mean(mask1) 

            for j in range(0,len(idr2)):
                
                row2=idr2[j];
                col2=idc2[j];
                if row2>N and col2>N and row2< size_r2-N and col2< size_c2-N:
                    mask2=[];
                    for ii in range(-N,N+1):
                        for jj in range(-N,N+1):
                            mask2.append( Im2[row2+ii][col2+jj] )      

                  #mask2=[Im2(row2,col2) Im2(row2-1,col2-1) Im2(row2-1,col2) Im2(row2-1,col2+1) Im2(row2,col2+1) Im2(row2+1,col2+1) Im2(row2+1,col2) Im2(row2+1,col2-1) Im2(row2,col2-1)];
                    mu2=np.mean(mask2)       
        #         zero-mean-sum of squared distance -> ZMSSD
                    ZMSSD=sum( ((mask2-mu2)-(mask1-mu1))**2 )  
                 
                  #ZMSSD1=[ZMSSD1 [ZMSSD;double(Im1(row1,col1));double(Im2(row2,col2))]];
                    allZMSSD.append(ZMSSD)
                  
            if min(allZMSSD)<10000:
                idx = allZMSSD.index(min(allZMSSD))
                posr1.append(row1)
                posc1.append(col1)
                bestr.append(idr2[idx])
                bestc.append(idc2[idx])
    return (posr1,posc1,bestr,bestc)

def showMatches(Im1,Im2,posr1,posc1,posr2,posc2):
    size_r1= Im1.shape[0]
    size_c1= Im1.shape[1]
    size_r2= Im2.shape[0]
    size_c2= Im2.shape[1]

    #Concatenation
    imAp=np.concatenate([Im1,Im2],axis=1)
    posc2loc = np.array(posc2) + size_c1
    plt.figure()
    plt.title('Im_match')
##    plt.plot([posc1[0],posc2loc[0]],[posr1[0],posr2[0]], 'ro-')
    for i in range(0,len(posr1)):
        plt.plot([posc1[i],posc2loc[i]],[posr1[i],posr2[i]], 'ro-')
    plt.gray()
    plt.imshow(imAp)
