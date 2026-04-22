#==================================================#
#  Just Yuri Mod - Main File
#==================================================#
#  This file is responsible for loading submods in
#  the game/submods folder and providing the
#  documentation for mod developers
#  :D
#==================================================#

init -999 python:
    submods = {}
    submods.mods = {}
    submods.mod_count = 0
    submods.modinfo_template = {
        "name": "",
        "id": "",
        "version": "1.0.0",
        "dependencies": [],
        "developer_mode": True
    }

    # --- Define Documentation Content ---
    getting_started_content = """Welcome to the submodding community! - Docs Version 1.0.0

If you are seeing this for the first time, these files automatically generate anytime a submod folder is missing a modinfo.json file.
To create a submod, change any of the information you want in the modinfo.json file, create your first .rpy file and start implementing whatever you can think of.

For a brief introduction into renpy, see: https://www.renpy.org/doc/html/quickstart.html#the-ren-py-launcher
If you intend on creating a more advanced submod, you may need knowledge of python as well. The one good place to learn the basics is: https://www.w3schools.com/python/python_intro.asp

To add dialogue to the talk menu, you use the add_dialogue method and provide it with your own Dialogue instance:

label test_label:
    $ show_chr("A-ABGBA-AAAA")
    y "Hi there!"

init python:
    add_dialogue(Dialogue("test_label", DialogueAPI.category_talk, name="Greet Yuri", sub_category="Greetings"))

You can get the sprite code via the control panel when you enable developer mode.

This mod contains various apis to help speed up development since the Just Yuri source is kinda messy at the moment. We will rectify the mess in time.
You can find the sources here: https://github.com/DarkskullDawnZenith/JustYuri

In the future, this documentation will be more fleshed out and user friendly, but for now this will only cover the bare minimum.

You can feel free to delete these documents if you would like to free up space for your mod. If you ever need to regenerate these docs, delete the modinfo.json file and reboot the game. Have fun!
"""

    modinfo_setup_content = """{
    ####################################################################################
    # This is what the Just Yuri mod reads to figure out what this submod is.          #
    # This is always automatically generated when a modinfo.json file is not detected. #
    ####################################################################################

    # The name of your submod. This will show up in game in the mods menu.
    "name": "",

    # The unique id of your submod. This is used in the dependencies blocks of other mods.
    "id": "",

    # The version of your submod. This can be anything you want, but keep it close to the format #.#.#
    "version": "1.0.0",

    # The unique ids of each submod that this submod requires.
    # If any id is present here and the mod isn't loaded, the game will crash and display any mods that are missing
    # Also supports putting a single string as well if you don't want to use a list
    "dependencies": [],

    # Whether to enable debug mode for Just Yuri. Adds additional information to the logs and allows access to the control panel
    "developer_mode": true
}
"""
    #==================================================#
    #  Functions
    #==================================================#
    def parse_mod_id(name):
        match = regex.match("[a-z0-9\\_\\-]*", name.lower().replace(" ", "_"))
        return match.group(0) if match != None else "unknown"

    class Submod:
        name = None
        id = None
        version = "1.0.0"
        description = None
        dependencies = []
        missing_dependencies = []
        icon = None
        path = None

        def __init__(self, mod_name, mod_id, path):
            self.name = mod_name
            self.id = mod_id
            self.path = path
            # Default icon is still loaded from the *game* directory's images.
            self.icon = Transform(os.path.join(config.gamedir, "images", "default_submod.png"), size=(100,100), fit="contain")

    #==================================================#
    #  Start Submod System
    #==================================================#
    dir_submods = os.path.join(config.gamedir, "submods")
    request_dev_access = False
    print("Initializing submods...")

    # -- Check if base submod directory exists
    if not os.path.isdir(dir_submods):
        print_debug("  - Creating submods folder...")
        try:
            os.makedirs(dir_submods, exist_ok=True)
        except Exception as e:
            print_error(e)
            print(f"  - Cannot create submods directory at {dir_submods}. Skipping submod loading...")
            
    # -- Scan for submods
    if os.path.isdir(dir_submods):
        for directory in os.scandir(dir_submods):
            if not directory.is_dir():
                continue

            submods.mod_count += 1
            mod_docs_dir = os.path.join(directory.path, "documentation")
            mod_info_path = os.path.join(directory.path, "modinfo.json")
            mod_icon_path = os.path.join(directory.path, "icon.png")
            submod = Submod(directory.name, parse_mod_id(directory.name), directory.path)

            # -- Read modinfo.json
            if not os.path.isfile(mod_info_path):
                print_debug("  - Generating modinfo.json for submod \"" + submod.id + "\"...")
                try:
                    with open(mod_info_path, 'w', encoding='utf-8') as file:
                        modinfo = submods.modinfo_template.copy()
                        modinfo["name"] = submod.name or "" 
                        modinfo["id"] = submod.id or ""
                        json.dump(modinfo, file, indent=4)
                    print_debug("  - Finished generating modinfo.json!")
                except Exception as e:
                    print_debug("  - Failed to generate modinfo.json. Skipping...")
                    print_error(e, path=mod_error_path)
            else:
                print(f"  - Reading modinfo.json for {submod.id}...")
                try:
                    with open(mod_info_path, 'r', encoding='utf-8') as file:
                        modinfo = json.load(file)
                        submod.name = str(modinfo.get("name", submod.name))
                        submod.id = str(modinfo.get("id", submod.id))
                        submod.version = str(modinfo.get("version", submod.version))
                        submod.description = modinfo.get("description", submod.description)
                        submod.dependencies = modinfo.get("dependencies", submod.dependencies)
                        request_dev_access = modinfo.get("developer_mode", request_dev_access)
                        
                        if submod.description is not None:
                            submod.description = str(submod.description)
                        if isinstance(submod.dependencies, str):
                            submod.dependencies = [submod.dependencies]
                        elif not isinstance(submod.dependencies, builtins.list):
                            submod.dependencies = []
                except Exception as e:
                    print_debug("  - Failed to load modinfo.json")
                    print_error(e, path=mod_error_path)

            # -- Load icon
            if os.path.isfile(mod_icon_path):
                try:
                    relative_icon_path = os.path.relpath(mod_icon_path, config.gamedir)
                    relative_icon_path = relative_icon_path.replace(os.path.sep, '/')

                    submod.icon = Transform(relative_icon_path, size=(100, 100), fit="contain")
                except Exception as e:
                    print_debug("  - Failed to load icon.png")
                    print_error(e, path=mod_error_path)
            renpy.image(submod.id + ":icon", submod.icon)
            submods.mods[submod.id] = submod
            print("  - Mod ID: " + submod.id + ", Version: " + submod.version)

    # --- Dependency check ---
    print("Checking loaded submods for missing dependencies...")
    should_continue = True

    for key, submod in submods.mods.items():
        if len(submod.dependencies) > 0:
            error_message = f"  - Submod '{submod.id}' is missing one or more dependencies:"
            for dependency in submod.dependencies:
                parsed_dependency_id = parse_mod_id(dependency)
                if parsed_dependency_id not in submods.mods:
                    
                    submod.missing_dependencies.append(parsed_dependency_id)
                    error_message += f"\n    > {parsed_dependency_id}"
                    print(error_message)
                    should_continue = False

    if not should_continue:
        print_fatal(KeyError("One or more submods are missing dependencies. Check error.log or console output for details."))

    # --- Developer mode check ---
    if request_dev_access:
        print("One or more mods have requested developer mode. Enabling developer mode...")
        config.developer = True
        dev_access = True

    print("Mod loading complete! Loaded " + str(submods.mod_count) + " mod(s)")
