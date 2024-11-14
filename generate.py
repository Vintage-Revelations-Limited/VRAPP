import pandas as pd
import datetime as dt
import compare
import importCSV as csv
import init as ini


key_delimeter = "^"

def generate_monthly_csv_from_employees():
    monthly_csv = pd.DataFrame(columns=["Name", "Hours", "Mileage", "Travel Hours"])
    for e in ini.employee_list:
        monthly_csv.loc[len(monthly_csv.index)] = [e.employee_name, e.hours, e.mileage, e.travel_hours]
    print("csv generated in monthly_roundups folder")
    monthly_csv.to_csv("csv/monthly_roundups/roundup_" + dt.datetime.now().strftime("%d_%m_%y_%H%M%S") + ".csv")

def generate_hours_csv_from_employee(e):
    csv = pd.DataFrame(columns=["Name", "Hours", "Mileage", "Travel Hours"])
    csv.loc[len(csv.index)] = [e.employee_name, e.hours, e.mileage, e.travel_hours]
    print("csv generated in employee_csv folder")
    csv.to_csv("csv/employee_csv/" + e.employee_name + "_HOURS" + dt.datetime.now().strftime("%d_%m_%y_%H%M%S") + ".csv")

def generate_visits_csv_from_employee(e):
    events = extract_keys_from_datetime(e.personal_cm_df, e.personal_pass_df)
    csv = pd.DataFrame(columns=["Date", "Time", "Name", "Client name", "Duration (Hours)"])
    keys = []
    count = 0
    total_duration = 0
    for ev in events:
        val = validate_event_from_key(ev, e.personal_pass_df)
        if val is not None:
            keys.append(val)
    for k in keys:
            vals = k.split(key_delimeter)
            total_duration += float(vals[4])
            csv.loc[count] = pd.Series({"Date": vals[0], "Time" : vals[1], "Name": vals[2], "Client name" : vals[3], "Duration (Hours)" : round(float(vals[4]), 2)})
            count += 1
    csv.loc[count] = pd.Series({"Date": "", "Time" : "", "Name": "", "Client name" : "", "Duration (Hours)" : "Total: " + str(round(float(total_duration), 2))})
    print("csv generated in employee_csv folder")
    csv.to_csv("csv/employee_csv/" + e.employee_name + "_VISITS" + dt.datetime.now().strftime("%d_%m_%y_%H%M%S") + ".csv")


def extract_keys_from_datetime(cm_df, pass_df):
    events  = set()
    for i in range(len(cm_df.index)):
        date = cm_df["Date"].iloc[i]
        time = cm_df["Planned Start Time"].iloc[i]
        name = str(cm_df["Planned Care Worker Forename"].iloc[i]) + " " + str(cm_df["Planned Care Worker Surname"].iloc[i])
        client_name = cm_df["Client Forename"].iloc[i] + " " + cm_df["Client Surname"].iloc[i]
        events.add(generate_event_key(date, time, name, client_name))
    for i in range(len(pass_df.index)):
        date = compare.convert_pass_date_to_standard(pass_df["Planned Date"].iloc[i].split("/"))
        time = compare.strip_pass_time(pass_df["Planned Time"].iloc[i])
        name = pass_df["Employee Name"].iloc[i]
        client_name = pass_df["Customer Name"].iloc[i]
        events.add(generate_event_key(date, time, name, client_name))
    return events

def validate_event_from_key(key, pass_df):
    keys = key.split(key_delimeter)
    for i in range(len(pass_df.index)):
        date = compare.convert_pass_date_to_standard(pass_df["Planned Date"].iloc[i].split("/"))
        pt = compare.strip_pass_time(pass_df["Planned Time"].iloc[i])
        name = pass_df["Employee Name"].iloc[i].lower()
        if keys[0] == str(date) and keys[1] == pt and keys[2] == name:
            duration = pass_df["Total Actual Duration (Hours)"].iloc[i]
            return key + key_delimeter + str(duration)


def generate_event_key(date, time, name, client_name):
    return str(date) + key_delimeter + str(time) + key_delimeter + name.lower() + key_delimeter + client_name.lower()

def generate_discrepency_report(t):
    cm_df = csv.get_monthly_cm_csv()
    pass_df = csv.get_pass_csv()

    if t == "PASS":
        pass_keys = compare.on_pass_not_on_cm_keys(pass_df, cm_df)
        on_pass_not_cm = pd.DataFrame(columns=["Date", "Time", "Employee", "Client", "Duration"])
        for pass_key in pass_keys:
            keys = pass_key.split(key_delimeter)
            on_pass_not_cm.loc[len(on_pass_not_cm.index)] =  [keys[0], keys[1], keys[2], keys[3], keys[4]]

        on_pass_not_cm.to_csv("csv/employee_csv/on_pass_not_cm_" + dt.datetime.now().strftime("%d_%m_%y_%H%M%S") + ".csv")
    elif t == "CM":
        cm_keys = compare.on_cm_not_on_pass_keys(pass_df, cm_df)
        on_cm_not_pass = pd.DataFrame(columns=["Date", "Time", "Employee", "Client", "Duration"])
        for cm_key in cm_keys:
            keys = cm_key.split(key_delimeter)
            on_cm_not_pass.loc[len(on_cm_not_pass.index)] =  [keys[0], keys[1], keys[2], keys[3], keys[4]]
        on_cm_not_pass.to_csv("csv/employee_csv/on_cm_not_pass_" + dt.datetime.now().strftime("%d_%m_%y_%H%M%S") + ".csv")

def generate_partial_report():
    cm_df = csv.get_monthly_cm_csv()
    partials = pd.DataFrame(columns=["Date", "Carer first name", "Carer last name", "Client first name", "Client last name"])
    for x in range(len(cm_df.index)):
        if str(cm_df["Actual End Time"].iloc[x]).lower() == "nan":
            partials.loc[len(partials.index)] = [cm_df["Date"].iloc[x],
                                                cm_df["Actual Care Worker Forename"].iloc[x],
                                                cm_df["Actual Care Worker Surname"].iloc[x],
                                                cm_df["Client Forename"].iloc[x],
                                                cm_df["Client Surname"].iloc[x]]
    partials.to_csv("csv/employee_csv/partials_" + dt.datetime.now().strftime("%d_%m_%y_%H%M%S") + ".csv")
def generate_sub_50_report():
    sub_50 = []

    for e in ini.employee_list:
        sub_50 += e.under_50_dur
    df = pd.DataFrame(sub_50)
    df = df.drop_duplicates()
    df.to_csv("csv/employee_csv/sub_50_report_" + dt.datetime.now().strftime("%d_%m_%y_%H%M%S") + ".csv")
    