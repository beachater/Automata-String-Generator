import random


class FiniteAutomaton:
    """
    Class representing a finite automaton (FA) that can generate valid strings
    based on user-defined transitions.
    """

    def __init__(self):
        self.states = set()
        self.alphabet = set()
        self.transitions = {}
        self.initial_state = None
        self.accept_states = set()

    def input_fa(self):
        """
        Allow user to define FA's states, transitions, initial state, and accept states.
        """
        print("\nDefine your finite automaton (FA):")
        
        # Input states
        state_input = input("Enter all states (comma-separated): ").strip()
        self.states = set(state_input.split(","))
        print(f"States defined: {self.states}")
        
        # Input alphabet
        alphabet_input = input("Enter the alphabet symbols (comma-separated): ").strip()
        self.alphabet = set(alphabet_input.split(","))
        print(f"Alphabet defined: {self.alphabet}")

        # Input initial state
        self.initial_state = input("Enter the initial state: ").strip()
        if self.initial_state not in self.states:
            print("Error: Initial state must be part of the defined states.")
            return

        # Input accept states
        accept_input = input("Enter accept states (comma-separated): ").strip()
        self.accept_states = set(accept_input.split(","))
        print(f"Accept states defined: {self.accept_states}")

        # Input transitions
        print("\nDefine transitions in the format 'state,symbol,next_state'. Type 'done' to finish.")
        while True:
            transition_input = input("Enter transition: ").strip()
            if transition_input.lower() == "done":
                break
            try:
                state, symbol, next_state = transition_input.split(",")
                if state not in self.states or next_state not in self.states:
                    print("Error: States must be part of the defined states.")
                    continue
                if symbol not in self.alphabet:
                    print("Error: Symbol must be part of the defined alphabet.")
                    continue
                self.transitions[(state, symbol)] = next_state
                print(f"Transition added: ({state}, {symbol}) -> {next_state}")
            except ValueError:
                print("Error: Invalid transition format. Ensure you follow the format 'state,symbol,next_state'.")

    def simulate_string(self, string):
        """
        Simulate a string through the finite automaton to determine if it's accepted.
        :param string: Input string to simulate.
        :return: True if accepted, False otherwise.
        """
        current_state = self.initial_state
        for symbol in string:
            if (current_state, symbol) in self.transitions:
                current_state = self.transitions[(current_state, symbol)]
            else:
                print(f"Transition not found for ({current_state}, {symbol}). String rejected.")
                return False

        if current_state in self.accept_states:
            print(f"String '{string}' is accepted. Final state: {current_state}")
            return True
        else:
            print(f"String '{string}' is rejected. Final state: {current_state}")
            return False

    def generate_random_string(self, max_length):
        """
        Randomly generate a string up to the given length accepted by the FA.
        """
        current_state = self.initial_state
        string = ""
        for _ in range(max_length):
            valid_symbols = [symbol for (state, symbol), next_state in self.transitions.items() if state == current_state]
            if not valid_symbols:
                break
            symbol = random.choice(valid_symbols)
            string += symbol
            current_state = self.transitions[(current_state, symbol)]
            if current_state in self.accept_states:
                print(f"String accepted early: {string}")
                break
        return string


# Main driver function

print("Welcome to the Finite Automaton String Generator!")

# Create FA object
fa = FiniteAutomaton()

# Step 1: Allow user to input FA details
fa.input_fa()

# Simulate user's choice
print("\nChoose an action:")
print("1. Simulate a string through FA")
print("2. Generate a random string up to a given length")
choice = input("Enter choice (1/2): ").strip()

if choice == "1":
    # Simulate a string
    string = input("\nEnter a string to simulate: ").strip()
    fa.simulate_string(string)
elif choice == "2":
    # Generate random string
    max_length = int(input("\nEnter the maximum string length to generate randomly: ").strip())
    random_string = fa.generate_random_string(max_length)
    print(f"Generated random string: {random_string}")
else:
    print("\nInvalid choice. Exiting...")