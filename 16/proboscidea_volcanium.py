'''
https://adventofcode.com/2022/day/16

[1] Max pressure found: 2265

'''

import re
from typing import NamedTuple

input_re = re.compile('Valve (..) has flow rate=(\d+); tunnels? leads? to valves? (.*)')
global cache_hit

class Valve(NamedTuple):
    name: str
    flow_rate: int
    tunnel_names: list[str]
    
def example():
    valves: dict[str, Valve] = {}
    with open('16/example.txt', 'r') as file:
        for line in file:
            match = input_re.match(line.strip())
            name, flow, tunnels = match.groups()
            v = Valve(name, int(flow), [t.strip() for t in tunnels.split(',')])
            valves.setdefault(v.name, v)
    score = release_pressure(valves, 30)
    assert score == 1651, f"Release pressure expected is 1651, actual is {score}"
    
def main():
    valves: dict[str, Valve] = {}
    with open('16/input.txt', 'r') as file:
        for line in file:
            match = input_re.match(line.strip())
            name, flow, tunnels = match.groups()
            v = Valve(name, int(flow), [t.strip() for t in tunnels.split(',')])
            valves.setdefault(v.name, v)
    score = release_pressure(valves, 30)
    print(f"[1] Max pressure found:", score)
    
    
def release_pressure(valves: dict[str, Valve], time_limit: int):
    global cache_hit
    cache_hit = 0
    time_valve_pressure_cache = {}
    actions = []
    open_valves = set()
    max_open_valves = len([v for v in valves.values() if v.flow_rate > 0])
    start = valves.get('AA')
    score = do_action(start, 1, open_valves, actions, time_limit, valves, max_open_valves, time_valve_pressure_cache)
    print(f"Cache hit", cache_hit)
    del time_valve_pressure_cache
    return score

def do_action(position: Valve, time: int, open_valves:set[str], actions: list[tuple[str, int]], time_limit: int, valves: dict[str, Valve], max_open_valves: int, time_pos_actions_cache: dict[tuple[int, str, str], int]) -> int:
    global cache_hit # Sorry for the global variable, this is for debugging purpose (and flex a little bit!)
    
    cache_key = _get_cache_key(position, time, actions)
    if cache_key in time_pos_actions_cache:
        cache_hit += 1 # TODO remove
        return time_pos_actions_cache.get(cache_key)
    
    if len(open_valves) == max_open_valves:
        total_pressure = 0
        _update_cache(cache_key, total_pressure, time_pos_actions_cache)
        return total_pressure
    
    if time >= time_limit or len(open_valves) == max_open_valves:
        total_pressure = position.flow_rate * (time_limit-time)
        _update_cache(cache_key, total_pressure, time_pos_actions_cache)
        return total_pressure
    
    max_pressure = -1
    if (not position.name in open_valves) and position.flow_rate > 0:
        open_valves_updated_copy = open_valves.copy()
        open_valves_updated_copy.add(position.name)
        actions_updated_copy = actions.copy()
        actions_updated_copy.append((position.name, time))
        local_pressure = do_action(position, time+1, open_valves_updated_copy, actions_updated_copy, time_limit, valves, max_open_valves, time_pos_actions_cache)
        max_pressure = local_pressure + position.flow_rate * (time_limit-time)
        del actions_updated_copy, open_valves_updated_copy
    
    for tunnel_name in position.tunnel_names:
        tunnel = valves.get(tunnel_name)
        local_pressure = do_action(tunnel, time+1, open_valves, actions, time_limit, valves, max_open_valves, time_pos_actions_cache)
        if local_pressure > max_pressure:
            max_pressure = local_pressure
    
    _update_cache(cache_key, max_pressure, time_pos_actions_cache)
    return max_pressure

def _get_cache_key(position: Valve, time: int, actions:list[tuple[str, int]]) -> tuple[int, str, str]:
    sorted_actions_time_string = ''.join(a[0] for a in actions)
    # Note: I think the correct way of computing the cache key is the following one (commented due to memory shortage)
    # sorted_actions_time_string = '-'.join([a[0] + str(a[1]) for a in actions]) # name + time
    # The cache works anyway, maybe I'm just lucky
    return (time, position.name, sorted_actions_time_string)

def _update_cache(key: tuple[int, str, str], value: int, cache: dict[tuple[int, str, str], int]):
    if not key in cache:
        cache.setdefault(key, value)
    else:
        old_value = cache.pop(key)
        cache.setdefault(key, value if value > old_value else old_value)
    return

if __name__ == '__main__':
    example()
    main()