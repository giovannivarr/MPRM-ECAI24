from random import Random
from typing import Dict, Hashable, List, Optional, Tuple

from environment import ActionId, State

from .rl import Policy


class Greedy(Policy):
    alpha: float
    default_q: Tuple[float, bool]
    gamma: float
    num_actions: int
    Q: Dict[Tuple[Hashable, ActionId], Tuple[float, bool]]
    rng: Random

    def __init__(self, alpha: float, gamma: float, default_q: float,
                 num_actions: int, rng: Random):
        self.alpha = alpha
        self.gamma = gamma
        self.default_q = default_q, False
        self.num_actions = num_actions
        self.rng = rng
        self.Q = {}

    def clear(self):
        self.Q = {}

    def estimate(self, state: State) -> float:
        max_q = self.Q.get((state.uid, 0), self.default_q)
        for action in range(1, self.num_actions):
            q = self.Q.get((state.uid, action), self.default_q)
            if q > max_q:
                max_q = q
        return max_q[0]

    def get_best_action(self, state: State,
                        restrict: Optional[List[int]] = None) -> ActionId:
        if restrict is None:
            restrict = list(range(self.num_actions))
        max_q = self.Q.get((state.uid, restrict[0]), self.default_q)
        best_actions = [restrict[0]]
        for action in restrict[1:]:
            q = self.Q.get((state.uid, action), self.default_q)
            if q > max_q:  # or (self.evaluation and q[1] and not max_q[1]):
                max_q = q
                best_actions = [action]
            elif q == max_q:
                best_actions.append(action)
        return self.rng.choice(best_actions)

    def get_train_action(self, state: State,
                         restrict: Optional[List[int]] = None) -> ActionId:
        return self.get_best_action(state, restrict)

    def update(self, s0: State, a: ActionId, s1: State, r: float, end: bool):
        q = (1.0 - self.alpha) * self.Q.get((s0.uid, a), self.default_q)[0]
        if end:
            q += self.alpha * r
        else:
            q += self.alpha * (r + self.gamma * self.estimate(s1))

        self.Q[(s0.uid, a)] = q, True

    def reset(self, evaluation: bool):
        self.evaluation = evaluation

    def report(self) -> str:
        return "|Q| = {}".format(len(self.Q))


class EpsilonGreedy(Greedy):
    epsilon: float

    def __init__(self, alpha: float, gamma: float, epsilon: float,
                 default_q: float, num_actions: int, rng: Random):
        self.epsilon = epsilon
        super().__init__(alpha, gamma, default_q, num_actions, rng)

    def get_train_action(self, state: State,
                         restrict: Optional[List[int]] = None) -> ActionId:
        if self.rng.random() < self.epsilon:
            if restrict is None:
                restrict = list(range(self.num_actions))
            return self.rng.choice(restrict)
        else:
            return self.get_best_action(state, restrict)


class QState(State):
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

        self.uid = (self.x, self.y)

    def __str__(self) -> str:
        return "({:2d}, {:2d})".format(self.x, self.y)


class TrueQLearning(EpsilonGreedy):
    def __init__(self, alpha: float, gamma: float, epsilon: float,
                 default_q: float, num_actions: int, rng: Random):
        super().__init__(alpha, gamma, epsilon, default_q, num_actions, rng)

    def estimate(self, state: State) -> float:
        state_q = QState(state.x, state.y)
        return super().estimate(state_q)

    def get_best_action(self, state: State,
                        restrict: Optional[List[int]] = None) -> ActionId:
        state_q = QState(state.x, state.y)
        return super().get_best_action(state_q, restrict)

    def get_train_action(self, state: State,
                         restrict: Optional[List[int]] = None) -> ActionId:
        return self.get_best_action(state, restrict)

    def update(self, s0: State, a: ActionId, s1: State, r: float, end: bool):
        s0_q = QState(s0.x, s0.y)
        s1_q = QState(s1.x, s1.y)
        q = (1.0 - self.alpha) * self.Q.get((s0_q.uid, a), self.default_q)[0]
        if end:
            q += self.alpha * r
        else:
            q += self.alpha * (r + self.gamma * self.estimate(s1_q))

        self.Q[(s0_q.uid, a)] = q, True

