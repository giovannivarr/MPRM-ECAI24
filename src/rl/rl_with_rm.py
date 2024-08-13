import itertools
import logging
from abc import ABC, abstractmethod
from random import Random
from typing import List, Optional, Sequence, Tuple, Set

from environment import ActionId, Environment, RewardFn, State, CraftState, Observation
from utils import Report


# DISCLAIMER: this is a modified version of the rl.py file from the illanes-code repository
# The modifications are to allow for the CRM experiments to be run
# However, this dates back to a previous version where the update_facts function wasn't defined in its own separate file
# based on the agent's "name", but was just modified in the craft.py file

OBJECTS = dict([(v, k) for k, v in enumerate(
    ["wood", "grass", "iron", "bridge", "stick", "axe", "gold", "gem"])])

def update_facts(facts: Sequence[bool], objects: Observation, craft_exp: str) -> Set[int]:
    if craft_exp in ["CRM-bridge", "CRM-gold"]:
        state = set([i for i, v in enumerate(facts) if v])
        for o in objects:
            if o != "gold" and o in OBJECTS:
                # Used for QRM with MaxPOP
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
    elif craft_exp == "CRM-gold-gem":
        state = set([i for i, v in enumerate(facts) if v])
        for o in objects:
            if o not in ["gold", "gem"] and o in OBJECTS:
                # Used for QRM with MaxPOP
                state.add(OBJECTS[o])
                # Used for QRM with individual sequential plans (in this case SEQ-3)
                #if (o == 'iron' and OBJECTS["wood"] in state) or o == 'wood':
                #    state.add(OBJECTS[o])
            #Used for QRM with single POP (in this case POP-0)
            #if o not in ["gold", "gem"] and o in ["wood", "iron"]:
                #state.add(OBJECTS[o])
                #THIS IS TO MAKE THE QRM-POP-3 EXPERIMENT
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
            # THIS IS TO MAKE SEQ-6
            #if OBJECTS["wood"] in state and OBJECTS["iron"] in state:
            #    state.remove(OBJECTS["wood"])
            #    state.add(OBJECTS["stick"])
            # BELOW IS FOR ALL OTHER PLANS
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

class QRMPolicy(ABC):
    @abstractmethod
    def clear(self):
        pass

    @abstractmethod
    def get_best_action(self, state: State,
                        restrict: Optional[List[int]] = None) -> ActionId:
        pass

    @abstractmethod
    def get_train_action(self, state: State,
                         restrict: Optional[List[int]] = None) -> ActionId:
        pass

    def report(self) -> str:
        return ""

    @abstractmethod
    def reset(self, evaluation: bool):
        pass

    @abstractmethod
    def update(self, s0: State, a: ActionId, s1: State, r: float, end: bool):
        pass


l = [False, True]

class RMAgent:
    environment: Environment
    policy: QRMPolicy
    reward: RewardFn
    rng: Random
    exp: str

    def __init__(self, environment: Environment, policy: QRMPolicy,
                 reward: RewardFn, rng: Random, exp: str):
        self.environment = environment
        self.policy = policy
        self.reward = reward
        self.rng = rng
        self.rm_states = list(itertools.product(l, repeat=7))
        self.exp = exp

    def demo(self, state: State, steps: int):
        rng_state = self.rng.getstate()

        self.environment.reset(state)
        self.reward.reset()
        self.policy.reset(evaluation=True)

        total_reward: float = 0.0

        print(state)

        for step in range(steps):
            s0 = self.environment.state

            a = self.policy.get_best_action(s0)
            self.environment.apply_action(a)
            print(a)

            s1 = self.environment.state
            print(s1)

            step_reward, finished = self.reward(s0, a, s1)
            print(step_reward)

            total_reward += step_reward

            if finished:
                print("fin")
                break
        print("total reward:", total_reward)

        self.rng.setstate(rng_state)

    def evaluate(self, states: Sequence[State], steps: int, trials: int,
                 name: str = "") -> List[float]:
        state_rewards: List[float] = []
        rng_state = self.rng.getstate()
        for initial_state in states:
            trial_rewards: List[float] = []
            for trial in range(trials):
                self.environment.reset(initial_state)
                self.reward.reset()
                self.policy.reset(evaluation=True)
                trial_reward: float = 0.0
                for step in range(steps):
                    s0 = self.environment.state

                    a = self.policy.get_best_action(s0)
                    self.environment.apply_action(a)

                    s1 = self.environment.state

                    step_reward, finished = self.reward(s0, a, s1)

                    trial_reward += step_reward

                    logging.debug("(%s, %s, %s) -> %s", s0, a, s1, step_reward)

                    if finished:
                        break

                logging.debug("Evaluation from %s obtained reward of %s.",
                              initial_state, trial_reward)

                trial_rewards.append(trial_reward)
            state_rewards.append(sum(trial_rewards)/trials)

        logging.info("Evaluation %s obtained %s average reward per trial. %s",
                     name, sum(state_rewards)/len(states),
                     self.policy.report())

        self.rng.setstate(rng_state)
        return state_rewards

    def train_episode(self, current_step: int, end_step: int,
                      report: Optional[Report] = None) -> Tuple[int, float,
                                                                bool]:
        self.environment.reset()
        self.reward.reset()
        self.policy.reset(evaluation=False)

        episode_reward = 0.0
        finished = False

        logging.debug("Begin episode (current step is %s)", current_step)

        for step in range(current_step, end_step + 1):
            if finished:
                break

            s0 = self.environment.state

            a = self.policy.get_train_action(s0)
            new_objects = self.environment.apply_action(a)

            s1 = self.environment.state

            step_reward, finished = self.reward(s0, a, s1)
            self.policy.update(s0, a, s1, step_reward, finished)

            episode_reward += step_reward

            x0, y0, x1, y1 = s0.uid[0], s0.uid[1], s1.uid[0], s1.uid[1]
            for rm_state in self.rm_states:
                counterfactual_s0 = CraftState(x0, y0, rm_state)
                if (counterfactual_s0, a) not in self.policy.Q.keys():
                    continue
                new_counterfactual_facts = update_facts(rm_state, new_objects)
                counterfactual_s1 = CraftState(x1, y1, new_counterfactual_facts)
                counterfactual_reward, _ = self.reward(s0, a, counterfactual_s1)
                self.policy.update(counterfactual_s0, a, counterfactual_s1, counterfactual_reward, finished)

            logging.debug("(%s, %s, %s) -> %s", s0, a, s1, step_reward)

            if report is not None:
                # Adding 1 to the step might cause the training to skip some evaluations
                report.evaluate(self, step)


        logging.debug("End episode (last step was %s, success=%s)", step,
                      finished)
        #self.policy.update_current()
        #print("End episode (last step was {}, success={})".format(step,
        #                                                          finished))

        return step, episode_reward, finished

    def train(self, steps: int, steps_per_episode: int,
              report: Optional[Report] = None) -> Tuple[float, int, int]:
        total_reward: float = 0.0
        current_step: int = 0
        episode: int = 0

        #if report is not None:
        #    report.evaluate(self, 0, force=True)

        while current_step < steps:
            next_end = min(current_step + steps_per_episode, steps)
            current_step, episode_reward, finished = \
                self.train_episode(current_step, next_end, report)

            total_reward += episode_reward
            logging.debug("Training episode %s obtained reward %s after %s"
                          "steps.", episode, episode_reward, current_step + 1)

            episode += 1

        logging.info("Training finished after %s total steps (%s episodes).",
                     current_step, episode)
        logging.info("Total cumulative reward was %s.", total_reward)

        return total_reward, current_step, episode
