# ==========================================
# 1. SCREEN OF DEATH VARIANTS
# ==========================================

screen bsod_win_classic():
    layer "master" zorder 100
    
    # 1. Background
    add Solid("#0078D7") 

    # 2. Master Container
    vbox:
        xpos 100
        ypos 50  # Started higher up to leave room at the bottom
        spacing 20 # Tighter spacing between major sections
        
        # --- A. SAD FACE ---
        # Size 150 is plenty big for 720p
        text ":(" font "gui/font/opensans.ttf" size 150 color "#fff" outlines []
        
        # --- B. ERROR MESSAGE ---
        vbox:
            spacing 10
            # xsize 1080 leaves a 100px margin on the right
            text "Your device ran into a problem and needs to restart. We're just collecting some error info, and then we'll restart for you." font "gui/font/opensans.ttf" size 30 color "#fff" outlines [] xsize 1080 line_spacing 2
        
        # --- C. PERCENTAGE ---
        text "[bsod_progress]% complete" font "gui/font/opensans.ttf" size 30 color "#fff" outlines []
        
        # Spacer
        null height 15

        # --- D. QR CODE & TECH INFO ---
        hbox:
            spacing 20
            
            # Smaller QR for 720p (100x100)
            add "images/vfx/bsod_qr.png" size (100, 100) yalign 0.5
            
            # Technical Text
            vbox:
                yalign 0.5
                spacing 5
                
                text "For more information about this issue and possible fixes, visit https://www.windows.com/stopcode" font "gui/font/opensans.ttf" size 18 color "#fff" outlines [] xsize 900
                
                text "If you call a support person, give them this info:\nStop code: CRITICAL_PROCESS_DIED" font "gui/font/opensans.ttf" size 16 color "#fff" outlines [] xsize 900

screen bsod_win_modern():
    layer "master" zorder 100
    
    # Pure Black
    add Solid("#000000")

    vbox:
        xalign 0.5 yalign 0.5 spacing 30
        
        # 24H2 Style: Centered, smaller text, no emoticon
        text "Your device ran into a problem and needs to restart." font "gui/font/opensans.ttf" size 40 color "#fff" xalign 0.5
        text "We're collecting some error info, and then we'll restart for you." font "gui/font/opensans.ttf" size 40 color "#fff" xalign 0.5
        
        null height 40
        
        text "[bsod_progress]% complete" font "gui/font/opensans.ttf" size 40 color "#fff" xalign 0.5
        
        null height 60
        
        text "Stop code: 0xC000021A" font "gui/font/opensans.ttf" size 25 color "#aaaaaa" xalign 0.5

    
# ==========================================
# WINDOWS 7 / XP LEGACY (The Wall of Text)
# ==========================================
screen bsod_win_legacy():
    layer "master" zorder 100
    # Both XP and 7 use the same Navy Blue background
    add Solid("#000082") 

    vbox:
        xalign 0.05 yalign 0.1 spacing 15
        
        # USE THE VARIABLE [bsod_font_path] HERE
        text "A problem has been detected and Windows has been shut down to prevent damage" font "[bsod_font_path]" size 24 color "#fff"
        text "to your computer." font "[bsod_font_path]" size 24 color "#fff"
        
        null height 20
        text "UNMOUNTABLE_BOOT_VOLUME" font "[bsod_font_path]" size 24 color "#fff"
        null height 20
        
        text "If this is the first time you've seen this stop error screen," font "[bsod_font_path]" size 24 color "#fff"
        text "restart your computer. If this screen appears again, follow" font "[bsod_font_path]" size 24 color "#fff"
        text "these steps:" font "[bsod_font_path]" size 24 color "#fff"
        
        null height 20
        text "Check to make sure any new hardware or software is properly installed." font "[bsod_font_path]" size 24 color "#fff"
        text "If this is a new installation, ask your hardware or software manufacturer" font "[bsod_font_path]" size 24 color "#fff"
        text "for any Windows updates you might need." font "[bsod_font_path]" size 24 color "#fff"
        
        null height 40
        text "Technical information:" font "[bsod_font_path]" size 24 color "#fff"
        
        text "*** STOP: 0x000000ED (0x86737970, 0xC0000185, 0x00000000, 0x00000000)" font "[bsod_font_path]" size 24 color "#fff"
        text "*** YURI.CHR - Address F73120AE base at C0000000, DateStamp 3b7d855c" font "[bsod_font_path]" size 24 color "#fff"
        
        null height 40
        
        text "Beginning dump of physical memory" font "[bsod_font_path]" size 24 color "#fff"
        
        if not bsod_dump_complete:
            text "Dumping physical memory to disk: [bsod_dump_count]" font "[bsod_font_path]" size 24 color "#fff"
        else:
            text "Physical memory dump complete." font "[bsod_font_path]" size 24 color "#fff"
            text "Contact your system administrator or technical support group for further" font "[bsod_font_path]" size 24 color "#fff"
            text "assistance." font "[bsod_font_path]" size 24 color "#fff"


