# PyDatapack

A python library for creating Minecraft Datapacks!

## Introduction

The examples below are combined into a python file located in the examples folder.

## Importing the Library

```python
from pydatapack import *
```

### Creating a Datapack

```python
dp = Datapack('.','Name','Description')
```

### Making a Function

Functions are objects defined in the library to hold all of the commands run when called in the game. Using `.newFunction()` on the datapack pre registers the function with the datapack. This method also returns the Function object created.

```python
hello = dp.functions.newFunction('hello_world')
hello.add_command('say hello')
hello.add_command(tellraw('world!'))
```

A function can be defined before the datapack, and then added afterwards.

```python
hello = functions.Function('hello_world')
hello.add_command('say hello')
hello.add_command(tellraw('world!'))

dp.functions.registerFunction(hello)
```

### Calling a Function from another

Calling the function (`function_name()`) as if it were a python function converts it to a runnable minecraft command.

```python
wrapper = dp.newFunction('hello_world_wrapper')
wrapper.add_command(hello())
```

### Compiling the Datapack

compiling the datapack with `.compile()` places the unzipped datapack in the current directory.

```python
dp.compile()
```