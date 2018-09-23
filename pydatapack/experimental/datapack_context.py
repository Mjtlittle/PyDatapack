from .function import *
from .datapack import *

class DatapackContext:
    def __init__(self,datapack):
        self.datapack = datapack

        # initialize variable engine
        init = self.datapack.newFunction('internal/init','minecraft:load')
        init.addCommand('scoreboard objectives ')
    
    def var_set(var,value):

    
    def var_op(expression):

    def var_if(conditional,function):

class VarSystem:
    def __init__(self):
        
        pass
    
    def set_value(self,variable,value):
