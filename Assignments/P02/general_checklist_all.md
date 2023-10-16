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
|   1.1   | `assignments` folder exists in Repo                                                                    |    ▢    |        |
|   1.2   | `P02` folder exists in `assignments` with appropriate README.md                                        |    ▢    |        |
|         | along with all of the python code.                                                                     |         |        |
| ***2*** | ***General Code and Comments***                                                                        | **25**  |        |
|   2.1   | README.md file exists and describes everything as instructed per [this](../../Resources/03-Readmees/). |    ▢    |        |
|   2.2   | There is a main comment block at the top of every code file.                                           |    ▢    |        |
|   2.3   | Each function has an appropriate comment block.                                                        |    ▢    |        |
|         |                                                                                                        |         |        |
| ***3*** | ***Classes***                                                                                          | **25**  |        |
|   3.1   | Code was written with an attempt at:                                                                   |    ▢    |        |
|         | **--->** Organization (functions and classes)                                                          |    ▢    |        |
|         | **--->** Readability (appropriate naming conventions for readability)                                  |    ▢    |        |
|         | **--->** Modular design that doesn't tightly couple DB with Filesystem                                 |    ▢    |        |
|         | **--->** Main class maintained current FS state (cwd), and current user at a minimum                   |    ▢    |        |
|         |                                                                                                        |         |        |
| ***4*** | ***Sql Db***                                                                                           | **25**  |        |
|   4.1   | Table Columns use correct data type                                                                    |    ▢    |        |
|   4.2   | Table gets updated appropriately for each command                                                      |    ▢    |        |
|   4.3   | Each command has a sql statement associated with it                                                    |    ▢    |        |
|         |                                                                                                        |         |        |
|         |                                                                                                        |         |        |
| ***5*** | ***Checklist***                                                                                        | **100** |        |
|   5.1   | The command checklist below was followed                                                               |    ▢    |        |
|         |                                                                                                        |         |        |
| ***6*** | ***General***                                                                                          |         |        |
|         | Prompt line acts correct (cleans command etc.)                                                         |    ▢    |        |
|         | Arrow keys work                                                                                        |    ▢    |        |
|         | Items were not printed to the screen unnecessarily                                                     |    ▢    |        |
|         | Too many messages (like successful .....) weren't used                                                 |    ▢    |        |
|         | Program did not crash or need restarted                                                                |    ▢    |        |
|         | **Total:**                                                                                             | **200** |        |


## Command Checklist
|    #    | Item                                             | Value | Earned |
| :-----: | ------------------------------------------------ | :---: | :----: |
| ***1*** | ***Commands***                                   |       |        |
|    1    | *ls -lah*                                        |   ▢   |        |
|    2    | *mkdir bananas*                                  |   ▢   |        |
|    3    | *cd bananas*                                     |   ▢   |        |
|    4    | *cd ..*                                          |   ▢   |        |
|    5    | *cd ~*                                           |   ▢   |        |
|    6    | *pwd*                                            |   ▢   |        |
|    7    | *mv somefile.txt bananas*                        |   ▢   |        |
|    8    | *cp bananas/somefile.txt somefile/otherfile.txt* |   ▢   |        |
|    9    | *rm -rf bananas*                                 |   ▢   |        |
|   10    | *cat somefile*                                   |   ▢   |        |
|   11    | *less somefile*                                  |   ▢   |        |
|   12    | *head somefile -n 10*                            |   ▢   |        |
|   13    | *tail somefile -n 10*                            |   ▢   |        |
|   14    | *grep -l bacon bacon.txt*                        |   ▢   |        |
|   15    | *wc -w bacon.txt*                                |   ▢   |        |
|   16    | *history*                                        |   ▢   |        |
|   17    | *!x*                                             |   ▢   |        |
|   18    | *chmod 777 somefile.txt*                         |   ▢   |        |
|   19    | *sort bacon.txt*                                 |   ▢   |        |
|   20    | *Command of your choice*                         |   ▢   |        |
| ***2*** | ***Piping***                                     |       |        |
|         | Similar to (but open for me to choose command):  |       |        |
|         | *grep bacon bacon.txt \| wc -l*                  |   ▢   |        |
| ***3*** | ***Redirection***                                |       |        |
|         | Similar to (but open for me to choose):          |       |        |
|         | *cat file1 file2 > file0*                        |   ▢   |        |


