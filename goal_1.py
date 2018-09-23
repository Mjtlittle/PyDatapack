from pydatapack import *
from pydatapack.commands import *

dp = Datapack('Test Pack','Use anvils to compress sandstone slabs together!')

marker_tag = 'marker_tag'

tick_marker = dp.newFunction('__tick_fire_marker')
tick_marker.addCommand('execute if block ~ ~ ~ minecraft:air run kill @s')
tick_marker.addCommand('particle minecraft:dust 0.2 0.2 0.2 2 ~ ~0.5 ~ 0.2 0.5 0.2 10 1 force')

tick_marker.addCommand('execute if block ~ ~1 ~ minecraft:cauldron[level=3] run particle minecraft:poof ~ ~1.5 ~ 0.1 0 0.1 0 10 force')
tick_marker.addCommand('execute if block ~ ~1 ~ minecraft:cauldron[level=2] run particle minecraft:poof ~ ~1.5 ~ 0.05 0 0.05 0 4 force')
tick_marker.addCommand('execute if block ~ ~1 ~ minecraft:cauldron[level=1] run particle minecraft:poof ~ ~1.5 ~ 0.02 0 0.02 0 2 force')


summon_marker = dp.newFunction('__summon_marker')
#summon_marker.addCommand(f'kill @e[tag={marker_tag},distance=0..0.5]')
summon_marker.addCommand(f'summon armor_stand ~ ~ ~ {{NoGravity:1b,Invulnerable:1b,Invisible:1b,Tags:["{marker_tag}"]}}')
#summon_marker.addCommand('summon fireball ~ ~ ~ {direction:[0.0,-1.0,0.0],power:[0.0,0.0,0.0]}')
summon_marker.addCommand('kill @s')

ontick = dp.newFunction('__on_tick',TAG_ONTICK)
ontick.addCommand(f'execute as @e[type=item,nbt={{Item:{{id:"minecraft:coal"}}}}] at @s align xyz positioned ~0.5 ~0.5 ~0.5 if block ~ ~ ~ minecraft:fire run function {summon_marker.target}')
ontick.addCommand(f'execute as @e[tag={marker_tag}] at @s run function {tick_marker.target}')

make_place_debug(dp,'D:/Games/Minecraft/Instances/Official/saves/Datapack Testing/datapacks')





#ontick.addCommand(f'execute as @e[type=falling_block,nbt={{BlockState:{{Name:"minecraft:anvil"}}}}] at @s run function {tick_fire_marker.target}'')

