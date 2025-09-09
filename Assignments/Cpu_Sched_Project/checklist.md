## Checklist for CPU Scheduling Project|

| Category                  | Task                                                                                                           | Completed |
| ------------------------- | -------------------------------------------------------------------------------------------------------------- | --------- |
| General Requirements      | Implement a simulation for CPU scheduling based on the given algorithms:                                       |           |
|                           | - First-Come-First-Serve (FCFS)                                                                                | &#x2610;  |
|                           | - Round-Robin (RR)                                                                                             | &#x2610;  |
|                           | - Priority-Based Scheduling (PB)                                                                               | &#x2610;  |
|                           | - Multi-Level-Feedback-Queue (MLFQ)                                                                            | &#x2610;  |
|                           | Include a visualization of all six process states (~~NEW~~, READY, RUNNING, WAITING, IO, ~~TERMINATED~~, EXIT) | &#x2610;  |
|                           | **Implement functionality to pause and resume the simulation.**                                                | &#x2610;  |
| Inputs and Configuration  | Accept command-line arguments for:                                                                             |           |
|                           | - Scheduling algorithm (`sched=`)                                                                              | &#x2610;  |
|                           | - Random seed (`seed=`)                                                                                        | &#x2610;  |
|                           | - Number of CPUs (`cpus=`)                                                                                     | &#x2610;  |
|                           | - Number of IO devices (`ios=`)                                                                                | &#x2610;  |
|                           | **Ensure the random seed is applied consistently for reproducible runs.**                                      | &#x2610;  |
| Simulation Functionality  | Correctly transition processes through states:                                                                 |           |
|                           | - ~~NEW~~ → READY → RUNNING → WAITING → ~~TERMINATED~~ → EXIT                                                  | &#x2610;  |
|                           | Handle time quantums for Round-Robin.                                                                          | &#x2610;  |
|                           | Implement dynamic priority adjustments for Priority-Based Scheduling.                                          | &#x2610;  |
|                           | Implement friendly aging so processes do not starve (for too long) in the system.                              | &#x2610;  |
| Visualization             | Display the ~~six~~five states and their queues dynamically as the simulation progresses.                      | &#x2610;  |
|                           | Use a color-coded or organized format for readability (e.g., NCurses, Rich, or DearPyGui).                     | &#x2610;  |
|                           | Include key messages during the simulation:                                                                    |           |
|                           | - Process entering the NEW queue.                                                                              | &#x2610;  |
|                           | - Process obtaining a CPU or IO device.                                                                        | &#x2610;  |
|                           | - Process termination and stats display.                                                                       | &#x2610;  |
| Output and Statistics     | Generate and display the following at the end of each simulation:                                              |           |
|                           | - `CPU utilization percentage`.                                                                                | &#x2610;  |
|                           | - `Average Turnaround Time (TAT)`.                                                                             | &#x2610;  |
|                           | - `Average Ready Wait Time (RWT)`.                                                                             | &#x2610;  |
|                           | - `Average IO Wait Time (IWT)`.                                                                                | &#x2610;  |
|                           | Write aggregate data for all runs to a CSV file:                                                               |           |
|                           | - Algorithms: FCFS, RR, PB, MLFQ.                                                                              | &#x2610;  |
|                           | - Number of CPUs: 1–4.                                                                                         | &#x2610;  |
|                           | - Number of IO Devices: 2, 4, 6.                                                                               | &#x2610;  |
|                           | - Time Quantums for RR: 3, 5, 7, 9.                                                                            | &#x2610;  |
| Presentation Requirements | Present results for six simulation runs (two per scheduling algorithm):                                        |           |
|                           | - Use the provided random seeds for consistency.                                                               | &#x2610;  |
|                           | Include detailed outputs for each run:                                                                         |           |
|                           | - Messages indicating state transitions.                                                                       | &#x2610;  |
|                           | - Individual process stats at termination.                                                                     | &#x2610;  |
|                           | - Final aggregate statistics.                                                                                  | &#x2610;  |
|                           | Ensure visualizations are clear and align with the simulation states.                                          | &#x2610;  |
| Deliverables              | Submit the code and a detailed write-up on GitHub:                                                             |           |
|                           | - Include a README with a description of the project, implementation process, and team members.                | &#x2610;  |
|                           | - Ensure the repository is well-organized and includes necessary files.                                        | &#x2610;  |
|                           | Prepare for an in-class presentation following the outlined guidelines.                                        | &#x2610;  |
