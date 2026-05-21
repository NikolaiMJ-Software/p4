class RuntimeValue:
    def __init__(self, type_name, value):
        self.type = type_name
        self.value = value

    def __repr__(self):
        return f"{self.type}({self.value})"