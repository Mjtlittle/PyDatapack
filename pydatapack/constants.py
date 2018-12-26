import string
import json
import sys

TAG_ONLOAD = 'minecraft:load'
TAG_ONTICK = 'minecraft:tick'

PLAYER_HEAD_HEIGHT = 1.62000000476837

AIR_BLOCKS = ['minecraft:air','minecraft:cave_air','minecraft:void_air']
DYE_COLORS = ['white','orange','magenta','light_blue','yellow','lime','pink','gray','light_gray','cyan','purple','blue','brown','green','red','black']

INTERNAL_PREFIX = 'internal/'
VALID_OBJECTIVE_CHARACTERS = list(string.ascii_letters + string.digits + '_-.+')
GAMERULE_DEFUALTS = json.load(open('pydatapack/data/gamerule_defualts.json'))
