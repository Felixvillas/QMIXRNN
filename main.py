import argparse
import torch.optim as optim
from smac.env import StarCraft2Env

from model import QMIX_agent
from learn import qmix_learning
from utils.schedule import LinearSchedule
from utils.sc_wrapper import single_net_sc2env

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--map-name', type=str, default='8m')
    parser.add_argument('--batch-size', type=int, default=32)
    parser.add_argument('--gamma', type=float, default=0.99)
    parser.add_argument('--training-steps', type=int, default=2000000)
    parser.add_argument('--anneal-steps', type=int, default=100000)
    parser.add_argument('--anneal-start', type=float, default=1.0)
    parser.add_argument('--anneal-end', type=float, default=0.01)
    parser.add_argument('--replay-buffer-size', type=int, default=5000)
    parser.add_argument('--learning-starts', type=int, default=0)
    parser.add_argument('--target-update-freq', type=int, default=200)
    parser.add_argument('--save-model-freq', type=int, default=2000)
    parser.add_argument('--test-freq', type=int, default=10000)
    parser.add_argument('--learning-rate', type=float, default=3e-4)
    parser.add_argument('--grad-norm-clip', type=float, default=0.5)
    # seed
    parser.add_argument('--seed', type=int, default=0)
    # ddqn
    parser.add_argument('--is-ddqn', type=int, default=True)
    # per
    parser.add_argument('--is-per', type=int, default=False)
    parser.add_argument('--alpha', type=float, default=0.6)
    parser.add_argument('--beta', type=float, default=0.2)
    parser.add_argument('--prior-eps', type=float, default=1e-6)
    # multi_step
    parser.add_argument('--multi-steps', type=int, default=1)
    # share networks
    parser.add_argument('--share-para', type=int, default=True)
    # evaluate
    parser.add_argument('--is-evaluate', type=int, default=True)
    parser.add_argument('--evaluate-num', type=int, default=32)
    # store hyper parameters
    parser.add_argument('--store-hyper-para', type=int, default=True)
    # optimizer
    parser.add_argument('--optimizer', type=int, default=0, help="0: Adam--[3m, 2s_vs_1sc]; 1: RMSprop--[others]")

    return parser.parse_args()

def main(args=get_args()):

    exploration_schedule = LinearSchedule(args.anneal_steps, args.anneal_end, args.anneal_start)

    if args.share_para:
        env_class = single_net_sc2env
    else:
        env_class = StarCraft2Env

    qmix_learning(
        env_class=env_class,
        q_func=QMIX_agent,
        exploration=exploration_schedule,
        args=args
    )

if __name__ == '__main__':
    main()