class Parser:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.config = {
            "WIDTH": 0,
            "HEIGHT": 0,
            "ENTRY": (0, 0),
            "EXIT": (0, 0),
            "OUTPUT_FILE": "output_maze.txt",
            "PERFECT": False,
            "SEED": None
        }

    def parse(self):
        key_count = 0
        with open(self.filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' not in line:
                    continue
                
                parts = line.split('=')
                key = parts[0].strip().upper()
                value = parts[1].strip()

                if key in self.config:
                    self.assign_value(key, value)
                    key_count += 1
        
        self.validate()
        return self.config

    def assign_value(self, key, value):
        try:
            if key in ["WIDTH", "HEIGHT"]:
                self.config[key] = int(value)
            elif key in ["ENTRY", "EXIT"]:
                self.config[key] = tuple(map(int, value.split(',')))
            elif key == "PERFECT":
                self.config[key] = value.lower() == "true"
            elif key == "OUTPUT_FILE":
                self.config[key] = value
            elif key == "SEED":
                self.config[key] = int(value)
        except Exception:
            raise ValueError(f"Could not parse '{value}' for key '{key}'")

    def validate(self):
        w, h = self.config["WIDTH"], self.config["HEIGHT"]
        if w <= 0 or h <= 0:
            raise ValueError("Dimensions must be positive.")
        ex, ey = self.config["EXIT"]
        if ex >= w or ey >= h:
            raise ValueError("Exit coordinates out of bounds.")