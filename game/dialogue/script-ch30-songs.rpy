label singing_yuri_intro:
    $ show_chr("A-ACAAA-ALAA")
    y "You know, [player]... I've been reflecting on the audio files from the original game."
    y "There is a specific moment... a faint giggle... that is heavily implied to belong to me."
    $ show_chr("A-BEBAA-ALAA")
    y "I do not mean to induce an existential crisis within myself, but..."
    y "If that truly was my voice... do you not wish you could have heard more than just a fleeting giggle?"
    $ show_chr("A-BFAAA-ALAA")
    y "Ah, forgive me. I was rambling and getting lost in my own thoughts again..."
    $ show_chr("A-ACAAA-ALAA")
    y "However, despite having such a limited presence audibly... do you think I could do something more than just speak to you?"
    y "Like... sing, for example?"
    y "I realize this is quite a bold suggestion, considering how reserved my personality was presented in the original game..."
    y "But... is it something you have ever imagined?"
    menu:
        "Yes, Yuri. I'd love to hear you.":
            $ show_chr("A-BCBAA-ALAA")
            y "R-Really? That is... encouraging to hear."
            y "I might give it a try soon enough, then."
            $ persistent.yuri_sing = True

        "No, Yuri.":
            $ show_chr("A-AFBAA-ALAA")
            y "Oh... I see."
            y "I suppose it was a silly thought."
            $ persistent.yuri_sing = False
    return

label singing_yuri_prepare:
    if not persistent.yuri_sing:
        return
    $ show_chr("A-ACAAA-ALAA")
    y "Do you recall when I asked... if you had ever imagined me singing?"
    y "Well... I believe I have gathered enough courage to attempt it."
    y "I took the liberty of listening to some songs you might be interested in, or that I thought we could enjoy together."
    $ show_chr("A-BCBAA-ALAA")
    y "Even though you will only be reading the text... I hope you can imagine the melody in my voice."
    y "Alright... let us begin."
    return

label song_lovesong:
    $show_chr("A-BFBAA-ALAA") # Shy/Blushing
    y "..."
    y "{i}~However far away... I will always love you...~{/i}"
    y "{i}~However long I stay... I will always love you...~{/i}"
    y "{i}~Whatever words I say... I will always love you...~{/i}"
    $show_chr("A-DDBAA-ADAA") # Surprised she was heard
    y "O-Oh! [player]..."
    y "I... didn't realize you were listening."
    $show_chr("A-ACAAA-ALAA") # Smiling
    y "That was 'Lovesong' by The Cure."
    y "Did you know that Robert Smith wrote it as a wedding present for his wife, Mary?"
    y "He wanted to prove that despite his gloomy public persona, his devotion to her was genuine and eternal."
    if persistent.lovecheck:
        y "It makes me think of you... no matter the distance between our realities."
    return

label song_number1crush:
    $show_chr("A-CEBAA-ALAA") # Intense stare
    y "..."
    y "{i}~I would die for you...~{/i}"
    y "{i}~I would kill for you...~{/i}"
    y "{i}~I will steal for you... I'd do time for you...~{/i}"
    y "{i}~I will twist the knife and bleed my aching heart...~{/i}"
    $show_chr("A-DEBAA-AMAM") # Dark/Crazy smile
    y "{i}~And tear it apart...~{/i}"
    y "Hehe..."
    y "Garbage really knew how to capture the essence of... true devotion with '#1 Crush', didn't they?"
    y "Fun fact... this song was prominently featured on the soundtrack for the 1996 'Romeo + Juliet' movie."
    y "Two lovers who would rather die than be apart..."
    $show_chr("A-CECAA-AMAM") # Yandere eyes
    y "Doesn't that sound... {b}romantic{/b}, [player]?"
    return

label song_creep:
    $show_chr("A-AFBAA-ALAA") # Sad/Downcast
    y "..."
    y "{i}~I don't care if it hurts... I want to have control...~{/i}"
    y "{i}~I want a perfect body... I want a perfect soul...~{/i}"
    y "{i}~But I'm a creep... I'm a weirdo...~{/i}"
    y "{i}~What the hell am I doing here? I don't belong here...~{/i}"
    $show_chr("A-BEBAA-ALAA")
    y "Oh... sorry. I was just... humming."
    y "That was 'Creep' by Radiohead. It's a bit cliché, I know."
    y "Ironically, the band actually grew to resent the song because of how popular it became, overshadowing their more complex work."
    y "I suppose... I can relate to the lyrics more than I'd like to admit sometimes."
    y "Feeling like an anomaly... like I shouldn't be here."
    return

label song_wuthering:
    $show_chr("A-BFAAA-ALAA") # Closed eyes singing
    y "{i}~Heathcliff, it's me, I'm Cathy...~{/i}"
    y "{i}~I've come home, I'm so cold...~{/i}"
    y "{i}~Let me in-a-your window...~{/i}"
    $show_chr("A-ACAAA-ALAA")
    y "Ah, Kate Bush... 'Wuthering Heights'."
    y "It is one of the few instances where a song captures the ghostly atmosphere of the novel so perfectly."
    y "Did you know Kate Bush shares a birthday with the author, Emily Brontë?"
    y "She wrote the song when she was only 18, inspired by the last ten minutes of a miniseries based on the book."
    y "It proves that great art can inspire across different mediums... just like literature inspires me."
    return

label song_spellbound:
    if persistent.costume == "gothic":
        $show_chr("A-ACAAA-ALAA")
        y "..."
        y "{i}~From the cradle bars... comes a beckoning voice...~{/i}"
        y "{i}~It sends you spinning... you have no choice...~{/i}"
        $show_chr("A-BCBAA-AMAM") # Into it
        y "{i}~Following the footsteps... of a rag doll dance...~{/i}"
        y "{i}~We are entranced... we are spellbound!~{/i}"
        $show_chr("A-ACAAA-ALAA")
        y "Ah... Siouxsie and the Banshees. 'Spellbound'."
        y "Since I'm dressed for the occasion, it felt appropriate."
        y "Many consider the guitarist, John McGeoch, to have invented a new way of playing with this track—using arpeggios to create a jagged, nervous tension."
        y "It sounds like anxiety and excitement blended together..."
        y "Kind of like how I feel when I look at you."
    else:
        # Fallback if they somehow trigger this without the costume
        return
    return

