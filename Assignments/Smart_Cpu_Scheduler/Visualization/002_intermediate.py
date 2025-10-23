import pygame
import sys
import random

# =========================================================
# --- CONFIG ---
# =========================================================
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BG_COLOR = (25, 25, 25)
TEXT_COLOR = (255, 255, 0)
BOX_COLOR = (200, 200, 200)
FULL_COLOR = (255, 100, 100)  # highlight for full queues

pygame.init()
FONT = pygame.font.SysFont("Consolas", 20)


# =========================================================
# --- JOB SPRITE ---
# =========================================================
class Job(pygame.sprite.Sprite):
    def __init__(self, job_id, bursts=None, state="new"):
        super().__init__()
        self.id = job_id
        self.bursts = bursts or []
        self.state = state
        self.current_burst = 0
        self.text_surface = FONT.render(f"P{self.id}", True, TEXT_COLOR)
        self.image = self.text_surface
        self.rect = self.image.get_rect()

    def draw(self, surface, x, y):
        surface.blit(self.text_surface, (x, y))


# =========================================================
# --- QUEUE SPRITE ---
# =========================================================
class QueueSprite(pygame.sprite.Sprite):
    """Visual queue container for Jobs (horizontal layout)."""

    def __init__(self, name, x, y, width, height, max_size=None):
        super().__init__()
        self.name = name
        self.rect = pygame.Rect(x, y, width, height)
        self.jobs = []
        self.max_size = max_size  # None = unbounded

    # -------------------------------
    def enqueue(self, job):
        if self.max_size is None or len(self.jobs) < self.max_size:
            self.jobs.append(job)
        else:
            print(f"[!] {self.name} queue is full")

    def dequeue(self):
        if self.jobs:
            return self.jobs.pop(0)

    def is_full(self):
        return self.max_size is not None and len(self.jobs) >= self.max_size

    # -------------------------------
    def draw(self, surface):
        color = FULL_COLOR if self.is_full() else BOX_COLOR
        pygame.draw.rect(surface, color, self.rect, width=2)

        label = FONT.render(self.name.upper(), True, color)
        surface.blit(label, (self.rect.x + 5, self.rect.y + 5))

        # Draw jobs horizontally
        offset_x = 10
        for i, job in enumerate(self.jobs):
            job_x = self.rect.x + offset_x + i * 40
            job_y = self.rect.y + self.rect.height // 2 - 10
            job.draw(surface, job_x, job_y)


# =========================================================
# --- MAIN ---
# =========================================================
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Scheduler Queues – Step 2 (Interactive)")

    clock = pygame.time.Clock()
    running = True
    next_job_id = 1

    # Layout
    box_w, box_h = 300, 100
    x = 20
    spacing = 20

    ready_q = QueueSprite("ready", x, 20, box_w, box_h)
    wait_q = QueueSprite("wait", x, 20 + (box_h + spacing), box_w, box_h)
    cpu_q = QueueSprite("cpu", x, 20 + 2 * (box_h + spacing), box_w, box_h, max_size=2)
    io_q = QueueSprite("io", x, 20 + 3 * (box_h + spacing), box_w, box_h, max_size=2)

    queues = [ready_q, wait_q, cpu_q, io_q]

    # -----------------------------------------------------
    # Controls
    #   N : create a new job in Ready queue
    #   1 : move job from Ready -> CPU
    #   2 : move job from CPU -> Wait
    #   3 : move job from Wait -> IO
    #   4 : move job from IO -> Ready
    # -----------------------------------------------------
    print(
        """
Controls:
  N - Add new job to READY queue
  1 - Move READY → CPU
  2 - Move CPU → WAIT
  3 - Move WAIT → IO
  4 - Move IO → READY
  Q - Quit
"""
    )

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                key = event.key
                if key == pygame.K_q:
                    running = False

                elif key == pygame.K_n:
                    # Create and enqueue a new job
                    job = Job(next_job_id)
                    next_job_id += 1
                    ready_q.enqueue(job)

                elif key == pygame.K_1:  # READY → CPU
                    if ready_q.jobs and not cpu_q.is_full():
                        job = ready_q.dequeue()
                        cpu_q.enqueue(job)

                elif key == pygame.K_2:  # CPU → WAIT
                    if cpu_q.jobs:
                        job = cpu_q.dequeue()
                        wait_q.enqueue(job)

                elif key == pygame.K_3:  # WAIT → IO
                    if wait_q.jobs and not io_q.is_full():
                        job = wait_q.dequeue()
                        io_q.enqueue(job)

                elif key == pygame.K_4:  # IO → READY
                    if io_q.jobs:
                        job = io_q.dequeue()
                        ready_q.enqueue(job)

        # ----------------------------
        # Drawing
        # ----------------------------
        screen.fill(BG_COLOR)
        for q in queues:
            q.draw(screen)
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
