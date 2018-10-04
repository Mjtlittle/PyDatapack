from .function import *
from .constants import *

def player_first_join(datapack,*functions):
    # vars
    target_tag = datapack.namespace+'_joined'

    # register function/s
    datapack.registerFunctions(functions)


    # make trigger function
    datapack.newFunction(f'{INTERNAL_PREFIX}first_join_trigger','minecraft:tick')

    # add lines for running functions
    for func in functions:
        datapack.last_function.addCommand(f'execute as @a[tag=!{target_tag}] at @s run function {func.target}')
    
    # tag players after complete
    datapack.last_function.addCommand(f'execute as @a[tag=!{target_tag}] run tag @s add {target_tag}')


    # make reset join function
    datapack.newFunction('first_join_reset')
    datapack.last_function.addCommand(f'tag @a[tag={target_tag}] remove {target_tag}')

def carrot_click_trigger(datapack,*functions):
    
    # vars
    objective_name = datapack.standardObjective('carrot_click')

    # register function/s
    datapack.registerFunctions(functions)
    

    # initialize scoreboards
    datapack.newFunction(f'{INTERNAL_PREFIX}carrot_click_init','minecraft:load')
    datapack.last_function.addCommand(f'scoreboard objectives add {objective_name} minecraft.used:minecraft.carrot_on_a_stick')
    datapack.last_function.addCommand(f'scoreboard players set @a {objective_name} 0')


    # tick check
    datapack.newFunction(f'{INTERNAL_PREFIX}carrot_click_trigger','minecraft:tick')

    # call functions from tick
    for func in functions:
        datapack.last_function.addCommand(f'execute as @a[scores={{{objective_name}=1..}}] at @s run function {func.target}')

    # reset score
    datapack.last_function.addCommand(f'scoreboard players set @a[scores={{{objective_name}=1..}}] {objective_name} 0')
    pass

def instant_raycast(
    datapack, name, 
    hit_command=None, 
    traveling_command=None, 
    pass_blocks=AIR_BLOCKS, 
    block_limit=32, iteration_speed=0.5, halt_on_entities=True, is_player=True):

    # ! halt system ???
    # raycast player halt tag
    #halt_tag = f'{name}_raycast_halt'

    # stop function
    #stop_function = datapack.newFunction(f'{INTERNAL_PREFIX}{name}_raycast_stop')
    #stop_function.addCommand('')


    # recursion function
    recursion_function = datapack.newFunction(f'{INTERNAL_PREFIX}{name}_raycast_recursion')

    # raycast pass blocks tag
    pass_blocks_tag = datapack.newBlocksTag(f'{name}_raycast_pass',pass_blocks)

    # traveling command
    if traveling_command != None:
        recursion_function.addCommand(traveling_command)

    #if pass
    working_command = [f'execute if block ~ ~ ~ {pass_blocks_tag} '] # start passing blocks
    
    # block limit
    if block_limit != -1:
        working_command.append(f'unless entity @s[distance={block_limit}..] ')
    
    # hit entity
    if halt_on_entities:
        working_command.append(f'unless entity @e[distance=..1] ')

    working_command.append(f'positioned ^ ^ ^{iteration_speed} run {recursion_function()}') # end
    recursion_function.addCommand(''.join(working_command))

    #else hit
    if hit_command == None:
        if halt_on_entities:
            recursion_function.addCommand(f'execute if entity @e[distance=..1] run {hit_command}')
        recursion_function.addCommand(f'execute unless block ~ ~ ~ {pass_blocks_tag} run {hit_command}')

    # trigger function
    vert_offset = str(PLAYER_HEAD_HEIGHT) if is_player else ''
    trigger_function = datapack.newFunction(f'{INTERNAL_PREFIX}{name}_raycast_trigger')
    trigger_function.addCommand(f'execute as @s rotated as @s at @s positioned ~ ~{vert_offset} ~ run {recursion_function()}')

    return trigger_function

    pass
