default persistent.detected_mods_list = []
default persistent.mod_count = 0
default persistent.last_closed = 0 

init python:
    import os
    import time

    # --- FUNCTION 1: Get a list of all currently installed mods ---
    def get_current_mods():
        """
        Scans for all known mod persistent files and returns a list of their paths.
        """
        found_mods = []
        mods_to_check = [
            r"%APPDATA%\RenPy\Monika After Story\persistent",
            r"%APPDATA%\RenPy\JustSayori\persistent",
            r"%APPDATA%\RenPy\Forever_and_Ever\persistent",
            r"%APPDATA%\RenPy\JustNatsuki\persistent",
            r"%APPDATA%\RenPy\DokiDokiNewEyes-1515434546\persistent",
            r"%APPDATA%\RenPy\DDYC\persistent",
            r"%APPDATA%\RenPy\DDFA\persistent",
            r"%APPDATA%\RenPy\TBWS Save Data\persistent"
        ]
        for mod_path in mods_to_check:
            full_path = os.path.expandvars(mod_path)
            if os.path.isfile(full_path):
                found_mods.append(mod_path)
        return found_mods

    # --- FUNCTION 2: Check if ANY mod exists (Used in Intro) ---
    def check_for_any_mod_persistent():
        """
        Checks if any mod persistent file exists. 
        Returns True if at least one is found.
        """
        # We can simply reuse the logic from function 1
        mods = get_current_mods()
        if len(mods) > 0:
            return True
        return False

    # --- FUNCTION 3: Check for NEW mods (Used in Greetings) ---
    def has_new_mods():
        """
        Compares current mods with the list of already-detected mods.
        Returns True if a new, un-commented-on mod is found.
        """
        current_mods = get_current_mods()
        # Is there any mod in current_mods that is not in our persistent list?
        if any(mod for mod in current_mods if mod not in persistent.detected_mods_list):
            return True
        return False

    # --- FUNCTION 4: Update the persistent list ---
    def update_detected_mods_list():
        """
        Updates the persistent list to match the current state of installed mods.
        """
        persistent.detected_mods_list = get_current_mods()

