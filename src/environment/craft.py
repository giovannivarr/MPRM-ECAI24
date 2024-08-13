import logging
from random import Random
from typing import FrozenSet, List, Mapping, Optional, Sequence, Set, Tuple, Callable

from .environment import ActionId, Environment, Observation, State

from .update_facts import (update_facts_SEQ0, update_facts_SEQ1, update_facts_SEQ2,
                           update_facts_SEQ3, update_facts_SEQ4, update_facts_SEQ5, update_facts_SEQ6,
                           update_facts_POP0, update_facts_POP1, update_facts_POP2,
                           update_facts_bridge_gold_MPRM, update_facts_gold_gem_MPRM,)

ACTIONS: List[Tuple[int, int]] = [
    (0, 1),   # down
    (0, -1),  # up
    (-1, 0),  # left
    (1, 0),   # right
]

# New objects set for our experiments
OBJECTS = dict([(v, k) for k, v in enumerate(
    ["wood", "grass", "iron", "bridge", "stick", "axe", "gold", "gem"])])

def update_facts(facts: Sequence[bool], objects: Observation) -> Set[int]:
    state = set([i for i, v in enumerate(facts) if v])
    for o in objects:
        if o != "gold" and o in OBJECTS:
            # Used for QRM with MaxPOP
            state.add(OBJECTS[o])
            # Used for QRM with individual sequential plans (in this case SEQ-3)
            #if (o == 'wood' and OBJECTS["grass"] in state) or o == 'grass':
            #    state.add(OBJECTS[o])
        #Used for QRM with single POP (in this case POP-0)
        #if o != "gold" and o in ["wood", "iron"]:
        #    state.add(OBJECTS[o])
        elif o == "gold" and OBJECTS["bridge"] in state:
            state.add(OBJECTS[o])
    if "toolshed" in objects:
        # check whether the agent can first make a grass bridge
        if OBJECTS["wood"] in state and OBJECTS["grass"] in state:
            state.add(OBJECTS["bridge"])
            state.remove(OBJECTS["wood"])
            state.remove(OBJECTS["grass"])
        if OBJECTS["wood"] in state:
            state.remove(OBJECTS["wood"])
        if OBJECTS["grass"] in state:
            state.remove(OBJECTS["grass"])
    if "workbench" in objects:
        if OBJECTS["wood"] in state:
            state.remove(OBJECTS["wood"])
        if OBJECTS["iron"] in state:
            state.remove(OBJECTS["iron"])
    if "factory" in objects:
        if OBJECTS["grass"] in state:
            state.remove(OBJECTS["grass"])
        if OBJECTS["iron"] in state and OBJECTS["wood"] in state:
            state.add(OBJECTS["bridge"])
            state.remove(OBJECTS["iron"])
            state.remove(OBJECTS["wood"])

    return state


class CraftState(State):
    facts: Tuple[bool, ...]
    map_data: Tuple[Tuple[Observation, ...], ...]

    def __init__(self, x: int, y: int, facts: Set[int]):
        self.x = x
        self.y = y

        fact_list = [False] * len(OBJECTS)
        for fact in facts:
            fact_list[fact] = True
        self.facts = tuple(fact_list)

        self.uid = (self.x, self.y, self.facts)

    def __str__(self) -> str:
        return "({:2d}, {:2d}, {})".format(self.x, self.y, self.facts)

    @staticmethod
    def random(rng: Random,
               map_data: Sequence[Sequence[Observation]],
               update_facts: Callable) -> 'CraftState':
        # return CraftState(5, 5, set())
        while True:
            y = rng.randrange(len(map_data))
            x = rng.randrange(len(map_data[0]))
            if "wall" not in map_data[y][x]:
                return CraftState(x, y, update_facts((), map_data[y][x]))


MAPPING: Mapping[str, FrozenSet[str]] = {
    'A': frozenset(),
    'X': frozenset(["wall"]),
    'a': frozenset(["wood"]),
    'b': frozenset(["toolshed"]),
    'c': frozenset(["workbench"]),
    'd': frozenset(["grass"]),
    'e': frozenset(["factory"]),
    'f': frozenset(["iron"]),
    'g': frozenset(["gold"]),
    'h': frozenset(["gem"]),
    ' ': frozenset(),
    }


def load_map(map_fn: str) -> Tuple[Tuple[Observation, ...], ...]:
    with open(map_fn) as map_file:
        array = []
        for l in map_file:
            if len(l.rstrip()) == 0:
                continue

            row = []
            for cell in l.rstrip():
                row.append(MAPPING[cell])
            array.append(tuple(row))

    return tuple(array)


class Craft(Environment[CraftState]):
    map_data: Tuple[Tuple[Observation, ...], ...]
    num_actions = 4

    def __init__(self, map_fn: str, rng: Random, agent: str = ''):
        self.map_data = load_map(map_fn)
        self.height = len(self.map_data)
        self.width = len(self.map_data[0])
        self.rng = rng
        self.agent = agent
        self.update_facts = eval("update_facts_" + agent)

        super().__init__(CraftState.random(self.rng, self.map_data, self.update_facts))

    def apply_action(self, a: ActionId):
        x, y = self.state.x + ACTIONS[a][0], self.state.y + ACTIONS[a][1]
        logging.debug("applying action %s:%s", a, ACTIONS[a])
        if x < 0 or y < 0 or x >= self.width or y >= self.height or \
                "wall" in self.map_data[y][x]:
            return set()

        objects = self.map_data[y][x]
        new_facts = self.update_facts(self.state.facts, objects)

        self.state = CraftState(x, y, new_facts)
        logging.debug("success, current state is %s", self.state)

        return objects

    def cost(self, s0: CraftState, a: ActionId, s1: CraftState) -> float:
        return 1.0

    def observe(self, state: CraftState) -> Observation:
        return self.map_data[self.state.y][self.state.x]

    def reset(self, state: Optional[CraftState] = None):
        if state is not None:
            self.state = state
        else:
            self.state = CraftState.random(self.rng, self.map_data, self.update_facts)

    @staticmethod
    def label(state: CraftState) -> FrozenSet[int]:
        return frozenset([i for i in range(len(OBJECTS)) if state.facts[i]])
