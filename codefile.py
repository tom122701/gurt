import pygame


# Initialize Pygame
pygame.init()

# Window setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Game with Enemy")

# Colors
WHITE = (255, 255, 255) 
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Clock and timer
clock = pygame.time.Clock()
time_limit = 30  # seconds

# Load images
try:
    lebron_img = pygame.image.load("lebron.png").convert_alpha()
    lebron_img = pygame.transform.scale(lebron_img, (60, 50))
except pygame.error:
    lebron_img = pygame.Surface((60, 50), pygame.SRCALPHA)
    lebron_img.fill(RED)

try:
    kawhi_img = pygame.image.load("yn.png").convert_alpha()
    kawhi_img = pygame.transform.scale(kawhi_img, (50, 50))
except pygame.error:
    kawhi_img = pygame.Surface((50, 50), pygame.SRCALPHA)
    kawhi_img.fill((0, 0, 255))

try:
    mj_img = pygame.image.load("lockedin.png").convert_alpha()
    mj_img = pygame.transform.scale(mj_img, (50, 50))
except pygame.error:
    mj_img = pygame.Surface((50, 50), pygame.SRCALPHA)
    mj_img.fill((0, 0, 255))
# Enemy class
class Enemy:
    def __init__(self, x, y, image, speed):
        self.rect = pygame.Rect(x, y, 50, 50)
        self.image = image
        self.speed = speed

    def move_towards(self, target):
        dx, dy = target.x - self.rect.x, target.y - self.rect.y
        dist = (dx ** 2 + dy ** 2) ** 0.5
        if dist > 0:
            self.rect.x += int(dx / dist * self.speed)
            self.rect.y += int(dy / dist * self.speed)

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

# Level setup
def setup_level(level):
    if level == 1:
        player = pygame.Rect(100, 100, 60, 50)
        treasure = pygame.Rect(700, 500, 30, 30)
        obstacles = [
            pygame.Rect(300, 250, 200, 20),
            pygame.Rect(150, 400, 300, 20),
            pygame.Rect(500, 150, 20, 200),
            pygame.Rect(400, 500, 200, 20),
            pygame.Rect(600, 300, 150, 20),
        ]
        enemy = Enemy(600, 100, kawhi_img, speed=3)
    elif level == 2:
        player = pygame.Rect(50, 50, 60, 50)
        treasure = pygame.Rect(700, 50, 30, 30)
        obstacles = [
            pygame.Rect(100, 150, 600, 20),
            pygame.Rect(100, 300, 600, 20),
            pygame.Rect(100, 450, 600, 20),
            pygame.Rect(350, 150, 20, 300),
            pygame.Rect(550, 300, 20, 150),
        ]
        enemy = Enemy(700, 500, mj_img, speed=5)
    return player, treasure, obstacles, enemy

# Game initialization
level = 1
player, treasure, obstacles, enemy = setup_level(level)
start_time = pygame.time.get_ticks()
running = True

# Game loop
while running:
    screen.fill(WHITE)
    current_time = (pygame.time.get_ticks() - start_time) // 1000
    if current_time >= time_limit:
        screen.fill(RED)
        font = pygame.font.Font(None, 60)
        text = font.render("you ran out of time", True, BLACK)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        pygame.display.update()
        pygame.time.delay(3000)
        break

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movement input
    keys = pygame.key.get_pressed()
    player_speed = 5
    if keys[pygame.K_a]:
        player.x -= player_speed
    if keys[pygame.K_d]:
        player.x += player_speed
    if keys[pygame.K_w]:
        player.y -= player_speed
    if keys[pygame.K_s]:
        player.y += player_speed

    # Boundary limits
    player.x = max(0, min(player.x, WIDTH - player.width))
    player.y = max(0, min(player.y, HEIGHT - player.height))

    # Collision with obstacles
    for obs in obstacles:
        if player.colliderect(obs):
            player.x, player.y = (100, 100) if level == 1 else (50, 50)
            break

    # Enemy chases player
    enemy.move_towards(player)

    # Enemy catches player
    if player.colliderect(enemy.rect):
        screen.fill(RED)
        font = pygame.font.Font(None, 48)
        text = font.render("unc js retire atp", True, BLACK)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
        pygame.display.update()
        pygame.time.delay(3000)
        break

    # Player reaches treasure
    if player.colliderect(treasure):
        if level == 1:
            # Level 2
            screen.fill(BLACK)
            font = pygame.font.Font(None, 60)
            text = font.render("Final boss", True, RED)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
            pygame.display.update()
            pygame.time.delay(2000)

            # Load level 2
            level = 2
            player, treasure, obstacles, enemy = setup_level(level)
            start_time = pygame.time.get_ticks()
            continue
        else:
            # Final win screen
            screen.fill(GREEN)
            font = pygame.font.Font(None, 60)
            text = font.render("you survived jordan", True, BLACK)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
            pygame.display.update()
            pygame.time.delay(3000)
            break

    # Draw game elements
    screen.blit(lebron_img, (player.x, player.y))
    pygame.draw.rect(screen, GREEN, treasure)
    for obs in obstacles:
        pygame.draw.rect(screen, BLACK, obs)
    enemy.draw(screen)

    # Draw timer
    font = pygame.font.Font(None, 36)
    timer_text = font.render(f"Time: {time_limit - current_time}", True, BLACK)
    screen.blit(timer_text, (10, 10))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
