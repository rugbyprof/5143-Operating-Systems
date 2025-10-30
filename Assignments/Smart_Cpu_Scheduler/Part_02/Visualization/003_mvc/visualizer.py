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

    def __init__(self, name, x, y, width, height, color=BOX_COLOR, max_size=None):
        self.name = name
        self.rect = pygame.Rect(x, y, width, height)
        self.jobs = []
        self.max_size = max_size
        self.color = color

    def set_jobs(self, job_ids):
        """Replace current job display with IDs from scheduler."""
        self.jobs = job_ids

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, width=1)
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
        self.last_snapshot = None
        self.snap = None
        self.current_clock = 0

        # Layout (stacked vertically)
        w, h, x, spacing = 300, 75, 100, 50
        self.ready_q = QueueSprite("ready", x, 20, w, h, (0, 255, 0))
        self.wait_q = QueueSprite("wait", x, 20 + (h + spacing), w, h, (0, 255, 255))
        self.wait_q = QueueSprite("wait", x, 20 + (h + spacing), w, h, (0, 0, 255))
        self.cpu_q = QueueSprite(
            "cpu", x, 20 + 2 * (h + spacing), w, h, (255, 0, 255), max_size=2
        )
        self.io_q = QueueSprite(
            "io", x, 20 + 3 * (h + spacing), w, h, (200, 200, 200), max_size=2
        )
        self.queues = [self.ready_q, self.wait_q, self.cpu_q, self.io_q]

    # -----------------------------------------------------
    def update_from_scheduler(self):
        self.last_snapshot = self.snap
        self.snap = self.scheduler.snapshot()

        print(f"Last snapshot: {self.last_snapshot}")
        print(f"Current snapshot: {self.snap}")

        self.ready_q.set_jobs(self.snap["ready"])
        self.wait_q.set_jobs(self.snap["wait"])
        self.cpu_q.set_jobs(self.snap["cpu"])
        self.io_q.set_jobs(self.snap["io"])
        self.current_clock = self.snap["clock"]

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
