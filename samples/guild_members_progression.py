#! /usr/bin/env python

# standard Python modules
import sys
import os

# the battlenet modules
import battlenet
from battlenet import Guild
from battlenet import Raid

# load your key if existing
PUBLIC_KEY = os.environ.get('BNET_PUBLIC_KEY')
PRIVATE_KEY = os.environ.get('BNET_PRIVATE_KEY')

# the existing region
regions = {
    'us': battlenet.UNITED_STATES,
    'eu': battlenet.EUROPE,
    'kr': battlenet.KOREA,
    'tw': battlenet.TAIWAN,
}

if __name__ == '__main__':

    # read parameters
    region = regions[sys.argv[1]]
    realm_name = sys.argv[2]
    guild_name = sys.argv[3]

    # open set connection
    battlenet.Connection.setup(public_key=PUBLIC_KEY, private_key=PRIVATE_KEY, locale='fr')

    # load the guild
    guild = Guild(region, realm_name, guild_name)

    # display the kills of all the guild members
    nb_level_85 = 0
    for character in guild.members:
        if character['character'].level != 85:
            continue
        nb_level_85 += 1
        print character['character'].name
        try:
            for r in character['character'].progression['raids']:
                print '\t%s (%s)' % (r.name, Raid(r.id).expansion()[0])
                for b in r.bosses:
                    print '\t\tN: %2d H: %2d %s' % (b.normal, b.heroic, b.name)
        except battlenet.CharacterNotFound:
            print '\tNOT FOUND'

    print nb_level_85, 'characters level 85'
