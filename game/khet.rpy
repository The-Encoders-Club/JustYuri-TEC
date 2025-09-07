# --- Khet Game Screen and Labels ---

# Define a persistent variable to hold the game result for the label block.
default persistent.khet_winner = None # None=Game in progress, 0=AI won, 1=Player won

# This label starts the game sequence.
label Khet:
    python:
        # Ren'Py specific setup
        renpy.dynamic(player_team=True, yuri_team=True, khet_engine=True)
        DisableTalk()
        boopable = False
        persistent.khet_winner = None # Reset winner state

    menu:
        y "Oh, so you'd like to play some Khet, hm?"
        "Yes.":
            y "Oh, good."
        "No.":
            y "I see..."
            y "Perhaps some other time, then."
            jump ch30_loop # Assumes you have a ch30_loop label to return to

    menu:
        y "Do you want me to explain the rules?"
        "Yes.":
            jump ExplainRules
        "No.":
            y "I see. Let's get right to it, then."
            jump StartKhet

# This label handles the game setup menus.
label StartKhet:
    $ layout_choice = "classic"
    menu:
        y "What starting configuration would you like to play?"
        "Classic":
            $ layout_choice = "classic"
        "Dynasty":
            $ layout_choice = "dynasty"
        "Imhotep":
            $ layout_choice = "imhotep"

    $ ai_difficulty = 1000
    menu:
        y "Would you like me to go easy on you?"
        "Yes. (Easy)":
            $ ai_difficulty = 500 # Faster, less thorough
        "Maybe. (Normal)":
            $ ai_difficulty = 1500 # A good balance
        "No. (Hard)":
            $ ai_difficulty = 5000 # More challenging, but thinks longer
        "Bring it on. (Expert)":
            $ ai_difficulty = 10000 # Very thorough, may cause noticeable pauses

    $ player_team = Team.SILVER
    menu:
        y "Would you like to play first (Silver)?"
        "Silver.":
            $ player_team = Team.SILVER
            $ yuri_team = Team.RED
        "Red.":
            $ player_team = Team.RED
            $ yuri_team = Team.SILVER

    # Create an instance of our new game engine
    $ khet_engine = KhetGame(setup=layout_choice)

    # If the player chose Red, the game's turn must be set to Red.
    if player_team == Team.RED:
        $ khet_engine.current_turn = Team.RED

    # Call the main game screen
    call screen KhetScreen(game_engine=khet_engine, player_team=player_team, yuri_team=yuri_team, difficulty=ai_difficulty)

# This label handles the game's conclusion.
label Khet_over:
    if persistent.khet_winner == 0:
        $ show_chr("A-ABAAA-AAAD") # Assumes you have this character display logic
        y "Oh, I won!"
        y "That was quite fun, [player]!"
        y "It's a very interesting game, there's no doubt about that."
        y "Maybe next time..."
    elif persistent.khet_winner == 1:
        $ show_chr("A-BEBAA-AMAM")
        y "Congrats, [player]!"
        $ show_chr("A-ABAAA-AAAA")
        y "This is quite fun, I must admit!"
        y "Don't get too ahead of yourself, though. I may have a new trick or two for the next time we play."
    else:
        # Fallback for unexpected states
        y "Well, that was an interesting game!"

    jump ch30_loop # Return to the main loop

# The main game screen. It hosts the custom displayable that runs the game.
screen KhetScreen(game_engine, player_team, yuri_team, difficulty):
    # Use a modal screen to prevent clicking on things behind the game.
    modal True

    # This fixed container will take up the full 1280x720 screen.
    # The alignment properties (xalign, yalign) will center its single child.
    fixed:
        xalign 0.5  # Center horizontally
        yalign 0.5  # Center vertically

        # Add the KhetDisplayable here. Since its size is 700x560 (10x8 cells of 70px),
        # Ren'Py will automatically center this 700x560 area within the 1280x720 screen.
        add KhetDisplayable(
            game=game_engine,
            player_team=player_team,
            yuri_team=yuri_team,
            ai_difficulty=difficulty
        )

    # UI element to show whose turn it is. This is positioned relative
    # to the whole screen, not the game board.
    frame:
        style "default"
        xalign 0.5      # Center horizontally on the screen
        yalign 0.05     # Place near the top of the screen
        text "Current Turn: [game_engine.current_turn.capitalize()]" font "gui/font/Aller_Rg.ttf" size 22

