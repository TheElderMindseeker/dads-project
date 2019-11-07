class Stat:

    def __init__(self, alias, name, def_value, oaths):
        self.alias = alias
        self.name = name
        self.default_value = def_value
        self.oaths = oaths

    def __str__(self):
        return f"""Alias: {self.alias}
Name: {self.name}
Default value: {self.default_value}
Oaths: {self.oaths}"""
