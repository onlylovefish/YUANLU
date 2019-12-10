import  numpy as np
from scipy.ndimage import filters,measurements,interpolation
from math import pi

def imresize(im,scale_factor=None,output_shape=None,kernel=None,antialiasing=True,kernel_shift_flag=False):


def fix_scale_and_size(input_shape,output_shape,scale_factor):
    #first fixing the scale-factor(if given) to be standardized the function expects(a list of scale factors in the same size as the number of input dimensions)
    if scale_factor is not None:
        #by default,if scale-factor is a scalar we assume 2d resizing and duplicate it
        if np.isscalar(scale_factor):
          scale_factor=[scale_factor,scale_factor]
        #we extend the size of scale-factor list to the size of the input by assigning 1 to all the unspecified scales
        scale_factor=list(scale_factor)
        scale_factor.extend([1]*(len(input_shape)-len(scale_factor)))
    #Fixing output-shape(if given):extending it to the size of the input-shape,by assigning the original input-size
    #to all the unspecified dimensions
    if output_shape is not None:
        output_shape=list(np.uint(np.array(output_shape)))+list(input_shape[len(output_shape):])

#Dealing with the case of non-give scale-factor,calculating according to output-shape,note that this is sub-optimal,because there can be different scales to the same output-shape
    if scale_factor is None:
        output_shape=1.0*np.array(output_shape)/np.array(input_shape)
    
    #dealing with missing output-shape,calculating according to scale-factor
    if output_shape is None:
        #np.ceil用于以元素方式返回输入的上限
        output_shape=np.uint(np.ceil(np.array(input_shape)*np.array(scale_factor)))
    return scale_factor,output_shape

def contributions(in_length,out_length,scale,kernel,kernel_width,antialiasing):
    '''
    this function calculates a set of 'filters' and a set of field_of_view that will later on be applied such that each position from the field_of_view will be multiplied with a matching
    fliter from the weights based on the interpolation method and the distance of the sub-pixel location from the pixel centers around it this is only done for one dimension of the image.
    '''
    
    #when anti-aliasing is activated(default and only for downscaling) the receptive field is stretched to size of 1/sf.this means filtering is more 'low-pass filter'
    fixed_kernel=(lambda arg:scale*kernel(scale*arg)) if antialiasing else kernel
    kernel_width*=1.0/scale if antialiasing else 1.0
    #these are the coordinates of the ouyput image

    #range函数，和arrange函数类似，但是arange返回的是一个数据，而range范围的是一个list
    out_coordinates=np.arange(1,out_length+1)
    '''
    these are the matching positions of the output-coordinates on the input image coordinates
    best explained by example:say we have 4 horizontal pixels for HR and we downscale by SF=2 and get 2 pixels:
    [1,2,3,4]->[1,2].Remember each pixel is the middle of the pixel
    The scaling is down between the distances and not pixel numbers(the right boundary of pixel 4 is transformed to the right boundary of pixel 2,pixel 1 in the small image
    matches the boundary between pixels 1 and 2 in the big one and not to pixel 2缩放是在距离而不是像素数之间进行的（像素 4 的右边界转换为
 像素 2 的右边界。小图像中的像素 1 与大图像中的像素 1 和 2 之间的边界匹配，而不是像素 2。这意味着该位置不仅仅是按比例因子乘以旧位置
 So if we measure distance from the left border, middle of pixel 1 is at distance d=0.5, border between 1 and 2 is
at d=1, and so on (d = p - 0.5).  we calculate (d_new = d_old / sf) which means:因此，如果我们测量与左侧边框的距离，像素 1 的中间位于距离 d=0.5，1 和 2 之间的边框是
在 d=1，等等 （d = p - 0.5）。 我们计算 （d_new = d_old / sf），这意味着:# (p_new-0.5 = (p_old-0.5) / sf)->p_new = p_old/sf + 0.5 * (1-1/sf)
    matches )
    '''
    match_coordinates=1.0*out_coordinates/scale+0.5*(1-1.0/scale)#求解的是该像素点匹配的新的点的值
    
    #this is the left boundary to start multiplying the filter from it depends on the size of the filter
    left_boundary=np.floor(match_coordinates-kernel_width/2)#np.floor 返回不大于输入参数的最大整数

    #kernel width needs to be enlarged because when covering has sub-pixel borders,it must 'see' the pixel centers of the pixels it only covered a part from.
    #so we add one pixel at each side to consider(weights can zeroize them)
    expanded_kernel_width=np.ceil(kernel_width)+2#ceil向上取整
    '''
    determine a set of field_of_view for each output position,these are the pixels in the input image that the pixel in the output image 'sees'.we get a matrix whos
    horizontal dim is the output pixels(big) 
    and the vertical dim is the pixels it sees(kernel_size+2)
    '''
    field_of_view=np.squeeze(np.uint(np.expand_dims(left_boundary,axis=1)+np.arange(expanded_kernel_width)-1))
    '''
    assigh weight to each pixel in the field of view.A matrix whose horizontal dim is the output pixels and the vertical dim is a list of weigths matching to the pixel
    in the field of view(that are specialed in field_of_view)
    '''
    weights=fixed_kernel(1.0*np.expand_dims(match_coordinates,axis=1)-field_of_view-1)

    #normalize weights to sum up to 1,be careful from dividing by 0
    sum_weights=np.sum(weights,axis=1)
    sum_weights[sum_weights==0]=1.0
    weights=1.0*weights/np.expand_dims(sum_weights,axis=1)

    #we use the mirror structure as a trick for reflection padding at the boundaries,镜像结构，就是左右都相等，关于中心对称的那种
    mirror=np.uint(np.concatenate((np.arange(in_length),np.arange(in_length-1,-1,step=-1))))
    field_of_view=mirror[np.mod(field_of_view,mirrror.shape[0])]

    #get rid of weights and pixel positions that are of zero weight
    '''
    当使用布尔数组直接作为下标对象或者元组下标对象中有布尔数组时，都相当于用nonzero将布尔数组转换成一组整数数组，然后使用整数数组进行下标运算
    b1=np.array([True,False,True,False])
    np.nonzero(b1)返回(array([0,2]),)得到的是一个长度为1的元组，表示b1[0]和b1[2]的值不为0
    b2=np.array([[True, False, True], [True, False, False]])
    np.nonzero(b2)
    (array([0,0,1]),array([0,2,0]))这个的意思是b2[0,0],b2[0,2],b2[1,0]位置上的值不为0
    '''
    non_zero_out_pixels=np.nonzero(np.any(weight,axis=0))
    weights=np.squeeze(weights[:,non_zero_out_pixels])
    field_of_view=np.squeeze(field_of_view[:,non_zero_out_pixels]) #squeeze压缩维度
    return weights,field_of_view

