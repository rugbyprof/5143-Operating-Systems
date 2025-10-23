# =========================================================
# visualizer.py – Pygame visualizer (no scheduling logic)
# =========================================================
import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BG_COLOR = (25, 25, 25)
BOX_COLOR = (200, 200, 200)
TEXT_COLOR = (255, 255, 0)

pygame.init()
FONT = pygame.font.SysFont("Consolas", 20)


class QueueSprite:
    """Visual representation of a single queue (horizontal layout)."""

    def __init__(self, name, x, y, width, height, max_size=None):
        self.name = name
        self.rect = pygame.Rect(x, y, width, height)
        self.jobs = []
        self.max_size = max_size

    def set_jobs(self, job_ids):
        """Replace current job display with IDs from scheduler."""
        self.jobs = job_ids

    def draw(self, surface):
        pygame.draw.rect(surface, BOX_COLOR, self.rect, width=2)
        label = FONT.render(self.name.upper(), True, BOX_COLOR)
        surface.blit(label, (self.rect.x + 5, self.rect.y + 5))
        for i, jid in enumerate(self.jobs):
            text = FONT.render(f"P{jid}", True, TEXT_COLOR)
            x = self.rect.x + 10 + i * 40
            y = self.rect.y + self.rect.height // 2 - 10
            surface.blit(text, (x, y))


class Visualizer:
    def __init__(self, scheduler):
        self.scheduler = scheduler
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Scheduler Visualizer")
        self.clock = pygame.time.Clock()

        # Layout (stacked vertically)
        w, h, x, spacing = 300, 100, 20, 20
        self.ready_q = QueueSprite("ready", x, 20, w, h)
        self.wait_q = QueueSprite("wait", x, 20 + (h + spacing), w, h)
        self.cpu_q = QueueSprite("cpu", x, 20 + 2 * (h + spacing), w, h, max_size=2)
        self.io_q = QueueSprite("io", x, 20 + 3 * (h + spacing), w, h, max_size=2)
        self.queues = [self.ready_q, self.wait_q, self.cpu_q, self.io_q]

    # -----------------------------------------------------
    def update_from_scheduler(self):
        snap = self.scheduler.snapshot()
        self.ready_q.set_jobs(snap["ready"])
        self.wait_q.set_jobs(snap["wait"])
        self.cpu_q.set_jobs(snap["cpu"])
        self.io_q.set_jobs(snap["io"])
        self.current_clock = snap["clock"]

    # -----------------------------------------------------
    def draw(self):
        self.screen.fill(BG_COLOR)
        for q in self.queues:
            q.draw(self.screen)
        # Draw clock
        clock_text = FONT.render(f"Clock: {self.current_clock}", True, TEXT_COLOR)
        self.screen.blit(clock_text, (600, 20))
        pygame.display.flip()
        self.clock.tick(30)  # limit to 30 FPS
