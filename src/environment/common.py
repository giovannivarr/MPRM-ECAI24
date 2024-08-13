from typing import Iterable, Tuple, Union

from .craft import Craft, CraftState
from .environment import ActionId, RewardFn

CraftOffice = Union[Craft]
CraftOfficeState = Union[CraftState]


class ReachFacts(RewardFn):
    target: Tuple[int, ...]

    def __init__(self, environment: CraftOffice, facts: Iterable[int]):
        super().__init__(environment)
        self.target = tuple(facts)

    def __call__(self, s0: CraftOfficeState, a: ActionId,
                 s1: CraftOfficeState) -> Tuple[float, bool]:
        cost = self.environment.cost(s0, a, s1)
        for fact in self.target:
            if not s1.facts[fact]:
                return -cost, False
        return -cost, True

    def reset(self):
        pass


# This is to give the reward for tasks where the agent only needs to reach one of the facts in the "target" list
class ReachDisjunctiveFacts(RewardFn):
    target: Tuple[int, ...]

    def __init__(self, environment: CraftOffice, facts: Iterable[int]):
        super().__init__(environment)
        self.target = tuple(facts)

    def __call__(self, s0: CraftOfficeState, a: ActionId,
                 s1: CraftOfficeState) -> Tuple[float, bool]:
        cost = self.environment.cost(s0, a, s1)
        for fact in self.target:
            if s1.facts[fact]:
                return -cost, True
        return -cost, False

    def reset(self):
        pass
