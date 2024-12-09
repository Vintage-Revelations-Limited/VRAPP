import pandas as pd
import datetime as dt
import compare as com

class Employee:
    def __init__(self, employee_name):
        self.employee_name = employee_name
        self.hours = 0
        self.mileage = 0
        self.travel_hours = 0
        self.list_of_cm_events = []
        self.list_of_pass_events = []
        self.personal_cm_df = None
        self.personal_pass_df = None
        self.under_50_dur = []
        self.non_contact_events = ["Office/Field Time", "Training", "Supervision"]
    def to_df(self):
        self.personal_cm_df = pd.DataFrame(self.list_of_cm_events)
        self.personal_pass_df = pd.DataFrame(self.list_of_pass_events)
        
    def percentage_duration_check(self, index):
        if com.is_less_than_50_dur(self.personal_cm_df["Actual Duration"].iloc[index], self.personal_cm_df["Planned Duration"].iloc[index]):
            self.under_50_dur.append(self.personal_cm_df.iloc[index])



    def calc_hours(self):
        r = len(self.personal_cm_df.index)
        for index in range(r):
            self.percentage_duration_check(index)
            duration = float(str(self.personal_cm_df["Actual Duration"].iloc[index]).replace(":", "."))
            pln_dur = self.personal_cm_df["Planned Duration"].iloc[index]
            
            if not isinstance(pln_dur, float):
                pln_dur = float(pln_dur.replace(":", "."))
            else:
                pln_dur = duration
            try:
                time = dt.datetime.strptime(str(self.personal_cm_df['Planned Start Time'].iloc[index][0:5]), "%H:%M").time()
            except:
                time = dt.datetime.strptime(str(self.personal_cm_df['Actual Start Time'].iloc[index][0:5]), "%H:%M").time()
            if com.is_twilight(dt.time(22, 0), dt.time(3, 30), time):
                if(str(self.personal_cm_df["Planned Duration"].iloc[index]).lower() != "nan"):
                    pln_dur = float(self.personal_cm_df["Planned Duration"].iloc[index].replace(":", "."))
                else:
                    pln_dur = duration
                self.hours += com.convert_to_hours_value(pln_dur)
            else:
                self.hours += com.convert_to_hours_value(duration)

        for j in range(len(self.personal_pass_df.index)):
            if self.personal_pass_df["Visit/ Event Type"].iloc[j] in self.non_contact_events:
                self.hours += float(self.personal_pass_df["Total Planned Duration (Hours)"].iloc[j])

    def print_hours(self):
        print("Events: " + str(len(self.personal_cm_df.index)))
        print(self.employee_name)
        print("Hours: " + str(self.hours))
        print("Mileage: " + str(self.mileage))
        print("Travel hours: " + str(self.travel_hours))
    
    def print_visits(self):
        pd.set_option("display.max_columns", None)
        pd.set_option('display.max_colwidth', None)
        pd.set_option("display.expand_frame_repr", False)
        print(self.personal_cm_df)
        print(self.personal_pass_df)