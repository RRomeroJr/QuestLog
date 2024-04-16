import json
from QuestNode import *
import os
class QuestNodeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, QuestNode):
            
            _subquests = [] # Needed to make the deafult an empty array instead of None
            if(len(o.subquests) > 0):
                for sq in o.subquests:
                    _subquests.append(self.default(sq))

            # Getting a dict obj. Dicts become JSON objects
            return {"header": o.header, "short_desc": o.short_desc, "long_desc": o.long_desc, "subquests": _subquests, "id": o.id}

        return super().default(o) #This is make the Encoder Error out.
tempOpts = []
# root = QuestNode(_header="ROOT NODE")
with open("QuestNodes.json", "r") as file:
    root = QuestNode.fromdict(json.loads(file.read()))
displayNode = root
QUITBUTTON = "x"
SELECTBUTTON = "s"
TOPARERNTBUTTON = "p"
INCREASELEVELBUTTON = "+"
DECREASELEVELBUTTON = "-"
SAVEBUTTON = "w"
def display_subquests():
    os.system("cls")
    print("{}: {}".format(displayNode.header, displayNode.short_desc))
    for count, sq in enumerate(displayNode.subquests):
        print("{}) {}".format(count + 1, sq.header))
        if(len(sq.subquests) > 0):
            for ssq in sq.subquests:
                print("- {}".format(ssq.header))
        count += 1
def choose_quest():
    global displayNode
    choice = input("Enter quest number that you would like to select")
    loop = True
    while(loop):
        if(not choice.isnumeric()):
            display_subquests()
            print("You did not enter a number")
            choice = input("Enter quest number that you would like to select")
        elif((int(choice) <= 0) or (int(choice) > len(displayNode.subquests))):
            display_subquests()
            print("You're choice was out of range")
            choice = input("Enter quest number that you would like to select")
        else:
            loop = False
    return displayNode.subquests[int(choice) - 1]
def select_subquest_loop():
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
def display_options():
    global displayNode
    global root
    to_return = ""
    def add_separator_if_needed():
        nonlocal to_return
        if(len(to_return) > 0):
            to_return += ", "
    if(len(displayNode.subquests) > 0):
        add_separator_if_needed()
        to_return += "{} = sel subquest".format(SELECTBUTTON)
    if (displayNode != root):
        add_separator_if_needed()
        to_return += "{} = parent ({})".format(TOPARERNTBUTTON, displayNode.parent.header)
    if (displayNode != root and displayNode.parent != root):
        add_separator_if_needed()
        to_return += "{} = reparent to ({})".format(INCREASELEVELBUTTON, displayNode.parent.parent.header)
    if (len(displayNode.subquests) > 1):
        add_separator_if_needed()
        to_return += "{} = re-parent subquest".format(DECREASELEVELBUTTON)

    add_separator_if_needed()
    to_return += "{} = save".format(SAVEBUTTON)
    add_separator_if_needed()
    to_return += "{} = quit".format(QUITBUTTON)
    return to_return
def main():
    run = True
    opt = ""
    while(run):
        display_subquests()
        opt = input(display_options()).lower()
        if(opt == SELECTBUTTON):
            select_subquest_loop()
        elif (opt == TOPARERNTBUTTON):
            select_parent()
        elif(opt == INCREASELEVELBUTTON):
            increase_level()
        elif(opt == DECREASELEVELBUTTON):
            decrease_level()
        elif(opt == SAVEBUTTON):
            save()
        elif(opt == QUITBUTTON):
            run = False



if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
