from dataclasses import dataclass

"""
Works with a header and data return data
Header is in the form of 
name
seperated by 3 dolar signs $$$
"""
@dataclass
class FileManager:
    def __init__(self, filename:str):
        self.filename = filename
        self.lines:list[str] = []
        
    def get_file_lines(self):
        try:
            with open(self.filename, 'r') as file:
                self.lines = file.readlines()
        except FileNotFoundError:
            print(f"The file {self.filename} does not exist.")
        except Exception as e:
            print(f"An error occurred: {e}")
            
    def update(self, header:str, new_line:str):
        index, line = self.get_line_of_header(header)
        split_line = self.lines[index].split("$$$")
        self.lines[index] = split_line[0] + "$$$" + new_line
    
    def get_line_of_header(self, header:str) -> tuple[int, str]:
        target_header = header + "$$$"
        for i, line in enumerate(self.lines):
            if line.startswith(target_header):
                return i, line
        return -1, ""
    
    def append_line(self, header:str, line:str):
        self.lines.append(header + "$$$" + line)
    
    def save(self):
        with open(self.filename, 'w') as file:
            for line in self.lines:
                file.write(f"{line}\n")
                