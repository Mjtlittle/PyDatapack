from ..internals import inferMCNamespace
import os

class TagManager:
    def __init__(self, datapack):
        self.datapack = datapack

        self.function_tags = {}
        self.block_tags = {}
        self.item_tags = {}

    def compile(self):
        self.__process_function_tags()
        self.__process_block_tags()
        self.__process_item_tags()

    #* Functions
    def new_function_tag(self, tag, function_targets=[]):
        
        # if no namespace is provided use own
        if ':' not in tag:
            tag = f'{self.datapack.namespace}:{tag}'

        # add blank tag
        self.function_tags[tag] = []

        # tag the functions
        for function in function_targets:
            self.tag_function(tag, function)

        # return tag target
        return f'#{tag}'

    def tag_function(self, tag, function_target):

        # if no namespace is provided use own
        if ':' not in tag:
            tag = f'{self.datapack.namespace}:{tag}'

        # create tag if doesnt exist
        if tag not in self.function_tags.keys():
            self.new_function_tag(tag)

        # add tag
        self.function_tags[tag].append(function_target)

        # return tag target
        return f'#{tag}'

    def __process_function_tags(self, replace=False):
        
        # iterate over all tags
        for tag in self.function_tags.keys():
            
            namespace = tag.split(':')[0]
            tag_name = tag.split(':')[1]
            path = self.datapack.root_data_path + namespace + '/tags/function'
            content = self.function_tags[tag]
            
            # make namespace if doesnt exist
            if not os.path.exists(path):
                os.makedirs(path)
            
            # make tag file
            with open(f'{path}/{tag_name}.json','w') as f:
                sub_content = '",\n\t\t"'.join(content)
                replace_set = ('true' if replace else 'false')
                f.write(f'{{\n\t"replace":{replace_set},\n\t"values": [\n\t\t"{sub_content}"\n\t]\n}}')

    #* Blocks
    def new_block_tag(self, tag, blocks=[]):
        
        # if no namespace is provided use own
        if ':' not in tag:
            tag = self.datapack.namespace + ':' + tag
        
        # add blank tag
        self.block_tags[tag] = []

        # tag the blocks
        for block in blocks:
            self.tag_block(tag, block)

        # return tag target
        return f'#{tag}'

    def tag_block(self, tag, block):
        
        # if no namespace is provided use own
        if ':' not in tag:
            tag = self.datapack.namespace + ':' + tag

        # create tag if doesnt exist
        if tag not in self.block_tags.keys():
            self.new_block_tag(tag)

        # add tag
        self.block_tags[tag].append(inferMCNamespace(block))

        # return tag target
        return f'#{tag}'

    def __process_block_tags(self, replace=False):

        # iterate over all tags
        for tag in self.block_tags.keys():

            blocks = self.block_tags[tag]
            namespace = tag.split(':')[0]
            tag_name = tag.split(':')[1]
            path = self.datapack.root_data_path + namespace + '/tags/blocks'
            
            # make namespace if doesnt exist
            if not os.path.exists(path):
                os.makedirs(path)
            
            # make tag file
            with open(f'{path}/{tag_name}.json','w') as f:
                sub_content = '",\n\t\t"'.join(blocks)
                replace_set = ('true' if replace else 'false')
                f.write(f'{{\n\t"replace":{replace_set},\n\t"values": [\n\t\t"{sub_content}"\n\t]\n}}')

    #* Items
    def new_item_tag(self, tag, items=[]):
        
        # if no namespace is provided use own
        if ':' not in tag:
            tag = self.datapack.namespace + ':' + tag
        
        # add blank tag
        self.item_tags[tag] = []

        # tag the items
        for item in items:
            self.tag_item(tag, item)

        # return tag target
        return f'#{tag}'

    def tag_item(self, tag, item):
        
        # if no namespace is provided use own
        if ':' not in tag:
            tag = self.datapack.namespace + ':' + tag

        # create tag if doesnt exist
        if tag not in self.item_tags.keys():
            self.new_item_tag(tag)

        # add tag
        self.item_tags[tag].append(inferMCNamespace(item))

        # return tag target
        return f'#{tag}'

    def __process_item_tags(self, replace=False):

        # iterate over all tags
        for tag in self.item_tags.keys():

            items = self.item_tags[tag]
            namespace = tag.split(':')[0]
            tag_name = tag.split(':')[1]
            path = self.datapack.root_data_path + namespace + '/tags/items'
            
            # make namespace if doesnt exist
            if not os.path.exists(path):
                os.makedirs(path)
            
            # make tag file
            with open(f'{path}/{tag_name}.json','w') as f:
                sub_content = '",\n\t\t"'.join(items)
                replace_set = ('true' if replace else 'false')
                f.write(f'{{\n\t"replace":{replace_set},\n\t"values": [\n\t\t"{sub_content}"\n\t]\n}}')
