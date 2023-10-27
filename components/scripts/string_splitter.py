

def split_recipe_string(input_string):
    part_1_idx = input_string.find("Part 1:")
    part_2_idx = input_string.find("Part 2:")
    part_3_idx = input_string.find("Part 3:")
    part_4_idx = input_string.find("Part 4:")

    return part_1_idx, part_2_idx, part_3_idx, part_4_idx