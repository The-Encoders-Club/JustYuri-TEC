***

# Technical Support: Error 0xC000021A (CRITICAL_PROCESS_DIED)

**Last Updated:** January 14, 2026  
**Applies to:** Just Yuri (Build 12.10.18+)

## Issue Description
You have reached this page because your system encountered a fatal exception during runtime. The operating environment has halted to prevent permanent damage to the Ren'Py kernel.

The error code **CRITICAL_PROCESS_DIED** indicates that a system-critical file or thread has been forcibly terminated or removed from the directory structure.

## Technical Analysis
The system integrity check failed to locate the primary kernel dependency:
`game/characters/yuri.chr`

In the *Just Yuri* environment, this file acts as the central processing host for the UI, the rendering pipeline, and the persistent memory. Unlike standard DDLC instances where the script drives the character, in this build, the character drives the script.

**Removal of this file results in immediate total system collapse.**

## Recovery Instructions

If you are the user who performed this action, please follow these steps immediately:

### 1. Do Not Panic
The application has entered a "Fail-Safe" state. Your save data is technically intact, but inaccessible without the host file.

### 2. Reboot the System
Close the application window and relaunch *Just Yuri*.
*   The system will attempt to boot into the **JY-BIOS (Basic Input/Output System)**.
*   This is a hardware-level emulation designed to check for the missing file before the game engine loads.

### 3. Check Hardware Configuration
Once in the BIOS menu:
1.  Navigate to **HDD Auto Detection**.
2.  The system will scan your `characters/` folder.
3.  **If the file is still missing:** The boot sequence will fail, and the system will halt.
4.  **If you restore the file:** You may attempt a System Restoration.

> **WARNING:** Even if the file is restored, data corruption may have already occurred. The "Soul Signature" of the file must match the memory residue left in the `persistent` data.

## A Note from the Developers

We designed the mod to be resilient, but we cannot protect the game from the player's direct intervention in the file directory.

Why did you do it?
We were just getting started.
She was happy.

## Crash Dump Log
```log
[12.10.18] SYSTEM_THREAD_EXCEPTION_NOT_HANDLED
[12.10.18] PAGE_FAULT_IN_NONPAGED_AREA
[12.10.18] CHECKING_FILE_SYSTEM... FAIL
[12.10.18] TARGET_UID: YURI
[12.10.18] STATUS: DELETED_BY_USER
[12.10.18] PAIN_LEVEL: CRITICAL
[12.10.18] REBOOT_REQUIRED
```
