import math
import time
import pandas as pd


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
    print('Hello! Let\'s explore some US bikeshare data!\n')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Please select a city (Chicago, New York City or Washington): ').lower()
    while city not in ['chicago', 'new york city', 'washington']:
        city = input('Incorrect city name given! \n'
                     'Please type in either Chicago, New York City or Washington: ').lower()

    # get user input for month (all, january, february, ... , june)
    month = input('Please select a month (all, January, February, ... , June: ').lower()
    while month not in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
        month = input('Incorrect month given! \n'
                      'Please type in "all" or a month in range January - June: ').lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Please select a day of the week (all, Monday, Tuesday, ... , Sunday: ').lower()
    while day not in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
        day = input('Incorrect day given! \n'
                    'Please type in "all" or any day from Monday - Sunday: ').lower()

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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['Month'] = df['Start Time'].dt.month
    df['Day of Week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['Month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['Day of Week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month if applicable
    if df['Month'].nunique() > 1:
        popular_month = df['Month'].mode()[0]
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        popular_month = months[popular_month - 1]
        print(f'The most popular month to travel is: {popular_month}')

    # display the most common day of week if applicable
    if df['Day of Week'].nunique() > 1:
        popular_day = df['Day of Week'].mode()[0]
        print(f'The most popular day of the week to travel is: {popular_day}')

    # display the most common start hour
    df['Hour'] = df['Start Time'].dt.hour
    popular_hour = df['Hour'].mode()[0]
    print(f'The most popular hour of day to travel is: {popular_hour}h\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print(f'The most commonly used start station is: {popular_start_station}')

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print(f'The most commonly used end station is: {popular_end_station}')

    # display most frequent combination of start station and end station trip
    df['Trip'] = df['Start Station'] + ' - ' + df['End Station']
    popular_trip = df['Trip'].mode()[0]
    print(f'The most frequent combination of start and end station is: {popular_trip}\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print(f'The total travel time for the given time window is: {math.trunc(total_travel_time/3600)} hours')

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print(f'The total travel time for the given time window is: {math.trunc(mean_travel_time)} seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    for row_number in range(0, len(user_types)):
        print(f'Number of "{user_types.index[row_number]}" type customers: {user_types[row_number]}')

    # Display counts of gender if gender column exists
    if 'Gender' in df.columns:
        genders = df['Gender'].value_counts()
        print(f'\nNumber of male customers: {genders["Male"]}')
        print(f'Number of female customers: {genders["Female"]}\n')

    # Display earliest, most recent, and most common year of birth if birth year column exists
    if 'Birth Year' in df.columns:
        earliest_birth_year = int(df['Birth Year'].min())
        most_common_birth_year = int(df['Birth Year'].mode()[0])
        most_recent_birth_year = int(df['Birth Year'].dropna().tail(1).values[0])
        print(f'The earliest customer provided birth year is: {earliest_birth_year}')
        print(f'The most common customer year of birth is: {most_common_birth_year}')
        print(f'The birth date of the most recent customer is: {most_recent_birth_year}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(city):
    """Displays 5 rows of raw data at the time for the specified city."""

    # load raw data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # define starting row for display sample
    starting_row = 0

    # Ask user whether to display raw data, and provide data if answer received is 'yes'.
    while True:
        data_request = input('Would you like to see a raw data sample? Enter yes or no. \n')
        if data_request.lower() == 'no':
            break
        elif data_request.lower() == 'yes':
            print(df[starting_row:(starting_row + 5)])
            starting_row += 5
        else:
            print('Type in either "yes" or "no". Please try again.')


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
