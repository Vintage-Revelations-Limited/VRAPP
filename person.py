import pandas as pd
import compare as com
import datetime as dt

class Person:
    def __init__(self, name):
        self.name = name
        self.hours = 0
        self.mileage = 0
        self.travel_hours = 0
        self.list_of_cm_events = []
        self.list_of_pass_events = []
        self.personal_cm_df = None
        self.personal_pass_df = None
        self.planned_hours = 0
        self.under_50_dur = []
        self.non_contact_events = ["Office/Field Time", "Training", "Supervision", "Shadowing", "Staff meeting"]
    
    def to_df(self):
        self.personal_cm_df = pd.DataFrame(self.list_of_cm_events)
        self.personal_pass_df = pd.DataFrame(self.list_of_pass_events)
    
    def calc_hours(self):
        r = len(self.personal_cm_df.index)
        for index in range(r):
            duration = float(str(self.personal_cm_df["Actual Duration"].iloc[index]).replace(":", "."))
            pln_dur = self.personal_cm_df["Planned Duration"].iloc[index]

            if str(duration) == "nan":
                duration = 0
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
                self.hours += float(com.convert_to_hours_value(pln_dur))
            else:
                self.hours += float(com.convert_to_hours_value(duration))

        for j in range(len(self.personal_pass_df.index)):
            if self.personal_pass_df["Visit/ Event Type"].iloc[j] in self.non_contact_events:
                self.hours += float(self.personal_pass_df["Total Planned Duration (Hours)"].iloc[j])
            self.travel_hours += self.personal_pass_df["Total Travel Time (Hours)"].iloc[j]
            self.mileage += self.personal_pass_df["Mileage"].iloc[j]
            self.planned_hours += self.personal_pass_df["Total Planned Duration (Hours)"].iloc[j]