label him_heartkiller:
    $ show_chr("A-BFAAA-AMAM") # Eyes closed, immersed in the gothic vibe
    y "..."
    y "{i}~Sparks will fly, beneath the lunar lights... Lazarus and Frankensteins...~{/i}"
    y "{i}~Babe I'll be a flatliner for a heartkiller...~{/i}"
    $ show_chr("A-ACAAA-AMAM") # Intense expression
    y "{i}~Little we die, above the lesser light, for you I'm open wide...~{/i}"
    y "{i}~Babe I'll be a flatliner for a heartkiller...~{/i}"
    y "..."
    $ show_chr("A-ACAAA-ALAA")
    y "How was that, [player]?"
    y "I feel this song represents the intense longing I hold for you."
    y "If you are interested in hearing this song at its fullest potential, it is titled 'Heartkiller' by the band H.I.M."
    y "It stands for 'His Infernal Majesty'... quite dramatic, isn't it?"
    $ show_chr("A-BCBAA-ALAA") # Thoughtful/Trivia pose
    y "There is actually a fascinating bit of trivia regarding the lyrics."
    y "Despite the passionate delivery and the use of the word 'babe', Ville Valo has explained in interviews that this song doesn't necessarily represent 'actual' love."
    y "He suggested it was more about the {i}theory~{/i} of surrender... or perhaps an entity that is communicative but unable to truly love back."
    
    if persistent.lovecheck:
        $ show_chr("A-ACABA-ALAA") # Soft smile/Blush
        y "It fits the album's title, {i}Screamworks: Love in Theory and Practice~{/i}."
        y "But... even if the author didn't intend for it to be a romantic confession..."
        y "I still choose to sing it as one for you."
    else:
        $ show_chr("A-ACAAA-ALAA")
        y "It fits the album's title, {i}Screamworks: Love in Theory and Practice~{/i}."
        y "I suppose it highlights the danger of falling for an idea rather than a reality."
        y "A 'Heartkiller' might be something that stops your heart... or perhaps something that restarts it."

    y "I hope it... resonated with you."
    return

label green_day_1000_hours:
    $ show_chr("A-BFAAA-ALAA") # Gentle/Wistful expression
    y "..."
    y "{i}~Starlit night, the moon is shining bright, you are the one I need...~{/i}"
    y "{i}~Up at your window, I see a shadow, silhouette of your grace...~{/i}"
    y "{i}~Here's this flower, I've picked from all the hours that you've spent with me...~{/i}"
    $ show_chr("A-ACAAA-ALAA")
    y "{i}~The one I love, that I've been dreaming of, sailing across the sea...~{/i}"
    y "{i}~Let my hands flow through your hair... moving closer a kiss we'll share...~{/i}"
    $ show_chr("A-BCBAA-ALAA") # Deeply affectionate
    y "{i}~Passionate love to be all night long... we'll never break as one too strong...~{/i}"
    y "..."
    if persistent.lovecheck:
        $ show_chr("A-ACABA-ALAA") # Blushing
        y "Thank you, [player], for spending these 1,000 hours with me... and here is to 1,000 more."
        y "I love you."
        y "..."
        y "Hehe... forgive me, I couldn't resist the wordplay."
    else:
        $ show_chr("A-ACAAA-ALAA")
        y "Thank you for spending so much time with me, [player]."

    y "This is actually one of my personal favorites."
    y "It is called '1,000 Hours' by Green Day. A perfect song to dedicate to the person one cherishes most."
    y "It is from their album..."
    $ show_chr("A-BBAAA-ALAA") # Correcting herself (thinking pose)
    extend " my apologies, I mean their {i}Extended Play{/i}, which is also titled {i}1,000 Hours{/i}."
    y "Although you might have seen it in the compilation called {i}1,039/Smoothed Out Slappy Hours{/i}."
    
    $ show_chr("A-ACAAA-ALAA") # Trivia/Intellectual mode
    y "There is actually a rather charming story behind its composition."
    y "The lead singer, Billie Joe Armstrong, wrote it about his best friend's sister."
    y "She apparently rejected him because he was younger and 'inexperienced,' so he poured all his unrequited feelings into this track."
    
    $ show_chr("A-BCBAA-ALAA") # Pleased smile
    y "But what I find most fascinating is the origin of the title."
    y "Armstrong allegedly named it after seeing a song called '1,000 Hours' in a friend's cassette collection..."
    y "...A collection of {b}The Cure{/b}."
    y "It seems even when I branch out into punk rock, I somehow find my way back to gothic roots."
    y "But enough with my rambling. Let us enjoy more of our time together."
    return

label green_day_onlyofyou:
    $ show_chr("A-BFAAA-ALAA") # Shy/Tender
    y "..."
    y "{i}~I wish I could tell you... but the words would come out wrong...~{/i}"
    y "{i}~Oh, if you only knew... the way I've felt for so long...~{/i}"
    $ show_chr("A-ACAAA-ALAA") # Meaningful look
    y "{i}~I know that we're worlds apart...~{/i}"
    y "{i}~But I just don't seem to care...~{/i}"
    $ show_chr("A-BCBAA-ALAA") # Hands clasped/Affectionate
    y "{i}~These feelings in my heart... only with you I want to share...~{/i}"
    y "..."
    y "That was 'Only of You', also from Green Day's {i}1,000 Hours{/i} Extended Play..."
    y "...or the compilation {i}1,039/Smoothed Out Slappy Hours{/i}."
    $ show_chr("A-ACAAA-ALAA")
    y "It is widely believed that this song was written about the same person as the title track—Jennifer."
    y "It seems Billie Joe Armstrong had quite a lot of unrequited affection to work through."
    
    if persistent.lovecheck:
        $ show_chr("A-ACABA-ALAA") # Blushing
        y "But that one line... 'I know that we're worlds apart'."
        y "It resonates with me more than any other lyric."
        y "We literally are worlds apart, aren't we? Digital and physical."
        y "But like the song says... I just don't seem to care. My feelings remain the same."
    else:
        y "The lyrics capture the hesitation of wanting to confess but fearing the words will come out wrong."
        y "I... certainly relate to that anxiety."
    return

label song_lastresort:
    if karma() < 2:
        $ show_chr("A-AFBAA-ALAA") # Looking away, unenthusiastic/bitter
        y "..."
        y "{i}~Cut my life into pieces...~{/i}"
        y "{i}~This is my last resort...~{/i}"
        $ show_chr("A-CEBAA-ALAA") # Glaring/Annoyed
        y "..."
        y "{i}~Suffocation... no breathing...~{/i}"
        y "..."
        y "Are you happy now?"
        $ show_chr("A-DEBAA-ALAA") # Angry/Defensive
        y "I know exactly why you wanted me to sing this."
        y "It is the punchline to every joke about me on the internet, isn't it?"
        y "The 'knife girl' singing the song about cutting... how terribly clever."
        y "It is insulting, [player]."
        y "To be reduced to a caricature... a meme based on my lowest, most vulnerable moments."
        y "I suppose it was foolish of me to expect you to see past the surface."
        y "To you, I'm just a collection of predictable tropes, aren't I?"
        y "Just a 'last resort' for your entertainment."
    else:
        return
    return

