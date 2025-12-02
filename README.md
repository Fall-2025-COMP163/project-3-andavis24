Quest Game

COMP 163 Project 3
Author: Ajani Davis

Overview

Quest Chronicles is a text based RPG system built from modular Python files. The project loads quests and items from external data files, manages character creation and progression, handles inventory and equipment, processes quest completion logic, and simulates turn based combat. All systems interact through a clean dictionary based data flow.

How to Run

Run the game from the main module:

python main.py


The program automatically creates default data files in the data directory if they do not exist.

File Structure
project/
│
├── main.py
├── game_data.py
├── character_manager.py
├── inventory_system.py
├── quest_handler.py
├── combat_system.py
├── custom_exceptions.py
│
└── data/
    ├── items.txt
    ├── quests.txt
    └── save_games/

Module Summaries
game_data.py

Handles loading, parsing, validating, and generating game data.
Reads items and quests from text files, checks formatting, converts fields to correct types, and returns clean dictionaries used by other modules.

character_manager.py

Creates characters and manages stats like health, level, experience, gold, and equipped gear.
Also manages saving and loading character progress from the save_games directory.

inventory_system.py

Handles all inventory operations.
Includes item adding and removal, capacity checks, item usage, weapon and armor equipment, stat modification, and shop purchasing or selling.

quest_handler.py

Loads available quests, tracks active and completed quests, checks level requirements, applies rewards, and ensures prerequisite quests are completed.

combat_system.py

Runs simple turn based battles.
Handles damage calculation, special abilities, health checks, and battle results.

main.py

Coordinates all modules.
Starts the game, loads data, creates or loads a character, shows menus, and routes user actions to the correct system.

Data Format Requirements
Quest Format
QUEST_ID: example_quest
TITLE: Title Here
DESCRIPTION: Description text.
REWARD_XP: 50
REWARD_GOLD: 20
REQUIRED_LEVEL: 1
PREREQUISITE: NONE

Item Format
ITEM_ID: example_item
NAME: Item Name
TYPE: consumable
EFFECT: health:20
COST: 30
DESCRIPTION: Some description.

Error Handling

The project raises custom exceptions for:

Missing or unreadable data files

Invalid text formatting

Inventory full conditions

Item not found

Insufficient gold

Invalid item type

These are defined in custom_exceptions.py.

AI Usage

AI assistance was used for debugging.
