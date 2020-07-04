import csv
import calendar
import datetime
import json
import os

ms_threshold = input("Enter a minimum threshold to determine whether a song is played or not in ms: [Default: 10000 (10 seconds)]: ")
while True:
    ms_threshold = ms_threshold.strip()
    if len(ms_threshold) == 0:
        ms_threshold = "10000"
    try:
        ms_threshold = int(ms_threshold)
        break
    except ValueError:
        print("")
        print("Invalid value. Try again.")
        ms_threshold = input("Enter a minimum threshold to determine whether a song is played or not in ms: [Default: 10000 (10 seconds)]: ")

streaming_history_files = []

# Find all StreamingHistory.json files
print("")
print("Finding all StreamingHistory files...")
print("")
for file in os.listdir():
    if file.startswith("StreamingHistory"):
        streaming_history_files.append(file)

# Check to see if found any JSON files
if len(streaming_history_files) == 0:
    print("No StreamingHistory JSON files were found in this directory.")
else:
    print("Found " + str(len(streaming_history_files)) + " StreamingHistory files.")
    for f in streaming_history_files:
        print(" - " + str(f))

# Parse data into dictionaries for analysis
timesDate = {}
timesHr = {}
timesDay = {}
lenDay = {"Monday" : 0, "Tuesday" : 0, "Wednesday" : 0, "Thursday" : 0, "Friday" : 0, "Saturday" : 0, "Sunday" : 0}
timesArtist = {}
timesTracks = {}
print("")
print("Reading StreamingHistory files.")
for file in streaming_history_files:
    print(" - Reading " + str(file) + "...")
    with open(file, encoding="utf8") as json_file:
        data = json.load(json_file)
        print("    - " + str(len(data)) + " records found")
        for record in data:
            if int(record["msPlayed"]) < ms_threshold:
                continue
            date = record["endTime"][0:10]
            hr = record["endTime"][11:13]
            day = datetime.datetime.strptime(date, '%Y-%m-%d').strftime("%A")
            artist = record["artistName"]
            track = record["trackName"] + " by: " + artist
            msPlayed = record["msPlayed"]

            # Add to timesDate
            if date in timesDate:
                timesDate[date] = timesDate[date] + int(msPlayed)
            else:
                timesDate[date] = int(msPlayed)

            # Add to timesHr
            if hr in timesHr:
                timesHr[hr] = timesHr[hr] + int(msPlayed)
            else:
                timesHr[hr] = int(msPlayed)

            # Add to timesDay
            if day in timesDay:
                timesDay[day] = timesDay[day] + int(msPlayed)
            else:
                timesDay[day] = int(msPlayed)

            # Add to timesArtist
            if artist in timesArtist:
                timesArtist[artist] = timesArtist[artist] + int(msPlayed)
            else:
                timesArtist[artist] = int(msPlayed)

            # Add to timesTracks
            if track in timesTracks:
                timesTracks[track] = timesTracks[track] + int(msPlayed)
            else:
                timesTracks[track] = int(msPlayed)

            # Add to day counter
            lenDay[day] += 1

print("")
print("Data parsed.")
print("")

if not input("Store data? (Y/N) [Default: Y]: ").strip().lower() == "n":
    # Get file name
    file_root_name = input("Enter name for files: ")
    while file_root_name.strip() == "":
        print("")
        file_root_name = input("Invalid name. Enter name for files: ")

    # Write timesDate data
    with open(file_root_name+"_timesDate.spotifydata", "w", encoding="utf8", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        for key in timesDate:
            csv_writer.writerow([key, timesDate[key]])

    # Write timesHr data
    with open(file_root_name + "_timesHr.spotifydata", "w", encoding="utf8", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        for key in timesHr:
            csv_writer.writerow([key, timesHr[key]])

    # Write timesDay data
    with open(file_root_name+"_timesDay.spotifydata", "w", encoding="utf8", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        for key in timesDay:
            csv_writer.writerow([key, timesDay[key]])

    # Write timesArtist data
    with open(file_root_name+"_timesArtist.spotifydata", "w", encoding="utf8", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        for key in timesArtist:
            csv_writer.writerow([key, timesArtist[key]])

    # Write timesTracks data
    with open(file_root_name+"_timesTracks.spotifydata", "w", encoding="utf8", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        for key in timesTracks:
            csv_writer.writerow([key, timesTracks[key]])

if not input("See quick stats? (Y/N) [Default: Y]: ").strip().lower() == "n":
    print("")
    print("Total daily listening time:")
    print(timesDay)
    print(lenDay)
    for x in timesDay:
        print(" - " + x + ": " + str(timesDay[x] / 60000) + " minutes")
    print("")
    input("Press enter to continue...")

    print("")
    print("Artist leaderboard:")
    count = 1
    for x in sorted(timesArtist.items(), key=lambda i: i[1], reverse=True):
        print(str(count) + ". " + x[0] + ": " + str(x[1] / 60000) + " minutes")
        count += 1
    print("")
    input("Press enter to continue...")

    print("")
    print("Track leaderboard:")
    count = 1
    for x in sorted(timesTracks.items(), key=lambda i: i[1], reverse=True):
        print(str(count) + ". " + x[0] + ": " + str(x[1] / 60000) + " minutes")
        count += 1
    print("")
    input("Press enter to continue...")

    print("")
    print("Track leaderboard:")
    count = 1
    for x in sorted(timesHr.items(), key=lambda i: i[0], reverse=False):
        print(str(x[0]) + ":00 - " + str(x[1] / 60000) + " minutes")
        count += 1
    print("")
    input("Press enter to continue...")