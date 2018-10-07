from pydatapack import implementations
from pydatapack import snippets
from pydatapack import debug
from pydatapack import *

from colorsys import hsv_to_rgb
import math

dp = Datapack('Test Pack','--')

nudge = dp.newFunction('nudge')
nudge.addCommand('clone ~ ~ ~ ~ ~ ~ ^ ^ ^1')
nudge.addCommand(setblock('minecraft:air'))
nudge.addCommand('tp @s ^ ^ ^1')
nudge.addCommand('particle minecraft:dust 1.0 0.0 0.0 1.0 ~ ~ ~ 1 1 1 1 100 force')
nudge.addCommand('kill @s')

# trigg = dp.newFunction('trigg')
# trigg.addCommand(snippets.custom_kill('@s was killed by a falling peice of shit!'))
# implementations.carrot_click_trigger(dp,trigg)

# this is a test


# colorful armor
amount = 255
radius = 10
test = dp.newFunction('armor_wall')

#test.addCommand(f'fill ~ ~-1 ~ ~ ~ ~{amount-1} minecraft:stone')
for i in range(amount):
    color = snippets.leather_armor_color_value(*map(lambda v: int(v*255), hsv_to_rgb(i/amount,1,1)))
    x = math.cos(i/amount*math.pi*2)*radius
    y = math.sin(i/amount*math.pi*2)*radius
    w = math.sin(i/amount*math.pi*2*10)*2
    rot = i/amount*360
    test.addCommand(f'summon armor_stand ~{round(x,3)} ~{round(w,3)} ~{round(y,3)} {{NoGravity:1b,Invisible:1b,NoBasePlate:1b,Rotation:[{rot}F,0F],ArmorItems:[{{id:"minecraft:leather_boots",Count:1b,tag:{{display:{{color:{color}}}}}}},{{id:"minecraft:leather_leggings",Count:1b,tag:{{display:{{color:{color}}}}}}},{{id:"minecraft:leather_chestplate",Count:1b,tag:{{display:{{color:{color}}}}}}},{{id:"minecraft:leather_helmet",Count:1b,tag:{{display:{{color:{color}}}}}}}]}}')

test.addCommand('clear @s minecraft:carrot_on_a_stick')
implementations.carrot_click_trigger(dp,test)


dp.tick_function.addCommand(snippets.item_frame_connected_block('minecraft:cobblestone',nudge()))


debug.move_datapack(dp,'D:/Games/Minecraft/Instances/Official/saves/Datapack Testing/datapacks')
