import numpy as np
from players.base_player import BasePlayer

class QLearningPlayer(BasePlayer):
    def __init__(self, learning_rate=0.1, discount_factor=0.95, exploration_rate=0.2, 
                 history_length=5, initial_value=0.0, pretrained_q_table=None):
        """
        Inicializacija igralca s spodbujevalnim učenjem.
        
        Args:
            learning_rate: Hitrost učenja (alpha) - kako hitro se posodabljajo Q-vrednosti
            discount_factor: Faktor diskontiranja (gamma) - pomembnost prihodnjih nagrad
            exploration_rate: Verjetnost raziskovanja (epsilon) - raziskovanje vs. izkoriščanje
            history_length: Koliko potez nazaj se upošteva pri odločanju
            initial_value: Začetna Q-vrednost za vse stanja
        """
        super().__init__()
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.history_length = history_length
        self.initial_value = initial_value
        
        # Q-tabela: ključ je stanje (zadnjih N potez nasprotnika in lastnih potez), 
        # vrednosti so Q-vrednosti za akciji cooperate/defect
        self.q_table = pretrained_q_table if pretrained_q_table else {} 
        
        # Zadnje stanje in akcija za učenje
        self.last_state = None
        self.last_action = None
        
    def _get_state(self, opponents_history):
        """Pretvori zgodovino potez v stanje za Q-tabelo"""
        # Če je zgodovina prekratka, uporabimo kar kar imamo
        if len(opponents_history) < self.history_length:
            opp_history = opponents_history.copy()
            my_history = self.past_actions.copy()
        else:
            # Uporabimo zadnjih N potez
            opp_history = opponents_history[-self.history_length:]
            my_history = self.past_actions[-self.history_length:]
        
        # Pretvorimo zgodovino v diskreten ključ za Q-tabelo
        # Uporabljamo "c" za cooperate in "d" za defect zaradi lažje berljivosti
        state_key = ""
        
        # Prvo dodamo nasprotnikovo zgodovino
        for action in opp_history:
            state_key += "c" if action == "cooperate" else "d"
            
        state_key += "|"  # Ločilo med nasprotnikovo in lastno zgodovino
        
        # Nato dodamo lastno zgodovino
        for action in my_history:
            state_key += "c" if action == "cooperate" else "d"
        
        return state_key
    
    def _get_q_values(self, state):
        """Vrne Q-vrednosti za podano stanje"""
        if state not in self.q_table:
            # Če stanje še ne obstaja, ga inicializiramo z začetnimi vrednostmi
            self.q_table[state] = {
                "cooperate": self.initial_value,
                "defect": self.initial_value
            }
        return self.q_table[state]
    
    def _get_reward(self, my_action, opponent_action):
        """Izračuna nagrado glede na poteze obeh igralcev"""
        # Nagrade določimo glede na leta zapora (nižje je bolje)
        if my_action == "cooperate" and opponent_action == "cooperate":
            return -1  # (1 leto)
        elif my_action == "cooperate" and opponent_action == "defect":
            return -20  # (20 let)
        elif my_action == "defect" and opponent_action == "cooperate":
            return 0  # (0 let)
        else:  # my_action == "defect" and opponent_action == "defect"
            return -5  # (5 let)
    
    def _update_q_values(self, state, action, next_state, reward):
        """Posodobi Q-vrednosti na podlagi nagrade in naslednjega stanja"""
        # Q-learning formula: Q(s,a) = Q(s,a) + α * [r + γ * max(Q(s',a')) - Q(s,a)]
        q_values = self._get_q_values(state)
        next_q_values = self._get_q_values(next_state)
        
        # Maksimalna Q-vrednost naslednjega stanja
        max_next_q = max(next_q_values["cooperate"], next_q_values["defect"])
        
        # Posodobitev trenutne Q-vrednosti
        current_q = q_values[action]
        new_q = current_q + self.learning_rate * (reward + self.discount_factor * max_next_q - current_q)
        self.q_table[state][action] = new_q
    
    def initial_action(self):
        """Prva poteza v igri"""
        self.last_state = "|"  # Prazno začetno stanje
        self.last_action = "cooperate"  # Začnemo sodelovalno
        return self.last_action
    
    def get_action(self, opponents_history: list):
        """Izbere akcijo glede na nasprotnikovo zgodovino"""
        if len(opponents_history) == 0:
            return self.initial_action()
        
        # Izračunamo trenutno stanje
        current_state = self._get_state(opponents_history)
        
        # Če imamo prejšnje stanje in akcijo, se učimo iz tega
        if self.last_state is not None and len(opponents_history) > 0:
            last_opponent_action = opponents_history[-1]
            reward = self._get_reward(self.last_action, last_opponent_action)
            self._update_q_values(self.last_state, self.last_action, current_state, reward)
        
        # Strategija epsilon-greedy: raziskovanje vs. izkoriščanje
        if np.random.random() < self.exploration_rate:
            # Raziskovanje: naključna izbira
            action = np.random.choice(["cooperate", "defect"])
        else:
            # Izkoriščanje: izbira akcije z najvišjo Q-vrednostjo
            q_values = self._get_q_values(current_state)
            if q_values["cooperate"] > q_values["defect"]:
                action = "cooperate"
            elif q_values["defect"] > q_values["cooperate"]:
                action = "defect"
            else:
                # Če sta vrednosti enaki, naključna izbira
                action = np.random.choice(["cooperate", "defect"])
        
        # Shranimo za naslednji krog učenja
        self.last_state = current_state
        self.last_action = action
        
        # Beleženje akcije in števca iger
        self.past_actions.append(action)
        self.num_games += 1
        
        return action
    
    def reset(self):
        """Ponastavi igralca na začetno stanje"""
        super().reset()
        self.last_state = None
        self.last_action = None
        # Q-tabelo ohranimo, da se igralec uči skozi več iger