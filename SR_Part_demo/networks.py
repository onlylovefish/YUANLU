import torch
import torch.nn as nn
from util import swap_axis
from configs import Config
#自添
import argparse

class Generator(nn.Module):
    #conf=Config.conf
    def __init__(self, conf):
        super(Generator, self).__init__()
        struct = conf.G_structure
        #自添

        # struct=[7, 5, 3, 1, 1, 1]
        # First layer - down sampling
        self.first_layer = nn.Conv2d(in_channels=1, out_channels=conf.G_chan, kernel_size=struct[0], stride=int(1 / conf.scale_factor), bias=False)
        #self.first_layer = nn.Conv2d(in_channels=1, out_channels=conf.G_chan, kernel_size=struct[0], stride=int(1 / conf.scale_factor), bias=False)

        feature_block = []  # Stacking intermediate layer
        for layer in range(1, len(struct) - 1):
            feature_block += [nn.Conv2d(in_channels=conf.G_chan, out_channels=conf.G_chan, kernel_size=struct[layer], bias=False)]
        self.feature_block = nn.Sequential(*feature_block)
        self.final_layer = nn.Conv2d(in_channels=conf.G_chan, out_channels=1, kernel_size=struct[-1], bias=False)

        # Calculate number of pixels shaved in the forward pass
        self.output_size = self.forward(torch.FloatTensor(torch.ones([1, 1,conf.input_crop_size,conf.input_crop_size]))).shape[-1]
        self.forward_shave = int(conf.input_crop_size * conf.scale_factor) - self.output_size

    def forward(self, input_tensor):
        # Swap axis of RGB image for the network to get a "batch" of size = 3 rather the 3 channels
        input_tensor = swap_axis(input_tensor)
        downscaled = self.first_layer(input_tensor)
        features = self.feature_block(downscaled)
        output = self.final_layer(features)
        return swap_axis(output)


class Discriminator(nn.Module):

    def __init__(self, conf):
        super(Discriminator, self).__init__()

        # First layer - Convolution (with no ReLU)
        self.first_layer = nn.utils.spectral_norm(nn.Conv2d(in_channels=3, out_channels=conf.D_chan, kernel_size=conf.D_kernel_size, bias=True))
        feature_block = []  # Stacking layers with 1x1 kernels
        for _ in range(1, conf.D_n_layers - 1):
            feature_block += [nn.utils.spectral_norm(nn.Conv2d(in_channels=conf.D_chan, out_channels=conf.D_chan, kernel_size=1, bias=True)),
                              nn.BatchNorm2d(conf.D_chan),
                              nn.ReLU(True)]
        self.feature_block = nn.Sequential(*feature_block)
        self.final_layer = nn.Sequential(nn.utils.spectral_norm(nn.Conv2d(in_channels=conf.D_chan, out_channels=1, kernel_size=1, bias=True)),
                                         nn.Sigmoid())

        # Calculate number of pixels shaved in the forward pass
        self.forward_shave = conf.input_crop_size - self.forward(torch.FloatTensor(torch.ones([1, 3, conf.input_crop_size, conf.input_crop_size]))).shape[-1]

    def forward(self, input_tensor):
        receptive_extraction = self.first_layer(input_tensor)
        features = self.feature_block(receptive_extraction)
        return self.final_layer(features)


def weights_init_D(m):
    """ initialize weights of the discriminator """
    class_name = m.__class__.__name__
    if class_name.find('Conv') != -1:
        nn.init.xavier_normal_(m.weight, 0.1)
        if hasattr(m.bias, 'data'):
            m.bias.data.fill_(0)
    elif class_name.find('BatchNorm2d') != -1:
        m.weight.data.normal_(1.0, 0.02)
        m.bias.data.fill_(0)


def weights_init_G(m):
    """ initialize weights of the generator """
    if m.__class__.__name__.find('Conv') != -1:
        nn.init.xavier_normal_(m.weight, 0.1)
        if hasattr(m.bias, 'data'):
            m.bias.data.fill_(0)


# # 自添,打印该网络模型
# def main():
#     parser=argparse.ArgumentParser()
#     parser.add_argument("G_chan",type=int,default=64,help="of channels in hidden layer in the G")
#     parser.add_argument("scale_factor",type=float,default=0.5,help='the downscaling scale factor')
#     parser.add_argument("input_crop_size",type=int,default=64,help="generators crop size")
#     #discriminator
#     parser.add_argument('D_chan',type=int,default=64,help="of channel in hidden layer in the Discriminator")
#     parser.add_argument('D_kernel_size',type=int,default=7,help='discriminators convolution kernel size')
#     parser.add_argument("D_n_layers",type=int,default=7,help="discriminators convolution kernels size")
#     conf=parser.parse_args()
#     conf=parser.parse_args()
#     conf=parser.parse_args()
#     conf=parser.parse_args()
#     conf=parser.parse_args()
#     conf=parser.parse_args()
#     g=Generator(conf)
#     print(g.first_layer)
#     print(g.feature_block)
#     print(g.final_layer)
#     print(g.output_size)

#     d=Discriminator(conf)
#     print(d.first_layer)
#     print(d.feature_block)
#     print(d.final_layer)
#     print(d.output_size)
#     #print(g.first_layer+'\n'+g.feature_block+'\n'+g.final_layer+'\n'+g.out_channels+'\n'+g.output_size)
# if __name__ == '__main__':
#     main()
    