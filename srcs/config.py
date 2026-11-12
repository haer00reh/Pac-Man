from pydantic import BaseModel
import json
import sys


class Config(BaseModel):
    file_path: str
    data: dict

    def extract(self):
        try:
            with open(self.file_path, "r") as f:
                lst = f.readlines()
                s = ""
                for l in lst:
                    s += l.rsplit("#")[0]
                self.data = json.loads(s)
        except FileNotFoundError as e:
            print(f"Error: File not found - {e}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON format - {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Error: An unexpected error occurred - {e}")
            sys.exit(1)
