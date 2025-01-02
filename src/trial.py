# new word
import time

input("Press Enter to continue...")

start_time = time.time()
last_time = time.time()
lap_num = 1


try:
    while True:
        input()
        lap_time = round(time.time() - last_time,2 )
        total_time = round (time.time() - start_time,2)
        print(f"lap number:{lap_num}  {total_time} {lap_time}")
        lap_num +=1
        last_time = time.time()
except KeyboardInterrupt:
    print("program ended")
        