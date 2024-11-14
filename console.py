import init as ini
import generate as g

running = True
states = ['i','s', 'g', 'd', 'e', 'f']
state = 'i'
selected_employee = None

def sanitize_key(key):
    key = key.lower()
    if len(key) > 1:
        key = key[0]
    return key
ini.init_for_use()

while(running):
    if state == 'i':
        print("Welcome to VRAPP, please ensure relevant CSV's are place in vrapp/csv/cm and vrapp/csv/pass folders.")
        print("CM csv's should be named cm1, cm2, cm3 etc.. The relating Pass CSV should named passcsv")
        input("Press Enter to continue...")
        print("Please select a function by the corresponding key:")
        print("[S]earch for specific employee details")
        print("[G]enerate a monthly csv for data") 
        print("[D]etect discrepencies between PASS and CM data")
        print("[E]xit")
    
    if state == 'i':
        key = sanitize_key(input())
 
    if not key in states and state == "i":
        print("Incorrect selection, please use the first letter of the function")
    elif state == 'i':
        state = key
    
    if state == 'e':
        running = False

    if state == "g":
        g.generate_monthly_csv_from_employees()
        state = "i"

    if state == 's':
        print("please enter the name as it appears on CM, this is not case sensitive: ")
        name = input()
        for e in ini.employee_list:
            if e.employee_name == name.lower():
                print(name + " has been found")
                state = 'f'
                selected_employee = e
                break
        if not state == 'f':
            print(name + " was not found, please check the spelling and csv files and try again")
    if state == 'f':
        print("What would you like to do with " + name)
        print("[0] Show their hours, mileage and travel hours")
        print("[1] Show their visits")
        print("[2] Save their hours to CSV")
        print("[3] Save their visits to CSV")
        print("[4] Back to main menu")

        key = sanitize_key(input())

        if key == "0":
            selected_employee.print_hours()
            state = "f"
        elif key == "1":
            selected_employee.print_visits()
            state = "f"
        elif key == "2":
            g.generate_hours_csv_from_employee(selected_employee)
            state = "f"
        elif key == "3":
            g.generate_visits_csv_from_employee(selected_employee)
            state = "f"
        elif key == "4":
            state = "i"
        else:
            print("Incorrect selection")
            state = "f"


    if state == "d":
       print("[0] Generate report for PASS discrepencies")
       print("[1] Generate report for CM discrepencies")
       print("[2] Sub 50 percent duration report")
       print("[3] Partial/Planned only on CM report")

       key = input()
       key = sanitize_key(key)
       if key == "0":
           state = "disp"
       elif key == "1":
           state = "disc"
       elif key == "2":
           state = "sub"
       elif key == "3":
           state = "part"     
       else:
           print("incorrect selection")
    if state == "disp":
        print("Generating report, please wait...")
        g.generate_discrepency_report("PASS")
        state = "i"
    if state == "disc":
        print("Generating report, please wait...")
        g.generate_discrepency_report("CM")
        state = "i"
    if state == "sub":
        print("Generating report, please wait...")
        g.generate_sub_50_report()
        state = "i"
    if state == "part":
        print("Generating report, please wait...")
        g.generate_partial_report()
        state = "i"