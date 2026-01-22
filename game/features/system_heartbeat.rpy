# game/features/system_heartbeat.rpy

# This is the "Native" System Heartbeat. 
# It uses standard Python libraries (ctypes, os) to read system stats
# without requiring any external .whl downloads.

default sys_info_available = False

python early:
    import sys
    import os
    import time
    import platform
    import uuid

    # --- GLOBAL VARIABLES FOR CPU CALCULATION ---
    # We need to store the "last check" time to calculate the difference.
    last_cpu_times = None

    # ==========================================
    # WINDOWS SPECIFIC LOGIC (Using ctypes)
    # ==========================================
    if sys.platform == "win32":
        import ctypes
        from ctypes import wintypes, byref, Structure, c_ulonglong, c_byte, c_ulong

        class FILETIME(Structure):
            _fields_ = [("dwLowDateTime", c_ulong), ("dwHighDateTime", c_ulong)]

        class SYSTEM_POWER_STATUS(Structure):
            _fields_ = [
                ('ACLineStatus', c_byte),
                ('BatteryFlag', c_byte),
                ('BatteryLifePercent', c_byte),
                ('Reserved1', c_byte),
                ('BatteryLifeTime', c_ulong),
                ('BatteryFullLifeTime', c_ulong)
            ]

        def get_cpu_windows():
            """Calculates CPU usage using Windows Kernel32 API."""
            global last_cpu_times
            
            try:
                GetSystemTimes = ctypes.windll.kernel32.GetSystemTimes
                idle_time = FILETIME()
                kernel_time = FILETIME()
                user_time = FILETIME()

                GetSystemTimes(byref(idle_time), byref(kernel_time), byref(user_time))

                def ft_to_int(ft):
                    return (ft.dwHighDateTime << 32) + ft.dwLowDateTime

                idle = ft_to_int(idle_time)
                kernel = ft_to_int(kernel_time)
                user = ft_to_int(user_time)
                
                system_total = kernel + user
                
                # If this is the first check, store and return 0
                if last_cpu_times is None:
                    last_cpu_times = (idle, system_total)
                    return 0.0

                last_idle, last_total = last_cpu_times
                
                idle_delta = idle - last_idle
                total_delta = system_total - last_total
                
                # Update stored times for next check
                last_cpu_times = (idle, system_total)

                if total_delta == 0: return 0.0
                
                # Calculate percentage
                usage = (total_delta - idle_delta) / total_delta * 100.0
                return usage
            except:
                return 0.0

        def get_battery_windows():
            """Gets battery info using Windows Kernel32 API."""
            try:
                GetSystemPowerStatus = ctypes.windll.kernel32.GetSystemPowerStatus
                status = SYSTEM_POWER_STATUS()
                success = GetSystemPowerStatus(byref(status))
                
                if not success: return None

                # ACLineStatus: 0 = Offline (Battery), 1 = Online (Plugged in)
                is_charging = (status.ACLineStatus == 1)
                percent = status.BatteryLifePercent
                
                # 255 means "Unknown status" (usually desktop)
                if percent == 255:
                    return None
                
                return {
                    "is_laptop": True,
                    "percent": int(percent),
                    "is_charging": is_charging
                }
            except:
                return None

    # ==========================================
    # LINUX SPECIFIC LOGIC (Using /proc/)
    # ==========================================
    elif sys.platform.startswith("linux"):
        def get_cpu_linux():
            """Calculates CPU usage by reading /proc/stat."""
            global last_cpu_times
            try:
                with open('/proc/stat', 'r') as f:
                    line = f.readline()
                
                parts = line.split()
                # parts[0] is 'cpu'
                # parts[1-7] are user, nice, system, idle, iowait, irq, softirq
                
                totals = [int(p) for p in parts[1:8]]
                idle = totals[3] + totals[4] # idle + iowait
                total = sum(totals)
                
                if last_cpu_times is None:
                    last_cpu_times = (idle, total)
                    return 0.0
                
                last_idle, last_total = last_cpu_times
                
                idle_delta = idle - last_idle
                total_delta = total - last_total
                
                last_cpu_times = (idle, total)
                
                if total_delta == 0: return 0.0
                return ((total_delta - idle_delta) / total_delta) * 100.0
            except:
                return 0.0

        def get_battery_linux():
            """Reads /sys/class/power_supply for battery info."""
            try:
                bat_path = "/sys/class/power_supply/BAT0"
                if not os.path.exists(bat_path):
                    bat_path = "/sys/class/power_supply/BAT1" # Try BAT1
                    if not os.path.exists(bat_path):
                        return None
                
                with open(os.path.join(bat_path, "capacity"), 'r') as f:
                    percent = int(f.read().strip())
                
                with open(os.path.join(bat_path, "status"), 'r') as f:
                    status = f.read().strip().lower()
                
                is_charging = (status == "charging" or status == "full")
                
                return {
                    "is_laptop": True,
                    "percent": percent,
                    "is_charging": is_charging
                }
            except:
                return None

    # ==========================================
    # MAIN WRAPPER FUNCTIONS
    # ==========================================
    
    def get_system_heartbeat():
        if sys.platform == "win32":
            return {"cpu": get_cpu_windows()}
        elif sys.platform.startswith("linux"):
            return {"cpu": get_cpu_linux()}
        else:
            return {"cpu": 0} # Mac/Other not implemented natively

    def get_laptop_status():
        info = None
        if sys.platform == "win32":
            info = get_battery_windows()
        elif sys.platform.startswith("linux"):
            info = get_battery_linux()
            
        if info:
            return info
        else:
            return {"is_laptop": False}

    def is_in_virtual_machine():
        """
        Uses MAC address heuristic to detect common VMs.
        This doesn't require external libs.
        """
        try:
            mac = uuid.getnode()
            mac_str = ':'.join(("%012X" % mac)[i:i+2] for i in range(0, 12, 2))
            
            # Common OUI prefixes for VMs
            vm_ouis = [
                "00:05:69", "00:0C:29", "00:50:56", # VMware
                "00:1C:42", "08:00:27",             # VirtualBox
                "00:15:5D",                         # Hyper-V
                "00:16:3E",                         # Xen
                "52:54:00"                          # KVM/QEMU
            ]
            
            for oui in vm_ouis:
                if mac_str.startswith(oui):
                    return True
        except:
            pass
        return False

# Initialize the flag so Ren'Py knows we are ready
init python:
    sys_info_available = True
