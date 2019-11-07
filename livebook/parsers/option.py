class Option:
    def __init__(self, text, next_scene, prompt):
        self.text = text
        self.next = next_scene
        self.prompt = prompt

    def __str__(self):
        return f"""Option text: {self.text}
Next Scene: {self.next}
Flavor: {self.prompt}"""

    def parse_text(self, stats):
        """
        Replaces the stat references (@alias) to human-oriented stat names
        :param stats: stats to use for replacement
        """
        for stat in stats:
            self.text = self.text.replace(f"@{stat.alias}", stat.name)
            self.prompt = self.prompt.replace(f"@{stat.alias}", stat.name)
