from gym import spaces
from supersuit.aec_wrappers import ObservationWrapper


def convert_space(space):
    if isinstance(space, spaces.Dict):
        return spaces.Tuple([space for agent, space in sorted(space.spaces.items())])
    elif isinstance(space, spaces.Tuple):
        return space
    else:
        return spaces.Tuple([space])


def convert_observation(observation):
    if isinstance(observation, dict):
        return tuple([item for agent, item in sorted(observation.items())])
    elif isinstance(observation, tuple):
        return space
    else:
        return (space,)


class from_tuple(ObservationWrapper):
    def _check_wrapper_params(self):
        pass

    def _modify_spaces(self):
        self.observation_spaces = {agent: convert_space(space) for agent, space in self.env.observation_spaces.items()}

    def _modify_observation(self, agent, observation):
        return convert_observation(observation)
