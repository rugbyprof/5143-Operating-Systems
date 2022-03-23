## Http Producer Consumer

Using the http protocol, implement a producer / consumer framework where producers will send data to the server to stored in some shared data structure, and consumers will request data from the servers shared memory structure. This project is not very hard, so don't overthink it. We will expand on this project for our next one, adding the ability to synchronize events over the network. For now,

-   The server, will just listen on a port waiting for "clients" to send data or request data.
-   The server should print messages to the console as incoming requests are received.
-   Clients will initiate a network connection with the server, and then either send data or request data, depending on current need.
-   The server should use threads to respond to incoming requests by producers and consumers.
-

You need to have a shared data structure
There should be one producer thread. It should add random strings of text (from 4-10 characters long) to the data structure. (add 100 of them)
There should be 2 consumer threads. Each thread should remove a string from the shared data structure, and then print the string along with some identification of the thread which did the consuming.
All three threads should, of course, be running in parallel.

https://realpython.com/intro-to-python-threading/

https://medium.com/geekculture/distributed-lock-implementation-with-redis-and-python-22ae932e10ee

https://www.laurentluce.com/posts/python-threads-synchronization-locks-rlocks-semaphores-conditions-events-and-queues/
