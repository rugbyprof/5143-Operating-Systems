

with open("datafile.dat") as f:
    data = f.read().split("\n")



for process in data:
    if len(process) > 0:
        parts = process.split(' ')
        arrival = parts[0]
        pid = parts[1]
        priority = parts[2]
        bursts = parts[3:]

        print(f"{arrival}, {pid}, {priority} {len(bursts)}{bursts}")

