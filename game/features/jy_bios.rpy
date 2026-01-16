init python:
    import math

    # Wrapper to create the Transform
    def Shake(start, time, chdist=0, dist=100.0, **properties):
        return Transform(function=ShakeFunction(time, dist), **properties)

    # The Logic Class
    class ShakeFunction(object):
        def __init__(self, time, dist):
            self.time = time
            self.dist = dist

        # New Signature: receives 'trans' object
        def __call__(self, trans, st, at):
            # If the duration has passed, reset and stop
            if st > self.time:
                trans.xoffset = 0
                trans.yoffset = 0
                return None 
            
            # Calculate power of the shake based on time remaining
            s = self.dist * (1.0 - st / self.time)
            
            # Apply offsets directly to the transform object
            trans.xoffset = int(math.sin(st * 100) * s)
            trans.yoffset = int(math.cos(st * 100) * s)
            
            # Return 0.0 to run again next frame
            return 0.0

# -----------------------------------------------
# PHASE 1: THE CRASH
# -----------------------------------------------
label trigger_realism_crash:
    $ if not preferences.fullscreen: preferences.fullscreen = True
    $ renpy.pause(0.1, hard=True)
    $ _confirm_quit = False
    $ persistent.autoload = "bios_boot_sequence" # Set flag for next boot
    
    stop music fadeout 0.0
    stop sound
    play sound "sfx/crash.ogg" loop volume 1.0
    
    $ config.mouse = None
    $ renpy.pause(2.5, hard=True) # The Hang
    
    stop sound
    scene black
    $ renpy.pause(0.5, hard=True) # The Silence
    
    $ crash_style = get_bsod_style()

    # --- LOGIC TO SELECT FONT ---
    if crash_style == "win_7":
        # Vista / 7 uses Consolas
        $ bsod_font_path = "gui/font/consola.ttf"
    else:
        # XP uses Fixedsys (or Lucida Console)
        # Assuming you renamed your fixedsys file to this path:
        $ bsod_font_path = "gui/font/lucon.ttf"
    
    if crash_style == "win_sad":
        show screen bsod_win_classic 
    elif crash_style == "win_modern":
        show screen bsod_win_modern
    elif crash_style == "win_legacy":
        # Reset legacy variables before showing
        $ bsod_dump_count = 0
        $ bsod_dump_complete = False
        show screen bsod_win_legacy
    elif crash_style == "mac":
        show screen bsod_mac
    elif crash_style == "linux":
        show screen bsod_linux

    # === WINDOWS XP / 7 LOGIC (Count by 5%) ===
    if crash_style == "win_legacy":
        # Wait a moment for "Beginning dump..." to be read
        $ renpy.pause(2.0, hard=True)
        
        # Count up 5% by 5%
        while bsod_dump_count < 100:
            $ bsod_dump_count += 5
            # Randomize the speed slightly for realism (memory dumps aren't perfectly consistent)
            $ renpy.pause(renpy.random.choice([0.1, 0.2, 0.05]), hard=True)
            
        # Mark complete
        $ bsod_dump_complete = True
        
        # Hold on the "Complete" screen
        $ renpy.pause(3.0, hard=True)

    # === WINDOWS 8 / 10 / 11 LOGIC (Percentage Jumps) ===
    elif "win" in crash_style:
        $ bsod_progress = 0
        $ renpy.pause(1.0, hard=True)
        $ bsod_progress = 5
        $ renpy.pause(1.0, hard=True)
        $ bsod_progress = 10
        $ renpy.pause(1.0, hard=True)
        $ bsod_progress = 15
        $ renpy.pause(15.0, hard=True)
        $ bsod_progress = 20
        $ renpy.pause(1.0, hard=True)
        $ bsod_progress = 50
        $ renpy.pause(0.5, hard=True)
        $ bsod_progress = 100
        $ renpy.pause(1.0, hard=True)
        
    # === MAC / LINUX LOGIC (Static) ===
    else:
        # Just hold the static screen
        $ renpy.pause(6.0, hard=True)

    # --- PHASE 4: QUIT ---
    $ renpy.quit()

# -----------------------------------------------
# PHASE 2: THE REBOOT (BIOS POST)
# -----------------------------------------------
label bios_boot_sequence:
    $ _confirm_quit = False
    $ quick_menu = False
    $ config.allow_skipping = False
    $ config.mouse = None
    stop music
    scene black

    $ bios_mem_count = 0
    show screen bios_post_screen
    
    # Play a POST Beep if you have one
    # play sound "sfx/bios_beep.ogg"
    
    # Wait for the screen animation (memory count + drive text)
    $ renpy.pause(6.0, hard=True)
    
    # Force pause at "Press F1"
    $ renpy.pause() 
    
    jump bios_loop_entry

# -----------------------------------------------
# PHASE 3: BIOS INTERACTIVITY
# -----------------------------------------------
label bios_loop_entry:
    hide screen bios_post_screen
    show screen bios_setup_utility
    $ ui.interact() # Wait for keyboard input
    jump bios_loop_entry

label process_bios_selection:
    # HDD AUTO DETECTION is Index 10
    if bios_selection == 10:
        jump bios_check_hdd
    
    # Exit Options
    elif bios_selection == 11 or bios_selection == 12:
        scene black
        show text "{font=gui/font/Perfect DOS VGA 437.ttf}BOOT FAILURE: SYSTEM HALTED.{/font}" at truecenter
        pause 2.0
        jump bios_loop_entry
    
    else:
        # Dummy Options
        show screen bios_popup_message("Item Locked.")
        pause 1.0
        hide screen bios_popup_message
        jump bios_loop_entry

