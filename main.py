# main.py
import time
import random
import config
from game_env import GameEnvironment
from rl_agent import RLAgent
from persona_manager import PersonaManager

def main():
    """
    Main function to run the PersonaGameAI simulation.
    Initializes the environment, RL agent, and persona manager,
    then runs the simulation loop. This version uses a dual-policy
    RL agent that maintains separate Q-tables for each persona.
    """
 
    env = GameEnvironment()
    rl_agent = RLAgent()
    persona_manager = PersonaManager(initial_persona='aggressive')

    print("Starting PersonaGameAI Simulation (Python Console Version)")
    print(f"Player: '{config.PLAYER_CHAR}', AI Aggressive: '{config.AI_CHAR_AGGRESSIVE}', AI Evasive: '{config.AI_CHAR_EVASIVE}'")
    print("Watch the AI's persona adapt based on player proximity.")
    print("-------------------------------------------------------")

    for step in range(config.NUM_SIMULATION_STEPS):
        print(f"\n--- Step {step + 1} ---")
        current_persona = persona_manager.get_current_persona()
        print(f"AI Persona: {current_persona.capitalize()}")

        player_move_choice = random.choice(config.ACTIONS)
        env.move_entity(env.player, player_move_choice[0], player_move_choice[1])

       
        persona_manager.update_persona(env.player, env.ai, step)

        old_ai_state = env.get_state_key()
        old_ai_distance = env.get_distance(env.player, env.ai)

        
        chosen_action_idx = rl_agent.choose_action(old_ai_state, current_persona)
        action_dx, action_dy = config.ACTIONS[chosen_action_idx]

     
        env.move_entity(env.ai, action_dx, action_dy)

        new_ai_distance = env.get_distance(env.player, env.ai)
        reward = rl_agent.get_reward(old_ai_distance, new_ai_distance, current_persona)
        new_ai_state = env.get_state_key()

        rl_agent.update_q_table(old_ai_state, chosen_action_idx, reward, new_ai_state, current_persona)

        # --- Draw Game State ---
        env.draw(current_persona)

        
        time.sleep(config.SIMULATION_DELAY_SECONDS)

    print("\n--- Simulation Complete ---")
    print("Final AI Persona:", persona_manager.get_current_persona().capitalize())
    
    
    print("\nFinal Aggressive Q-table (first few states):")
    for state, q_values in rl_agent.get_q_table_summary('aggressive').items():
        print(f"  State '{state}': {q_values}")
    
    print("\nFinal Evasive Q-table (first few states):")
    for state, q_values in rl_agent.get_q_table_summary('evasive').items():
        print(f"  State '{state}': {q_values}")


if __name__ == "__main__":
    main()
