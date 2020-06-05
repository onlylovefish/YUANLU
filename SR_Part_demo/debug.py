from PIL import Image
import numpy as np
im=Image.open(r'SR_Part_demo\train.png').convert('RGB')
#如果不转换成array，则不能变成矩阵形式，所以这里的转换是为了换成数字形式
im=np.array(im,dtype=np.uint8)
#print(im)