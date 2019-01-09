from typing import List, TextIO

# A type to represent cleaned (see clean_data()) for multiple stations
SystemData = List[List[object]]
# A type to represent cleaned data for one station
StationData = List[object]
# A type to represent a list of stations
StationList = List[int]


#Constants
# station information.
ID = 0
NAME = 1
LATITUDE = 2
LONGITUDE = 3
CAPACITY = 4
BIKES_AVAILABLE = 5
DOCKS_AVAILABLE = 6
IS_RENTING = 7
IS_RETURNING = 8


#HELPER FUNCTIONS

def is_number(value: str) -> bool:
    '''Return True iff value represents a decimal number.

    >>> is_number('csc108')
    False
    >>> is_number('  108 ')
    True
    >>> is_number('+3.14159')
    True
    '''

    return value.strip().lstrip('+-').replace('.', '', 1).isnumeric()

def csv_to_list(csv_file: TextIO) -> List[List[str]]:
    '''Return the contents of the open CSV file csv_file as a list of lists,
    where each inner list contains the values from one line of csv_file.

    Docstring examples not provided since results depend on a data file.
    '''

    # Read and discard the header
    csv_file.readline()

    data = []
    for line in csv_file:
        data.append(line.strip().split(','))
    return data


#SAMPLE STATIONS TO BE USED IN TESTING

SAMPLE_STATIONS = [
    [7087, 'Danforth/Aldridge', 43.684371, -79.316756, 23, 9, 14, True, True],
    [7088, 'Danforth/Coxwell', 43.683378, -79.322961, 15, 13, 2, False, False]]

HANDOUT_STATIONS = [
    [7000, 'Ft. York / Capreol Crt.', 43.639832, -79.395954, 31, 20, 11, True, True],
    [7001, 'Lower Jarvis St / The Esplanade', 43.647992, -79.370907,
     15, 5, 10, True, True]]


def clean_data(data: List[List[str]]) -> None:
    '''Modify the list data by converting each string in data to:
        . an int iff if it represents a whole number
        . a float iff it represents a number that is not a whole number
        . True or False iff the string is 'True' or 'False', respectively
        . None iff the string is 'null' or the empty string
    and leaving the string as it is otherwise.

    >>> d = [['abc', '123', '45.6', 'True', 'False']]
    >>> clean_data(d)
    >>> d
    [['abc', 123, 45.6, True, False]]
    >>> d = [['ab2'], ['-123'], ['False', '3.2']]
    >>> clean_data(d)
    >>> d
    [['ab2'], [-123], [False, 3.2]]
    '''

    for i in range(len(data)):
        for n in range(len(data[i])):
            if data[i][n] == 'True':
                data[i][n] = True
            elif data[i][n] == 'False':
                data[i][n] = False
            elif data[i][n] == '':
                data[i][n] = None
            elif is_number(data[i][n]) is True:
                if '.' in data[i][n]:
                    data[i][n] = float(data[i][n])
                else:
                    data[i][n] = int(data[i][n])
            else:
                data[i][n] = str(data[i][n])
    
                                    
def get_station_info(station_id: int, stations: SystemData) -> StationData:
    '''Return a list containing the following information from stations
    about the station with id number station_id:
        . station name
        . number of bikes available
        . number of docks available
    (in this order)

    Precondition: station_id will appear in stations.

    >>> get_station_info(7087, SAMPLE_STATIONS)
    ['Danforth/Aldridge', 9, 14]
    >>> get_station_info(7088, SAMPLE_STATIONS)
    ['Danforth/Coxwell', 13, 2]
    '''
    avaliable_bikes_docks = []
    for i in range(len(stations)):
        if stations[i][0] == station_id:
            avaliable_bikes_docks.append(stations[i][1])
            avaliable_bikes_docks.append(stations[i][5])
            avaliable_bikes_docks.append(stations[i][6])
    return avaliable_bikes_docks
    

def get_total(index: int, stations: SystemData) -> int:
    '''Return the sum of the column in stations given by index.

    Precondition: the items in stations at the position
                  that index refers to are ints.

    >>> get_total(BIKES_AVAILABLE, SAMPLE_STATIONS)
    22
    >>> get_total(DOCKS_AVAILABLE, SAMPLE_STATIONS)
    16
    '''
    total = 0
    for i in range(len(stations)):
        total = total + stations[i][index]
    return total
    