def resize_along_dim(im,dim,weights,field_of_view):
    '''to be able to act on each dim,we swap so that dim 0 is wanted dim to resize
    np.swapaxes函数：np.swapaxes(a,axis1,axis2),interchange(互换) two axes of an array,a为输入array(阵列)，另外两个参数为维度
    '''
    tmp_dim=np.swapaxes(im,dim,0)
    #we add singleton dimensions（一个单一维） to the weight matrix so we can multiply it with the big tensor we get for tmp_im[field_of_view.T],(bsxfun style)
    weights=np.reshape(weights.T,list(weights.T.shape)+(np.ndim(im)-1)*[1])
    # This is a bit of a complicated multiplication: tmp_im[field_of_view.T] is a tensor of order image_dims+1.

    # for each pixel in the output-image it matches the positions the influence it from the input image (along 1 dim

    # only, this is why it only adds 1 dim to the shape). We then multiply, for each pixel, its set of positions with

    # the matching set of weights. we do this by this big tensor element-wise multiplication (MATLAB bsxfun style:

    # matching dims are multiplied element-wise while singletons mean that the matching dim is all multiplied by the

    # same number
    tmp_out_im=np.sum(tmp_im[field_of_view.T]*weights,axis=0)
    return np.swapaxes(tmp_out_im,dim,0)

def numeric_kernel(im,kernel,scale_factor,output_shape,kernel_shift_flag):
    '''
    see kernel_shift function to understand what this is'''
    if kernel_shift_flag:
        kernel=kernel_shift(kernel,scale_factor)
    #first run a correlation(convolution with flipped kernel)
    out_im=np.zeros_like(im)
    for channel in range(np.ndim(im)):
        out_im[:,:,channel]=filter.correlate(im[:,:,channel],kernel)
    #then subsample and return 
    return out_im[np.round(np.linspace(0,im.shape[0]-1/scale_factor[0],output_shape[0])).astype(int)[:,None],np.round(np.linspace(0,im.shape[1]-1/scale_factor[1],output_shape[1])).astype(int),:]

def kernel_shift(kernel,sf):
    '''
    there are two reasons for shifting the kernel;
    1.center of mass is not in the center of the kernel which creates ambiguity.There is no possible way to know the degradation on process included shifting so we always assume
    center of mass is center of the kernel.
    2.we further shift kernel center so that top left result pixel corresponds to the middle of the sfxsf first pixels.Default is for odd size to be in the middle of the first pixel
    and for even sized kernel to be at the top left corner of the first pixel.that is why different shfit size needed between od and even size.
    given that these two conditions are fulfilled,we are happy and aligned,the way to test it is as follows
    the input image,when interpolated(regular bicubic) is exactly aligbed with ground truth.
    '''
    #first calculate the current center of mass for the kernel
    current_center_of_mass=measurements.center_of_mass(kernel)
    #the second("+0.5*……")is for applying condition 2 from the comments above
    wanted_center_of_mass=np.array(kernel.shape)/2+0.5*(sf-(kernel.shape[0]%2))
    #define the shift vector for the kernel shifting(x,y)
    shift_vec=wanted_center_of_mass-current_center_of_mass
    #before applying the shift,we first pad the kernel so that nothing is lost due to the shift
    #biggest shift among dims+1 for safety
    kernel=np.pad(kernel,np.int(np.ceil(np.max(shift_vec)))+1,'constant')
    #finally shift the kernel and return
    return interpolation.shift(kernel,shift_vec)

''' the next functions are all interpolation method,x is the distance from left pixel center'''
def cubic(x):#三次函数插值，三次曲线
    absx=np.abs(x)
    absx2=absx**2
    absx3=absx**3
    return ((1.5*absx3-2.5*absx2+1)*(absx<=1)+(-0.5*absx+2)*((1<absx)&(absx<=2)))

def lanczos2(x):#一种将对称矩阵通过正交相似变换变成对称三对角矩阵的算法
    return (((np.sin(x*pi)*np.sin(pi*x/2)+np.finfo(np.float32).eps)/((pi**2*x**2/2)+np.info(np.float32).eps))*(abs(x)<2))

def box(x):
    return ((-0.5<=x)&(x<0.5))*1.0

def lanczos3(x):
    return (((np.sin(pi*x)*np.sin(pi*x/3)+np.info(np.float32).eps)/((pi**2*x**2/3)+np.finfo(np.float32).eps))*(abs(x)<3))

def linear(x):
    return (x+1)*((-1<=x)&(x<0))+(1-x)*((0<=x)&(x<=1))




