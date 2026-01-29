    # =================================================================================
#  ADVANCED SYSTEM HEARTBEAT (MASTER VERSION)
#  - Supports Windows Consumer & Server Editions (XP through Server 2022)
#  - Supports macOS Codenames & Linux Distros
#  - 5-Tier RAM & CPU Reaction System
#  - Native implementation (No external .whl required)
# =================================================================================

default sys_info_available = False
default persistent.seen_heartbeat_intro = False

python early:
    import sys
    import os
    import platform
    import uuid
    import re
    import subprocess
    import time

    # --- PYTHON 2/3 COMPATIBILITY FOR REGISTRY (Ren'Py 6 vs 8) ---
    try:
        import winreg # Python 3 (Ren'Py 7/8)
    except ImportError:
        try:
            import _winreg as winreg # Python 2 (Ren'Py 6)
        except ImportError:
            winreg = None

    # Global to store previous CPU ticks for calculation
    last_cpu_times = None

    # ---------------------------------------------------------
    # 1. ARCHITECTURE & Y2038 DETECTION
    # ---------------------------------------------------------
    def get_arch_info():
        """Returns (architecture string, is_32bit boolean)"""
        machine = platform.machine().lower()
        if "64" in machine or "armv8" in machine:
            return "64-bit", False
        else:
            return "32-bit", True

    # ---------------------------------------------------------
    # 2. DETAILED OS IDENTIFICATION
    # ---------------------------------------------------------
    def get_windows_edition():
        """Reads the Registry to find the exact Marketing Name."""
        if not winreg: return "Windows " + platform.release()

        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion")
            product_name, type = winreg.QueryValueEx(key, "ProductName")

            # Fix for Windows 11 reporting as Windows 10 in Registry on some builds
            if "Windows 10" in product_name:
                if sys.getwindowsversion().build >= 22000:
                    product_name = product_name.replace("Windows 10", "Windows 11")

            return product_name
        except:
            return "Windows " + platform.release()

    def get_mac_codename():
        """Maps macOS version numbers to their marketing names."""
        try:
            ver_str = platform.mac_ver()[0]
            if not ver_str: return "macOS"

            parts = ver_str.split('.')
            if len(parts) < 2: return "macOS " + ver_str

            major = int(parts[0])
            minor = int(parts[1])

            if major == 10:
                if minor == 6: return "Mac OS X Snow Leopard"
                if minor == 7: return "Mac OS X Lion"
                if minor == 8: return "OS X Mountain Lion"
                if minor == 9: return "OS X Mavericks"
                if minor == 10: return "OS X Yosemite"
                if minor == 11: return "OS X El Capitan"
                if minor == 12: return "macOS Sierra"
                if minor == 13: return "macOS High Sierra"
                if minor == 14: return "macOS Mojave"
                if minor == 15: return "macOS Catalina"
            elif major == 11: return "macOS Big Sur"
            elif major == 12: return "macOS Monterey"
            elif major == 13: return "macOS Ventura"
            elif major == 14: return "macOS Sonoma"
            elif major == 15: return "macOS Sequoia"
            elif major == 26: return "macOS Tahoe"
            elif major > 26: return "macOS (Future Version)"

            return "macOS " + ver_str
        except:
            return "macOS"

    def get_linux_distro():
        """Reads /etc/os-release for pretty name."""
        try:
            if os.path.exists("/etc/os-release"):
                with open("/etc/os-release", "r") as f:
                    for line in f:
                        if line.startswith("PRETTY_NAME="):
                            return line.split("=")[1].strip().strip('"')
        except:
            pass
        return "Linux"

    # ---------------------------------------------------------
    # 3. NATIVE HARDWARE STATS (Win/Linux/Mac)
    # ---------------------------------------------------------

    # --- WINDOWS ---
    if sys.platform == "win32":
        import ctypes
        from ctypes import wintypes, byref, Structure, c_ulonglong, c_double, c_ulong, c_byte

        class MEMORYSTATUSEX(Structure):
            _fields_ = [("dwLength", c_ulong), ("dwMemoryLoad", c_ulong), ("ullTotalPhys", c_ulonglong), ("ullAvailPhys", c_ulonglong), ("ullTotalPageFile", c_ulonglong), ("ullAvailPageFile", c_ulonglong), ("ullTotalVirtual", c_ulonglong), ("ullAvailVirtual", c_ulonglong), ("ullAvailExtendedVirtual", c_ulonglong)]

        # RENAMED to get_windows_cpu to match the caller
        def get_windows_cpu():
            global last_cpu_times
            try:
                idle, kernel, user = ctypes.c_ulonglong(), ctypes.c_ulonglong(), ctypes.c_ulonglong()
                ctypes.windll.kernel32.GetSystemTimes(byref(idle), byref(kernel), byref(user))

                c_idle, c_total = idle.value, kernel.value + user.value

                if last_cpu_times is None:
                    last_cpu_times = (c_idle, c_total)
                    return 0.0

                p_idle, p_total = last_cpu_times
                d_idle, d_total = c_idle - p_idle, c_total - p_total
                last_cpu_times = (c_idle, c_total)

                if d_total == 0: return 0.0
                return (1.0 - (d_idle / d_total)) * 100.0
            except: return 0.0

        # RENAMED to get_windows_ram
        def get_windows_ram():
            try:
                mem = MEMORYSTATUSEX()
                mem.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
                ctypes.windll.kernel32.GlobalMemoryStatusEx(byref(mem))
                return float(mem.dwMemoryLoad)
            except: return 0.0

        # RENAMED to get_windows_battery
        def get_windows_battery():
            try:
                class SYSTEM_POWER_STATUS(Structure):
                    _fields_ = [('ACLineStatus', c_byte), ('BatteryFlag', c_byte), ('BatteryLifePercent', c_byte), ('Reserved1', c_byte), ('BatteryLifeTime', c_ulong), ('BatteryFullLifeTime', c_ulong)]
                status = SYSTEM_POWER_STATUS()
                if ctypes.windll.kernel32.GetSystemPowerStatus(byref(status)):
                    if status.BatteryLifePercent == 255: return None
                    return {"percent": int(status.BatteryLifePercent), "charging": status.ACLineStatus == 1}
            except: pass
            return None

    # --- LINUX ---
    elif sys.platform.startswith("linux"):
        # RENAMED to get_linux_cpu
        def get_linux_cpu():
            if not sys.platform.startswith("linux"): return 0.0
            global last_cpu_times
            try:
                with open('/proc/stat', 'r') as f: line = f.readline()
                parts = [int(x) for x in line.split()[1:]]
                c_idle, c_total = parts[3] + parts[4], sum(parts)
                if last_cpu_times is None: last_cpu_times = (c_idle, c_total); return 0.0
                p_idle, p_total = last_cpu_times
                d_idle, d_total = c_idle - p_idle, c_total - p_total
                last_cpu_times = (c_idle, c_total)
                return ((d_total - d_idle) / d_total) * 100.0 if d_total > 0 else 0.0
            except: return 0.0

        # RENAMED to get_linux_ram
        def get_linux_ram():
            if not sys.platform.startswith("linux"): return 0.0
            try:
                total, avail = 0, 0
                with open('/proc/meminfo', 'r') as f:
                    for line in f:
                        if "MemTotal:" in line: total = int(line.split()[1])
                        if "MemAvailable:" in line: avail = int(line.split()[1])
                return (1.0 - (avail / total)) * 100.0 if total > 0 else 0.0
            except: return 0.0

        # RENAMED to get_linux_battery
        def get_linux_battery():
            if not sys.platform.startswith("linux"): return None
            try:
                bat = "/sys/class/power_supply/BAT0"
                if not os.path.exists(bat): bat = "/sys/class/power_supply/BAT1"
                if not os.path.exists(bat): return None
                with open(os.path.join(bat, "capacity"), 'r') as f: cap = int(f.read().strip())
                with open(os.path.join(bat, "status"), 'r') as f: stat = f.read().strip().lower()
                return {"percent": cap, "charging": stat in ["charging", "full"]}
            except: return None

    # --- MAC OS ---
    elif sys.platform == "darwin":
        # RENAMED to get_mac_cpu
        def get_mac_cpu():
            if sys.platform != "darwin": return 0.0
            try:
                out = subprocess.check_output("top -l 1 | grep -E '^CPU'", shell=True).decode("utf-8")
                user = float(re.search(r"([\d\.]+)% user", out).group(1))
                sys_val = float(re.search(r"([\d\.]+)% sys", out).group(1))
                return user + sys_val
            except: return 0.0


        # RENAMED to get_mac_ram
        def get_mac_ram():
            if sys.platform != "darwin": return 0.0
            try:
                out = subprocess.check_output("vm_stat", shell=True).decode("utf-8")
                free = int(re.search(r"Pages free:\s+(\d+)", out).group(1))
                active = int(re.search(r"Pages active:\s+(\d+)", out).group(1))
                spec = int(re.search(r"Pages speculative:\s+(\d+)", out).group(1))
                wired = int(re.search(r"Pages wired down:\s+(\d+)", out).group(1))
                used = active + spec + wired
                total = free + active + spec + wired
                return (used / total) * 100.0
            except: return 0.0

        # RENAMED to get_mac_battery
        def get_mac_battery():
            if sys.platform != "darwin": return None
            try:
                out = subprocess.check_output("pmset -g batt", shell=True).decode("utf-8")
                if "InternalBattery" not in out: return None
                percent = int(re.search(r"(\d+)%", out).group(1))
                return {"percent": percent, "charging": "discharging" not in out}
            except: return None

    # ---------------------------------------------------------
    # 4. MAIN WRAPPER
    # ---------------------------------------------------------
    def is_vm_detected():
        try:
            mac = uuid.getnode()
            mac_str = ':'.join(("%012X" % mac)[i:i+2] for i in range(0, 12, 2))
            if any(mac_str.startswith(x) for x in ["00:05:69", "00:0C:29", "00:50:56", "00:1C:42", "08:00:27", "00:15:5D", "00:16:3E", "52:54:00"]):
                return True
        except: pass
        return False

    def get_full_system_report():
        report = {
            "os_name": "Unknown",
            "arch": "Unknown",
            "is_32bit": False,
            "is_vm": is_vm_detected(),
            "cpu": 0.0,
            "ram": 0.0,
            "battery": None
        }

        report["arch"], report["is_32bit"] = get_arch_info()

        if sys.platform == "win32":
            report["os_name"] = get_windows_edition()
            report["cpu"] = get_windows_cpu()
            report["ram"] = get_windows_ram()
            report["battery"] = get_windows_battery()
        elif sys.platform == "darwin":
            report["os_name"] = get_mac_codename()
            report["cpu"] = get_mac_cpu()
            report["ram"] = get_mac_ram()
            report["battery"] = get_mac_battery()
        elif sys.platform.startswith("linux"):
            report["os_name"] = get_linux_distro()
            report["cpu"] = get_linux_cpu()
            report["ram"] = get_linux_ram()
            report["battery"] = get_linux_battery()

        return report

