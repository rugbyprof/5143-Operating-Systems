# =========================================================
# main.py – Glue between scheduler and visualizer
# =========================================================
import pygame
import time
from scheduler import Scheduler, Job
from visualizer import Visualizer


def main():
    # -------------------------------
    # 1. Create mock jobs
    jobs = [Job(i, [5]) for i in range(1, 6)]
    scheduler = Scheduler(jobs)
    visualizer = Visualizer(scheduler)

    # -------------------------------
    # 2. Main loop: step scheduler + draw
    running = True
    while running and scheduler.has_jobs():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        scheduler.step()  # advance logic
        visualizer.update_from_scheduler()  # sync display
        visualizer.draw()  # draw new frame
        time.sleep(0.5)  # slow down to see it happen

    # -------------------------------
    # Cleanup
    time.sleep(1)
    pygame.quit()


if __name__ == "__main__":
    main()
