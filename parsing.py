class Parser:

    number_of_keys = 0
    def __init__(self, filepath: str):
        self.config = {
            "WIDTH":0,
            "HEIGHT":0,
            "ENTRY":(0, 0),
            "EXIT": (0, 0),
            "OUTPUT_FILE": "output_file.txt",
            "PERFECT": False,
            "SEED": None
        }
    def parse(self):
        dict_param = {}
        key_count = 0
        try:
            try:
                with open(self.filepath, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if not line or line[0] == '#':
                            continue
                        if '=' not in line:
                            raise ValueError("The parameter should me in this format 'key':'value'")
                        if len(line.split('=')) > 2:
                            raise ValueError("this line {line} should containe exactly this format 'key'='format'")
                        key, value = line.split('=')
                        dict_param[key] = value
                        if key.strip().upper() not in self.config:
                            raise ValueError(f"Unknown key {key}")
                        elif key.strip().upper() in self.config:
                            key_count += 1
                        self.assigne_value(key.strip().upper(), value.strip())
                    if key_count != len(self.config):
                        raise ValueError("Make sure to enter the required parametre")
            except (FileNotFoundError, PermissionError, IsADirectoryError) as e:
                print(f"Error File: {e}")
        except Exception as e:
            print(e)

    def assigne_value(self, key, value):
        """
        Docstring for assigne_value
        
        for this function I assigne each value from the file config
        to a value parametre
        """
        try:
            if key in ["WIDTH", "HEIGHT"]:
                value = int(value)
                self.config[key] = value
            if key in ["ENTRY", "EXIT"]:
                value = tuple(map(int, value.split(',').strip()))
                self.config[key] = value
            if key == "PERFECT":
                if value.lower() == "true":
                    self.config[value] = True
                elif value.lower() == "false":
                    self.config[value] = False
                else:
                    raise ValueError
            if key == "OUTPUT_FILE":
                self.config[key] = value
            if key == "SEED":
                self.config[key] = int(value)
        except Exception:
            raise(f"Could not Parse '{value}' for key '{key}'")
        
        def validate(self):
            width = self.config["WIDTH"]
            height = self.config["HEIGHT"]
            try:
                if width < 9 or height < 7
                    raise ValueError("Give a reasonale width and height to build a maze"):
                if width < 0