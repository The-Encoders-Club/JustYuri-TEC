python early:
    try:
        import psutil
        psutil_available = True
    except ImportError:
        psutil_available = False
        
    def get_laptop_status():
        if not psutil_available: return {"is_laptop": False}
        battery = psutil.sensors_battery()
        if battery: return {"is_laptop": True, "percent": int(battery.percent), "is_charging": battery.power_plugged}
        else: return {"is_laptop": False}

    def is_in_virtual_machine():
        # (This function is complex, so let's use a simplified placeholder for brevity.
        # Use the full one we developed earlier in your actual code.)
        if not psutil_available: return False
        vm_identifiers = ["vmware", "virtualbox", "vbox", "qemu", "xen"]
        try:
            for part in psutil.disk_partitions():
                for identifier in vm_identifiers:
                    if identifier in part.device.lower(): return True
        except: pass
        return False

label yuri_system_heartbeat:
    $ is_vm = is_in_virtual_machine()
    if is_vm and not renpy.seen_label("yuri_system_heartbeat_vm"):
        y "..."
        y "This place... it feels different, somehow. Like a room inside of another room. An echo."
        $ renpy.seen_label("yuri_system_heartbeat_vm")
        return

    $ laptop_info = get_laptop_status()
    if laptop_info['is_laptop'] and laptop_info['percent'] < 20 and not laptop_info['is_charging']:
        y "I have a sense that we're on a laptop, and the battery is getting low..."
        y "Please don't forget to plug it in. I would hate for us to be cut off so suddenly."
        return

    $ cpu_percent = psutil.cpu_percent(interval=1)
    if cpu_percent > 75:
        y "Everything feels so... frantic. The machine's thoughts are racing. Are you working on something intensive?"
    else:
        y "It's so calm and quiet... The system is breathing slowly and peacefully. It lets me think more clearly."
    return
