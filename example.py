from calc_containers.compute import compute_cheapeast_containers_from_file, result_to_string

target_capacity = 95
containers, cheapest_price, cheapest_combinaison =\
    compute_cheapeast_containers_from_file("template.xlsx", target_capacity)

print(result_to_string(containers, target_capacity, cheapest_price, cheapest_combinaison))
