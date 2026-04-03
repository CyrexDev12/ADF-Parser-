import json
import deca_tools

fname = "./data/animal_population_8"

data_bytes = bytearray(deca_tools.read_file(fname))
data_bytes = data_bytes[32:]
decompressed = bytearray(deca_tools.decompress(data_bytes))
decompressed = decompressed[5:]

adf_file = fname + "_parsed"
deca_tools.save_file(adf_file, decompressed)

parse_obj = deca_tools.parse_adf(adf_file)

root = parse_obj.table_instance_full_values[0].value
populations = root["Populations"].value

summary = []

for pop_index, pop in enumerate(populations):
    pop_obj = {
        "population_index": pop_index,
        "groups": []
    }

    groups = pop.value["Groups"].value

    for group_index, group in enumerate(groups):
        animals = group.value["Animals"].value
        group_obj = {
            "group_index": group_index,
            "animal_count": len(animals),
            "animals": []
        }

        for animal_index, animal in enumerate(animals):
            a = animal.value
            animal_obj = {
                "animal_index": animal_index,
                "Gender": a["Gender"].value if "Gender" in a else None,
                "Weight": a["Weight"].value if "Weight" in a else None,
                "Score": a["Score"].value if "Score" in a else None,
                "IsGreatOne": a["IsGreatOne"].value if "IsGreatOne" in a else None,
                "VisualVariationSeed": a["VisualVariationSeed"].value if "VisualVariationSeed" in a else None,
                "Id": a["Id"].value if "Id" in a else None,
                "MapPosition": {
                    "X": a["MapPosition"].value["X"].value if "MapPosition" in a else None,
                    "Y": a["MapPosition"].value["Y"].value if "MapPosition" in a else None,
                } if "MapPosition" in a else None,
                "offsets": {
                    "Gender": a["Gender"].data_offset if "Gender" in a else None,
                    "Weight": a["Weight"].data_offset if "Weight" in a else None,
                    "Score": a["Score"].data_offset if "Score" in a else None,
                    "IsGreatOne": a["IsGreatOne"].data_offset if "IsGreatOne" in a else None,
                    "VisualVariationSeed": a["VisualVariationSeed"].data_offset if "VisualVariationSeed" in a else None,
                    "Id": a["Id"].data_offset if "Id" in a else None,
                    "MapPosition_X": a["MapPosition"].value["X"].data_offset if "MapPosition" in a else None,
                    "MapPosition_Y": a["MapPosition"].value["Y"].data_offset if "MapPosition" in a else None,
                }
            }
            group_obj["animals"].append(animal_obj)

        pop_obj["groups"].append(group_obj)

    summary.append(pop_obj)

with open("population_summary.json", "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=2)

print("Saved population_summary.json")
print(f"Populations: {len(summary)}")