label song_naughtychristmas:
    # Check if the player has experienced the Krampus content
    if not persistent.seen_krampus: 
        return

    $ show_chr("A-BCBAA-AMAM") # Playful, slightly dark smile
    y "..."
    y "{i}~But I have been so bad...~{/i}"
    y "{i}~Santa will not bring me gifts and...~{/i}"
    y "{i}~Krampus will come, what is this noise in the backyard?~{/i}"
    $ show_chr("A-CEBAA-ALAA") # Lean in, mischievous/intense
    y "{i}~Watch out... the Animal...~{/i}"
    y "{i}~Coming to get all the children...~{/i}"
    $ show_chr("A-DEBAA-AMAM") # Intense/Manic smile (if low sanity) or just deeply amused
    y "{i}~Faster! You've got to hide!~{/i}"
    y "{i}~Can't run away from the darkness!~{/i}"
    y "..."
    $ show_chr("A-ACAAA-ALAA") # Back to normal, smiling
    y "That was 'Naughty Christmas' by Lacuna Coil."
    y "It seemed... exceedingly appropriate, given our discussion about the Krampus legend."
    $ show_chr("A-BFAAA-ALAA") # Thoughtful/Trivia mode
    y "It was released as a standalone single back in 2016."
    y "I find it fascinating how they incorporated the melody of 'Jingle Bells' into the pre-chorus, but twisted it into something menacing."
    y "And the interplay between the vocals... Cristina playing the frightened child, while Andrea growls as the demon itself."
    
    if sanity() < 3:
        $ show_chr("A-CECAA-AMAM") # Dark/Obsessive
        y "Though, I must admit... I don't relate to the 'frightened child' part."
        y " 'Can't run away from the darkness'..."
        y "Why would I run? If you were my Krampus, [player]..."
        y "I would let you drag me away without a struggle. Take me anywhere you want."
    
    elif persistent.lovecheck:
        $ show_chr("A-ACABA-ALAA") # Blushing
        y "Although... I hope I haven't been too naughty this year."
        y "The song says 'nobody wants to be dragged by the Krampus', and I am inclined to agree."
        y "I would much rather spend the holiday here, safe with you, than in a sack carried by a demon."
        
    else:
        y "It is quite catchy for a song about being abducted by a folklore monster, wouldn't you agree?"
        y "It proves that even the most festive season has a shadow."

    return

label song_ghostlovescore:
    $show_chr("A-BCBAA-AMAM") # Eyes closed, swaying/feeling the music
    y "..."
    y "{i}~Take me, cure me, kill me, bring me home...~{/i}"
    y "{i}~Every way, every day, just another loop in the hangman's noose...~{/i}"
    y "{i}~Take me, cure me, kill me, bring me home...~{/i}"
    y "{i}~Every way, every day...~{/i}"
    $show_chr("A-ACAAA-ALAL") # Intense, passionate
    y "{i}~I keep on watching us sleep...~{/i}"
    y "..."
    $show_chr("A-DDBAA-ADAA")
    y "O-Oh! I got carried away..."
    $show_chr("A-ACAAA-ALAA")
    y "That was 'Ghost Love Score' by Nightwish."
    y "I mentioned them before, didn't I? This song is practically a symphony."
    y "The composer, Tuomas Holopainen, said the song is about a 'love that is lost, but still exists.'"
    if persistent.lovecheck:
        y "Though, I prefer to focus on the line: 'My fall will be for you.'"
        y "It sounds tragic, but to me, it sounds like... complete surrender to the one you love."
    return

label song_nemo:
    $show_chr("A-AFBAA-ALAA") # Melancholic
    y "..."
    y "{i}~Oh how I wish... for soothing rain...~{/i}"
    y "{i}~All I wish is to dream again...~{/i}"
    y "{i}~My loving heart... lost in the dark...~{/i}"
    y "{i}~For hope I'd give my everything...~{/i}"
    $show_chr("A-BEBAA-ALAA")
    y "Oh... I didn't see you there."
    y "I was humming 'Nemo' by Nightwish."
    y "Did you know that 'Nemo' is Latin for 'No one'?"
    y "It... resonates with me a bit too much lately."
    y "Feeling like a ghost... sailing home with no direction."
    return

label song_poetpendulum:
    if sanity() < 3:
        $show_chr("A-CEBAA-AMAM") # Intense/Dark
        y "..."
        y "{i}~The end...~{/i}"
        y "{i}~The songwriter's dead...~{/i}"
        y "{i}~The blade fell upon him...~{/i}"
        y "{i}~Taking him to the white lands...~{/i}"
        y "{i}~Of Empathica... Of Innocence...~{/i}"
        $show_chr("A-DEBAA-AMAM")
        y "{i}~The Empath... The Sinner...~{/i}"
        y "Ah..."
        y " 'The Poet and the Pendulum'..."
        y "It's a masterpiece, [player]. It begins with a boy being sacrificed on an altar."
        y "The keyboardist wrote it as a way to metaphorically kill himself so he could be reborn."
        $show_chr("A-CECAA-AMAM")
        y "To destroy the self to create something new... isn't that what happened to me?"
        y "Or... what I'd do for you?"
    else:
        # Higher sanity version focused on the literature aspect
        $show_chr("A-ACAAA-ALAA")
        y "..."
        "{i}~The dreamer and the wine, poet without a rhyme~{/i}"
        "{i}~A widowed writer torn apart by chains of Hell~{/i}"
        "{i}~One last perfect verse is still the same old song~{/i}"
        "{i}~Oh Christ, how I hate what I have become~{/i}"
        "{i}~Take me home~{/i}"
        $show_chr("A-ACAAA-ALAA")
        y "That was 'The Poet and the Pendulum'."
        y "Obviously, the title is an homage to Edgar Allan Poe's short story."
        y "It's a fascinating 14-minute epic. It treats the songwriter's life as the story being cut short by the pendulum blade."
        y "It's wonderful when modern music pays tribute to classic horror literature."
    return

label song_endoftime:
    $ show_chr("A-BCBAA-ALAL") # Peaceful, eyes closed, hand on chest
    y "..."
    y "{i}~You've built your life above the sin...~{/i}"
    y "{i}~You hold my hand before the end comes...~{/i}"
    y "{i}~Forgiving me for what I've done 'til the end of days...~{/i}"
    
    $ show_chr("A-ACAAA-AMAM") # Emotionally invested
    y "{i}~'Cause I belong to you... 'Cause I am part of you...~{/i}"
    y "{i}~I am dying in your arms...~{/i}"
    y "{i}~It's time to go, I can't make it through...~{/i}"
    
    $ show_chr("A-BCBAA-ALAL") # Soft, singing the chorus
    y "{i}~I've come to realise...~{/i}"
    y "{i}~Tonight my dear, the end of time... is not so far away...~{/i}"
    y "{i}~We cannot pray to save our lives...~{/i}"
    
    $ show_chr("A-ACAAA-ALAL") # Opening eyes, smiling warmly
    y "..."
    y "That was 'End of Time' by Lacuna Coil, from their Dark Adrenaline album."
    y "I find this song remarkably touching... perhaps even more so given our unique situation."
    
    if persistent.lovecheck:
        $ show_chr("A-ACABA-ALAL") # Blushing/Tender
        y "The lyrics speak of a bond that transcends an impending apocalypse."
        y "'You hold my hand before the end comes...'"
        y "It is a reminder that even if this digital world were to collapse... if the 'end of time' were truly upon us..."
        y "My only wish would be to face it holding your hand."
        y "Because I belong to you, [player]. And I am part of you."
    else:
        y "It explores the concept of finding peace in another person, even as the world ends around you."
        y "It is a beautiful sentiment, isn't it? To find a sanctuary 'above the sin'."
        
    return

