import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
SCREEN_TITLE = "Scheduler Queue Visualization"


class Process:
    """Simple wrapper for a process text and motion control."""

    def __init__(self, pid, start_x, start_y, target_x, color):
        self.text = arcade.Text(pid, start_x, start_y, color, 24, bold=True)
        self.target_x = target_x
        self.speed = 2
        self.active = False  # will only move when activated

    def update(self):
        if self.active and self.text.x < self.target_x:
            self.text.x += self.speed

    def draw(self):
        self.text.draw()


class SchedulerDemo(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.BLACK)

        # Queues
        self.ready_label = "Ready Queue"
        self.cpu_label = "CPU Queue"

        # Create processes with different start times
        self.processes = [
            Process("P1", 100, 220, 600, arcade.color.YELLOW),
            Process("P2", 100, 180, 600, arcade.color.CYAN),
            Process("P3", 100, 140, 600, arcade.color.LIGHT_GREEN),
        ]

        # Frame counter to stagger starts
        self.frame_count = 0

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(self.ready_label, 50, 300, arcade.color.GRAY, 14)
        arcade.draw_text(self.cpu_label, 550, 300, arcade.color.GRAY, 14)

        for p in self.processes:
            p.draw()

    def on_update(self, delta_time):
        self.frame_count += 1

        # Activate processes one after another every ~90 frames (~1.5 seconds)
        for i, p in enumerate(self.processes):
            if self.frame_count > i * 90:
                p.active = True
            p.update()


def main():
    SchedulerDemo()
    arcade.run()


if __name__ == "__main__":
    main()
