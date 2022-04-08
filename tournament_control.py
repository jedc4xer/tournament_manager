import os
import requests
import string

# Clean the screen
clear_term = "cls||clear"
os.system(clear_term)

# Get text print blocks from template file
def get_statements():
    path = "https://raw.githubusercontent.com/jedc4xer/python_exercises/main/tournament_statements.txt"
    statements = requests.get(path).text.split(",")
    return statements

# Determine if new tournament or loading existing
def get_tournament_info():
    print(statements[0])
    
    # Check for registration files in directory
    possible_files = [_ for _ in os.listdir() if "registrations.csv" in _]
    allow_choosing = True if len(possible_files) > 0 else False
    print(statements[9]) if allow_choosing else print(statements[10])

    passed = False
    while not passed:
        if allow_choosing:
            task = input("      Choose an option: >> ")
            passed = check_input(task, "number", 2)
        else:
            task = "1"
            passed = True

    if task == "1":
        # Get name of tournament
        tournament = input("      What is the name of the tournament? >> ")
        tournament = "".join(
            _ for _ in tournament if _ in string.ascii_letters + string.digits + " "
        )

        # Collect # of Participants
        passed = False
        while not passed:
            num_slots = input("\n      Enter the number of participants: >> ")
            passed = check_input(num_slots, "number", 100000000)
            num_slots = int(num_slots)
        registrations = {
            slot: {"First Name": None, "Last Name": None}
            for slot in range(1, num_slots + 1)
        }
    else:
        print("      File Options")
        for i, item in enumerate(possible_files):
            print(f"      {i+1}. {item}")
        passed = False
        while not passed:
            picked_file = input("      Choose which file to load: >> ")
            passed = check_input(picked_file, "number", len(possible_files))
        file_path = possible_files[int(picked_file) - 1]

        with open(f"{file_path}", "r") as file:
            data = file.read().split("\n")
            file.close()

        new_data = [_.split(",") for _ in data][1:]
        registrations = {}
        for i, item in enumerate(new_data):
            first = None if item[1] == 'None' else item[1]
            second = None if item[2] == 'None' else item[2]
            registrations[int(item[0])] = {"First Name": first, "Last Name": second}
        tournament = file_path.replace("_registrations.csv","").replace("-"," ")

    return registrations, tournament


def check_input(input_string, requirement, limit):
    if requirement == "number":
        if input_string.isnumeric():
            if int(input_string) in range(1, limit + 1):
                passed = True
            else:
                print(
                    "      The number you have entered is unrealistic. Please try again"
                )
                passed = False
        else:
            print("      You must enter a valid number. Please try again")
            passed = False
    else:
        cleaned_length = len(
            "".join(_ for _ in input_string if _ in string.ascii_letters + " ")
        )
        if cleaned_length == len(input_string):
            passed = True
        else:
            print("      You must enter a valid name. Please try again")
            passed = False
    return passed


def main_menu(registrations, tournament):
    # registrations = {slot: None for slot in range(1, num_slots + 1)}
    num_slots = len(registrations)
    # available_slots = num_slots
    outer_passed = False
    while not outer_passed:
        available_slots = num_slots - len(
            [_ for _ in registrations.keys() if registrations[_]["First Name"] != None]
        )
        os.system(clear_term)
        print(statements[1])
        print(
            f"      Available Slots: {available_slots}\n      Filled Slots: {num_slots - available_slots}\n"
        )
        print(statements[2])

        passed = False
        while not passed:
            print(registrations)
            menu_option = input("      Please choose a task: >> ")
            passed = check_input(menu_option, "number", 5)
        menu_option = int(menu_option)
        if menu_option == 1:
            registrations, saved = sign_up_menu(registrations)
        elif menu_option == 2:
            registrations, saved = deregister_menu(registrations)
        elif menu_option == 3:
            view_participants(registrations)
        elif menu_option == 4:
            saved = save_menu(registrations, tournament)
        elif menu_option == 5:
            outer_passed = exit_menu(saved)


def sign_up_menu(registrations):
    os.system(clear_term)
    print(statements[3])
    name_picked = False
    passed = False
    while not passed:
        if not name_picked:
            name = input("      Participant Name: >> ")
            passed = check_input(name, "string", None)
            name_picked = True

        if name_picked:
            desired_slot = input(
                f"      Desired Starting Slot [1-{len(registrations)}]: >> "
            )
            passed = check_input(desired_slot, "number", len(registrations))
        if passed:
            desired_slot = int(desired_slot)
            if registrations[desired_slot]["First Name"] != None:
                print(f"      Slot #{desired_slot} is filled. Please try again")
                passed = False
            else:
                split_name = name.strip().rsplit(" ", 1)
                registrations[desired_slot]["First Name"] = split_name[0].upper()
                registrations[desired_slot]["Last Name"] = split_name[1].upper()

    print(f"      {name.upper()} is signed up in starting slot #{desired_slot}")
    return registrations, False


