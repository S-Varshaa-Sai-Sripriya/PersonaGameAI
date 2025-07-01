# rl_agent.py
import random
import config 

class RLAgent:
    """
    Implements a Q-learning agent that learns to achieve specific goals
    (aggressive or evasive) based on rewards. This version uses dual Q-tables
    to maintain separate policies for each persona.
    """
    def __init__(self):
        """
        Initializes the RLAgent with two separate Q-tables, one for each persona.
        """
        
        self.q_table_aggressive = {}
        
        self.q_table_evasive = {}

    def _get_active_q_table(self, persona):
        """
        Helper method to return the correct Q-table based on the current persona.
        """
        if persona == 'aggressive':
            return self.q_table_aggressive
        elif persona == 'evasive':
            return self.q_table_evasive
        else:
            raise ValueError(f"Unknown persona: {persona}")

    def get_q_values(self, state, persona):
        """
        Retrieves the Q-values for a given state from the active Q-table.
        If the state is new for the current persona's Q-table, it initializes its Q-values to zeros.

        Args:
            state (str): The state key obtained from the environment.
            persona (str): The AI's current persona ('aggressive' or 'evasive').

        Returns:
            list: A list of Q-values for each possible action in that state.
        """
        active_q_table = self._get_active_q_table(persona)
        if state not in active_q_table:
            active_q_table[state] = [0.0] * len(config.ACTIONS) 
        return active_q_table[state]

    def choose_action(self, state, persona):
        """
        Chooses an action using an epsilon-greedy policy, consulting the Q-table
        corresponding to the current persona.

        Args:
            state (str): The current state key.
            persona (str): The AI's current persona ('aggressive' or 'evasive').

        Returns:
            int: The index of the chosen action from config.ACTIONS.
        """
        if random.random() < config.EXPLORATION_RATE:
            
            return random.randrange(len(config.ACTIONS))
        else:
            
            q_values = self.get_q_values(state, persona)
            max_q = -float('inf')
            best_action_idx = 0
            for i, q_val in enumerate(q_values):
                if q_val > max_q:
                    max_q = q_val
                    best_action_idx = i
            return best_action_idx

    def get_reward(self, old_ai_distance, new_ai_distance, persona):
        """
        Calculates the reward for the AI based on its current persona and movement.
        (This function remains the same as reward definition is persona-dependent).

        Args:
            old_ai_distance (float): Distance from AI to player before the move.
            new_ai_distance (float): Distance from AI to player after the move.
            persona (str): The AI's current persona ('aggressive' or 'evasive').

        Returns:
            int: The calculated reward (+1 or -1).
        """
        if persona == 'aggressive':
            
            return 1 if new_ai_distance < old_ai_distance else -1
        elif persona == 'evasive':
            
            return 1 if new_ai_distance > old_ai_distance else -1
        return 0 

    def update_q_table(self, old_state, action_idx, reward, new_state, persona):
        """
        Updates the Q-value for the (old_state, action_idx) pair in the
        active Q-table (corresponding to the current persona).

        Args:
            old_state (str): The state key before the action was taken.
            action_idx (int): The index of the action taken.
            reward (int): The reward received for taking the action.
            new_state (str): The state key after the action was taken.
            persona (str): The AI's current persona ('aggressive' or 'evasive').
        """
        active_q_table = self._get_active_q_table(persona)
        
        old_q = self.get_q_values(old_state, persona)[action_idx] 
        max_new_q = max(self.get_q_values(new_state, persona)) 
        
        new_q = old_q + config.LEARNING_RATE * (reward + config.DISCOUNT_FACTOR * max_new_q - old_q)
        active_q_table[old_state][action_idx] = new_q

    def get_q_table_summary(self, persona, num_states=5):
        """
        Returns a summary of the Q-table for a specific persona for inspection.
        """
        active_q_table = self._get_active_q_table(persona)
        summary = {}
        for i, (state, q_values) in enumerate(active_q_table.items()):
            if i >= num_states:
                break
            summary[state] = q_values
        return summary

    def reset_all_q_tables(self):
        """
        Resets both Q-tables. This might be used for a full simulation restart,
        but not for persona switching in this dual-policy setup.
        """
        self.q_table_aggressive = {}
        self.q_table_evasive = {}
