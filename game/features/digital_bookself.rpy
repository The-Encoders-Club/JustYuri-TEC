python early:
    import os
    # We need renpy.config.basedir, which is available in an init block.
    # We'll define the full path inside the functions themselves.

    def find_books_in_game_folder():
        """
        Scans for .txt files in a 'books' folder located in the game's root directory.
        """
        # config.basedir is the absolute path to the folder containing DDLC.exe
        book_folder_path = os.path.join(config.basedir, 'books')
        
        found_books = []
        
        # If the 'books' folder doesn't exist, create it for the user and return empty.
        if not os.path.exists(book_folder_path):
            try:
                os.makedirs(book_folder_path)
                return [] # Return an empty list as it was just created.
            except:
                return [] # Failed to create folder for some reason.

        # Scan the folder if it exists.
        for filename in os.listdir(book_folder_path):
            if filename.lower().endswith('.txt'):
                found_books.append(filename)
                    
        return found_books

    def read_book_from_game_folder(filename):
        """
        Reads the content of a specific .txt file from the 'books' folder.
        """
        book_folder_path = os.path.join(config.basedir, 'books')
        file_path = os.path.join(book_folder_path, filename)

        try:
            # Try to open and read the file with utf-8 encoding.
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            # If it fails, return an error message.
            return "I'm sorry, I had trouble reading that file. It might be corrupted or in a format I don't understand."

# First, define a persistent variable to hold the bookshelf so we don't scan every time.
default persistent.bookshelf = None

label yuri_scan_for_books:
    # New dialogue explaining the 'books' folder.
    y "You know, I was thinking it would be lovely to share some reading material."
    y "I've set up a special folder named 'books' right here in the mod's main directory."
    y "If you place any '.txt' files in there, I can find them and we can read them together."
    y "Would you like me to check that folder now?"

    menu:
        "Yes, check the 'books' folder.":
            # Call our updated Python function.
            $ persistent.bookshelf = find_books_in_game_folder()

            if persistent.bookshelf:
                y "Wonderful! Let me see..."
                y "It looks like you've placed [len(persistent.bookshelf)] books here for us."
                y "Which one should we look at?"

                python:
                    book_menu_options = []
                    for book_filename in persistent.bookshelf:
                        book_menu_options.append( (book_filename, book_filename) )
                    
                    book_menu_options.append( ("Let's not read right now.", "cancel") )
                    book_choice = renpy.display_menu(book_menu_options)

                if book_choice != "cancel":
                    # Call our other updated function.
                    $ book_content = read_book_from_game_folder(book_choice)
                    y "Alright, let's read '[book_choice]' together."
                    
                    show text "[book_content[:500]]..." with dissolve
                    y "That was a fascinating read. Thank you for sharing it with me."
                    hide text with dissolve
                    "..."
                else:
                    y "Alright. We can look at them another time."

            else:
                y "Oh... It doesn't look like there are any text files in the 'books' folder yet."
                y "That's perfectly fine. Feel free to add some whenever you like."

        "No, not right now.":
            y "Of course. Let me know when you'd like me to check."

    return
