python main.py file_num=8 cpus=1 ios=1 sched=fcfs
python main.py file_num=8 cpus=2 ios=1 sched=fcfs
python main.py file_num=8 cpus=4 ios=1 sched=fcfs
python main.py file_num=8 cpus=1 ios=2 sched=fcfs
python main.py file_num=8 cpus=1 ios=4 sched=fcfs
python main.py file_num=8 cpus=2 ios=2 sched=fcfs job_gen=static
python main.py file_num=8 cpus=2 ios=2 sched=fcfs job_gen=sporadic
python main.py file_num=8 cpus=2 ios=2 sched=sjf job_gen=normal
python main.py file_num=8 cpus=2 ios=2 sched=rr job_gen

