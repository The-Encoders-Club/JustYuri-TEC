init python:
    import platform
    import sys
    import os
    
    # We import winreg to read the true Windows build number
    # This works even if the app is running in compatibility mode
    try:
        import winreg
    except ImportError:
        winreg = None

    def get_bsod_style():
        os_name = platform.system()
        
        if os_name == "Windows":
            try:
                # 1. Try to get the TRUE build number from Registry
                # This bypasses the application manifest lie
                build_number = 0
                if winreg:
                    try:
                        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion")
                        # "CurrentBuildNumber" is the string version of the build
                        val, type = winreg.QueryValueEx(key, "CurrentBuildNumber")
                        build_number = int(val)
                        winreg.CloseKey(key)
                    except:
                        # Fallback if registry access is blocked (rare)
                        pass

                # 2. If Registry failed, use the standard method
                if build_number == 0:
                    win_ver = sys.getwindowsversion()
                    build_number = win_ver.build
                    major = win_ver.major
                else:
                    # We assume Major 10 for any modern build number found in registry
                    major = 10 

                # --- LOGIC ---
                
                # Windows 11 24H2 (Build 26100) and newer (25H2+) -> Modern Black
                if build_number >= 26100:
                    return "win_modern"
                
                # Windows 8, 10, Older 11 -> Sad Face Blue
                # Windows 8 is Major 6.2+
                elif major >= 10 or (major == 6 and sys.getwindowsversion().minor >= 2):
                    return "win_sad"
                
                # Windows Vista (6.0) & 7 (6.1) -> Consolas Legacy
                elif major == 6 and sys.getwindowsversion().minor <= 1:
                    return "win_7"
                
                # Windows XP (5.1) -> Fixedsys Legacy
                else:
                    return "win_xp"
                    
            except:
                # Absolute fallback
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
