import pandas as pd


def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv(print_data)
    #working with series here 
    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    race_count = df['race'].value_counts()

    # What is the average age of men?
    ppl_age = df.loc[:, ['sex', 'age']] #.loc gets all rows and columns of specified range
    men_age = ppl_age[ppl_age['sex']=='Male'] # Get only men
    sum_men = men_age['age'].sum() # Get sum of all men age's
    total_men = men_age['sex'].count() # Count all men
    average_age_men = (sum_men/total_men).round(1)

    # What is the percentage of people who have a Bachelor's degree?
    
    education_c = df.loc[:, ['education']] # Get only education column
    bachelors = education_c[education_c['education']== 'Bachelors']['education'] # Only get bachelors degree & count
    num_bachelors = bachelors.count()
    total_ppl = df['education'].count()
    percentage_bachelors = ((num_bachelors/total_ppl)*100).round(1)
    

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    edu_salary = df.loc[:, ['education', 'salary']]
    adv_edu = edu_salary[edu_salary['education'].isin(['Bachelors', 'Masters', 'Doctorate'])] # only filter out advanced edu 
    more_50k = adv_edu[adv_edu['salary']=='>50K']['salary'].count() # We only need from salary column! so ['Salary']
    num_adv_edu = adv_edu['education'].count()
    higher_education_rich_c = ((more_50k/num_adv_edu)*100).round(1)
    
    # What percentage of people without advanced education make more than 50K?
    adv_eduwithout = edu_salary[edu_salary['education'].isin(['HS-grad', '11th', '9th', 'Some-college',
       'Assoc-acdm', 'Assoc-voc', '7th-8th', 'Prof-school',
       '5th-6th', '10th', '1st-4th', 'Preschool', '12th'])] # only filter out advanced edu,use unique to identify education rankings, df['education'].unique() 
    more_50kwithout = adv_eduwithout[adv_eduwithout['salary']=='>50K']['salary'].count()
    num_advwithout = adv_eduwithout['education'].count()
    lower_education_rich_c = ((more_50kwithout/num_advwithout)*100).round(1)

    # percentage with salary >50K
    higher_education_rich = higher_education_rich_c
    lower_education_rich = lower_education_rich_c

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    df_hours = df['hours-per-week']
    min_work_hours = df_hours.min()

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    hours_salary = df.loc[:, ['hours-per-week', 'salary']]
    num_minhours = df[df['hours-per-week']==min_work_hours] #work min hours per week 
    more_50k_minhours = num_minhours[num_minhours['salary']=='>50K']['salary'].count() 
    num_min_workers = num_minhours['hours-per-week'].count()

    rich_percentage = ((more_50k_minhours/num_min_workers)*100).round(1)


    # What country has the highest percentage of people that earn >50K? TBD CONTINUED
    earn_more50k = df[df['salary']=='>50K']['native-country'].value_counts()
    df_earnmore = pd.DataFrame({'country':earn_more50k.index, 'count': earn_more50k.values})
    total_people = df['native-country'].value_counts()
    df_total = pd.DataFrame({'country': total_people.index, 'people':total_people.values})
    join = pd.merge(df_earnmore, df_total, on = 'country', how = 'left') # Merge tables to calulcate percentage
    join['percentage > 50K'] = (join['count']/join['people'])*100
    join.sort_values(['percentage > 50K'], ascending = [False])
    highest_earning_country = join.loc[13][0] # Get top value, index!
    highest_earning_country_percentage = join['percentage > 50K'].max().round(1)

    # Identify the most popular occupation for those who earn >50K in India.
    india = df[df['native-country']=='India']
    india_more50k = india[india['salary']=='>50K']['occupation'].value_counts() # Number of each occupation that salary > 50K
    top_occ_df = pd.DataFrame({'occupation':india_more50k.index, 'count':india_more50k.values}) # Turn to series to dataframe for easier use index and pull values, other than that usually no need for counting
    top_IN_occupation = top_occ_df.loc[0][0] # Access only occupation of most popular occupation

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

#calculate_demographic_data('adult.data.csv')
