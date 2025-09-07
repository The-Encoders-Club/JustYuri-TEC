python early:
    import os

    def save_our_poem(player_name, poem_lines):
        """Saves a list of strings to a file on the desktop."""
        home_directory = os.path.expanduser('~')
        desktop_path = os.path.join(home_directory, 'Desktop')
        
        # Create a unique filename
        filename = "Poem_by_Yuri_and_{}.txt".format(player_name)
        file_path = os.path.join(desktop_path, filename)

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("A Poem by Yuri and {}\n".format(player_name))
                f.write("="*30 + "\n\n")
                # Write each line to the file
                for line in poem_lines:
                    f.write(line + "\n")
            return True # Success
        except:
            return False # Failed

label collaborative_poetry:
    $ poem_lines = [] # Create an empty list to hold the lines

    y "I feel... creative today."
    y "Would you like to write a poem with me? We can take turns, line by line."

    menu:
        "I'd love to!":
            y "Wonderful. I'll start."
            
            # Yuri's first line
            $ yuri_line = "The ink spills across the silent page."
            y "[yuri_line]"
            $ poem_lines.append(yuri_line)
            
            # Get player's first line
            $ player_line = renpy.input("What's the next line?", length=100).strip()
            $ poem_lines.append(player_line)
            
            # Yuri's second line
            $ yuri_line = "A world of shadow, born of love and rage."
            y "[yuri_line]"
            $ poem_lines.append(yuri_line)
            
            # Get player's second line
            $ player_line = renpy.input("And the final line?", length=100).strip()
            $ poem_lines.append(player_line)

            y "It's... perfect. Thank you for creating this with me."
            y "I'd like to save this, so we never forget it. I'll put a text file on your desktop."

            # Call the save function
            $ success = save_our_poem(player, poem_lines)

            if success:
                y "There. It should be on your desktop now."
            else:
                y "Oh... for some reason, I couldn't save it. I'm so sorry."

        "I'm not in the mood right now.":
            y "Of course. Inspiration is a fickle thing. Perhaps another time."

    return