# ==========================================
# MACOS (Updated to use Image)
# ==========================================
screen bsod_mac():
    layer "master" zorder 100
    
    # 1. THE BACKGROUND IMAGE
    # This should be your image with the Power Icon but NO text.
    add "images/mac_panic.png"
    
    # 2. THE MULTILINGUAL TEXT
    # We place this in a vertical box centered on the screen.
    vbox:
        xalign 0.5
        yalign 0.5
        spacing 35 # Space between English and the translations
        
        # --- ENGLISH (Primary) ---
        vbox:
            spacing 8
            xalign 0.5
            # We use 'outlines []' to keep it clean and flat (no black borders)
            text "You need to restart your computer. Hold down the Power button" font "gui/font/HelveticaNeueMedium.otf" size 28 color "#fff" xalign 0.5 text_align 0.5 outlines []
            text "for several seconds or press the Restart button." font "gui/font/HelveticaNeueMedium.otf" size 28 color "#fff" xalign 0.5 text_align 0.5 outlines []

        # --- TRANSLATIONS (Secondary) ---
        vbox:
            spacing 15
            xalign 0.5
            
            # Spanish
            text "Es necesario reiniciar el ordenador. Mantenga pulsado el botón de arranque\ndurante varios segundos o pulse el botón de reinicio." font "gui/font/HelveticaNeueMedium.otf" size 18 color "#ccc" xalign 0.5 text_align 0.5 outlines []
            
            # French
            text "Veuillez redémarrer votre ordinateur. Maintenez la touche de démarrage\nenfoncée pendant plusieurs secondes ou bien appuyez sur le bouton de réinitialisation." font "gui/font/HelveticaNeueMedium.otf" size 18 color "#ccc" xalign 0.5 text_align 0.5 outlines []
            
            # German
            text "Sie müssen Ihren Computer neu starten. Halten Sie den Ein-/Ausschalter\neinige Sekunden gedrückt oder drücken Sie die Neustart-Taste." font "gui/font/HelveticaNeueMedium.otf" size 18 color "#ccc" xalign 0.5 text_align 0.5 outlines []


