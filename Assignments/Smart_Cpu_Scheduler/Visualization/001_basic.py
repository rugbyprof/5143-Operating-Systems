import pygame
import sys

# =========================================================
# --- CONFIG ---
# =========================================================
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BG_COLOR = (25, 25, 25)
TEXT_COLOR = (255, 255, 0)
BOX_COLOR = (200, 200, 200)

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

        # Rendered text (ex: "P1")
        self.text_surface = FONT.render(f"P{self.id}", True, TEXT_COLOR)
        self.image = self.text_surface
        self.rect = self.image.get_rect()

    def draw(self, surface, x, y):
        surface.blit(self.text_surface, (x, y))


# =========================================================
# --- QUEUE SPRITE ---
# =========================================================
class QueueSprite(pygame.sprite.Sprite):
    """A visual queue container for Jobs (draws horizontally)."""

    def __init__(self, name, x, y, width, height, max_size=None):
        super().__init__()
        self.name = name
        self.rect = pygame.Rect(x, y, width, height)
        self.jobs = []
        self.max_size = max_size  # None = unbounded

    def enqueue(self, job):
        if self.max_size is None or len(self.jobs) < self.max_size:
            self.jobs.append(job)

    def dequeue(self):
        if self.jobs:
            return self.jobs.pop(0)

    def draw(self, surface):
        """Draw the queue rectangle, name, and jobs."""
        # Draw rectangle outline
        pygame.draw.rect(surface, BOX_COLOR, self.rect, width=2)

        # Draw name label
        label = FONT.render(self.name.upper(), True, BOX_COLOR)
        surface.blit(label, (self.rect.x + 5, self.rect.y + 5))

        # Draw jobs left-to-right inside the queue
        offset_x = 10
        for i, job in enumerate(self.jobs):
            job_x = self.rect.x + offset_x + i * 40  # horizontal spacing
            job_y = self.rect.y + self.rect.height // 2 - 10
            job.draw(surface, job_x, job_y)


# =========================================================
# --- MAIN WINDOW ---
# =========================================================
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Scheduler Queues – Step 1 (Horizontal)")

    clock = pygame.time.Clock()
    running = True

    # Layout positions (stack vertically, but jobs grow horizontally)
    box_w, box_h = 300, 100
    x = 20
    spacing = 20

    ready_q = QueueSprite("ready", x, 20, box_w, box_h)
    wait_q = QueueSprite("wait", x, 20 + (box_h + spacing), box_w, box_h)
    cpu_q = QueueSprite("cpu", x, 20 + 2 * (box_h + spacing), box_w, box_h, max_size=2)
    io_q = QueueSprite("io", x, 20 + 3 * (box_h + spacing), box_w, box_h, max_size=2)

    # Sample jobs
    for i in range(1, 5):
        ready_q.enqueue(Job(i))
    wait_q.enqueue(Job(5))
    wait_q.enqueue(Job(6))
    cpu_q.enqueue(Job(7))
    io_q.enqueue(Job(8))

    queues = [ready_q, wait_q, cpu_q, io_q]

    # --- Main loop ---
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BG_COLOR)

        # Draw each queue
        for q in queues:
            q.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
