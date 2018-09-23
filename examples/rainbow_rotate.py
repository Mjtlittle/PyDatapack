import sys
sys.path[0] = '\\'.join(sys.path[0].split('\\')[0:-1])

from pydatapack import implementations
from pydatapack import snippets
from pydatapack import debug
from pydatapack import *

from colorsys import hsv_to_rgb
import math

# settings
amount = 255
radius = 5
speed = 3
tag_prefix = 'rainbow_'

# create datapack
dp = Datapack('Rainbow Rotate','summon a rainbow disk with the carrot on a stick')

# summon
summon_stands = dp.newFunction('summon_armorstands')
for i in range(amount):
    x = math.cos(i/amount*math.pi*2)*radius
    y = math.sin(i/amount*math.pi*2)*radius
    w = 0#math.sin(i/amount*math.pi*2*10)*2
    rot = (i/amount*360)%360
    summon_stands.addCommand(f'summon armor_stand ~{round(x,3)} ~{round(w,3)} ~{round(y,3)} {{NoGravity:1b,Invisible:1b,NoBasePlate:1b,Tags:["{tag_prefix}{i}"],Rotation:[{rot}F,0F]}}')

#summon_stands.addCommand('clear @s minecraft:carrot_on_a_stick')
implementations.carrot_click_trigger(dp,summon_stands)

# experimental summon sphere
layers = 20
max_amount = 30
summon_sphere = dp.newFunction('piller_summon')
for h in range(layers):
    sr = math.sin(h/layers*math.pi)*radius
    z = math.cos(h/layers*math.pi)*radius
    sa = int(sr/radius*max_amount)

    for i in range(sa):
        x = math.cos(i/sa*math.pi*2)*sr
        y = math.sin(i/sa*math.pi*2)*sr
        
        rot = (i/sa*360)%360
        summon_sphere.addCommand(f'summon armor_stand ~{round(x,3)} ~{round(z,3)} ~{round(y,3)} {{NoGravity:1b,Invisible:1b,NoBasePlate:1b,Tags:["{tag_prefix}{(i+h)%amount}"],Rotation:[{rot}F,0F]}}')

# id shifter
shift_ids = dp.newFunction('shift_ids')
# marker
for i in range(amount):
    shift_ids.addCommand(f'tag @e[tag={tag_prefix}{i}] add {tag_prefix}{i}_t')
    shift_ids.addCommand(f'tag @e[tag={tag_prefix}{i}_t] remove {tag_prefix}{i}')
# enforcer
for i in range(amount):
    new_i = (i+speed) % amount
    shift_ids.addCommand(f'tag @e[tag={tag_prefix}{i}_t] add {tag_prefix}{new_i}')
    shift_ids.addCommand(f'tag @e[tag={tag_prefix}{i}_t] remove {tag_prefix}{i}_t')

# update color to id
update_color = dp.newFunction('update_color')
for i in range(amount):
    color = snippets.leather_armor_color_value(*map(lambda v: int(v*255), hsv_to_rgb(i/amount,1,1)))
    update_color.addCommand(f'execute as @e[tag={tag_prefix}{i}] run data merge entity @s {{ArmorItems:[{{id:"minecraft:leather_boots",Count:1b,tag:{{display:{{color:{color}}}}}}},{{id:"minecraft:leather_leggings",Count:1b,tag:{{display:{{color:{color}}}}}}},{{id:"minecraft:leather_chestplate",Count:1b,tag:{{display:{{color:{color}}}}}}},{{id:"minecraft:leather_helmet",Count:1b,tag:{{display:{{color:{color}}}}}}}]}}')

# tick color rotation
tick_rotation = dp.newFunction('tick_color_rot','minecraft:tick')
tick_rotation.addCommand(shift_ids())
tick_rotation.addCommand(update_color())

c = 0
for func in dp.functions:
    c += len(str(func).split('\n'))
print(c)

debug.move_datapack(dp,'D:/Games/Minecraft/Instances/Official/saves/Datapack Testing/datapacks')