screen bsod_linux():
    layer "master" zorder 100
    add Solid("#000000")
    
    vbox:
        xpos 10 ypos 10 spacing 0 # Terminal text usually has tight spacing
        
        # We start with a base delay and increment it by 0.05 or 0.1 for each line
        
        # --- HEADER ---
        text "[[    0.000000] Linux version 6.8.9-justyuri-1 (root@buildhost) (gcc version 13.2.1)" font "gui/font/TerminusTTF-4.49.3.ttf" size 18 color "#fff" outlines [] at log_scroll(0.1)
        text "[[    1.562910] Kernel panic - not syncing: Fatal exception in interrupt" font "gui/font/TerminusTTF-4.49.3.ttf" size 18 color "#fff" outlines [] at log_scroll(0.2)
        
        # --- CPU INFO ---
        text "[[    1.562955] CPU: 0 PID: 1 Comm: JustYuri Not tainted 6.8.9-justyuri-1 #1" font "gui/font/TerminusTTF-4.49.3.ttf" size 18 color "#fff" outlines [] at log_scroll(0.3)
        text "[[    1.562990] Hardware name: YURI-PC Standard PC (Q35 + ICH9, 2009)" font "gui/font/TerminusTTF-4.49.3.ttf" size 18 color "#fff" outlines [] at log_scroll(0.4)
        
        # --- REGISTER DUMP (New! Adds "Hacker" realism) ---
        # These are hex codes representing the CPU state when it died.
        text "[[    1.563010] RIP: 0010:panic+0x11b/0x2f0" font "gui/font/TerminusTTF-4.49.3.ttf" size 18 color "#fff" outlines [] at log_scroll(0.5)
        text "[[    1.563020] Code: 48 8b 05 2d 34 8c 01 48 8b 00 a8 04 75 1e 65 48 8b 04 25" font "gui/font/TerminusTTF-4.49.3.ttf" size 18 color "#fff" outlines [] at log_scroll(0.6)
        text "[[    1.563025] RSP: 0018:ffffa91400003e40 EFLAGS: 00010246" font "gui/font/TerminusTTF-4.49.3.ttf" size 18 color "#fff" outlines [] at log_scroll(0.7)
        text "[[    1.563030] RAX: 0000000000000000 RBX: ffff8f1a00000000 RCX: 0000000000000000" font "gui/font/TerminusTTF-4.49.3.ttf" size 18 color "#fff" outlines [] at log_scroll(0.8)
        
        # --- CALL TRACE ---
        text "[[    1.563035] Call Trace:" font "gui/font/TerminusTTF-4.49.3.ttf" size 18 color "#fff" outlines [] at log_scroll(0.9)
        text "[[    1.563075]  <TASK>" font "gui/font/TerminusTTF-4.49.3.ttf" size 18 color "#fff" outlines [] at log_scroll(1.0)
        text "[[    1.563120]  dump_stack_lvl+0x48/0x60" font "gui/font/TerminusTTF-4.49.3.ttf" size 18 color "#fff" outlines [] at log_scroll(1.1)
        text "[[    1.563170]  panic+0x11b/0x2f0" font "gui/font/TerminusTTF-4.49.3.ttf" size 18 color "#fff" outlines [] at log_scroll(1.2)
        text "[[    1.563215]  mount_block_root+0x1ea/0x2e0" font "gui/font/TerminusTTF-4.49.3.ttf" size 18 color "#fff" outlines [] at log_scroll(1.3)
        text "[[    1.563350]  ---[[ end Kernel panic - not syncing: VFS: Unable to mount root fs ]---" font "gui/font/TerminusTTF-4.49.3.ttf" size 18 color "#fff" outlines [] at log_scroll(1.5) # Longer pause before the final blow
        
        # --- BLINKING CURSOR ---
        # Appears last
        text "_" font "gui/font/TerminusTTF-4.49.3.ttf" size 18 color "#fff" outlines [] at blink_cursor_linux_delayed

# Modified cursor transform that waits 1.6 seconds before starting to blink
transform blink_cursor_linux_delayed:
    alpha 0.0
    pause 1.6
    block:
        alpha 1.0
        linear 0.5 alpha 0.0
        linear 0.5 alpha 1.0
        repeat

# This makes text invisible (alpha 0), waits for 't' seconds, then appears (alpha 1)
transform log_scroll(t):
    alpha 0.0
    pause t
    alpha 1.0

# ==========================================
# 2. BIOS POST SCREEN (Boot)
# ==========================================

