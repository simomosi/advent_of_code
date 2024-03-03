'''
https://adventofcode.com/2023/day/5

Output
[1] The lowest location number that corresponds to any of the initial seed numbers is 226172555
[2] it requires a bruteforce solution (kinda): it is not feasible on a VM
'''

def main() -> None:
    asset_mapper = None
    with open('2023/05/input.txt', 'r') as file:
        for line in file:
            line = line.strip()
            match line.split(':'):
                case 'seeds', seeds_string:
                    seeds = [int(s) for s in seeds_string.split()]
                    asset_mapper = AssetMapper(seeds)
                    #ranged_asset_mapper = RangedSeedsAssetMapper(seeds)
                    pass
                case 'seed-to-soil map', _:
                    pass
                case 'soil-to-fertilizer map', _:
                    pass
                case 'fertilizer-to-water map', _:
                    pass
                case 'water-to-light map', _:
                    pass
                case 'light-to-temperature map', _:
                    pass
                case 'temperature-to-humidity map', _:
                    pass
                case 'humidity-to-location map', _:
                    pass
                case ['']:
                    asset_mapper.convert_remaining()
                    #ranged_asset_mapper.convert_remaining()
                case one_string:
                    destination, source, range_length = one_string[0].split()
                    asset_mapper.map(int(destination), int(source), int(range_length))
                    #ranged_asset_mapper.map(int(destination), int(source), int(range_length))

    asset_mapper.convert_remaining()
    locations = [v for v in asset_mapper.get_values()]
    min_location = min(locations)
    print(f"[1] The lowest location number that corresponds to any of the initial seed numbers is {min_location}")

    # ranged_asset_mapper.convert_remaining()
    # locations = [v for v in ranged_asset_mapper.get_values()]
    # min_location = min(locations)
    # print(f"[2] The lowest location number that corresponds to any of the initial seed numbers is {min_location}")

class AssetMapper:
    def __init__(self, values:list[int]):
        self.values = set(values)
        self.converted_values = []

    def map(self, destination:int, source:int, range_length:int) -> None:
        to_remove = []
        for v in self.values:
            if source <= v <= source+range_length:
                delta = v-source
                to_remove.append(v)
                self.converted_values.append(destination+delta)

        for r in to_remove:
            self.values.remove(r)

    def convert_remaining(self) -> None:
        while len(self.converted_values) > 0:
            self.values.add(self.converted_values.pop())

    def get_values(self) -> set[int]:
        return self.values

class RangedSeedsAssetMapper(AssetMapper):
    def __init__(self, values: list[int]):
        super().__init__(values)

        self.values = set()
        for v in range(0, len(values), 2):
            start_seed = values[v]
            range_length = values[v+1]
            for seed in range(start_seed, start_seed+range_length):
                self.values.add(seed)

if __name__ == '__main__':
    main()