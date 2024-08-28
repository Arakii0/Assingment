import os
from api import get_api
##################################################################################
# THIS FUNCTION READS THE INFO FILE AT THE START OF THE PROGRAM AND STORES IT IN A LIST
def read_data_info(file):
    with open(file, 'r') as f:
        carpark_info = []
        for i in f:
            carpark_info.append(i.strip().split(',', maxsplit=3))

        carpark_info_done = []

        # FOR EVERY NEW CARPARK LOCATION
        for i in range(1, len(carpark_info)):
            carpark_info_dict = {}

            # CREATES THE KEYS FIRST
            for j in carpark_info[0]:
                carpark_info_dict[j] = ""

            # THEN APPENDS THE VALUES TO THE KEYS
            for x in range(4):
                carpark_info_dict[carpark_info[0][x]] = carpark_info[i][x]
            carpark_info_done.append(carpark_info_dict)

    return carpark_info_done
##################################################################################
# THIS FUNCTION PRINTS OUT THE MENU AND ALSO ASKS THE USER FOR HIS OPTIONS WITH ERROR HANDLING
def main_menu(done):
    options =  ["Display Total Number of Carparks in 'carpark-information.csv' |",
                "Display All Basement Carparks in 'carpark-information.csv'    |", 
                "Read Carpark Availability Data File                           |", 
                "Print Total Number of Carparks in the File Read in [3]        |", 
                "Display Carparks Without Available Lots                       |", 
                "Display Carparks With At Least x% Available Lots              |", 
                "Display Addresses of Carparks With At Least x% Available Lots |", 
                "Advanced Features                                             |"]
    
    print("MENU")
    print("====================================================================")
    for i in range(len(options)):
        print(f"[{i+1}]  {options[i]}")
    print("[0]  Exit                                                          |")
    print("====================================================================")

    # ASK FOR USER INPUT
    while True:
        try:
            while True:
                user = int(input("Enter your option: "))
                if user not in range(9):
                    print("Not a valid option, please enter again!")
                # CHECKS IF THE USER HAS CHOOSEN THE OPTION 3 FIRST, IF HE DID NOT, HE WILL NOT HAVE ACCESS TO THE OTHER OPTIONS 4-8
                elif user in [4,5,6,7,8] and not done:
                    print("Unable to access file, maybe try to read the file first!")
                else:
                    break
            break
        except ValueError:
            print("Enter an integer please!")

    return user
##################################################################################
# THIS FUNCTION FINDS OUT THE AMOUNT OF CARPARKS AVAILIABLE
def display_carpark(file):
    print()
    print("======================================================================================")
    print(f"Total Number of carparks in 'carpark-information.csv': {len(file)}")
    print("======================================================================================")
##################################################################################
# THIS FUNCTION OUTPUTS THE TOTAL AMOUNT OF CARPARKS WITH NO AVAILABILITY
def display_basement(file):
    print()
    print("======================================================================================")
    print(f"{'Carpark No':<12} {'Carpark Type':<20} {'Address'}")
    print("======================================================================================")
    total = 0
    for i in file:
        if i['Carpark Type'] == 'BASEMENT CAR PARK':
            print(f"{i['Carpark Number']:<12} {i['Carpark Type']:<20} {i['Address']}")
            total += 1
    print(f"Total number: {total}")
    print("======================================================================================")
##################################################################################
# THIS FUNCTION READS THE CARPARK-AVAILABLE FILE AND STORES IT IN A LIST FOR FUTURE USES
def read_data_avail(file):
    with open(file, 'r') as f:
        carpark_avail = []
        for i in f:
            carpark_avail.append(i.strip().split(','))

        # ONLY GETS THE TIMESTAMP OF THE FILE
        timestamp = str(carpark_avail[0]).strip("[]'").removeprefix("Timestamp: ")
        print(f"Timestamp: {timestamp}")

        carpark_avail_done = []

        for i in range(2, len(carpark_avail)):
            carpark_avail_dict = {}

            # GETS THE KEYS FIRST AND STORES IT IN A DICT
            for j in carpark_avail[1]:
                carpark_avail_dict[j] = ""

            # NOW IT GETS THE ACTUAL VALUES AND APPENDS IT TO THE KEYS
            for x in range(3):
                carpark_avail_dict[carpark_avail[1][x]] = carpark_avail[i][x]
            carpark_avail_done.append(carpark_avail_dict)
    return carpark_avail_done
