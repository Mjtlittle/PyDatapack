from .richtext import tellRichText
from .function import *
from .internals import *

import shutil
import os
import re

class Datapack:
    def __init__(self,name,description=None,namespace=None):
        self.name = name
        self.description = description if description != None else ''
        self.namespace = namespace if namespace != None else formatNamespace(name)

        self.root_data_path = f'{self.name}/data/'

        self.functions = []
        self.block_tags = {}

        # populate helper functions
        self.__make_helper_functions()

    # * with support
    def __enter__(self):
        return self
    
    def __exit__(self,*args,**kwargs):
        self.compile()

    # * blocks tags
    def newBlocksTag(self,tag_name,blocks):
        if tag_name in self.block_tags.keys():
            self.block_tags[tag_name].append(blocks)
        else:
            self.block_tags[tag_name] = blocks
            
        return self.getBlockTagReference(tag_name)

    def getBlockTagReference(self,name):
        return f'#{self.namespace}:{name}'

    # * functions
    def newFunction(self,target,*tags):
        self.registerFunction(Function(target,*tags))
        return self.last_function

    def registerFunctions(self,functions):
        for function in functions:
            self.registerFunction(function)

    def registerFunction(self,function):
        
        # function already in datapack
        if function in self.functions:
            return False

        # assign namespace if none given
        if function.namespace == None:
            function.namespace = self.namespace

        self.functions.append(function)
        return True

    @property
    def last_function(self):
        return self.functions[-1]

    # * other
    def standardObjective(self,name,length=16):
        return standardObjective(self.namespace,name,length)

    # * compilation factors
    def compile(self):
        # initialize progression variables
        active_tags = {}

        # remove old root folder if exists
        if os.path.exists(self.name):
            shutil.rmtree(self.name)

        # create root folder
        os.makedirs(self.root_data_path)
        self.__make_meta()

        # process the block tags
        self.__make_block_tags()

        # process functions
        for function in self.functions:

            path = self.root_data_path + function.namespace + '/functions' + (f'/{function.parentStructure}' if function.parentStructure != None else '')

            # make directory if doesnt exist
            if not os.path.exists(path):
                os.makedirs(path)
            
            # add tags to active tags
            for tag in function.tags:
                if tag in active_tags.keys():
                    active_tags[tag].append(function.target)
                else:
                    active_tags[tag] = [function.target]

            # process the tags for all of the functions
            self.__process_function_tags(active_tags)

            # write file for function
            with open(f'{path}/{function.name}.mcfunction','w') as f:
                f.write(str(function))

    def __make_meta(self):
        with open(f'{self.name}/pack.mcmeta','w') as f:
            f.write(f'{{\n\t"pack": {{\n\t\t"pack_format": 1,\n\t\t"description": "{escapeJson(self.description)}"\n\t}}\n}}')

    def __make_block_tags(self,replace=False):
        for tag in self.block_tags.keys():
            blocks = self.block_tags[tag]
            
            # if no namespace is provided use own
            if ':' in tag:
                namespace = tag.split(':')[0]
                tag_name = tag.split(':')[1]
            else:
                namespace = self.namespace
                tag_name = tag

            path = self.root_data_path + namespace + '/tags/blocks'
            
            # make namespace if doesnt exist
            if not os.path.exists(path):
                os.makedirs(path)
            
            # add minecraft namespace if not provided
            for i in range(len(blocks)):
                if ':' not in blocks[i]:
                    blocks[i] = 'minecraft:' + blocks[i]
            
            # make tag file
            with open(f'{path}/{tag_name}.json','w') as f:
                sub_content = '",\n\t\t"'.join(blocks)
                replace_set = ('true' if replace else 'false')
                f.write(f'{{\n\t"replace":{replace_set},\n\t"values": [\n\t\t"{sub_content}"\n\t]\n}}')

    def __process_function_tags(self,active_tags,replace=False):
        for tag in active_tags.keys():
            # if no namespace is provided use own
            if ':' in tag:
                namespace = tag.split(':')[0]
                tag_name = tag.split(':')[1]
            else:
                namespace = self.namespace
                tag_name = tag

            path = self.root_data_path + namespace + '/tags/functions'
            content = active_tags[tag]
            
            # make namespace if doesnt exist
            if not os.path.exists(path):
                os.makedirs(path)
            
            # make tag file
            with open(f'{path}/{tag_name}.json','w') as f:
                sub_content = '",\n\t\t"'.join(content)
                replace_set = ('true' if replace else 'false')
                f.write(f'{{\n\t"replace":{replace_set},\n\t"values": [\n\t\t"{sub_content}"\n\t]\n}}')

    # * helper functions creation
    def __make_helper_functions(self):
        self.__make_tick_function()
        self.__make_install_function()
        self.__make_uninstall_function()

    def __make_tick_function(self):
        # every tick
        tick_function = self.newFunction('core/tick','core:tick','minecraft:tick')
        self.tick_function = tick_function

    def __make_install_function(self):
        # installer
        install_function = self.newFunction('core/install','core:install','minecraft:load')
        self.install_function = install_function

        # alert players
        install_function.addCommand(tellRichText(f'&aSetup datapack {self.name}!'))

    def __make_uninstall_function(self):
        # uninstaller
        uninstall_function = self.newFunction('core/uninstall','core:uninstall')
        self.uninstall_function = uninstall_function

        # gather all objectives and tags
        all_objectives = []
        all_entity_tags = []
        for function in self.functions:
            all_objectives += function.created_objectives
            all_entity_tags += function.entity_tags_used

        # remove all objectives
        if len(all_objectives) > 0:
            for objective in all_objectives:
                uninstall_function.addCommand('scoreboard objectives remove '+objective)
        
        # remove all tags from all entities
        if len(all_entity_tags) > 0:
            for tag in all_entity_tags:
                uninstall_function.addCommand(f'tag @e[tag={tag}] remove {tag}')
        
        # disable datapack
        uninstall_function.addCommand(f'datapack disable "file/{self.name}"')

        # alert players
        uninstall_function.addCommand(tellRichText(f'&cUninstalled datapack {self.name}!'))
