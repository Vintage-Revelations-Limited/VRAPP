import pandas as pd
import os


def get_pass_csv():
    pass_filename = "passcsv"
    pass_df = pd.read_csv('csv\pass\\' + pass_filename + '.csv')
    drop_columns = ["GPA Timesheet Record ID", "GPA Reference", "Funder Name", "Pay Breakdown", "GPA Record Item IDS", "Weekday Actual Duration (Minutes)", "Weekday Actual Duration (Hours)",
                "Weekend Actual Duration (Minutes)", "Weekend Actual Duration (Hours)", "Overtime Duration (Minutes)", "Overtime Duration (Hours)", "Total Travel Time (Minutes)",
                "Travel Pay", "Total Holiday Pay", "Total Pay", "Total Gross (Pay with Expenses, Travel and Mileage)", "Mileage Pay", "Expenses Pay", "Customer SS Number"]
    #pass_df = pass_df.drop(columns=drop_columns)
    print("Successfully imported pass CSV")
    return pass_df

def get_weekly_cm_csv():
    None


def get_monthly_cm_csv():
    
    monthly_df = pd.DataFrame()
    file_num = len(os.listdir("csv/cm"))
    
    for i in range(file_num):
        filename = "cm" + str( i + 1) + ".csv"
        try: 
            print("Attempting to import" + filename +  " from csv/cm folder")
            tmp_df = pd.read_csv("csv/cm/" + filename) 
            print("Succesfully imported " + filename)
            monthly_df = pd.concat([tmp_df, monthly_df])
        except: 
            print("Could not find " + filename + " in csv/cm folder, please check this exists and try again")
    return monthly_df