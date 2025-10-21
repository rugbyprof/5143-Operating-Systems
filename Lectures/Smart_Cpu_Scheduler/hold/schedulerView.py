"""
Starting Template

Once you have learned how to use classes, you can begin your program with this
template.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.starting_template
"""

import arcade

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Starting Template"
DEFAULT_LINE_HEIGHT = 45
DEFAULT_FONT_SIZE = 20

# Load fonts bundled with Arcade such as the Kenney fonts
arcade.resources.load_kenney_fonts()
arcade.resources.load_liberation_fonts()


# =========================================================
# view.py
# =========================================================
# Visual layer for the scheduler, built with Arcade.
# It observes the scheduler and renders process states.
# =========================================================

import arcade


class SchedulerView(arcade.View):
    def __init__(self, scheduler):
        super().__init__()
        self.scheduler = scheduler
        self.visuals = {}
        self.positions = {
            "new": (100, 300),
            "ready": (250, 300),
            "running": (400, 300),
            "waiting": (550, 300),
            "terminated": (700, 300),
        }

        # Color coding per state
        self.colors = {
            "new": arcade.color.WHITE,
            "ready": arcade.color.YELLOW,
            "running": arcade.color.CYAN,
            "waiting": arcade.color.LIGHT_GREEN,
            "terminated": arcade.color.RED,
        }

        # Create a text visual for each process
        for pid in self.scheduler.processes():
            start_x, start_y = self.positions["new"]
            self.visuals[pid] = arcade.Text(
                pid,
                start_x,
                start_y - (30 * int(pid[1:])),
                self.colors["new"],
                20,
                bold=True,
            )

        # Register callback from scheduler
        self.scheduler.on_state_change(self.handle_state_update)

    # -------------------------------------
    # Scheduler callback
    # -------------------------------------
    def handle_state_update(self, pid, new_state):
        """Handle a process changing states."""
        visual = self.visuals[pid]
        visual.color = self.colors[new_state]

    # -------------------------------------
    # Arcade lifecycle
    # -------------------------------------
    def on_draw(self):
        arcade.start_render()

        # Draw state labels
        for state, (x, y) in self.positions.items():
            arcade.draw_text(state.upper(), x, y + 40, arcade.color.GRAY, 14)

        # Draw process visuals
        for text in self.visuals.values():
            text.draw()

    def on_update(self, delta_time):
        """Smoothly move text toward target positions based on current state."""
        for pid, process in self.scheduler.processes().items():
            visual = self.visuals[pid]
            target_x, target_y = self.positions[process.state]
            # Ease toward target
            visual.x += (target_x - visual.x) * 0.1
            visual.y += (target_y - visual.y) * 0.1


# class SchedulerView(arcade.View):
#     """
#     Main application class.

#     NOTE: Go ahead and delete the methods you don't need.
#     If you do need a method, delete the 'pass' and replace it
#     with your own code. Don't leave 'pass' in this program.
#     """

#     def __init__(self, scheduler=None):
#         super().__init__()

#         self.color = arcade.color.ALMOND
#         self.background_color = arcade.color.WHITE
#         self.scheduler = scheduler

#         # If you have sprite lists, you should create them here,
#         # and set them to None

#     def get_jobs(self, jobs):
#         pass

#     def reset(self):
#         """Reset the game to the initial state."""
#         # Do changes needed to restart the game here if you want to support that
#         pass

#     def on_draw(self):
#         """
#         Render the screen.
#         """

#         # This command should happen before we start drawing. It will clear
#         # the screen to the background color, and erase what we drew last frame.
#         self.clear()
#         arcade.draw_text("draw_rect", 243, 3, arcade.color.BLACK, 10)
#         arcade.draw_rect_outline(
#             arcade.rect.XYWH(295, 100, 45, 65), arcade.color.BRITISH_RACING_GREEN
#         )
#         self.title.draw()

#         # Call draw() on all your sprite lists below

#     def on_update(self, delta_time):
#         """
#         All the logic to move, and the game logic goes here.
#         Normally, you'll call update() on the sprite lists that
#         need it.
#         """

#     def on_key_press(self, key, key_modifiers):
#         """
#         Called whenever a key on the keyboard is pressed.

#         For a full list of keys, see:
#         https://api.arcade.academy/en/latest/arcade.key.html
#         """
#         pass

#     def on_key_release(self, key, key_modifiers):
#         """
#         Called whenever the user lets off a previously pressed key.
#         """
#         pass

#     def on_mouse_motion(self, x, y, delta_x, delta_y):
#         """
#         Called whenever the mouse moves.
#         """
#         pass

#     def on_mouse_press(self, x, y, button, key_modifiers):
#         """
#         Called when the user presses a mouse button.
#         """
#         pass

#     def on_mouse_release(self, x, y, button, key_modifiers):
#         """
#         Called when a user releases a mouse button.
#         """
#         pass


# def main():
#     """Main function"""
#     # Create a window class. This is what actually shows up on screen
#     window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

#     # Create and setup the GameView
#     game = SchedulerView()

#     # Show GameView on screen
#     window.show_view(game)

#     # Start the arcade game loop
#     arcade.run()


# if __name__ == "__main__":
#     main()
