import random
import streamlit as st
from itertools import product
from pyformlang.regular_expression import Regex
from pyformlang.finite_automaton import Symbol
import pygraphviz as pgv
from io import StringIO
from pyformlang.finite_automaton import State
from pyformlang.finite_automaton import DeterministicFiniteAutomaton

def rename_states(dfa):
    """
    Renames the states of a DFA to sequential letters starting from 'A'.
    """
    # Map existing states to sequential letters
    state_mapping = {state: State(chr(65 + idx)) for idx, state in enumerate(dfa.states)}

    # Create a new DFA with renamed states
    renamed_dfa = dfa.__class__()
    
    # Set the renamed start state
    renamed_dfa.add_start_state(state_mapping[dfa.start_state])

    # Set the renamed final states
    for final_state in dfa.final_states:
        renamed_dfa.add_final_state(state_mapping[final_state])

    # Add transitions with renamed states
    for state in dfa.states:
        for symbol in dfa.symbols:
            transitions = dfa.to_dict()
            if state in transitions and symbol in transitions[state]:
                next_state = transitions[state][symbol]
                renamed_dfa.add_transition(state_mapping[state], symbol, state_mapping[next_state])

    return renamed_dfa

def add_final_state_self_loops(dfa):
    """
    Adds a self-loop to each final state for the symbol that leads to it.
    This imitates the behavior of an NFA where the final state can accept more input symbols.
    """
    transitions = dfa.to_dict()

    # Iterate over all final states
    for final_state in dfa.final_states:
        # Iterate over all transitions to find the symbol that leads to the final state
        for state, transition_dict in transitions.items():
            for symbol, next_state in transition_dict.items():
                if next_state == final_state:
                    # Add a self-loop for this symbol on the final state
                    dfa.add_transition(final_state, symbol, final_state)

    return dfa

def user_regex_to_dfa(regex_string):
    """
    Converts a user-provided regex string into a deterministic finite automaton (DFA),
    and renames the states from 'A' to 'Z' for better visualization.
    """
    try:
        # Convert the regex to a minimal DFA
        dfa = Regex(regex_string).to_epsilon_nfa().to_deterministic().minimize()

        # Rename the states
        renamed_dfa = rename_states(dfa)
        
        renamed_dfa = add_final_state_self_loops(renamed_dfa)

        print("\nDFA Details (with renamed states):")
        print(f"Start State: {renamed_dfa.start_state}")
        print(f"Final States: {renamed_dfa.final_states}")
        print(f"Transitions: {renamed_dfa.to_dict()}")

        return renamed_dfa
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

def visualize_dfa(dfa, layout='dot'):
    """
    Visualizes the DFA as a graph using pygraphviz with structured and clean edges.
    :param dfa: The DFA to visualize.
    :param layout: The Graphviz layout engine to use ('dot', 'neato', etc.).
    """
    # Create the graph object
    graph = pgv.AGraph(strict=False, directed=True)

    # Set graph attributes for clean, structured layout
    graph.graph_attr.update(
        rankdir='LR',  # Horizontal layout
        nodesep='1',  # Space between nodes
        ranksep='1.5',  # Space between ranks (hierarchical layers)
        concentrate='false',  # Combine edges with same direction where possible
    )

    # Add nodes for all states
    for state in dfa.states:
        if state == dfa.start_state:
            # Highlight the start state
            graph.add_node(state, shape='circle', style='filled', color='lightgreen', fontcolor='black', width='0.5')
        elif state in dfa.final_states:
            # Highlight the final states
            graph.add_node(state, shape='doublecircle', style='filled', color='lightblue', fontcolor='black', width='0.5')
        else:
            # Default state style
            graph.add_node(state, shape='circle', style='filled', color='gray', fontcolor='black', width='0.5')

    # Add edges for all transitions
    for state, transitions in dfa.to_dict().items():
        for symbol, next_state in transitions.items():
            graph.add_edge(state, next_state, label=str(symbol), fontsize='10', color='black', weight='5')

    # Apply the chosen layout
    graph.layout(prog=layout)  # Set layout engine (default is 'dot' for structure)

    return graph

def main():
    st.title("Formal Language String Generator Tool")

    # Provide option to either generate DFA from regex or manually create automaton
    option = st.radio("Choose an option", ("Generate from Regex", "Make Own Automaton"))

    if option == "Generate from Regex":
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

    elif option == "Make Own Automaton":
        # Manually create DFA

        start_state = st.text_input("Enter start state:")
        final_states = st.text_input("Enter final states (comma separated):").split(",")
        transitions_input = st.text_area("Enter transitions (format: state1,symbol,state2):")
        
        if start_state and final_states and transitions_input:
            dfa = DeterministicFiniteAutomaton()
            dfa.add_start_state(State(start_state))

            for final_state in final_states:
                dfa.add_final_state(State(final_state.strip()))

            for transition in transitions_input.splitlines():
                state1, symbol, state2 = transition.split(",")
                dfa.add_transition(State(state1.strip()), symbol.strip(), State(state2.strip()))

            dfa = add_final_state_self_loops(dfa)

            # Visualize DFA
            st.subheader("DFA Visualization")
            graph = visualize_dfa(dfa)
            img_path = "/tmp/dfa_manual_graph.png"
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

if __name__ == "__main__":
    main()
