# =========================================================
# main.py
# =========================================================
# Wires together the scheduler and view, runs Arcade.
# =========================================================

import arcade
from scheduler import Scheduler
from Assignments.Smart_Cpu_Scheduler.hold.schedulerView import SchedulerView
from controller import Controller


def main():
    window = arcade.Window(800, 400, "Scheduler Visualization")
    scheduler = Scheduler()
    view = SchedulerView(scheduler)
    controller = Controller(scheduler)

    window.show_view(view)

    # Hook the controller’s update loop into Arcade’s event system
    def update(delta_time):
        controller.update(delta_time)

    arcade.schedule(update, 1 / 60)

    arcade.run()


if __name__ == "__main__":
    main()
