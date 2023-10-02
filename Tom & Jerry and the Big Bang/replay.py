import pickle
from typing import Tuple, List

import numpy as np
import settings as s
from agents import Agent
from environment import GenericWorld, WorldArgs
from fallbacks import pygame
from items import Coin

class ReplayWorld(GenericWorld):
    def __init__(self, args: WorldArgs):
        super().__init__(args)
        self.load_replay(args.replay)

    def load_replay(self, replay_file):
        self.logger.info(f'Loading replay file "{replay_file}"')
        self.replay_file = replay_file
        with open(replay_file, 'rb') as f:
            self.loaded_replay = pickle.load(f)
        if 'n_steps' not in self.loaded_replay:
            self.loaded_replay['n_steps'] = s.MAX_STEPS

        pygame.display.set_caption(f'{replay_file}')
        self.recreate_agents()

    def recreate_agents(self):
        agents = []
        for name, _, b, xy in self.loaded_replay["agents"]:
            avatar_sprite_desc = bomb_sprite_desc = self.colors.pop()
            if "display_names" in self.loaded_replay:
                display_name = self.loaded_replay["display_names"].get(name, name)
                avatar_sprite_desc = self.loaded_replay["avatars"].get(name, avatar_sprite_desc)
                bomb_sprite_desc = self.loaded_replay["bombs"].get(name, bomb_sprite_desc)
            else:
                display_name = name
            agents.append(ReplayAgent(name, display_name, avatar_sprite_desc, bomb_sprite_desc))
        self.agents = agents

    def build_arena(self) -> Tuple[np.array, List[Coin], List[Agent]]:
        arena = np.array(self.loaded_replay['arena'])

        coins = [Coin(xy, arena[xy] == 0) for xy in self.loaded_replay['coins']]

        agents = []
        for i, agent in enumerate(self.agents):
            agents.append(agent)
            agent.x, agent.y = self.loaded_replay['agents'][i][-1]

        return arena, coins, agents

    def poll_and_run_agents(self):
        perm = self.loaded_replay['permutations'][self.step - 1]
        self.replay['permutations'].append(perm)
        for i in perm:
            a = self.active_agents[i]
            self.logger.debug(f'Repeating action from agent <{a.name}>')
            action = self.loaded_replay['actions'][a.name][self.step - 1]
            self.logger.info(f'Agent <{a.name}> chose action {action}.')
            self.replay['actions'][a.name].append(action)
            self.perform_agent_action(a, action)

    def time_to_stop(self):
        time_to_stop = super().time_to_stop()
        if self.step == self.loaded_replay['n_steps']:
            self.logger.info('Replay ends here, wrap up round')
            time_to_stop = True
        return time_to_stop

class ReplayAgent(Agent):
    def __init__(self, name, display_name, avatar_sprite_desc, bomb_sprite_desc):
        super().__init__(name, None, display_name, False, None, avatar_sprite_desc, bomb_sprite_desc)

    def setup(self):
        pass

    def act(self, game_state):
        pass

    def wait_for_act(self):
        return 0, self.actions.popleft()
