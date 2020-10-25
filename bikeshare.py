import time
import pandas as pd
import numpy as np
import math

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

MONTH_DATA = {'jan': 1,
              'feb': 2,
              'mar': 3,
              'apr': 4,
              'may': 5,
              'jun': 6}

WEEK_DATA = {'mon': 0,
             'tues': 1,
             'wed': 2,
             'thur': 3,
             'fri': 4,
             'sat': 5,
             'sun': 6}

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
    while 1:
        print('Which country\'s should we look for?')
        city = input('Chicago/CH, New York City/NYC, or Washington/WA? ').lower()
        print()
        if city == 'ch':
            city = 'chicago'
        if city == 'ny' or city == 'nyc' or city == 'new york city' or city == 'new':
            city = 'new york city'
        if city == 'wa' or city == 'washington dc' or city == 'washington':
            city = 'washington'
        if city not in CITY_DATA:
            print('Please enter a valid city')
            continue
        city = CITY_DATA[city]
        break

    # get user input for month (all, january, february, ... , june)
    while 1:
        choice = input('Do you want to filter the data by month and/or week? Yes/No ').lower()
        print()
        if choice == 'yes' or choice == 'y':
            choice = True
        elif choice == 'no' or choice == 'n':
            choice = False
        else:
            print('Please enter a valid choice. Let\'s try again. ')
            continue
        break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while 1:
        if choice:
            filter = input('You can filter by month / day / both ').lower()
            print()
            if filter == 'month':
                print('Which month\'s data to look at?')
                month = input('jan, feb, mar, apr, may, jun- ').lower()
                print()
                if month not in MONTH_DATA:
                    print('Input not understood. Please try again?')
                    continue
                month = MONTH_DATA[month]
                day = 'all'
            elif filter == 'day':
                print('Which day\'s data to look at? ')
                day = input(
                    'mon, tues, wed, thur, fri, sat, sun- ').lower()
                print()
                if day not in WEEK_DATA:
                    print('Input not understood. Please try again?')
                    continue
                day = WEEK_DATA[day]
                month = 'all'
            elif filter == 'both':
                print('Which month\'s data to look at?')
                month = input('jan, feb, mar, apr, may, jun- ').lower()
                print()
                if month not in MONTH_DATA:
                    print('Input not understood. Please try again?')
                    continue
                month = MONTH_DATA[month]
                print('And day of the week?')
                day = input(
                    'mon, tues, wed, thur, fri, sat, sun- ').lower()
                print()
                if day not in WEEK_DATA:
                    print('Input not understood. Please try again?')
                    continue
                day = WEEK_DATA[day]
            else:
                print('Input not understood. Please try again?')
                continue
            break
        else:
            day = 'all'
            month = 'all'
            break

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
    df = pd.read_csv(city)
    df['day_of_week'] = pd.to_datetime(df['Start Time']).dt.dayofweek
    df['month'] = pd.to_datetime(df['Start Time']).dt.month
    if day != 'all':
        df = df[df['day_of_week'] == day]
    if month != 'all':
        df = df[df['month'] == month]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    df['day_of_week'] = pd.to_datetime(df['Start Time']).dt.dayofweek
    df['month'] = pd.to_datetime(df['Start Time']).dt.month

    # display the most common month
    most_freq_month = df['month'].mode()[0]
    for num in MONTH_DATA:
        if MONTH_DATA[num] == most_freq_month:
            most_freq_month = num.title()
    print('Most common month for travel : {}'.format(most_freq_month))

    # display the most common day of week
    most_freq_day = df['day_of_week'].mode()[0]
    for num in WEEK_DATA:
        if WEEK_DATA[num] == most_freq_day:
            most_freq_day = num.title()
    print('Most common day of week for travel : {}'.format(most_freq_day))

    # display the most common start hour
    df['hour'] = pd.to_datetime(df['Start Time']).dt.hour
    most_freq_hour = df['hour'].mode()[0]
    print('Most common hour for travel : {}'.format(most_freq_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most commonly used start station : {}'.format(df['Start Station'].mode()[0]))

    # display most commonly used end station
    print('Most commonly used end station : {}'.format(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    most_freq_station_comb = df['Start Station'] + ' to ' + df['End Station']
    print('Most frequent combination of start station and end station trip : {}'.format(
        most_freq_station_comb.mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total Duration : {} seconds'.format(df['Trip Duration'].sum()))
    print('Average Duration : {} seconds'.format(int(df['Trip Duration'].mean())))
    print('Minimum Duration : {} seconds'.format(df['Trip Duration'].min()))
    print('Maximum Duration : {} seconds'.format(df['Trip Duration'].max()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    types_of_users = df.groupby('User Type', as_index=False).count()
    print('Count by User Types:')
    print('-----------------------')
    user_types = df['User Type'].value_counts()
    print(user_types)
    print('-----------------------')

    # Display counts of gender
    if 'Gender' not in df:
        print('NOTE: Gender data of users is not available for this city.')
    else:
        gender_of_users = df.groupby('Gender', as_index=False).count()
        print('Count by Gender:')
        print('-----------------------')
        gender = df['Gender'].value_counts()
        print(gender)
        print('-----------------------')

        print('NOTE: Gender data for {} users is not available.\n'.format(
            len(df) - gender_of_users['Start Time'][0] - gender_of_users['Start Time'][1]))

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' not in df:
        print('NOTE: Birth Year of users is not available for this city.')
    else:
        birth = df.groupby('Birth Year', as_index=False).count()
        print('Earliest year of birth : {}.'.format(int(birth['Birth Year'].min())))
        print('Most recent year of birth : {}.'.format(int(birth['Birth Year'].max())))
        print('Most common year of birth year : {}.'.format(
            int(birth.iloc[birth['Start Time'].idxmax()]['Birth Year'])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """Displays detailed records on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n')
    start_loc = 0
    while (1):
        print(df.iloc[start_loc:start_loc+5])
        start_loc += 5
        view_display = input('Do you wish to continue and see more records? Enter yes or no.: ').lower()
        if view_display != 'yes' and view_display != 'y':
            break
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
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes' and restart != 'y':
            break


if __name__ == "__main__":
	main()
