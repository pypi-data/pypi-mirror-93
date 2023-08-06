def stack_observations(obs_list):
    num_items = len(obs_list[0])
    for obs in obs_list:
        if len(obs) != num_items:
            raise AssertionError("bad observation tuples, something wrong")

    return [np.stack(res) for res in zip(*obs_list)]
