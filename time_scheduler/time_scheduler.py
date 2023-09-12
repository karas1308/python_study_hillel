import datetime


def calculate_booking_time(booked_time_frames, min_time_duration, min_time_slot=15):
    min_time_duration = datetime.timedelta(hours=min_time_duration)
    min_time_slot = min_time = datetime.timedelta(minutes=min_time_slot)
    working_hours = (datetime.time(8), datetime.time(18))
    open_datetime = datetime.datetime.combine(datetime.datetime(1900, 1, 1), working_hours[0])
    close_datetime = datetime.datetime.combine(datetime.datetime(1900, 1, 1), working_hours[1])

    booked_time_slots = []
    all_time_slots = []
    while open_datetime <= close_datetime - min_time_slot:
        all_time_slots.append(open_datetime.strftime("%H:%M"))
        open_datetime += min_time_slot
    print(f"All possible time slots: {all_time_slots}")

    for start_time, end_time in booked_time_frames:
        while start_time < end_time:
            booked_time_slots.append(start_time.strftime("%H:%M"))
            start_time += min_time_slot
    print(f"Booked time slot start: {booked_time_slots}")
    available_times = sorted(set(all_time_slots) - set(booked_time_slots))
    print(f"Available time slot start: {available_times}")
    available_times = [datetime.datetime.strptime(time_str, "%H:%M") for time_str in available_times]

    free_periods = []
    current_time = available_times[0]
    for i in range(len(available_times) - 1):
        i += 1
        next_time = available_times[i]
        if (next_time - current_time) == min_time_slot:
            min_time_slot += min_time
            if i == len(available_times) - 1:
                free_periods.append((current_time, available_times[i] + min_time))
        else:
            free_periods.append((current_time, available_times[i - 1]))
            current_time = next_time
            min_time_slot = min_time
        i += 1

    possible_periods = []
    possible_booking_time = []
    for start, end in free_periods:
        if end - start >= min_time_duration:
            possible_periods.append((start, end))
            while (start + min_time_duration <= end + min_time) and (start + min_time_duration <= close_datetime):
                possible_booking_time.append(start)
                start += min_time
    return possible_periods, possible_booking_time


####################################################################

x = [(datetime.datetime(2023, 8, 1, 8, 0),
      datetime.datetime(2023, 8, 1, 9, 0)),
     (datetime.datetime(2023, 8, 1, 12, 30),
      datetime.datetime(2023, 8, 1, 13, 0)),
     (datetime.datetime(2023, 8, 1, 14, 30),
      datetime.datetime(2023, 8, 1, 15, 0))]
y = 2

posible_periods, possible_booking_time = calculate_booking_time(x, y)
print(possible_booking_time)
for time in possible_booking_time:
    print(
        f"posible time: {time.strftime('%H:%M')}")

for start, end in posible_periods:
    print(
        f"posible period: З в {start.strftime('%H:%M')} до {end.strftime('%H:%M')} (тривалість: {str(end - start)})")
