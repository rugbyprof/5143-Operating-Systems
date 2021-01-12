# Bash Scripting - An introduction to bash.

## Introduction

A Bash script is a plain text file which contains a series of commands. These commands are a mixture of commands we would normally type ourselves on the command line (such as `ls` or `cp` for example) and commands we could type on the command line but generally wouldn't (you'll discover these over the next few pages). An important point to remember though is:

>Anything you can run normally on the command line can be put into a script and it will do exactly the same thing. Similarly, anything you can put into a script can also be run normally on the command line and it will do exactly the same thing.

It is convention to give files that are Bash scripts an extension of .sh (`myscript.sh` for example). Linux is an extension-less system so a script doesn't necessarily have to have this characteristic in order to work.

## How do you run a script?

- Permission need to be correct. The file has to be executable.
- Note: the `~$` in all the scripts is the "command prompt".  So don't assume that is part of the command.

```bash
~$ chmod 755 myscript.sh # Sets executable for Owner, Group, and All (as well as readable by all and writable by the owner)
```

or

```bash
~$ chmod u+x myscript.sh # Sets executable for owner
~$ chmod a+x myscript.sh # Sets executable for all
```

- `u`: the user who owns it
- `g`: other users in the file's group
- `o`: other users not in the file's group
- `a` or all users

You can add more than just execute with the `+x`, but that's not for this lesson.


```bash
~$ ./myscript.sh
# Output: ./myscript.sh: Permission denied
~$ ls -l myscript.sh
#Output: -rw-r--r-- 18 owner group 4096 Feb 17 09:12 myscript.sh
~$ chmod 755 myscript.sh
~$ ls -l myscript.sh
# Output: -rwxr-xr-x 18 owner group 4096 Feb 17 09:12 myscript.sh
~$ ./myscript.sh
# Output: Hello World!
```

#### Example myscript.sh

```bash
#!/bin/bash
# A sample Bash script

echo Hello World!
```
 

- **Line 1** - Is what's referred to as the shebang. See below for what this is.
- **Line 2** - This is a comment. Anything after # is not executed. It is for our reference only.
- **Line 4** - Is the command `echo` which will print a message to the screen. You can type this command yourself on the command line and it will behave exactly the same.


## Why the ./

You've possibly noticed that when we run a normal command (such as ls) we just type its name, but when running our script we put a `./` in front of it. When you just type a name on the command line Bash tries to find it in a series of directories stored in a variable called `$PATH`. We can see the current value of this variable using the command echo (you'll learn more about variables in the next section).

```bash
~$ echo $PATH
~$ /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
~$ 
```

The directories are separated by " : "

Bash only looks in those specific directories and doesn't consider sub directories or your current directory. It will look through those directories in order and execute the first instance of the program or script that it finds.

The `$PATH` variable is an individual user variable so each user on a system may set it to suit themselves.

This is done for a few different reasons.

- It allows us to have several different versions of a program installed. We can control which one gets executed based on where it sits in our `$PATH`.
- It allows for convenience. As you saw above, the first directory for myself is a bin directory in my home directory. This allows me to put my own scripts and programs there and then I can use them no matter where I am in the system by just typing their name. I could even create a script with the same name as a program (to act as a wrapper) if I wanted slightly different behavior.
- It increases safety - For example a malicious user could create a script called `ls` which actually deletes everything in your home directory. You wouldn't want to inadvertently run that script. But as long as it's not in your `$PATH` that won't happen.

If a program or script is not in one of the directories in your `$PATH` then you can run it by telling Bash where it should look to find it. You do so by including either an absolute or relative path in front of the program or script name. You'll remember that dot ( . ) is actually a reference to your current directory. Assuming this script is in my home directory I could also have run it by using an `absolute path`.

```bash
~$ /home/user/assignment1/myscript.sh
~$ Hello World!
~$ 
```

## The Shebang (#!)

**\#!/bin/bash**

