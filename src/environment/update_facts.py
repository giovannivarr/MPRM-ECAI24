from typing import Sequence, Set
from .environment import Observation

OBJECTS = dict([(v, k) for k, v in enumerate(
    ["wood", "grass", "iron", "bridge", "stick", "axe", "gold", "gem"])])

def update_facts_bridge_gold_MPRM(facts: Sequence[bool], objects: Observation) -> Set[int]:
    state = set([i for i, v in enumerate(facts) if v])
    for o in objects:
        if o != "gold" and o in OBJECTS:
            state.add(OBJECTS[o])
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


def update_facts_SEQ0(facts: Sequence[bool], objects: Observation) -> Set[int]:
    state = set([i for i, v in enumerate(facts) if v])
    for o in objects:
        if o != "gold" and o in OBJECTS:
            if (o == 'iron' and OBJECTS["wood"] in state) or o == 'wood':
                state.add(OBJECTS[o])
        elif o == "gold" and OBJECTS["bridge"] in state:
            state.add(OBJECTS[o])
    if "toolshed" in objects:
        if OBJECTS["wood"] in state:
            state.remove(OBJECTS["wood"])
    if "workbench" in objects:
        if OBJECTS["wood"] in state:
            state.remove(OBJECTS["wood"])
        if OBJECTS["iron"] in state:
            state.remove(OBJECTS["iron"])
    if "factory" in objects:
        if OBJECTS["iron"] in state and OBJECTS["wood"] in state:
            state.add(OBJECTS["bridge"])
            state.remove(OBJECTS["iron"])
            state.remove(OBJECTS["wood"])
        if OBJECTS["wood"] in state:
            state.remove(OBJECTS["wood"])
        if OBJECTS["iron"] in state:
            state.remove(OBJECTS["iron"])

    return state

def update_facts_SEQ1(facts: Sequence[bool], objects: Observation) -> Set[int]:
    state = set([i for i, v in enumerate(facts) if v])
    for o in objects:
        if o != "gold" and o in OBJECTS:
            if (o == 'grass' and OBJECTS["wood"] in state) or o == 'wood':
                state.add(OBJECTS[o])
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
    if "factory" in objects:
        if OBJECTS["grass"] in state:
            state.remove(OBJECTS["grass"])
        if OBJECTS["wood"] in state:
            state.remove(OBJECTS["wood"])

    return state


def update_facts_SEQ2(facts: Sequence[bool], objects: Observation) -> Set[int]:
    state = set([i for i, v in enumerate(facts) if v])
    for o in objects:
        if o != "gold" and o in OBJECTS:
            if (o == 'wood' and OBJECTS["iron"] in state) or o == 'iron':
                state.add(OBJECTS[o])
        elif o == "gold" and OBJECTS["bridge"] in state:
            state.add(OBJECTS[o])
    if "toolshed" in objects:
        if OBJECTS["wood"] in state:
            state.remove(OBJECTS["wood"])
    if "workbench" in objects:
        if OBJECTS["wood"] in state:
            state.remove(OBJECTS["wood"])
        if OBJECTS["iron"] in state:
            state.remove(OBJECTS["iron"])
    if "factory" in objects:
        if OBJECTS["iron"] in state and OBJECTS["wood"] in state:
            state.add(OBJECTS["bridge"])
            state.remove(OBJECTS["iron"])
            state.remove(OBJECTS["wood"])
        if OBJECTS["wood"] in state:
            state.remove(OBJECTS["wood"])
        if OBJECTS["iron"] in state:
            state.remove(OBJECTS["iron"])

    return state

def update_facts_SEQ3(facts: Sequence[bool], objects: Observation) -> Set[int]:
    state = set([i for i, v in enumerate(facts) if v])
    for o in objects:
        if o != "gold" and o in OBJECTS:
            if (o == 'wood' and OBJECTS["grass"] in state) or o == 'grass':
                state.add(OBJECTS[o])
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
    if "factory" in objects:
        if OBJECTS["grass"] in state:
            state.remove(OBJECTS["grass"])
        if OBJECTS["wood"] in state:
            state.remove(OBJECTS["wood"])

    return state


