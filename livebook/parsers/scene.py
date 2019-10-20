class Scene:

    def __init__(self, text, options):
        self.text = text
        self.options = options

    def __str__(self):
        return f"""Scene text: {self.text}
Options: {self.options}"""

    def parse_text(self, stats):
        """
        Replaces the stat references (@alias) to human-oriented stat names
        Affects both the scene and the options in it
        :param stats: stats to use for replacement
        """
        for stat in stats:
            self.text = self.text.replace(f"@{stat.alias}", stat.name)

        for option in self.options:
            option.parse_text(stats)
