from __future__ import annotations
from typing import List, Tuple
import numpy as np
import pandas as pd

from .container import Range, Container

def __get_all_combinaison(containers: List[Container], target_capacity: Range) -> List[List[int]]:
    if len(containers) == 0 or target_capacity.max <= 0:
        return []

    results = []

    curr_capacity = containers[0].capacity
    remaining_containers = containers[1:]

    # Get the maximum number of containers to consider
    max_quantity = target_capacity.max // curr_capacity.min

    # Loop over the maximum quantity
    for quantity in range(max_quantity + 1): # +1 needed for the range
        curr_range = Range(quantity * curr_capacity.min, quantity * curr_capacity.max)
        # If the current capacity range is within target, then we found a possible combinaison
        if target_capacity in curr_range: # Stop here
            results.append([quantity] + [0] * len(remaining_containers))
        else: # Else, recursively find with other containers
            remaining_capacity = Range(target_capacity.min - curr_range.max, target_capacity.max - curr_range.min)
            for option in __get_all_combinaison(remaining_containers, remaining_capacity):
                results.append([quantity] + option)

    return results

def get_all_combinaison(containers: List[Container], target_capacity: int) -> List[List[int]]:
    return __get_all_combinaison(containers, Range(target_capacity, target_capacity))


def get_combinaison_prices(combinaisons: List[List[int]], containers: List[Container]):
    def get_price(combinaison, containers):
        total = 0
        for i in range(len(combinaison)):
            quantity = combinaison[i]
            total += quantity * containers[i].price
        return total

    return [get_price(combinaison, containers) for combinaison in combinaisons]

def get_cheapest_combinaison(prices: List[int], combinaisons: List[List[int]]) -> Tuple[int, List[int]]:
    # There might be an equality
    min_index_price = np.argmin(prices)
    return prices[min_index_price], combinaisons[min_index_price]

def compute_cheapest_containers(containers: List[Container], target_capacity: int):
    combinaisons = get_all_combinaison(containers, target_capacity)
    prices = get_combinaison_prices(combinaisons, containers)
    cheapest_price, cheapest_combinaison = get_cheapest_combinaison(prices, combinaisons)

    return cheapest_price, cheapest_combinaison

def compute_cheapest_combinaisons_many_capacity(containers: List[Container], max_capacity: int):
    prices = [(0, 0, [0, 0, 0, 0])]
    for capacity in range(1, max_capacity):
        cheapest_price, cheapest_combinaison = compute_cheapest_containers(containers, capacity)
        prices.append((capacity, cheapest_price, cheapest_combinaison))

    return prices

def compute_cheapest_combinaison_without_smallest_container(containers: List[Container],
                                                            target_capacity: int,
                                                            max_capacity: int):
    assert target_capacity < max_capacity
    prices = compute_cheapest_combinaisons_many_capacity(containers, max_capacity)

    # Find the closest cheapest combinaison without LCL container
    for new_capacity in range(target_capacity + 1, max_capacity):
        if prices[new_capacity][2][-1] == 0:
            break

    for new_capacity2 in range(target_capacity - 1, 0, -1):
        if prices[new_capacity2][2][-1] == 0:
            break

    return prices[target_capacity], prices[new_capacity], prices[new_capacity2]


## -- from file section -- ##
def containers_from_file(filename: str):
    df = pd.read_excel(filename)

    containers = []
    for _, row in df.iterrows():
        new_container = Container(row['ContainerName'],
                                 Range(row['MinCapacity'], row['MaxCapacity']),
                                 row['Price'])
        containers.append(new_container)
    ## TODO: sort container by capacity
    return containers

def compute_cheapeast_containers_from_file(filename: str, target_capacity: int):
    containers = containers_from_file(filename)
    cheapest_price, cheapest_combinaison = compute_cheapest_containers(containers, target_capacity)
    return containers, cheapest_price, cheapest_combinaison

def compute_cheapest_combinaisons_many_capacity_from_file(filename: str, max_capacity: int):
    containers = containers_from_file(filename)
    return (containers,) + compute_cheapest_combinaisons_many_capacity(containers, max_capacity)

def compute_cheapest_combinaison_without_smallest_container_from_file(filename: str,
                                                                      target_capacity: int,
                                                                      max_capacity: int):
    containers = containers_from_file(filename)
    return (containers,) + compute_cheapest_combinaison_without_smallest_container(containers, target_capacity, max_capacity)

## -- print result -- ##
def result_to_string(containers: List[Container],
                     target_capacity: int,
                     cheapest_price: int,
                     cheapest_combinaison: List[int]):
    str = f"The cheapest containers for the capacity of {target_capacity} is\n"
    for i in range(len(containers)):
        str += f"* {containers[i].name}: {cheapest_combinaison[i]}\n"
    str += f"The cost will be {cheapest_price}"
    return str