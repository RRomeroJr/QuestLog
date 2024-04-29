import json
from QuestNode import *
import os

root = None
displayNode = None

def choose_quest(): # --check: would be nice if I could have prompts here. and a way to cancle
    global displayNode
    choice = input("Enter quest number that you would like to select: ")
    loop = True
    while(loop):
        if(not choice.isnumeric()):
            # display_subquests()
            print("You did not enter a number")
            choice = input("Enter quest number that you would like to select: ")
        elif((int(choice) <= 0) or (int(choice) > len(displayNode.subquests))):
            # display_subquests()
            print("You're choice was out of range")
            choice = input("Enter quest number that you would like to select: ")
        else:
            loop = False
    return displayNode.subquests[int(choice) - 1]
def select_subquest_loop():  # --revise: remove this what was in here is now in choose_quest
    select_subquest(choose_quest())
def select_subquest(_in_quest):
    global displayNode
    displayNode = _in_quest
def select_parent():
    global displayNode
    displayNode = displayNode.parent
def increase_level():
    global displayNode
    if(displayNode == root):
        print("You are at the root!")
        return
    elif(displayNode.parent == root):
        print("This node is already at the highest level.")
        return
    
    displayNode.parent.subquests.remove(displayNode)
    displayNode.parent.parent.subquests.append(displayNode)
    displayNode.parent = displayNode.parent.parent
    displayNode = displayNode.parent
def decrease_level():
    global displayNode
    target = choose_quest()
    new_parent = choose_quest()

    target.parent.subquests.remove(target)
    new_parent.subquests.append(target)
    target.parent = new_parent
def save():
    with open('QuestNodes.json', 'w') as qnFile:
        result = json.dumps(root, cls= QuestNodeEncoder, indent=2)
        qnFile.write(result)

def add_quest():
    global displayNode
    cancle = False
    _input = ""
    _in_header = None
    _in_short = None
    _in_long = None
    
    _in_header = input("Header (REQ):")
    if _in_header == "":
        return
    
    _in_short = input("Short Description (opt):")

    _in_long = input("Long Description (opt):")
    
    newQuest = QuestNode(_header=_in_header, _short_desc=_in_short, _long_desc=_in_long)
    displayNode.subquests.append(newQuest)
    newQuest.parent = displayNode
    return

def remove_quest():
    selectedQuest = choose_quest()
    assert selectedQuest != root
    if(selectedQuest != None):
        recursive_delete(selectedQuest)
    
    input("Anything to continue..")

def recursive_delete(_quest):
    print("deleting {}".format(_quest.header))
    while len(_quest.subquests) > 0:
        recursive_delete(_quest.subquests[0])
    
    _quest.parent.subquests.remove(_quest)
    del _quest
    return
