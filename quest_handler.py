"""
COMP 163 - Project 3: Quest Chronicles
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
    
    if quest_id not in quests:
        raise QuestNotFoundError("Quest does not exist.")

    quest = quests[quest_id]

    # if already finished, cannot accept again
    if quest_id in character["completed_quests"]:
        raise QuestAlreadyCompletedError("Quest already completed.")

    # check prerequisite requirement
    prereq = quest.get("prerequisite", "NONE")
    if prereq != "NONE" and prereq not in character["completed_quests"]:
        raise QuestRequirementsNotMetError("Missing prerequisite quest.")

    # character level too low
    if character["level"] < quest["required_level"]:
        raise InsufficientLevelError("Not high enough level for this quest.")

    # cannot accept an already active quest
    if quest_id in character["active_quests"]:
        raise QuestRequirementsNotMetError("Quest already active.")

    # add quest to active list
    character["active_quests"].append(quest_id)
    return True


# ============================================================================
# QUEST COMPLETION
# ============================================================================

def complete_quest(character, quest_id, quests):
    """Complete an active quest and grant XP/gold rewards"""

    if quest_id not in quests:
        raise QuestNotFoundError("Quest does not exist.")

    # can only complete if it's active
    if quest_id not in character["active_quests"]:
        raise QuestNotActiveError("Quest is not active.")

    quest = quests[quest_id]

    # remove from active and move to completed
    character["active_quests"].remove(quest_id)
    character["completed_quests"].append(quest_id)

    # give rewards
    xp = quest["reward_xp"]
    gold = quest["reward_gold"]

    gain_experience(character, xp)
    add_gold(character, gold)

    return {"xp": xp, "gold": gold}


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
    return [quests[q] for q in character["active_quests"] if q in quests]


def get_completed_quests(character, quests):
    """Return full quest data for completed quests"""
    return [quests[q] for q in character["completed_quests"] if q in quests]


def get_available_quests(character, quests):
    """Return quests the character is eligible to accept"""
    available = []

    for qid, quest in quests.items():

        if qid in character["completed_quests"]:
            continue
        if qid in character["active_quests"]:
            continue

        if character["level"] < quest["required_level"]:
            continue

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
    if quest_id not in quests:
        raise QuestNotFoundError("Quest not found.")

    chain = []
    current = quest_id

    while True:
        if current not in quests:
            raise QuestNotFoundError("Invalid quest in chain.")

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
    xp_total = 0
    gold_total = 0

    for q in character["completed_quests"]:
        if q in quests:
            xp_total += quests[q]["reward_xp"]
            gold_total += quests[q]["reward_gold"]

    return {"total_xp": xp_total, "total_gold": gold_total}


def get_quests_by_level(quests, min_level, max_level):
    return [
        q for q in quests.values()
        if min_level <= q["required_level"] <= max_level
    ]

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
            raise QuestNotFoundError("Invalid prerequisite found.")
    return True

# ============================================================================
# TESTING
# ============================================================================

#if __name__ == "__main__":
#    print("=== QUEST HANDLER TEST ===")
    
    # Test data
#      test_char = {
#          'level': 1,
#          'active_quests': [],
 #         'completed_quests': [],
  #        'experience': 0,
     #     'gold': 100
   #   }
    #
  #    test_quests = {
   #       'first_quest': {
#              'quest_id': 'first_quest',
          #    'title': 'First Steps',
       #       'description': 'Complete your first quest',
    #       'reward_xp': 50,
 #             'reward_gold': 25,
          #    'required_level': 1,
       #       'prerequisite': 'NONE'
    #      }
 #     }
    #
   #   try:
      #    accept_quest(test_char, 'first_quest', test_quests)
      #    print("Quest accepted!")
   #   except QuestRequirementsNotMetError as e:
#          print(f"Cannot accept: {e}")

