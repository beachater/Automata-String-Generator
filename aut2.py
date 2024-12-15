class CFLGenerator:
    def __init__(self, language_description):
        """
        Initialize the generator with the language description.
        :param language_description: String describing the language (e.g., "a^nb^n")
        """
        self.language_description = language_description
        self.grammar = {
            "start": "S",
            "productions": {}
        }
        self.terminals = set()
        self.non_terminals = set()

    def generate_cfg(self):
        """
        Reverse engineer the CFG from the language description.
        """
        # Parse the description (basic patterns like a^nb^n or alternations)
        if "^n" in self.language_description:
            self._handle_power_n()
        elif "|" in self.language_description:
            self._handle_alternation()
        else:
            raise NotImplementedError("This type of CFL is not yet supported!")

        return self.grammar

    def _handle_power_n(self):
        """
        Handle languages with patterns like a^nb^n.
        """
        import re

        # Use regex to extract patterns like `a^n` and `b^n`
        pattern = r'([a-z])\^n([a-z])\^n'
        match = re.search(pattern, self.language_description.replace(" ", ""))

        if match:
            t1, t2 = match.groups()  # Extract terminal symbols
            self.terminals.update({t1, t2})

            # Generate production rules
            self.grammar["productions"]["S"] = [f"{t1}S{t2}", ""]
        else:
            raise ValueError(f"Invalid format for a^nb^n in description: {self.language_description}")

    def _handle_alternation(self):
        """
        Handle languages with alternation patterns like 'a | b'.
        """
        # Split by alternation character "|"
        alternatives = [alt.strip() for alt in self.language_description.split("|")]
        
        # If there's a valid alternation
        if len(alternatives) >= 2:
            self.terminals.update(alternatives)
            self.grammar["productions"]["S"] = alternatives
        else:
            raise ValueError(f"Invalid alternation format in description: {self.language_description}")

    def display_cfg(self):
        """
        Pretty print the generated CFG.
        """
        print("Start Symbol: S")
        print("Terminals:", ", ".join(self.terminals))
        print("Non-terminals:", ", ".join(self.grammar["productions"].keys()))
        print("Production Rules:")
        for nt, rules in self.grammar["productions"].items():
            print(f"  {nt} -> {' | '.join(rules)}")
    
    

# Example Usage
if __name__ == "__main__":
    # Example 1: a^nb^n
    description = "a^nb^n"
    generator = CFLGenerator(description)
    grammar = generator.generate_cfg()
    generator.display_cfg()

    # Example 2: {ab | |w| = 4}
    description = "a | b"
    generator = CFLGenerator(description)
    grammar = generator.generate_cfg()
    generator.display_cfg()
