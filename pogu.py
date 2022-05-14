import shutil

for i in range(100, 200):
    shutil.copy('imgbase/you.png', 'imgbase/you'+str(i)+'.png')