def get_station_with_max_bikes(stations: SystemData) -> int:
    '''Return the station ID of the station that has the most bikes available.
    If there is a tie for the most available, return the station ID that appears
    first in stations.

    Precondition: len(stations) > 0

    >>> get_station_with_max_bikes(SAMPLE_STATIONS)
    7088
    '''
    max_bikes = []
    for i in range(len(stations)):
        max_bikes.append(stations[i][5])
    maximum = max_bikes.index(max(max_bikes))
    return stations[maximum][0]
    

def get_stations_with_n_docks(n: int, stations: SystemData) -> StationList:
    '''Return a list containing the station IDs for the stations in stations
    that have at least n docks available, in the same order as they appear
    in stations.

    Precondition: n >= 0

    >>> get_stations_with_n_docks(2, SAMPLE_STATIONS)
    [7087, 7088]
    >>> get_stations_with_n_docks(5, SAMPLE_STATIONS)
    [7087]
    '''
    stations_with_n_docks = []
    for i in range(len(stations)):
        if stations[i][6] >= n:
            stations_with_n_docks.append(stations[i][0])
    return stations_with_n_docks
    

def get_direction(start_id: int, end_id: int, stations: SystemData) -> str:
    '''Return a string that contains the direction to travel to get from
    station start_id to station end_id according to data in stations.

    Precondition: start_id and end_id will appear in stations.

    >>> get_direction(7087, 7088, SAMPLE_STATIONS)
    'SOUTHWEST'
    '''
    import math
    for i  in range(len(stations)):
        if stations[i][0] == start_id:
            latitude_start = stations[i][2]
            longitude_start = stations[i][3]
        elif stations[i][0] == end_id:
            latitude_end = stations[i][2]
            longitude_end = stations[i][3]
            
    #To stop division over 0, if longitude at start and end are the same
    if longitude_start == longitude_end:
        longitude_start = longitude_start+0.00001
              
    degree = (180*math.atan2(latitude_start - latitude_end, longitude_start - \
            longitude_end))/math.pi
    
    if (degree > -22.5 and degree < 0) or  (degree < 22.5 and degree > 0):
        return 'WEST'
    elif degree >= 22.5 and degree <= 67.5:
        return 'SOUTHWEST'
    elif degree > 67.5 and degree < 112.5:
        return 'SOUTH'
    elif degree >= 112.5 and degree <= 157.5:
        return 'SOUTHEAST'
    elif (degree > 157.5 and degree < 180) or (degree < -157.5 and degree > -180):
        return 'EAST'
    elif degree >= -157.5 and degree <= -112.5:
        return 'NORTHEAST'
    elif degree > -112.5 and degree < -67.5:
        return 'NORTH'
    elif degree >= -67.5 and degree >= -22.5:
        return 'NORTHWEST'                  
    
    
def rent_bike(station_id: int, stations: SystemData) -> bool:
    '''Update the specified available bike count and the docks available
    count in stations, if possible. Return True iff the rental from
    station_id was successful.

    Precondition: station_id will appear in stations.

    >>> station_id = SAMPLE_STATIONS[0][ID]
    >>> original_bikes_available = SAMPLE_STATIONS[0][BIKES_AVAILABLE]
    >>> original_docks_available = SAMPLE_STATIONS[0][DOCKS_AVAILABLE]
    >>> rent_bike(station_id, SAMPLE_STATIONS)
    True
    >>> original_bikes_available - 1 == SAMPLE_STATIONS[0][BIKES_AVAILABLE]
    True
    >>> original_docks_available + 1 == SAMPLE_STATIONS[0][DOCKS_AVAILABLE]
    True
    >>> station_id = SAMPLE_STATIONS[1][ID]
    >>> original_bikes_available = SAMPLE_STATIONS[1][BIKES_AVAILABLE]
    >>> original_docks_available = SAMPLE_STATIONS[1][DOCKS_AVAILABLE]
    >>> rent_bike(station_id, SAMPLE_STATIONS)
    False
    >>> original_bikes_available == SAMPLE_STATIONS[1][BIKES_AVAILABLE]
    True
    >>> original_docks_available == SAMPLE_STATIONS[1][DOCKS_AVAILABLE]
    True
    '''
    rental = False
    for i in range(len(stations)):
        if stations[i][0] == station_id:
            if stations[i][7] is True and stations[i][5] > 0:
                stations[i][5] = stations[i][5] - 1
                stations[i][6] = stations[i][6] +1
                rental = True
    return rental is True
    