def deregister_menu(registrations):
    os.system(clear_term)
    print(statements[4])
    passed = False
    while not passed:
        current_slot = input(f"      Current Slot [1-{len(registrations)}]: >> ")
        name = input("      Participant Name: >> ")
        passed = check_input(current_slot, "number", len(registrations))
        if passed:
            current_slot = int(current_slot)
            full_name = (
                str(registrations[current_slot]["First Name"])
                + " "
                + str(registrations[current_slot]["Last Name"])
            )

            if full_name == name.upper():
                registrations.update(
                    {current_slot: {"First Name": None, "Last Name": None}}
                )
                print("\n      Success:")
                print(
                    f"      {name.upper()} has been cancelled from slot {current_slot}."
                )
                go_again = (
                    "\n      Would you like to cancel another participant? (y/n) >> "
                )
                passed = False if input(go_again).lower() == "y" else True
            else:
                print("\n      Error:")
                print(f"      {name.upper()} is not in that starting slot.\n")
                passed = False

    return registrations, False

def sort_participants(reg_list,sort_parameter, sort_direction):
    sorted_reg = sorted(
        reg_list, key=lambda x: x[sort_parameter], reverse = sort_direction
    )
                
    sorted_reg_string = (
        "\n".join(str(_[0]) + ": " + _[1] + " " + _[2] for _ in sorted_reg)
    )
    sorted_reg_string = sorted_reg_string.replace("None None","[empty]")
    print(sorted_reg_string)
    
    passed = False
    while not passed:
        passed = True if input("Go Back: (y/n) >> ").lower() == 'y' else False
    return

def view_participants(registrations):
    errors = None
    outer_passed = False
    while not outer_passed:
        os.system(clear_term)
        print(statements[5], statements[11], errors,'\n')
        print("******* CURRENTLY IN DEVELOPMENT **********")
        errors = None
        reverse_sort = False
        passed = False
        while not passed:
            option = input('Choose an option: (include "a" for ascending)>> ')
            
            # Check for directional adjustment
            if 'a' in option.lower():
                option = option.replace('a','')
                reverse_sort = True
                
            passed = check_input(option, 'number', 6)
        option = int(option)
        
        if option == 1:
            print('This option has not yet been coded')
        elif option == 2:
            print('This option has not yet been coded')
        elif option == 3:
            reg_list = convert_dict_to_list(registrations)
            reg_list = [[int(_.split(",")[0]),_.split(",")[1],_.split(",")[2]] for _ in reg_list]
            sort_participants(reg_list, 1, reverse_sort)
        elif option == 4:
            reg_list = convert_dict_to_list(registrations)
            reg_list = [[int(_.split(",")[0]),_.split(",")[1],_.split(",")[2]] for _ in reg_list]
            sort_participants(reg_list, 2, reverse_sort)
        elif option == 5:
            reg_list = convert_dict_to_list(registrations)
            reg_list = [[int(_.split(",")[0]),_.split(",")[1],_.split(",")[2]] for _ in reg_list]
            sort_participants(reg_list, 0, reverse_sort)
        elif option == 6:
            return
        else:
            errors = "You did not pick a valid option."


    


def convert_dict_to_list(registrations):
    registration_list = [
        str(key)
        + ","
        + str(registrations[key]["First Name"])
        + ","
        + str(registrations[key]["Last Name"])
        for key in registrations.keys()
    ]
    return registration_list


def save_menu(registrations, tournament):
    os.system(clear_term)
    print(statements[6])
    to_write = convert_dict_to_list(registrations)
    to_write.insert(0, "slot,First Name,Last Name")
    tournament = tournament.replace(" ", "-")
    with open(f"{tournament}_registrations.csv", "w") as file:
        file.write("\n".join(to_write))
        file.close()
    saved = True
    return saved


def exit_menu(unsaved_changes):
    os.system(clear_term)
    print(statements[7])
    if unsaved_changes:
        print("      Any unsaved changes will be lost.")
    confirm = input("      Are you sure you want to exit? [y/n] >> ")
    if confirm.lower() == "y":
        print(statements[8])
        # raise SystemExit
        return True


statements = get_statements()
print(statements[0])

# Control Access
input("      User Name: >> ")
input("       Password: >> ")
os.system(clear_term)


registrations, tournament = get_tournament_info()
main_menu(registrations, tournament)
