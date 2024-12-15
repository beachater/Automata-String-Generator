import random
from pyformlang.regular_expression import Regex


def user_regex_to_nfa(regex_string):
    """
    Converts a regex string to an NFA (without epsilon transitions) using the pyformlang library.
    """
    try:
        # Convert regex to epsilon-NFA and then to NFA
        nfa = Regex(regex_string).to_epsilon_nfa().remove_epsilon_transitions()
        print("NFA Details:")
        print(f"Start States: {nfa.start_states}")
        print(f"Final States: {nfa.final_states}")
        print(f"Symbols: {nfa.symbols}")
        print(f"Transitions: {nfa.to_dict()}")

        return nfa
    except Exception as e:
        print(f"Error converting regex to NFA: {e}")
        return None



def generate_random_string(nfa, max_length):
    """
    Simulates random transitions through the NFA to generate a valid string.
    """
    # Debugging: Print NFA details
    print("NFA Details:")
    print(f"Start States: {nfa.start_states}")
    print(f"Final States: {nfa.final_states}")
    print(f"Symbols: {nfa.symbols}")
    print(f"Transitions: {nfa.to_dict()}")

    # Start from one of the initial states
    current_state = random.choice(list(nfa.start_states))
    random_string = ""

    for _ in range(max_length):
        # Collect all possible transitions from the current state
        transitions_dict = nfa.to_dict()
        next_states = {
            symbol: list(transitions_dict.get((current_state, symbol), []))
            for symbol in nfa.symbols
        }

        print(f"Current state: {current_state}, Available transitions: {next_states}")

        # If no transitions are available, terminate
        if not any(next_states.values()):
            print("No transitions available. Terminating string generation.")
            break

        # Randomly select a transition
        transition_symbol = random.choice([symbol for symbol in next_states if next_states[symbol]])
        next_state = random.choice(next_states[transition_symbol])

        # Update the state and string
        current_state = next_state
        random_string += str(transition_symbol)

        # Check if we've reached a final state
        if current_state in nfa.final_states:
            return random_string

    return random_string if random_string else None


def generate_random_string_test(nfa, max_length):
    """
    Simulates transitions through the NFA in a fixed (hardcoded) manner for debugging.
    """
    # Debugging: Print NFA details
    print("NFA Details:")
    print(f"Start States: {nfa.start_states}")
    print(f"Final States: {nfa.final_states}")
    print(f"Symbols: {nfa.symbols}")
    print(f"Transitions: {nfa.to_dict()}")

    # Start from the first initial state
    current_state = list(nfa.start_states)[0]
    random_string = ""

    transitions_dict = nfa.to_dict()

    for _ in range(max_length):
        # Collect all possible transitions for the current state
        next_states = {}
        for symbol in nfa.symbols:
            targets = transitions_dict.get((current_state, symbol), [])
            if targets:
                next_states[symbol] = list(targets)

        print(f"Current state: {current_state}, Available transitions: {next_states}")

        # If no transitions are available, terminate
        if not next_states:
            print("No transitions available. Terminating string generation.")
            break

        # Select the first available transition for testing
        transition_symbol = list(next_states.keys())[0]
        next_state = next_states[transition_symbol][0]

        # Update the state and string
        current_state = next_state
        random_string += transition_symbol

        # Stop if we reach a final state
        if current_state in nfa.final_states:
            print(f"Reached final state {current_state}.")
            return random_string

    print("Max length reached without reaching a final state.")
    return random_string if random_string else None



def enumerate_strings(nfa, max_length):
    """
    Enumerates all valid strings accepted by the NFA up to a given max string length.
    """
    from itertools import product

    valid_strings = []
    for length in range(1, max_length + 1):
        # Generate combinations of all possible strings of the given length
        for sequence in product('01', repeat=length):  # Adjust alphabet as needed
            string_candidate = ''.join(sequence)
            if nfa.accepts(string_candidate):
                valid_strings.append(string_candidate)

    return valid_strings



def main():
    print("Welcome to the formal language string generator tool!")
    # Allow user to input a regex
    user_input_regex = input("\nEnter a regular expression (e.g., a*(01|0)*b): ")

    # Convert regex to NFA
    print("\nConverting regex to NFA...")
    nfa = user_regex_to_nfa(user_input_regex)
    
    print("NFA Details:")
    print(f"Start States: {nfa.start_states}")
    print(f"Final States: {nfa.final_states}")
    print(f"Symbols: {nfa.symbols}")
    print(f"Transitions: {nfa.to_dict()}")

    if not nfa:
        print("Invalid regex or unable to generate NFA. Exiting...")
        return

    print("\nNFA created successfully. Ready to perform operations.")

    # Ask the user for the desired action
    while True:
        print("\nChoose an operation:")
        print("1. Generate random strings")
        print("2. Enumerate all valid strings up to a certain length")
        print("3. Exit")
        choice = input("Enter your choice (1/2/3): ")

        if choice == '1':
            # Random string generation
            num_strings = int(input("\nEnter the number of random strings to generate: "))
            print("\nGenerated random strings:")
            for _ in range(num_strings):
                rand_length = random.randint(1, 6)  # Random length for variety
                
                print("nfa start state", nfa._start_state)
                rand_string = generate_random_string_test(nfa, rand_length)
                print("rand string", rand_string)
                if rand_string:
                    print(rand_string)
                else:
                    print("Failed to generate a valid string.")
        elif choice == '2':
            # Enumerate valid strings
            max_length = int(input("\nEnter the maximum string length to enumerate: "))
            print("\nEnumerating strings...")
            valid_strings = enumerate_strings(nfa, max_length)
            print(f"\nTotal strings found: {len(valid_strings)}")
            for string in valid_strings:
                print(string)
        elif choice == '3':
            print("\nExiting the tool. Goodbye!")
            break
        else:
            print("\nInvalid choice. Please select 1, 2, or 3.")


if __name__ == "__main__":
    main()
