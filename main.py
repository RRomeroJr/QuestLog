import json
from QuestNode import *
import os
import ql_tree_handler as tree

# root = QuestNode(_header="ROOT NODE")
with open("QuestNodes.json", "r") as file:
    tree.root = QuestNode.fromdict(json.loads(file.read()))
tree.displayNode = tree.root

QUITBUTTON = "x"
SELECTBUTTON = "s"
TOPARERNTBUTTON = "p"
INCREASELEVELBUTTON = "+"
DECREASELEVELBUTTON = "-"
SAVEBUTTON = "w"
ADDQUEST = "a"
REMOVEQUEST = "r"
def display_subquests():
    os.system("cls")
    print("{}: {}".format(tree.displayNode.header, tree.displayNode.short_desc))
    for count, sq in enumerate(tree.displayNode.subquests):
        print("{}) {}".format(count + 1, sq.header))
        if(len(sq.subquests) > 0):
            for ssq in sq.subquests:
                print("- {}".format(ssq.header))
        count += 1
def display_options():
    # global displayNode
    # global root
    to_return = ""
    def add_separator_if_needed():
        nonlocal to_return
        if(len(to_return) > 0):
            to_return += ", "
    if(len(tree.displayNode.subquests) > 0):
        add_separator_if_needed()
        to_return += "{} = sel subquest".format(SELECTBUTTON)
    if (tree.displayNode != tree.root):
        add_separator_if_needed()
        to_return += "{} = parent ({})".format(TOPARERNTBUTTON, tree.displayNode.parent.header)
    if (tree.displayNode != tree.root and tree.displayNode.parent != tree.root):
        add_separator_if_needed()
        to_return += "{} = reparent to ({})".format(INCREASELEVELBUTTON, tree.displayNode.parent.parent.header)
    if (len(tree.displayNode.subquests) > 1):
        add_separator_if_needed()
        to_return += "{} = re-parent subquest".format(DECREASELEVELBUTTON)

    add_separator_if_needed()
    to_return += "{} = save".format(SAVEBUTTON)
    add_separator_if_needed()
    to_return += "{} = add".format(ADDQUEST)
    add_separator_if_needed()
    to_return += "{} = remove".format(REMOVEQUEST)
    add_separator_if_needed()
    to_return += "{} = quit".format(QUITBUTTON)
    return to_return
def main():
    run = True
    opt = ""
    while(run):
        display_subquests()
        opt = input(display_options() + "\n").lower()
        if(opt == SELECTBUTTON):
            tree.select_subquest_loop()
        elif (opt == TOPARERNTBUTTON):
            tree.select_parent()
        elif(opt == INCREASELEVELBUTTON):
            tree.increase_level()
        elif(opt == DECREASELEVELBUTTON):
            tree.decrease_level()
        elif(opt == SAVEBUTTON):
            tree.save()
        elif(opt == ADDQUEST):
            tree.add_quest()
        elif(opt == REMOVEQUEST):
            tree.remove_quest()
        elif(opt == QUITBUTTON):
            run = False



if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
