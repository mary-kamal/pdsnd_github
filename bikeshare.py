import time
import pandas as pd
import numpy as np

# bike share datasets
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'july']
DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


# helpers
def print_line():
    print('-'*40)


def timeit(func, df):
    start_time = time.time()
    func(df)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print_line()


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington)
    city = ''
    while city not in CITY_DATA:
        city = input('Please select a valid city from {%s}: ' % (', '.join(CITY_DATA.keys()))).lower()


    # get user input for month (all, january, february, ... , june)
    month = ''
    while month not in MONTHS + ['all']:
        month = input('Please select a valid month from {all, %s}: ' % (', '.join(MONTHS))).lower()


    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ''
    while day not in DAYS + ['all']:
        day = input('Please select a valid day from {all, %s}: ' % (', '.join(DAYS))).lower()

    print_line()
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
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = MONTHS.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')

    # display the most common month
    popular_month = MONTHS[df['month'].mode()[0] - 1].capitalize()
    print('Most popular month: %s.' % (popular_month))


    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('Most popular day: %s.' % (popular_day))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most popular hour: %d.' % (popular_hour))


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most popular start station: %s.' % (popular_start_station))

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most popular end station: %s.' % (popular_end_station))

    # display most frequent combination of start station and end station trip
    popular_combo = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print('Most popular combination of start station and end station: %s and %s.' % popular_combo)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time (days): %.2f' % (total_travel_time / (24 * 3600)))


    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean travel time (minutes): %.2f' % (mean_travel_time / 60))


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')

    # display counts of user types
    if 'User Type' in df.columns:
        user_types = df['User Type'].value_counts()
        print(user_types, '\n')


    # display counts of gender
    if 'Gender' in df.columns:
        genders = df['Gender'].value_counts()
        print(genders, '\n')


    # display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print(df['Birth Year'].describe())


def view_data(df):
    """Let user view raw data, 5 rows at a time."""
    
    # counter to track which rows to display
    i = 0

    while True:
        
        # obtain yes/no input
        see_data = ''
        while see_data not in ('yes', 'no'):
            see_data = input('Would you like to see 5 rows of raw data (yes/no): ').lower()
        
        # handle print request
        if see_data == 'yes':

            # print 5 lines of raw data
            if i < len(df):
                print(df[i:i+5])
                i += 5
            
            # notify there's no data to print and exit
            else:
                print('No more raw data.\n')
                return
        
        # handle exit request
        else:
            return


def main():
    while True:
        # obtain filters
        city, month, day = get_filters()

        # load data
        df = load_data(city, month, day)

        timeit(time_stats, df)
        timeit(station_stats, df)
        timeit(trip_duration_stats, df)
        timeit(user_stats, df)
        
        # let user explore raw data
        view_data(df)

        # ask user if they'd like to start again
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
