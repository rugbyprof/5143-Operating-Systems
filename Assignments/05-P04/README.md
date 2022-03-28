## Reader Writer Part 1

#### Due: TBD

### References + Help

-   https://realpython.com/python-concurrency/
-   https://realpython.com/async-io-python/
-   https://stackoverflow.com/questions/49005651/how-does-asyncio-actually-work/51116910#51116910

Using the python concurrency mechanism that best fits the job, implement a reader / writer framework that will keep a shared memory section safe so that readers will get accurate data and writers won't conflict with each other. This is the first part of our concurrency project in which we protect a critical section of local code. Next project will involve protecting a similar critical section of code via network requests.

The reader/writer problem is a classic which is still very much relevant in todays architexture, especially with database and file servers being so prevalent. The problem is as follows:

> -   Any processes can read from the shared resource, even while others are reading.
> -   Any process may write to the shared resource.
> -   No process may access the shared resource for either reading or writing <ins>**while another process is in the act of writing to it**</ins>.
>
>     <sub>Note: The term "process" is interchangeable with "thread".</sub>

This project is not very hard, so don't overthink it. We will expand on this project for our next one, adding the ability to synchronize events over the network. For now, we are only locking the "shared memory" to ensure data integrity.

### Server

The "server" is our program in charge of monitoring / controlling the readers and writers. It has the following responsibilities:

-   Waits and listens for "clients" to attempt a read or a write.
-   Controls access to shared memory using some concurrency mechanism.
-   Should print messages to the console as events are processed.

### Clients

#### Reader

-   Wants to read from shared memory.
-   Makes no changes.
-   Needs to permission for access (somewhat).

#### Writer

-   Wants to edit one or more shared memory values.
-   Needs to obtain access before this happens.

```
['MOV','ADD','SUB','MUL','DIV','SET','READ','WRITE']
```

-   'MOV': `MOV A B` = Copy value from register `A` to register `B`
-   'ADD': `ADD A B` Add values in `A` and `B`, storing result in `A`.
-   'SUB': `SUB A B` Subtract values in `A` and `B`, storing result in `A`.
-   'MUL': `MUL A B` Multiply values in `A` and `B`, storing result in `A`.
-   'DIV': `DIV A B` Divide values in `A` and `B`, storing result in `A`.
-   'SET': `SET B 7` Load 7 into `B`.
-   'READ': `READ B 100` Read memory location `100` into `B`.
-   'WRITE': `WRITE A 100` Write contents of A into memory location `100`.

Generate instructions:

ADD 27 N
SET 97 I

### Shared Memory

```python
sharedMem = {
    'A': 0,
    'B': 0,
    'C': 0,
    'D': 0,
    'E': 0,
    'F': 0,
    'G': 0,
    'H': 0,
    'I': 0,
    'J': 0,
    'K': 0,
    'L': 0,
    'M': 0,
    'N': 0,
    'O': 0,
    'P': 0,
    'Q': 0,
    'R': 0,
    'S': 0,
    'T': 0,
    'U': 0,
    'V': 0,
    'W': 0,
    'X': 0,
    'Y': 0,
    'Z': 0
}
```

You need to have a shared data structure
There should be one producer thread. It should add random strings of text (from 4-10 characters long) to the data structure. (add 100 of them)
There should be 2 consumer threads. Each thread should remove a string from the shared data structure, and then print the string along with some identification of the thread which did the consuming.
All three threads should, of course, be running in parallel.

https://realpython.com/intro-to-python-threading/

https://medium.com/geekculture/distributed-lock-implementation-with-redis-and-python-22ae932e10ee

https://www.laurentluce.com/posts/python-threads-synchronization-locks-rlocks-semaphores-conditions-events-and-queues/