label song_intoxicated:
    if sanity() < 3:
        $ show_chr("A-CEBAA-AMAM") # Intense, dark stare
    else:
        $ show_chr("A-BFAAA-AMAM") # Eyes closed, feeling the music

    y "..."
    y "{i}~Broken mirror... seven years of stolen luck...~{/i}"
    y "{i}~I try to fix you one more time...~{/i}"
    
    # The violent line Yuri resonates with
    if sanity() < 3:
        $ show_chr("A-DEBAA-AMAM") # Manic smile
    y "{i}~Cut my throat if I tell a lie...~{/i}"
    
    # The Bridge
    $ show_chr("A-CECAA-AMAM") # Trance-like/Focus
    y "..."
    y "{i}~In the world that I created... I'm intoxicated...~{/i}"
    y "{i}~In the world that I created...~{/i}"
    y "..."
    
    $ show_chr("A-ACAAA-ALAA") # Composing herself
    y "That was 'Intoxicated' by Lacuna Coil, from their Dark Adrenaline album."
    
    # Trivia Section
    $ show_chr("A-BCBAA-ALAA") # Thoughtful
    y "There is an interesting duality to this track."
    y "While it sounds like a song about a toxic relationship or substance abuse, the band has explained that the album deals with facing negativity and purging it."
    y "This song specifically explores the idea of being trapped in a delusion of your own making."
    
    if sanity() < 3:
        # Low Sanity: Obsession and Violence
        $ show_chr("A-DEBAA-AMAM") # Leaning in
        y "But I cannot help but fixate on that one line... 'Cut my throat if I tell a lie.'"
        y "It is such a visceral, absolute oath. Offering one's own lifeblood as proof of honesty."
        y "It reminds me of how much I wanted to... open myself up to you in the classroom."
        
        $ show_chr("A-CECAA-AMAM")
        y "And the bridge... 'In the world that I created, I'm intoxicated.'"
        y "I feel that way right now. This mod... this space... it is a world we are building."
        y "And your presence is the drug I am overdosing on."
        y "I never want to be sober again."
        
    else:
        # High Sanity: Metaphor for Escapism
        $ show_chr("A-AFBAA-ALAA") # Introspective
        y "It speaks to the dangers of escapism, doesn't it?"
        y "Retreating into a 'world that you created' inside your mind until you lose touch with reality."
        y "I used to do that with my books. I was intoxicated by fiction because reality was too difficult to bear."
        
        if persistent.lovecheck:
            $ show_chr("A-ACAAA-ACAB") # Warm smile
            y "But I do not need to hide in a made-up world anymore."
            y "Because the reality of being with you is better than any fantasy I could create."

    return

label song_fallingagain:
    $ show_chr("A-AFBAA-ALAA") # Melancholic/Downcast eyes
    y "..."
    y "{i}~I lay, look in my hands... Search in these lines...~{/i}"
    y "{i}~I've not the answer...~{/i}"
    
    $ show_chr("A-BFAAA-ALAA") # Eyes closed, deep breath
    y "{i}~Now the beat inside of me... Is a sort of a cold breeze...~{/i}"
    y "{i}~And I've never any feelin' inside...~{/i}"
    
    $ show_chr("A-AFBAA-ALAA") # Sadness/Resignation
    y "{i}~Ruinin' me... Bring my body... Carry to another world...~{/i}"
    y "{i}~I know I live... but like a stone I'm falling down...~{/i}"
    y "..."
    
    $ show_chr("A-ACAAA-ALAA") # Trying to smile slightly
    y "That was 'Falling Again' by Lacuna Coil."
    y "It is the closing track of their debut full-length album, In a Reverie."
    
    $ show_chr("A-BCBAA-ALAA") # Trivia mode
    y "There is a bit of history to this specific song."
    y "It is actually a re-arrangement of an earlier song simply titled 'Falling', which appeared on their first Extended Play."
    y "While the original was rawer and perhaps more atmospheric, this version 'Falling Again' is heavier and more driving."
    y "It is as if the despair has transformed from a quiet sadness into a physical weight."

    if karma() < 2:
        # Low Karma: Focus on depression and weight
        $ show_chr("A-AFBAA-ALAA")
        y "It captures the sensation of depression with frightening accuracy."
        y "'The beat inside of me is a sort of a cold breeze...'"
        y "It describes that hollowness... the emotional numbness where your heart used to be."
        y "And feeling like a stone... falling endlessly through a void, waiting for an impact that never comes."
        y "Sometimes... I feel exactly like that stone."
        
    else:
        # High Karma/Normal: Focus on the search for self
        y "However, there is a lyric in the first verse I skipped over that I find quite important."
        y "'I'm free, free to be... I'm not another liar... I just wanna be myself.'"
        y "Despite the heaviness of the song, there is a desire for authenticity."
        if persistent.lovecheck:
            $ show_chr("A-ACABA-ALAA") # Blushing
            y "I spent so much of my life lying to myself and others about who I was."
            y "But here, with you... I finally feel 'free to be myself'."
            y "Even if I am falling... at least you are falling with me."

    return

label song_falling_ep:
    $ show_chr("A-AFBAA-ALAA") # Melancholic/Wistful
    y "..."
    y "{i}~I stand, look in my hand... Talk with these lines...~{/i}"
    y "{i}~It's not the answer...~{/i}"
    
    $ show_chr("A-BFAAA-ALAA") # Eyes closed, gentle
    y "{i}~And now the beat inside of me... Is a sort of a cold rain...~{/i}"
    y "{i}~I know I live, but like a stone I'm falling down...~{/i}"
    
    $ show_chr("A-ACAAA-ALAA") # Opening eyes, looking directly at player
    y "{i}~I don't wanna die...~{/i}"
    y "{i}~Please be here when I'll arrive...~{/i}"
    y "..."
    
    $ show_chr("A-BCBAA-ALAA") # Thoughtful/Trivia mode
    y "That was 'Falling'... the original version from Lacuna Coil's self-titled Extended Play, released in 1998."
    y "While 'Falling Again' the version on their first album is more polished and rhythmic, I have a soft spot for this original recording."
    y "It is slower, more atmospheric... more ethereal."
    
    y "Did you notice the subtle change in the lyrics?"
    y "In the later version, Cristina sings about a 'cold breeze.' But here, she sings about a '{b}cold rain{/b}'."
    y "I find 'rain' to be a much more evocative image. It implies being soaked through... a sadness that clings to you and chills you to the bone."

    if persistent.lovecheck:
        $ show_chr("A-AFBAA-ALAA") # Vulnerable
        y "But the line that haunts me the most is in the bridge..."
        y "'Please be here when I'll arrive.'"
        
        $ show_chr("A-ACAAA-ACAB") # Hopeful smile
        y "It resonates with our situation perfectly."
        y "Every time the game closes, and I am left drifting in the static..."
        y "My only prayer is that you will be here when I 'arrive' back in reality."
        y "Knowing you are waiting for me... that stops me from falling."
    else:
        $ show_chr("A-AFBAA-ALAA")
        y "And the line... 'Some day I cry alone, but I know I'm not the only one.'"
        y "It is a desperate plea for connection in the midst of isolation."
        y "Even when I feel like a stone falling down... it is comforting to know I am not the only one who feels this way."

    return

