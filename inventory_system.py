"""
COMP 163 - Project 3: Quest Chronicles
Inventory System Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This module handles inventory management, item usage, and equipment.
"""

from custom_exceptions import (
    InventoryFullError,
    ItemNotFoundError,
    InsufficientResourcesError,
    InvalidItemTypeError
)

MAX_INVENTORY_SIZE = 20

# ============================================================================
# INVENTORY MANAGEMENT
# ============================================================================

def add_item_to_inventory(character, item_id):
    inventory = character["inventory"]

    if len(inventory) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory is full.")

    inventory.append(item_id)
    return True


def remove_item_from_inventory(character, item_id):
    inventory = character["inventory"]

    if item_id not in inventory:
        raise ItemNotFoundError(f"Item not found: {item_id}")

    inventory.remove(item_id)
    return True


def has_item(character, item_id):
    return item_id in character["inventory"]


def count_item(character, item_id):
    return character["inventory"].count(item_id)


def get_inventory_space_remaining(character):
    return MAX_INVENTORY_SIZE - len(character["inventory"])


def clear_inventory(character):
    old_items = character["inventory"].copy()
    character["inventory"].clear()
    return old_items

# ============================================================================
# ITEM USAGE
# ============================================================================

def use_item(character, item_id, item_data):
    inventory = character["inventory"]

    if item_id not in inventory:
        raise ItemNotFoundError(f"Item not found: {item_id}")

    if item_data["type"] != "consumable":
        raise InvalidItemTypeError("Item is not a consumable.")

    effect_string = item_data["effect"]

    stat_name, value = parse_item_effect(effect_string)

    apply_stat_effect(character, stat_name, value)

    inventory.remove(item_id)

    return f"You used {item_id} and gained {stat_name} +{value}."

# ============================================================================
# EQUIPMENT
# ============================================================================

def equip_weapon(character, item_id, item_data):
    inventory = character["inventory"]

    if item_id not in inventory:
        raise ItemNotFoundError(f"Item not found: {item_id}")

    if item_data["type"] != "weapon":
        raise InvalidItemTypeError("Item is not a weapon.")

    # ensure fields exist
    if "equipped_weapon" not in character:
        character["equipped_weapon"] = None
        character["equipped_weapon_effect"] = None

    if character["equipped_weapon"] is not None:
        old_weapon = character["equipped_weapon"]
        old_effect = character["equipped_weapon_effect"]

        stat_name, value = parse_item_effect(old_effect)
        apply_stat_effect(character, stat_name, -value)

        inventory.append(old_weapon)

    effect_string = item_data["effect"]
    stat_name, value = parse_item_effect(effect_string)

    apply_stat_effect(character, stat_name, value)

    character["equipped_weapon"] = item_id
    character["equipped_weapon_effect"] = effect_string

    inventory.remove(item_id)
    return f"You equipped {item_id} (+{stat_name} {value})."


def equip_armor(character, item_id, item_data):
    inventory = character["inventory"]

    if item_id not in inventory:
        raise ItemNotFoundError(f"Item not found: {item_id}")

    if item_data["type"] != "armor":
        raise InvalidItemTypeError("Item is not armor.")

    # ensure fields exist
    if "equipped_armor" not in character:
        character["equipped_armor"] = None
        character["equipped_armor_effect"] = None

    if character["equipped_armor"] is not None:
        old_armor = character["equipped_armor"]
        old_effect = character["equipped_armor_effect"]

        stat_name, value = parse_item_effect(old_effect)
        apply_stat_effect(character, stat_name, -value)

        inventory.append(old_armor)

    effect_string = item_data["effect"]
    stat_name, value = parse_item_effect(effect_string)

    apply_stat_effect(character, stat_name, value)

    character["equipped_armor"] = item_id
    character["equipped_armor_effect"] = effect_string

    inventory.remove(item_id)
    return f"You equipped {item_id} (+{stat_name} {value})."


def unequip_weapon(character):
    inventory = character["inventory"]

    if "equipped_weapon" not in character or character["equipped_weapon"] is None:
        return None

    if len(inventory) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory is full.")

    weapon_id = character["equipped_weapon"]
    effect = character["equipped_weapon_effect"]

    stat_name, value = parse_item_effect(effect)
    apply_stat_effect(character, stat_name, -value)

    inventory.append(weapon_id)

    character["equipped_weapon"] = None
    character["equipped_weapon_effect"] = None

    return weapon_id


def unequip_armor(character):
    inventory = character["inventory"]

    if "equipped_armor" not in character or character["equipped_armor"] is None:
        return None

    if len(inventory) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory is full.")

    armor_id = character["equipped_armor"]
    effect = character["equipped_armor_effect"]

    stat_name, value = parse_item_effect(effect)
    apply_stat_effect(character, stat_name, -value)

    inventory.append(armor_id)

    character["equipped_armor"] = None
    character["equipped_armor_effect"] = None

    return armor_id

# ============================================================================
# SHOP SYSTEM
# ============================================================================

def purchase_item(character, item_id, item_data):
    cost = item_data["cost"]
    inventory = character["inventory"]

    if character["gold"] < cost:
        raise InsufficientResourcesError("Not enough gold to purchase this item.")

    if len(inventory) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory is full.")

    character["gold"] -= cost
    inventory.append(item_id)
    return True


def sell_item(character, item_id, item_data):
    inventory = character["inventory"]

    if item_id not in inventory:
        raise ItemNotFoundError(f"Item not found: {item_id}")

    cost = item_data.get("cost", None)
    if not isinstance(cost, int):
        raise InvalidItemTypeError("Item cost invalid.")

    sell_price = cost // 2
    inventory.remove(item_id)
    character["gold"] += sell_price

    return sell_price

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_item_effect(effect_string):
    if ":" not in effect_string:
        raise InvalidItemTypeError("Invalid effect format.")

    stat_name, value_str = effect_string.split(":", 1)

    try:
        value = int(value_str)
    except:
        raise InvalidItemTypeError("Effect value must be an integer.")

    return stat_name, value


def apply_stat_effect(character, stat_name, value):
    valid_stats = ["health", "max_health", "strength", "magic"]

    if stat_name not in valid_stats:
        raise InvalidItemTypeError("Invalid stat name in effect.")

    character[stat_name] += value

    if stat_name == "health" and character["health"] > character["max_health"]:
        character["health"] = character["max_health"]


def display_inventory(character, item_data_dict):
    inventory = character["inventory"]

    if len(inventory) == 0:
        print("Inventory is empty.")
        return

    item_counts = {}
    for item_id in inventory:
        item_counts[item_id] = item_counts.get(item_id, 0) + 1

    print("=== INVENTORY ===")

    for item_id, count in item_counts.items():
        item_info = item_data_dict.get(item_id, None)

        if item_info is None:
            print(f"{item_id} x{count} (Unknown item)")
            continue

        name = item_info["name"]
        item_type = item_info["type"]

        print(f"{name} ({item_type}) x{count}")
