import os

import shutil

def content_copier(source, target):
    if os.path.exists(target):
        shutil.rmtree(target)
    os.mkdir(target)
    for content in os.listdir(source):
        new_path = os.path.join(source, content)
        new_target = os.path.join(target, content)
        if os.path.isfile(new_path):
           shutil.copy(new_path, new_target)
        elif not os.path.isfile(new_path):
            content_copier(new_path, new_target)



        

    
