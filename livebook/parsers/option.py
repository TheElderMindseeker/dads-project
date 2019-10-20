class Option:
    def __init__(self, text, next_scene, flavor):
        self.text = text
        self.next_scene = next_scene
        self.flavor = flavor

    def __str__(self):
        return f"""Option text: {self.text}
Next Scene: {self.next_scene}
Flavor: {self.flavor}"""

    def parse_text(self, stats):
        """
        Replaces the stat references (@alias) to human-oriented stat names
        :param stats: stats to use for replacement
        """
        for stat in stats:
            self.text = self.text.replace(f"@{stat.alias}", stat.name)
            self.flavor = self.flavor.replace(f"@{stat.alias}", stat.name)
