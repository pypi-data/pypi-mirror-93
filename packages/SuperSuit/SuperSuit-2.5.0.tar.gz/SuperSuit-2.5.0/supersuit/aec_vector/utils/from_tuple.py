from gym import spaces
from supersuit.aec_wrappers import ObservationWrapper


def convert_observation(observation, space):
    if isinstance(space, spaces.Dict):
        return {agent: item for agent, item in zip(sorted(space.spaces.keys()), observation)}
    elif isinstance(space, spaces.Tuple):
        return space
    else:
        return space[0]


class from_tuple(ObservationWrapper):
    def __init__(self, env, orig_spaces):
        self.orig_spaces = orig_spaces
        super().__init__(env)

    def _check_wrapper_params(self):
        pass

    def _modify_spaces(self):
        self.observation_spaces = self.orig_spaces

    def _modify_observation(self, agent, observation):
        return convert_observation(observation, self.observation_spaces[agent])
