from . import constants

import string
import json
import random

def escapeJson(text):
    return json.dumps(text)[1:-1]

def formatNamespace(name):
    valid_chars = string.ascii_lowercase + string.digits + '_'
    namespace = []
    for char in name.lower():
        if char in valid_chars:
            namespace.append(char)
        if char == ' ':
            namespace.append('_')
    if namespace[0] in string.digits:
        namespace.insert(0,'_')
    
    return ''.join(namespace)

def mangleObjective(namespace, name, length=16):
    random.seed(namespace)
    nsu = 5-len(namespace) if len(namespace) < 5 else 0
    nu = 7-len(name) if len(name) < 7 else 0
    c = ''.join([random.choice(constants.VALID_OBJECTIVE_CHARACTERS) for _ in range((length-5-7)+nsu+nu)])
    return namespace[:5] + c + name[:7]

def inferMCNamespace(block):
    if ':' not in block:
        return f'minecraft:{block}'
    return block

class TextSegment:
    def __init__(self, text=None):
        self.working_text = []

        if text != None:
            self.working_text.append(text)

        self.selector = False

        self.color = None
        self.obfuscated = False
        self.bold = False
        self.strikethrough = False
        self.underlined = False
        self.italic = False

        self.hover_text = None
        self.click_command = None

    @property
    def text(self):
        return ''.join(self.working_text)

    @text.setter
    def text(self,value):
       self.working_text = [value]
    
    @property
    def empty(self):
        return len(self.working_text) == 0
    
    def append(self, value):
        self.working_text.append(value)

    def insert(self, i, value):
        self.working_text.insert(i,value)
    
    def __str__(self):
        return self.render()

    def render(self):
        final_text = ''.join(self.working_text)
        

        if self.selector:
            working_output = [f'{{"selector":"{final_text}"']
        else:
            working_output = [f'{{"text":"{final_text}"']

        # color
        if self.color != None:
            working_output.append(f',"color":"{self.color}"')

        # attributes
        for part in ['obfuscated','bold','strikethrough','underlined','italic']:
            if getattr(self,part):
                working_output.append(f',"{part}":true')
        
        # hover text
        if self.hover_text != None:
            working_output.append(f',"hoverEvent":{{"action":"show_text","value":"{self.hover_text}"}}')

        # click event
        if self.click_command != None:
            working_output.append(f',"clickEvent":{{"action":"run_command","value":"{self.click_command}"}}')
    
        working_output.append('}')
        return ''.join(working_output)

class NamespaceAdressable:
    def __init__(self, target):
        self.target = target

    @property
    def name(self):
        # remove namespace if provided
        target = self.target
        if ':' in target:
            target = target.split(':')[1]

        # get name if in subdirectories
        if '/' in target:
            return target.split('/')[-1]
        else:
            return target
            
    @property
    def namespace(self):
        if ':' in self.target:
            return self.target.split(':')[0]
        else:
            return None

    @namespace.setter
    def namespace(self, value):
        if ':' in self.target:
            self.target = value+':'+self.target.split(':')[1]
        else:
            self.target = value+':'+self.target
        return True

    @property
    def parentStructure(self):
        # remove namespace if provided
        target = self.target
        if ':' in target:
            target = target.split(':')[1]

        if '/' in target:
            return '/'.join(target.split('/')[:-1])
        else:
            return None