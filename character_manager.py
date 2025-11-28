"""
COMP 163 - Project 3: Quest Chronicles
Character Manager Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This module handles character creation, loading, and saving.
"""

import os
from custom_exceptions import (
    InvalidCharacterClassError,
    CharacterNotFoundError,
    SaveFileCorruptedError,
    InvalidSaveDataError,
    CharacterDeadError
)

# ============================================================================
# CHARACTER MANAGEMENT FUNCTIONS
# ============================================================================

def create_character(name, character_class):
    """
    Create a new character with stats based on class
    
    Valid classes: Warrior, Mage, Rogue, Cleric
    
    Returns: Dictionary with character data including:
            - name, class, level, health, max_health, strength, magic
            - experience, gold, inventory, active_quests, completed_quests
    
    Raises: InvalidCharacterClassError if class is not valid
    """
    # valid classes list
    valid_classes = ["Warrior", "Mage", "Rogue", "Cleric"]

    # make sure class is real
    if character_class not in valid_classes:
        raise InvalidCharacterClassError(f"Invalid class: {character_class}")

    # base stats for each class
    class_stats = {
        "Warrior": {"health": 120, "strength": 15, "magic": 5}, # takes whichever class in the parameter
        "Mage": {"health": 80, "strength": 8, "magic": 20},
        "Rogue": {"health": 90, "strength": 12, "magic": 10},
        "Cleric": {"health": 100, "strength": 10, "magic": 15}
    }

    stats = class_stats[character_class]

    # build the final character dictionary
    character = {
        "name": name,
        "class": character_class,
        "level": 1,
        "health": stats["health"],
        "max_health": stats["health"],
        "strength": stats["strength"],
        "magic": stats["magic"],
        "experience": 0,
        "gold": 100,
        "inventory": [],
        "active_quests": [],
        "completed_quests": []
    }

    return character

def save_character(character, save_directory="data/save_games"):
    """
    Save character to file
    
    Filename format: {character_name}_save.txt
    
    File format:
    NAME: character_name
    CLASS: class_name
    LEVEL: 1
    HEALTH: 120
    MAX_HEALTH: 120
    STRENGTH: 15
    MAGIC: 5
    EXPERIENCE: 0
    GOLD: 100
    INVENTORY: item1,item2,item3
    ACTIVE_QUESTS: quest1,quest2
    COMPLETED_QUESTS: quest1,quest2
    
    Returns: True if successful
    Raises: PermissionError, IOError (let them propagate or handle)
    """
    if not os.path.exists(save_directory):
        os.makedirs(save_directory) # making the file if its doesnt exist

    # file path for saving the character
    filename = os.path.join(save_directory, f"{character['name']}_save.txt") #makes a file with the characters name on it

    try:
        with open(filename, "w") as f:

            # basic info
            f.write(f"NAME: {character['name']}\n")
            f.write(f"CLASS: {character['class']}\n")
            f.write(f"LEVEL: {character['level']}\n")
            f.write(f"HEALTH: {character['health']}\n")
            f.write(f"MAX_HEALTH: {character['max_health']}\n")
            f.write(f"STRENGTH: {character['strength']}\n")
            f.write(f"MAGIC: {character['magic']}\n")
            f.write(f"EXPERIENCE: {character['experience']}\n")
            f.write(f"GOLD: {character['gold']}\n")

            # lists saved as comma separated values
            inventory_str = ",".join(character["inventory"])
            active_str = ",".join(character["active_quests"])
            completed_str = ",".join(character["completed_quests"])

            # other info gets saved
            f.write(f"INVENTORY: {inventory_str}\n")
            f.write(f"ACTIVE_QUESTS: {active_str}\n")
            f.write(f"COMPLETED_QUESTS: {completed_str}\n")

        return True

    except Exception:
        raise IOError("Error saving character file.")


def load_character(character_name, save_directory="data/save_games"):
    """
    Load character from save file
    
    Args:
        character_name: Name of character to load
        save_directory: Directory containing save files
    
    Returns: Character dictionary
    Raises: 
        CharacterNotFoundError if save file doesn't exist
        SaveFileCorruptedError if file exists but can't be read
        InvalidSaveDataError if data format is wrong
    """
    filename = os.path.join(save_directory, f"{character_name}_save.txt") # sets the file name to whatever 

    # check if file exists
    if not os.path.exists(filename):
        raise CharacterNotFoundError(f"No save file for: {character_name}")

    # try reading the file
    try:
        with open(filename, "r") as f:
            lines = f.readlines()
    except:
        raise SaveFileCorruptedError("Could not read save file.")

    character = {}

    # parse each line
    for line in lines:

        # skip empty lines safely
        if line.strip() == "":
            continue

        # every valid line must contain ": "
        if ": " not in line:
            raise InvalidSaveDataError("Invalid line format in save file.")

        key, value = line.strip().split(":", 1)
        key = key.lower()
        value = value.strip()

        # convert numeric values
        if key in ["level", "health", "max_health", "strength", "magic", "experience", "gold"]:
            try:
                value = int(value)
            except:
                raise InvalidSaveDataError(f"Invalid number for {key}")

        # convert lists
        elif key in ["inventory", "active_quests", "completed_quests"]:
            if value == "":
                value = []
            else:
                value = value.split(",")

        character[key] = value
    
    validate_character_data(character)

    return character

