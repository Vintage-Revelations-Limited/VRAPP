import pandas as pd
import compare as com
import person

class Employee(person.Person):
    def __init__(self, employee_name):
        super().__init__(employee_name)
        
    def percentage_duration_check(self, index):
        if com.is_less_than_50_dur(self.personal_cm_df["Actual Duration"].iloc[index], self.personal_cm_df["Planned Duration"].iloc[index]):
            self.under_50_dur.append(self.personal_cm_df.iloc[index])

    def print_hours(self):
        print("Events: " + str(len(self.personal_cm_df.index)))
        print(self.employee_name)
        print("Hours: "  + str(self.hours))
        print("Mileage: " + str(self.mileage))
        print("Travel hours: " + str(self.travel_hours))
    
    def print_visits(self):
        pd.set_option("display.max_columns", None)
        pd.set_option('display.max_colwidth', None)
        pd.set_option("display.expand_frame_repr", False)
        print(self.personal_cm_df)
        print(self.personal_pass_df)