def update_facts_POP0(facts: Sequence[bool], objects: Observation) -> Set[int]:
    state = set([i for i, v in enumerate(facts) if v])
    for o in objects:
        if o in ["wood", "iron"]:
            state.add(OBJECTS[o])
        elif o == "gold" and OBJECTS["bridge"] in state:
            state.add(OBJECTS[o])
    if "toolshed" in objects:
        if OBJECTS["wood"] in state:
            state.remove(OBJECTS["wood"])
    if "workbench" in objects:
        if OBJECTS["wood"] in state:
            state.remove(OBJECTS["wood"])
        if OBJECTS["iron"] in state:
            state.remove(OBJECTS["iron"])
    if "factory" in objects:
        if OBJECTS["iron"] in state and OBJECTS["wood"] in state:
            state.add(OBJECTS["bridge"])
            state.remove(OBJECTS["iron"])
            state.remove(OBJECTS["wood"])
        if OBJECTS["wood"] in state:
            state.remove(OBJECTS["wood"])
        if OBJECTS["iron"] in state:
            state.remove(OBJECTS["iron"])

    return state

def update_facts_POP1(facts: Sequence[bool], objects: Observation) -> Set[int]:
    state = set([i for i, v in enumerate(facts) if v])
    for o in objects:
        if o != "gold" and o in ["wood", "grass"]:
            state.add(OBJECTS[o])
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
    if "factory" in objects:
        if OBJECTS["grass"] in state:
            state.remove(OBJECTS["grass"])
        if OBJECTS["wood"] in state:
            state.remove(OBJECTS["wood"])

    return state

def update_facts_gold_gem_MPRM(facts: Sequence[bool], objects: Observation) -> Set[int]:
    state = set([i for i, v in enumerate(facts) if v])
    for o in objects:
        if o not in ["gold", "gem"] and o in OBJECTS:
            state.add(OBJECTS[o])
        elif o == "gold" and OBJECTS["bridge"] in state:
            state.add(OBJECTS[o])
        elif o == "gem" and OBJECTS["axe"] in state:
            state.add(OBJECTS[o])
    if "toolshed" in objects:
        # check whether the agent can first make a grass bridge
        if OBJECTS["wood"] in state and OBJECTS["grass"] in state:
            state.add(OBJECTS["bridge"])
            state.remove(OBJECTS["wood"])
            state.remove(OBJECTS["grass"])
        if OBJECTS["stick"] in state and OBJECTS["iron"] in state:
            state.add(OBJECTS["axe"])
            state.remove(OBJECTS["stick"])
            state.remove(OBJECTS["iron"])
        if OBJECTS["wood"] in state:
            state.remove(OBJECTS["wood"])
        if OBJECTS["grass"] in state:
            state.remove(OBJECTS["grass"])
        if OBJECTS["iron"] in state:
            state.remove(OBJECTS["iron"])
    if "workbench" in objects:
        if OBJECTS["wood"] in state:
            state.remove(OBJECTS["wood"])
            state.add(OBJECTS["stick"])
        if OBJECTS["iron"] in state:
            state.remove(OBJECTS["iron"])
    if "factory" in objects:
        if OBJECTS["iron"] in state and OBJECTS["wood"] in state:
            state.add(OBJECTS["bridge"])
            state.remove(OBJECTS["iron"])
            state.remove(OBJECTS["wood"])
        if OBJECTS["grass"] in state:
            state.remove(OBJECTS["grass"])
        if OBJECTS["wood"] in state:
            state.remove(OBJECTS["wood"])
        if OBJECTS["iron"] in state:
            state.remove(OBJECTS["iron"])

    return state

def update_facts_SEQ4(facts: Sequence[bool], objects: Observation) -> Set[int]:
    state = set([i for i, v in enumerate(facts) if v])
    for o in objects:
        if o != "gem" and o in OBJECTS:
            if (o == 'iron' and OBJECTS["stick"] in state) or o == 'wood':
                state.add(OBJECTS[o])
        elif o == "gem" and OBJECTS["axe"] in state:
            state.add(OBJECTS[o])
    if "toolshed" in objects:
        if OBJECTS["stick"] in state and OBJECTS["iron"] in state:
            state.add(OBJECTS["axe"])
            state.remove(OBJECTS["stick"])
            state.remove(OBJECTS["iron"])
        if OBJECTS["wood"] in state:
            state.remove(OBJECTS["wood"])
        if OBJECTS["grass"] in state:
            state.remove(OBJECTS["grass"])
        if OBJECTS["iron"] in state:
            state.remove(OBJECTS["iron"])
    if "workbench" in objects:
        if OBJECTS["wood"] in state:
            state.add(OBJECTS["stick"])
            state.remove(OBJECTS["wood"])
        if OBJECTS["iron"] in state:
            state.remove(OBJECTS["iron"])
    if "factory" in objects:
        if OBJECTS["grass"] in state:
            state.remove(OBJECTS["grass"])
        if OBJECTS["wood"] in state:
            state.remove(OBJECTS["wood"])
        if OBJECTS["iron"] in state:
            state.remove(OBJECTS["iron"])

    return state

