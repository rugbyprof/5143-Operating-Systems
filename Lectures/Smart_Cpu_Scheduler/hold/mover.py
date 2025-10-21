import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
SCREEN_TITLE = "Scheduler Text Object Example"

class SchedulerDemo(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.BLACK)

        # Create text object for process
        self.process_text = arcade.Text("P1", 100, 200, arcade.color.YELLOW, 24)

        # Movement parameters
        self.target_x = 600
        self.speed = 2

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Ready Queue", 50, 300, arcade.color.GRAY, 14)
        arcade.draw_text("CPU Queue", 550, 300, arcade.color.GRAY, 14)

        self.process_text.draw()

    def on_update(self, delta_time):
        if self.process_text.x < self.target_x:
            self.process_text.x += self.speed

def main():
    SchedulerDemo()
    arcade.run()

if __name__ == "__main__":
    main()