##################################################################################
# THIS FUNCTION FIND THE AMOUNT OF CARPARKS IN THE AVAILABILITY FILE
def display_carpark_avail(file):
    print()
    print("======================================================================================")
    print(f"Total Number of Carparks in the File: {len(file)}")
    print("======================================================================================")
##################################################################################
# THIS FUNCTION SHOWS HOW MANY CARPARKS HAVE NO AVAILABILITY AND PRINTS OUT HE CARPARK ALSO
def no_avail(file):
    print()
    print("======================================================================================")
    total = 0
    for i in file:
        if i['Lots Available'] == '0':
            print(f"Carpark Number: {i['Carpark Number']}")
            total += 1
    print(f"Total number: {total}")
    print("======================================================================================")
##################################################################################
# THIS FUNCTIONS TAKE THE USER'S INPUT AND MAKES SURE TO DISPLAY ONLY CARPARKS THAT HAS AVAILABILITY HIGHER THAN WHAT THE USER PROVIDED
def carparks_percentage_avail(file, percentage):
    print()
    print("======================================================================================")
    print(f"{'Carpark No':<15} {'Total Lots':<15} {'Lots Available':<15} {'Percentage'}")
    print("======================================================================================")
    total = 0
    for i in file:
        
        #USED TRY EXCEPT AS IN THE CASE OF THE TOTAL LOTS BEING ZERO, WE CAN JUST SKIP OVER IT INSTEAD OF CAUSING AN ERROR
        try:
            per = (int(i['Lots Available']) / int(i['Total Lots'])) * 100
            if per >= percentage:
                print(f"{i['Carpark Number']:<20} {i['Total Lots']:>5} {i['Lots Available']:>19} {per:>11.1f}")
                total += 1

        except ZeroDivisionError:
            pass
    print(f"Total number: {total}")
    print("======================================================================================")
##################################################################################
# THIS FUNCTIONS TAKE THE USER'S INPUT AND MAKES SURE TO DISPLAY ONLY CARPARKS THAT HAS AVAILABILITY HIGHER THAN WHAT THE USER PROVIDED WITH THE ADDITION OF THE CARPARK ADDRESS
def address_percentage_avail(avail, info, percentage):
    print()
    print("======================================================================================")
    print(f"{'Carpark No':<15} {'Total Lots':<15} {'Lots Available':<15} {'Percentage':<15} Address")
    print("======================================================================================")
    total = 0
    for i in avail:
        #USED TRY EXCEPT AS IN THE CASE OF THE TOTAL LOTS BEING ZERO, WE CAN JUST SKIP OVER IT INSTEAD OF CAUSING AN ERROR
        try:
            per = (int(i['Lots Available']) / int(i['Total Lots'])) * 100
            if per >= percentage:

                # CHECKS IF THE CARPARK NUMBERS ARE THE SAME BEFORE GETTING THE ADDRESS
                for x in info:
                    if x['Carpark Number'] == i['Carpark Number']:
                        add = x['Address']
                        print(f"{i['Carpark Number']:<20} {i['Total Lots']:>5} {i['Lots Available']:>19} {per:>11.1f}      {add}")
                        total += 1
                        break

        except ZeroDivisionError:
            pass
    print(f"Total number: {total}")
    print("======================================================================================")