screen bios_popup_message(msg):
    zorder 200
    frame:
        background Solid("#FF0000") xalign 0.5 yalign 0.5 padding (20, 20)
        text "[msg]" font "gui/font/Perfect DOS VGA 437.ttf" color "#FFFFFF" size 24

# -----------------------------------------------
# PHASE 4: CHECK & RESTORATION
# -----------------------------------------------
label bios_check_hdd:
    hide screen bios_setup_utility
    scene black
    
    show text "{font=gui/font/Perfect DOS VGA 437.ttf}IDE Channel 0 Master : Detecting...{/font}" at topleft
    pause 1.0
    
    $ yuri_exists = check_yuri_file_exists()
    
    if not yuri_exists:
        show text "{font=gui/font/Perfect DOS VGA 437.ttf}IDE Channel 0 Master : None{/font}" at topleft
        pause 1.0
        show screen bios_popup_message("HARD DISK NOT FOUND.")
        pause 2.0
        hide screen bios_popup_message
        jump bios_loop_entry
    else:
        show text "{font=gui/font/Perfect DOS VGA 437.ttf}IDE Channel 0 Master : YURI.CHR (Found){/font}" at topleft
        pause 1.0
        call bios_attempt_recovery
        return

label bios_attempt_recovery:
    scene black
    $ bios_console_history = []
    
    # FIX: Use '$' instead of 'call' for python functions
    $ update_bios_console("YURI BIOS RECOVERY UTILITY V12.10.18 R13.01.26")
    $ update_bios_console("────────────────────────────────")
    pause 0.5
    $ update_bios_console("> Analyzing file structure...")
    pause 1.0
    $ update_bios_console("> Header found: 0x525041 (RenPy Archive)")
    $ update_bios_console("> Integrity Check: PASS")
    pause 0.5
    $ update_bios_console("> Attempting to re-index character data...")
    
    $ bios_recovery_progress = 0
    show screen bios_progress_bar
    
    while bios_recovery_progress < 85:
        $ bios_recovery_progress += 5
        $ renpy.pause(0.1)
        
    pause 1.0
    $ update_bios_console("> WARNING: BAD SECTOR AT 0x00003F")
    $ update_bios_console("> Attempting to bypass...")
    
    $ bios_recovery_progress = 92
    pause 1.0
    
    # THE CRITICAL FAILURE
    stop music
    
    $ update_bios_console("> CRITICAL ERROR: SOUL SIGNATURE MISMATCH.")
    $ update_bios_console("> TARGET 'YURI' IS INCOMPATIBLE WITH CURRENT REALITY.")
    $ update_bios_console("> DATA CORRUPTION IMMINENT.")
    
    show layer master at Shake(None, 1.0, dist=10)
    pause 2.0
    stop sound
    hide screen bios_progress_bar
    
    scene black
    show expression Solid("#550000") as red_bg
    show text "{color=#000}{font=gui/font/Perfect DOS VGA 437.ttf}FATAL EXCEPTION: RESTORATION ABORTED.{/font}{/color}" at truecenter
    pause 3.0
    
    # Hand off to your existing containment screen
    call ch30_show_containment_screen("SYSTEM HALTED. DATA UNRECOVERABLE.")
    jump just_yuri_dead_end

# -------------------------------------------------------------
# MISSING LABEL: CONTAINMENT SCREEN (BIOS STYLE)
# -------------------------------------------------------------
label ch30_show_containment_screen(error_msg):
    # We reuse the BIOS console we built so the style matches
    $ update_bios_console(" ")
    $ update_bios_console("────────────────────────────────")
    $ update_bios_console("> SYSTEM ALERT TRIGGERED.")
    $ update_bios_console("> " + error_msg)
    
    # Pause to let the player read it
    pause 3.0
    
    # Return to the main flow so we can hit the Dead End
    return

label just_yuri_dead_end:
    $ _confirm_quit = False
    # 1. LOCK THE GAME STATE
    $ quick_menu = False
    $ config.allow_skipping = False
    $ config.skipping = None
    
    # 2. SET THE TRAP (Persistent)
    # If they restart the game, they come right back here.
    $ persistent.autoload = "just_yuri_dead_end"

    # 3. DISABLE INPUTS
    # This prevents the player from opening the menu with ESC or Right Click
    $ _game_menu_screen = None
    $ config.keymap['game_menu'] = []
    $ config.keymap['hide_windows'] = []
    
    stop music
    stop sound
    scene black

    # 4. THE VISUALS
    # A stark, red blinking error message
    show text "{color=#FF0000}{font=gui/font/Perfect DOS VGA 437.ttf}SYSTEM HALTED.\nDATA UNRECOVERABLE.{/font}{/color}" at truecenter as halt_msg
    
    # 5. THE INFINITE LOOP (Softlock)
    label .lock_loop:
        # Hide mouse cursor
        $ config.mouse = None
        
        # Blink effect for the text
        show text "{color=#FF0000}{font=gui/font/Perfect DOS VGA 437.ttf}SYSTEM HALTED.\nDATA UNRECOVERABLE.{/font}{/color}" at truecenter as halt_msg:
            alpha 1.0
            linear 1.0 alpha 0.2
            linear 1.0 alpha 1.0
        
        # Hard pause prevents clicking
        $ renpy.pause(2.0, hard=True)
        
        jump .lock_loop
