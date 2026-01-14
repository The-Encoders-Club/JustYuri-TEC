init python:
    import platform
    import sys
    import os

    def get_bsod_style():
        os_name = platform.system()
        
        if os_name == "Windows":
            try:
                win_ver = sys.getwindowsversion()
                
                # Windows 11 24H2 (Build 26100+) -> Modern Black
                if win_ver.major >= 10 and win_ver.build >= 26100:
                    return "win_modern"
                
                # Windows 8, 10, 11 (Pre-24H2) -> Sad Face
                # Windows 8 is Major 6.2 or 6.3
                elif win_ver.major >= 10 or (win_ver.major == 6 and win_ver.minor >= 2):
                    return "win_sad"
                
                # Windows Vista (6.0) & Windows 7 (6.1) -> Consolas Look
                elif win_ver.major == 6 and win_ver.minor <= 1:
                    return "win_7"
                
                # Windows XP (5.1), 2000 (5.0) -> Lucida/Fixedsys Look
                else:
                    return "win_xp"
                    
            except:
                return "win_sad"
                
        elif os_name == "Darwin": 
            return "mac"
        elif os_name == "Linux":
            return "linux"
        
        return "win_sad"

    # Define a variable to hold the font path
    bsod_font_path = "gui/font/lucon.ttf" # Default fallback

    # --- YURI FILE CHECKER ---
    def check_yuri_file_exists():
        try:
            if renpy.android: return False
            basedir = config.basedir
            # Checks game/characters/yuri.chr
            path = os.path.join(basedir, "characters", "yuri.chr")
            return os.path.exists(path)
        except:
            return False

    # --- MEMORY COUNTER ANIMATION ---
    bios_mem_count = 0
    def memory_counter(st, at):
        global bios_mem_count
        # Target: 64GB (65536 MB)
        if bios_mem_count < 65536:
            bios_mem_count += 2048 # Speed up count
            return 0.02
        else:
            bios_mem_count = 65536
            return None
            
    # --- CONSOLE HELPER ---
    bios_console_history = []
    def update_bios_console(txt):
        bios_console_history.append(txt)
        renpy.show_screen("bios_console_display")

# Variables
default bsod_progress = 0
default bios_selection = 0
default bios_recovery_progress = 0
default bsod_dump_count = 0
default bsod_dump_complete = False
