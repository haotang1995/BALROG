#!/usr/bin/env python
# coding=utf-8

import os, os.path as osp, sys

import time
import copy
import pandas as pd

def reformat_obs(obs):
    agent_split = obs.rfind('Agent')
    agent_info, obs = obs[agent_split:], obs[:agent_split]
    map_split = obs.rfind('map:')
    map_info, obs = obs[map_split+4:], obs[:map_split]

    # Put the map info at the left and the other info at the right
    obs = obs + agent_info
    map_lines = map_info.split('\n')
    map_length = set(len(line) for line in map_lines)
    map_length.discard(0)
    assert len(map_length) == 1, f"map_lines: {map_lines}, map_length: {map_length}"
    map_length = map_length.pop()
    map_left_padding_length = [len(line) - len(line.lstrip()) for line in map_lines if len(line) > 0]
    map_left_padding_length = min(map_left_padding_length) if map_left_padding_length else 0
    map_right_padding_length = [len(line) - len(line.rstrip()) for line in map_lines if len(line) > 0]
    map_right_padding_length = min(map_right_padding_length) if map_right_padding_length else 0
    map_lines = [line[map_left_padding_length:map_length-map_right_padding_length] for line in map_lines if len(line) > 0]
    map_length = map_length - map_left_padding_length - map_right_padding_length
    while not len(map_lines[0].strip()):
        map_lines = map_lines[1:]
    while not len(map_lines[-1].strip()):
        map_lines = map_lines[:-1]

    obs_lines = obs.split('\n')
    obs_lines = [line for line in obs_lines if len(line.strip()) > 0 and line.strip().lower() not in ['cursor:', 'language observation:', 'message:']]

    lines = copy.deepcopy(map_lines)
    for li, line in enumerate(obs_lines):
        if li >= len(lines):
            lines.append(' ' * map_length)
        lines[li] += ' '*5 + line

    return '\n'.join(lines)

def main():
    fn = sys.argv[1]
    assert fn.endswith('.csv')
    df = pd.read_csv(fn)
    print(f"Read {len(df)} rows from {fn}")
    print(f"Columns: {df.columns}")
    print()

    for i, row in df.iterrows():
        print(f"Step {i}: {row['Action']}, {row['Reward']}, {row['Done']}")
        print(reformat_obs(row['Observation']))
        time.sleep(0.5)

if __name__ == '__main__':
    main()