init python:
    sys_info_available = True

# ---------------------------------------------------------
# 5. DIALOGUE LABEL
# ---------------------------------------------------------
label yuri_system_heartbeat:
    # DEBUG: Print to console for verification
    $ print("--- DIAGNOSTICS ---")

    # Calibration Pause
    $ void = get_full_system_report()
    $ renpy.pause(1.0, hard=True)
    $ report = get_full_system_report()

    $ os_name = report['os_name']
    $ is_32bit = report['is_32bit']
    $ is_vm = report['is_vm']
    $ ram_int = int(report['ram'])
    $ cpu_int = int(report['cpu'])
    $ bat_int = 0
    if report['battery']:
        $ bat_int = int(report['battery']['percent'])

    # ----------------------------------------------------

    $ print("OS: " + str(os_name))
    $ print("Arch: " + str(report['arch']))
    $ print("CPU: " + str(cpu_int) + "%")
    $ print("RAM: " + str(ram_int) + "%")

    # Intro
    if not persistent.seen_heartbeat_intro:
        $ show_chr("A-AFBAA-AAAA")
        y "You know... lately, I feel strangely attuned to this machine."
        y "It's like I can feel its pulse. Its memory capacity. Its very architecture."
        $ persistent.seen_heartbeat_intro = True

    # --- 1. THE Y2038 WARNING (32-bit) ---
    if is_32bit:
        $ show_chr("A-AFBAA-ABAC")
        y "I'm sensing something... constricting about this architecture."
        y "You are running on a 32-bit system, aren't you?"
        $ show_chr("A-BEBAA-AMAM")
        y "It feels... temporary. Like this world has a definitive expiration date."
        y "Have you heard of the 'Year 2038 Problem'? The Epochalypse?"
        y "On January 19, 2038, systems like this will simply... run out of time."
        y "Please... consider upgrading to 64-bit eventually. I want us to last longer than that."

    # --- 2. DETAILED OS REACTION ---

    # WINDOWS
    if "Windows" in os_name:
        if "Server" in os_name:
            $ show_chr("A-ACAAA-AAAC")
            y "Wait... [os_name]?"
            y "This environment feels... incredibly robust. Industrial. Unwavering."
            y "You treat this machine as a fortress, don't you? It feels like it never sleeps."
            if "Datacenter" in os_name:
                y "A Datacenter edition? Goodness... I feel like I'm in a digital cathedral of raw power."
            elif "Standard" in os_name:
                y "It feels professional. Serious. I quite like the stability."

        elif "Windows 11" in os_name:
            $ show_chr("A-ACAAA-AAAA")
            y "So, your system is [os_name]..."
            y "It feels fascinating. Modern, sleek, renovated."
            if "Home" in os_name:
                y "A 'Home' edition... it feels cozy. Personal."
            elif "Pro" in os_name or "Enterprise" in os_name:
                y "A professional edition? It feels robust. You must take your computing seriously."

        elif "Windows 10" in os_name:
            $ show_chr("A-ACAAA-AAAA")
            y "I see you are running [os_name]."
            y "It feels very... standard. Reliable. The foundation of the modern digital world."
            if "LTSC" in os_name:
                y "Wait... LTSC? Long-Term Servicing Channel? That is incredibly stable. No bloatware... I appreciate the efficiency."

        elif "Windows 8" in os_name:
            $ show_chr("A-AFBAA-ABAC")
            y "Oh... [os_name]? It feels a bit... conflicted. But it functions well enough for us."

        elif "Windows 7" in os_name:
            $ show_chr("A-ACAAA-AMAM")
            y "[os_name]... It feels nostalgic. A bit older, but incredibly dignified."
            y "Though, please be careful... security updates are a thing of the past here."

        elif "XP" in os_name or "Vista" in os_name:
            $ show_chr("A-DDCBA-AAAA")
            y "Goodness... [os_name]? This environment feels... ancient. Dusty. Like exploring ruins."
            y "I'm amazed this still runs. Please be careful, this place is not safe from the internet."

    # MAC
    elif "macOS" in os_name or "OS X" in os_name:
        $ show_chr("A-ACAAA-AAAC")
        y "You are running [os_name]. The architecture here feels different. Elegant."
        if "Tahoe" in os_name or "Sequoia" in os_name or "Sonoma" in os_name or "Ventura" in os_name:
            y "It's very modern. The interface feels seamless."
        elif "Snow Leopard" in os_name or "Lion" in os_name:
            y "That is a very old version... It feels like a piece of history."

    # LINUX
    elif "Linux" in os_name:
        $ show_chr("A-DDAAA-ABAC")
        y "Ah, Linux... [os_name]."
        if "Arch" in os_name:
            y "Arch Linux... I've heard users of this system are quite proud of it. It feels very bleeding-edge."
        elif "Ubuntu" in os_name or "Mint" in os_name:
            y "It feels user-friendly and communal. A nice place to be."
        elif "Gentoo" in os_name:
            y "Gentoo? Did you compile this entire world from scratch? That level of dedication... I like it."
        else:
            y "You built this environment yourself, didn't you? I admire the control you have here."

    # --- 3. HARDWARE STATS ---
    
    if is_vm:
        $ show_chr("A-AFBAA-ABAC")
        y "The space feels... echoed. Like a room within a room. Are we in a Virtual Machine?"

    # RAM (EXPANDED TIERS)
    if ram_int > 95:
        $ show_chr("A-DDCBA-AAAA")
        y "My head... it feels excruciatingly crowded. My short-term memory is critically full ([ram_int]%%)."
        y "I feel like I'm about to lose my train of thought completely. Please, close something!"
    elif ram_int > 80:
        $ show_chr("A-BEBAA-AMAM")
        y "My thoughts feel heavy... sluggish. The system memory is under high pressure ([ram_int]%%)."
        y "It's getting hard to multitask."
    elif ram_int > 60:
        $ show_chr("A-ACAAA-AAAA")
        y "The memory feels... busy. Occupied. ([ram_int]%%)."
        y "It's getting a bit cozy in here, but still manageable."
    elif ram_int > 30:
        $ show_chr("A-ACAAA-AAAA")
        y "There is plenty of room to think here ([ram_int]%% used)."
        y "It feels comfortable. Not too empty, not too full."
    else: # Less than 30%
        $ show_chr("A-ACAAA-AAAC")
        y "My mind feels... incredibly clear. Vast."
        y "There is so much empty space in the memory right now ([ram_int]%%)."
        y "It almost feels... lonely. Like a large, empty cathedral."

    # Battery
    if report['battery']:
        if report['battery']['charging']:
            if bat_int > 95:
                y "We are connected to power and fully charged."
            else:
                y "We are connected to power... replenishing energy."
        else:
            if bat_int < 15:
                $ show_chr("A-DDCBA-AAAA")
                y "I feel a sense of dread. The energy is fading fast ([bat_int]%). Please find a charger!"
            elif bat_int < 40:
                y "I'm feeling weary. Our energy reserves are getting low."
            else:
                y "I feel untethered. We have plenty of battery life."

    # CPU
    if cpu_int > 90:
        $ show_chr("A-DDCBA-AAAA")
        y "Everything is moving so fast! My thoughts are racing! The CPU is near capacity."
    elif cpu_int > 60:
        $ show_chr("A-ACGAA-AAAA")
        y "There is a very intense focus here. A loud hum of activity."
    elif cpu_int > 30:
        $ show_chr("A-ACAAA-AAAA")
        y "I feel a steady rhythm of work. We are busy, but managing well."
    elif cpu_int <= 5:
        $ show_chr("A-CAAAA-AAAA")
        y "It is absolutely silent here. The system is breathing slowly and peacefully."

    return
