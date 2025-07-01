# app.py
from flask import Flask, render_template, request, jsonify
import json 
import config
from game_env import GameEnvironment
from rl_agent import RLAgent
from persona_manager import PersonaManager

app = Flask(__name__)


env = GameEnvironment()
rl_agent = RLAgent()
persona_manager = PersonaManager(initial_persona='aggressive')

@app.route('/')
def index():
    """
    Renders the main game HTML page.
    """
    return render_template('index.html')

@app.route('/get_initial_state', methods=['GET'])
def get_initial_state():
    """
    Provides the initial state of the game (player/AI positions, persona)
    to the frontend.
    """
    return jsonify({
        'player_pos': env.player,
        'ai_pos': env.ai,
        'ai_persona': persona_manager.get_current_persona()
    })

@app.route('/move_player', methods=['POST'])
def move_player():
    """
    Handles player movement requests from the frontend.
    """
    data = request.get_json()
    action_idx = data.get('action_idx')

    if action_idx is None or not (0 <= action_idx < len(config.ACTIONS)):
        return jsonify({'error': 'Invalid action index'}), 400

    dx, dy = config.ACTIONS[action_idx]
    env.move_entity(env.player, dx, dy)

    update_ai_logic()

    return jsonify({
        'player_pos': env.player,
        'ai_pos': env.ai,
        'ai_persona': persona_manager.get_current_persona()
    })

@app.route('/reset_game', methods=['POST'])
def reset_game():
    """
    Resets the game state and AI learning.
    """
    env.reset()
    rl_agent.reset_all_q_tables() 
    persona_manager.reset(initial_persona='aggressive')
    return jsonify({
        'player_pos': env.player,
        'ai_pos': env.ai,
        'ai_persona': persona_manager.get_current_persona()
    })

def update_ai_logic():
    """
    Encapsulates the AI's logic for a single step, including persona adaptation
    and RL learning. This is called after the player moves.
    """
    current_persona = persona_manager.get_current_persona()
    
    persona_manager.update_persona(env.player, env.ai, 100000) 
    old_ai_state = env.get_state_key()
    old_ai_distance = env.get_distance(env.player, env.ai)

    chosen_action_idx = rl_agent.choose_action(old_ai_state, current_persona)
    action_dx, action_dy = config.ACTIONS[chosen_action_idx]

    env.move_entity(env.ai, action_dx, action_dy)

    new_ai_distance = env.get_distance(env.player, env.ai)
    reward = rl_agent.get_reward(old_ai_distance, new_ai_distance, current_persona)
    new_ai_state = env.get_state_key()

    rl_agent.update_q_table(old_ai_state, chosen_action_idx, reward, new_ai_state, current_persona)

if __name__ == '__main__':
    app.run(debug=True) # debug=True enables auto-reloading and helpful error messages
