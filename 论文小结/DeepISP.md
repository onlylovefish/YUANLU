# **关于论文DeepISP这篇文章**:
### 2019.12.4-12.5
### author：袁小白

## RAW的意思就是CMOS或CCD图像感应器将捕捉到的光源信号转化为数字信号的原始数据。

## 1.Retinex方法：
### 这是一种常用的建立再科学实验和科学分析基础上的图像增强方法，至于整体的解释以及方式，后期使用时百度就行。

## 2.上面提到的方法的两个实现：单尺度和多尺度

### 即SSR和MSR两种情况，目的就是为了降低入射图像的影响，使得图像的整体信息尽量从反射图像中来。

## 3.关于平均池化和最大池化

### 平均池化：对邻域内点都求平均，一般情况下，平均池化能够减小邻域大小受限造成估计均值方差的增大，最大池化：用于减小卷积层参数误差造成估计均值的偏移。更多保留图像的纹理信息。

## 4.关于损失函数：

### In the full ISP case,the loss function is defined in the Lab domain,Because the network operates in the RGB color space,for calculating the loss,the network output needs to go through an RGB-to-Lab color conversion operator. This operator is differentiable almost everywhere and it is easy to calculate its gradient.while we compute the L1 loss on all the three Lab channels,the MS-SSIM is evaluated only on the luminance L channels.
## Loss(ˆI, I) = (1 − α) ||Lab(ˆI) − Lab(I)||1+α MSSSIM (L(ˆI), L(I))


## 5.用到了残差结构，跳跃结构，当然，这个结构到处可见。没有差别，但是这篇文章有个点，就是它同样证明了网络的宽度可以提高质量，以及参数共享等等。两层结构之类，lowlevel,和highlevel


## 6.关于RGB和Lab色域问题：

### 主要的关于Lab的介绍，使用时候可以查找怎么转换，主要就是Lab的色域更大，同样的精度，Lab需要更多的像素，此外，设备无关，对于在RGB能够表示的，Lab都能表示，L表示整张图的明暗度，（黑白版），a和b只负责颜色的多少，a表示从洋红到深绿，b表示焦黄到，RGB不能直接转Lab，需要借助XYZ。

## 7.关于图像质量评估方式：
### 这篇文章的图像质量的评估，也不是常见的采用PSNR，而是采用的是人工(human rating)+专门的评估方面的网络模型。DeepIQA

## 8.文中提到的一点还可以继续探索的方向是：
### share information while performing different tasks.this has the potential to lower computational costs compared to the case when each processing step is performed independently.The step that are excluded in the current network and require further exploration are removing camera shake/blur,adding options for HDR and adapting the network for various levels of noise.

### 关于英文生词：
### discrete离散的，
### emulate模仿，
### deviation偏差
### landscape orientation横向的，
### retain保留，
### quadratic二次变换，
### well-lit image亮的，光线好的图像
### mimic 模仿
### simultaneous 同步的
### inferior较差的


## 总结：
### 关于该篇文章最后的东西，看到了网络结构，但是我关于它的参数共享，到底是怎么共享的，我还不清楚，是否是采用的金字塔结构，至于金字塔结构又是怎么实现的，我也还是不清楚，还有网络的大小，训练时常的问题，此外文中涉及到的超参数，并没有给出原因，还有，个人觉得除了模拟ISP之外并没有太多的创新点，端到端的直接的网络模型，感觉还是玄学的亚子，真是好难啊~~