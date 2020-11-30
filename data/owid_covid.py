# Import data analysis dependencies
import pandas as pd

# Import OWID covid data to Pandas dataframe
#df = pd.read_csv('https://covid.ourworldindata.org/data/owid-covid-data.csv')
df = pd.read_csv("data/owid-covid-data_2020-10-19.csv")
df = df[~df['location'].isin(["World"])]

# Convert time to datetime.
df["date"] = pd.to_datetime(df["date"], infer_datetime_format=True).values

# Create a daterange
daterange = pd.date_range(start=df["date"].min(),end=df["date"].max(),freq='M')

y_axis_labels = ["total_cases", "new_cases", "new_cases_smoothed", "total_deaths", "new_deaths", "new_deaths_smoothed", "total_cases_per_million", "new_cases_per_million", "new_cases_smoothed_per_million", "total_deaths_per_million", "new_deaths_per_million", "new_deaths_smoothed_per_million", "reproduction_rate", "icu_patients", "icu_patients_per_million", "hosp_patients", "hosp_patients_per_million", "weekly_icu_admissions", "weekly_icu_admissions_per_million", "weekly_hosp_admissions", "weekly_hosp_admissions_per_million", "total_tests", "new_tests", "new_tests_smoothed", "total_tests_per_thousand", "new_tests_per_thousand", "new_tests_smoothed_per_thousand", "tests_per_case", "positive_rate"]
y_axis_comparison=["total_tests_per_thousand", "new_tests_per_thousand", "new_tests_smoothed_per_thousand", "tests_per_case", "weekly_hosp_admissions_per_million","icu_patients_per_million", "hosp_patients", "hosp_patients_per_million", "weekly_icu_admissions", "weekly_icu_admissions_per_million", "hosp_patients_per_million", "icu_patients_per_million", "reproduction_rate", "total_cases_per_million", "new_cases_per_million", "new_cases_smoothed_per_million", "total_deaths_per_million", "new_deaths_per_million", "new_deaths_smoothed_per_million"]
countries = df["location"].unique()

filters=['population_density', 'median_age', 'aged_65_older',
       'aged_70_older', 'gdp_per_capita', 'extreme_poverty',
       'cardiovasc_death_rate', 'diabetes_prevalence', 'female_smokers',
       'male_smokers', 'handwashing_facilities', 'hospital_beds_per_thousand',
       'life_expectancy', 'human_development_index']

def convert_to_readable(strings):
    cstrings = []
    for string in strings:
        string = string.capitalize()
        string = string.replace("_", " ")
        cstrings.append(string)
    return cstrings

def convert_to_original(string):
    string = string.lower()
    string = string.replace(" ", "_")
    return string

def convert_cname_iso(cname):
    c = df[df["location"]==cname]
    return c["iso_code"].unique()[0]