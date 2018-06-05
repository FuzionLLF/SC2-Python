# This file will contain all actions
# ADD SOME ACTIONS
# SHOULD TAKE IN FULL OBSERVATIONS
# move these to an actions.py?
# Maybe these actions should return a list of functions to be called.
# In our agent we can then use a state machine to iterate through the action list.
# Would allow much more dynamic actions I think.

# Nothing
from pysc2.lib import actions
from pysc2.lib import features

import random

from BuildQueues import Zerg

_PLAYER_RELATIVE = features.SCREEN_FEATURES.player_relative.index
_PLAYER_SELF = 1
_PLAYER_FRIENDLY = 1
_PLAYER_NEUTRAL = 3  # beacon/minerals
_PLAYER_HOSTILE = 4
_MOVE_SCREEN = actions.FUNCTIONS.Move_screen.id
_ATTACK_SCREEN = actions.FUNCTIONS.Attack_screen.id
_SELECT_ARMY = actions.FUNCTIONS.select_army.id
_NOT_QUEUED = [0]
_SELECT_ALL = [0]
_NO_OP = actions.FUNCTIONS.no_op.id
_SELECT_POINT = actions.FUNCTIONS.select_point.id
_BUILD_SUPPLY_DEPOT = actions.FUNCTIONS.Build_SupplyDepot_screen.id
_BUILD_BARRACKS = actions.FUNCTIONS.Build_Barracks_screen.id
_ATTACK_MINIMAP = actions.FUNCTIONS.Attack_minimap.id
_RALLY_UNITS = actions.FUNCTIONS.Rally_Units_minimap.id
_UNIT_TYPE = features.SCREEN_FEATURES.unit_type.index
_PLAYER_ID = features.SCREEN_FEATURES.player_id.index

_MAP_SIZE = 128


def no_op():
    """THIS IS THE NO OPERATION ACTION"""
    return [actions.FunctionCall(actions.FUNCTIONS.no_op.id, [])]


# Build actions
def build_building(obs, building, x, y):
    """Build next building in build order.
    Actions will be select drone. Build building. """
    building_actions = []

    units = obs.observation['screen'][_UNIT_TYPE]
    d_target = [0, 0]  # makybe put a better init value here

    # pycharm won't recognize numpy's overloaded == operator.
    drone_x, drone_y = (units == Zerg.Drone).nonzero()
    if drone_y.any():
        i = random.randint(0, len(drone_y) - 1)
        d_target = [drone_x[i], drone_y[i]]
    else:
        return [actions.FunctionCall(actions.FUNCTIONS.no_op.id, [])]
    # pycharm won't recognize numpy's overloaded == operator.
    hatch_x, hatch_y = (units == Zerg.Hatchery).nonzero()

    if hatch_y.any():
        h_target = [hatch_x.mean() + x, hatch_y.mean() + y]
        return [actions.FunctionCall(building, [_NOT_QUEUED, h_target]),
                actions.FunctionCall(_SELECT_POINT, [_NOT_QUEUED, d_target])]
    return [actions.FunctionCall(actions.FUNCTIONS.no_op.id, [])]


def build_units(unit):
    """Build more units. Maybe separate into military and worker?"""
    # Train next unit in military build order
    return [actions.FunctionCall(unit, [_NOT_QUEUED])]


def build_worker(drone_func):
    """Build workers"""
    # Select hatchery with available larvae
    # Build drone
    return [actions.FunctionCall(drone_func, [_NOT_QUEUED])]


def get_materials(obs):
    """Send drone to nearest unoccupied mineral/gas deposit, Select drone, move to nearest mineral/gas deposit"""
    # Claimed by Greg
    pass


def research(obs):
    """get upgrades going. Maybe abstract this into build?"""
    # Research next upgrade in research build order
    pass


def cancel(obs):
    """Cancel build queue. To free up resources? May be to complicated of action for learner to consider."""


# View control
def move_view(obs):
    """Move screen/ minimap to see more. This is the action that will fuck us."""


# Unit Control
def attack(obs):
    """General Attack Function."""
    # Have army attack enemy base/enemy army
    # If possible, keep roaches and ultralisks at the front of the army and hydralisks at the rear

    enemy_y, enemy_x = (obs.observation['screen'][_PLAYER_RELATIVE] == _PLAYER_HOSTILE).nonzero()
    if enemy_y.any():
        x, y = enemy_x.mean(), enemy_y.mean()

        return [actions.FunctionCall(_ATTACK_MINIMAP, [_NOT_QUEUED, x, y]),
                actions.FunctionCall(_SELECT_ARMY, [_NOT_QUEUED])]
    else:
        return [actions.FunctionCall(actions.FUNCTIONS.no_op.id, [])]
def defend(obs):
    """Send units to defensive"""
    # Send army to base
    # Move defensive structures up in priority?

    # Select army

    # Move to base


def patrol(obs):
    """Make it part of defend?"""


def return_to_base(rally_x, rally_y):
    """Move units to some rally_x & rally_y. This should be an offset from the hatchery."""
    return [actions.FunctionCall(_SELECT_ARMY, [_NOT_QUEUED]),
            actions.FunctionCall(_MOVE_SCREEN, [_NOT_QUEUED, rally_x, rally_y])]

# Maybe these could be part of the other actions:

# def spawn_larvae(obs):
# Spawn larvae

# Select queen

# Use spawn larvae ability

# Target nearest hatchery/lair/hive

# def spread_creep(obs):
# Spawn creep tumor and have all available creep tumors spawn another

# Spawn creep tumor
# Select queen
# Use Spawn creep tumor ability
# Target the edge of the creep

# Spread creep tumors
# For all creep tumors:
# Select the tumor
# Use Spawn creep tumor ability (if available, if not go to the next creep tumor)
# Target as far away as possible
