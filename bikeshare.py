import time
import pandas as pd
import numpy as np

pd.set_option('display.max_columns',200) #Added from a reviewer suggestion.

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def list_append(flag, series, result):
    """Iterates over a pd.Series and saves the highest index of the highest values in a list.
    returns a list.
    """
    for index, value in series.items():
            if flag == value:
                result.append(index)

    return result


def printing(result):
    """Prints the elements of a list."""
    for element in result:
            print("------> ", element)


#NEW FUNCTION
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    print("\n")
    valid_days = ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']
    valid_months = ['all','january','february','march','april','may','june']
    invalid_months = ['july','august','september','october','november','december']
    while True: #Lesson 7.13
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
        try:
            city = str(input('Please choose the city (chicago, new york city or washington) that you\'d like to analyze: ')).lower()
            print("\n")
        except:
            print("Sorry, thats not a valid input.")
            print("\n")
            continue

        if city == 'new york':
            print("Please type the input as 'new york city' instead of 'new york'")
            print("\n")
            continue
        elif city not in ['chicago','new york city','washington']:
            print("Please type a valid input. That is: chicago, new york city or washington.")
            print("\n")
            continue
        else:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = str(input("Please choose a month to filter by or type 'all' if you don't want a filter: ")).lower()
            print("\n")
        except:
            print("Sorry, that's not a valid input.")
            print("\n")
            continue

        if month in invalid_months:
            print("Sorry, the data only goes from january to june. Select a month within that range")
            print("\n")
            continue
        elif month not in valid_months:
            print("Please type a valid input. That is: a month between january and june.")
            print("\n")
            continue
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = str(input("Choose a day of the week or type 'all' if you don't want a filter: ")).lower()
            print("\n")
        except:
            print("Sorry, that's not a valid input.")
            print("\n")
            continue
        if day not in valid_days:
            print("Please enter a valid day of the week.")
            print("\n")
            continue
        else:
            break
        
    print('-'*40)
    print("\n")
    print("You have filtered by:\nCity: {}\nMonth: {}\nDay of the week: {}".format(city,month,day))
    return city, month, day


