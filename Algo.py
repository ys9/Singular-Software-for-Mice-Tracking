import csv
from math import sqrt

class Nap:
    nap_num = 0         #nap number during recording
    time_slept = 0      #how long a nap occurs for
    start = 0           #start time of nap
    end = 0             #end time of nap (-1 if napping when recording ends)
    time_since_last = 0 #time since mouse had last napped
    
class Mouse:
    
    mid = 0             # Mouse ID, camera 1, 2, 3, or 4
    nap_list = None     # List of all naps taken by mouse during recording
    nap_count = 0
    nap_track = 0       #count for seconds to check is asleep for >= 40 seconds, iterates by 5 seconds of low velocity
    time_slept = 0
    start = 0
    end = 0
    napping = False
    last_point = (0, 0)

def algo(csv_filename):
    time_count = 0  # total recording time
    sec_per_frame = 5  # how many seconds between each point
    
    with open(csv_filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        
        ncol = len(next(csv_reader))  # Read first line and count columns
        csv_file.seek(0)
        
        nmice = round(ncol / 2)
        
        mice = list()
        for i in range(0, nmice):
            mouse = Mouse()
            mouse.nap_list = list()
            mouse.mid = i + 1
            mice.append(mouse)
        
        # Every row 5 seconds have past, start at 0 seconds
        for row in csv_reader:
            
            # FOR EVERY MOUSE
            # ITERATE MOUSE COUNTER 1 TO NUMBER OF MICE
            for mouse in mice:
                if line_count == 0:
                    mouse.last_point = (int(row[0 + 2 * (mouse.mid - 1)]), int(row[1 + 2 * (mouse.mid - 1)]))

                # calculations happen here
                else:
                    velocity = sqrt((int(row[0 + 2 * (mouse.mid - 1)]) - int(mouse.last_point[0])) ** 2 + (
                                int(row[1 + 2 * (mouse.mid - 1)]) - int(mouse.last_point[1])) ** 2) / sec_per_frame
                    # Nap tracking
                    # movement has stopped
                    if (velocity <= 1):
                        mouse.nap_track += sec_per_frame
                        
                        if (mouse.nap_track == 40):  # officially a nap
                            mouse.nap_count += 1
                            mouse.start = time_count - 40
                            mouse.napping = True
                            mouse.time_slept = 40
                        
                        elif (mouse.nap_track > 40):  # nap is continuing
                            mouse.time_slept += sec_per_frame
                    
                    # nap has just finished so save stats of nap and reset
                    elif (mouse.napping):  # velocity is above 1 so mouse is awake, but was napping
                        mouse.end = time_count
                        new_nap = Nap()
                        new_nap.time_slept = mouse.time_slept + sec_per_frame
                        new_nap.nap_num = mouse.nap_count
                        new_nap.start = mouse.start
                        new_nap.end = mouse.end

                        # to calculate have to look at last nap in nap list and check that nap end subtracted by this nap start
                        if (mouse.nap_list.__len__() > 0):
                            last_nap = mouse.nap_list[mouse.nap_list.__len__() - 1]
                            new_nap.time_since_last = mouse.start - last_nap.end
                        # object naps: list
                        mouse.nap_list.append(new_nap)
                        mouse.nap_count = mouse.nap_count
                        
                        mouse.nap_track = 0
                        mouse.napping = False
                    
                    else:
                        mouse.nap_track = 0

                    # end of loop saving
                    mouse.last_point = (row[0 + 2 * (mouse.mid - 1)], row[1 + 2 * (mouse.mid - 1)])

                # each mouse end
            line_count += 1
            time_count += sec_per_frame
        
        # FOR EVERY MOUSE, IF THE MOUSE IS NAPPING AT END OF RECORDING, RECORD DATA
        for mouse in mice:
            if (mouse.napping):
                mouse.end = time_count
                new_nap = Nap()
                new_nap.time_slept = mouse.time_slept + sec_per_frame
                new_nap.nap_num = mouse.nap_count
                new_nap.start = mouse.start
                
                new_nap.end = -1
                
                # to calculate have to look at last nap in nap list and check that nap end subtracted by this nap start
                if (mouse.nap_list.__len__() > 0):
                    last_nap = mouse.nap_list[mouse.nap_list.__len__() - 1]
                    new_nap.time_since_last = mouse.start - last_nap.end + sec_per_frame
                # object naps: list
                mouse.nap_list.append(new_nap)
                mouse.nap_count = mouse.nap_count

        # TIME TESTING
        print("Duration of recording: ", time_count, "seconds")

        # NAP TESTING
        # FOR EVERY MOUSE IN MOUSE LIST
        for mouse in mice:
            print("Mouse: ", mouse.mid)
            print("Nap count: ", mouse.nap_count)
            print("---------------------\n")

            # LIST NAPS FOR MOUSE
            for i in mouse.nap_list:
                print("Nap num: ", i.nap_num)
                print("Time slept: ", i.time_slept)
                print("start time: ", i.start)
                print("end time: ", i.end)
                print("time since last nap: ", i.time_since_last)
                print()
    
    with open('testout.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for mouse in mice:
            writer.writerow(['Mouse', mouse.mid, mouse.nap_count])
            
        for mouse in mice:
            writer.writerow(['Mouse', mouse.mid])
            writer.writerow(['Mouse', 'Nap num', 'time slept', 'start time', 'end time', 'time since last nap'])
            
            for nap in mouse.nap_list:
                writer.writerow([mouse.mid, nap.nap_num, nap.time_slept, nap.start, nap.end, nap.time_since_last])
    
    return 0

#CSV file needs to have exactly 1 newline at end of file. no more.
#5 seconds per frame
def main():
    algo('coor.csv')
    return 0

if __name__ == '__main__':
    main()
