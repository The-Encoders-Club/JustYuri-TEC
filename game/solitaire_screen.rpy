# The generic card object
screen render_card(card, x_pos, y_pos, click_action):
    button:
        pos (x_pos, y_pos)
        xysize (80, 116) # Adjust this size to match your asset ratio
        
        # Load the image dynamically
        background card.image_file()
        
        # Highlight logic (Yellow overlay when selected)
        if solitaire.selected_card == card:
            foreground Solid("#ffff00", alpha=0.3)
        
        action click_action

screen solitaire_game():
    modal True
    
    # Background (Dark Green Table)
    add Solid("#005500")

    # Quit Button
    textbutton "Exit Game":
        action Return()
        align (0.95, 0.05)
        text_color "#fff"
        text_hover_color "#fcc"

    # --- STOCK PILE (Draw) ---
    button:
        pos (50, 50)
        xysize (80, 116)
        # Show back of card if cards remain, otherwise showing Empty/Reset slot
        if solitaire.stock:
            background "game/solitaire/card_back.png"
        else:
            background "game/solitaire/empty_slot.png"
            text "Reset" align (0.5, 0.5) size 12 color "#fff"
        
        action Function(solitaire.draw_card)

    # --- WASTE PILE (Face Up Draw) ---
    if solitaire.waste:
        use render_card(solitaire.waste[-1], 150, 50, Function(solitaire.select_card, solitaire.waste[-1], "waste"))

    # --- FOUNDATIONS (Top Right) ---
    $ x_start_found = 600
    for i, suit in enumerate(solitaire.foundations):
        $ pile = solitaire.foundations[suit]
        $ current_x = x_start_found + (i * 100)
        
        # Base slot (The green empty card)
        imagebutton:
            idle "mod_assets/games/solitaire/empty_slot.png"
            pos (current_x, 50)
            xysize (80, 116)
            action Function(solitaire.select_empty_slot, "foundation", i)

        # Top card if exists
        if pile:
            use render_card(pile[-1], current_x, 50, Function(solitaire.select_card, pile[-1], "foundation", i))

    # --- TABLEAU (Main Game Rows) ---
    $ x_start_tab = 100
    for i in range(7):
        $ pile = solitaire.tableau[i]
        $ col_x = x_start_tab + (i * 120)
        $ start_y = 200
        
        # Empty slot detector (Green card)
        if not pile:
            imagebutton:
                idle "mod_assets/games/solitaire/empty_slot.png"
                pos (col_x, start_y)
                xysize (80, 116)
                action Function(solitaire.select_empty_slot, "tableau", i)
        
        # Loop cards
        for j, card in enumerate(pile):
            # Calculate Y offset. Face up cards spread out more than face down.
            $ card_y = start_y + (j * 25) 
            
            # If face down, just show the back
            if not card.is_face_up:
                add "mod_assets/games/solitaire/card_back.png":
                    pos (col_x, card_y)
                    xysize (80, 116)
            else:
                use render_card(card, col_x, card_y, Function(solitaire.select_card, card, "tableau", i))