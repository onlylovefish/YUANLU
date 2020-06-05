import os
for files in os.listdir('F:\\y\\downscale'):
    #print(files)
    if files[-2:]=='py':
        continue
    #new_name=files.join('x2')
    new_name=files.replace('.png','x2')
    new_name=os.path.join(new_name,'.png').replace('\\','')
    #name=files.replace('x','').replace('2','')
    print(new_name)     # 