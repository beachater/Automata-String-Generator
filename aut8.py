import random
import streamlit as st
from itertools import product
from pyformlang.regular_expression import Regex
from pyformlang.finite_automaton import Symbol
import pygraphviz as pgv
from io import StringIO


def user_regex_to_dfa(regex_string):
    """
    Converts a user-provided regex string into a deterministic finite automaton (DFA).
    """
    try:
        # Convert the regex to a minimal DFA
        dfa = Regex(regex_string).to_epsilon_nfa().to_deterministic().minimize()
        return dfa
    except Exception as e:
        st.error(f"Error converting regex to DFA: {e}")
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


def visualize_dfa(dfa):
    """
    Visualizes the DFA as a graph using pygraphviz.
    """
    graph = pgv.AGraph(strict=False, directed=True)
    
    # Add nodes for all states
    for state in dfa.states:
        if state in dfa.final_states:
            graph.add_node(state, shape='doublecircle', style='filled', color='lightblue')
        else:
            graph.add_node(state)
    
    # Add edges for all transitions
    for state, transitions in dfa.to_dict().items():
        for symbol, next_state in transitions.items():
            graph.add_edge(state, next_state, label=str(symbol))
    
    return graph


def main():
    st.title("Formal Language String Generator Tool")

    # Input for regular expression
    user_input_regex = st.text_input("Enter a regular expression (e.g., a*(01|0)*b):")
    
    if user_input_regex:
        # Convert the regex to DFA
        st.text("Converting regex to DFA...")
        dfa = user_regex_to_dfa(user_input_regex)

        if dfa:
            # Visualize DFA
            st.subheader("DFA Visualization")
            graph = visualize_dfa(dfa)
            img_path = "/tmp/dfa_graph.png"
            graph.layout(prog="dot")
            graph.draw(img_path)
            st.image(img_path)

            # Option for generating random strings
            st.subheader("Generate Random Strings")
            num_strings = st.number_input("Number of random strings to generate", min_value=1, value=5)
            max_length = st.number_input("Enter the maximum string length", min_value=1, value=5)

            if st.button("Generate"):
                st.text("Generated Random Strings:")
                for _ in range(num_strings):
                    rand_string = generate_random_string(dfa, max_length)
                    if rand_string:
                        st.text(rand_string)
                    else:
                        st.text("Failed to generate a valid string.")

            # Option for enumerating valid strings
            st.subheader("Enumerate Valid Strings")
            max_enum_length = st.number_input("Enter the maximum length to enumerate", min_value=1, value=5)

            if st.button("Enumerate"):
                st.text("Enumerating strings...")
                valid_strings = enumerate_strings(dfa, max_enum_length)
                st.text(f"Total strings found: {len(valid_strings)}")
                for string in valid_strings:
                    st.text(string)
        else:
            st.error("Invalid regex or unable to generate DFA.")

if __name__ == "__main__":
    main()
