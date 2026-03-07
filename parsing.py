from typing import Dict, Optional
from coordinates42 import Coordinates


class Parser:
    """
    Handles the parsing and validation of the project configuration file.
    """

    def __init__(self, filepath: str) -> None:
        self.filepath = filepath
        self.config: Dict = {
            "WIDTH": 0,
            "HEIGHT": 0,
            "ENTRY": (0, 0),
            "EXIT": (0, 0),
            "OUTPUT_FILE": "maze.txt",
            "PERFECT": False,
            "SEED": None,
        }

    def parse(self) -> Optional[dict]:
        """
        The parsing method, parses the config file entries.
        """
        keys_count = 0
        required_keys = ["width", "height", "entry",
                         "exit", "output_file", "perfect"]
        try:
            with open(self.filepath, 'r') as file:
                for line in file:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue

                    if '=' not in line:
                        raise ValueError("Use # to make comments! "
                                         f"Error in {self.filepath}")

                    parts = line.split('=')
                    if len(parts) != 2:
                        raise ValueError(f"This Line '{line}' Should "
                                         "Have Exactly The Format key = Value")

                    key, value = parts[0].strip(), parts[1].strip()

                    if key.upper() not in self.config:
                        raise ValueError(f"Unsupported key: {key} !!")

                    self.assign_value(key.upper(), value)

                    if key.lower() in required_keys:
                        keys_count += 1

            if keys_count < len(required_keys):
                raise ValueError("Make Sure to Enter All Required Entries !!")

            if self.validate():
                return self.config

        except FileNotFoundError:
            print(f"Error: The File '{self.filepath}' Was Not Found !")
        except PermissionError:
            print(f"Error: Can't Access to '{self.filepath}'")
        except ValueError as e:
            print(f"Configuration Error: {e}")
        return None

    def assign_value(self, key: str, value: str) -> None:
        """
        Helper method to set values, now handling tuple-like SEED strings.
        """
        try:
            if key in ["WIDTH", "HEIGHT"]:
                self.config[key] = int(value)
            elif key in ["ENTRY", "EXIT"]:
                # Removes () if present and splits by comma
                clean_val = value.replace('(', '').replace(')', '')
                coords = tuple(map(int, clean_val.split(',')))
                self.config[key] = coords
            elif key == "PERFECT":
                if value.lower() == 'true':
                    self.config[key] = True
                elif value.lower() == 'false':
                    self.config[key] = False
                else:
                    self.config[key] = None
            elif key == "OUTPUT_FILE":
                self.config[key] = value
            elif key == "SEED":
                # Handle SEED=(1,1,1) by converting to a hashable tuple
                clean_seed = value.replace('(', '').replace(')', '')
                if ',' in clean_seed:
                    seed_tuple = tuple(map(int, clean_seed.split(',')))
                    # Use hash of the tuple
                    self.config[key] = hash(seed_tuple)
                else:
                    self.config[key] = int(clean_seed)
        except Exception:
            raise ValueError(f"Could Not Parse '{value}' for key '{key}'")

    def validate(self) -> bool:
        """
        Validates entries against maze constraints.
        """
        w = self.config["WIDTH"]
        h = self.config["HEIGHT"]

        if w < 9 or h < 7:
            raise ValueError("Give reasonable height and width (min 9x7) "
                             "to accommodate the 42 block")

        if self.config["ENTRY"] == self.config["EXIT"]:
            raise ValueError("Entry and Exit must be different")

        # Validate coordinate dimensions
        if len(self.config["ENTRY"]) != 2 or len(self.config["EXIT"]) != 2:
            raise ValueError("Entry and Exit Coordinates should be 2D (x,y)")

        entry_x, entry_y = self.config["ENTRY"]
        exit_x, exit_y = self.config["EXIT"]

        # 42 block collision check
        block_cells = Coordinates._42_cells(w, h)
        if self.config["ENTRY"] in block_cells:
            raise ValueError("Entry should not be inside the 42 block")
        if self.config["EXIT"] in block_cells:
            raise ValueError("Exit should not be inside the 42 block")

        # Bounds check
        if not (0 <= entry_x < w and 0 <= entry_y < h):
            raise ValueError(f"Entry {entry_x},{entry_y} is outside the grid!")
        if not (0 <= exit_x < w and 0 <= exit_y < h):
            raise ValueError(f"Exit {exit_x},{exit_y} is outside the grid!")

        if self.config["PERFECT"] is None:
            raise ValueError("PERFECT value must be True or False!")

        if (not self.config["OUTPUT_FILE"] or
           self.config["OUTPUT_FILE"] in [".", "..", "/", "./", "../"]):
            raise ValueError("Invalid Output File name or its a Directory!")

        return True
