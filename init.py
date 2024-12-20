import importCSV as csv
import compare as com
import employee as em
import client as cl

cm_df = csv.get_monthly_cm_csv()
pass_df = csv.get_pass_csv()
actual_events = {}
employee_set = set()
employee_list = []
client_set = set()
client_list = []

def populate_employees():
    for entry in range(len(cm_df.index)):
        employee_set.add(str(cm_df["Actual Care Worker Forename"].iloc[entry]).lower() + " " + str(cm_df["Actual Care Worker Surname"].iloc[entry]).lower())
    for entry in range(len(pass_df.index)):
        employee_set.add(str(pass_df["Employee Name"].iloc[entry]).lower())
    for e in employee_set:
        employee_list.append(em.Employee(e))
    print("Employees indetified")
    com.remove_employees(["nan nan", "jamie test", "to be cancelled", "cancelled visit", "cancelled visit 2"], employee_list)

def populate_clients():
    for entry in range(len(cm_df.index)):
        client_set.add(str(cm_df["Client Forename"].iloc[entry]).lower() + " " + str(cm_df["Client Surname"].iloc[entry]).lower())
    for entry in range(len(pass_df.index)):
        client_set.add(str(pass_df["Customer Name"].iloc[entry]).lower())
    for e in client_set:
        client_list.append(cl.client(e))
    print("Clients indetified")

def find_descrepenies():
       missing_start = []
       missing_finish = []
       missing_start_and_finish = []

       for i in range(cm_df.index):
            if cm_df["Planned Start Time"].iloc[i].lower() == "nan":
                if cm_df["Planned End Time"].iloc[i].lower() == "nan":
                   missing_start_and_finish.append(cm_df.loc[i])
                else:
                   missing_start.append(cm_df.loc[i])
            elif cm_df["Planned End Time"].iloc[i].lower() == "nan":
               missing_finish.append(cm_df.loc[i])

def add_cm_event_to_person(series, name, person_list):
    for e in person_list:
        if e.name.lower() == name.lower():
            e.list_of_cm_events.append(series)

def add_pass_event_to_person(series, name, person_list):
    for e in person_list:
        if e.name.lower() == str(name).lower():
                e.list_of_pass_events.append(series)


def fill_employee_events():
    print("Generating totals, please wait")
    print("Collecting hours data...")
    for index in range(len(cm_df.index)):
        add_cm_event_to_person(cm_df.iloc[index], str(cm_df["Actual Care Worker Forename"].iloc[index]) + " " + str(cm_df["Actual Care Worker Surname"].iloc[index]), employee_list)
    for index in range(len(pass_df.index)):
        add_pass_event_to_person(pass_df.iloc[index], pass_df["Employee Name"].iloc[index], employee_list)
    for e in employee_list:
        e.to_df()
        e.calc_hours()

def fill_client_events():
    print("Generating clients, please wait")
    for index in range(len(cm_df.index)):
        add_cm_event_to_person(cm_df.iloc[index], str(cm_df["Client Forename"].iloc[index]) + " " + str(cm_df["Client Surname"].iloc[index]), client_list)
    for index in range(len(pass_df.index)):
        add_pass_event_to_person(pass_df.iloc[index], pass_df["Customer Name"].iloc[index], client_list)
    for e in client_list:
        e.to_df()
        e.calc_hours()

def init_for_use():
    populate_employees()
    populate_clients()
    fill_employee_events()
    fill_client_events()