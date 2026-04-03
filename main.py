import json
import deca_tools

fname = "./data/animal_population_1"


def convert_node(node):
    """
    Recursively convert parsed ADF nodes into JSON-serializable Python data.
    Includes offsets when available.
    """

    # Plain Python primitives
    if isinstance(node, (int, float, str, bool)) or node is None:
        return node

    # Lists / arrays
    if isinstance(node, list):
        return [convert_node(item) for item in node]

    # Dicts
    if isinstance(node, dict):
        return {key: convert_node(value) for key, value in node.items()}

    # ADF field/object with .value and maybe .data_offset
    if hasattr(node, "value"):
        value = node.value
        offset = getattr(node, "data_offset", None)

        # Nested structure (dict-like)
        if isinstance(value, dict):
            converted = {key: convert_node(val) for key, val in value.items()}
            if offset is not None:
                converted["__offset__"] = offset
            return converted

        # Array/list-like
        if isinstance(value, list):
            converted = [convert_node(item) for item in value]
            if offset is not None:
                return {
                    "__value__": converted,
                    "__offset__": offset
                }
            return converted

        # Primitive field
        return {
            "__value__": convert_node(value),
            "__offset__": offset
        }

    # Fallback: string representation
    return str(node)


# Read and unpack file
data_bytes = bytearray(deca_tools.read_file(fname))
data_bytes = data_bytes[32:]                  # strip outer header
decompressed = bytearray(deca_tools.decompress(data_bytes))
decompressed = decompressed[5:]              # strip inner header

adf_file = fname + "_parsed"
deca_tools.save_file(adf_file, decompressed)

parse_obj = deca_tools.parse_adf(adf_file)

root = parse_obj.table_instance_full_values[0].value
converted = convert_node(root)

with open("population_full_dump.json", "w", encoding="utf-8") as f:
    json.dump(converted, f, indent=2)

print("Saved population_full_dump.json")