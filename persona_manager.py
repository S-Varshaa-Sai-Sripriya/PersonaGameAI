# persona_manager.py
import config 
import math

class PersonaManager:
    """
    Manages the AI's persona, adapting it based on player interaction patterns.
    """
    def __init__(self, initial_persona='aggressive'):
        """
        Initializes the persona manager.

        Args:
            initial_persona (str): The starting persona for the AI.
        """
        self.ai_persona = initial_persona
        self.player_movement_trend = 0 
        self.last_persona_change_step = 0

    def update_persona(self, player_pos, ai_pos, current_step):
        """
        Updates the AI's persona based on the player's proximity and interaction trend.
        If player is consistently close, AI becomes evasive.
        If player is consistently far, AI becomes aggressive.

        Args:
            player_pos (dict): The current position of the player.
            ai_pos (dict): The current position of the AI.
            current_step (int): The current simulation step.

        Returns:
            bool: True if the persona changed, False otherwise.
        """
        persona_changed = False

        if current_step - self.last_persona_change_step < config.PERSONA_CHANGE_COOLDOWN_STEPS:
            return persona_changed 

       
        dx = player_pos['x'] - ai_pos['x']
        dy = player_pos['y'] - ai_pos['y']
        current_distance = math.sqrt(dx * dx + dy * dy)

        if current_distance < config.CLOSE_RADIUS and self.ai_persona != 'evasive':
            self.player_movement_trend += 1
            if self.player_movement_trend > config.TREND_THRESHOLD:
                self.ai_persona = 'evasive'
                print(f"\n--- AI Persona changed to: EVASIVE ---")
                self.last_persona_change_step = current_step
                self.player_movement_trend = 0 
                persona_changed = True
        elif current_distance > config.FAR_RADIUS and self.ai_persona != 'aggressive':
            self.player_movement_trend -= 1
            if self.player_movement_trend < -config.TREND_THRESHOLD:
                self.ai_persona = 'aggressive'
                print(f"\n--- AI Persona changed to: AGGRESSIVE ---")
                self.last_persona_change_step = current_step
                self.player_movement_trend = 0 
                persona_changed = True
        else:
           
            if self.player_movement_trend > 0:
                self.player_movement_trend = max(0, self.player_movement_trend - 1)
            elif self.player_movement_trend < 0:
                self.player_movement_trend = min(0, self.player_movement_trend + 1)
        
        return persona_changed

    def get_current_persona(self):
        """
        Returns the AI's current persona.
        """
        return self.ai_persona

    def reset(self, initial_persona='aggressive'):
        """
        Resets the persona manager to its initial state.
        """
        self.ai_persona = initial_persona
        self.player_movement_trend = 0
        self.last_persona_change_step = 0
