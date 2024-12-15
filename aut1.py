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



def input_grammar():
    """
    Allow the user to input a grammar interactively.
    :return: A dictionary representing the grammar.
    """
    print("Enter your grammar rules. Use the format:")
    print("Non-terminal -> production1 | production2 | ...")
    print("Example:")
    print("S -> a S b | ε")
    print("Type 'done' when finished.\n")

    grammar = {}
    while True:
        rule = input("Enter rule: ").strip()
        if rule.lower() == "done":
            break
        if "->" not in rule:
            print("Invalid format. Use the format: Non-terminal -> production1 | production2")
            continue

        non_terminal, productions = map(str.strip, rule.split("->"))
        grammar[non_terminal] = [prod.strip() for prod in productions.split("|")]

    return grammar


# Input the grammar from the user
grammar = input_grammar()

print("Input grammar", grammar)

# Create the generator
generator = CFGStringGenerator(grammar)

# Ask for the start symbol and max depth
start_symbol = input("\nEnter the start symbol: ").strip()
max_depth = int(input("Enter the maximum depth for generation: ").strip())

# Generate strings
results = generator.generate(start_symbol, max_depth)

# Filter out empty strings and display results
results = [s for s in results if s]
print("\nGenerated strings:", results)