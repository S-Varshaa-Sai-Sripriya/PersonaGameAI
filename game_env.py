# game_env.py
import math
import random
import config # Import our configuration constants

class GameEnvironment:
    """
    Manages the game state, including player and AI positions,
    and provides methods for updating positions and drawing the environment.
    """
    def __init__(self):
        """
        Initializes the game environment with player and AI starting positions.
        Both player and AI now start in the center of the canvas.
        """
        self.player = {'x': config.CANVAS_WIDTH // 2, 'y': config.CANVAS_HEIGHT // 2}
        
        self.ai = {'x': config.CANVAS_WIDTH // 2 + 100, 'y': config.CANVAS_HEIGHT // 2 + 100}  

    def move_entity(self, entity, dx, dy):
        """
        Moves an entity (player or AI) by (dx, dy) within the canvas boundaries.

        Args:
            entity (dict): The entity dictionary with 'x' and 'y' keys.
            dx (int): Change in x-coordinate.
            dy (int): Change in y-coordinate.
        """
        entity['x'] = max(0, min(config.CANVAS_WIDTH - 1, entity['x'] + dx * config.SPEED))
        entity['y'] = max(0, min(config.CANVAS_HEIGHT - 1, entity['y'] + dy * config.SPEED))

    def get_distance(self, pos1, pos2):
        """
        Calculates the Euclidean distance between two positions.

        Args:
            pos1 (dict): First position with 'x' and 'y'.
            pos2 (dict): Second position with 'x' and 'y'.

        Returns:
            float: The Euclidean distance.
        """
        return math.sqrt((pos1['x'] - pos2['x'])**2 + (pos1['y'] - pos2['y'])**2)

    def draw(self, ai_persona):
        """
        Draws the current game state to the console as a grid.

        Args:
            ai_persona (str): The current persona of the AI ('aggressive' or 'evasive')
                              to determine its character representation.
        """
        print("-" * (config.CANVAS_WIDTH + 2)) # Top border
        for y in range(config.CANVAS_HEIGHT):
            row = "|"
            for x in range(config.CANVAS_WIDTH):
                if x == self.player['x'] and y == self.player['y']:
                    row += config.PLAYER_CHAR
                elif x == self.ai['x'] and y == self.ai['y']:
                    row += config.AI_CHAR_AGGRESSIVE if ai_persona == 'aggressive' else config.AI_CHAR_EVASIVE
                else:
                    row += config.EMPTY_CHAR
            row += "|"
            print(row)
        print("-" * (config.CANVAS_WIDTH + 2)) # Bottom border

    def reset(self):
        """
        Resets the player and AI positions to their initial states (both in the center).
        """
        self.player = {'x': config.CANVAS_WIDTH // 2, 'y': config.CANVAS_HEIGHT // 2}
        self.ai = {'x': config.CANVAS_WIDTH // 2, 'y': config.CANVAS_HEIGHT // 2}

    def get_state_key(self):
        """
        Determines the current state key based on the relative position of the player to the AI.
        This is crucial for the RL agent to perceive the environment.

        Returns:
            str: A string representing the relative state (e.g., 'top-left', 'center').
        """
        dx = self.player['x'] - self.ai['x']
        dy = self.player['y'] - self.ai['y']

        state_key = ''

       
        if dy < -1:  
            state_key += 'top-'
        elif dy > 1: 
            state_key += 'bottom-'

        # Determine horizontal relation
        if dx < -1:  
            state_key += 'left'
        elif dx > 1: 
            state_key += 'right'

      
        if state_key == '':
            state_key = 'center'
        elif state_key == 'top-': 
            state_key = 'top'
        elif state_key == 'bottom-': 
            state_key = 'bottom'
        elif state_key == '-left': 
            state_key = 'left'
        elif state_key == '-right': 
            state_key = 'right'

        
        valid_states = ['top-left', 'top', 'top-right', 'left', 'center', 'right', 'bottom-left', 'bottom', 'bottom-right']
        if state_key not in valid_states:
            
            if abs(dx) <= 1 and abs(dy) <= 1: state_key = 'center'
            elif dy < 0 and abs(dx) <= 1: state_key = 'top'
            elif dy > 0 and abs(dx) <= 1: state_key = 'bottom'
            elif dx < 0 and abs(dy) <= 1: state_key = 'left'
            elif dx > 0 and abs(dy) <= 1: state_key = 'right'
            elif dy < 0 and dx < 0: state_key = 'top-left'
            elif dy < 0 and dx > 0: state_key = 'top-right'
            elif dy > 0 and dx < 0: state_key = 'bottom-left'
            elif dy > 0 and dx > 0: state_key = 'bottom-right'
            else: state_key = 'center' 

        return state_key
