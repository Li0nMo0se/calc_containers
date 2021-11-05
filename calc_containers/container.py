from __future__ import annotations

class Range:
    def __init__(self: Range, _min: int, _max: int) -> Range:
        self.min = _min
        self.max = _max

    def __add__(self: Range, other: Range) -> Range:
        return Range(self.min + other.min, self.max + other.max)

    def __str__(self: Range) -> str:
        return f"[{self.min}, {self.max}]"

    def __contains__(self: Range, elt: int):
        return elt >= self.min and elt <= self.max

    def __contains__(self: Range, elt: Range):
        return (elt.min >= self.min and elt.min <= self.max) or (elt.max >= self.min and elt.max <= self.max)

class Container:
    def __init__(self: Container, name: str, capacity: Range, price: int) -> Container:
        self.name = name
        self.capacity = capacity
        self.price = price

    def __str__(self: Container) -> str:
        return f"name: {self.name}, capacity: {self.capacity}, price: {self.price}"