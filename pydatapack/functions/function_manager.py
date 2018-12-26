from .function import Function
from .commands import tellRichText

import os
import sys

class FunctionManager:
    def __init__(self, datapack):
        
        self.datapack = datapack
        self.functions = []

        self.__make_helper_functions()

    def new(self, target, *tags):
        """Create a new function. Returns the function object created."""

        # register and create function
        function = Function(target)
        self.register(function)

        # add tags
        for tag in tags:
            self.datapack.tags.tag_function(tag, function.target)

        return function

    def register(self, function):
        """Register a function into the datapack. Returns the function object provided."""

        # function already in datapack
        if function in self.functions:
            return False

        # assign namespace if none given
        if function.namespace == None:
            function.namespace = self.datapack.namespace

        self.functions.append(function)
        return function

    @property
    def last(self):
        return self.functions[-1]
    
    def compile(self):
        
        # process functions
        for function in self.functions:

            path = self.datapack.root_data_path + function.namespace + '/functions' + (f'/{function.parentStructure}' if function.parentStructure != None else '')

            # make directory if doesnt exist
            if not os.path.exists(path):
                os.makedirs(path)

            # write file for function
            with open(f'{path}/{function.name}.mcfunction','w') as f:
                f.write(function.raw_text())

    # * helper functions creation
    def __make_helper_functions(self):
        self.__make_tick_function()
        self.__make_reload_function()

        self.__make_install_function()
        self.__make_uninstall_function()

    def __make_tick_function(self):
        # every tick
        tick_function = self.new('core/tick','core:tick','minecraft:tick')
        self.tick_function = tick_function

    def __make_reload_function(self):
        # installer
        reload_function = self.new('core/reload','core:reload','minecraft:load')
        self.reload_function = reload_function

        # alert players
        reload_function.add_command(tellRichText(f'&6Reloaded datapack {self.datapack.name}!'))

    def __make_install_function(self):
        # installer
        install_function = self.new('core/install','core:install')
        self.install_function = install_function

        # alert players
        install_function.add_command(tellRichText(f'&aSetup datapack {self.datapack.name}!'))

    def __make_uninstall_function(self):
        # uninstaller
        uninstall_function = self.new('core/uninstall','core:uninstall')
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
                uninstall_function.add_command('scoreboard objectives remove '+objective)
        
        # remove all tags from all entities
        if len(all_entity_tags) > 0:
            for tag in all_entity_tags:
                uninstall_function.add_command(f'tag @e[tag={tag}] remove {tag}')
        
        # disable datapack
        uninstall_function.add_command(f'datapack disable "file/{self.datapack.name}"')

        # alert players
        uninstall_function.add_command(tellRichText(f'&cUninstalled datapack {self.datapack.name}!'))