##################################################################################
#                               ADVANCED FUNCTIONS                               #
##################################################################################
# THIS FUNCTIONS DISPLAYS ALL CARPARKS AT A GIVEN LOCATION
def carpark_loc(avail, info, location):
    print()
    print("======================================================================================")
    print(f"{'Carpark No':<15} {'Total Lots':<15} {'Lots Available':<15} {'Percentage':<15} Address")
    print("======================================================================================")
    total = 0
    for i in info:

        # CHECKS IF THE LOCATION IS IN THE ADDRESS PORTION OF THE CARPARK
        if location in i['Address']:
            for x in avail:
                if i['Carpark Number'] == x['Carpark Number']:
                    # USED TRY EXCEPT AS IN THE CASE OF THE TOTAL LOTS BEING ZERO, WE CAN JUST SKIP OVER IT INSTEAD OF CAUSING AN ERROR
                    try:
                        add = i['Address'].strip('"')
                        per = (int(x['Lots Available']) / int(x['Total Lots'])) * 100
                        print(f"{x['Carpark Number']:<20} {x['Total Lots']:>5} {x['Lots Available']:>19} {per:>11.1f}      {add}")
                        total += 1
                        break

                    except ZeroDivisionError:
                        pass
    if not total:
        print("Unable to find location given!")
        print("No Carparks Found!")
        print("======================================================================================")
    else:
        print(f"Total number: {total}")
        print("======================================================================================")
##################################################################################
# THIS FUNCTIONS DISPLAYS ONLY THE CARPARK WITH THE MOST PARKING LOTS
def most_parking(avail, info):
    most = 0

    # PREPARE STORING THE CARPARKS INFO
    carpark_no = ''
    total_lots = ''
    lots_avail = ''
    address = ''
    carpark_type = ''
    parking_system = ''

    # IF CARPARK LOTS > MOST, THEN THE WHOLE INFO WILL CHANGE ACCORDINGLY
    for i in avail:
        if int(i['Total Lots']) > most:

            # THIS IS JUST TO GET THE ADDRESS AND THE INFORMATION AFTER KNOWING THAT THIS CARPARK HAS MORE LOTS
            for x in info:
                if x['Carpark Number'] == i['Carpark Number']:
                    carpark_no = x['Carpark Number']
                    total_lots = i['Total Lots']
                    lots_avail = i['Lots Available']
                    address = x['Address']
                    carpark_type = x['Carpark Type']
                    parking_system = x['Type of Parking System']
                    break
            most = int(i['Total Lots'])
    print()
    print("=====================================================================================================================================")
    print(f"{'Carpark No':<15} {'Total Lots':<15} {'Lots Available':<20} {'Carpark Type':<25} {'Parking System':<20} Address")
    print(f"{carpark_no:<20} {total_lots:>5} {lots_avail:>19} {carpark_type:>27} {parking_system:>22}   {address}")
    print("=====================================================================================================================================")
