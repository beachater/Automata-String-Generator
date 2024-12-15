import re

# CFG String Generator Class
class CFGStringGenerator:
    def __init__(self, grammar):
        """
        Initialize the generator with a grammar.
        :param grammar: A dictionary where keys are non-terminals and values are lists of production rules.
        """
        self.grammar = grammar

    def generate(self, symbol, max_depth):
        """
        Recursively generate strings from the given symbol.
        :param symbol: The current non-terminal or terminal.
        :param max_depth: The maximum recursion depth.
        :return: A list of strings generated from the symbol.
        """
        # Debugging: Print the current symbol and depth
        print(f"Generating for symbol: {symbol} at depth: {max_depth}")
        
        # If max_depth reaches 0, don't expand anymore
        if max_depth == 0:
            return []

        # Base case: if symbol is terminal, return itself
        if symbol not in self.grammar:
            print(f"Base case hit for terminal: {symbol}")
            return [symbol]

        # Recursive case: symbol is a non-terminal, expand it
        strings = []
        for rule in self.grammar[symbol]:
            print(f"Processing rule: {symbol} -> {rule}")
            if rule == "ε":  # Handle epsilon explicitly
                print(f"Rule is epsilon, adding empty string.")
                strings.append("")
            else:
                parts = rule.split()  # Split the production rule into parts
                generated = [""]
                for part in parts:
                    print(f"Expanding part: {part}")
                    if part in self.grammar:  # If the part is a non-terminal, expand it
                        sub_strings = self.generate(part, max_depth - 1)  # Recursively expand non-terminal parts
                    else:
                        sub_strings = [part]  # Otherwise, it's a terminal, so just return it
                    print(f"Substrings generated for {part}: {sub_strings}")
                    generated = [g + s for g in generated for s in sub_strings]  # Combine all generated parts
                    print(f"Generated after combining: {generated}")
                strings.extend(generated)  # Add the expanded strings from this rule
            print(f"Strings so far: {strings}")
        
        return strings




# CFL Generator (CFG Parser) Class
class CFLGenerator:
    def __init__(self, language_description):
        """
        Initialize the generator with the language description.
        :param language_description: String describing the language (e.g., "a^nb^n")
        """
        self.language_description = language_description
        self.grammar = {
            "start": 'S',
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

        # Return grammar productions for CFGStringGenerator
        return self.grammar["productions"]

    def _handle_power_n(self):
        """
        Handle languages with patterns like a^nb^n.
        """
        pattern = r'([a-z])\^n([a-z])\^n'
        match = re.search(pattern, self.language_description.replace(" ", ""))

        if match:
            t1, t2 = match.groups()  # Extract terminal symbols
            self.terminals.update({t1, t2})

            # Generate production rules for a^nb^n
            self.grammar["productions"]["S"] = [f"{t1} S {t2}", "ε"]
        else:
            raise ValueError(f"Invalid format for a^nb^n in description: {self.language_description}")

    def _handle_alternation(self):
        """
        Handle languages with alternation patterns like 'a | b'.
        """
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


# Main Program to Combine CFG Generation and String Generation
if __name__ == "__main__":
    # Example: Language description "a^nb^n"
    description = input("Enter the language description (e.g., a^nb^n or a | b): ").strip()
    generator = CFLGenerator(description)

    # Generate CFG from the description
    grammar = generator.generate_cfg()
    generator.display_cfg()

    # Now, pass the CFG to CFGStringGenerator (no need for "productions" key anymore)
    print(grammar)
    cfg_string_generator = CFGStringGenerator(grammar)

    # Ask for the start symbol and max depth for string generation
    start_symbol = "S"  # Assuming S is the start symbol
    max_depth = int(input("Enter the maximum depth for generation (e.g., 5 or 6): ").strip())

    # Generate random strings based on the CFG
    generated_strings = cfg_string_generator.generate(start_symbol, max_depth)

    # Filter out empty strings and display the results
    generated_strings = [s for s in generated_strings if s]
    print("\nGenerated strings:", generated_strings)
