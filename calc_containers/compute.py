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


def get_combinaison_prices(combinaisons, containers):
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

def compute_cheapest_containers(containers: List[Container], target_capacity: int, print_output: bool=False):
    combinaisons = get_all_combinaison(containers, target_capacity)
    prices = get_combinaison_prices(combinaisons, containers)
    cheapest_price, cheapest_combinaison = get_cheapest_combinaison(prices, combinaisons)

    if print_output:
        print(f"The cheapest containers for the capacity of {target_capacity} is")
        for i in range(len(containers)):
            print(f"* {containers[i].name}: {cheapest_combinaison[i]}")
        print(f"The cost will be {cheapest_price}")

    return cheapest_price, cheapest_combinaison

def compute_cheapeast_containers_from_file(filename: str, price: int, print_output: bool=False):
    df = pd.read_excel(filename)

    containers = []
    for _, row in df.iterrows():
        new_container = Container(row['ContainerName'],
                                 Range(row['MinCapacity'], row['MaxCapacity']),
                                 row['Price'])
        containers.append(new_container)

    return containers, compute_cheapest_containers(containers, price, print_output)