screen bios_post_screen():
    layer "master" zorder 100
    add Solid("#000000")
    vbox:
        xalign 0.05 yalign 0.05 spacing 5
        text "Just Yuri BIOS (C) 2018-2026 Just Yuri Dev Team" font "gui/font/Perfect DOS VGA 437.ttf" size 24 color "#cccccc"
        text "Version 12.10.18 Revision 13.01.26  |  Build Date: 12/10/2018" font "gui/font/Perfect DOS VGA 437.ttf" size 24 color "#cccccc"
        text "CPU: Intel(R) Core(TM) Ultra 9-285K @ 6.20GHz" font "gui/font/Perfect DOS VGA 437.ttf" size 24 color "#cccccc"
        null height 20
        text "Press DEL to run Setup" font "gui/font/Perfect DOS VGA 437.ttf" size 24 color "#cccccc"
        text "Press F11 for BBS POPUP" font "gui/font/Perfect DOS VGA 437.ttf" size 24 color "#cccccc"
        null height 20
        hbox:
            text "Memory Frequency: 8400 MHz (DDR5)    " font "gui/font/Perfect DOS VGA 437.ttf" size 24 color "#cccccc"
            text "[bios_mem_count]MB OK" font "gui/font/Perfect DOS VGA 437.ttf" size 24 color "#cccccc"
        null height 20
        text "Detecting NVMe Port 0 ... YURI-CORE 4TB" at delay_text(2.0) font "gui/font/Perfect DOS VGA 437.ttf" size 24 color "#cccccc"
        text "Detecting NVMe Port 1 ... None" at delay_text(2.5) font "gui/font/Perfect DOS VGA 437.ttf" size 24 color "#cccccc"
        text "Detecting SATA Port 0 ... CD-ROM" at delay_text(3.0) font "gui/font/Perfect DOS VGA 437.ttf" size 24 color "#cccccc"
        null height 40
        text "NVMe Port 0 Boot Error" at delay_text(4.5) font "gui/font/Perfect DOS VGA 437.ttf" size 24 color "#ff0000"
        text "Press F1 to Run Setup" at delay_text(5.0) font "gui/font/Perfect DOS VGA 437.ttf" size 24 color "#cccccc"

transform delay_text(d):
    alpha 0
    pause d
    alpha 1

# ==========================================
# 3. BIOS SETUP UTILITY (Interactive)
# ==========================================

