import pandas as pd
import os

def calculate_demographic_data(print_data=True):
    # Check for the file (assuming 'adult.data.csv' is the standard file name for this problem)
    file_name = 'adult.data.csv'
    if not os.path.exists(file_name):
        print(f"Error: The file '{file_name}' was not found. Please ensure it is uploaded.")
        return None

    # Read data from file
    df = pd.read_csv(file_name)

    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    race_count = df['race'].value_counts()

    # What is the average age of men? (Rounded to nearest tenth)
    average_age_men = df.loc[df['sex'] == 'Male', 'age'].mean().round(1)

    # What is the percentage of people who have a Bachelor's degree? (Rounded to nearest tenth)
    total_people = len(df)
    bachelors_count = df['education'].eq('Bachelors').sum()
    percentage_bachelors = (bachelors_count / total_people * 100).round(1)

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    # What percentage of people without advanced education make more than 50K?

    # with and without `Bachelors`, `Masters`, or `Doctorate`
    higher_education_levels = ['Bachelors', 'Masters', 'Doctorate']
    higher_education = df['education'].isin(higher_education_levels)
    lower_education = ~higher_education # All others

    # percentage with salary >50K
    # Higher Education Rich Percentage (Rounded to nearest tenth)
    higher_education_count = higher_education.sum()
    higher_education_rich_count = df.loc[higher_education, 'salary'].eq('>50K').sum()
    higher_education_rich = (higher_education_rich_count / higher_education_count * 100).round(1)

    # Lower Education Rich Percentage (Rounded to nearest tenth)
    lower_education_count = lower_education.sum()
    lower_education_rich_count = df.loc[lower_education, 'salary'].eq('>50K').sum()
    lower_education_rich = (lower_education_rich_count / lower_education_count * 100).round(1)

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = df['hours-per-week'].min()

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    num_min_workers_df = df[df['hours-per-week'] == min_work_hours]
    num_min_workers = len(num_min_workers_df)
    
    # Percentage of rich among those who work fewest hours (Rounded to nearest tenth)
    rich_min_workers_count = num_min_workers_df['salary'].eq('>50K').sum()
    rich_percentage = (rich_min_workers_count / num_min_workers * 100).round(1)

    # What country has the highest percentage of people that earn >50K?
    # Group by native-country and calculate the percentage of people earning >50K
    country_stats = df.groupby('native-country')['salary'].value_counts(normalize=True).mul(100).unstack()
    
    # Get the percentage for '>50K', fill NaN (countries with 0 rich people) with 0
    rich_percentage_by_country = country_stats['>50K'].fillna(0)
    
    # Find the country with the maximum percentage
    highest_earning_country = rich_percentage_by_country.idxmax()
    # Highest percentage (Rounded to nearest tenth)
    highest_earning_country_percentage = rich_percentage_by_country.max().round(1)

    # Identify the most popular occupation for those who earn >50K in India.
    # Filter for India and salary >50K, then find the mode of 'occupation'
    india_rich_occupation = df.loc[(df['native-country'] == 'India') & (df['salary'] == '>50K'), 'occupation']
    top_IN_occupation = india_rich_occupation.mode()[0]
    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count) 
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }
