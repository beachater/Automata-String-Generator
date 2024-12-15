import random
from itertools import product
from pyformlang.regular_expression import Regex
from pyformlang.finite_automaton import Symbol


def user_regex_to_dfa(regex_string):
    """
    Converts a user-provided regex string into a deterministic finite automaton (DFA).
    """
    try:
        # Convert the regex to a minimal DFA
        dfa = Regex(regex_string).to_epsilon_nfa().to_deterministic().minimize()
        print("\nDFA Details:")
        print(f"Start State: {dfa.start_state}")
        print(f"Final States: {dfa.final_states}")
        print(f"Transitions: {dfa.to_dict()}")

        return dfa
    except Exception as e:
        print(f"Error converting regex to DFA: {e}")
        return None


def generate_random_string(dfa, max_length):
    """
    Generates a random string accepted by the DFA up to max_length.
    """
    transitions = dfa.to_dict()
    for _ in range(100):  # Try multiple attempts to generate a valid string
        current_state = dfa.start_state
        random_string = ""
        for _ in range(max_length):
            # Get possible transitions from the current state
            if current_state not in transitions:
                break

            possible_transitions = {
                symbol: transitions[current_state][symbol]
                for symbol in transitions[current_state]
            }

            if not possible_transitions:  # No valid transitions
                break

            # Randomly pick a transition
            symbol = random.choice(list(possible_transitions.keys()))
            current_state = possible_transitions[symbol]
            random_string += str(symbol)  # Convert Symbol to string

            # Check if we are in a final state and stop early
            if current_state in dfa.final_states:
                return random_string

        # If the loop finishes but doesn't reach a final state, try again
    return None  # Return None if no valid string could be generated after attempts


def enumerate_strings(dfa, max_length):
    """
    Enumerates all valid strings accepted by the DFA up to a given max string length.
    """
    valid_strings = []
    alphabet = list(dfa.symbols)  # Use DFA's symbols directly

    for length in range(1, max_length + 1):
        # Generate combinations of all possible strings of the given length
        for sequence in product(alphabet, repeat=length):
            # Convert tuple of symbols to string and check acceptance
            if dfa.accepts(sequence):
                valid_strings.append("".join(map(str, sequence)))

    return valid_strings


def main():
    print("Welcome to the formal language string generator tool!")
    user_input_regex = input("\nEnter a regular expression (e.g., a*(01|0)*b): ")

    print("\nConverting regex to DFA...")
    dfa = user_regex_to_dfa(user_input_regex)

    if not dfa:
        print("Invalid regex or unable to generate DFA. Exiting...")
        return

    print("\nDFA created successfully. Ready to perform operations.")

    while True:
        print("\nChoose an operation:")
        print("1. Generate random strings")
        print("2. Enumerate all valid strings up to a certain length")
        print("3. Exit")
        choice = input("Enter your choice (1/2/3): ")

        if choice == '1':
            num_strings = int(input("\nEnter the number of random strings to generate: "))
            max_length = int(input("Enter the maximum string length: "))
            print("\nGenerated random strings:")
            for _ in range(num_strings):
                rand_string = generate_random_string(dfa, max_length)
                if rand_string:
                    print(rand_string)
                else:
                    print("Failed to generate a valid string.")
        elif choice == '2':
            max_length = int(input("\nEnter the maximum string length to enumerate: "))
            print("\nEnumerating strings...")
            valid_strings = enumerate_strings(dfa, max_length)
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
