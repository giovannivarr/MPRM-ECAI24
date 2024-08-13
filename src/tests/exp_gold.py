import sys  # noqa
from os import path as p  # noqa

sys.path.append(p.abspath(p.join(p.dirname(sys.modules[__name__].__file__),
                                 "..")))  # noqa

import logging
from os import path
from random import Random
from time import time

from environment import Craft, CraftState, ReachFacts
from rl import Agent, RMAgent, EpsilonGreedy, EpsilonGreedyQRM
from utils import SequenceReport

from environment.craft import OBJECTS

DEFAULT_Q = 0.0
# this ensures that all the experiments have results up to the 10_000_000 step mark
TOTAL_STEPS = 10_001_000
EPISODE_LENGTH = 1_000
LOG_STEP = 10_000
TRIALS = 5
START_TASK = 0
END_TASK = 0

logging.basicConfig(level=logging.INFO)

# inits for new_map_40x40
init = [CraftState(10, 38, set()), CraftState(39, 28, set()),
        CraftState(21, 21, set()), CraftState(3, 3, set()),
        CraftState(39, 5, set())]

here = path.dirname(__file__)
rng = Random(2024)

def qrm_test(out_file: str, alpha: float = 0.95, gamma: float = 1.0, epsilon: float = 0.1, name: str =''):
    print(out_file)
    with open(out_file, "w") as csvfile:
        print("qrm_{}, {}: begin experiment".format(name, map_fn))
        report = SequenceReport(csvfile, LOG_STEP, init, EPISODE_LENGTH, TRIALS)

        rng.seed(2024)

        env = Craft(map_fn, rng, agent=name)

        reward = ReachFacts(env, GOAL)
        policyQRM = EpsilonGreedy(alpha=alpha, gamma=gamma, epsilon=epsilon, default_q=DEFAULT_Q, num_actions=4, rng=rng)

        agentQRM = Agent(env, policyQRM, reward, rng)

        try:
            start = time()
            agentQRM.train(steps=TOTAL_STEPS,
                           steps_per_episode=EPISODE_LENGTH, report=report)
            end = time()
            print("qrm_{}: Ran task for {} seconds.".format(name, end - start))
        except KeyboardInterrupt:
            end = time()
            logging.warning("qrm: interrupted task after %s seconds!",
                            end - start)

        agentQRM.demo(init[0], 100)
        report.increment(TOTAL_STEPS)

    del policyQRM
    del agentQRM


def crm_test(out_file: str, alpha: float = 1.0, gamma: float = 1.0, epsilon: float = 0.1, name: str =''):
    with open(out_file, "w") as csvfile:
        print("crm: begin experiment")
        report = SequenceReport(csvfile, LOG_STEP, init, EPISODE_LENGTH, TRIALS)

        print("crm: begin task")
        rng.seed(2024)

        env = Craft(map_fn, rng, agent=name)

        reward = ReachFacts(env, GOAL)
        policyCRM = EpsilonGreedyQRM(alpha=alpha, gamma=gamma, epsilon=epsilon, default_q=DEFAULT_Q, num_actions=4, rng=rng)

        agentCRM = RMAgent(env, policyCRM, reward, rng, "CRM-gold")

        try:
            start = time()
            agentCRM.train(steps=TOTAL_STEPS,
                           steps_per_episode=EPISODE_LENGTH, report=report)
            end = time()
            print("crm: Ran task for {} seconds.".format(end - start))
        except KeyboardInterrupt:
            end = time()
            logging.warning("crm: interrupted task after %s seconds!",
                            end - start)

        agentCRM.demo(init[0], 100)
        report.increment(TOTAL_STEPS)

    del policyCRM
    del agentCRM


if __name__=="__main__":
    for i in range(0, 10):
        print(here)
        map_fn = './src/tests/craft/gold-maps/map_{}.map'.format(i)

        GOAL = [OBJECTS["gold"]]

        qrm_test("plots/gold-results/mprm-gold{}.csv".format(i), alpha=0.95, name='bridge_gold_MPRM')
        qrm_test("plots/gold-results/seq0-gold{}.csv".format(i), alpha=0.95, name='SEQ0')
        qrm_test("plots/gold-results/seq1-gold{}.csv".format(i), alpha=0.95, name='SEQ1')
        qrm_test("plots/gold-results/seq2-gold{}.csv".format(i), alpha=0.95, name='SEQ2')
        qrm_test("plots/gold-results/seq3-gold{}.csv".format(i), alpha=0.95, name='SEQ3')
        qrm_test("plots/gold-results/pop0-gold{}.csv".format(i), alpha=0.95, name='POP0')
        qrm_test("plots/gold-results/pop1-gold{}.csv".format(i), alpha=0.95, name='POP1')

        #crm_test("plots/gold-results/crm-gold{}.csv".format(i), name='bridge_gold_MPRM')