# This label contains the rules explanation. It can be expanded as needed.
label ExplainRules:
    y "Khet is a chess-like game with lasers. The goal is to hit the opponent's Pharaoh."
    y "On your turn, you can move a piece one square, or rotate it 90 degrees."
    y "After your move, your Sphinx will fire its laser automatically."
    y "Pieces with mirrored sides will bounce the laser."
    y "If the laser hits a non-mirrored side, the piece is removed."
    y "The Pharaoh, Anubis, Pyramid, and Scarab are your key pieces."
    y "The Sphinx fires the laser and can only rotate."
    y "Good luck!"
    jump StartKhet


# --- The Khet Game Engine and Displayable (The Core Logic) ---

init -1 python:
    import collections
    import random
    import time

    # --- Data Structures and Constants ---
    Position = collections.namedtuple("Position", ["x", "y"])

    class PieceType:
        PHARAOH = "pharaoh"
        ANUBIS = "anubis"
        PYRAMID = "pyramid"
        SCARAB = "scarab"
        SPHINX = "sphinx"

    class Team:
        SILVER = "silver"
        RED = "red"

    class Orientation:
        UP = 0
        RIGHT = 90
        DOWN = 180
        LEFT = 270

    class KhetAssets:
        """A class to pre-load and manage all visual assets for the game."""
        def __init__(self):
            # Define cell size based on piece assets (59px) + padding
            self.PIECE_SIZE = 59
            self.CELL_SIZE = 70
            self.BOARD_WIDTH_CELLS = 10
            self.BOARD_HEIGHT_CELLS = 8

            # Load images
            self.images = {
                'board': "images/khet/board.png",
                'move': "images/khet/move.png",
                'target': "images/khet/target.png",
                'laser': Transform("images/khet/laser.png", size=(self.CELL_SIZE, self.CELL_SIZE), yalign=0.5),
                'laser_bounce': "images/khet/laser_bounce.png",
                'hit': "images/khet/aaa.png",
                Team.SILVER: {
                    PieceType.ANUBIS: "images/khet/Silver/anubis.png",
                    PieceType.PHARAOH: "images/khet/Silver/pharaoh.png",
                    PieceType.PYRAMID: "images/khet/Silver/pyramid.png",
                    PieceType.SCARAB: "images/khet/Silver/scarab.png",
                    PieceType.SPHINX: "images/khet/Silver/sphinx.png",
                },
                Team.RED: {
                    PieceType.ANUBIS: "images/khet/Red/anubis.png",
                    PieceType.PHARAOH: "images/khet/Red/pharaoh.png",
                    PieceType.PYRAMID: "images/khet/Red/pyramid.png",
                    PieceType.SCARAB: "images/khet/Red/scarab.png",
                    PieceType.SPHINX: "images/khet/Red/sphinx.png",
                }
            }
            # Pre-load displayables for performance
            for key, value in self.images.items():
                if isinstance(value, dict):
                    for sub_key, sub_value in value.items():
                        value[sub_key] = renpy.displayable(sub_value)
                else:
                    self.images[key] = renpy.displayable(value)

    # --- Piece and Game State Classes ---
    class Piece:
        """Represents a single piece on the board."""
        def __init__(self, piece_type, team, position, orientation=Orientation.UP):
            self.type = piece_type
            self.team = team
            self.position = position
            self.orientation = orientation
        def __repr__(self):
            return f"{self.team.capitalize()} {self.type.capitalize()} at {self.position}"
        def copy(self):
            return Piece(self.type, self.team, self.position, self.orientation)

    class KhetGame:
        """The main game engine. Manages the board state, rules, and logic."""
        def __init__(self, setup="classic"):
            self.board = [[None for _ in range(8)] for _ in range(10)]
            self.current_turn = Team.SILVER
            self.winner = None
            self._setup_board(setup)

        def copy(self):
            """Creates a deep copy of the game state for AI simulation."""
            new_game = KhetGame()
            new_game.current_turn = self.current_turn
            new_game.winner = self.winner
            for x in range(10):
                for y in range(8):
                    if self.board[x][y]:
                        new_game.board[x][y] = self.board[x][y].copy()
                    else:
                        new_game.board[x][y] = None
            return new_game

        def _setup_board(self, setup):
            """Populates the board with one of the standard layouts."""
            self.board = [[None for _ in range(8)] for _ in range(10)]
            layouts = {
                "classic": {
                    (0, 0): Piece(PieceType.SPHINX, Team.RED, Position(0, 0), Orientation.RIGHT), (4, 0): Piece(PieceType.ANUBIS, Team.RED, Position(4, 0), Orientation.DOWN), (5, 0): Piece(PieceType.PHARAOH, Team.RED, Position(5, 0), Orientation.DOWN), (6, 0): Piece(PieceType.ANUBIS, Team.RED, Position(6, 0), Orientation.DOWN), (1, 3): Piece(PieceType.PYRAMID, Team.RED, Position(1, 3), Orientation.RIGHT), (3, 3): Piece(PieceType.SCARAB, Team.RED, Position(3, 3), Orientation.UP), (6, 3): Piece(PieceType.SCARAB, Team.RED, Position(6, 3), Orientation.RIGHT), (8, 3): Piece(PieceType.PYRAMID, Team.RED, Position(8, 3), Orientation.UP),
                    (9, 7): Piece(PieceType.SPHINX, Team.SILVER, Position(9, 7), Orientation.LEFT), (3, 7): Piece(PieceType.ANUBIS, Team.SILVER, Position(3, 7), Orientation.UP), (4, 7): Piece(PieceType.PHARAOH, Team.SILVER, Position(4, 7), Orientation.UP), (5, 7): Piece(PieceType.ANUBIS, Team.SILVER, Position(5, 7), Orientation.UP), (1, 4): Piece(PieceType.PYRAMID, Team.SILVER, Position(1, 4), Orientation.DOWN), (3, 4): Piece(PieceType.SCARAB, Team.SILVER, Position(3, 4), Orientation.LEFT), (6, 4): Piece(PieceType.SCARAB, Team.SILVER, Position(6, 4), Orientation.UP), (8, 4): Piece(PieceType.PYRAMID, Team.SILVER, Position(8, 4), Orientation.LEFT),
                },
                "imhotep": {
                    (0, 0): Piece(PieceType.SPHINX, Team.RED, Position(0,0), Orientation.RIGHT), (2, 0): Piece(PieceType.PYRAMID, Team.RED, Position(2,0), Orientation.DOWN), (4, 0): Piece(PieceType.ANUBIS, Team.RED, Position(4,0), Orientation.DOWN), (5, 0): Piece(PieceType.PHARAOH, Team.RED, Position(5,0), Orientation.DOWN), (7, 0): Piece(PieceType.PYRAMID, Team.RED, Position(7,0), Orientation.DOWN), (1, 3): Piece(PieceType.SCARAB, Team.RED, Position(1,3), Orientation.RIGHT), (8, 3): Piece(PieceType.SCARAB, Team.RED, Position(8,3), Orientation.UP),
                    (9, 7): Piece(PieceType.SPHINX, Team.SILVER, Position(9,7), Orientation.LEFT), (2, 7): Piece(PieceType.PYRAMID, Team.SILVER, Position(2,7), Orientation.UP), (4, 7): Piece(PieceType.PHARAOH, Team.SILVER, Position(4,7), Orientation.UP), (5, 7): Piece(PieceType.ANUBIS, Team.SILVER, Position(5,7), Orientation.UP), (7, 7): Piece(PieceType.PYRAMID, Team.SILVER, Position(7,7), Orientation.UP), (1, 4): Piece(PieceType.SCARAB, Team.SILVER, Position(1,4), Orientation.DOWN), (8, 4): Piece(PieceType.SCARAB, Team.SILVER, Position(8,4), Orientation.LEFT),
                },
                "dynasty": {
                    (0, 0): Piece(PieceType.SPHINX, Team.RED, Position(0,0), Orientation.RIGHT), (3, 0): Piece(PieceType.PYRAMID, Team.RED, Position(3,0), Orientation.RIGHT), (4, 0): Piece(PieceType.PYRAMID, Team.RED, Position(4,0), Orientation.DOWN), (5, 0): Piece(PieceType.PHARAOH, Team.RED, Position(5,0), Orientation.DOWN), (2, 1): Piece(PieceType.ANUBIS, Team.RED, Position(2,1), Orientation.DOWN), (7, 1): Piece(PieceType.ANUBIS, Team.RED, Position(7,1), Orientation.DOWN), (2, 4): Piece(PieceType.SCARAB, Team.RED, Position(2,4), Orientation.UP), (7, 4): Piece(PieceType.SCARAB, Team.RED, Position(7,4), Orientation.UP),
                    (9, 7): Piece(PieceType.SPHINX, Team.SILVER, Position(9,7), Orientation.LEFT), (6, 7): Piece(PieceType.PYRAMID, Team.SILVER, Position(6,7), Orientation.LEFT), (5, 7): Piece(PieceType.PYRAMID, Team.SILVER, Position(5,7), Orientation.UP), (4, 7): Piece(PieceType.PHARAOH, Team.SILVER, Position(4,7), Orientation.UP), (2, 6): Piece(PieceType.ANUBIS, Team.SILVER, Position(2,6), Orientation.UP), (7, 6): Piece(PieceType.ANUBIS, Team.SILVER, Position(7,6), Orientation.UP), (2, 3): Piece(PieceType.SCARAB, Team.SILVER, Position(2,3), Orientation.DOWN), (7, 3): Piece(PieceType.SCARAB, Team.SILVER, Position(7,3), Orientation.DOWN),
                }
            }
            if setup in layouts:
                for pos, piece in layouts[setup].items():
                    self.board[pos[0]][pos[1]] = piece

        def get_piece_at(self, pos):
            return self.board[pos.x][pos.y] if 0 <= pos.x < 10 and 0 <= pos.y < 8 else None

        def get_valid_moves(self, piece):
            """Returns a list of valid actions for a piece."""
            moves = []
            if not piece or piece.team != self.current_turn:
                return []
            
            # Rotations (all pieces can rotate)
            moves.append({'action': 'rotate', 'orientation': (piece.orientation + 90) % 360})
            moves.append({'action': 'rotate', 'orientation': (piece.orientation - 90 + 360) % 360})

            # Moves (Sphinx cannot move)
            if piece.type != PieceType.SPHINX:
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx == 0 and dy == 0: continue
                        new_pos = Position(piece.position.x + dx, piece.position.y + dy)
                        target = self.get_piece_at(new_pos)
                        if target is None: # Standard move to empty square
                             moves.append({'action': 'move', 'position': new_pos})
                        # Scarab swap logic
                        elif piece.type == PieceType.SCARAB and target.type in [PieceType.ANUBIS, PieceType.PYRAMID]:
                            moves.append({'action': 'swap', 'position': new_pos})
            return moves

        def apply_action(self, piece, action):
            """Applies a move, rotation, or swap action."""
            if action['action'] == 'rotate':
                piece.orientation = action['orientation']
            else: # move or swap
                old_pos = piece.position
                new_pos = action['position']
                target_piece = self.get_piece_at(new_pos)
                
                self.board[new_pos.x][new_pos.y] = piece
                piece.position = new_pos
                if action['action'] == 'swap':
                    self.board[old_pos.x][old_pos.y] = target_piece
                    target_piece.position = old_pos
                else:
                    self.board[old_pos.x][old_pos.y] = None
        
        def fire_laser(self, for_team):
            """Calculates the laser path and its result."""
            path, destroyed_piece = [], None
            sphinx = next((p for row in self.board for p in row if p and p.type == PieceType.SPHINX and p.team == for_team), None)
            if not sphinx: return path, destroyed_piece

            beam_pos, beam_dir = sphinx.position, sphinx.orientation
            path.append({'position': beam_pos, 'type': 'start', 'direction': beam_dir})
            
            for _ in range(30): # Safety break
                if beam_dir == Orientation.UP: beam_pos = Position(beam_pos.x, beam_pos.y - 1)
                elif beam_dir == Orientation.RIGHT: beam_pos = Position(beam_pos.x + 1, beam_pos.y)
                elif beam_dir == Orientation.DOWN: beam_pos = Position(beam_pos.x, beam_pos.y + 1)
                else: beam_pos = Position(beam_pos.x - 1, beam_pos.y)

                if not (0 <= beam_pos.x < 10 and 0 <= pos.y < 8):
                    path.append({'position': beam_pos, 'type': 'off_board', 'direction': beam_dir})
                    break

                piece_hit = self.get_piece_at(beam_pos)
                if not piece_hit:
                    path.append({'position': beam_pos, 'type': 'pass', 'direction': beam_dir})
                    continue

                # Determine laser interaction result
                result, new_dir = self.get_laser_interaction(piece_hit, beam_dir)
                path.append({'position': beam_pos, 'type': result, 'direction': beam_dir})
                
                if result == 'hit':
                    destroyed_piece = piece_hit
                    break
                elif result == 'stop':
                    break
                elif result == 'bounce':
                    beam_dir = new_dir
            
            # If a piece was destroyed, update the board and check for a winner
            if destroyed_piece:
                self.board[destroyed_piece.position.x][destroyed_piece.position.y] = None
                if destroyed_piece.type == PieceType.PHARAOH:
                    self.winner = for_team
            return path, destroyed_piece

        def get_laser_interaction(self, piece, beam_dir):
            """Core rules for what happens when a laser hits a piece."""
            # piece orientation, incoming beam direction -> result, new direction
            # This is the heart of the Khet rules engine.
            # Mirror sides deflect, non-mirror sides are hit. Some pieces have special rules.
            t, o = piece.type, piece.orientation
            
            if t == PieceType.SPHINX: return 'stop', None
            if t == PieceType.PHARAOH: return 'hit', None

            if t == PieceType.ANUBIS:
                if (o == Orientation.UP and beam_dir == Orientation.DOWN) or \
                   (o == Orientation.DOWN and beam_dir == Orientation.UP) or \
                   (o == Orientation.LEFT and beam_dir == Orientation.RIGHT) or \
                   (o == Orientation.RIGHT and beam_dir == Orientation.LEFT):
                    return 'stop', None # Hit indestructible front
                return 'hit', None # Hit vulnerable side

            if t == PieceType.PYRAMID:
                # UP (0) mirror is on the bottom-left hypotenuse
                if o == 0 and beam_dir == 180: return 'bounce', 90
                if o == 0 and beam_dir == 270: return 'bounce', 0
                # RIGHT (90) mirror is on the top-left hypotenuse
                if o == 90 and beam_dir == 180: return 'bounce', 270
                if o == 90 and beam_dir == 90: return 'bounce', 0
                # DOWN (180) mirror is on the top-right hypotenuse
                if o == 180 and beam_dir == 0: return 'bounce', 270
                if o == 180 and beam_dir == 90: return 'bounce', 180
                # LEFT (270) mirror is on the bottom-right hypotenuse
                if o == 270 and beam_dir == 0: return 'bounce', 90
                if o == 270 and beam_dir == 270: return 'bounce', 180
                return 'hit', None # Hit non-mirrored side

            if t == PieceType.SCARAB:
                # Reflects any beam back along its path
                if beam_dir in [0, 180]: # Vertical beam
                    if o in [0, 180]: return 'bounce', (beam_dir + 180) % 360 # Reflects back
                    else: # Horizontal orientation, deflects
                        if beam_dir == 0: return 'bounce', (270 if o == 90 else 90)
                        else: return 'bounce', (90 if o == 90 else 270)
                else: # Horizontal beam
                    if o in [90, 270]: return 'bounce', (beam_dir + 180) % 360 # Reflects back
                    else: # Vertical orientation, deflects
                        if beam_dir == 90: return 'bounce', (0 if o == 0 else 180)
                        else: return 'bounce', (180 if o == 0 else 0)
            return 'stop', None

        def end_turn(self):
            self.current_turn = Team.RED if self.current_turn == Team.SILVER else Team.SILVER

        def get_ai_move(self, difficulty):
            """Simple AI to select the best possible move."""
            my_team = self.current_turn
            opponent_team = Team.RED if my_team == Team.SILVER else Team.SILVER
            best_move = {'score': -9999, 'piece': None, 'action': None}
            
            my_pieces = [p for row in self.board for p in row if p and p.team == my_team]
            random.shuffle(my_pieces)

            candidate_moves = []
            for piece in my_pieces:
                for action in self.get_valid_moves(piece):
                    candidate_moves.append({'piece': piece, 'action': action})
            
            random.shuffle(candidate_moves) # Introduce variety

            for move in candidate_moves[:difficulty]: # Limit moves to check based on difficulty
                sim_game = self.copy()
                sim_piece = sim_game.get_piece_at(move['piece'].position)
                sim_game.apply_action(sim_piece, move['action'])
                _, destroyed = sim_game.fire_laser(my_team)

                score = 0
                if destroyed:
                    if destroyed.type == PieceType.PHARAOH: score = 1000 # Winning move
                    elif destroyed.type == PieceType.PYRAMID: score = 200
                    elif destroyed.type == PieceType.ANUBIS: score = 200
                    elif destroyed.type == PieceType.SCARAB: score = 100 # Can't happen, but for completeness
                
                # Check for suicide moves (if opponent can now win)
                _, opponent_destroyed = sim_game.fire_laser(opponent_team)
                if opponent_destroyed and opponent_destroyed.type == PieceType.PHARAOH and opponent_destroyed.team == my_team:
                    score = -1000 # Avoid moves that let the opponent win

                if score > best_move['score']:
                    best_move = {'score': score, 'piece': move['piece'], 'action': move['action']}
            
            # If no good move is found, pick a random one
            if best_move['piece'] is None and candidate_moves:
                return candidate_moves[0]
            
            return best_move

    # --- The Custom Displayable for Rendering and Events ---
    class KhetDisplayable(renpy.Displayable):
        def __init__(self, game, player_team, yuri_team, ai_difficulty, **kwargs):
            super(KhetDisplayable, self).__init__(**kwargs)
            self.game = game
            self.player_team = player_team
            self.yuri_team = yuri_team
            self.ai_difficulty = ai_difficulty
            self.assets = KhetAssets()

            # UI and Animation State
            self.selected_piece = None
            self.valid_moves_ui = []
            self.laser_path = []
            self.laser_anim_progress = 0.0
            self.last_st = 0.0
            self.is_animating = False
            self.ai_thinking = False

        def render(self, width, height, st, at):
            # Calculate timing delta
            if self.last_st == 0.0: self.last_st = st
            dtime = st - self.last_st
            self.last_st = st
            
            r = renpy.Render(self.assets.CELL_SIZE * 10, self.assets.CELL_SIZE * 8)
            
            # 1. Draw Board
            r.place(self.assets.images['board'], x=-5, y=-43) # Fine-tuned offset for the 710x566 board image

            # 2. Draw Pieces
            for piece in [p for row in self.game.board for p in row if p]:
                img = self.assets.images[piece.team][piece.type]
                d = Transform(img, rotate=piece.orientation, size=(self.assets.PIECE_SIZE, self.assets.PIECE_SIZE))
                x_pos = piece.position.x * self.assets.CELL_SIZE + (self.assets.CELL_SIZE - self.assets.PIECE_SIZE) / 2
                y_pos = piece.position.y * self.assets.CELL_SIZE + (self.assets.CELL_SIZE - self.assets.PIECE_SIZE) / 2
                r.place(d, x=x_pos, y=y_pos)

            # 3. Draw UI Highlights (Valid moves and selected piece)
            if self.selected_piece:
                pos = self.selected_piece.position
                r.place(self.assets.images['target'], x=pos.x * self.assets.CELL_SIZE, y=pos.y * self.assets.CELL_SIZE)
                for move in self.valid_moves_ui:
                    if move['action'] != 'rotate':
                        m_pos = move['position']
                        r.place(self.assets.images['move'], x=m_pos.x * self.assets.CELL_SIZE, y=m_pos.y * self.assets.CELL_SIZE)
            
            # 4. Draw Laser Animation
            if self.is_animating:
                self.laser_anim_progress += dtime * 15 # Speed of the laser
                path_to_draw = self.laser_path[:int(self.laser_anim_progress)]
                
                for segment in path_to_draw:
                    pos = segment['position']
                    x_pos, y_pos = pos.x * self.assets.CELL_SIZE, pos.y * self.assets.CELL_SIZE
                    
                    if segment['type'] == 'pass' or segment['type'] == 'start':
                        r.place(Transform(self.assets.images['laser'], rotate=segment['direction']), x=x_pos, y=y_pos)
                    elif segment['type'] == 'bounce':
                        # Complex rotation logic for bounce sprite would go here if needed.
                        r.place(self.assets.images['hit'], x=x_pos, y=y_pos) # Simple flash for bounce
                    elif segment['type'] == 'hit':
                        r.place(self.assets.images['hit'], x=x_pos, y=y_pos)

                if int(self.laser_anim_progress) > len(self.laser_path):
                    self.is_animating = False
                    self.laser_path = []
                    if self.game.winner:
                        persistent.khet_winner = 1 if self.game.winner == self.player_team else 0
                        renpy.jump("Khet_over")
                    else:
                        self.game.end_turn()

            renpy.redraw(self, 0.05) # Redraw continuously for smooth animation
            return r

        def event(self, ev, x, y, st):
            if self.is_animating or self.ai_thinking or self.game.winner:
                return

            # --- AI TURN LOGIC ---
            if self.game.current_turn == self.yuri_team:
                self.ai_thinking = True
                renpy.redraw(self, 0)
                move = self.game.get_ai_move(self.ai_difficulty)
                if move and move['piece']:
                    piece_to_move = self.game.get_piece_at(move['piece'].position)
                    self.game.apply_action(piece_to_move, move['action'])
                    self.laser_path, _ = self.game.fire_laser(self.yuri_team)
                    self.is_animating = True
                    self.laser_anim_progress = 0
                else: # AI can't find a move (should not happen in a normal game)
                    self.game.end_turn()
                self.ai_thinking = False
                renpy.raise_signal("Redraw") # Force a redraw after AI move
                return

            # --- PLAYER TURN LOGIC ---
            # **** Convert x and y to int before division ****
            grid_x = int(x) // self.assets.CELL_SIZE
            grid_y = int(y) // self.assets.CELL_SIZE
            clicked_pos = Position(grid_x, grid_y)

            def player_commit_action(piece, action):
                self.game.apply_action(piece, action)
                self.laser_path, _ = self.game.fire_laser(self.player_team)
                self.is_animating = True
                self.laser_anim_progress = 0
                self.selected_piece = None
                self.valid_moves_ui = []
                renpy.raise_signal("Redraw")

            # Handle Keyboard Input for Rotation
            if self.selected_piece and ev.type == pygame.KEYDOWN:
                action = None
                if ev.key == pygame.K_RIGHT:
                    action = {'action': 'rotate', 'orientation': (self.selected_piece.orientation + 90) % 360}
                elif ev.key == pygame.K_LEFT:
                    action = {'action': 'rotate', 'orientation': (self.selected_piece.orientation - 90 + 360) % 360}
                if action:
                    player_commit_action(self.selected_piece, action)
                    return

            # Handle Mouse Clicks
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                # If a piece is selected, check if click is a valid move
                if self.selected_piece:
                    for move in self.valid_moves_ui:
                        if move['action'] != 'rotate' and move['position'] == clicked_pos:
                            player_commit_action(self.selected_piece, move)
                            return
                
                # If no piece is selected, or click was not a move, try to select a new piece
                piece_at_click = self.game.get_piece_at(clicked_pos)
                if piece_at_click and piece_at_click.team == self.player_team:
                    self.selected_piece = piece_at_click
                    self.valid_moves_ui = self.game.get_valid_moves(piece_at_click)
                else: # Clicked on empty square or enemy
                    self.selected_piece = None
                    self.valid_moves_ui = []
                renpy.redraw(self, 0) # Redraw to show new selection