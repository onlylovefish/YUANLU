import numpy as np
from torch.utils.data import Dataset
from SR_Part_demo.Inter_GAN_resizer import imresize
from SR_Part_demo.util import read_image,create_gradient_map,im2tensor,create_probability_map,nn_interpolation
from SR_Part_demo.networks import *
class DataGenerator(Dataset):
    '''load the image once,calculation it's gradient map on initialization and then outputs'''
    def __init__(self,conf,gan):
        #default shape
        self.g_input_shape=conf.input_crop_size
        self.d_input_shape=gan.output_size
        self.output_shape=self.d_input_shape-gan.D.forward_shave

        #read input image
        self.input_image=read_image(conf.input_image_path)/255
        self.shave_edges(scale_factor=conf.scale_factor,read_image=conf.real_image)
        self.in_rows,self.in_cols=self.input_image.shape[0:2]
        
        #create prob map for choosing the crop
        self.crop_indices_for_g,self.crop_indices_for_d=self.make_list_of_crop_indices(conf=conf)

    def __len__(self):
        return 1

    def __getitem__(self,idx):
        '''get a crop for both G and D'''
        g_in=self.next_crop(for_g=True,idx=idx)
        d_in=self.next_crop(for_g=False,idx=idx)
        return g_in,d_in

    def next_crop(self,for_g,idx):
        '''return a crop according to the pre-determined list of indices.Noise is added to crops for D'''
        size=self.g_input_shape if for_g else self.d_input_shape
        top,left=self.get_top_left(size,for_g,idx)
        crop_im=self.input_image[top:top+size,left:left+size,:]
        if not for_g:
            crop_im+=np.random.randn(*crop_im.shape)/255.0
        return im2tensor(crop_im)

    def make_list_of_crop_indices(self,conf):
        iterations=conf.max_iters
        prob_map_big,prob_map_sml=self.create_prob_maps(scale_factor=conf.scalf_factor)


    def create_prob_maps(self,scale_factor):
        '''create loss maps for input image and downscaled one'''
        loss_map_big=create_gradient_map(self.input_image)
        loss_map_smal=create_gradient_map()
