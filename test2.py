import psutil

for proc in psutil.process_iter(['pid', 'name', 'username']):
    print(proc.info)