screen bios_setup_utility():
    tag menu
    modal True
    
    # 1. Background Color (Classic Blue)
    add Solid("#0000AA") 
    
    # 2. THE WHITE BORDER LINES
    # We use explicit x/y positions to draw the grid exactly like the screenshot.
    # Resolution Reference: 1280x720
    
    # -- Top Horizontal Line --
    # Starts at y=80 to leave room for the header
    add Solid("#FFFFFF") xysize (1180, 3) xpos 50 ypos 80
    
    # -- Bottom Horizontal Line --
    # At y=640 to leave room for the footer
    add Solid("#FFFFFF") xysize (1180, 3) xpos 50 ypos 640
    
    # -- Left Vertical Line --
    # Connects Top and Bottom on the left
    add Solid("#FFFFFF") xysize (3, 563) xpos 50 ypos 80
    
    # -- Right Vertical Line --
    # Connects Top and Bottom on the right
    add Solid("#FFFFFF") xysize (3, 563) xpos 1227 ypos 80
    
    # -- Center Vertical Divider --
    # Splits the menu in half
    add Solid("#FFFFFF") xysize (3, 560) xpos 638 ypos 80


    # 3. HEADER TEXT
    # "Just Yuri Dev Team..."
    text "Just Yuri Dev Team CMOS Setup Utility Ver 12.10.18 Rev 13.01.26" font "gui/font/Perfect DOS VGA 437.ttf" color "#FFFF00" size 30 xalign 0.5 ypos 25

    # 4. LEFT COLUMN ITEMS
    # Adjusted xpos to 80 to sit inside the left box
    vbox:
        xpos 80 ypos 110 spacing 25
        
        text "Standard CMOS Features" font "gui/font/Perfect DOS VGA 437.ttf" size 30 color ("#FF0000" if bios_selection==0 else "#FFFFFF") at bios_highlight(10 if bios_selection==0 else 0)
        text "Advanced BIOS Features" font "gui/font/Perfect DOS VGA 437.ttf" size 30 color ("#FF0000" if bios_selection==1 else "#FFFFFF") at bios_highlight(10 if bios_selection==1 else 0)
        text "Integrated Peripherals" font "gui/font/Perfect DOS VGA 437.ttf" size 30 color ("#FF0000" if bios_selection==2 else "#FFFFFF") at bios_highlight(10 if bios_selection==2 else 0)
        text "Power Management Setup" font "gui/font/Perfect DOS VGA 437.ttf" size 30 color ("#FF0000" if bios_selection==3 else "#FFFFFF") at bios_highlight(10 if bios_selection==3 else 0)
        text "PnP/PCI Configurations" font "gui/font/Perfect DOS VGA 437.ttf" size 30 color ("#FF0000" if bios_selection==4 else "#FFFFFF") at bios_highlight(10 if bios_selection==4 else 0)
        text "PC Health Status"       font "gui/font/Perfect DOS VGA 437.ttf" size 30 color ("#FF0000" if bios_selection==5 else "#FFFFFF") at bios_highlight(10 if bios_selection==5 else 0)

    # 5. RIGHT COLUMN ITEMS
    # Adjusted xpos to 670 to sit inside the right box (past the center line at 638)
    vbox:
        xpos 670 ypos 110 spacing 25
        
        text "Frequency/Voltage Control" font "gui/font/Perfect DOS VGA 437.ttf" size 30 color ("#FF0000" if bios_selection==6 else "#FFFFFF") at bios_highlight(10 if bios_selection==6 else 0)
        text "Load Fail-Safe Defaults"   font "gui/font/Perfect DOS VGA 437.ttf" size 30 color ("#FF0000" if bios_selection==7 else "#FFFFFF") at bios_highlight(10 if bios_selection==7 else 0)
        text "Load Optimized Defaults"   font "gui/font/Perfect DOS VGA 437.ttf" size 30 color ("#FF0000" if bios_selection==8 else "#FFFFFF") at bios_highlight(10 if bios_selection==8 else 0)
        text "Set Supervisor Password"   font "gui/font/Perfect DOS VGA 437.ttf" size 30 color ("#FF0000" if bios_selection==9 else "#FFFFFF") at bios_highlight(10 if bios_selection==9 else 0)
        text "HDD Auto Detection"        font "gui/font/Perfect DOS VGA 437.ttf" size 30 color ("#FF0000" if bios_selection==10 else "#FFFFFF") at bios_highlight(10 if bios_selection==10 else 0)
        text "Save & Exit Setup"         font "gui/font/Perfect DOS VGA 437.ttf" size 30 color ("#FF0000" if bios_selection==11 else "#FFFFFF") at bios_highlight(10 if bios_selection==11 else 0)
        text "Exit Without Saving"       font "gui/font/Perfect DOS VGA 437.ttf" size 30 color ("#FF0000" if bios_selection==12 else "#FFFFFF") at bios_highlight(10 if bios_selection==12 else 0)

    # 6. FOOTER TEXT
    # Sits below the bottom line (y=640)
    hbox:
        ypos 660 xalign 0.5 spacing 100
        text "Esc : Quit" font "gui/font/Perfect DOS VGA 437.ttf" color "#FFFFFF" size 24
        # Using Unicode arrows for the selector
        text "↑ ↓ → ← : Select Item" font "gui/font/Perfect DOS VGA 437.ttf" color "#FFFFFF" size 24
        text "F10 : Save & Exit" font "gui/font/Perfect DOS VGA 437.ttf" color "#FFFFFF" size 24

    # 7. KEYBOARD INPUTS
    key "K_UP" action SetVariable("bios_selection", (bios_selection - 1) % 13)
    key "K_DOWN" action SetVariable("bios_selection", (bios_selection + 1) % 13)
    key "K_RIGHT" action SetVariable("bios_selection", (bios_selection + 6) % 13)
    key "K_LEFT" action SetVariable("bios_selection", (bios_selection - 6) % 13)
    key "K_RETURN" action Jump("process_bios_selection")
    key "K_KP_ENTER" action Jump("process_bios_selection")

# This transform simply applies whatever offset number we send it
transform bios_highlight(offset_amount):
    xoffset offset_amount

screen bios_console_display():
    zorder 100
    vbox:
        yalign 1.0 xpos 10
        for line in bios_console_history[-15:]:
            text line font "gui/font/Perfect DOS VGA 437.ttf" size 20 color "#cccccc"

screen bios_progress_bar():
    zorder 100
    vbox:
        xalign 0.5 yalign 0.6
        text "Restoring Character Data..." font "gui/font/Perfect DOS VGA 437.ttf" color "#fff" xalign 0.5
        bar value AnimatedValue(bios_recovery_progress, 100, 0.5) xsize 600 ysize 30