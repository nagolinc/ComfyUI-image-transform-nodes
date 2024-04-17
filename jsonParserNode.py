import json


class JsonParserNode:
    """
    Parses a JSON string and extracts specific numerical values.

    Class methods
    -------------
    INPUT_TYPES (dict):
        Specifies the input parameters of the node.

    Attributes
    ----------
    RETURN_TYPES (`tuple`):
        Specifies the types of each element in the output tuple.
    RETURN_NAMES (`tuple`):
        Names of each output in the output tuple.
    FUNCTION (`str`):
        The name of the entry-point method, which in this case is `parse_json`.
    CATEGORY (`str`):
        The category the node should appear in the UI.
    """

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        value = {
            "required": {
                "json_string": (
                    "STRING",
                    {
                        "multiline": True,
                        "dynamicPrompts": False,
                        "default": '{"offsetX": 0.0, "offsetY": 0.0, "zoom": 1.0}',
                    },
                ),
            }
        }

        print("returning", value)

        return value

    RETURN_TYPES = ("FLOAT", "FLOAT", "FLOAT")
    RETURN_NAMES = ("offsetX", "offsetY", "zoom")

    FUNCTION = "parse_json"
    CATEGORY = "JSON Parsing"

    def parse_json(self, json_string):
        """
        Parses a JSON string to extract offsetX, offsetY, and zoom values.

        Parameters:
        json_string (str): A JSON formatted string containing offsetX, offsetY, and zoom keys.

        Returns:
        tuple: Contains the values of offsetX, offsetY, and zoom extracted from the JSON string.
        """

        print("about to die", json_string)
        
        #remove everything before the first '{' and after the last '}'
        json_string = json_string[json_string.index('{'):json_string.rindex('}')+1]

        data = json.loads(json_string)
        return (
            data.get("offsetX", 0.0),
            data.get("offsetY", 0.0),
            data.get("zoom", 1.0),
        )


# Example of how you might set up the node mappings and display names for UI integration.
NODE_CLASS_MAPPINGS = {"JsonParserNode": JsonParserNode}

NODE_DISPLAY_NAME_MAPPINGS = {"JsonParserNode": "JSON Parser Node"}