##################################################################################
# THIS FUNCTIONS CREATES AN OUTPUT FILE WITH CARPARK AVAILABILITY WITH ADDRESSES AND SORTS THEM OUT BY THE NUMBER OF LOTS AVAILABLE IN ASCENDING ORDER
def output_updated(ori_avail, avail, info):

    with open(ori_avail, 'r') as f:
        carpark_avail = []
        for i in f:
            carpark_avail.append(i.strip().split(','))

        timestamp = str(carpark_avail[0]).strip("[]'").removeprefix("Timestamp: ")

    # SORT THE DICTIONARY OUT IN ASCENDING ORDER USING THE LOTS AVAILABLE AS THE KEY TO IT.
    # THE key=lambda x: int(x['Lots Available']) TELLS THE SORTED FUNCTION TO SORT THE AVAIL FILE USING 'LOTS AVAILABLE' AS THE NUMBER TO COMPARE

    # def func(x):
    #    return int(x['Lots Available'])   This just returns the number of lots available

    new = sorted(avail, key=lambda x: int(x['Lots Available'])) # lambda makes it so that u don't have to use the def function, the function is one time use
    written = 0
    # SEEN TELLS ME WHICH CARPARK HAS ALREADY BEEN WRITTEN
    seen = set()
    new_file = "carpark-availability-with-addresses.csv"

    # WRITES THE OUTPUT TO A FILE
    with open(new_file, 'w') as f:
        f.write(f"Timestamp: {timestamp}\n")
        f.write("Carpark No,Total Lots,Lots Available,Address\n")
        written += 2
        for i in new:
            for x in info:
                # IF THE CARPARK HAS AN ADDRESS, WE NEED TO PRINT IT WITH THE ADDRESS
                if i['Carpark Number'] == x['Carpark Number']:
                    f.write(f"{i['Carpark Number']},{i['Total Lots']},{i['Lots Available']},{x['Address']}\n")
                    # ADDS THE CARPARK TO THE SEEN SET
                    seen.add(i['Carpark Number'])
                    written += 1
                    break

            # IF THE CARPARK HAS NOT BEEN SEEN IN THE SET() (NO ADDRESS), WE NEED TO STILL PRINT IT WITHOUT ADDRESS
            if i['Carpark Number'] not in seen:
                f.write(f"{i['Carpark Number']},{i['Total Lots']},{i['Lots Available']},ADDRESS NOT FOUND\n")
                # ADDS THE CARPARK TO THE SEEN SET
                seen.add(i['Carpark Number'])
                written += 1

    print()
    print("======================================================================================")                
    print(f"Successfully written {written} lines into: {new_file}")
    print("======================================================================================")
##################################################################################

# THIS STARTS THE APPLICATION

#CHECKS IF THIS FILE IS MEANT TO BE RUN AND NOT A LIBRARY
if __name__ == '__main__':

    print("""===================================
| A Program Written By: Araki Yeo |
| Class: CSF03/P08                |
===================================""")

    # GETS THE PROGRAM READY BY CLEANING THE FILE AND SETTING THE BOOLS
    done = False  # MAKES SURE THAT OPTIONS 4-8 CANNOT BE ACCESSED UNTIL AVAILABILITY FILE IS READ
    info = read_data_info('carpark-information.csv')
    loop = True

    # PROGRAM STARTS
    while loop:

        print()
        # GETS USER INPUT
        choice = main_menu(done)
        
        # THIS IS TO CLEAR THE TERMINAL AFTER EVERY OPTION FOR A CLEANER UI
        os.system('cls' if os.name == 'nt' else 'clear')

        # MATCHES THE USER INPUT TO A NUMBER
        # MATCH CASE IS ESSENTIALLY JUST DOING: if choice == 1:
        #                                          elif choice == 2:
        #                                          elif choice == 3:
        #                                          ...........
        match choice:

            case 1:
                print("Option 1: Display Total Number of Carparks in 'carpark-information.csv'")
                display_carpark(info)
            case 2:
                print("Option 2: Display All Basement Carparks in 'carpark-information.csv'")
                display_basement(info)
            case 3:
                print("Option 3: Read Carpark Availability Data File")
                while True:
                    try:
                        print()
                        # ASKS USER IF THEY WANT TO USE THWEIR OWN FILE OR USE THE API
                        api_or_own = int(input("""======================================
[1] Use Latest Data Available
[2] Use Own File
======================================
input: """))
                        if api_or_own not in [1,2]:
                            print("\nEnter 1 or 2 only!")
                            continue

                        if api_or_own == 1:
                            try:
                                file_name = get_api()
                                avail = read_data_avail(file_name)
                                # MAKES OPTIONS 4-8 AVAILABLE NOW
                                done = True
                                break
                            except:
                                print("Unable to do that, try your own file!")

                        # USER VALIDATION FOR THE FILE THEY WANT TO USE
                        else:
                            while True:
                                try:
                                    print()
                                    file_name = input("Enter the file name: ")
                                    avail = read_data_avail(file_name)
                                    # MAKES OPTIONS 4-8 AVAILABLE NOW
                                    done = True
                                    break
                                except FileNotFoundError:
                                    print("\nEnter the correct file!")
                            break
                    except KeyboardInterrupt:
                        break
                    except ValueError:
                        print("\nEnter an integer only!")

            case 4:
                print("Option 4: Print Total Number of Carparks in the File Read in [3]")
                display_carpark_avail(avail)
            case 5:
                print("Option 5: Display Carparks without Available Lots")
                no_avail(avail)
            case 6:
                print("Option 6: Display Carparks With At Least x% Available Lots")
                # USER VALIDATION
                while True:
                    try:
                        user_per = float(input("Enter percentage required: "))
                        carparks_percentage_avail(avail, user_per)
                        break
                    except ValueError:
                        print("\nEnter an integer!")
            case 7:
                print("Option 7: Display Addresses of Carparks With At Least x% Available Lots")
                # USER VALIDATION
                while True:
                    try:
                        user_per = float(input("Enter percentage required: "))
                        address_percentage_avail(avail, info, user_per)
                        break
                    except ValueError:
                        print("\nEnter an integer only!")
            case 0:
                # ENDS THE PROGRAM
                print("\n=========================================")
                print("| Thank You For Using This Application! |")
                print(f"| {'GoodBye!':^36}  |")
                print("=========================================")
                # BREAKS OUT OF THE MAIN LOOP
                loop = False

