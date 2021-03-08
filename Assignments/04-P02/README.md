## The Producer/Consumer Problem - Part 1
#### Due: 03-17-2021 (Wednesday @ 2:30 p.m.)

The producer-consumer problem is a classic scenario in distributed systems involving two processes:

1. The producer, which writes data into the shared buffer.
2. The consumer, which reads from the shared buffer.

A good solution to this problem should satisfy the following three properties:

1. **Mutual exclusion:** The producer and consumer processes never access the shared buffer simultaneously.
2. **Non-starvation:** The consumer accesses the buffer infinitely often. (You may assume that the producer never runs out of data to supply, and the consumer never stops attempting to read new data.)
3. **Producer-consumer:**
    - The producer never overwrites the data buffer unless the consumer has already read the current data
    - The consumer never reads the data buffer unless it contains new data.

One algorithm for a single user producer-consumer uses a single flag bit. The flag bit is set by the producer when data ready to be read, and unset by the consumer once it has read the data. You could simplify this approach by only having the producer set the bit when it is done writing. 

### System "Liveness"

Your system much fullfill the liveness property. 

Several forms of **liveness** are recognized. The following ones are defined in terms of a multi-process system that has a critical section, protected by some mutual exclusion (mutex) device. All processes are assumed to correctly use the mutex; progress is defined as finishing execution of the critical section.

- Freedom from **deadlock** is a form of liveness, although a weak one. Consider a system with multiple processes and a single critical section, protected by some mutual exclusion device. Such a system is said to be deadlock-free if, when a group of processes is competing for access to the critical section at some point in time, then some process eventually makes progress at a later point in time. That process need not belong to the aforementioned group; it might have gained access at an earlier or even later moment.
- Freedom from **starvation** (or "finite bypass") is a stronger liveness guarantee than deadlock-freedom. It states that all processes vying for access to the critical region eventually make progress. `Any starvation-free system is also deadlock-free`.
- Stronger still is the requirement of **bounded bypass**. This means that, if `n` processes are competing for access to the critical region, then each process makes progress after being bypassed at most `f(n)` times by other processes for some function `f` <sup>[1]</sup>.
  
### Assignment

Our assignment will contain the following entities:

1. Centralized Coordinator (aka our cloud server)
2. Client Producer 
3. Client Consumer

#### Centralized Coordinator

The centralized coordinator will maintain the following attributes / behaviors:

1. It will keep track of all clients that are connecting (count them and assign a unique id like a uuid).
2. It is multi-threaded.
3. It can server different clients (one per thread) if data exists.
4. It will maintain a queue data structure to hold all items produced by our producer clients.
5. It will serve one produced item to one consumer. 
6. It will follow the "liveness" properties as stated above.
7. A counting semaphore will determine max clients that can be served.
8. It will maintain a log file of all transactions 
   - uuid of clients
   - produced items and by who
   - consumed items and by who
   - timestamps of all

To summarize the coordinators behavior, it should guarantee:

- A produced item should be served to only one consumer.
- None of the items in the queue would be missed.
- No producer or consumer should starve (wait forever).
- The program should not deadlock.

#### Stock Price

The stock price will have the following data:

- Symbol: `goog`
- Price: 314.55
- Timestamp: 1615233339

#### Client Producer 

The producer will maintain the following behaviors:

- The client producer will "produce" one stock price that can be generated at random.
- It sleeps for some configurable "time quantum" **`tp`** (we will figure out a good time quantum through class discussion).
- It will send a data "packet" (stock price) to the central server to be handled every time it wakes up.
- It goes back to sleep for **`tp`** time.


#### Client Consumer

The consumer will maintain the following behaviors:

- The client consumer will "consume" a stock price whenever it can. 
- It sleeps for some configurable "time quantum" **`tc`** (again we will figure out a good time quantum through class discussion).
- It will log all transactions including:
  - Stock consumed
  - Timestamp
  - Uuid id of producer
- Once it consumes a stock price, it will go back to sleep for **`tc`** time.



### Deliverables:

- Presentations in class ...
- More to come.


Sources: 

1. https://en.wikipedia.org/wiki/Liveness