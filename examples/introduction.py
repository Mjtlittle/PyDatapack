from pydatapack import implementations
from pydatapack import snippets
from pydatapack import debug
from pydatapack import *

# creating datapacks
dp = Datapack('Name','Description')

# creating functions
hello = dp.newFunction('hello_world')
hello.addCommand('say hello')
hello.addCommand(tellraw('world!'))

# calling functions
wrapper = dp.newFunction('hello_world_wrapper')
wrapper.addCommand(hello())

# compiling the datapack
dp.compile()