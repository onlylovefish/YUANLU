import cv2
import os
import torch
import numpy as np

def main():
    '''read image and reshape'''
    rgb=cv2.cvtColor(cv2.imread(r"SR_Part_demo\train.png"),cv2.COLOR_BGR2RGB)
    h,w,c=rgb.shape
#h=h-h%(2*opt.scale)
    h=h-h%(2*2)
    w=w-w%(2*2)
    rgb=rgb[0:h,0:w]
    rgb=torch.from_numpy(np.ascontiguousarray(np.transpose(rgb,[2,0,1]))).float()
    raw=rgb_raw(rgb,True,'rggb').unsqueeze_(0)
    print(rgb.shape)
    print("----------------------------------------------------")
    print(raw.shape)

def rgb_raw(img,is_tensor=False,bayer_pattern='rggb'):
    if bayer_pattern=='rggb':
        h_shift=0
        w_shift=0
    elif bayer_pattern=='grbg':
        h_shift=0
        w_shift=1
    elif bayer_pattern=='gbrg':
        h_shift=1
        w_shift=0
    elif bayer_pattern=='bggr':
        h_shift=1
        w_shift=1
    else:
        raise SystemExit('bayer_pattern is not supported')
    if not is_tensor:
        raw=img[:,:,1:2]
        h,w,c=img.shape
        raw[h_shift:h:2,w_shift:w:2,:]=img[h_shift:h:2,w_shift:w:2,0:1]
        raw[1-h_shift:h:2,1-w_shift:w:2,:]=img[1-h_shift:h:2,1-w_shift:w:2,2:3]
    else:
        raw=img[1:2,:,:]
        c,h,w=img.shape
        raw[:,h_shift:h:2,w_shift:w:2]=img[0:1,h_shift:h:2,w_shift:w:2]
        raw[:,1-h_shift:h:2,1-w_shift:w:2]=img[2:3,1-h_shift:h:2,1-w_shift:w:2]
    return raw

if __name__=='__main__':
    main()
