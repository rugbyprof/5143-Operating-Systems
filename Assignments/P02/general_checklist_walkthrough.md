## File System Assignment General Checklist for a Walkthrough

## Name: _______________________________________

## Name: _______________________________________

## Name: _______________________________________

|    #    | Item                                                                                                   |  Value  | Earned |
| :-----: | ------------------------------------------------------------------------------------------------------ | :-----: | :----: |
|         | ***Pre-Cursors***                                                                                      |         |        |
|   0.1   | Repository was NOT uploaded on time.                                                                   | **-25** |        |
|   0.2   | Provided code does NOT run.                                                                            | **-50** |        |
| ***1*** | ***General***                                                                                          | **25**  |        |
|   1.1   | `assignments` folder exists in Repo                                                                    |         |        |
|   1.2   | `P02` folder exists in `assignments` with appropriate README.md                                        |         |        |
|         | along with all of the python code.                                                                     |         |        |
|         |                                                                                                        |         |        |
| ***2*** | ***General Code and Comments***                                                                        | **25**  |        |
|   2.1   | README.md file exists and describes everything as instructed per [this](../../Resources/03-Readmees/). |         |        |
|   2.2   | There is a main comment block at the top of every code file.                                           |         |        |
|   2.3   | Each function has an appropriate comment block.                                                        |         |        |
|         |                                                                                                        |         |        |
| ***3*** | ***Classes***                                                                                          | **25**  |        |
|   3.1   | Code was written with an attempt at:                                                                   |         |        |
|         | **--->** Organization (functions and classes)                                                          |         |        |
|         | **--->** Readability (appropriate naming conventions for readability)                                  |         |        |
|         | **--->** Modular design that doesn't tightly couple DB with Filesystem                                 |         |        |
|         | **--->** Main class maintained current FS state (cwd), and current user at a minimum                   |         |        |
|         |                                                                                                        |         |        |
| ***4*** | ***Sql Db***                                                                                           | **25**  |        |
|   4.1   | Table Columns use correct data type                                                                    |         |        |
|   4.2   | Table gets updated appropriately for each command                                                      |         |        |
|   4.3   | Each command has a sql statement associated with it                                                    |         |        |
|         |                                                                                                        |         |        |
|         |                                                                                                        |         |        |
| ***5*** | ***Checklist***                                                                                        | **50**  |        |
|   5.1   | The command checklist below was followed                                                               |         |        |
|         |                                                                                                        |         |        |
| ***6*** | ***General Walkthrough***                                                                              | **50**  |        |
|   6.1   | The walkthrough was either executed step by step with something like hitting enter again and again.    |         |        |
|   6.2   | The walkthrough was automated, but slowed down enough to follow.                                       |         |        |
|   6.3   | The commands were clear and easy to read.                                                              |         |        |
|   6.4   | The outputs were clear and easy to read.                                                               |         |        |
|   6.5   | The change in the database were clear and easy to find.                                                |         |        |
|   6.6   | Program did not crash.                                                                                 |         |        |
|   6.6   | Showed snapshots of the database or at least long listings between commands to see changes.            |         |        |
|         | **Total:**                                                                                             | **200** |        |



## Command Checklist

Run variations of the commands below, but this is not an exhaustive list. You should show the same type of commands but add parameters and flags in order to show a full working set. 

|   #   | Item                                           | Value | Earned |
| :---: | ---------------------------------------------- | :---: | :----: |
|   1   | ls -lah                                        |   ▢   |        |
|   2   | mkdir bananas                                  |   ▢   |        |
|   3   | cd bananas                                     |   ▢   |        |
|   4   | cd ..                                          |   ▢   |        |
|   5   | pwd                                            |   ▢   |        |
|   6   | mv somefile.txt bananas                        |   ▢   |        |
|   7   | cp bananas/somefile.txt somefile/otherfile.txt |   ▢   |        |
|   8   | rm -rf bananas                                 |   ▢   |        |
|   9   | history                                        |   ▢   |        |
|  10   | chmod 777 somefile.txt                         |   ▢   |        |