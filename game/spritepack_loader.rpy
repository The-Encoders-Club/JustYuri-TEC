init -99 python:
    # A list to store the names of all available costumes, including defaults.
    # We start with the default costumes already in the mod.
    available_costumes = {
        "School Uniform": "school",
        "Casual Sweater": "sweater",
        "Valentine's Outfit": "valentines",
        "Bikini": "bikini",
        "Romantic Goth Dress": "gothic"
        # Add any other hardcoded costumes here.
    }

    # This function will scan for new spritepacks.
    def discover_spritepacks():
        spritepacks_path = "spritepacks"
        
        # renpy.scandir() is the correct way to look for files, as it also checks inside .rpa archives.
        try:
            # Get all the pack folders inside /spritepacks
            packs = renpy.scandir(spritepacks_path)
            
            for pack_name in packs:
                pack_path = spritepacks_path + "/" + pack_name
                
                # We only care about directories
                if renpy.isdir(pack_path):
                    
                    # Scan all files within the pack directory
                    asset_files = renpy.scandir(pack_path)
                    for filename in asset_files:
                        if filename.lower().endswith('.png'):
                            
                            # Logic to extract the costume name.
                            # e.g., "torso_beach.png" -> we want to extract "beach"
                            parts = filename.rsplit('.', 1)[0].split('_')
                            if len(parts) > 1:
                                costume_name = parts[-1]
                                image_tag = '_'.join(parts[:-1]) # e.g., "torso" or "downarm_left_1"
                                full_image_name = f"{image_tag}_{costume_name}"
                                full_image_path = f"{pack_path}/{filename}"
                                
                                # Use renpy.image() to define this sprite part for the game to use.
                                # This is the crucial step. It makes "torso_beach" a valid image.
                                renpy.image(full_image_name, full_image_path)
                                
                                # Add the new costume to our list if it's not already there.
                                # We create a user-friendly name for the menu.
                                friendly_name = costume_name.replace('_', ' ').title()
                                if friendly_name not in available_costumes:
                                    # We also add the artist/pack name for credit!
                                    pack_friendly_name = pack_name.replace('_', ' ').title()
                                    available_costumes[f"{friendly_name} ({pack_friendly_name})"] = costume_name

        except:
            # If the spritepacks folder doesn't exist or is empty, we do nothing.
            pass

    # Run the discovery function at startup.
    discover_spritepacks()