def update_facts_SEQ5(facts: Sequence[bool], objects: Observation) -> Set[int]:
    state = set([i for i, v in enumerate(facts) if v])
    for o in objects:
        if o != "gem" and o in OBJECTS:
            if (o == 'wood' and OBJECTS["iron"] in state) or o == 'iron':
                state.add(OBJECTS[o])
        elif o == "gem" and OBJECTS["axe"] in state:
            state.add(OBJECTS[o])
    if "toolshed" in objects:
        if OBJECTS["stick"] in state and OBJECTS["iron"] in state:
            state.add(OBJECTS["axe"])
            state.remove(OBJECTS["stick"])
            state.remove(OBJECTS["iron"])
        if OBJECTS["wood"] in state:
            state.remove(OBJECTS["wood"])
        if OBJECTS["grass"] in state:
            state.remove(OBJECTS["grass"])
        if OBJECTS["iron"] in state:
            state.remove(OBJECTS["iron"])
    if "workbench" in objects:
        if OBJECTS["wood"] in state:
            state.add(OBJECTS["stick"])
            state.remove(OBJECTS["wood"])
        if OBJECTS["iron"] in state:
            state.remove(OBJECTS["iron"])
    if "factory" in objects:
        if OBJECTS["grass"] in state:
            state.remove(OBJECTS["grass"])
        if OBJECTS["wood"] in state:
            state.remove(OBJECTS["wood"])
        if OBJECTS["iron"] in state:
            state.remove(OBJECTS["iron"])

    return state


def update_facts_SEQ6(facts: Sequence[bool], objects: Observation) -> Set[int]:
    state = set([i for i, v in enumerate(facts) if v])
    for o in objects:
        if o != "gem" and o in OBJECTS:
            if (o == 'iron' and OBJECTS["wood"] in state) or o == 'wood':
                state.add(OBJECTS[o])
        elif o == "gem" and OBJECTS["axe"] in state:
            state.add(OBJECTS[o])
    if "toolshed" in objects:
        if OBJECTS["stick"] in state and OBJECTS["iron"] in state:
            state.add(OBJECTS["axe"])
            state.remove(OBJECTS["stick"])
            state.remove(OBJECTS["iron"])
        if OBJECTS["wood"] in state:
            state.remove(OBJECTS["wood"])
        if OBJECTS["grass"] in state:
            state.remove(OBJECTS["grass"])
        if OBJECTS["iron"] in state:
            state.remove(OBJECTS["iron"])
    if "workbench" in objects:
        if OBJECTS["wood"] in state and OBJECTS["iron"] in state:
            state.add(OBJECTS["stick"])
            state.remove(OBJECTS["wood"])
    if "factory" in objects:
        if OBJECTS["grass"] in state:
            state.remove(OBJECTS["grass"])
        if OBJECTS["wood"] in state:
            state.remove(OBJECTS["wood"])
        if OBJECTS["iron"] in state:
            state.remove(OBJECTS["iron"])

    return state


def update_facts_POP2(facts: Sequence[bool], objects: Observation) -> Set[int]:
    state = set([i for i, v in enumerate(facts) if v])
    for o in objects:
        if o in ["wood", "iron"]:
            state.add(OBJECTS[o])
        elif o == "gem" and OBJECTS["axe"] in state:
            state.add(OBJECTS[o])
    if "toolshed" in objects:
        if OBJECTS["stick"] in state and OBJECTS["iron"] in state:
            state.add(OBJECTS["axe"])
            state.remove(OBJECTS["stick"])
            state.remove(OBJECTS["iron"])
        if OBJECTS["wood"] in state:
            state.remove(OBJECTS["wood"])
        if OBJECTS["grass"] in state:
            state.remove(OBJECTS["grass"])
        if OBJECTS["iron"] in state:
            state.remove(OBJECTS["iron"])
    if "workbench" in objects:
        if OBJECTS["wood"] in state:
            state.add(OBJECTS["stick"])
            state.remove(OBJECTS["wood"])
    if "factory" in objects:
        if OBJECTS["grass"] in state:
            state.remove(OBJECTS["grass"])
        if OBJECTS["wood"] in state:
            state.remove(OBJECTS["wood"])
        if OBJECTS["iron"] in state:
            state.remove(OBJECTS["iron"])

    return state
