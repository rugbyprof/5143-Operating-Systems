Ok, let's use sfml with c++ and try and calculate the best font size, rectangle size, and a minimal amount of repositioning. The problem boils down to:

### background

Using C++ with SFML, I would like to draw a queue like data structure horizontally or vertically showing all of the items currently in the queue. What ever item is in the queue, it will have to determine how itself prints. Below I will list the requirements of what I would like to acheive.

1. The following should be configurable in a json file or similar:

   - **Padding and Spacing**

     - `window_margins`: spacing from edge of window to all contents
     - `margins`: spacing between elements (e.g. items in the queue, or between two queues)
     - `border`: applied to any element that allows a border (size and color)
     - `padding`: if margins are spacing between elements, padding is spacing within an element from contents to edges.

   - **Font**
     - (str) font name,
     - (str) path
     - (rgb tuple) color
     - (int) initial_font_size
   - rectangle
     - (rgb tuple) color
     - (int) border_size (zero = no border)
     - (rgb tuple) border color
   - orientation
     - horizontal
     - vertical external
   - container (visual aid for queue)
     - (bool) show_container
     - (rgb tuple) fill_color
     - (int) border_size (zero = no border)
     - (rgb tuple) border color

Getting the screen size



- Assume an unkown number of key:val pair sets need printed inside a rectangular shape, that is dynamically sized for the best fit of the data. Based on previous discussions, I'm sure you realize this is me helping students print their queues in an organized and readible fashion.
- What is known is: 
  - Screen width and height (get it from sfml)
  - Direction user wants the key:value pair sets to be printed (horizontal or vertical)
  - User can pass in a `target` number of items to print knowing this may be adjusted for convenience by the method.
  - Font path and preferred font size.
  


Given a set of key : value pairs to be printed in the same container shape in any organized configuration (1 pair per row, 2 pairs per row, etc.) I would like a method to calculate a rectangles with and height based on the data to be printed and the following constraints (or requests):
- The width and height of the window.
- Horizontal or Vertical (the direction in which the data items would be printed)
- The target number of 

Can you write a function or a class in c++ that will calculate a rectangle width and height given a set of key value pairs to print along with some padding and margin information? In addition, one would inform the function of the direction (horizontal or vertical) of the items to print, and also a target number of items to show on the screen. 