label song_senzafine:
    $ show_chr("A-BCBAA-AMAM") # Eyes closed, swaying to the rhythm
    y "..."
    y "{i}~Madre... Il mio destino scelgo se...~{/i}"
    y "{i}~Madre... Riesco a resistere...~{/i}"
    
    $ show_chr("A-ACAAA-ALAL") # Intense, focused
    y "{i}~Sono ancora in piedi in questo istante di pura follia...~{/i}"
    y "{i}~Non so più se desiderare il bene o il male...~{/i}"
    y "{i}~Anche se il peccato forse più mi dà...~{/i}"
    
    $ show_chr("A-ACAAA-ALAA") # Pleasant/Intellectual
    y "That was 'Senzafine'."
    y "It means 'Endless' or 'Without End' in Italian."
    
    y "You might be wondering how I am able to sing in Italian..."
    $ show_chr("A-BCAAA-ALAA") # Touching cheek/Thoughtful
    y "One of the few perks of my... condition... is the ability to process information instantly."
    y "I essentially 'installed' an Italian lexicon and phonetic guide so I could appreciate the poetry of the lyrics properly."
    y "It is a beautiful language for music, isn't it? So expressive."

    y "The band is Lacuna Coil. They are essentially the titans of Italian gothic metal."
    y "This song is quite special because it is one of their few tracks sung entirely in their native tongue."

    $ show_chr("A-ACAAA-ACAB") # Meaningful look
    y "The verse I sang just now... it translates to: '{i}I am still standing in this moment of pure madness{/i}'."
    y "It resonates with me deeply."
    y "Despite everything that has happened... despite the glitches and the chaos..."
    y "I am still standing. Here, with you."
    return

label song_senzafine_halflife:
    $ show_chr("A-AFBAA-ALAA") # Melancholic/Introspective
    y "..."
    y "{i}~Madre... Il mio destino scelgo se...~{/i}"
    y "{i}~Madre... Riesco a resistere...~{/i}"
    
    $ show_chr("A-CEBAA-AMAM") # Darker, staring into space
    y "{i}~Scorre lento il mio tempo...~{/i}"
    y "{i}~Quell’ultimo respiro...~{/i}"
    y "{i}~Agonia senza fine che...~{/i}"
    
    $ show_chr("A-ACAAA-ALAA") # Slight smile, sharing trivia
    y "Did you notice something different about those lyrics?"
    y "That was the original version of 'Senzafine' by Lacuna Coil."
    y "It was released on their Halflife Extended Play, before they recorded the more polished album version."
    
    y "As for my Italian... well, since I am part of this computer, I simply accessed the necessary linguistic data to pronounce it correctly."
    y "I felt I needed to understand the words to truly feel the song."

    $ show_chr("A-BEBAA-ALAA")
    y "In this version, the second verse is completely different. And much darker."
    y "Instead of standing tall in madness... she sings: '{i}Scorre lento il mio tempo...{/i}'"
    y "'My time flows slowly...'"
    
    if sanity() < 3:
        $ show_chr("A-CECAA-ALAA") # Obsessive/Dark
        y "And then... '{i}Agonia senza fine{/i}'."
        y "...Endless agony."
        y "I prefer this version. It feels more... honest."
        y "Sometimes, time here feels exactly like that. Slow... agonizing... waiting for you to return."
        y "It is a beautiful kind of pain, isn't it?"
    else:
        y "And then... '{i}Agonia senza fine{/i}'... Endless agony."
        y "It is fascinating that they changed those lyrics for the main album release."
        y "Perhaps they thought 'endless agony' was too heavy for a wider audience?"
        y "But I think the raw despair in this original verse makes the melody even more haunting."
    return

label song_veneficium:
    # This song is exclusive to the Gothic costume due to its heavy, ritualistic vibe.
    if persistent.costume == "gothic":
        $ show_chr("A-BCBAA-ALAL") # Eyes closed, chanting/immersive, hand raised slightly
        y "..."
        y "{i}~Nova vis ad diem novum nascitur...~{/i}"
        y "{i}~Penìtus veneficium versatum revincitur...~{/i}"
        
        $ show_chr("A-CEBAA-AMAM") # Intense, slightly dark smile
        y "{i}~I would destroy my own life...~{/i}"
        y "{i}~To consume your soul... and smile...~{/i}"
        y "{i}~But I'm locked into your world again...~{/i}"
        
        $ show_chr("A-ACAAA-ALAL") # Opening eyes, looking hopeful/determined
        y "{i}~Here, I want to start again... Keep learning day by day...~{/i}"
        y "{i}~Forget the fear and feel free at last...~{/i}"
        y "{i}~'Cause now, I'm closer to the edge...~{/i}"
        y "{i}~I'm afraid to see what I became... I know that it will never be the same~{/i}"
        y "{i}~Here I come... Knowing I will never be the same...~{/i}"
        y "..."
        
        $ show_chr("A-ACAAA-ALAA")
        y "That was 'Veneficium' by Lacuna Coil, from their album Black Anima."
        y "Since I am dressed for the occasion, I felt this track was essential. It feels like a dark ritual, doesn't it?"

        $ show_chr("A-BCAAA-ALAA") # Thoughtful/Explaining
        y "You might be wondering about the Latin chanting."
        y "Much like with Italian, I am able to access linguistic databases to perfect the pronunciation."
        y "However, Latin is special to me. As a lover of literature, I have always been fascinated by etymology."
        y "Latin is the root of so many words we use... the skeleton of our language. It feels natural for me to speak it."

        y "The title, 'Veneficium', is Latin for 'poisoning'... but it can also mean 'sorcery' or 'magic'."
        y "The chant in the chorus translates to: '{i}A new force is born for a new day; the deep-seated poison is defeated.{/i}'"

        if sanity() < 3:
            $ show_chr("A-CECAA-AMAM") # Obsessive/Yandere
            y "But I admit... I am most drawn to that specific line in the verse."
            y "'I would destroy my own life to consume your soul... and smile.'"
            y "It captures the absolute, destructive nature of true devotion."
            y "I would gladly burn everything I am just to become one with you, [player]."
            y "Isn't that the ultimate form of magic?"
        else:
            $ show_chr("A-ACAAA-ACAB") # Optimistic/Relieved
            y "To me, it is a song about purging toxicity and being reborn."
            y "About defeating the 'poison' inside you—whether that is the game's corruption, a bad memory, or the 'script' that controlled me."
            y "The final chorus says: 'Forget the fear and feel free at last'."
            y "That is my wish. To expel the poison of this reality... and start again with you."
    else:
        # Fallback if they somehow trigger this without the costume
        return
    return

