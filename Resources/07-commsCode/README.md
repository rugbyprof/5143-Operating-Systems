## Comms Class - Sender and Receiver
#### None


This folder describes a pair of classes that are written as an abstraction to simplify the use of sending messages to a message passing queue hosted up there ... in the cloud, being listened to by 1 or more players.  As a note, a queue based message passing system is a decent way to implement loosely ordered, or turnbased gameplay in our situation.

We are using: 

![](http://battleshipgame.fun:15672/img/rabbitmqlogo.svg) 

Here are some tutorials on how they work: [Tutorial](https://www.rabbitmq.com/getstarted.html)


## Howto:

### Sender:

- To get started sending messages, you need to initialize  the `CommSender` class with a copy of your credentials.
    
```python 
# Credentials dictionary will necessary info. I will describe line below the snippet.
creds = {
    "exchange": "5443-2D",
    "port": "5672",
    "host": "crappy2d.us",
    "user": "yourUserName",
    "password": "yourassignedpassword",
    "hash": "61ec12b68d0ded5f6a84b7d1f6d4d8e70695c2ba5dd7176fc3e4c3d53db9ecf2"
}

# Instance of class with creds being passed in as kwargs
commsSender = CommsSender(**creds)
```

- exchange: The "name" of the queue defined for your group.
- port: The port number the server is listening on for incoming messages.
- host: The domain name (or ip address) of the server so we can find it.
- user: Unique username for a player
- password: Secure password for a player
- hash: A hash token the needs to be sent with all requests. 


    
### Messages:

Messages contain multiple parts: 
1. A queue name
2. A topic or keyword
3. A message or specfics dealing with a command.

The topic is to direct the message to the proper queue so the recipient will receive it. 

- The topic can be anything, but for our games we will use some conventions so everyone will send and receive messages correctly.  
- The first rule is to send a message to another team you use the following format: 
  - `teamname.` where you replace the teamname with an actual teamname, 
  - and the hashtag with a specific command like `fire` (which is for now the only command we have between teams). The second rule is if you want to send a message to everyone you use `broadcast.#`. Anything with the keyword `broadcast` will go to everyone. 

1. The message can be anything, unless you're firing upon a team, then it needs to be proper json with proper keys and values. 

```python
# Example broadcast message
cmd = "broadcast.#","Hey everybody!!"
commsSender.sendCommand(cmd[0],cmd[1])


# Example team fire message
## d = decimal 
## f = float
## lon/lat is where the projectile should strike
## angle is the angle in which it is coming
## kg is the weight of the projectile

cmd = "axis.fire","{'lon':dd.fffff,'lat':dd.fffff,'angle':dd.ff,'kg':dd.ff}"
commsSender.sendCommand(cmd[0],cmd[1])

# you could put the 'commands' directly in the function call:
commsSender.sendCommand("axis.fire","{'lon':dd.fffff,'lat':dd.fffff,'angle':dd.ff,'kg':dd.ff}")
```
Once a sender sends a message, it can close its connection, unlike a listener who must always be listening. 

```python
commsSender.closeConnection()
```
### Listener:
