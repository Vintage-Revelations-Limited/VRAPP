import math

pass_visit_list = ["Personal care", "Companionship", "Sleeping night", "Waking night","Welfare, Shopping", "Cleaning", "Training", "Supervision", "Pick Up/Off"]
visit_list = ["Personal care", "Companionship", "Sleeping night", "Waking night","Welfare, Shopping", "Cleaning"]
##on pass not cm that matter = Personal care, Companionship, Sleeping night, Waking night, Welfare, Shopping, Cleaning


HOURS_THRESHOLD = 2.5
key_delimeter = "^"


def convert_pass_date_to_standard(date):
    date_nums= date.split("/")
    if len(date_nums[0]) < 2:
        date_nums[0] = "0" + date_nums[0]
    if len(date_nums[1]) < 2:
        date_nums[1] = "0" + date_nums[1]
    if len(date_nums[2]) > 2:
        date_nums[2] = date_nums[2][2:]
    return date_nums[1] + "/" + date_nums[0] + "/" + date_nums[2]

def strip_pass_time(pass_time):
    pass_time = str(pass_time)
    return pass_time[0:5]

def convert_cm_date_to_standard(date):
    date_nums = date.split("/")
    if len(date_nums[2]) > 2:
        date_nums[2] = date_nums[2][2:]
    return date_nums[0] + "/" + date_nums[1] + "/" + date_nums[2]

def is_pass_visit_type(visit_type):
    return visit_type in pass_visit_list


def is_visit_type(visit_type):
    return visit_type in visit_list

def remove_employees(list_to_remove, employee_list):
    for i in list_to_remove:
        for e in employee_list:
            if i == e.employee_name:
                employee_list.remove(e)

def is_twilight(begin_time, end_time, check_time):
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time
    
def convert_to_hours_value(duration):
    hours = 0
    elapsed = 0
    if duration >= 1:
        hours = math.floor(duration)
        minutes = ((duration % 1) * 100) / 60
        elapsed = hours + minutes
    else:
        elapsed = (duration * 100) / 60
    return elapsed


def get_confirmed_event_indexes(date, time, client_name, df_to_get_indexes_from):
    indexes = []
    date  = convert_cm_date_to_standard(date)
    for j in range(len(df_to_get_indexes_from.index)):
        p_time = strip_pass_time(df_to_get_indexes_from["Planned Time"].iloc[j])
        p_date = convert_pass_date_to_standard(df_to_get_indexes_from["Planned Date"].iloc[j])
        p_client = df_to_get_indexes_from["Customer Name"].iloc[j].lower()
        if (p_time == time and p_date == date and p_client == client_name.lower()):
                indexes.append(j)
    return indexes

def is_less_than_50_dur(duration, planned_duration):
    if isinstance(duration, float) or isinstance(planned_duration, float):
        return True
    duration = duration.replace(":", ".")
    planned_duration = planned_duration.replace(":", ".")
    percent = (float(duration)/float(planned_duration)) * 100
    return percent < 50
    

def on_pass_not_on_cm_keys(pass_df, cm_df):
    pass_keys = set()
    cm_keys = set()
    fuzzy_remove = set()

    for i in range(len(pass_df.index)):
        date = pass_df["Planned Date"].iloc[i]
        p_time = pass_df["Planned Time"].iloc[i]

        if is_visit_type(pass_df["Visit/ Event Type"].iloc[i]):
            pass_keys.add(create_duration_key(convert_pass_date_to_standard(date),
                    strip_pass_time(p_time),
                    pass_df["Employee Name"].iloc[i].lower(),
                    pass_df["Customer Name"].iloc[i].lower(),
                    str(pass_df["Total Planned Duration (Hours)"].iloc[i])))
    for j in range(len(cm_df.index)):
        plnd_cw_name = str(cm_df["Planned Care Worker Forename"].iloc[j]).lower() + " " + str(cm_df["Planned Care Worker Surname"].iloc[j]).lower()
        actual_cw_name = str(cm_df["Actual Care Worker Forename"].iloc[j]).lower() + " " + str(cm_df["Actual Care Worker Surname"].iloc[j]).lower()
        
        plnd_time = cm_df["Planned Start Time"].iloc[j]
        actual_time = cm_df["Actual Start Time"].iloc[j]

        duration_str = cm_df["Planned Duration"].iloc[j]

        if isinstance(duration_str, float):
            duration = 0
        else:
            duration = duration_str.replace(":", ".")
            duration = convert_to_hours_value(float(duration))


        cm_keys.add(create_duration_key(convert_cm_date_to_standard(cm_df["Date"].iloc[j]),
                  actual_time,
                  actual_cw_name,
                  str(cm_df["Client Forename"].iloc[j].lower()) + " " + str(cm_df["Client Surname"].iloc[j]).lower(),
                  str(duration)))
        cm_keys.add(create_duration_key(convert_cm_date_to_standard(cm_df["Date"].iloc[j]),
                  actual_time,
                  plnd_cw_name,
                  str(cm_df["Client Forename"].iloc[j].lower()) + " " + str(cm_df["Client Surname"].iloc[j]).lower(),
                  str(duration)))
        cm_keys.add(create_duration_key(convert_cm_date_to_standard(cm_df["Date"].iloc[j]),
                  plnd_time,
                  actual_cw_name,
                  str(cm_df["Client Forename"].iloc[j].lower()) + " " + str(cm_df["Client Surname"].iloc[j]).lower(), 
                  str(duration)))
        cm_keys.add(create_duration_key(convert_cm_date_to_standard(cm_df["Date"].iloc[j]),
                  plnd_time,
                  plnd_cw_name,
                  str(cm_df["Client Forename"].iloc[j].lower()) + " " + str(cm_df["Client Surname"].iloc[j]).lower(),
                  str(duration)))
    difference = pass_keys - cm_keys
    fuzzy_remove = generate_fuzzy_set(difference, cm_keys)
    final = difference - fuzzy_remove
    return final


def on_cm_not_on_pass_keys(pass_df, cm_df):
    pass_keys = set()
    cm_keys = set()
    fuzzy_remove = set()

    for i in range(len(pass_df.index)):
        date = pass_df["Planned Date"].iloc[i]
        p_time = pass_df["Actual TIme"].iloc[i]

        if is_pass_visit_type(pass_df["Visit/ Event Type"].iloc[i]):
            pass_keys.add(create_duration_key(convert_pass_date_to_standard(date),
                    strip_pass_time(p_time),
                    pass_df["Employee Name"].iloc[i].lower(),
                    pass_df["Customer Name"].iloc[i].lower(),
                    str(pass_df["Total Planned Duration (Hours)"].iloc[i])))
    for j in range(len(cm_df.index)):
        plnd_cw_name = str(cm_df["Planned Care Worker Forename"].iloc[j]).lower() + " " + str(cm_df["Planned Care Worker Surname"].iloc[j]).lower()
        actual_cw_name = str(cm_df["Actual Care Worker Forename"].iloc[j]).lower() + " " + str(cm_df["Actual Care Worker Surname"].iloc[j]).lower()
        if actual_cw_name != "nan nan":
            name = actual_cw_name
        elif plnd_cw_name != "nan nan":
            name = plnd_cw_name
        else:
            name = "NO DATA"

        plnd_time = str(cm_df["Planned Start Time"].iloc[j])
        actual_time = str(cm_df["Actual Start Time"].iloc[j])

        if actual_time != "nan":
            time = actual_time
        elif plnd_time != "nan":
            time = plnd_time
        else:
            time = "NO DATA"

        plnd_dur = str(cm_df["Planned Duration"].iloc[j])
        actual_dur = str(cm_df["Actual Duration"].iloc[j])
        
        if plnd_dur != "nan":
            duration_str = plnd_time
            duration = duration_str.replace(":", ".")
            duration = duration[0:5]
            duration = convert_to_hours_value(float(duration))
        elif actual_dur != "nan":
            duration_str = actual_time
            duration = duration_str.replace(":", ".")
            duration = duration[0:5]
            duration = convert_to_hours_value(float(duration))
        else:
            duration_str = "NO DATA"
        cm_keys.add(create_duration_key(convert_cm_date_to_standard(cm_df["Date"].iloc[j]),
                  time,
                  name,
                  str(cm_df["Client Forename"].iloc[j].lower()) + " " + str(cm_df["Client Surname"].iloc[j]).lower(),
                  str(duration)))
    difference = cm_keys - pass_keys
    fuzzy_remove = generate_fuzzy_set(difference, pass_keys)
    final = difference - fuzzy_remove
    return final

def pass_df_to_keys(pass_df):
    pass_keys = set()
    for i in range(len(pass_df.index)):
        date = pass_df["Planned Date"].iloc[i]
        p_time = pass_df["Planned Time"].iloc[i]
        pass_keys.add(create_key(convert_pass_date_to_standard(date),
                strip_pass_time(p_time),
                pass_df["Employee Name"].iloc[i].lower(),
                pass_df["Customer Name"].iloc[i].lower()))
    return pass_keys

def cm_df_to_keys(cm_df):
    cm_keys = set()
    for i in range(len(cm_df.index)):
        date = cm_df["Date"].iloc[i]
        p_time = cm_df["Planned Start Time"].iloc[i]
        cm_keys.add(create_key(convert_cm_date_to_standard(date),
                strip_pass_time(p_time),
                str(cm_df["Planned Care Worker Forename"].iloc[i]).lower() + " " + str(cm_df["Planned Care Worker Surname"].iloc[i]).lower(),
                str(cm_df["Client Forename"].iloc[i]).lower() + " " + str(cm_df["Client Surname"].iloc[i]).lower()))
    return cm_keys

def calc_travel_data(self):
    for j in range((len(self.personal_pass_df.index))):
        self.travel_hours += self.personal_pass_df["Total Travel Time (Hours)"].iloc[j]
        self.mileage += self.personal_pass_df["Mileage"].iloc[j]

def create_key(date, time, employee, customer):
    return str(date) + key_delimeter + str(time) + key_delimeter + employee + key_delimeter + customer

def create_duration_key(date, time, employee, customer, duration):
    return str(date) + key_delimeter + str(time) + key_delimeter + employee + key_delimeter + customer + key_delimeter + duration

def fuzzy_time_check(time1_hours, time2_hours, max_change_hours):
    return time1_hours - time2_hours <= max_change_hours and time1_hours - time2_hours >= max_change_hours * -1

def generate_fuzzy_set(difference, keys_to_remove):
    fuzzy_remove = set()
    for d in difference:
        d_keys = d.split(key_delimeter)
        for p in keys_to_remove:
            keys = p.split(key_delimeter)
            if len(keys) > 1:
                time1 = keys[1].replace(":", ".")
                time1 = time1[:5]
            time2 = d_keys[1].replace(":", ".")
            time2 = time2[:5]
            if fuzzy_time_check(convert_to_hours_value(float(time1)), convert_to_hours_value(float(time2)), HOURS_THRESHOLD) and keys[3] == d_keys[3] and keys[0] == d_keys[0] and keys[2] == d_keys[2]:
                fuzzy_remove.add(d)
    return fuzzy_remove
       