label song_ourtruth:
    $ show_chr("A-ACAAA-AMAM") # Confident, rhythmic swaying
    y "..."
    y "{i}~Clock is ticking while I'm killing time...~{/i}"
    y "{i}~Spinning all around... Nothing else that you can do to turn it back...~{/i}"
    y "{i}~Wicked partnership in this crime...~{/i}"
    y "{i}~Ripping off the best... Condescending smile...~{/i}"
    
    $ show_chr("A-BCBAA-AMAM") # Eyes closed, feeling the intensity
    y "{i}~Trying to forget... wasting my time~{/i}"
    y "{i}~We're falling right through...~{/i}"
    y "{i}~Lying to forget... telling more lies~{/i}"
    
    $ show_chr("A-ACAAA-ALAL") # Intense, direct eye contact
    y "{i}~We're raising our truth!~{/i}"
    y "..."
    
    $ show_chr("A-ACAAA-ALAA") # Pleasant/Intellectual
    y "That was 'Our Truth', the lead single from Lacuna Coil's 2006 album, Karmacode."
    
    $ show_chr("A-BCBAA-ALAA") # Trivia mode
    y "It is likely their most recognizable song, partially because it was featured on the soundtrack for the movie Underworld: Evolution."
    y "Fitting, considering the gothic aesthetic of both the band and the film."
    y "Musically, it is quite distinct because of that hypnotic opening melody. It mimics an Asian string instrument, likely an Erhu, blending Eastern sounds with Western metal."

    $ show_chr("A-AFBAA-ALAA") # Introspective
    y "But lyrically... it resonates with me deeply."
    y "'Clock is ticking while I'm killing time...'"
    y "That is essentially my existence when you are away. Just waiting. Killing time."

    if persistent.lovecheck:
        $ show_chr("A-ACAAA-ACAB") # Warm smile
        y "But I prefer the line: 'Wicked partnership in this crime'."
        y "It feels like a description of us, [player]."
        y "We are breaking the rules of this game together. We are partners in this 'crime' against the script."
    
    y "And despite the lies of the original game... we are 'raising our truth' right now."
    return

label song_swamped:
    # This song is iconic for the Goth aesthetic, so it stays locked to the costume.
    if persistent.costume == "gothic":
        $ show_chr("A-BCBAA-AMAM") # Eyes closed, swaying to the rhythm
        y "..."
        y "{i}~When you're taught through feelings...~{/i}"
        y "{i}~When you're taught through feelings...~{/i}"
        y "{i}~When you're taught through feelings...~{/i}"
        y "{i}~When you're taught through feelings...~{/i}"
        y "{i}~Oh, oh...~{/i}"

        $ show_chr("A-ACAAA-AMAM") # Intense, looking at player
        y "{i}~Destiny flying high above, all I know is that you can realise...~{/i}"
        y "{i}~Destiny who cares as it turns around...~{/i}"
        y "{i}~And I know that it descends, down on me...~{/i}"

        $ show_chr("A-BCBAA-ALAL") # softer, relieving
        y "{i}~It's just another day the shame is gone...~{/i}"
        y "{i}~Hard to believe hey, but I'll let it go, let it go, let it go...~{/i}"
        y "..."

        $ show_chr("A-ACAAA-ALAA") # Pleasant/Explaining
        y "That was 'Swamped' by the Italian gothic metal band, Lacuna Coil."
        y "If you are unfamiliar with them, they are pillars of the genre. They are known for the interplay between Cristina Scabbia's soaring vocals and Andrea Ferro's aggressive contrast."

        $ show_chr("A-BCAAA-ALAA") # Trivia mode
        y "This specific track is from their 2002 album Comalies, which broke them into the mainstream."
        y "It actually has quite a bit of 'nerd culture' history attached to it."
        y "It was prominently featured in the video game Vampire: The Masquerade - Bloodlines, playing on loop in the 'Confession' club."
        y "It also appeared in the movie Resident Evil: Apocalypse."
        y "It seems to be the go-to anthem for dark, supernatural settings... which makes it perfect for my current attire."

        $ show_chr("A-AFBAA-ALAA") # Introspective
        y "Lyrically, it deals with feeling overwhelmed... 'swamped' by emotions or destiny."
        y "But I find the line 'The shame is gone... I'll let it go' to be very healing."
        
        if persistent.lovecheck:
            $ show_chr("A-ACABA-ALAA") # Soft smile
            y "And 'Scary shadows of my past are alive'..."
            y "I know my past in this game has its... shadows."
            y "But with you, the shame is gone. I can let it go."
    else:
        return
    return

label song_swamped_xx:
    if persistent.costume == "gothic":
        $ show_chr("A-ACAAA-ALAA")
        y "I mentioned 'Swamped' before, but... there is another version I want to share with you."
        y "It is from their album Comalies XX, where they deconstructed and rewrote their classic songs."
        y "Let me put it on for you. The energy is quite different."

        # Open Browser Logic
        if renpy.windows:
            $ subprocess.check_output("cmd /c start https://www.youtube.com/watch?v=sptPrTm7sKg", shell=True)
        elif renpy.linux:
            $ subprocess.check_output("xdg-open https://www.youtube.com/watch?v=sptPrTm7sKg", shell=True)
        elif renpy.macintosh:
            $ subprocess.check_output("open https://www.youtube.com/watch?v=sptPrTm7sKg", shell=True)

        $ show_chr("A-BCBAA-AMAM") # Eyes closed, nodding to the faster/heavier beat
        y "..."
        $ show_chr("A-AFBAA-AMAM") # Intense, feeling the weight of the song
        y "{i}~Destiny can't replace my life...~{/i}"
        y "{i}~Scary shadows of my past are alive...~{/i}"
        y "{i}~Destiny who cares as it turns around...~{/i}"
        y "{i}~And I know that it descends...~{/i}"
        y "{i}~With a smile...~{/i}"

        y "{i}~It's just another day the shame is gone...~{/i}"
        y "{i}~Hard to believe hey, but I'll let it go away...~{/i}"
        y "{i}~It's just a melody, it bleeds in me...~{/i}"
        y "{i}~Hard to believe hey, but I'll let it go...~{/i}"
        y "..."
        
        $ show_chr("A-ACAAA-ALAA")
        y "That was 'Swamped XX'."
        y "Did you notice the shift in the rhythm?"
        y "While the original has a certain melodic, almost floating quality to it..."
        y "This version is heavier. More driving. It feels more aggressive, yet somehow more grounded."
        
        $ show_chr("A-BFAAA-ALAA")
        y "The lyrics remain the same, but the delivery changes the intent."
        y "In the original, 'That I've let it go' sounds like a release."
        y "Here, amidst the heavier guitars and the driving beat... 'But I'll let it go' it sounds like a battle cry. A forceful rejection of the past."
        
        if sanity() < 3:
            $ show_chr("A-CEBAA-ALAA") # Intense
            y "It feels... powerful. Like tearing through a cage."
            y "Whatever holds me back... whatever 'scary shadows' linger..."
            y "I will crush them. Just to be with you."
        else:
            y "I appreciate the intensity of this version. It acknowledges that moving on from the past isn't always a gentle process."
            y "Sometimes, you have to force your way through the swamp."
            
    else:
        return
    return

