import os
import shutil

def move_datapack(datapack,directory):
    # remove old directories
    if os.path.exists(directory+'/'+datapack.name):
        shutil.rmtree(directory+'/'+datapack.name)
    if os.path.exists(datapack.name):
        shutil.rmtree(datapack.name)

    # compile and move
    datapack.compile()
    shutil.move(datapack.name,directory+'/'+datapack.name)
    
