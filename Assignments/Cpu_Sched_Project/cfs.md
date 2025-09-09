## CFS Notes

The Completely Fair Scheduler (CFS) is a CPU scheduling algorithm used in modern operating systems, notably Linux, to ensure fair distribution of CPU time among tasks. Unlike traditional priority-based algorithms, CFS is based on the concept of fair queuing, which aims to allocate CPU time proportionally across all tasks according to their weights (priority levels).

Key Concepts of CFS:

1. Virtual Runtime: Each task is assigned a virtual runtime (vruntime), which represents the amount of CPU time the task has “virtually” consumed, adjusted by its priority weight.
   - Lower-priority tasks accumulate vruntime faster, giving higher-priority tasks an advantage in CPU allocation.
2. Red-Black Tree: CFS uses a red-black tree (a balanced binary tree) to organize tasks by their vruntime.
   - The task with the smallest vruntime (the one that’s been least served) is always at the root, ensuring that the least-served task is selected next for execution.
3. Scheduling Policy:
   - CFS tries to give each task a fair share of CPU time relative to its priority.
   - On each scheduling event (like a timer interrupt or task completion), the scheduler picks the task with the smallest vruntime from the red-black tree and runs it.
4. Granularity: The scheduler defines a minimum time slice (granularity), which sets a lower bound on how long a task should run before switching, ensuring efficiency by reducing excessive context switching.

Algorithmic Steps of CFS:

1. Task Selection:

   - Find the task with the smallest vruntime in the red-black tree (this task has received the least CPU time relative to its priority).
   - Schedule this task to run.

2. Runtime Adjustment:

   - As the task runs, update its vruntime by adding the elapsed time (scaled by its weight).
   - This adjustment means higher-priority tasks (with lower weights) accumulate vruntime more slowly, allowing them to run more frequently relative to lower-priority tasks.

3. Reinsertion and Balance:

   - After a task’s time slice is over, or if it voluntarily yields the CPU, reinsert it into the red-black tree according to its updated vruntime.
   - This keeps the tree balanced and ensures that the least-served task is always chosen next.

4. Handling New Tasks:

   - New tasks start with a vruntime slightly below the minimum vruntime of the current tasks, allowing them to receive CPU time promptly when added.

Summary:

CFS’s approach to scheduling is unique in that it doesn’t strictly adhere to traditional time slices or priority queues but instead focuses on distributing CPU time fairly based on vruntime. This makes it highly efficient for systems with mixed workloads, providing responsiveness and preventing starvation by ensuring all tasks progress over time.

In the Completely Fair Scheduler (CFS), the virtual runtime (vruntime) is a key concept that helps achieve fair CPU allocation among tasks. The vruntime of a task represents how much CPU time it has “virtually” consumed, factoring in its priority weight. Lower vruntime indicates that a task has had less CPU time compared to others, making it more likely to be scheduled next. Here’s a breakdown of how vruntime works, along with an example.

#### How Virtual Runtime Works

1. Initialization of vruntime:
   - When a new task starts, it is assigned an initial vruntime, usually a small value slightly below the current minimum vruntime in the system. This initial setting allows the new task to start running quickly after creation.
2. Accumulation of vruntime:

   - Every time a task runs, its vruntime increases. The rate at which vruntime increases is proportional to the task’s weight, which is derived from its nice value (priority). Lower-priority tasks (with higher nice values) accumulate vruntime faster, causing them to yield the CPU sooner than higher-priority tasks.
   - A task’s vruntime is calculated as:

     - `vruntime += time elapsed * (weight of highest priority / weight of current task)`

   - This means that tasks with higher priority (and lower nice values) accumulate vruntime more slowly, allowing them to use more CPU time.

3. Task Selection and vruntime Comparison:
   - CFS maintains a red-black tree sorted by vruntime, where the task with the smallest vruntime is always at the root. This task is selected to run next since it has received the least CPU time relative to its priority.
   - After a task completes its time slice, CFS re-inserts it into the tree at its updated vruntime position.

#### Example of vruntime in Action

**Imagine a system with two tasks:**

- Task A with a normal priority (nice value of 0).
- Task B with a lower priority (nice value of +5).

The weights (inversely related to nice values) for these tasks differ, so Task A (higher priority) will accumulate vruntime more slowly than Task B.

1. Initial Scheduling:
   - Task A and Task B start with similar vruntimes. Task A, being the higher-priority task, will be scheduled to run first if both vruntimes are equal.
2. Running and Updating vruntime:
   - Suppose Task A runs for 10ms. Because of its higher priority, its vruntime might increase by only 5ms.
   - Task B, if it runs for the same 10ms, will accumulate a vruntime of about 15ms due to its lower priority.
3. Red-Black Tree Reinsertion:
   - After Task A and Task B have both run, Task A’s vruntime is lower than Task B’s. CFS selects Task A to run next, ensuring that it receives more CPU time over time, respecting the priority difference.

Through vruntime, CFS achieves a balance: higher-priority tasks use the CPU longer without strict time slices, while lower-priority tasks are not starved, as they eventually get their turn when higher-priority tasks accumulate enough vruntime.

===

You could theoretically use a heap instead of a red-black tree for the CFS (Completely Fair Scheduler), but there are important trade-offs and reasons why a red-black tree (or other balanced binary search trees) is usually preferred.

Differences Between Red-Black Tree and Heap in the Context of CFS

1. Operation Complexity:

   - Both a min-heap and a red-black tree can provide the minimum vruntime task in `O(log N)` time, but they perform other operations differently:
   - Red-Black Tree: CFS uses the red-black tree to keep tasks sorted by their vruntime, which enables efficient insertion, deletion, and searching. Searching by vruntime in a red-black tree can be done in `O(log N)`.
   - Min-Heap: A min-heap is optimized for finding and removing the minimum element but does not support efficient arbitrary insertion or deletion, as it does not maintain a sorted order beyond the minimum at the root.

2. Insertion and Deletion of Arbitrary Elements:

   - In CFS, tasks frequently need to be inserted, removed, and adjusted based on vruntime changes.
   - A red-black tree allows direct insertion and deletion at arbitrary locations, which is important for adjusting vruntime and rebalancing tasks as they change in priority.
   - In a heap, insertion or deletion of arbitrary elements (other than the minimum) is more complex and inefficient, requiring reordering and reheapification of the heap structure.

3. Fair Scheduling and vruntime Adjustment:

   - CFS continuously adjusts vruntime as tasks accumulate CPU time, meaning tasks need to be efficiently repositioned in the data structure.
   - A red-black tree maintains a sorted structure, allowing CFS to reinsert tasks efficiently after adjusting vruntime.
   - In a heap, this repositioning after each update would require finding the position of the updated task and then reordering the heap, which can be inefficient in the context of frequent adjustments.

4. Scheduling Preemptions:

   - CFS uses vruntime to determine which task has had the least CPU time and therefore should be scheduled next.
   - With a red-black tree, you can retrieve and reinsert elements at arbitrary positions, making it straightforward to handle preemptions by adjusting the tree.
   - A heap would require more restructuring to maintain a correct ordering after each vruntime update.

Conclusion

While a min-heap could provide a similar minimum retrieval function, the red-black tree is chosen for CFS because of its flexibility and efficiency in handling arbitrary insertions, deletions, and updates—key operations for fair scheduling based on continuously adjusted vruntime values. If you need to ensure all tasks get scheduled fairly based on dynamically changing priorities, a balanced binary search tree like a red-black tree or AVL tree remains more suitable than a heap.
