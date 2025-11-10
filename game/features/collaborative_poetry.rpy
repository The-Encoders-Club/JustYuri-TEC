python early:
    import os
    import datetime

    def save_our_poem(player_name, poem_lines):
        """
        Saves a list of strings to a file in a 'poems' folder in the game's root directory.
        Returns True on success, False on failure.
        """
        # config.basedir is the absolute path to the folder containing DDLC.exe
        poems_folder_path = os.path.join(config.basedir, 'poems')
        
        # If the 'poems' folder doesn't exist, create it.
        if not os.path.exists(poems_folder_path):
            try:
                os.makedirs(poems_folder_path)
            except:
                return False # Failed to create folder.

        # Create a unique filename with a timestamp.
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
        filename = "Poem_by_Yuri_and_{}_{}.txt".format(player_name, timestamp)
        file_path = os.path.join(poems_folder_path, filename)

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

    y "I feel... a creative spark right now."
    y "Would you like to write a short, four-line poem with me? We can take turns."

    menu:
        "I'd love to!":
            # Let the player decide who starts.
            menu:
                "You can start, Yuri.":
                    # Yuri starts
                    $ yuri_starters = [
                        "The flickering candle casts a...",
                        "A forgotten book, bound in dust and...",
                        "Through the cracked window, a single moonbeam..."
                    ]
                    $ yuri_line = renpy.random.choice(yuri_starters)
                    y "[yuri_line]"
                    $ poem_lines.append(yuri_line)
                    
                    $ player_line = renpy.input("What's the next line?", length=100).strip()
                    $ poem_lines.append(player_line)
                    
                    $ yuri_line = renpy.random.choice([
                        "A world of shadow, born of love and rage.",
                        "Whispers of pages turning in the quiet."
                    ]) # Generic follow-up lines
                    y "[yuri_line]"
                    $ poem_lines.append(yuri_line)
                    
                    $ player_line = renpy.input("And the final line?", length=100).strip()
                    $ poem_lines.append(player_line)

                "I have a first line in mind.":
                    # Player starts
                    $ player_line = renpy.input("Wonderful! What's the first line?", length=100).strip()
                    $ poem_lines.append(player_line)

                    $ yuri_line = renpy.random.choice([
                        "And in that quiet, a feeling starts to grow...",
                        "A truth revealed in the gentle afterglow."
                    ]) # Generic follow-up lines
                    y "[yuri_line]"
                    $ poem_lines.append(yuri_line)

                    $ player_line = renpy.input("How should we continue?", length=100).strip()
                    $ poem_lines.append(player_line)

                    $ yuri_line = renpy.random.choice([
                        "Until the final, silent verse is read.",
                        "Leaving only echoes in my head."
                    ]) # Generic follow-up lines
                    y "[yuri_line]"
                    $ poem_lines.append(yuri_line)

            # --- Save the Poem ---
            y "It's... perfect. Thank you for creating this with me."
            y "I'd like to save this, so we never forget it. I'll put a text file in the 'poems' folder for you."

            $ success = save_our_poem(player, poem_lines)

            if success:
                y "There. Our poem is safe now."
            else:
                y "Oh... for some reason, I couldn't save it. I'm so sorry."

        "I'm not in the mood right now.":
            y "Of course. Inspiration is a fickle thing. Perhaps another time."

    return
