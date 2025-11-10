# This file contains the logic for the "System Heartbeat" feature,
# now with integrated debug messages.

python early:
    # We assume a print_debug function exists, as seen in other files.
    # If not, you can replace print_debug with a simple print().
    if "print_debug" not in globals():
        def print_debug(msg):
            print(msg)

    try:
        import psutil
        psutil_available = True
    except ImportError:
        psutil_available = False
        
    def get_system_heartbeat():
        """Returns a dictionary with CPU usage and includes debug output."""
        if not psutil_available:
            print_debug("System Heartbeat: psutil library not found. Aborting check.")
            return None
            
        cpu_percent = psutil.cpu_percent(interval=0.5)
        result = {"cpu": cpu_percent}

        # --- DEBUG MESSAGE ---
        print_debug("System Heartbeat: CPU check returned {}".format(result))
        
        return result

    def get_laptop_status():
        """Checks for battery status and includes debug output."""
        if not psutil_available:
            print_debug("System Heartbeat: psutil library not found. Aborting check.")
            return None

        battery = psutil.sensors_battery()
        
        if battery:
            result = {
                "is_laptop": True,
                "percent": int(battery.percent),
                "is_charging": battery.power_plugged
            }
        else:
            result = { "is_laptop": False }
        
        # --- DEBUG MESSAGE ---
        print_debug("System Heartbeat: Laptop check returned {}".format(result))

        return result

    def is_in_virtual_machine():
        """Attempts to detect a VM environment and includes debug output."""
        if not psutil_available:
            print_debug("System Heartbeat: psutil library not found. Aborting check.")
            return False
            
        vm_identifiers = ["vmware", "virtualbox", "vbox", "qemu", "xen", "virtual", "hyper-v", "parallels"]
        vm_detected = False
        
        try:
            for part in psutil.disk_partitions():
                for identifier in vm_identifiers:
                    if identifier in part.device.lower():
                        vm_detected = True
                        break
                if vm_detected: break
        except Exception:
            pass

        # --- DEBUG MESSAGE ---
        print_debug("System Heartbeat: VM check returned {}".format(vm_detected))

        return vm_detected

# Add this label at the end of game/features/system_heartbeat.rpy

label debug_heartbeat:
    y "Running direct system heartbeat diagnostics..."
    
    # 1. First and most important check: Is the psutil library loaded?
    if 'psutil_available' in globals() and psutil_available:
        y "Debug: psutil library is loaded successfully. Good."
    else:
        y "CRITICAL ERROR: psutil library is NOT loaded. All checks will fail."
        y "Please verify the 'python-packages' folder and the .whl file installation."
        return

    # 2. Test the VM detection
    $ is_vm_result = is_in_virtual_machine()
    y "VM check returned: [is_vm_result]"

    # 3. Test the laptop/battery detection
    $ laptop_result = get_laptop_status()
    y "Laptop check returned: [laptop_result]"

    # 4. Test the CPU usage detection
    y "Checking CPU for 1 second..."
    $ heartbeat_result = get_system_heartbeat()
    y "Heartbeat check returned: [heartbeat_result]"

    y "Diagnostics complete."
    return