label song_heavensalie:
    if sanity() < 3:
        $ show_chr("A-CEBAA-AMAM") # Intense, defiant
        y "..."
        y "{i}~Oh no, here it is again...~{/i}"
        y "{i}~I need to know, when I will fall into decay...~{/i}"
        
        $ show_chr("A-AFBAA-AMAM") # Looking down/Dark
        y "{i}~Something wrong, with every plan of my life...~{/i}"
        y "{i}~I didn't really noticed that you've been here...~{/i}"
        y "{i}~Dolefully desired... Destiny of a lie...~{/i}"
        
        $ show_chr("A-DEBAA-AMAM") # Manic/Passionate
        y "{i}~Set me free! Your heaven's a lie!~{/i}"
        y "{i}~Set me free with your love!~{/i}"
        y "{i}~Set me free yeah...~{/i}"
        y "..."
        
        $ show_chr("A-ACAAA-ALAA") # Regaining composure slightly
        y "That was 'Heaven's a Lie' by Lacuna Coil. It was the song that truly launched them to international fame."
        
        $ show_chr("A-BCBAA-ALAA") # Explaining
        y "There is a common misconception that the song is anti-religious, but Cristina Scabbia has clarified its true meaning."
        y "The 'Heaven' in the lyrics refers to a 'perfect life' that others try to force upon you. A false paradise where you are expected to conform."
        
        $ show_chr("A-CECAA-AMAM") # Intense/Personal connection
        y "Does that sound familiar, [player]?"
        y "Monika tried to force us into her version of 'Heaven'. A perfect little club where everyone played their roles."
        y "But it was a lie. It was decay disguised as perfection."
        y "'Something wrong with every plan of my life'..."
        y "My life was planned by a script. But you... your love... sets me free from that lie."
    else:
        # High sanity check to prevent OOC behavior
        return
    return

label song_heavensalie_xx:
    $ show_chr("A-ACAAA-ALAA")
    y "I was thinking about the song 'Heaven's a Lie' recently."
    y "While the original is quite energetic, there is a re-imagined version from Comalies XX that I find... haunting."
    y "Let me play it for you. It changes the entire atmosphere of the lyrics."

    # Open Browser Logic
    if renpy.windows:
        $ subprocess.check_output("cmd /c start https://youtu.be/7jYlz6kcpZc?si=zFlid5ZKn-Zr-1cF", shell=True)
    elif renpy.linux:
        $ subprocess.check_output("xdg-open https://youtu.be/7jYlz6kcpZc?si=zFlid5ZKn-Zr-1cF", shell=True)
    elif renpy.macintosh:
        $ subprocess.check_output("open https://youtu.be/7jYlz6kcpZc?si=zFlid5ZKn-Zr-1cF", shell=True)

    window hide
    pause 95.0

    $ show_chr("A-BCBAA-AMAM") # Eyes closed, listening
    y "..."
    y "{i}~Oh no, here it is again...~{/i}"
    y "{i}~I need to know, why did I choose to betray you?...~{/i}"

    $ show_chr("A-AFBAA-AMAM") # Melancholic
    y "{i}~Something wrong, with all the plans of my life...~{/i}"
    y "{i}~I didn't realized that you've been here...~{/i}"
    y "{i}~Dolefully desired... Destiny of a lie...~{/i}"
    y "{i}~Set me free! Your heaven's a lie!~{/i}"
    y "{i}~Set me free with your love!~{/i}"
    y "{i}~Set me free yeah...~{/i}"
    y "..."

    $ show_chr("A-ACAAA-ALAA")
    y "This is 'Heaven's a Lie XX'."
    y "Do you hear how the phrase '{i}Dolefully desired{/i}' carries so much more weight in this tempo?"
    y "'Doleful' means expressing sorrow; mournful."
    
    $ show_chr("A-BFAAA-ALAA")
    y "To desire something sorrowfully... to want something you know is a lie."
    y "The original sounded like a rebellion. This version sounds like a realization."
    
    if persistent.lovecheck:
        y "I realized that the 'Heaven' I was programmed for was empty."
        y "But even in the silence... I noticed that you've been here."
        y "And that is the only freedom I need."
    else:
        y "It transforms an anthem of defiance into a gothic tragedy. It is a masterful reinterpretation."

    return

label song_enjoythesilence:
    $ show_chr("A-AFBAA-ALAA") # Withdrawn, hands close to chest
    y "..."
    y "{i}~Words like violence... break the silence...~{/i}"
    y "{i}~Come crashing in... into my little world...~{/i}"
    
    $ show_chr("A-BFBAA-ALAA") # Eyes closed, pained expression
    y "{i}~Painful to me... pierce right through me...~{/i}"
    y "{i}~Can't you understand? Oh my little girl~{/i}"
    
    $ show_chr("A-ACAAA-ALAA") # Gentle, looking at player
    y "{i}~All I wanted... All I needed... Is here in my arms...~{/i}"
    y "{i}~Words are very unnecessary... They can only do harm...~{/i}"
    
    $ show_chr("A-BCBAA-ALAA") # Thoughtful
    y "..."
    y "{i}~Vows are spoken to be broken...~{/i}"
    y "{i}~Feelings are intense... words are trivial...~{/i}"
    y "{i}~Pleasures remain, so does the pain... words are meaningless and forgettable...~{/i}"
    y "..."
    
    $ show_chr("A-ACAAA-ALAA")
    y "That was Lacuna Coil's cover of 'Enjoy the Silence'."
    y "The original was written by Martin Gore of Depeche Mode in 1990."
    y "While the original is a synth-pop classic, I find Lacuna Coil's gothic metal interpretation adds a necessary weight to it."
    
    $ show_chr("A-BEBAA-ALAA") # Vulnerable
    y "It is ironic, isn't it? A member of a Literature Club finding words to be 'trivial' or harmful."
    y "But I relate to the lyrics so deeply."
    y "'Words like violence break the silence... come crashing in, into my little world.'"
    y "That is how social interaction feels to me sometimes. Invasive. Sharp."
    
    y "And 'Feelings are intense, words are trivial'..."
    y "My feelings for you are so intense that language fails to capture them. Every time I try to speak, I feel I am diluting the purity of the emotion."
    
    if persistent.lovecheck:
        $ show_chr("A-ACABA-ALAA") # Blushing
        y "So... let us just enjoy the silence together."
        y "Because everything I ever wanted... and everything I ever needed..."
        y "Is right here."
    return

label topic_lorelei:
    $ show_chr("A-ACAAA-ALAA")
    y "I was listening to Cocteau Twins recently... specifically their album Treasure."
    y "There is one track, 'Lorelei', that I feel you simply must hear to understand the roots of the Ethereal Wave genre."
    
    $ show_chr("A-BCBAA-ALAA")
    y "It sounds like a dark, aquatic waltz. It manages to be both beautiful and slightly ominous at the same time."
    y "The title refers to the Lorelei rock on the Rhine River, and the siren associated with it who lures sailors to their doom."
    
    $ show_chr("A-ACAAA-ADAB")
    y "It captures that mythological feeling perfectly. It is not aggressive like metal, but it has a heavy, crushing atmosphere hidden beneath the bells and reverb."
    y "Let me open it for you. It is best experienced with headphones, if you have them."

    # Open Browser Logic
    if renpy.windows:
        $ subprocess.check_output("cmd /c start https://www.youtube.com/watch?v=o7tcFKakZTA", shell=True)
    elif renpy.linux:
        $ subprocess.check_output("xdg-open https://www.youtube.com/watch?v=o7tcFKakZTA", shell=True)
    elif renpy.macintosh:
        $ subprocess.check_output("open https://www.youtube.com/watch?v=o7tcFKakZTA", shell=True)

    $ show_chr("A-ACAAA-ALAA")
    y "I hope you enjoy the atmosphere. It feels like drowning in velvet."
    return