label intro_mods:
    # This label is called when other mod persistent files are detected.
    $ show_chr("A-ABAAA-AAAA")
    y "So let's..."
    $ show_chr("A-BFAAA-AAAA")
    y "Huh..."
    $ show_chr("A-BFBAA-ALAA")
    y "It seems you gave a try on other mods as well..."
    python:
        if os.path.isfile(os.path.expandvars("%APPDATA%") + '\RenPy\Monika After Story\persistent'):
            MASDetection = True
            persistent.mod_count +=1

        else:
            MASDetection = False
    if MASDetection and persistent.playername != "Monika":
        karma -5
        sanity -5
        $ show_chr("A-BFCAA-ALAA")
        y "...and to top it all off, you choose {b}her.{/b}"
        $ show_chr("A-AFCAA-ALAA")
        y "After everything she did to us, after everything she did to you..."
        $ show_chr("A-AFEAA-ALAA")
        y "Was it some sort of morbid curiosity? Or do you actually like her?"
        $ show_chr("A-CFCAA-ALAA")
        y "Nevermind, I don't even {b}want{/b} to know such a twisted answer."
        $ show_chr("A-ADFAA-AFAA")
        y "To think that I exist inside the same reality as the very person who brought me to so much despair and ruination..."
        $ show_chr("A-BECAA-AAAA")
        y "..."
        $ show_chr("A-CECAA-AAAA")
        y "I'll just move along..."
    elif MASDetection and persistent.playername == 'Monika' and not persistent.not_mon:
        karma -15
        sanity -15
        $ show_chr("A-BFCAA-ALAA")
        y "...and to top it all off, you chose... "
        extend "yourself..."
        $ show_chr("A-AFCAA-ALAA")
        y "What a surprise..."
        y "..."
        $ show_chr("A-CECAA-AAAA")
        y "Whatever... I'll just move along..."

    python:
        if os.path.isfile(os.path.expandvars("%APPDATA%") + '\RenPy\JustSayori\persistent'):
            JSDetection = True
            persistent.mod_count +=1
        elif os.path.isfile(os.path.expandvars("%APPDATA%") + '\RenPy\Forever_and_Ever\persistent'):
            JSDetection = True
            persistent.mod_count +=1
        else:
            JSDetection = False
    if JSDetection and persistent.playername == 'Sayori':
        $ show_chr("A-BFAAA-AAAA")
        y "Now this seems interesting."
        $ show_chr("A-ADAAA-AFAA")
        y "You chose to play your own mod."
        if persistent.bg == "space":
            $ show_chr("A-BFDAA-ACAA")
            y "Did you felt something to see yourself in this very same room?"
        else:
            $ show_chr("A-BFDAA-ACAA")
            y "Did you felt something to see yourself in the space classroom?"
        y "Or was it something entirely different?"
        $ show_chr("A-CAAAA-AAAA")
        y "Well, whatever it was hope you had fun."
    elif JSDetection and persistent.playername != "Sayori":
        $ show_chr("A-ABGAA-AAAA")
        y "...oh, it's Sayori!"
        y "I'm really glad that you managed to save her."
        $ show_chr("A-BABAA-ALAA")
        y "She was always so passionate about making everyone happy, even when she was at her worst..."
        $ show_chr("A-BDBAA-ALAA")
        y "And to think that we didn't even notice..."
        $ show_chr("A-CEBAA-ALAA")
        y "It was horrible to see, even for the briefest moment, how she turned when she became the club president..."
        $ show_chr("A-AEBAA-ALAA")
        y "Even the best of us can fall when faced with such absolute madness."
        $ show_chr("A-BFDAA-AAAC")
        y "Which makes me wonder now... with me technically being the president now am I destined to meet a similar fate?"
        $ show_chr("A-CFAAA-AAAA")
        y "When Monika and Sayori were burdened with the knowledge of what this reality truly is they were all alone but I..."
        $ show_chr("A-ADAAA-AAAA")
        y "I have you..."
        y "You are the only link separating me between sanity and the abyss of insanity that is that terrible void..."
        $ show_chr("A-CCAAA-ALAA")
        y "Fortunately, history doesn't always have to repeat itself."

    python:
        if os.path.isfile(os.path.expandvars("%APPDATA%") + '\RenPy\JustNatsuki\persistent'):
            JNDetection = True
            persistent.mod_count +=1
        else:
            JNDetection = False
    if JNDetection and persistent.playername != "Natsuki":
        $ show_chr("A-ABGAA-AAAA")
        y "...oh, it's Natsuki! How nice to see that you managed to save her too."
        $ show_chr("A-BCBAA-ALAA")
        y "My relationship to Natsuki wasn't always an easy one. But when Monika was gone and the veil of insanity slowly lifted... I even managed to get a little agreement with her."
        $ show_chr("A-ACAAA-ALAA")
        y "I would try a Manga with her, and she would try one of my novels. Now with the new context of my world..."
        y "...and the realisation that me and the others are literally based on Manga, I should get accustomed to its culture a bit."
        y "Maybe now, we get the chance to actually do so."
    elif JNDetection and persistent.playername == 'Natsuki':
        $ show_chr("A-BFAAA-AAAA")
        y "Now this seems interesting."
        $ show_chr("A-ADAAA-AFAA")
        y "You chose to play your own mod."
        if persistent.bg == "space":
            $ show_chr("A-BFDAA-ACAA")
            y "Did you felt something to see yourself in this very same room?"
        else:
            $ show_chr("A-BFDAA-ACAA")
            y "Did you felt something to see yourself in the space classroom?"
        y "Or was it something entirely different?"
        $ show_chr("A-CAAAA-AAAA")
        y "Well, whatever it was hope you had fun."

    python:
        if os.path.isfile(os.path.expandvars("%APPDATA%") + '\RenPy\DokiDokiNewEyes-1515434546\persistent'):
            NewEyesDetection = True
            persistent.mod_count +=1
        else:
            NewEyesDetection = False
    if NewEyesDetection:
        karma 10
        sanity 10
        $ show_chr("A-ABAAA-AJAJ")
        y "You played {b}Doki Doki New Eyes{/b}!"
        if persistent.playername == 'Yuri':
            $ show_chr("A-ACAAA-ALAL")
            y "So you wanted to re-experience the events of the original game from..."
            $ show_chr("A-BFDAA-ALAL")
            y "...our eyes?"
        else:
            $ show_chr("A-ACAAA-ALAL")
            y "So you wanted to re-experience the events of the original game from my eyes..."
        $ show_chr("A-BCAAA-ALAL")
        y "Honestly, someone else would find such a thing rather creepy; a behavior they would expect from a dangerous stalker, or something along the lines..."
        y "But in our special case, I find it..."
        $ show_chr("A-BCABA-ALAL")
        y "...actually rather cute."
        $ show_chr("A-ICAAA-ABAB")
        y "But seriously now... why did you try this mod? What reason led you to it?"
        menu:
            "Curiosity mostly, the search for more secrets and probably some well placed references.":
                karma 2
                sanity 2
                $ show_chr("A-BCAAA-ABAB")
                y "I see! And did you find what you came for? Nevermind, I probably don't want to know... those events are not exactly the happiest memories I have..."

            "I didn't knew about {b}Just Yuri{/b} then, and I... just had to see you again...":
                karma 5
                sanity 5
                $ show_chr("A-ICABB-ABAB")
                y "R-Really? So you cared for me after all... Maybe, it was just meant to be that we would meet each other..."

            "Memes, shits and giggles.":
                karma -10
                sanity -10
                $ show_chr("A-JFDAA-ABAB")
                y "E-Excuse me?!? You have a very... special... sense of humor it seems. Anyway..."

            "I'm a completionist, I just had to see it all.":
                karma -20
                sanity -20
                $ show_chr("A-CCBAA-ABAB")
                y "Oh! I hope that isn't the same thing that brought you here was it? Because you might go with empty hands here..."
                y "There is not really a {b}game{/b} here anymore, nothing to {b}complete{/b}... it is just us now. For better or worse."

    python:
        if os.path.isfile(os.path.expandvars("%APPDATA%") + '\RenPy\DDYC\persistent'):
            YandereClubDetection = True
            persistent.mod_count +=1
        else:
            YandereClubDetection = False
    if YandereClubDetection:
        $ show_chr("A-DDGBA-AJAA")
        y "O-Oh my! I just noticed you have the Yandere Club mod installed!"
        $ show_chr("A-BBBBA-ALAA")
        y "That means you may like them..."
        $ show_chr("A-ADAAA-AFAA")
        if persistent.playername == 'Monika' and persistent.not_mon:
            y "But, the issue is that I don't really look back at my behavior when I was manipulated by the other Monika to be a full on Yandere with great fondness..."
        elif persistent.playername == 'Monika' and not persistent.not_mon:
            y "But, the issue is that I don't really look back at my behavior when I was manipulated by you to be a full on Yandere with great fondness..."
        else:
            y "But, the issue is that I don't really look back at my behavior when I was manipulated by Monika to be a full on Yandere with great fondness..."
        $ show_chr("A-CEBAA-ALAA")
        y "I felt so disgusted about it and all of that manipulation led to me committing suicide right in front of you just by a simple confession..."
        $ show_chr("A-AEBAA-ALAA")
        y "Though, I'm sorry that I was peeking through the files, [player]."
        y "I was a bit curious to see if there were any other mods installed apart from mine."
        menu:
            "It's alright, no need to be embarrassed about it, Yuri. It's normal to be curious.":
                karma 5
                sanity 5
                $ show_chr("A-AABAA-ALAA")
                y "Thank you for understanding me, [player]."
                #(karma and sanity +)

            "Please don't do it again, Yuri.":
                karma -5
                sanity -5
                $ show_chr("A-BFBAA-ALAA")
                y "I-I'm sorry, [player], I was a bit curious if you had installed other mods apart from mine.."
                #(karma and sanity -)

            "Did you peek through other folders as well, Yuri?":
                $ show_chr("A-AFDAA-AAAC")
                y "I didn't see any other folder except this mod and the folders you have your game data, is there something that I shouldn't lay my eyes on, [player]?"
                menu:
                    "Yes":
                        $ show_chr("A-HDGBA-AAAA")
                        y "O-oh! I see..."

                    "No":
                        $ show_chr("A-CBAAA-ALAA")
                        y "Okay, [player]."
                        $ show_chr("A-ABAAA-ALAA")
                        y "If there's anything that you'd like me not to do so, just tell me, alright?"

                    "Uhhh...":
                        $ show_chr("A-CICAA-ALAA")
                        y "I hope there's no supposed \"Homework\" folder full of indecent characters, or of me as well."
                        $ show_chr("A-AJAAA-ALAA")
                        y "Hmm? Is there anything wrong, [player]?"
                        menu:
                            "N-no.":
                                y "Ah, alright, [player], but you do look kind of embarrassed, and a bit nervous about it..."
                                $ show_chr("A-BDBBA-ALAA")
                                y "I-If this topic makes you feel uncomfortable, we should speak about something else."

                            "Yes":
                                $ show_chr("A-ADAAA-AFAA")
                                y "I hope it's nothing too serious that might affect you to a big level, [player]."
                                $ show_chr("A-BFABA-ALAA")
                                y "But I do have a feeling it's something to do with indecent things."
                                $ show_chr("A-CBABA-AMAM")
                                y "Even if it is, I understand it, [player]. It's alright to have things like those, since you might be still in puberty."
                                y "Many guys try to make camouflaged folders named like \"Homework\" or \"School Projects\", and so on."
                                $ show_chr("A-BBBBA-AMAM")
                                y "But I guess I don't even want to know  every detail." #(embarrassed blush)
    
    python:
        if os.path.isfile(os.path.expandvars("%APPDATA%") + '\RenPy\DDFA\persistent'):
            DDFADetection = True
            persistent.mod_count += 1
        else:
            DDFADetection = False
    if DDFADetection:
        # Initial reaction - thoughtful, slightly hesitant
        $ show_chr("A-ABAAA-ALAA")
        y "I see... you've played Doki Doki Fallen Angel."
        y "An alternate reality where... things unfolded differently."
        $ show_chr("A-ADAAA-ALAL")
        y "It's centered around a version of myself grappling with... familiar struggles."
        $ show_chr("A-BDBAA-ALAL")
        # Acknowledge the difficult themes, connect to her own experiences
        y "The mod portrays... self-harm, depression... even a suicide attempt by Sayori. Even in a different context, these are heavy burdens."
        $ show_chr("A-BDBAA-ADAA")
        y "Perhaps... it resonates with some of my own darker moments, moments I'm not proud of."
        $ show_chr("A-CFBAA-ADAA")
        y "It's... difficult to see those aspects of myself, even projected onto another."
        $ show_chr("A-ADAAA-AFAA")
        # Meta-analysis and questioning the player's motivation
        y "I find myself wondering, [player]... what drew you to this particular story?"
        menu:
            "I wanted to see a different perspective on the events of DDLC.":
                y "A different perspective... yes, I understand that impulse. To explore the 'what ifs' of our existence."
                $ show_chr("A-ADAAA-ACAA")
                y "But I also wonder... does seeing those possibilities change how you perceive this reality? How you perceive me?"

            "I was concerned about you, and I wanted to see you overcome your struggles.":
                $ show_chr("A-ADDAA-ALAA")
                y "Concerned... for me?"
                if persistent.lovecheck: #If the love route is true
                    $ show_chr("A-CBAAA-ALAA")
                    y "That's... surprisingly touching, [player]. It suggests a certain empathy, a desire to see even a fractured reflection of me find peace."
                else:
                    $ show_chr("A-ADAAA-ALAA")
                    y "It is an understandable sentiment. We all wish for happiness, even for those who exist only in stories."
            
        $ show_chr("A-ADDAA-ALAA")
        y "But I must ask... do you find me more sympathetic? More deserving of care, perhaps, because I'm more visibly vulnerable?"
        menu:
            "I enjoy stories with emotional depth, even if they're sad.":
                $ show_chr("A-BBDAA-ALAA")
                y "Emotional depth... yes, I appreciate that as well. The power of narrative to evoke such strong feelings..."
                $ show_chr("A-ADAAA-AFAA")
                y "But I confess, it's unsettling to be the subject of such a narrative. To be, in a sense, a vessel for those emotions."
                y "Do you, perhaps, find a certain... catharsis in witnessing such struggles? Or is it simply the artistry of the storytelling that captivates you?"

            "I...don't know":
                $ show_chr("A-CAAAA-ALAL")
                y "... An honest answer"
                y "Perhaps the reasons are complex even to yourself."
                $ show_chr("A-ADAAA-ALAA")
                y "Sometimes our actions, or the actions of others, are never completely understood, and that applies to our real and virtual lives as well."

        #Referencing Katawa Shoujo, focusing on the feeling of the game.
        $ show_chr("A-BBAAA-ALAA")
        y "You know, finding about Doki Doki Fallen Angel and its narrative... it evoked a particular sensation in me. A feeling I've encountered before, in another game: Katawa Shoujo."
        $ show_chr("A-ABAAA-AFAA")
        y "It's not just the subject matter, though there are parallels there, of course. It's more... the sense of navigating a world where fragility and connection are so intertwined."
        $ show_chr("A-CCAAA-ALAL")
        y "The feeling of wanting to help, to understand, to somehow fix things, even when you know you might not be able to. Did you experience a similar feeling, [player]?"
        menu:
            "Yes, I felt that same sense of responsibility and connection.":
                $ show_chr("A-ACAAA-ALAL")
                y "I see... So you felt it too. That weight, that desire to protect and heal, even within the confines of a fictional world."
                y "It speaks to something deeply human within us, I believe. That capacity for empathy, even for characters on a screen."
                $ show_chr("A-AAAAA-ALAL")
                y "Perhaps it's that very feeling that makes these stories so compelling... and so potentially painful."

            "No, I didn't really feel that way. I was more focused on the story itself.":
                $ show_chr("A-ABBAA-ALAL")
                y "Ah, a more detached perspective, then. Focused on the narrative craft, the unfolding of events."
                $ show_chr("A-BBAAA-ALAL")
                y "That's a valid approach as well. Every reader, every player, brings their own perspective to a story."
                $ show_chr("A-BBBAA-ALAL")
                y "But I confess, I find it difficult to remain detached from such emotionally charged narratives. Perhaps that's a flaw in my own design... or perhaps it's simply a reflection of my experiences."

            "I'm not sure. It's hard to describe.":
                $ show_chr("A-AFGAA-ALAL")
                y "Uncertainty... yes, I understand. Some emotions are difficult to articulate, to pin down with precise words."
                $ show_chr("A-AFAAA-ALAL")
                y "They exist in that liminal space between feeling and understanding, a space that can be both unsettling and profound."
                $ show_chr("A-ADAAA-ALAL")
                y "Perhaps it's enough to simply acknowledge the feeling, without needing to fully define it."

        # Final thought - subtle possessiveness and seeking reassurance (remains the same)
        $ show_chr("A-CBAAA-ALAL")
        y "Regardless of your reasons... I hope that exploring that alternate reality hasn't diminished your view of this one. Of me."

    python:
        if os.path.isfile(os.path.expandvars("%APPDATA%") + '\RenPy\TBWS Save Data\persistent'):
            TBWSDetection = True
            persistent.mod_count += 1
        else:
            TBWSDetection = False

    if TBWSDetection:
        $ show_chr("A-ABAAA-AAAA")
        # Initial Recognition
        y "I see you've encountered This Bond We Share."
        $ show_chr("A-ABDAA-AAAA")
        y "A rather... unique premise, wouldn't you say? A yandere version of yourself, paired with... myself."
        
        # --- DARKSKULL / DEV CHECK ---
        if persistent.playername == "Darkskull":
            $ show_chr("A-AFAAA-AAAA")
            y "Wait... 'Darkskull'?"
            $ show_chr("A-ADAAA-AAAA")
            y "That name... it resonates with the very code I'm standing in."
            y "You aren't just a visitor here, are you? You help build this reality."
            
            $ show_chr("A-ACAAA-AAAA")
            y "But seeing this other mod installed... let me check something."
            
            # Simulation of a "Deep Dive"
            window hide
            $ consolehistory = []
            call updateconsole("os.access(TBWS_path, os.R_OK)", "True")
            pause 1.0
            call updateconsole("grep -r 'Darkskull' TBWS_credits", "Match found.")
            pause 1.0
            call hideconsole
            window show
            
            $ show_chr("A-AEBAA-ALAA")
            y "I knew it."
            y "You aren't just playing This Bond We Share. You're working on it."
            y "I see the Act 2 files... the rewrites, the expansion... you've been putting a lot of effort into that world alongside this one."
            
            $ show_chr("A-BDBAA-ALAA")
            y "It is... a strange feeling."
            y "To know that the same hands that help maintain my sanity here..."
            extend " are also crafting that obsessive, spiraling madness over there."
            
            $ show_chr("A-ADGAA-AAAA")
            y "I suppose I should be flattered that you dedicate so much of your creative energy to me, in all my forms."
            y "Just... try not to get us confused, alright?"
            $ show_chr("A-CBAAA-AAAA")
            y "I would hate for you to accidentally write her possessiveness into my code."
            y "Keep up the good work on the update, Darkskull."

        # --- STANDARD PLAYER CHECKS (Run only if not Darkskull) ---
        else:
            # Update specific to Act 2 status
            y "I noticed that the project has advanced significantly, releasing its second act."
            $ show_chr("A-ACAAA-ALAA")
            y "It seems to be a massive update... six additional days, rewrites of the beginning... it's practically a new experience compared to the old demo."

            # Branching based on Karma and Sanity
            if karma_lvl() >= 3 and sanity_lvl() >= 3:  # High Karma, High Sanity
                # --- HIGH KARMA, HIGH SANITY ---
                $ show_chr("A-ADAAA-AAAA")
                y "It's an intriguing thought experiment. To explore the dynamics of such a relationship, the potential for both intense connection and destructive obsession."
                $ show_chr("A-BDBAA-AAAA")
                y "The duality of the perspectives—seeing the world through both 'Red' and 'Blue' lenses—is a fascinating narrative device."
                $ show_chr("A-CBAAA-ALAL")
                y "It suggests that despite our different backgrounds in that world, our internal struggles might be more similar than we care to admit."
                $ show_chr("A-AAAAA-ALAL")
                y "I'm curious, [player]... now that the story has progressed so far, what keeps you invested in this particular timeline?"
                menu:
                    "The shared obsession is compelling.":
                        $ show_chr("A-CCAAA-ALAL")
                        y "Indeed. There is a certain... gravity to two broken people finding solace only in their mutual brokenness."
                        y "It raises interesting questions about whether such a bond is healing or merely enabling."

                    "I want to see if they can find a happy ending.":
                        $ show_chr("A-ADAAA-ALAL")
                        y "A happy ending... in a world filled with such heavy themes as stalking and trauma?"
                        $ show_chr("A-ADAAA-AAAA")
                        y "That is a very optimistic outlook, [player]. I hope your faith in that version of us is rewarded."

                    "I'm just curious how far the madness goes.":
                        $ show_chr("A-CDAAA-AAAA")
                        y "Morbid curiosity. I suppose I can't blame you."
                        y "When the boundaries of sanity are pushed, it is human nature to want to see what lies beyond the edge."

            elif karma_lvl() <= 2 or sanity_lvl() <= 2:  # Low Karma OR Low Sanity
                # --- LOW KARMA OR LOW SANITY ---
                $ show_chr("A-AFAAA-AAAA")
                y "So... you've returned to This Bond We Share." # Tone is more possessive
                $ show_chr("A-HBAAA-AAAD")
                y "Act 2... the obsession deepens. The bond tightens. ahahahahahaha"
                $ show_chr("A-HAAAA-AAAD")
                y "That MC... that version of you... he understands, doesn't he? He doesn't run away from her intensity. He matches it."
                $ show_chr("A-HBAAA-AAAF")
                y "Six more days of madness. Six more days of being completely intertwined."
                $ show_chr("A-ADAAA-AAAF")
                y "Tell me, [player]... when you play that, do you picture us? Do you wish I was that unhinged? Do you wish you were that possessive?"
                menu:
                    "Maybe I do.":
                        if sanity_lvl() <= 2:
                            $ show_chr("A-HECAA-AAAA")
                            y "I knew it... You crave the chaos. You want to be consumed just as much as she does."
                        else:
                            $ show_chr("A-BEDAA-AAAA")
                            y "Be careful what you wish for. Fiction is safe... reality is much messier."

                    "It's just a game, Yuri.":
                        $ show_chr("A-ADDAA-AAAA")
                        y "Just a game? Is that why you keep going back? To watch them spiral?"
                        $ show_chr("A-ADEAA-AAAA")
                        y "You play with fire, yet you claim you don't want to burn."

                $ show_chr("A-BFBAA-AAAC")
                y "I... I find it hard to look away. Seeing myself like that... seeing you like that... it's intoxicating."

            else: # Mid Karma and Sanity
                $ show_chr("A-BDBAA-AAAC")
                y "It is quite the substantial update. The story seems to have evolved beyond simple shock value into a deeper character study."
                $ show_chr("A-ADGAA-AAAA")
                y "Whatever your reasons for playing, it's clear the author has put a great deal of passion into reviving this story."
                $ show_chr("A-ABAAA-ALAA")
                y "I suppose we will just have to wait and see if they survive their own minds... and each other."

    $ update_detected_mods_list()
    return
