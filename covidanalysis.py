#import the necessary libraries for the below code
import requests
import json
import time
from datetime import datetime, timedelta

#list of each of the state names for the api
states = ['ut', 'ca', 'il', 'ma', 'tx']
#loop that will pull each of the state apis from the list
for state in states:
    url = 'https://api.covidtracking.com/v1/states/' + state + '/daily.json'
    request = requests.get(url)
    data = json.loads(request.text)
    #data is saved as a json. one json per state.
    file = '/home/ubuntu/environment/hw3/' + state + '.json'
    json.dump(data, open(file, 'wt'), indent = 4)
    #define keys that will be used to iterate through the different json
    #objects retrieving the values we care about; date and positive case increase
    datekey = 'date'
    poskey = 'positiveIncrease'
    #initialized dictionaries, lists and variables need to assign certain values
    #from the apis
    month_dict = { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0 }
    day_counter = 0
    total_cases = 0
    maxcases = 0
    latest_date = []
    #for loop that looks through each of the dates in each api.
    for day in data:
        #counts the number of days for each object in the json and adds one more
        #to the variable for each value.
        day_counter += 1
        #Positive case increase value for each day is added to total_cases variable
        total_cases += day[poskey]
        average_cases = total_cases / day_counter
        #below 2 lines are used to find the month of each date
        #Positive Increase values are added to the corresponding dates of the month dictionary
        month_num = int(str(day[datekey])[4:6])
        month_dict[month_num] += day[poskey]
        #checks if positive increase value is greater than max cases variable.
        #The highest value is stored in max_cases. The corresponding date is max_date
        if day[poskey] > maxcases:
            maxcases = day[poskey]
            maxdate = day[datekey]
        #If the there was no increase value on a day, the corresponding date is appended
        #to the latest_date list. The max of this list is the most recent date.   
        elif day[poskey] == 0:
            latest_date.append(day[datekey])
        
        else:
            pass
    #The results of the above loops are printed to the console.     
    print(state)
    print("Question 1: Average daily cases: ", round(average_cases, 2))
    print("Question 2: Date with highest new number of confirmed cases: ", maxdate,)
    print("Question 3: Most recent date with no new confirmed cases: ", max(latest_date)) 
    print("Question 4: Month with highest new confirmed cases: ", max(month_dict, key=month_dict.get))
    print("Question 5: Month with lowest new confirmed cases: ", min(month_dict, key=month_dict.get))
    print()
    print("----------------------------------------------------------------")
    print()