This is the first line of the script above. The hash exclamation mark ( #! ) character sequence is referred to as the Shebang. Following it is the path to the interpreter (or program) that should be used to run (or interpret) the rest of the lines in the text file. (For Bash scripts it will be the path to Bash, but there are many other types of scripts and they each have their own interpreter.)

Formatting is important here. The shebang must be on the very first line of the file (line 2 won't do, even if the first line is blank). There must also be no spaces before the `#` or between the `!` and the path to the interpreter.

Whilst you could use a relative path for the interpreter, most of the time you are going to want to use an absolute path. You will probably be running the script from a variety of locations so absolute is the safest (and often shorter than a relative path too in this particular case).

It is possible to leave out the line with the shebang and still run the script but it is unwise. If you are at a terminal and running the Bash shell and you execute a script without a shebang then Bash will assume it is a Bash script. So this will only work assuming the user running the script is running it in a Bash shell and there are a variety of reasons why this may not be the case, which is dangerous.

You can also run Bash, passing the script as an argument.

```bash
~$ bash myscript.sh
~$ Hello World!
~$ 
```

Whilst this is safe it also involves unnecessary typing every time you want to run the script.

## Formatting

Indenting is not required but it does make your code easier to read and make it harder to make simple errors.

===========================================================================

# Bash Scripting: Variables

## Introduction

A variable is a temporary store for a piece of information. There are two actions we may perform for variables:

- Setting a value for a variable.
- Reading the value for a variable.

Variables may have their value set in a few different ways. The most common are to set the value directly and for its value to be set as the result of processing by a command or program. You will see examples of both below.

To read the variable we then place its name (preceded by a $ sign) anywhere in the script we would like. Before Bash interprets (or runs) every line of our script it first checks to see if any variable names are present. For every variable it has identified, it replaces the variable name with its value. Then it runs that line of code and begins the process again on the next line.

Here are a few quick points on syntax. They will be elaborated on and demonstrated as we go into more detail below.

- When referring to or reading a variable we place a `$` sign before the variable name.
- When setting a variable we leave out the `$` sign.
- Some people like to always write variable names in uppercase so they stand out. It's your preference however. They can be all uppercase, all lowercase, or a mixture.
- A variable may be placed anywhere in a script (or on the command line for that matter) and, when run, Bash will replace it with the value of the variable. This is made possible as the substitution is done before the command is run.

## Command line arguments

Command line arguments are commonly used and easy to work with so they are a good place to start.

When we run a program on the command line you would be familiar with supplying arguments after it to control its behavior. For instance we could run the command:
- `ls -l /etc`

where:

- `-l` and 
- `/etc` 

are both command line arguments to the command `ls`. We can do similar with our bash scripts. To do this we use the variables `$1` to represent the first command line argument, `$2` to represent the second command line argument and so on. These are automatically set by the system when we run our script so all we need to do is refer to them.

Let's look at an example.

**mycopy.sh**
```sh
#!/bin/bash
# A simple copy script

cp $1 $2

# Let's verify the copy worked

echo Details for $2
ls -lh $2
```

- **Line 4** - run the command `cp` with the first command line argument as the source and the second command line argument as the destination.
- **Line 8** - run the command `echo` to print a message.
- **Line 9** - After the copy has completed, run the command `ls` for the destination just to verify it worked. We have included the options `l` to show us extra information and `h` to make the size human readable so we may verify it copied correctly.


We'll discuss their command line arguments a little more later.

## Other Special Variables

There are a few other variables that the system sets for you to use as well.

| Variable      |       Description                                             |
|:--------------|:--------------------------------------------------------------|
|**$0** | The name of the Bash script. |
|**$1** | $9 | The first 9 arguments to the Bash script. (As mentioned above.) |
|**$#** | How many arguments were passed to the Bash script. |
|**$@** | All the arguments supplied to the Bash script. |
|**$?** | The exit status of the most recently run process. |
|**$$** | The process ID of the current script. |
|**$USER** | The username of the user running the script. |
|**$HOSTNAME** | The hostname of the machine the script is running on. |
|**$SECONDS** | The number of seconds since the script was started. |
|**$RANDOM** | Returns a different random number each time is it referred to. |
|**$LINENO** | Returns the current line number in the Bash script. |


- The command `env` will show you a listing of other variables which you may also refer to.

Some of these variables may seem useful to you now. Others may not. As we progress to more complex scripts in later sections you will see examples of how they can be useful.

## Setting Our Own Variables

As well as variables that are preset by the system, we may also set our own variables. This can be useful for keeping track of results of commands and being able to refer to and process them later.

There are a few ways in which variables may be set (such as part of the execution of a command) but the basic form follows this pattern:

**Correct:**

- `variable=value`

Note there is NO SPACE on either side of the equals ( `=` ) sign. We also leave off the `$` sign from the beginning of the variable name when setting it.

**Not-Correct:**

- `variable = value`
- `variable =value`
- `variable= value`
- `variable=$value`

Variable names may be uppercase or lowercase or a mixture of both but Bash is a case sensitive environment so whenever you refer to a variable you must be consistent in your use of uppercase and lowercase letters. You should always make sure variable names are descriptive. This makes their purpose easier for you to remember.

Here is a simple example to illustrate their usage.

**simplevariables.sh**

```sh
#!/bin/bash
# A simple variable example

#cmd1
myvariable=Hello

anothervar=Fred

echo $myvariable $anothervar
echo

sampledir=/etc

ls $sampledir

```

- **Lines 4 and 6** - set the value of the two variables `myvariable` and `anothervar`.
- **Line 8** - run the command echo to check the variables have been set as intended.
- **Line 9** - run the command echo this time with no arguments. This is a good way to get a blank line on the screen to help space things out.
- **Line 11** - set another variable, this time as the path to a particular directory.
- **Line 13** - run the command ls substituting the value of the variable `sampledir` as its first command line argument.


## Quotes

- In the example above we kept things nice and simple. The variables only had to store a single word. When we want variables to store more complex values however, we need to make use of quotes. This is because under normal circumstances Bash uses a space to determine separate items.
- Remember, commands work exactly the same on the command line as they do within a script so it can sometimes be easier to experiment on the command line.
- When we enclose our content in quotes we are indicating to Bash that the contents should be considered as a single item. 
- You may use single quotes ( `'` ) or double quotes ( `"` ).
    - Single quotes will treat every character literally.
    - Double quotes will allow you to do substitution (that is include variables within the setting of the value).


## Command Substitution

Command substitution allows us to take the output of a command or program (what would normally be printed to the screen) and save it as the value of a variable. To do this we place it within brackets, preceded by a `$` sign.

```bash
~$ myvar=$( ls /etc | wc -l )

~$ echo There are $myvar entries in the directory /etc
```

Command substitution is nice and simple if the output of the command is a single word or line. If the output goes over several lines then the newlines are simply removed and all the output ends up on a single line.

```bash
~$ ls
bin Documents Desktop ...
Downloads public_html ...
~$ myvar=$( ls )
~$ echo $myvar
bin Documents Desktop Downloads public_html ...
~$ 
```

- Normally this output would be over several lines. It was shortened it a bit in the example above just to save space.
- When we save the command to the variable `myvar` all the newlines are stripped out and the output is now all on a single line.


## Exporting Variables

Remember how in the previous section we talked about scripts being run in their own process? This introduces a phenomenon known as `scope` which affects variables amongst other things. The idea is that variables are limited to the process they were created in. Normally this isn't an issue but sometimes, for instance, a script may run another script as one of its commands. If we want the variable to be available to the second script then we need to export the variable.

**script1.sh**
```bash
#!/bin/bash
# demonstrate variable scope 1.
var1=blah
var2=foo
# Let's verify their current value
echo $0 :: var1 : $var1, var2 : $var2
export var1
./script2.sh
# Let's see what they are now
echo $0 :: var1 : $var1, var2 : $var2
```

**script2.sh**
```bash
#!/bin/bash
# demonstrate variable scope 2
# Let's verify their current value
echo $0 :: var1 : $var1, var2 : $var2
# Let's change their values
var1=flop
var2=bleh
```

The output is as expected.
- script2 could not access var2 because it was not exported, but it could print out the value of var1
- when script2 completed, and control went back to script1, then newly assigned values went away (somewhat like a function call).


```
script1.sh :: var1 : blah, var2 : foo
script2.sh :: var1 : blah, var2 :
script1.sh :: var1 : blah, var2 : foo
```

Exporting variables is a one way process. The original process may pass variables over to the new process but anything that process does with the copy of the variables has no impact on the original variables.

Exporting variables is something you probably won't need to worry about for most Bash scripts you'll create. But it does help you break
larger problems into smaller pieces. You could think of the `export` command as passing parameters to a function. Whatever you pass to 
the function you can see/print/manipulate but when the function ends, so does the scope, and those changes go away. (Unless the variable is passed by
reference, yes I know.)

## Summary

- `$0` : Name of the script running
- `$1, $2, ...`: Command line arguments
- `variable=value`: To set a value for a variable. Remember, no spaces on either side of `=`
- `Quotes " '`: Double will do variable substitution, single will not.
- `variable=$( command )`: Save the output of a command into a variable
- `export var1`: Make the variable var1 available to child processes.

========================================================================================

# Bash Scripting: Input

## Introduction

- We looked at one form of user input (command line arguments) in the previous section. 
- Now we would like to introduce other ways the user may provide input to the Bash script. 


## Ask the User for Input

If we would like to ask the user for input then we use a command called read. This command takes the input and will save it into a variable.


- `read var1` 


Let's look at a simple example:

**introduction.sh**

```
#!/bin/bash
# Ask the user for their name

echo Hello, who am I talking to?

read varname

echo It\'s nice to meet you $varname
```

- **Line 4** - Print a message asking the user for input.
- **Line 6** - Run the command read and save the users response into the variable varname
- **Line 8** - echo another message just to verify the read command worked. Note: I had to put a backslash ( \ ) in front of the ' so that it was escaped.

## More with Read

You are able to alter the behavior of `read` with a variety of command line options. (See the man page for read to see all of them.) Two commonly used options however are `-p` which allows you to specify a prompt and -s which makes the input silent. This can make it easy to ask for a username and password combination like the example below:

**login.sh**
```bash
#!/bin/bash
# Ask the user for login details

read -p 'Username: ' uservar
read -sp 'Password: ' passvar

echo

echo Thankyou $uservar we now have your login details
```

- Notice the "space" at the end of each prompt. 
- This is for readability.


## More variables

So far we have looked at a single word as input. We can do more than that however.

**cars.sh**
```bash
#!/bin/bash
# Demonstrate how read actually works
echo What cars do you like?

read car1 car2 car3

echo Your first car was: $car1
echo Your second car was: $car2
echo Your third car was: $car3
```


The general mechanism is that you can supply several variable names to `read`. `Read` will then take your input and split it on whitespace. The first item will then be assigned to the first variable name, the second item to the second variable name and so on. If there are more items than variable names then the remaining items will all be added to the last variable name. If there are less items than variable names then the remaining variable names will be set to blank or null.

## Reading from STDIN

It's common in Linux to pipe a series of simple, single purpose commands together to create a larger solution tailored to our exact needs. The ability to do this is one of the real strengths of Linux. It turns out that we can easily accommodate this mechanism with our scripts also. By doing so we can create scripts that act as filters to modify data in specific ways for us.

Bash accommodates piping and redirection by way of special files. Each process gets it's own set of files (one for STDIN, STDOUT and STDERR respectively) and they are linked when piping or redirection is invoked. Each process gets the following files:

- **STDIN** - /proc/<processID>/fd/0
- **STDOUT** - /proc/<processID>/fd/1
- **STDERR** - /proc/<processID>/fd/2

To make life more convenient the system creates some shortcuts for us:

- **STDIN** - /dev/stdin or /proc/self/fd/0
- **STDOUT** - /dev/stdout or /proc/self/fd/1
- **STDERR** - /dev/stderr or /proc/self/fd/2

**fd** in the paths above stands for `file descriptor`.

So if we would like to make our script able to process data that is piped to it all we need to do is read the relevant file. All of the files mentioned above behave like normal files.


```
#!/bin/bash
# A basic summary of my sales report

echo Here is a summary of the sales data:
echo ====================================
echo
cat /dev/stdin | cut -d' ' -f 2,3 | sort
```

- Print a title for the output
- `cat` the file representing STDIN `|`  cut setting the delimiter to a space, fields 2 and 3 `|` sort the output.
- Assume you have a file like below named `salesdata.txt`:

```
Fred apples 20 January 4
Susy oranges 5 January 7
Mark watermelons 12 January 10
Terry peaches 7 January 15
```

The command: `cat salesdata.txt | ./summary` would print the following:

```
Here is a summary of the sales data:
====================================
apples 20
oranges 5
peaches 7
watermelons 12
```

## So which should I use?

So we now have 3 methods for getting input from the user:

1. Command line arguments
2. Read input during script execution
3. Accept data that has been redirected into the Bash script via STDIN

Which method is best depends on the situation.

- You should normally favor command line arguments wherever possible. They are the most convenient for users as the data will be stored in their command history so they can easily return to it. 
- It is also the best approach if your script may be called by other scripts or processes (eg. maybe you want it to run periodically using CRON).

Sometimes the nature of the data is such that it would not be ideal for it to be stored in peoples command histories etc. A good example of this is login credentials (username and password). In these circumstances it is best to read the data during script execution.

If all the script is doing is processing data in a certain way then it is probably best to work with STDIN. This way it can easily be added into a pipeline.

Sometimes you may find that a combination is ideal. The user may supply a filename as a command line argument and if not then the script will process what it finds on STDIN (when we look at If statements we'll see how this may be achieved). Or maybe command line arguments define certain behavior but read is also used to ask for more information if required.

Ultimately you should think about 3 factors when deciding how users will supply data to your Bash script:

- **Ease of use** - Which of these methods will make it easiest for users to use my script?
- **Security** - Is there sensitive data which I should handle appropriately?
- **Robustness** - Can I make it so that my scripts operation is intuitive and flexible and also make it harder to make simple mistakes?

## Summary
- **read varName**: Read input from the user and store it in the variable varName.
- **/dev/stdin**: A file you can read to get the STDIN for the Bash script
- **Usability**: Your choice of input methods will have an impact on how useable your script is.


===================================================================================================================

# Bash Scripting: Arithmetic

## Introduction
 
There are several ways to go about arithmetic in Bash scripting. All will be covered for completeness but the recommended approach is arithmetic expansion (covered last).

## Let

`let` is a builtin function of Bash that allows us to do simple arithmetic. It follows the basic format:


- `let <arithmetic expression>`


The left hand side is typically a variable, but not always.

Let's look at a simple example:

**let_example.sh**

```bash
#!/bin/bash
# Basic arithmetic using let

let a=5+4
echo $a # 9

let "a = 5 + 4"
echo $a # 9

let a++
echo $a # 10

let "a = 4 * 5"
echo $a # 20

let "a = $1 + 30"
echo $a # 30 + first command line argument
```

- **Line 4** - This is the basic format. Note that if we don't put quotes around the expression then it must be written with no spaces.
- **Line 7** - This time we have used quotes which allow us to space out the expression to make it more readable.
- **Line 10** - This is a shorthand for increment the value of the variable a by 1. It is the same as writing `a = a + 1`.
- **Line 16** - We may also include other variables in the expression.


Here is a table with some of the basic expressions:


|Operator      |   	Operation   |
|:------------:|:----------------:|
|+, -, /*, /	 | addition, subtraction, multiply, divide|
|var++	        | Increase the variable var by 1         |
|var--	        | Decrease the variable var by 1         |
|%	            | Modulus (Return the remainder after division)|


## Expr

`expr` is similar to `let` except instead of saving the result to a variable it instead prints the answer. Unlike `let` you don't need to enclose the expression in quotes. You also must have spaces between the items of the expression. It is also common to use `expr` within command substitution to save the output to a variable.

```
expr item1 operator item2
```

Let's look at a simple example:

**expr_example.sh**

```bash
#!/bin/bash
# Basic arithmetic using expr

expr 5 + 4

expr "5 + 4"

expr 5+4

expr 5 \* $1

expr 11 % 2

a=$( expr 10 - 3 )

echo $a # 7
```

- **Line 4** - This is the basic format. Note that there must be spaces between the items and no quotes.
- **Line 6** - If we do put quotes around the expression then the expression will not be evaluated but printed instead.
- **Line 8** - If we do not put spaces between the items of the expression then the expression will not be evaluated but printed instead.
- **Line 10** - Some characters have a special meaning to Bash so we must escape them (put a backslash in front of) to remove their special meaning.
- **Line 12** - Here we demonstrate the operator modulus. The modulus is the remainder when the first item is divided by the second item.
- **Line 14** - This time we're using expr within command substitution in order to save the result to the variable a.

## Double Parentheses

In the section on Variables we saw that we could save the output of a command easily to a variable. It turns out that this mechanism is also able to do basic arithmetic for us if we tweak the syntax a little. We do so by using double brackets like so:

- `$(( expression ))`

Here's an example to illustrate:

expansion_example.sh

```bash
#!/bin/bash
# Basic arithmetic using double parentheses

a=$(( 4 + 5 ))
echo $a # 9

a=$((3+5))
echo $a # 8

b=$(( a + 3 ))
echo $b # 11

b=$(( $a + 4 ))
echo $b # 12

(( b++ ))
echo $b # 13

(( b += 3 ))
echo $b # 16

a=$(( 4 * 5 ))
echo $a # 20
```

- **Line 4** - This is the basic format. As you can see we may space it out nicely for readability without the need for quotes.
- **Line 7** - As you can see, it works just the same if we take spacing out.
- **Line 10** - We may include variables without the preceding $ sign.
- **Line 13** - Variables can be included with the `$` sign if you prefer.
- **Line 16** - This is a slightly different form. Here the value of the variable b is incremented by 1. When we do this we don't need the `$` sign preceding the brackets.
- **Line 19** - This is a slightly different form of the previous example. Here the value of the variable b is incremented by 3. It is a shorthand for b = b + 3.
- **Line 19** - Unlike other methods, when we do multiplication we don't need to escape the * sign.

So as you can see double parenthese is quite flexible in how you format it's expression. This is part of why we prefer this method. As double parentheses are builtin to Bash it also runs slighly more efficiently (though to be honest, with the raw computing power of machines these days the difference in performance is really insignificant).

## Length of a Variable

This isn't really arithmetic but it can be quite useful. If you want to find out the length of a variable (how many characters) you can do the following:

- `${#variable}`


Here's an example:

**length_example.sh**

```bash
#!/bin/bash
# Show the length of a variable.

a='Hello World'
echo ${#a} # 11

b=4953
echo ${#b} # 4
```

## Summary

- `let expression`: Make a variable equal to an expression.
- `expr expression`: print out the result of the expression.
- `$(( expression ))`: Return the result of the expression.
- `${#var}`: Return the length of the variable var.

--

- **Arithmetic**: There are several ways in which to do arithmetic in Bash scripts. Double parentheses is the preferred method.
- **Formatting**: When doing arithmetic, the presence or absence of spaces (and quotes) is often important.


===================================================================================================================

# Bash Scripting: If Statements

## Introduction

- `If` statements and `case` statements work as in most programming languages. They let you control the flow of your program.
- Their syntax is very specific so stay on top of all the little details.

## Basic If Statements

A basic if statement effectively says, if a particular test is true, then perform a given set of actions. If it is not true then don't perform those actions. If follows the format below:

```
if [ <some test> ]
then
<commands>
fi
```

Anything between `then` and `fi` (if backwards) will be executed only if the test (between the square brackets) is true.

Let's look at a simple example:

**if_example.sh**

```sh
#!/bin/bash
# Basic if statement

if [ $1 -gt 100 ]
then
    echo Hey thats a large number.
    pwd
fi
date
```

- **Line 4** - Let's see if the first command line argument is greater than 100
- **Line 6 and 7** - Will only get run if the test on line 4 returns true. You can have as many commands here as you like.
- **Line 8** - fi signals the end of the if statement. All commands after this will be run as normal.
- **Line 10** - Because this command is outside the if statement it will be run regardless of the outcome of the if statement.


## Test

The square brackets ( `[ ]` ) in the if statement above are actually a reference to the command `test`. This means that all of the operators that `test` allows may be used here as well. Look up the man page for test to see all of the possible operators (there are quite a few) but some of the more common ones are listed below.


|Operator	            |  Description                               |
|---------------------:|:-------------------------------------------|
| ! EXPRESSION	         |  The EXPRESSION is false.      |
| -n STRING	   |  The length of STRING is greater than zero.  |
| -z STRING	   |  The lengh of STRING is zero (ie it is empty).  |
| STRING1 = STRING2   |  	STRING1 is equal to STRING2  |
| STRING1 != STRING2   |  	STRING1 is not equal to STRING2  |
| INTEGER1 -eq INTEGER2	   |  INTEGER1 is numerically equal to INTEGER2  |
| INTEGER1 -gt INTEGER2	   |  INTEGER1 is numerically greater than INTEGER2  |
| INTEGER1 -lt INTEGER2   |  	INTEGER1 is numerically less than INTEGER2  |
| -d FILE   |  	FILE exists and is a directory.  |
| -e FILE   |  	FILE exists.  |
| -r FILE   |  	FILE exists and the read permission is granted.  |
| -s FILE	   |  FILE exists and it's size is greater than zero (ie. it is not empty).  |
| -w FILE   |  	FILE exists and the write permission is granted.  |
| -x FILE   |  	FILE exists and the execute permission is granted.  |


A few points to note:

- `=` is slightly different to -eq. 
    - `=` does a string comparison
    - `-eq` does a numerical comparison
- `[ 001 = 1 ]` (will return false)
- `[ 001 -eq 1 ]` (will return true)

- When we refer to FILE above we are actually meaning a path. Remember that a path may be absolute or relative and may refer to a file or a directory.
- Because `[ ]` is just a reference to the command `test` we may experiment and trouble shoot with `test` on the command line to make sure our understanding of its behavior is correct.

```bash
~$ test 001 = 1
~$ echo $?
1
~$ test 001 -eq 1
~$ echo $?
0
~$ touch myfile
~$ test -s myfile
~$ echo $?
1
~$ ls /etc > myfile
~$ test -s myfile
~$ echo $?
0
```

- **Line 1** - Perform a string based comparison. Test doesn't print the rusult so instead we check it's exit status which is what we will do on the next line.
- **Line 2** - The variable $? holds the exit status of the previously run command (in this case test). 0 means TRUE (or success). 1 = FALSE (or failure).
- **Line 4** - This time we are performing a numerical comparison.
- **Line 7** - Create a new blank file myfile (assuming that myfile doesn't already exist).
- **Line 8**- Is the size of myfile greater than zero?
- **Line 11** - Redirect some content into myfile so it's size is greater than zero.
- **Line 12** - Test the size of myfile again. This time it is TRUE.

## Indenting

You'll notice that in the if statement above we indented the commands that were run if the statement was true. This is referred to as indenting and is an important part of writing good, clean code (in any language, not just Bash scripts). The aim is to improve readability and make it harder for us to make simple, silly mistakes. There aren't any rules regarding indenting in Bash so you may indent or not indent however you like and your scripts will still run exactly the same. I would highly recommend you do indent your code however (especially as your scripts get larger) otherwise you will find it increasingly difficult to see the structure in your scripts.

## Nested If statements

Talking of indenting. Here's a perfect example of when it makes life easier for you. You may have as many if statements as necessary inside your script. It is also possible to have an if statement inside of another if statement. For example, we may want to analyze a number given on the command line like so:

**nested_if.sh**

```bash
#!/bin/bash
# Nested if statements

if [ $1 -gt 100 ]
then
    echo Hey that's a large number.
    
    if (( $1 % 2 == 0 ))
    then
        echo And is also an even number.
    fi
fi
```

- **Line 4** - Perform the following, only if the first command line argument is greater than 100.
- **Line 8** - This is a light variation on the if statement. If we would like to check an expression then we may use the double brackets just like we did for variables.
- **Line 10** - Only gets run if both if statements are true.


## If Else

Sometimes we want to perform a certain set of actions if a statement is true, and another set of actions if it is false. We can accommodate this with the else mechanism.

```
if [ <some test> ]
then
    <commands>
else
    <other commands>
fi
```

Now we could easily read from a file if it is supplied as a command line argument, else read from STDIN.

**else.sh**

```bash
#!/bin/bash
# else example

if [ $# -eq 1 ]
then
    nl $1
else
    nl /dev/stdin
fi
```

## If Elif Else

Sometimes we may have a series of conditions that may lead to different paths.

```
if [ <some test> ]
then
    <commands>
elif [ <some test> ] 
then
    <different commands>
else
    <other commands>
fi
```

For example it may be the case that if you are 18 or over you may go to the party. If you aren't but you have a letter from your parents you may go but must be back before midnight. Otherwise you cannot go.

**if_elif.sh**

```bash
#!/bin/bash
# elif statements

if [ $1 -ge 18 ]
then
    echo You may go to the party.
elif [ $2 == 'yes' ]
then
    echo You may go to the party but be back before midnight.
else
    echo You may not go to the party.
fi
```

You can have as many elif branches as you like. The final else is also optional.

## Boolean Operations

Sometimes we only want to do something if multiple conditions are met. Other times we would like to perform the action if one of several condition is met. We can accommodate these with boolean operators.

- `and` - `&&`
- `or` - `||`

For instance maybe we only want to perform an operation if the file is readable and has a size greater than zero.

**and.sh**

```bash
#!/bin/bash
# and example

if [ -r $1 ] && [ -s $1 ]
then
    echo This file is useful.
fi
```

Maybe we would like to perform something slightly different if the user is either bob or andy.

**or.sh**

```bash
#!/bin/bash
# or example 

if [ $USER == 'bob' ] || [ $USER == 'andy' ]
then
    ls -alh
else
    ls
fi
```


## Case Statements

Sometimes we may wish to take different paths based upon a variable matching a series of patterns. We could use a series of if and elif statements but that would soon grow to be unweildly. Fortunately there is a case statement which can make things cleaner. It's a little hard to explain so here are some examples to illustrate:

```
case <variable> in
<pattern 1>)
    <commands>
;;
<pattern 2>)
    <other commands>
;;
esac
```

Here is a basic example:

**case.sh**

```bash
#!/bin/bash
# case example

case $1 in
start)
    echo starting
;;
stop)
    echo stoping
;;
restart)
    echo restarting
;;
*)
    echo don\'t know
;;
esac
```

- **Line 4** - This line begins the casemechanism.
- **Line 5** - If $1 is equal to 'start' then perform the subsequent actions. the ) signifies the end of the pattern.
- **Line 7** - We identify the end of this set of statements with a double semi-colon ( ;; ). Following this is the next case to consider.
- **Line 14** - Remember that the test for each case is a pattern. The * represents any number of any character. It is essentialy a catch all if for if none of the other cases match. It is not necessary but is often used.
- **Line 17** - esac is case backwards and indicates we are at the end of the case statement. Any other statements after this will be executed normally.

Now let's look at a slightly more complex example where patterns are used a bit more.

**disk_useage.sh**

```bash
#!/bin/bash
# Print a message about disk useage.

space_free=$( df -h | awk '{ print $5 }' | sort -n | tail -n 1 | sed 's/%//' )
case $space_free in
[1-5]*)
    echo Plenty of disk space available
;;
[6-7]*)
    echo There could be a problem in the near future
;;
8*)
    echo Maybe we should look at clearing out old files
;;
9*)
    echo We could have a serious problem on our hands soon
;;
*)
    echo Something is not quite right here
;;
esac
```

## Summary

- `if`: Perform a set of commands if a test is true.
- `else`: If the test is not true then perform a different set of commands.
- `elif`: If the previous test returned false then try this one.
- `&&`: Perform the and operation.
- `||`: Perform the or operation.
- `case`: Choose a set of commands to execute depending on a string matching a particular pattern.

--

- **Indentation**: Indenting makes your code much easier to read. It get's increasingly important as your Bash scripts get longer.



===================================================================================================================

# Bash Scripting: Loops

## Introduction

 
Bash loops are very useful. In this section of our Bash Scripting Tutorial we'll look at the different loop formats available to us as well as discuss when and why you may want to use each of them.

Loops allow us to take a series of commands and keep re-running them until a particular situation is reached. They are useful for automating repetitive tasks.

There are 3 basic loop structures in Bash scripting which we'll look at below. There are also a few statements which we can use to control the loops operation.

## While Loops

One of the easiest loops to work with is while loops. They say, while an expression is true, keep executing these lines of code. They have the following format:

```
while [ <some test> ]
do
    <commands>
done
```

You'll notice that similar to if statements the test is placed between square brackets `[ ]`.

While loop diagram
In the example below we will print the numbers 1 through to 10:

**while_loop.sh**
```bash
#!/bin/bash
# Basic while loop

counter=1
while [ $counter -le 10 ]
do
    echo $counter
    ((counter++))
done

echo All done
```

- **Line 4** - We'll initialize the variable counter with it's starting value.
- **Line 5** - While the test is true (counter is less than or equal to 10) let's do the following commands.
- **Line 7** - We can place any commands here we like. Here echo is being used as it's an easy way to illustrate what is going on.
- **Line 8** - Using the double brackets we can increase the value of counter by 1.
- **Line 9** - We're at the bottom of the loop so go back to line 5 and perform the test again. If the test is true then execute the commands. If the test is false then continue executing any commands following done.


**Tip**
>A common mistake is what's called an off by one error. In the example above we could have put `-lt` as opposed to `-le` (less than as opposed to less than or equal). Had we done this it would have printed up until 9. These mistakes are easy to make but also easy to fix once you've identified it so don't worry too much if you make this error.

## Until Loops

The until loop is fairly similar to the while loop. The difference is that it will execute the commands within it until the test becomes true.

```
until [ <some test> ]
do
    <commands>
done
```

**until_loop.sh**

```bash
#!/bin/bash
# Basic until loop

counter=1
until [ $counter -gt 10 ]
do
   echo $counter
   ((counter++))
done

echo All done
```

As you can see in the example above, the syntax is almost exactly the same as the while loop (just replace while with until). We can also create a script that does exactly the same as the while example above just by changing the test accordingly.


## For Loops

The for loop is a little bit different to the previous two loops. What it does is say for each of the items in a given list, perform the given set of commands. It has the following syntax.

```
for var in <list>
do
    <commands>
done
```

The for loop will take each item in the list (in order, one after the other), assign that item as the value of the variable var, execute the commands between do and done then go back to the top, grab the next item in the list and repeat over.

The list is defined as a series of strings, separated by spaces.

Here is a simple example to illustrate:

**for_loop.sh**
```bash
#!/bin/bash
# Basic for loop

names='Stan Kyle Cartman'

for name in $names
do
    echo $name
done

echo All done
```

- **Line 4** - Create a simple list which is a series of names.
- **Line 6** - For each of the items in the list $names assign the item to the variable $name and do the following commands.
- **Line 8** - echo the name to the screen just to show that the mechanism works. We can have as many commands here as we like.
- **Line 11** - echo another command to show that the bash script continued execution as normal after all the items in the list were processed.


## Ranges

We can also process a series of numbers

**for\_loop_series.sh**

```bash
#!/bin/bash
# Basic range in for loop

for value in {1..5}
do
    echo $value
done
echo All done
```

- **Line 4** - It's important when specifying a range like this that there are no spaces present between the curly brackts { }. If there are then it will not be seen as a range but as a list of items.

```

When specifying a range you may specify any number you like for both the starting value and ending value. The first first value may also be larger than the second in which case it will count down.

It is also possible to specify a value to increase or decrease by each time. You do this by adding another two dots ( .. ) and the value to step by.

**for\_loop_stepping.sh**

```bash
#!/bin/bash
# Basic range with steps for loop

for value in {10..0..2}
do
    echo $value
done
echo All done
```


One of the more useful applications of for loops is in the processing of a set of files. To do this we may use wildcards. Let's say we want to convert a series of .html files over to .php files.

**convert\_html\_to_php.sh**

```bash
#!/bin/bash
# Make a php copy of any html files

for value in $1/*.html
do
    cp $value $1/$( basename -s .html $value ).php
done
```

## Controlling Loops: Break and Continue

Most of the time your loops are going to through in a smooth and ordely manner. Sometimes however we may need to intervene and alter their running slightly. There are two statements we may issue to do this.

#### Break

The `break` statement tells Bash to leave the loop straight away. It may be that there is a normal situation that should cause the loop to end but there are also exceptional situations in which it should end as well. For instance, maybe we are copying files but if the free disk space get's below a certain level we should stop copying.

**copy_files.sh**

```bash
#!/bin/bash
# Make a backup set of files

for value in $1/*
do
    used=$( df $1 | tail -1 | awk '{ print $5 }' | sed 's/%//' )
    if [ $used -gt 90 ]
    then
        echo Low disk space 1>&2
        break
    fi
    cp $value $1/backup/
done
```

#### Continue

The `continue` statement tells Bash to stop running through this iteration of the loop and begin the next iteration. Sometimes there are circumstances that that stop us from going any further. For instance, maybe we are using the loop to process a series of files but if we happen upon a file which we don't have the read permission for we should not try to process it.

**copy_check.sh**

```bash
#!/bin/bash
# Make a backup set of files

for value in $1/*
do
    if [ ! -r $value ]
    then
        echo $value not readable 1>&2
        continue
    fi
    cp $value $1/backup/
done
```

## Select

The select mechanism allows you to create a simple menu system. It has the following format:

```
select var in <list>
do
    <commands>
done
```

When invoked it will take all the items in list (similar to other loops this is a space separated set of items) and present them on the screen with a number before each item. A prompt will be printed after this allowing the user to select a number. When they select a number and hit enter the corresponding item will be assigned to the variable var and the commands between do and done are run. Once finished a prompt will be displayed again so the user may select another option.

A few points to note:

- No error checking is done. If the user enters something other than a number or a number not corresponding to an item then var becomes null (empty)
- If the user hits enter without entering any data then the list of options will be displayed again.
- The loop will end when an EOF signal is entered or the break statement is issued.
- You may change the system variable PS3 to change the prompt that is displayed.

Here is a simple example to illustrate it's usage:

**select_example.sh**

```
#!/bin/bash
# A simple menu system

names='Kyle Cartman Stan Quit'

PS3='Select character: '

select name in $names
do
    if [ $name == 'Quit' ]
    then
        break
    fi
    echo Hello $name
done

echo Bye
```

- **Line 4** - Set up a variable with the list of characters and a last option which we may select to quit. Note that the items are separated by a space.
- **Line 6** - Change the value of the system variable PS3 so that the prompt is set to something a little more descriptive. (By default it is #?)
- **Lines 10** - 13 - If the last option, 'Quit', is selected then break out of the select loop.
- **Line 14** - Print out a message just to demonstrate the mechanism has worked. You may have as many commands here as you like.
- **Line 17** - Print a message just to show that the script has continued as normal after the select loop.


## Summary

- `while do done`: Perform a set of commands while a test is true.
- `until do done`: Perform a set of commands until a test is true.
- `for do done`: Perform a set of commands for each item in a list.
- `break`: Exit the currently running loop.
- `continue`: Stop this iteration of the loop and begin the next iteration.
- `select do done`: Display a simple menu system for selecting items from a list.


===================================================================================================================

Source: http://ryanstutorials.net/bash-scripting-tutorial/
