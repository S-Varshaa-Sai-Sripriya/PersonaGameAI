# config.py

# --- Game Constants ---
CANVAS_WIDTH = 50  
CANVAS_HEIGHT = 20 
PLAYER_CHAR = 'P'
AI_CHAR_AGGRESSIVE = 'A'
AI_CHAR_EVASIVE = 'E'
EMPTY_CHAR = '.'

# Movement speed (steps per turn)
SPEED = 1

# --- Reinforcement Learning Parameters ---
LEARNING_RATE = 0.1    
DISCOUNT_FACTOR = 0.9  
EXPLORATION_RATE = 0.1 
ACTIONS = [
    (0, 0),   
    (0, -1),  
    (0, 1),   
    (-1, 0),  
    (1, 0)     
]

# --- Persona Adaptation Parameters ---
TREND_THRESHOLD = 5      
PERSONA_CHANGE_COOLDOWN_STEPS = 3 
CLOSE_RADIUS = 10 
FAR_RADIUS = 5   

# --- Simulation Parameters ---
NUM_SIMULATION_STEPS = 10 
SIMULATION_DELAY_SECONDS = 0.1 
