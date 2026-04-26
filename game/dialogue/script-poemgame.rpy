init python:
    import random
    import codecs

    class PoemWord:
        def __init__(self, word, good_point, sad_point, insane_point, sane_point, glitch=False):
            self.word = word
            self.good_point = good_point
            self.sad_point = sad_point
            self.insane_point = insane_point
            self.sane_point = sane_point
            self.glitch = glitch

    full_wordlist =[]
    
    # Try to read the file safely from the game folder
    try:
        with renpy.file('poemwords_different.txt') as wordfile:
            for line in wordfile:
                line = line.decode('utf-8').strip()
                if not line or line.startswith('#'): continue

                x = line.split(',')
                if len(x) == 5:
                    full_wordlist.append(PoemWord(x[0], float(x[1]), float(x[2]), float(x[3]), float(x[4])))
    except Exception:
        # Fallback to absolute path just in case your game specifically relies on the root directory
        try:
            with codecs.open('/poemwords_different.txt', 'r', 'utf-8') as wordfile:
                for line in wordfile:
                    line = line.strip()
                    if not line or line.startswith('#'): continue

                    x = line.split(',')
                    if len(x) == 5:
                        full_wordlist.append(PoemWord(x[0], float(x[1]), float(x[2]), float(x[3]), float(x[4])))
        except Exception:
            pass

    # CRITICAL FAILSAFE: If the file was missing or empty, add a dummy word so the game never crashes.
    if not full_wordlist:
        full_wordlist.append(PoemWord("Error_NoWords", 1.0, 1.0, 1.0, 1.0))

    # Yuri sticker variables
    seen_eyes_this_chapter = False
    yuriTime = renpy.random.random() * 4 + 4
    yuriPos = 0
    yuriOffset = 0
    yuriZoom = 1

    def randomPauseYuri(trans, st, at):
        global yuriTime
        if st > yuriTime:
            yuriTime = renpy.random.random() * 4 + 4
            return None
        return 0

    def randomMoveYuri(trans, st, at):
        global yuriPos, yuriOffset, yuriZoom
        
        if st > .16:
            if yuriPos > 0:
                yuriPos = renpy.random.randint(-1, 0)
            elif yuriPos < 0:
                yuriPos = renpy.random.randint(0, 1)
            else:
                yuriPos = renpy.random.randint(-1, 1)
                
            if trans.xoffset * yuriPos > 5: 
                yuriPos *= -1
            return None
            
        if yuriPos > 0:
            trans.xzoom = -1
        elif yuriPos < 0:
            trans.xzoom = 1
            
        trans.xoffset += .16 * 10 * yuriPos
        yuriOffset = trans.xoffset
        yuriZoom = trans.xzoom
        return 0

# Modern Ren'Py screen to handle the minigame UI
screen poem_minigame(pstring, num_words, current_words):
    text "[pstring]/[num_words]" style "poemgame_text" xpos 810 ypos 80 color '#000'

    # Left Column
    vbox:
        xpos 440 ypos 160 spacing 12 
        for word in current_words[:5]:
            textbutton word.word action Return(word) text_style "poemgame_text"

    # Right Column
    vbox:
        xpos 680 ypos 160 spacing 12
        for word in current_words[5:]:
            textbutton word.word action Return(word) text_style "poemgame_text"


label poem(transition=True):
    if current_timecycle_marker in["_day", "_night", "_sunrise", "_sunset"]:
        show expression "bg notebook" + current_timecycle_marker zorder 30
    else:
        show bg notebook zorder 30

    show screen quick_menu
    show y_sticker at sticker_middle zorder 40
    
    if transition:
        with dissolve_scene_full
        
    $ config.skipping = False
    $ config.allow_skipping = False
    $ allow_skipping = False

    python:
        poemgame_glitch = False
        played_baa = False
        progress = 1
        numWords = 35 
        
        scores = {
            "goodpoemresponse": 0.0,
            "sadpoemresponse": 0.0,
            "insanepoemresponse": 0.0,
            "sanepoemresponse": 0.0
        }

        wordlist = list(full_wordlist)
        yuriTime = renpy.random.random() * 4 + 4
        yuriPos = renpy.random.randint(-1, 1)
        yuriOffset = 0
        yuriZoom = 1

        while progress <= numWords:
            if persistent.playthrough == 2 and chapter == 2:
                pstring = "1" * progress
            else:
                pstring = str(progress)

            # CRITICAL FAILSAFE: If we run below 10 words, replenish the list
            while len(wordlist) < 10:
                wordlist.extend(full_wordlist)

            # Generate 10 random choices for the screen
            current_words = random.sample(wordlist, 10)
            for w in current_words:
                wordlist.remove(w)

            # Call the custom screen and wait for the user to click a word
            chosen_word = renpy.call_screen("poem_minigame", pstring=pstring, num_words=numWords, current_words=current_words)

            # Add points
            scores["goodpoemresponse"] += chosen_word.good_point
            scores["sadpoemresponse"] += chosen_word.sad_point
            scores["insanepoemresponse"] += chosen_word.insane_point
            scores["sanepoemresponse"] += chosen_word.sane_point
            
            progress += 1

        # Determine winner
        winning_label = max(scores, key=scores.get)

    jump expression winning_label


# --- Images and Transforms ---

image y_sticker:
    "images/poem_game/stickers/sticker_uniform_1.png" 
    xoffset yuriOffset xzoom yuriZoom
    block:
        function randomPauseYuri
        parallel:
            function randomMoveYuri
        repeat

image y_sticker hop:
    "images/poem_game/stickers/sticker_uniform_2.png"
    xoffset yuriOffset xzoom yuriZoom
    sticker_hop
    xoffset 0 xzoom 1
    "y_sticker"

transform sticker_middle:
    xcenter 210 yalign 0.9 subpixel True

transform sticker_hop:
    easein_quad .18 yoffset -80
    easeout_quad .18 yoffset 0
    easein_quad .18 yoffset -80
    easeout_quad .18 yoffset 0
