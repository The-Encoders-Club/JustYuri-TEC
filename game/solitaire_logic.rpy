init python:
    import random

    # Configuration constants
    # Ensure your images are in game/solitaire/
    CARD_PATH = "game/solitaire/"
    
    SUITS = ["hearts", "diamonds", "clubs", "spades"]
    RANKS = range(1, 14) # 1 to 13
    RED_SUITS = ["hearts", "diamonds"]

    class Card:
        def __init__(self, suit, rank):
            self.suit = suit
            self.rank = rank
            self.is_face_up = False
        
        def color(self):
            return "red" if self.suit in RED_SUITS else "black"

        # This generates the filename automatically: e.g. "hearts_12.png"
        def image_file(self):
            if self.is_face_up:
                return f"{CARD_PATH}{self.suit}_{self.rank}.png"
            else:
                return f"{CARD_PATH}card_back.png"

    class SolitaireEngine:
        def __init__(self):
            self.deck = []
            self.tableau = [[] for _ in range(7)] 
            self.foundations = {s: [] for s in SUITS} 
            self.stock = [] 
            self.waste = [] 
            self.selected_card = None 
            self.selected_source = None 
            self.initialize_game()

        def initialize_game(self):
            self.deck = [Card(s, r) for s in SUITS for r in RANKS]
            random.shuffle(self.deck)

            # Deal to Tableau
            for i in range(7):
                for j in range(i + 1):
                    if self.deck:
                        card = self.deck.pop()
                        if j == i:
                            card.is_face_up = True
                        self.tableau[i].append(card)
            
            self.stock = self.deck
            self.waste = []

        def draw_card(self):
            if self.stock:
                card = self.stock.pop()
                card.is_face_up = True
                self.waste.append(card)
            elif self.waste:
                self.stock = list(reversed(self.waste))
                for c in self.stock:
                    c.is_face_up = False
                self.waste = []
            self.selected_card = None

        def select_card(self, card, source_type, index=None):
            # Only face-up cards can be interacted with
            if not card.is_face_up:
                return
            
            # Deselect if clicking the same card
            if self.selected_card == card:
                self.selected_card = None
                self.selected_source = None
                return

            # If a card is already selected, try to move it to this new card
            if self.selected_card:
                self.attempt_move(target_type=source_type, target_index=index)
            else:
                self.selected_card = card
                self.selected_source = (source_type, index)
                renpy.sound.play("audio/hover.ogg") # Optional sound effect

        def select_empty_slot(self, target_type, index=None):
            if self.selected_card:
                self.attempt_move(target_type, index)

        def attempt_move(self, target_type, target_index):
            card = self.selected_card
            source_type, source_idx = self.selected_source
            move_successful = False

            # 1. Moving to Foundation (Top Right Piles)
            if target_type == "foundation":
                suit = list(self.foundations.keys())[target_index]
                pile = self.foundations[suit]
                
                # Must handle moving only the top single card
                if self.is_top_card(card, source_type, source_idx):
                    if card.suit == suit:
                        if (not pile and card.rank == 1) or (pile and card.rank == pile[-1].rank + 1):
                            pile.append(card)
                            self.remove_from_source(card, source_type, source_idx)
                            move_successful = True

            # 2. Moving to Tableau (Main Columns)
            elif target_type == "tableau":
                pile = self.tableau[target_index]
                valid_placement = False
                
                if not pile:
                    if card.rank == 13: # King only on empty
                        valid_placement = True
                else:
                    top_card = pile[-1]
                    # Red on Black, Rank-1
                    if card.color() != top_card.color() and card.rank == top_card.rank - 1:
                        valid_placement = True
                
                if valid_placement:
                    stack = self.get_stack_from_source(card, source_type, source_idx)
                    for c in stack:
                        pile.append(c)
                    self.remove_stack_from_source(card, source_type, source_idx)
                    move_successful = True

            if move_successful:
                # renpy.sound.play("audio/page_flip.ogg") # Sound effect for placing card
                self.selected_card = None
                self.selected_source = None
                self.check_win()
            else:
                renpy.notify("Invalid Move")
                self.selected_card = None
                self.selected_source = None

        # --- Helpers ---
        def is_top_card(self, card, source_type, idx):
            if source_type == "waste": return card == self.waste[-1]
            if source_type == "tableau": return card == self.tableau[idx][-1]
            return False

        def get_stack_from_source(self, card, s_type, s_idx):
            if s_type == "waste": return [card]
            if s_type == "tableau":
                pile = self.tableau[s_idx]
                try: return pile[pile.index(card):]
                except: return []
            return []

        def remove_from_source(self, card, s_type, s_idx):
            if s_type == "waste": self.waste.pop()
            if s_type == "tableau": 
                self.tableau[s_idx].pop()
                self.flip_tableau_top(s_idx)

        def remove_stack_from_source(self, card, s_type, s_idx):
            if s_type == "waste": self.waste.pop()
            if s_type == "tableau":
                pile = self.tableau[s_idx]
                del pile[pile.index(card):]
                self.flip_tableau_top(s_idx)

        def flip_tableau_top(self, idx):
            if self.tableau[idx]:
                self.tableau[idx][-1].is_face_up = True

        def check_win(self):
            if sum(len(self.foundations[s]) for s in SUITS) == 52:
                renpy.notify("VICTORY!")