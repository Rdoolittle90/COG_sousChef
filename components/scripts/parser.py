import re

def split_recipe_string(input_string):
    part_1_idx = input_string.find("Part 1:")
    part_2_idx = input_string.find("Part 2:")
    part_3_idx = input_string.find("Part 3:")
    part_4_idx = input_string.find("Part 4:")

    return part_1_idx, part_2_idx, part_3_idx, part_4_idx

def extract_section_pretext(s:str):
        s = s.split("\n")[1:]
        s = "\n".join(s)
        return s

def determine_difficulty(recipe_info):
        steps = len(recipe_info.get('steps', []))
        ingredients = len(recipe_info.get('ingredients', []))
        
        total = steps + ingredients

        if total <= 5:
            return "Beginner"
        elif 5 < total <= 10:
            return "Intermediate"
        elif 10 < total <= 15:
            return "Advanced"
        else:
            return "Expert"

def extract_spicy_integer(s:str):
    match = re.search(r'\d+', s)
    if match:
        spice_rating = int(match.group())
        if spice_rating == 0:
            return 1
        else:
            return spice_rating
    else:
        return 0


def recipe_parser(recipe_name:str, message:str):
    part_idx = split_recipe_string(message)

    ingredients:list[str] = extract_section_pretext(message[part_idx[0]:part_idx[1]-1]).split("\n")

    instructions:list[str] = extract_section_pretext(message[part_idx[1]:part_idx[2]-1]).split("\n")

    description:str = extract_section_pretext(message[part_idx[2]:part_idx[3]-1])

    part_4:str = message[part_idx[3]:].strip("Part: 4")
    spice_rating = extract_spicy_integer(part_4)

    for idx, ingredient in enumerate(ingredients):
        ingredients[idx] = ingredient.replace("-", "").strip()
    ingredients.remove("")
    instructions.remove("")

    recipe_dict = {
        "name": recipe_name,
        "ingredients": ingredients,
        "instructions": instructions,
        "description": description,
        "spice": spice_rating,
        "ratings": {},
        "Fav_counts": 0
    }

    return recipe_dict