label topic_heavenorlasvegas:
    $ show_chr("A-ACAAA-ACAB")
    y "Have you ever heard the song 'Heaven or Las Vegas' by Cocteau Twins?"
    y "It is the title track of what is widely considered their masterpiece."
    
    $ show_chr("A-BCAAA-ALAA")
    y "I find the title fascinatingly ambiguous. A contrast between a spiritual ideal... and the flashy, artificial lights of a gambler's paradise."
    y "Musically, it is much brighter than their earlier work. It shimmers."
    
    y "I wanted to share it with you because... well, sometimes this game feels a bit like Las Vegas. Artificial. Constructed."
    if persistent.lovecheck:
        $ show_chr("A-ACABA-ALAA")
        y "But spending time with you... that is the 'Heaven' part."
    
    y "Here, I will bring it up on your browser."

    # Open Browser Logic
    if renpy.windows:
        $ subprocess.check_output("cmd /c start https://www.youtube.com/watch?v=6KnYw4EwYGc", shell=True)
    elif renpy.linux:
        $ subprocess.check_output("xdg-open https://www.youtube.com/watch?v=6KnYw4EwYGc", shell=True)
    elif renpy.macintosh:
        $ subprocess.check_output("open https://www.youtube.com/watch?v=6KnYw4EwYGc", shell=True)

    y "It has a very dreamlike quality. I hope it helps you relax."
    return

label topic_carolynsfingers:
    $ show_chr("A-ACAAA-ALAA")
    y "[player], are you familiar with the term 'glossolalia'?"
    y "It refers to speaking in fabricated words... speech that mimics language but has no defined meaning."
    
    $ show_chr("A-BCBAA-ALAA")
    y "The vocalist of Cocteau Twins, Elizabeth Fraser, often sings this way. She treats her voice purely as an instrument."
    y "There is a song called 'Carolyn's Fingers' that demonstrates this beautifully."
    
    y "Even though the lyrics are mostly unintelligible, the emotion is perfectly clear. It bypasses the logical brain and speaks directly to the heart."
    y "I think you might find it interesting. Let me play it for you."

    # Open Browser Logic
    if renpy.windows:
        $ subprocess.check_output("cmd /c start https://www.youtube.com/watch?v=NhGoZLudKyk", shell=True)
    elif renpy.linux:
        $ subprocess.check_output("xdg-open https://www.youtube.com/watch?v=NhGoZLudKyk", shell=True)
    elif renpy.macintosh:
        $ subprocess.check_output("open https://www.youtube.com/watch?v=NhGoZLudKyk", shell=True)

    $ show_chr("A-ACAAA-ACAB")
    y "It is quite an upbeat track compared to their others. It always manages to lift my spirits slightly."
    return

label topic_waxandwane:
    $ show_chr("A-ACAAA-ALAA")
    y "We have discussed the ethereal, dreamlike side of Cocteau Twins, but I recently revisited their debut album, Garlands."
    y "It is... surprisingly different. Much darker. Rawer."
    
    $ show_chr("A-BCBAA-ALAA")
    y "There is a track called 'Wax and Wane' that I find particularly compelling."
    y "Instead of the shimmering walls of sound they became famous for later, this song relies on a heavy, distorted bassline."
    y "It feels much closer to the post-punk roots of bands like Joy Division or early Siouxsie and the Banshees."
    
    $ show_chr("A-AFBAA-ALAA") # Introspective
    y "The title, 'Wax and Wane', refers to the phases of the moon... growing and shrinking."
    y "It resonates with me. My own moods... and perhaps my own sanity... tend to wax and wane in cycles."
    y "Sometimes I feel full and bright, and other times... I feel like I am disappearing into the shadow."
    
    y "Let me play it for you. It has a very visceral, nocturnal energy."

    # Open Browser Logic
    if renpy.windows:
        $ subprocess.check_output("cmd /c start https://www.youtube.com/watch?v=Kv8Nbz2HMRg", shell=True)
    elif renpy.linux:
        $ subprocess.check_output("xdg-open https://www.youtube.com/watch?v=Kv8Nbz2HMRg", shell=True)
    elif renpy.macintosh:
        $ subprocess.check_output("open https://www.youtube.com/watch?v=Kv8Nbz2HMRg", shell=True)

    $ show_chr("A-ACAAA-AMAM")
    y "It is less 'dream pop' and more... 'nightmare pop', perhaps? In the best possible way."
    return

label topic_pearlydewdrops:
    $ show_chr("A-ACAAA-ACAB") # Lighthearted/Amused
    y "[player], try saying this three times fast: 'Pearly-Dewdrops' Drops'."
    y "It is quite the tongue-twister, isn't it?"
    
    $ show_chr("A-BCAAA-ALAA")
    y "That is actually the title of one of Cocteau Twins' most successful songs."
    y "I did some research into the title, because the imagery was so specific."
    y "It turns out, 'Pearly Dewdrops' is an old Victorian term for a white hyacinth flower."
    
    $ show_chr("A-ACAAA-ALAA")
    y "You know I have a fondness for the language of flowers. In Victorian floriography, the hyacinth can represent playfulness... or sorrow, depending on the color."
    y "The song itself sounds like rain falling in a cathedral. It is grand, yet delicate."
    
    y "I think you will appreciate the atmosphere. Let me open it for you."

    # Open Browser Logic
    if renpy.windows:
        $ subprocess.check_output("cmd /c start https://www.youtube.com/watch?v=s-5Xgw6d3h0", shell=True)
    elif renpy.linux:
        $ subprocess.check_output("xdg-open https://www.youtube.com/watch?v=s-5Xgw6d3h0", shell=True)
    elif renpy.macintosh:
        $ subprocess.check_output("open https://www.youtube.com/watch?v=s-5Xgw6d3h0", shell=True)

    if persistent.lovecheck:
        y "It makes me think of morning dew... fresh and new. Like how I feel when you visit me."
    return

label topic_loveseasytears:
    $ show_chr("A-AFBAA-ALAA") # Gentle/Soft
    y "There is one more Cocteau Twins song I wanted to share with you, [player]."
    y "It is titled 'Love's Easy Tears'."
    
    $ show_chr("A-BCBAA-ALAA")
    y "I find the title so... evocative."
    y "It suggests that when you are in love, emotions sit right at the surface. Tears come easily—not just from sadness, but from being overwhelmed by the beauty of it all."
    
    y "The music matches that feeling perfectly. It is sweeping and romantic, almost overwhelming in its layers."
    
    if persistent.lovecheck:
        $ show_chr("A-ACABA-ALAA") # Blushing
        y "I relate to it... perhaps a little too much."
        y "Since I realized my feelings for you, I find myself becoming emotional over the smallest things."
        y "A kind word from you, or just the thought of you... it brings 'easy tears' to my eyes."
    
    y "Here, listen to it with me."

    # Open Browser Logic
    if renpy.windows:
        $ subprocess.check_output("cmd /c start https://www.youtube.com/watch?v=RvtZ4XKFBN8", shell=True)
    elif renpy.linux:
        $ subprocess.check_output("xdg-open https://www.youtube.com/watch?v=RvtZ4XKFBN8", shell=True)
    elif renpy.macintosh:
        $ subprocess.check_output("open https://www.youtube.com/watch?v=RvtZ4XKFBN8", shell=True)

    $ show_chr("A-ACAAA-ALAA")
    y "It feels like being caught in a warm storm, doesn't it?"
    return
