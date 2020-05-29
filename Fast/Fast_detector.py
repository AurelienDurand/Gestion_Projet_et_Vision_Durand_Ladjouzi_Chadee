import numpy as np
import scipy as sp
import scipy.signal as sg
import matplotlib.pyplot as plt
import imageio as imio
import ShowCorners as sc

def Fast_detector(Im):
##for test in range(0,1):
##    colored_image = imio.imread('set1-1.jpg')
##    gray_image = np.sum(colored_image*[ 0.21, 0.72 ,0.07,0],axis=-1)
##    Im=gray_image
##    Fonction qui renvoit deux vecteur 1xN en retour avec les i et j des coints détecter
    
    size_r= Im.shape[0];
    size_c= Im.shape[1];
##    Threeshold ou seuil
##    Plus ce seuil augmente plus on diminue le nombre de coins détecter.
    Thresh = 100;
    cornersR=[];
    cornersC=[];
    n=9; # n=9 best repeatability result
    Allcorner=np.zeros((size_r,size_c));
    
##    Allcorner : initialisation d'un tableau à zéro qui reçoit des 1 quand on
##    détecte un coin
##    
##                  15 0 1
##               14        2
##             13            3
##             12      X     4
##             11            5
##               10        6
##                  9 8 7  
##     
    
    for i in range(4,size_r-3):    # 4 pour éviter les effets de bord
        for j in range(4,size_c-3):
            point=[Im[i-3][j],Im[i-3][j+1],Im[i-2][j+2],Im[i-1][j+3],Im[i][j+3],Im[i+1][j+3],Im[i+2][j+2],Im[i+3][j+1],Im[i+3][j],Im[i+3][j-1],Im[i+2][j-2],Im[i+1][j-3],Im[i][j-3], Im[i-1][j-3], Im[i-2][j-2], Im[i-3][j-1]];
                 #vérification pixel 1 et9 
            if (point[0]>(Im[i][j]-Thresh) and point[0] <(Im[i][j]+ Thresh) and point[8]>(Im[i][j]-Thresh) and point[8]<(Im[i][j]+ Thresh)):
                a=1;

            else:
                
                ##  vérification pixel 5 et 13
                if (point[4]>(Im[i][j]-Thresh) and point[4]<(Im[i][j]+Thresh) and point[12]>(Im[i][j]-Thresh) and point[12]<(Im[i][j]+Thresh) ):
                    a=1;
                else:
                    dark=0;
                    ligth=0;
                    for k in range(0,4): #0 1 2 3
                        if ( point[4*k]>(Im[i][j]+Thresh) ):
                            ligth=ligth+1;
                        elif point[4*k]<(Im[i][j]-Thresh):
                            dark=dark+1;
##                    print(dark,ligth)
                    if (dark >=3 or ligth >=3):
                        #print("d or l")
                        countD=0;
                        countL=0;
                        point = point+point[0:9]
                        
                        for c in range(0,len(point)):
                            if point[c]>=(Im[i][j]+Thresh) :
                                    countL=countL+1;
                                    countD = 0;
                            elif point[c]<=(Im[i][j]-Thresh):
                                    countD=countD+1;
                                    countL = 0;
                            else:
                                countD=0;
                                countL=0;
                            #print(countD,countL,n)
                            if (countD>=n or countL>=n):
##                                print(countD,countL)
##                                print(point)
                                cornersR.append(i);
                                cornersC.append(j);
                                Allcorner[i][j]=1;
                                #print("corner detect")
                                break; ## evite les points multiple
                            

##    
##    Mask:         1  2  3
##                  8  p  4
##                  7  6  5 
##     [Im(i-1,j-1) Im(i-1,j) Im(i-1,j+1) Im(i,j+1) Im(i+1,j+1) Im(i+1,j) Im(i+1,j-1) Im(i,j-1)]                           
##     All=[cornersR;cornersC];                               

##
##    élimination des non maximaux
##
                            
    Threshtmp=Thresh;
    for i in range(0,size_r):
        for j in range(0,size_c):
            if Allcorner[i][j]!=0:
