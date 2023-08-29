# 5143 - Operating Systems

### Roster

<img src="https://images2.imgbox.com/35/7c/I0dU5rrM_o.png" width="20"> [Class Roster Section 101 (TTh)](https://docs.google.com/spreadsheets/d/1BQd54B5ROkXxd0QA9keMOFl5iev9BVzYPaPTdKIwZ4s/edit?usp=sharing)

<img src="https://images2.imgbox.com/35/7c/I0dU5rrM_o.png" width="20"> [Class Roster Section 102 (MW)](https://docs.google.com/spreadsheets/d/1fj4kxRc3PV5O_S3b6NjwIHQuC8tHzCN1370h5aI-MeE/edit?usp=sharing)




### General Course Info
- __Days:__ 
  - Section 101: TR 0200pm 0320pm
  - Section 102: MW 0500pm 0620pm 
- __Location:__ [BO 320](https://goo.gl/maps/19yTKot4pnxjgYqr9)
- [__Semester:__](https://msutexas.edu/registrar/_assets/files/pdfs/acadcal2324.pdf) Monday August 28<sup>th</sup> - Friday December 8<sup>th</sup>
- [__Holidays:__](https://msutexas.edu/registrar/_assets/files/pdfs/acadcal2324.pdf)
  - __Labor Day__ Monday September 4<sup>th</sup>
  - __Thanksgiving:__  November 22<sup>nd</sup> - Friday November 24<sup>th</sup> 
- [__Last Day for “W”:__](https://msutexas.edu/registrar/_assets/files/pdfs/acadcal2324.pdf)  Friday October 30<sup>th</sup>
- [__Last Day of Class:__](https://msutexas.edu/registrar/_assets/files/pdfs/acadcal2324.pdf) Friday December 8<sup>th</sup>
- [__Final Exam:__](https://msutexas.edu/registrar/_assets/files/pdfs/finalexamschedulespringfall2023.pdf)
  - Section 101: Thursday December 14<sup>th</sup> @ 1:00pm - 3:00pm in BO 320
  - Section 102: Monday December 11<sup>th</sup> @ 3:30pm - 5:30pm in BO 320


### Resources

Here is an open source book for the course. I hope you guys appreciate the amount of effort it takes to put material together and then put it on the internet for free.

- [Operating Systems: Three Easy Pieces](https://pages.cs.wisc.edu/~remzi/OSTEP/)
  - Thanks To: [Remzi H. Arpaci-Dusseau and Andrea C. Arpaci-Dusseau (University of Wisconsin-Madison)](http://people.scs.carleton.ca/~michiel/)
  - [Local Copy](Resources/01-Books/Operating_Systems-Three_Easy_Pieces.pdf)

### Assumed

- This course assumes you can program at level after completing CMPS 1063 which includes:
  - pointers
  - recursion
  - basic data structures
  - basic oop concepts 
- I make this course more project based so you must have a basic ability to program 


#### Topics List

- [ ] OOP Concepts for Project
- [ ] Processes
    - [ ] Concurrency
    - [ ] Synchronization
    - [ ] Semaphores
    - [ ] Deadlock
- [ ] Memory Management
    - [ ] Paging
    - [ ] Segmentation
    - [ ] Virtual Memory
- [ ] CPU Scheduling Algorithms
    - [ ] Uniprocessor
    - [ ] Multiprocessor & Multicore
- [ ] I/O & Disk Scheduling
    - [ ] Devices
    - [ ] Buffering
    - [ ] RAID
    - [ ] Disk Cache
- [ ] File Management

## Projects

- [ ] Implement a Shell (C++ or Python)
- [ ] Threading
  - [ ] C++ (posix threads)
  - [ ] Python chat client
- [ ] Student lead projects:
  - [ ] Virtual Memory 
  - [ ] Cache Memory
  - [ ] CPU Scheduling
  - [ ] File System simulation
  

## Grading

| Categories            |       |  \|   | Grade |          |
| :-------------------- | :---: | :---: | :---: | :------: |
| Midterm               |  20%  |  \|   |   A   |  89-100  |
| Projects              |  45%  |  \|   |   B   |  79-88   |
| Presentations         |  15%  |  \|   |   C   |  69-78   |
| Final<sup>**1**</sup> |  20%  |  \|   |   D   |  59-68   |
|                       |       |  \|   |   F   | below 59 |
>**1**. Plane ticket prices, events like weddings, or trips out of the country are not valid excuses for missing the final exam at its scheduled time. I will not make accommodations for anything other than an issue vetted by the dean of students. 

### Projects

- Projects will be written in C++ and Python depending on the project. 
- I don't teach the traditional OS course using slides and a linear progression through a text book. Instead I try to create projects that require a basic understanding of the underlying concept in order to implement the project. 
- Each project must run without error (some exceptions allowed). If they do not run, they will not be graded. Correctness is a different matter. 
- The majority of each project will be graded by the class and myself during your class presentation. I will review code and other components separately.
- Some projects can be done in groups. I will dictate the max size of each group. If I dictate a max size of 3, don't ask for 4. If you are that worried about a friend, then make 2 groups of 2. 
- Occasionally some students prefer to work alone. And although this was my preferred method in grad school, I may insist that you join a group. 
- Each group member will also fill out a performance evaluation on their team members. Sadly there are occasions when a group member does nothing. I want to give you the tools to let me know.
- Please read the *Academic Misconduct Policy & Procedures* below. Different cultures and countries have differing opinions on what constitutes academic dishonesty. To avoid any confusion, we will be abiding by MSU's policy on academic dishonesty and plagiarism. 

### Presentations

- Presentations are a major component of graduate work. The ability to discuss complex topics in front a group of your peers is an important skill to have. 
- Every project, group or individual, will be accompanied with a presentation.
- The quality of your presentation is somewhat based on the quality of your project. A poor project makes it hard to give a proper presentation if much of the expected functionality was not included in said project. Basically you don't have much to discuss. On the flip side, an excellent project doesn't ensure a great presentation either. So preparation is key, and I am ALWAYS available for help with presentations.
- I will give specific requirements for each presentation since each project may vary greatly. One project may simulate scheduling algorithms and will have results, whereas a shell project simply needs a walk-through showing commands, examples of piping, and redirection.  
- In general presentations in my course should follow a basic outline:
  - Project description (if necessary)
  - A logical progression of your steps in implementing the project. Make sure to include:
    - Pitfalls (any confusing components that gave problems)
    - Highlights (any good solutions or components you are proud of)
  - Discuss Results
  - OR
  - Show features
- Be prepared! Sometimes showing your project seems easy since you spent many hours writing it and have a very deep understanding of it. Using a shell as an example, practicing which commands you will use to show all features of a shell will definitely make for a better presentation. You can also hide small flaws with a well thought out presentation. 
- I am also much less inclined to ask pointed questions if you have a well thought out and thorough presentation.


## Academic Misconduct Policy & Procedures

Cheating, collusion, and plagiarism (the act of using source material of other persons, either published or unpublished, without following the accepted techniques of crediting, or the submission for credit of work not the individual’s to whom credit is given . The Department of Computer Science has adopted the following policy related to cheating (academic misconduct).  The policy will be applied to all instances of cheating on assignments and exams as determined by the instructor of the course.  (See below for link to MSU definitions.)

- 1<sup>st</sup> instance of cheating in a course on an individual assignment: The student will be assigned a non-replaceable grade of zero for the assignment, project or exam.  If the resulting grade does not result in a letter grade reduction, the student will receive a one letter grade reduction in course.
- 2<sup>nd</sup> instance of cheating in a course on an individual assignment: The student will receive a grade of F in course & immediately be removed from course.
- 1<sup>st</sup> instance of cheating in a course on a group assignment or major course project: The student will receive a grade of F in course & immediately be removed from course.
- All instances of cheating will be reported to the Department Chair and, in the case of graduate students, to the Department Graduate Coordinator.
  
>Note: Letting a student look at your work is collusion and is academic misconduct!
 
>See Also:   MSU Student Handbook: Appendix E: [Academic Misconduct Policy & Procedures](https://msutexas.edu/student-life/_assets/files/handbook.pdf).