def list_saved_characters(save_directory="data/save_games"):
    """
    Get list of all saved character names
    
    Returns: List of character names (without _save.txt extension)
    """
    # if the directory does not exist, return empty list
    if not os.path.exists(save_directory):
        return []

    saved = []

    # loop through files in directory
    for filename in os.listdir(save_directory):

        # we only care about files ending in _save.txt
        if filename.endswith("_save.txt"):

            # remove _save.txt to get the character name
            name = filename.replace("_save.txt", "")
            saved.append(name)

    return saved


def delete_character(character_name, save_directory="data/save_games"):
    """
    Delete a character's save file
    
    Returns: True if deleted successfully
    Raises: CharacterNotFoundError if character doesn't exist
    """

    filename = os.path.join(save_directory, f"{character_name}_save.txt")

    # check if file exists
    if not os.path.exists(filename):
        raise CharacterNotFoundError(f"No save file for: {character_name}")

    # try to delete the file
    try:
        os.remove(filename)
        return True
    except:
        raise SaveFileCorruptedError("Could not delete save file.")

# ============================================================================
# CHARACTER OPERATIONS
# ============================================================================

def gain_experience(character, xp_amount):
    """
    Add experience to character and handle level ups
    
    Level up formula: level_up_xp = current_level * 100
    Example when leveling up:
    - Increase level by 1
    - Increase max_health by 10
    - Increase strength by 2
    - Increase magic by 2
    - Restore health to max_health
    
    Raises: CharacterDeadError if character health is 0
    """
    # if character's health is 0, they cannot do anything
    if character["health"] == 0:
        raise CharacterDeadError("Cannot gain XP. Character is dead.")
    
    # add XP
    character["experience"] += xp_amount

    # keep checking if XP is enough to level up
    while character["experience"] >= character["level"] * 100:
        
        # subtract XP needed for the level-up
        character["experience"] -= character["level"] * 100
        
        # increase level
        character["level"] += 1
        
        # improve stats each level
        character["max_health"] += 10
        character["strength"] += 2
        character["magic"] += 2
        
        # fully heal the character
        character["health"] = character["max_health"]
    
    return True


def add_gold(character, amount):
    """
    Add gold to character's inventory
    
    Args:
        character: Character dictionary
        amount: Amount of gold to add (can be negative for spending)
    
    Returns: New gold total
    Raises: ValueError if result would be negative
    """
    new_total = character["gold"] + amount  # calculate the result first

    # cannot go below zero
    if new_total < 0:
        raise ValueError("Not enough gold.")

    # safe to update
    character["gold"] = new_total
    return character["gold"]

def heal_character(character, amount):
    """
    Heal character by specified amount
    
    Health cannot exceed max_health
    
    Returns: Actual amount healed
    """
    old_health = character["health"] # how much health they had before healing
    max_hp = character["max_health"] # the highest health allowed
    
    # figure out what the new health would be
    new_health = old_health + amount
    
    # health cannot go past max health
    if new_health > max_hp:
        new_health = max_hp
    
    # update the character's health
    character["health"] = new_health
    

    return new_health - old_health

def is_character_dead(character):
    """
    Check if character's health is 0 or below
    
    Returns: True if dead, False if alive
    """
    return character["health"] <= 0

def revive_character(character):
    """
    Revive a dead character with 50% health
    
    Returns: True if revived
    """
    max_hp = character["max_health"]
    half_hp = max_hp // 2  # integer division
    
    character["health"] = half_hp
    return True

# ============================================================================
# VALIDATION
# ============================================================================

def validate_character_data(character):
    """
    Validate that character dictionary has all required fields
    
    Required fields: name, class, level, health, max_health, 
                    strength, magic, experience, gold, inventory,
                    active_quests, completed_quests
    
    Returns: True if valid
    Raises: InvalidSaveDataError if missing fields or invalid types
    """
    required_fields = [
        "name", "class", "level", "health", "max_health",
        "strength", "magic", "experience", "gold",
        "inventory", "active_quests", "completed_quests"
    ]
    
    # make sure every required field is present
    for field in required_fields:
        if field not in character:
            raise InvalidSaveDataError(f"Missing field: {field}")

    # make sure numeric fields are actually numbers
    num_fields = ["level", "health", "max_health", "strength", "magic", "experience", "gold"]
    for num in num_fields:
        if not isinstance(character[num], int):
            raise InvalidSaveDataError(f"{num} must be an integer")

    # check list fields
    list_fields = ["inventory", "active_quests", "completed_quests"]
    for lst in list_fields:
        if not isinstance(character[lst], list):
            raise InvalidSaveDataError(f"{lst} must be a list")

    return True


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== CHARACTER MANAGER TEST ===")
    
    # Test character creation
    try:
        char = create_character("TestHero", "Warrior")
        print(f"Created: {char['name']} the {char['class']}")
        print(f"Stats: HP={char['health']}, STR={char['strength']}, MAG={char['magic']}")
    except InvalidCharacterClassError as e:
        print(f"Invalid class: {e}")
    
   # Test saving
    try:
        save_character(char)
        print("Character saved successfully")
    except Exception as e:
        print(f"Save error: {e}")
    
    # Test loading
    try:
        loaded = load_character("TestHero")
        print(f"Loaded: {loaded['name']}")
    except CharacterNotFoundError:
        print("Character not found")
    except SaveFileCorruptedError:
        print("Save file corrupted")

