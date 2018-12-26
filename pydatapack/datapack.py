import shutil
import os
import re

from .tags import tag_manager
from .functions import function_manager
from . import internals

class Datapack:
    def __init__(self,path,name,description=None,namespace=None):
        self.name = name
        self.path = f'{path}/{self.name}'
        self.description = description if description != None else ''
        self.namespace = namespace if namespace != None else internals.formatNamespace(name)
        
        self.root_data_path = f'{self.path}/data/'
        self.tags = tag_manager.TagManager(self)
        self.functions = function_manager.FunctionManager(self)

    # * with support
    def __enter__(self):
        return self
    
    def __exit__(self,*args,**kwargs):
        self.compile()

    # * blocks tags
    # def newBlocksTag(self,tag_name,blocks):
    #     if tag_name in self.block_tags.keys():
    #         self.block_tags[tag_name].append(blocks)
    #     else:
    #         self.block_tags[tag_name] = blocks
            
    #     return self.getBlockTagReference(tag_name)

    # def getBlockTagReference(self,name):
    #     return f'#{self.namespace}:{name}'


    # * compilation factors
    def compile(self):

        # initialize progression variables
        active_tags = {}

        # remove old root folder if exists
        if os.path.exists(self.path):
            shutil.rmtree(self.path)

        # create root folder
        os.makedirs(self.root_data_path)
        self.__make_meta()

        # process all managers
        self.functions.compile()
        self.tags.compile()

    def __make_meta(self):
        with open(f'{self.path}/pack.mcmeta','w') as f:
            f.write(f'{{\n\t"pack": {{\n\t\t"pack_format": 1,\n\t\t"description": "{internals.escapeJson(self.description)}"\n\t}}\n}}')

