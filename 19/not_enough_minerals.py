'''
https://adventofcode.com/2022/day/19
'''

import re
line_input_re = re.compile('^Blueprint (\d+): Each ore robot costs (\d+) ore\. Each clay robot costs (\d+) ore\. Each obsidian robot costs (\d+) ore and (\d+) clay\. Each geode robot costs (\d+) ore and (\d+) obsidian\.$')

from typing import NamedTuple
from enum import Enum

class Material(Enum):
    CLAY = 0,
    ORE = 1,
    OBSIDIAN = 2,
    GEODE = 3

class Robot(NamedTuple):
    material_produced: Material
    costs:dict[Material, int]
    
    def are_costs_satisfied(self, inventory: dict[Material, int]):
        for material, cost in self.costs.items():
            if inventory.get(material, 0) < cost:
                return False
        return True
        
class BluePrint(NamedTuple):
    id: int
    robots: list[Robot]

def example():
    blueprints:list[BluePrint] = []
    with open('19/example.txt', 'r') as file:
        for line in file:
            (id, 
            ore_robot_cost_in_ore, 
            clay_robot_cost_in_ore, 
            obs_robot_cost_in_ore, 
            obs_robot_cost_in_clay, 
            geode_robot_cost_in_ore, 
            geode_robot_cost_in_obs) = map(int, line_input_re.match(line.strip()).groups())
            
            ore_robot = Robot(Material.ORE, {Material.ORE: ore_robot_cost_in_ore})
            clay_robot = Robot(Material.CLAY, {Material.ORE: clay_robot_cost_in_ore})
            obsidian_robot = Robot(Material.OBSIDIAN, {Material.ORE: obs_robot_cost_in_ore, Material.CLAY: obs_robot_cost_in_clay})
            geode_robot = Robot(Material.GEODE, {Material.ORE: geode_robot_cost_in_ore, Material.OBSIDIAN: geode_robot_cost_in_obs})
            bp = BluePrint(id, [ore_robot, clay_robot, obsidian_robot, geode_robot])
            blueprints.append(bp)
    quality_level = find_quality_level_sum(blueprints, 24)
    assert quality_level == 33, f"Expected 33, actual {quality_level}"

def main():
    blueprints:list[BluePrint] = []
    with open('19/input.txt', 'r') as file:
        for line in file:
            (id, 
            ore_robot_cost_in_ore, 
            clay_robot_cost_in_ore, 
            obs_robot_cost_in_ore, 
            obs_robot_cost_in_clay, 
            geode_robot_cost_in_ore, 
            geode_robot_cost_in_obs) = map(int, line_input_re.match(line.strip()).groups())
            
            ore_robot = Robot(Material.ORE, {Material.ORE: ore_robot_cost_in_ore})
            clay_robot = Robot(Material.CLAY, {Material.ORE: clay_robot_cost_in_ore})
            obsidian_robot = Robot(Material.OBSIDIAN, {Material.ORE: obs_robot_cost_in_ore, Material.CLAY: obs_robot_cost_in_clay})
            geode_robot = Robot(Material.GEODE, {Material.ORE: geode_robot_cost_in_ore, Material.OBSIDIAN: geode_robot_cost_in_obs})
            bp = BluePrint(id, [ore_robot, clay_robot, obsidian_robot, geode_robot])
            blueprints.append(bp)
    quality_level = find_quality_level_sum(blueprints, 24)
    print(f"[1] The sum of quality levels of each blueprint is {quality_level}") # 868 too low

def find_quality_level_sum(blueprints:list[BluePrint], minutes: int):
    robots = {Material.ORE: 1, Material.CLAY:0, Material.OBSIDIAN: 0, Material.GEODE: 0}
    inventory = {Material.ORE: 0, Material.CLAY:0, Material.OBSIDIAN: 0, Material.GEODE: 0}
    
    quality_levels:list[tuple[int,int]] = []
    for bp in blueprints:
        robots_upper_limit:dict[Material, int] = {}
        for r in bp.robots:
            for material, cost in r.costs.items():
                if material in robots_upper_limit:
                    old_cost = robots_upper_limit.pop(material)
                    robots_upper_limit.setdefault(material, max(cost, old_cost))
                else:
                    robots_upper_limit.setdefault(material, cost)
                    
        geodes_number = find_largest_geodes_number(bp, minutes, robots.copy(), inventory.copy(), {}, robots_upper_limit)
        quality_levels.append((geodes_number, bp.id))
    return sum(number*id for number, id in quality_levels)

def find_largest_geodes_number(bp: BluePrint, minutes_left: int, robots:dict[Material, int], inventory:dict[Material, int], cache:dict[tuple, int], robots_upper_limit:dict[Material, int]) -> int:
    if minutes_left <= 0:
        return inventory.get(Material.GEODE, 0)
    
    cache_key = _get_cache_key(minutes_left, robots, inventory)
    if cache_key in cache:
        return cache.get(cache_key)
    
    largest_geodes_number = -1
    for r in bp.robots:
        if r.are_costs_satisfied(inventory) and _check_under_limit_threshold(r.material_produced, robots, robots_upper_limit):
            local_robots = robots.copy()
            local_inventory = inventory.copy()
            # Build robot
            for material, cost in r.costs.items():
                availability = local_inventory.pop(material)
                local_inventory.setdefault(material, availability-cost)
            robots_number = local_robots.pop(r.material_produced)
            local_robots.setdefault(r.material_produced, robots_number+1)
            # Produce material
            for material, produced in robots.items():
                availability = local_inventory.pop(material)
                local_inventory.setdefault(material, availability+produced)
            
            geodes_number = find_largest_geodes_number(bp, minutes_left-1, local_robots, local_inventory, cache, robots_upper_limit)
            if geodes_number > largest_geodes_number:
                largest_geodes_number = geodes_number
    
    should_wait_and_mine = False
    for material, robots_number in robots.items():
        if material == Material.GEODE:
            continue
        if robots_number > 0 and inventory.get(material) < robots_upper_limit.get(material):
            should_wait_and_mine = True
            break
    
    if should_wait_and_mine:   
        for material, qty in robots.items():
            availability = inventory.pop(material)
            inventory.setdefault(material, availability+qty)
        geodes_number = find_largest_geodes_number(bp, minutes_left-1, robots, inventory, cache, robots_upper_limit)
        if geodes_number > largest_geodes_number:
            largest_geodes_number = geodes_number
    
    if cache_key in cache:
        cache.pop(cache_key)
    cache.setdefault(cache_key, largest_geodes_number)        
    return largest_geodes_number
    
def _get_cache_key(minutes_left: int, robots:dict[Material, int], inventory:dict[Material, int]) -> tuple[int, str]:
    #robots_key = f"Ore {robots.get(Material.ORE)} - Clay {robots.get(Material.CLAY)} - Obs {robots.get(Material.OBSIDIAN)}- Geode {robots.get(Material.GEODE)}"
    inventory_key = f"Ore {inventory.get(Material.ORE)} - Clay {inventory.get(Material.CLAY)} - Obs {inventory.get(Material.OBSIDIAN)} - Geode {inventory.get(Material.GEODE)}"
    return (minutes_left, inventory_key)

def _check_under_limit_threshold(material: Material, robots: dict[Material, int], limits: dict[Material, int]):
    return (material == material.GEODE 
            or robots.get(material, 0) < limits.get(material, 0))
    

if __name__ == '__main__':
    example()
    main()
    