def return_bike(station_id: int, stations: SystemData) -> bool:
    '''Update stations by incrementing the appropriate available bike
    count and decrementing the docks available count, if possible.
    Return True iff a bike is successfully returned to station_id.

    Precondition: station_id will appear in stations.

    >>> station_id = SAMPLE_STATIONS[0][ID]
    >>> original_bikes_available = SAMPLE_STATIONS[0][BIKES_AVAILABLE]
    >>> original_docks_available = SAMPLE_STATIONS[0][DOCKS_AVAILABLE]
    >>> return_bike(station_id, SAMPLE_STATIONS)
    True
    >>> original_bikes_available + 1 == SAMPLE_STATIONS[0][BIKES_AVAILABLE]
    True
    >>> original_docks_available - 1 == SAMPLE_STATIONS[0][DOCKS_AVAILABLE]
    True
    >>> station_id = SAMPLE_STATIONS[1][ID]
    >>> original_bikes_available = SAMPLE_STATIONS[1][BIKES_AVAILABLE]
    >>> original_docks_available = SAMPLE_STATIONS[1][DOCKS_AVAILABLE]
    >>> return_bike(station_id, SAMPLE_STATIONS)
    False
    >>> original_bikes_available == SAMPLE_STATIONS[1][BIKES_AVAILABLE]
    True
    >>> original_docks_available == SAMPLE_STATIONS[1][DOCKS_AVAILABLE]
    True
    '''
    returning_bike = False
    for i in range(len(stations)):
        if stations[i][0] == station_id:
            if stations[i][8] is True and stations[i][6] > 0:
                stations[i][5] = stations[i][5] + 1
                stations[i][6] = stations[i][6] -1
                returning_bike = True
    return returning_bike is True
    

def balance_all_bikes(stations: SystemData) -> None:
    '''Update stations by redistributing bikes so that, as closely as
    possible, all bike stations has the same percentage of bikes available.

    >>> balance_all_bikes(HANDOUT_STATIONS)
    >>> HANDOUT_STATIONS == [\
     [7000, 'Ft. York / Capreol Crt.', 43.639832, -79.395954, 31, 17, 14, True, True],\
     [7001, 'Lower Jarvis St / The Esplanade', 43.647992, -79.370907,\
     15, 8, 7, True, True]]
    True
    '''
    
    overall_spaces = 0
    overall_bikes = 0
    
    for i in range(len(stations)):
        overall_spaces = overall_spaces + stations[i][6]
        overall_bikes = overall_bikes + stations[i][5]

    overall_percentage = round((overall_bikes/(overall_bikes + overall_spaces))*100)

    excess_bikes = 0
    deficit_bikes = 0
    
    
    for i in range(len(stations)):
        station_average = round(((stations[i][5])/(stations[i][5]+stations[i][6]))*100)
        number_remove = round(((-overall_percentage/100)*(stations[i][5] + \
                        stations[i][6]) + stations[i][5]))
        number_add = round(((overall_percentage/100)*(stations[i][5] + \
                     stations[i][6]) - stations[i][5]))
        
        if station_average > overall_percentage:
            excess_bikes = excess_bikes + number_remove
        elif station_average < overall_percentage:
            deficit_bikes = deficit_bikes + number_add

    for i in range(len(stations)):
        station_average = round(((stations[i][5])/(stations[i][5]+stations[i][6]))*100)
        number_remove = round(((-overall_percentage/100)*(stations[i][5] + \
                        stations[i][6]) + stations[i][5]))
        number_add = round(((overall_percentage/100)*(stations[i][5] + stations[i][6]) - \
                     stations[i][5]))

        if station_average > overall_percentage and stations[i][7] is True and \
           excess_bikes > 0:
            stations[i][5] = stations[i][5] - number_remove
            stations[i][6] = stations[i][6] + number_remove
            excess_bikes = excess_bikes - number_remove
            
        elif station_average < overall_percentage and stations[i][8] is True and \
            stations[i][6] > 0 and deficit_bikes > 0:
             stations[i][5] = stations[i][5] + number_add
             stations[i][6] = stations[i][6] - number_add
             deficit_bikes = deficit_bikes - number_add

    
    # Notes:
    # Calculate the percentage of bikes available across all stations
    # and balance the number of bikes available at each station so that
    # the percentage is similar across all stations.
    #
    # Remove bikes from a station if and only if the station is renting
    # and there is a bike available to rent, and return a bike if and
    # only if the station is allowing returns and there is a dock
    # available.
    
    

if __name__ == '__main__':
    pass
