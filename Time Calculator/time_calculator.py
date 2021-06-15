def add_time(start:str, duration:str, dow:str=None)->str:
    # Set counters for days and hours to add
    days_to_add, hours_to_add=0,0

    # Sets limits for AM and PM time periods
    pm_ranges = list(range(12,12*101,12))
    am_ranges = list(range(0,12*101,12))

    # Selects and cleans hours and minutes and places them in a dict
    start_half = start[-2:]
    current_half = start[-2:]
    keys = ["hours", "minutes"]
    clean_time = start.split(":")
    clean_time = [i[:-3] if i[-2:] in ['AM', "PM"] else i for i in clean_time]

    start_dict = {k:int(v) for k,v in zip(keys, clean_time)}
    # Converts given time to a 24 hour clock
    if start_half == "PM":
        start_dict['hours']+=12
    current_dict = start_dict.copy()

    # Creates a list of days and reorders it based on the given day
    if dow:
        start_day = dow.capitalize()
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        days = days[days.index(start_day):]+days[:days.index(start_day)]

    # Creates a dict for given duration
    duration_dict = {k:int(v) for k,v in zip(keys, duration.split(":"))}

    # Calculations begin here:
    # First, add the minutes of the duration to the start minutes
    current_dict['minutes'] += duration_dict['minutes']
    # As long as minutes in the current time are larger than 59,
    # keep subtracting 60 and noting an hour to add later
    while current_dict['minutes']>59:
        current_dict['minutes']-=60
        hours_to_add+=1
    # If the remaining minutes are less than 10, add a zero before it
    # to get the correct format
    if current_dict['minutes']<10:
        current_dict['minutes'] = "0"+str(current_dict['minutes'])

    # Second, calculate total hours to add, which is a combination of the 
    # starting hour, the duration hours, and extra hours from the minutes
    current_dict['hours'] += duration_dict['hours']+hours_to_add
    # Increase the days to add by the floor division of hours divided by 24
    days_to_add += current_dict['hours']//24

    # Loop through AM and PM time limits to figure out which one will be the 
    # ending time median to use
    for j in range(0,len(pm_ranges),2):
        k = j+1
        if (current_dict['hours']>=pm_ranges[j]) & (current_dict['hours']<pm_ranges[k]):
            current_half="PM"
            break
        elif (current_dict['hours']>=am_ranges[j]) & (current_dict['hours']<am_ranges[k]):
            current_half = "AM"
            break

    # As long as the current hours are greater than 12, subtract 12
    while current_dict['hours']>=12:
        current_dict['hours']-=12

    # After finishing, if the hours equals 0, change to 12
    if current_dict['hours']==0:
        current_dict['hours']=12

    if dow:
        # Extends days list to have enough elements for filling in day of week
        days *= (days_to_add//7)+1
        if days_to_add<1:
            new_time = f"{current_dict['hours']}:{current_dict['minutes']} {current_half}, {days[days_to_add]}"
        elif days_to_add==1:
            new_time = f"{current_dict['hours']}:{current_dict['minutes']} {current_half}, {days[days_to_add]} (next day)"
        else:
            new_time = f"{current_dict['hours']}:{current_dict['minutes']} {current_half}, {days[days_to_add]} ({days_to_add} days later)"
    else:
        if days_to_add==1:
            new_time = f"{current_dict['hours']}:{current_dict['minutes']} {current_half} (next day)"
        elif days_to_add>1:
            new_time = f"{current_dict['hours']}:{current_dict['minutes']} {current_half} ({days_to_add} days later)"
        else:
            new_time = f"{current_dict['hours']}:{current_dict['minutes']} {current_half}"

    return new_time

