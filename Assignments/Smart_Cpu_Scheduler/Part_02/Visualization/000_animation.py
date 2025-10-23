import pygame
import sys

# --- Initialize Pygame ---
pygame.init()

# --- Screen setup ---
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TextSprite Fly-In Example")

# --- Colors ---
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0, 100)
RED = (255, 0, 0, 100)
GREEN = (0, 255, 0, 100)
BLUE = (0, 0, 255, 100)

# --- Font setup ---
FONT = pygame.font.SysFont("Arial", 24)


# =========================================================
# VisualQueue Class
# (screen, (255, 255, 0), (100, 200, 120, 60), 0)
# =========================================================
class VisualQueue(pygame.sprite.Sprite):
    def __init__(self, color, pos_size):
        super().__init__()
        self.rect = pygame.Rect(color, pos_size)

    def update(self):
        """Move horizontally toward the target X position."""
        pass


# =========================================================
# TextSprite Class
# =========================================================
class TextSprite(pygame.sprite.Sprite):
    def __init__(self, text, color, start_pos, target_pos, speed=5):
        super().__init__()
        self.image = FONT.render(text, True, color)
        self.rect = self.image.get_rect(topleft=start_pos)
        self.target_x, self.target_y = target_pos
        self.speed = speed

    def update(self):
        """Move horizontally toward the target X position."""
        if self.rect.x < self.target_x:
            self.rect.x += self.speed
            if self.rect.x > self.target_x:
                self.rect.x = self.target_x  # stop exactly at target


# =========================================================
# Main Setup
# =========================================================
def main():
    clock = pygame.time.Clock()
    running = True

    # Create a single "P1" sprite
    p1 = TextSprite(
        text="P1",
        color=YELLOW,
        start_pos=(-100, 120),  # start offscreen to the left
        target_pos=(60, 120),  # stop here
        speed=5,
    )

    # Define queue rectangles
    ready_box = pygame.Rect(50, 100, 300, 50)
    running_box = pygame.Rect(50, 160, 300, 50)
    waiting_box = pygame.Rect(50, 220, 300, 50)

    # queues = [
    #     VisualQueue(RED, ready_box),
    #     VisualQueue(GREEN, running_box),
    #     VisualQueue(BLUE, waiting_box),
    # ]

    # Define sprite groups
    ready_queue = pygame.sprite.Group()
    running_queue = pygame.sprite.Group()
    waiting_queue = pygame.sprite.Group()

    # Group makes updating/drawing multiple sprites easy
    sprites = pygame.sprite.Group(p1)

    # Main loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # --- Update ---
        sprites.update()

        # --- Draw ---
        screen.fill(BLACK)
        sprites.draw(screen)
        pygame.draw.rect(screen, RED, ready_box, 2)
        pygame.draw.rect(screen, GREEN, running_box, 2)
        pygame.draw.rect(screen, BLUE, waiting_box, 2)

        ready_queue.draw(screen)
        running_queue.draw(screen)
        waiting_queue.draw(screen)
        pygame.display.flip()

        # --- Frame rate ---
        clock.tick(60)

    pygame.quit()
    sys.exit()


# =========================================================
# Entry point
# =========================================================
if __name__ == "__main__":
    main()
