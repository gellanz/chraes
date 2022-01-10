import pandas as pd
import json

def create_id(df):
    df["id"] = df["Asignatura"] + df["Grupo"]
    return df

def cleaning_nan(df):
    df = df[df["Grupo"].notna()]
    return df

def concat_sort(df1, df2):
    df1 = df1.sort_values("id").reset_index(drop=True)
    df2 = df2.sort_values("id").reset_index(drop=True)
    df_complete = pd.concat([df1, df2], join="inner", axis=1)
    df_complete = df_complete.loc[:,~df_complete.columns.duplicated()]
    return df_complete

def to_json_api(df, career):
    courses_keys = df.columns.tolist()
    processed_courses = df.values.tolist()
    data = [dict(zip(courses_keys, course)) for course in processed_courses]
    api = {"courses": data}
    with open(f'{career}_data.json', 'w') as f:
        json.dump(api, f)

M_schedule = pd.read_csv("Web_scraper/Data2022_2/mechatronics_schedules.csv")
M_ocupability = pd.read_csv("Web_scraper/Data2022_2/mechatronics_ocupability.csv")
B_schedule = pd.read_csv("Web_scraper/Data2022_2/bionics_schedules.csv")
B_ocupability = pd.read_csv("Web_scraper/Data2022_2/bionics_ocupability.csv")
T_schedule = pd.read_csv("Web_scraper/Data2022_2/telematics_schedules.csv")
T_ocupability = pd.read_csv("Web_scraper/Data2022_2/telematics_ocupability.csv")

careers_dfs = [M_schedule, B_schedule, T_schedule, M_ocupability, B_ocupability, T_ocupability]
careers = {"Mechatronics": (M_schedule, M_ocupability), "Bionics": (B_schedule, B_ocupability), "Telematics": (T_schedule, T_ocupability)}

for career_df in careers_dfs:
    career_df = create_id(career_df)

for schedule_df in [M_schedule, B_schedule, T_schedule]:
    schedule_df = cleaning_nan(schedule_df)

for career_name in careers.keys():
    career_full = concat_sort(careers[career_name][0], careers[career_name][1])
    to_json_api(career_full, career_name)