##################################################################################

            case 8:
                # THIS IS IF THE USER ENTERS ADVANCED FUNCTION PART WHICH IS THE SECOND PAGE
                while True: # MAKES SURE THAT THIS ADVANCED MENU WILL PRINT AFTER EVERY OPTION ENTERED HERE UNTIL USER WANTS TO RETURN TO BASCI MENU
                    
                    # PRINTS THE MENU
                    options = [f"Display All carparks at Given location {'|':>49}",
                               f"Display Carpark With the Most Parking Lots {'|':>45}",
                               f"Create a New File With Carpark Availability with Addresses and Sorts by Lots Available {'|':>1}"]
                    print()
                    print("MENU")
                    print("=============================================================================================")
                    print(f"[1]  Basic Features {'|':>73}")
                    for i in range(2, len(options)+2):
                        print(f"[{i}]  {options[i-2]}")
                    print(f"[0]  Exit {'|':>83}")
                    print("=============================================================================================")

                    # USER VALIDATION FOR THE OPTION
                    while True:
                        try:
                            while True:
                                user = int(input("\033[95mEnter your option:\033[0m "))
                                if user not in range(5):
                                    print("Not a valid option, please enter again!")
                                else:
                                    break
                            break
                        except ValueError:
                            print("Enter an integer please!")

                    # THIS IS TO CLEAR THE TERMINAL AFTER EVERY OPTION FOR A CLEANER UI
                    os.system('cls' if os.name == 'nt' else 'clear')

                    # MATCHES USER INPUT FOR ADVANCED OPTIONS
                    match user:
                        case 1:
                            break
                        case 2:
                            print("Advanced Option 2: Display All Carpark at Given Location")
                            location = input("Enter the location you want to search for: ").upper()
                            carpark_loc(avail, info, location)
                        case 3:
                            print("Advanced Option 3: Display Carpark With the Most Parking Lots")
                            most_parking(avail, info)
                        case 4:
                            print("Advanced Option 4: Create Output File With Carpark Availability With Addresses and Sort by Lots Available")
                            output_updated(file_name, avail, info)
                        case 0:
                            # ENDS THE PROGRAM
                            print("\n=========================================")
                            print("| Thank You For Using This Application! |")
                            print(f"| {'GoodBye!':^36}  |")
                            print("=========================================")
                            loop = False
                            break
##################################################################################
