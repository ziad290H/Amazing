from typing import Dict, Optional, List, Tuple, Any
from coordinates42 import Coordinates


class Parser:
    """Handles the parsing and validation of the project configuration file.

    This class reads a custom configuration file, extracts maze parameters,
    and validates them against structural constraints, including dimensions
    and coordinate bounds.

    Attributes:
        filepath (str): The path to the configuration file.
        config (Dict[str, Any]): Dictionary storing the parsed maze settings.
    """

    def __init__(self, filepath: str) -> None:
        """Initializes the parser with default configuration values.

        Args:
            filepath (str): Path to the input configuration file.
        """
        self.filepath: str = filepath
        self.config: Dict[str, Any] = {
            "WIDTH": 0,
            "HEIGHT": 0,
            "ENTRY": (0, 0),
            "EXIT": (0, 0),
            "OUTPUT_FILE": "output_maze.txt",
            "PERFECT": False,
            "SEED": None,
        }

    def parse(self) -> Optional[Dict[str, Any]]:
        """Parses the configuration file and populates the config dictionary.

        Reads line by line, ignores comments (#), and validates that all
        required keys are present.

        Returns:
            Optional[Dict[str, Any]]: The populated configuration dictionary
                if successful, None otherwise.

        Raises:
            ValueError: If the file format is invalid or required keys missing.
        """
        keys_count: int = 0
        required_keys: List[str] = [
            "width", "height", "entry", "exit", "output_file", "perfect"
        ]

        try:
            with open(self.filepath, 'r') as file:
                for line in file:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue

                    if '=' not in line:
                        raise ValueError(
                            f"Use # for comments in {self.filepath}"
                        )

                    parts = line.split('=')
                    if len(parts) != 2:
                        raise ValueError(
                            f"Line '{line}' must follow 'key = value' format."
                        )

                    key, value = parts[0].strip().upper(), parts[1].strip()

                    if key not in self.config:
                        raise ValueError(f"Unsupported key: {key}")

                    self.assign_value(key, value)

                    if key.lower() in required_keys:
                        keys_count += 1

            if keys_count < len(required_keys):
                raise ValueError("Required configuration entries are missing.")

            if self.validate():
                return self.config

        except FileNotFoundError:
            print(f"Error: The File '{self.filepath}' Was Not Found!")
        except PermissionError:
            print(f"Error: No permission to access '{self.filepath}'.")
        except ValueError as e:
            print(f"Configuration Error: {e}")
        return None

    def assign_value(self, key: str, value: str) -> None:
        """Helper method to cast and assign values to the config dictionary.

        Args:
            key (str): The configuration key (e.g., 'WIDTH').
            value (str): The string value associated with the key.

        Raises:
            ValueError: If the value cannot be parsed to the expected type.
        """
        try:
            if key in ["WIDTH", "HEIGHT"]:
                self.config[key] = int(value)
            elif key in ["ENTRY", "EXIT"]:
                coords = tuple(map(int, value.split(',')))
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
        except Exception:
            raise ValueError(f"Could not parse '{value}' for key '{key}'.")

    def validate(self) -> bool:
        """Validates maze parameters against logical and physical constraints.

        Ensures dimensions accommodate the '42' logo and that entry/exit
        points are valid and not obstructed by the logo.

        Returns:
            bool: True if all validations pass.

        Raises:
            ValueError: If any configuration value is logically invalid.
        """
        w, h = self.config["WIDTH"], self.config["HEIGHT"]

        if w < 9 or h < 7:
            raise ValueError("Maze dimensions too small for the '42' block.")

        if self.config["ENTRY"] == self.config["EXIT"]:
            raise ValueError("Entry and Exit must be different.")

        entry_coords: Tuple[int, int] = self.config["ENTRY"]
        exit_coords: Tuple[int, int] = self.config["EXIT"]

        logo_cells = Coordinates._42_cells(w, h)
        if entry_coords in logo_cells or exit_coords in logo_cells:
            raise ValueError("Entry/Exit cannot be located inside '42' block.")

        if not (0 <= entry_coords[0] < w and 0 <= entry_coords[1] < h):
            raise ValueError(f"Entry {entry_coords} is outside the grid.")

        if not (0 <= exit_coords[0] < w and 0 <= exit_coords[1] < h):
            raise ValueError(f"Exit {exit_coords} is outside the grid.")

        if self.config["PERFECT"] is None:
            raise ValueError("PERFECT value must be a boolean.")

        out_file = self.config["OUTPUT_FILE"]
        if not out_file or out_file in [".", "..", "./", "../", "/"]:
            raise ValueError("Invalid output file path.")

        return True