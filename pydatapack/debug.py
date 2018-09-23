import os
import shutil

def move_datapack(datapack,directory,remove_local=False):
    # remove old directories
    if os.path.exists(directory+'/'+datapack.name):
        shutil.rmtree(directory+'/'+datapack.name)
    
    # remove local datapack from generation
    if remove_local and os.path.exists(datapack.name):
        shutil.rmtree(datapack.name)

    # compile and move
    datapack.compile()
    shutil.move(datapack.name,directory+'/'+datapack.name)
    
