import time
import pandas as pd
import numpy as np
import sys

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print('We need to set some filter. Lets start with the city! \n')
    
    city = ''
    while city == '':
        userInput = str(input('Choose a city: "chicago", "new york city" or "washington"!')).lower()
        try:
            if userInput in CITY_DATA.keys():
                city = userInput
            else:
                print('no match, please try again!')
        
        except KeyboardInterrupt:
            sys.exit()
        except:
            print('Exception ', sys.exc_info()[0], ' occured.')    
    
    print('You have selected the city: {}.'.format(city))

    # get user input for month (all, january, february, ... , june)
    print('-'*40)
    print('Now, that we have a city, we need to set the month we want to look at. \n')

    month = ''
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    while month == '':
        userInput = str(input('Enter the month: all, january, february, ... , june.')).lower()
        try:
            if userInput in months:
                month = userInput
                print('You have chosen: {} as timeframe to look at. Great!'.format(month))
            else:
                print('I did not get it, try again!')
        
        except KeyboardInterrupt:
            sys.exit()
        except:
            print('Exception ', sys.exc_info()[0], ' occured.')   

    # get user input for day of week (all, monday, tuesday, ... sunday)
    print('-'*40)
    print('Finaly, we neet do specify a day of the week!')

    day = ''
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    while day == '':
        userInput = str(input('Now coose between: all, monday, tuesday, ... sunday')).lower()
        try:
            if userInput in days:
                day = userInput
                print('Cool! You have chosen {}, let\'s move on.'.format(day))
            else:
                print('One more try please!')

        except KeyboardInterrupt:
            sys.exit()
        except:
            print('Exception ', sys.exc_info()[0], ' occured.')    

    print('-'*40)
    return city, month, day


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
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    # somehow weekday_name did not work, so i use the index...
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday
    df['hour'] = df['Start Time'].dt.hour

    # creating the start-end stations combination
    df['Start-End Stations'] = df['Start Station'] + ' - ' + df['End Station']

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day = days.index(day)
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']   

    # display the most common month
    most_common_month = months[df['month'].mode()[0] - 1]
    print('The most common month is: {}.'.format(most_common_month))

    # display the most common day of week
    most_common_day = days[df['day_of_week'].mode()[0]]
    print('The most common day is: {}.'.format(most_common_day))

    # display the most common start hour
    most_common_hour = df['hour'].mode()[0]
    print('The most common hour is: {}.'.format(most_common_hour))

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print('The most used start station was: {}.'.format(most_common_start_station))

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print('The most used end station was: {}.'.format(most_common_end_station))

    # display most frequent combination of start station and end station trip
    most_common_start_end_stations = df['Start-End Stations'].mode()[0]
    how_many_start_end = (df['Start-End Stations'] == most_common_start_end_stations).sum()

    if most_common_start_station == most_common_end_station:
        print('The start and end station are equal, so people brought the bike back, where they took it from.')
        print('This happend {} times.'.format(how_many_start_end))
    else:
        print('The most seen start-end station Combination is: \"{}\" and was seen {} times.'.format(most_common_start_end_stations, how_many_start_end))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def seconds_to_readable_date(seconds):
    # min = 60
    # hour = 60 * 60 = 3600
    # day = 60 * 60 * 24 = 86400
    # weeks = 60 * 60 * 24 * 7 = 604800
    # years = 60 * 60 * 24 * 7 * 52.1429 = 31536025.92

    # total example value 280878987.0

    year = int(seconds // 31536025.92)
    week = int((seconds - (year * 31536025.92)) // 604800)
    day = int((seconds - ((year * 31536025.92) + (week * 604800)))// 86400)
    hour = int((seconds - ((year * 31536025.92) + (week * 604800) + (day * 86400))) // 3600)
    minit = int((seconds - ((year * 31536025.92) + (week * 604800) + (day * 86400) + (hour * 3600))) // 60)
    second = round((seconds - ((year * 31536025.92) + (week * 604800) + (day * 86400) + (hour * 3600) + (minit * 60))), 2)

    if week == 0:
        return ('{} days {} hours {} minutes {} seconds'.format(day, hour, minit, second))
    elif year == 0:
        return ('{} weeks {} days {} hours {} minutes {} seconds'.format(week, day, hour, minit, second))
    else:
        return ('{} years {} weeks {} days {} hours {} minutes {} seconds'.format(year, week, day, hour, minit, second))

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    """
    # first approach without using trip duration cloum (just oversaw)
    # display total travel time
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Travel Time'] = df['End Time'] - df['Start Time']
    df['Travel Time'] = df['Travel Time']/np.timedelta64(1, 's')

    # print('total travel time in seconds: {}.'.format(df['Travel Time'].sum()))
    total_travel_time = seconds_to_readable_date(df['Travel Time'].sum())
    print('The total travel time was: {}.'.format(total_travel_time))

    # display mean travel time
    mean_travel_time = seconds_to_readable_date(df['Travel Time'].mean())
    print('The mean travel time was: {}.'.format(mean_travel_time))
    """

    # display total travel time
    ttt = seconds_to_readable_date(df['Trip Duration'].sum())
    print('The total travel time was: {}.'.format(ttt))
    # display mean travel time
    mean_tt = seconds_to_readable_date(df['Trip Duration'].mean())
    print('The mean travel time was: {}.'.format(mean_tt))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    if 'User Type' in  df.columns:
        print('The user types:')
        user_types = df['User Type'].value_counts().to_dict()
        for key in user_types:
            print(key, user_types[key])
    else:
        print('Colum "User Type" is missing. Can not give insights.')


    # Display counts of gender
    if 'Gender' in df.columns:
        print('\nThe gender count:')
        gender_count = df['Gender'].value_counts().to_dict()
        for key in gender_count:
            print(key, gender_count[key])
    else:
        print('No data, do calculation for gender.')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Date' in df.columns:
        earliest_birth_year = int(df['Birth Year'].min())
        most_recent_birth_year = int(df['Birth Year'].max())
        common_birth_year = int(df['Birth Year'].mode()[0])
        message = 'The youngest user were born in {} and the oldest user were born in {}, but most of the user were boren in {}.'
        print(message.format(earliest_birth_year, most_recent_birth_year, common_birth_year))
    else:
        print('There is no data for birth date, so we can not calculate anything.\n')

    userINput = str(input('Would you like to see individual trip data? Enter yes or no')).lower()
    if userINput == 'yes':
        closer_look = df.sample(n=6)
        print(closer_look)



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
