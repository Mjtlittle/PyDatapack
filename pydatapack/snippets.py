from .commands import *

def item_frame_on_block_event(item, command, item_rotation=-1,on_block=''):
    parts = [f'execute as @e[type=item_frame, nbt={{Item:{{id:"{item}"}}']

    if item_rotation != -1:
        parts.append(f', ItemRotation: {item_rotation}b')
    
    
    parts.append(f'}}] at @s positioned ^ ^ ^-1 ')

    if on_block != '':
        parts.append(f'if block ~ ~ ~ {on_block} ')
    
    parts.append('run '+command)
    
    return ''.join(parts)

def item_frame_remove_item(selector, reset_rotation=True):
    parts = ['execute as ' ,selector ,' if entity @s[type=item_frame] run data merge entity @s {Item:{id:"minecraft:air",Count:1b}']
    if reset_rotation:
        parts.append(', ItemRotation: 0b')
    parts.append('}')
    return ''.join(parts)

def custom_kill(selector, richtext):
    parts = []
    parts.append(gamerule('showDeathMessages',False))
    parts.append(f'kill {selector}')
    parts.append(gamerule('showDeathMessages'))
    parts.append(tellRichText(richtext))
    return '\n'.join(parts)

def leather_armor_color_value(r,g,b):
    # example item: minecraft:leather_helmet{display:{color:VALUE}}
    return (r << 16) + (g << 8) + b