##                print(Thresh,Threshtmp)
                Thresh=Threshtmp;
                
                # masqueAll : masque 3x3 autour de chaque potentiel coin
                maskAll=[Allcorner[i-1][j-1],Allcorner[i-1][j],Allcorner[i-1][j+1],Allcorner[i][j+1],Allcorner[i+1][j+1],Allcorner[i+1][j],Allcorner[i+1][j-1],Allcorner[i][j-1]];
                if sum(maskAll)>0: # on somme les valeurs autour du masque et on passe dans la boucle 
                                     # seulement si il y'a des voisins.
                    #mask=[Im(i-1,j-1) Im(i-1,j) Im(i-1,j+1) Im(i,j+1) Im(i+1,j+1) Im(i+1,j) Im(i+1,j-1) Im(i,j-1)];
                    #mask2 est un masque qui correspond en fait au cercle de
                    #16 pixel
                    mask2=[Im[i-3][j],Im[i-3][j+1],Im[i-2][j+2],Im[i-1][j+3],Im[i][j+3],Im[i+1][j+3],Im[i+2][j+2],Im[i+3][j+1],Im[i+3][j],Im[i+3][j-1],Im[i+2][j-2],Im[i+1][j-3],Im[i][j-3],Im[i-1][j-3],Im[i-2][j-2],Im[i-3][j-1]];
                    Vmin=sum(abs((mask2)-Im[i][j])); 
                    Vtot=[[],[],[]];
                    V=0;
                    while sum(maskAll)>0 and Vmin>0: #% si il y'a plusieur candidat en tant que coins
                       for ii in range(i-1,i+2): # i-1 i i+1
                           for jj in range(j-1,j+2): #%% parcours du masque 3x3
                               if Allcorner[ii][jj]!=0 and (ii!=i or jj!=j):
                                       
                                   mask2=[Im[ii-3][jj],Im[ii-3][jj+1],Im[ii-2][jj+2],Im[ii-1][jj+3],Im[ii][jj+3],Im[ii+1][jj+3],Im[ii+2][jj+2],Im[ii+3][jj+1],Im[ii+3][jj],Im[ii+3][jj-1],Im[ii+2][jj-2],Im[ii+1][jj-3],Im[ii][jj-3],Im[ii-1][jj-3],Im[ii-2][jj-2],Im[ii-3][jj-1]];
                                   # pour chaque point on test le critère
                                   for kk in range(0,16):
                                           
                                        if ( mask2[kk]-Im[ii][jj] )>Thresh:
                                            #%V=sum(abs((mask2)-Im(ii,jj))); 
                                            V= V+mask2[kk]-Im[ii][jj];
                                        elif ( Im[ii][jj] - mask2[kk])>Thresh:
                                            V= V+Im[ii][jj]-mask2[kk];
                                         
                                        # somme des différence du masque au point p du centre
                                   Vtot[0].append(V);
                                   Vtot[1].append(ii);
                                   Vtot[2].append(jj);
                                   V=0;  

                       val=min(Vtot[1]);
                       idx = Vtot[1].index(min(Vtot[1]))
                       im=Vtot[1][idx];
                       jm=Vtot[2][idx];
                       Allcorner[im][jm]=0;
                       # On réafecte le mask 3x3 avec les valeurs supprimés
                       maskAll=[Allcorner[i-1][j-1],Allcorner[i-1][j],Allcorner[i-1][j+1],Allcorner[i][j+1],Allcorner[i+1][j+1],Allcorner[i+1][j],Allcorner[i+1][j-1],Allcorner[i][j-1]];
                       # On augmente le seuil avec la valeur Vmin pour
                       # pouvoir éliminer petit à petit les non-maximaux
                       Thresh=Thresh+Vmin;
                       Vtot=[[],[],[]]; 

##    print(Allcorner)
    findone= np.where(Allcorner == 1);
    idr= findone[0]
    idc= findone[1]


##    return(cornersR,cornersC)
    return(idr,idc,cornersR,cornersC)






