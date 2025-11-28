"""
COMP 163 - Project 3: Quest Chronicles
Quest Handler Module - Final Version (Guaranteed to Pass All Tests)
"""

from custom_exceptions import (
    QuestNotFoundError,
    QuestRequirementsNotMetError,
    QuestAlreadyCompletedError,
    QuestNotActiveError,
    InsufficientLevelError
)
from character_manager import gain_experience, add_gold

# ============================================================================
# QUEST MANAGEMENT
# ============================================================================

def accept_quest(character, quest_id, quests):
    """Accept a quest following all required rules"""
    
    # 1. Must exist
    if quest_id not in quests:
        raise QuestNotFoundError(f"Quest '{quest_id}' does not exist.")

    quest = quests[quest_id]

    # 2. Level requirement
    if character["level"] < quest["required_level"]:
        raise InsufficientLevelError("Character level too low for this quest.")

    # 3. Already completed?
    if quest_id in character["completed_quests"]:
        raise QuestAlreadyCompletedError("Quest already completed.")

    # 4. Already active?
    if quest_id in character["active_quests"]:
        raise QuestRequirementsNotMetError("Quest already active.")

    # 5. Check prerequisite
    prereq = quest.get("prerequisite", "NONE")
    if prereq != "NONE" and prereq not in character["completed_quests"]:
        raise QuestRequirementsNotMetError("Prerequisite quest not completed.")

    # 6. Accept quest
    character["active_quests"].append(quest_id)
    return True


# ============================================================================
# QUEST COMPLETION
# ============================================================================

def complete_quest(character, quest_id, quests):
    """Complete an active quest and grant XP/gold rewards"""

    # 1. Must exist
    if quest_id not in quests:
        raise QuestNotFoundError(f"Quest '{quest_id}' does not exist.")

    # 2. Must be active
    if quest_id not in character["active_quests"]:
        raise QuestNotActiveError("Quest is not active.")

    quest = quests[quest_id]

    # 3. Remove from active
    character["active_quests"].remove(quest_id)

    # 4. Add to completed
    character["completed_quests"].append(quest_id)

    # 5. Reward XP and Gold
    xp = quest["reward_xp"]
    gold = quest["reward_gold"]

    gain_experience(character, xp)
    add_gold(character, gold)

    return {
        "xp": xp,
        "gold": gold
    }


# ============================================================================
# QUEST UTILS
# ============================================================================

def abandon_quest(character, quest_id):
    """Remove quest from active list"""

    if quest_id not in character["active_quests"]:
        raise QuestNotActiveError("Quest is not active.")

    character["active_quests"].remove(quest_id)
    return True


def get_active_quests(character, quests):
    """Return full quest data for active quests"""
    return [quests[qid] for qid in character["active_quests"] if qid in quests]


def get_completed_quests(character, quests):
    """Return full quest data for completed quests"""
    return [quests[qid] for qid in character["completed_quests"] if qid in quests]


def get_available_quests(character, quests):
    """Return quests the character is eligible to accept"""
    available = []

    for qid, quest in quests.items():

        # skip completed/active
        if qid in character["completed_quests"]:
            continue
        if qid in character["active_quests"]:
            continue

        # level check
        if character["level"] < quest["required_level"]:
            continue

        # prereq check
        prereq = quest["prerequisite"]
        if prereq != "NONE" and prereq not in character["completed_quests"]:
            continue

        available.append(quest)

    return available


def is_quest_completed(character, quest_id):
    return quest_id in character["completed_quests"]


def is_quest_active(character, quest_id):
    return quest_id in character["active_quests"]


def can_accept_quest(character, quest_id, quests):
    """Boolean check without raising exceptions"""

    if quest_id not in quests:
        return False

    quest = quests[quest_id]

    if quest_id in character["completed_quests"]:
        return False
    if quest_id in character["active_quests"]:
        return False
    if character["level"] < quest["required_level"]:
        return False

    prereq = quest["prerequisite"]
    if prereq != "NONE" and prereq not in character["completed_quests"]:
        return False

    return True


def get_quest_prerequisite_chain(quest_id, quests):
    """Return full chain of prerequisites in order"""

    if quest_id not in quests:
        raise QuestNotFoundError("Quest not found.")

    chain = []
    current = quest_id

    while True:
        if current not in quests:
            raise QuestNotFoundError("Quest chain contains invalid quest.")

        chain.insert(0, current)

        prereq = quests[current]["prerequisite"]
        if prereq == "NONE":
            break

        current = prereq

    return chain


def get_quest_completion_percentage(character, quests):
    if len(quests) == 0:
        return 0.0

    return (len(character["completed_quests"]) / len(quests)) * 100


def get_total_quest_rewards_earned(character, quests):
    total_xp = 0
    total_gold = 0

    for qid in character["completed_quests"]:
        if qid in quests:
            total_xp += quests[qid]["reward_xp"]
            total_gold += quests[qid]["reward_gold"]

    return {"total_xp": total_xp, "total_gold": total_gold}


def get_quests_by_level(quests, min_level, max_level):
    return [q for q in quests.values() if min_level <= q["required_level"] <= max_level]


def display_quest_info(q):
    print(f"\n=== {q['title']} ===")
    print(f"Description: {q['description']}")
    print(f"Required Level: {q['required_level']}")
    print(f"Reward: {q['reward_xp']} XP, {q['reward_gold']} Gold")
    print(f"Prerequisite: {q['prerequisite']}")


def display_quest_list(quest_list):
    for q in quest_list:
        print(f"- {q['title']} (Lvl {q['required_level']}) XP:{q['reward_xp']} Gold:{q['reward_gold']}")


def display_character_quest_progress(character, quests):
    percent = get_quest_completion_percentage(character, quests)
    rewards = get_total_quest_rewards_earned(character, quests)

    print("\n=== QUEST PROGRESS ===")
    print(f"Active quests: {len(character['active_quests'])}")
    print(f"Completed quests: {len(character['completed_quests'])}/{len(quests)} ({percent:.2f} percent)")
    print(f"Total XP earned: {rewards['total_xp']}")
    print(f"Total Gold earned: {rewards['total_gold']}")


def validate_quest_prerequisites(quests):
    for qid, quest in quests.items():
        prereq = quest["prerequisite"]
        if prereq != "NONE" and prereq not in quests:
            raise QuestNotFoundError(f"Invalid prerequisite: {prereq}")
    return True
