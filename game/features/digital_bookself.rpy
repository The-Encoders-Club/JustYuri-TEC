# This is the complete Digital Bookshelf feature, with support for
# TXT, PDF, and DOCX files, and integration with the poem screen.

python early:
    import os
    import datetime

    # These libraries must be in your game/python-packages folder!
    try:
        from docx import Document
        docx_available = True
    except ImportError:
        docx_available = False

    try:
        from PyPDF2 import PdfReader
        pypdf2_available = True
    except ImportError:
        pypdf2_available = False

    def find_books_in_poems_folder():
        """
        Scans for .txt, .pdf, and .docx files in a 'poems' folder in the game's root directory.
        """
        poems_folder_path = os.path.join(config.basedir, 'poems')
        found_books = []
        if not os.path.exists(poems_folder_path):
            try: os.makedirs(poems_folder_path)
            except: return []
        
        for filename in os.listdir(poems_folder_path):
            if filename.lower().endswith(('.txt', '.pdf', '.docx')):
                found_books.append(filename)
        return found_books

    def get_book_metadata(filename):
        """

        Analyzes a file and returns its metadata as a dictionary.
        {'type': 'txt', 'content': '...', 'page_count': None}
        {'type': 'pdf', 'content': '...', 'page_count': 150}
        """
        poems_folder_path = os.path.join(config.basedir, 'poems')
        file_path = os.path.join(poems_folder_path, filename)
        
        # Handle TXT files
        if filename.lower().endswith('.txt'):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                return {'type': 'txt', 'content': content, 'page_count': None}
            except:
                return None

        # Handle DOCX files
        elif filename.lower().endswith('.docx') and docx_available:
            try:
                doc = Document(file_path)
                page_count = len(doc.element.xpath('//w:lastRenderedPageBreak')) + 1
                first_paragraph = doc.paragraphs[0].text if doc.paragraphs else ""
                return {'type': 'docx', 'content': first_paragraph, 'page_count': page_count}
            except:
                return None

        # Handle PDF files
        elif filename.lower().endswith('.pdf') and pypdf2_available:
            try:
                with open(file_path, 'rb') as f:
                    reader = PdfReader(f)
                    page_count = len(reader.pages)
                    first_page_text = reader.pages[0].extract_text() if page_count > 0 else ""
                return {'type': 'pdf', 'content': first_page_text, 'page_count': page_count}
            except:
                return None
        
        return None # File type not supported or library missing

    def format_text_for_poem_screen(raw_text, max_chars=100000, line_length=60):
        """
        Takes a long string and formats it beautifully for the poem screen.
        """
        snippet = raw_text[:max_chars]
        words = snippet.split()
        formatted_lines = []
        current_line = ""
        for word in words:
            if len(current_line) + len(word) + 1 <= line_length:
                current_line += " " + word
            else:
                formatted_lines.append(current_line.strip())
                current_line = word
        formatted_lines.append(current_line.strip())
        return "\n".join(formatted_lines)


# This is the introductory idle topic.
label yuri_bookshelf_intro:
    y "You know, I was thinking it would be lovely to share some reading material."
    y "I've set up a special 'poems' folder in the mod's main directory. It's the perfect place for us to build a little library."
    y "If you place any '.txt', '.pdf', or '.docx' files in there, I can analyze them and we can discuss them."
    y "For '.txt' files, we can even read a portion together, right here on the screen."
    y "To keep things manageable for a single reading session, I'll load the first 100,000 characters. That's enough for a novella, really!"
    y "Just let me know whenever you'd like me to check the folder."
    return

# This is the main label, callable from the "Talk" menu.
label yuri_scan_for_books:
    $ bookshelf = find_books_in_poems_folder()

    if bookshelf:
        y "Let me see what's in our shared 'poems' folder..."
        y "It looks like you've placed [len(bookshelf)] items here for us."
        y "Which one should we look at?"

        python:
            book_menu_options = [ (book_filename, book_filename) for book_filename in bookshelf ]
            book_menu_options.append( ("Let's not read right now.", "cancel") )
            book_choice = renpy.display_menu(book_menu_options)

        if book_choice != "cancel":
            $ metadata = get_book_metadata(book_choice)
            
            if metadata:
                # --- LOGIC FOR TXT FILES ---
                if metadata['type'] == 'txt':
                    $ formatted_poem_text = format_text_for_poem_screen(metadata['content'])
                    $ temp_poem = Poem(author="yuri", title=book_choice.replace(".txt", ""), text=formatted_poem_text)
                    y "Ah, a text file. Simple and elegant. Let's read a bit together."
                    call showpoem(poem=temp_poem)
                    y "That was a fascinating read. The style is so distinct. Thank you for sharing it with me."
                
                # --- LOGIC FOR DOCX/PDF FILES ---
                else:
                    $ page_count = metadata['page_count']
                    $ first_paragraph = metadata['content'][:300] # Snippet of the first paragraph/page
                    y "Oh, this is a [metadata['type']] file. That's a much more complex format."
                    y "I can't display the contents directly here—the formatting is too intricate, and there might be images I can't process."
                    if page_count > 0:
                        y "However, I can see some of its properties... It appears to be [page_count] pages long. That's quite a substantial work!"
                    if first_paragraph:
                        y "The opening seems to be..."
                        y "\"[first_paragraph]...\""
                        y "Based on that, it sounds fascinating. You have excellent taste."
                    else:
                        y "I'm having a bit of trouble extracting a preview, but I can tell it's a complex document. I'm sure it's an interesting read."

            else:
                y "I'm sorry, I had trouble analyzing that file. It might be corrupted, or it's a type I don't fully support yet."
        else:
            y "Alright. We can look at them another time."

    else:
        y "Oh... It doesn't look like there are any files in the 'poems' folder yet."
        y "That's perfectly fine. Feel free to add some whenever you like."

    return
