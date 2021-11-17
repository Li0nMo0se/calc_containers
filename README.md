# Containers calculator

**Compute the best combination of containers for a given capacity according to a price**

* See [container.ipynb](container.ipynb) for the proof of concept.
* See [template.xlsx](template.xlsx) for template input excel file.
* See [example.py](example.py) to see an example on how to use the library

Compute the cheapest combinaison of containers with a excel file as input
```python
containers, cheapest_price, cheapest_combinaison = compute_cheapeast_containers_from_file(file, target_capacity)
```
with :
* containers: list containers from the input file
* cheapest_price: price of the computed (cheapest) combinaison
* cheapest_combinaison: list of containers (following `containers` orders) giving the number of each container for the computed (cheapest) combinaison


