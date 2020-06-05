#%%
'''
图片转码转为base64
'''
import base64
f=open(r"C:\Users\ylaiv\Desktop\20150314102416687.jpg",'rb')#二进制方式打开文件
ls_f=base64.b64encode(f.read())
f.close()
print(ls_f)

# %%
print("s")

# %%