#NEW FUNCTION
def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # Load data from chosen city
    df = pd.read_csv(CITY_DATA[city])

    # Convert Start Time column to the correct date format
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract the month and week day into new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name() # .weekday_name gave me this error:
                                                       # 'DatetimeProperties' object has no attribute 'weekday_name'.

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        valid_months = ['january','february','march','april','may','june']
        month = valid_months.index(month)+1
    
        # filter by month to create the new dataframe
        df = df[df['month']==month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


#NEW FUNCTION
def time_stats(month, day, df): #I needed to add month and day to the arguments for my code to work because I'm using those values as conditions.
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Begin by adding the 'hour' column.
    df['hour'] = df['Start Time'].dt.hour 
       
    # display the most common month
    '''
    The same as days of week but, we needed to use the months by their name and not their number
    in order to avoid an error when defining 'flag', because the indexes this time were numbers from
    1 to 6 and variable[0] gives an error.
    '''
    if month == 'all':
        popular_month = df['month'].value_counts().sort_index() #Returns a pd.Series
        valid_months = ['january', 'february', 'march', 'april', 'may', 'june']
        popular_month = popular_month.set_axis(valid_months) # https://stackoverflow.com/a/69336374
            
        list_of_popular_months = []
        sorted_pop_month = popular_month.sort_values(ascending=False) # https://pandas.pydata.org/docs/reference/api/pandas.Series.sort_values.html
        flag = sorted_pop_month[0] #Here we neeeded to convert months to letters again or flag[0] would be month 0, which doesnt exist!
        
        list_append(flag, popular_month, list_of_popular_months)
 
        print("The most common month(s) to travel according to the data selected is/are: ")
       
        printing(list_of_popular_months)

    #==============================================================
    # display the most common day of week
    '''
    .mode()[0] gives the highest value but, what if there is more than one index with the highest value?

    The idea here is that flag's value is always the highest since it is sorted that way. Then, values 
    in list_append() would only be added if they are equal to the first one. Also, it makes sense to 
    display the most common day of the week only if all of them are selected.
    Finally, the last for loop would iterate over the list we generated and print the values.
    '''
    if day == 'all':
        popular_day = df['day_of_week'].value_counts() #Returns a pd.Series
        list_of_popular_days = []
        sorted_pop_day = popular_day.sort_values(ascending=False) # https://pandas.pydata.org/docs/reference/api/pandas.Series.sort_values.html
        flag = sorted_pop_day[0]
        
        list_append(flag, popular_day,list_of_popular_days)

        print("The most common day(s) of the week to travel according to the data selected is/are: ")
        
        printing(list_of_popular_days)

    #==============================================================
    # display the most common start hour
    popular_hour = df['hour'].value_counts()
    list_of_popular_hours = []
    sorted_pop_hour = popular_hour.sort_values(ascending=False)
    flag = sorted_pop_hour.iloc[0] # .iloc was needed here because, without it, we get the hour 0 
                                   # and not the first index of the Series.
    
    list_append(flag, popular_hour, list_of_popular_hours)

    print("The most common hour(s) of the day to travel according to the data selected is/are: ")
    
    printing(list_of_popular_hours)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


#NEW FUNCTION
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    '''
    I think it is logical to continue using the same method to check if there are more than one "most 
    commonly used X". That is, if there are more than one indexes with the highest value.
    '''
    # display most commonly used start station
    popular_station = df['Start Station'].value_counts().sort_values(ascending=False)
    #print(popular_station.index) https://pandas.pydata.org/docs/reference/api/pandas.Series.index.html
    
    list_of_popular_station = []
    flag = popular_station[0]
    
    list_append(flag, popular_station, list_of_popular_station)
            
    print("The most common starting station(s) according to the data selected is/are: ")
    
    printing(list_of_popular_station)

    #=======================================================================
    # display most commonly used end station
    popular_end_station = df['End Station'].value_counts().sort_values(ascending=False)
    #print(popular_station.index) https://pandas.pydata.org/docs/reference/api/pandas.Series.index.html
    
    list_of_popular_end_station = []
    flag = popular_end_station[0]
    
    '''Flag = 1 means that the highest occurrence is one.'''
    if flag == 1: # This obviously never happens for a large enough dataset, but I was using the 400 
                  # row version and sometimes it did so... one can never be too careful.
        print("For the selected filters, every occurrence only happens once. Therefore, the is not \
            a most commonly used station.")
    else:
        list_append(flag, popular_end_station, list_of_popular_end_station)
    
        print("The most common end station(s) according to the data selected is/are: ")
        
        printing(list_of_popular_end_station)

    #==============================================================
    # display most frequent combination of start station and end station trip
    '''
    The way I thought this question was: I need to make a new column using the 
    starting station + some separator + end station. Then, do the same calculation we have been doing
    so far. That is, counting the occurrence of each combination and printing the ones with the highest
    number of occurrences.
    '''
    #Adding the new column
    df['Start to End'] = "Starting in: " + df['Start Station'] + "\nEnding in: " + df['End Station']

    popular_trip = df['Start to End'].value_counts().sort_values(ascending=False)
    list_of_popular_trips = []
    flag = popular_trip[0]

    list_append(flag, popular_trip, list_of_popular_trips)

    print("The most common combination of starting-end stations, according to the data selected is/are: ")
    for item in list_of_popular_trips: 
        print(item)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


#NEW FUNCTION
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_hours = df['Trip Duration'].sum()/3600
    total_hours_int_part = total_hours // 1
    total_hours_decimal_part = total_hours % 1
    
    print("The total duration for trips selected by your filters is:\n {} hours {} minutes and {} seconds"\
        .format(int(total_hours_int_part),int((total_hours_decimal_part*60) // 1), \
            int(((total_hours_decimal_part*60)%1)*60)))

    # display mean travel time
    average_duration = (df['Trip Duration'].sum()/len(df['Trip Duration']))/3600
    total_int_avg = average_duration // 1
    total_dec_avg = average_duration % 1

    print("The average duration for a trip in your selected data is:\n {} hours {} minutes and {} seconds"\
        .format(int(total_int_avg),int((total_dec_avg*60)//1), int(((total_dec_avg*60)%1)*60)))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


#NEW FUNCTION
def user_stats(city, df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    '''
    Here, let's check if we have any Null value within this column in order to avoid adding an extra
    count to the statistics.
    '''
    # Display counts of user types
    count_user_types = len(df['User Type'].dropna().unique())
    user_types = df['User Type'].dropna().value_counts()

    print("There are {} types of users".format(count_user_types))
    print("The user type count for the applied filters are: ")
    for index, value in user_types.items():
        print("{} are {}s".format(value,index))
    
    # Display counts of gender
    '''Only available for Chicago and New York'''
    if city != "washington":
        not_null_gender = df['Gender'].dropna().value_counts()

        print("The gender count for the applied filters are: ")
        for index, value in not_null_gender.items():
            print("{} are {}".format(value,index))

        # Display earliest, most recent, and most common year of birth
        common_byear = df['Birth Year'].value_counts().sort_values(ascending=False)
        recent_byear = df['Birth Year'].value_counts().sort_index(ascending=False)

        print("The year of birth of the earliest person is: {}".format(int(recent_byear.index[-1])))
        print("The year of birth of the most recent person is: {}".format(int(recent_byear.index[0])))
        print("The most common year of birth is: {} with {} people that were born that year for the filters applied."\
            .format(int(common_byear.index[0]),common_byear.iloc[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        raw, show = "no","no"
        
        '''Message for the first time only.'''
        try:
            raw = str(input("Before we start the statistics, would you like to see raw data from your selection? Please answer 'yes' or 'no'.\n-------->"))
        except:
            print("I did not understand. Plase type 'yes' or 'no'.")
            continue

        '''To ask if they want to see 5 more rows of data'''
        for i in range(5,len(df)+1,5):
            if i > 5:
                try:
                    raw = str(input("Would you like to see more data?\n------->"))
                except:
                    print("I did not understand. Plase type 'yes' or 'no'.")
                    continue
            elif i >= len(df):
                print("There isn't more data to show")
                continue

            if raw == 'yes':
                print(df.head(i),"\n")
                raw = 'no'
            else:
                break
        '''
        This is the code I had when I made my first submission. It works perfectly in my laptop, but the
        reviewer got an error. I was told that eval() might be the problem.

        list_of_functions = ['time_stats(month, day, df)',' station_stats(df)',\
            'trip_duration_stats(df)','user_stats(city, df)'] # https://www.quora.com/How-can-you-make-a-list-of-functions-in-Python/answer/Michael-Yousrie
        
        for function in list_of_functions:
            try:
                show = str(input("Are you ready to see the next calculation? Please answer with 'yes' or 'no'.\n------->"))
            except:
                print("I did not understand your answer. Plase type 'yes' or 'no'.")
                continue

            if show == "yes":
                eval(function)
                show = "no"
            else:
                break
        '''
        time_stats(month, day, df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(city, df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
