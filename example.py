from calc_containers.compute import compute_cheapeast_containers_from_file, compute_cheapest_combinaison_without_smallest_container_from_file, result_to_string

target_capacity = 99
max_capacity = 250
file = "template.xlsx"

print(f"Target capacity: {target_capacity}")
print(f"Max capacity: {max_capacity}")
print(f"file: {file}")
print("---------------------------------------")

print("Compute cheapeast combinaison")
containers, cheapest_price, cheapest_combinaison =\
    compute_cheapeast_containers_from_file(file, target_capacity)

print(result_to_string(containers, target_capacity, cheapest_price, cheapest_combinaison))

print("---------------------------------------")
print("Compute cheapeast combinaison without smallest container")
containers, target_price, lower_price, higher_price =\
    compute_cheapest_combinaison_without_smallest_container_from_file(file, target_capacity, max_capacity)
print(result_to_string(containers, target_price[0], target_price[1], target_price[2]))
print(result_to_string(containers, lower_price[0], lower_price[1], lower_price[2]))
print(result_to_string(containers, higher_price[0], higher_price[1], higher_price[2]))
