from abc import ABC, abstractmethod
from typing import FrozenSet, Generic, Hashable, Optional, Tuple, TypeVar

ActionId = int
Observation = FrozenSet[str]


class State(ABC):
    uid: Hashable

    @abstractmethod
    def __str__(self) -> str:
        pass


S = TypeVar('S', bound=State)


class Environment(ABC, Generic[S]):
    num_actions: int = 0
    state: S

    def __init__(self, state: S):
        self.state = state

    @abstractmethod
    def apply_action(self, a: ActionId):
        pass

    @abstractmethod
    def cost(self, s0: S, a: ActionId, s1: S) -> float:
        pass

    @abstractmethod
    def observe(self, state: S) -> Observation:
        pass

    @abstractmethod
    def reset(self, state: Optional[S] = None):
        pass


class RewardFn(ABC, Generic[S]):
    environment: Environment

    def __init__(self, environment: Environment):
        self.environment = environment

    @abstractmethod
    def __call__(self, s0: S, a: ActionId, s1: S) -> Tuple[float, bool]:
        pass

    @abstractmethod
    def reset(self):
        pass
