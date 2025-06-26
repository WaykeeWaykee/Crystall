import pygame
import sys
import random

# Инициализация Pygame
pygame.init()

# Настройки экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Crystal Runner")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (100, 100, 100)

# Виртуальные кнопки (для телефона)
button_left = pygame.Rect(50, SCREEN_HEIGHT - 100, 60, 60)
button_right = pygame.Rect(120, SCREEN_HEIGHT - 100, 60, 60)
button_jump = pygame.Rect(SCREEN_WIDTH - 120, SCREEN_HEIGHT - 100, 60, 60)

# Игрок
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (100, SCREEN_HEIGHT - 100)
        self.speed = 5
        self.jump_power = 12
        self.velocity_y = 0
        self.on_ground = False

    def update(self, touches):
        # Гравитация
        self.velocity_y += 0.5
        self.rect.y += self.velocity_y

        # Ограничение по земле
        if self.rect.bottom >= SCREEN_HEIGHT - 50:
            self.rect.bottom = SCREEN_HEIGHT - 50
            self.velocity_y = 0
            self.on_ground = True

        # Управление (кнопки или касания)
        move_left = False
        move_right = False
        jump = False

        for touch in touches:
            if button_left.collidepoint(touch):
                move_left = True
            elif button_right.collidepoint(touch):
                move_right = True
            elif button_jump.collidepoint(touch):
                jump = True

        # Движение
        if move_left:
            self.rect.x -= self.speed
        if move_right:
            self.rect.x += self.speed
        if jump and self.on_ground:
            self.velocity_y = -self.jump_power
            self.on_ground = False

# Кристаллы
class Crystal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

# Ловушки (шипы)
class Trap(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 20))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

# Монстры
class Monster(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 2

    def update(self, player):
        # Движение к игроку
        if self.rect.x < player.rect.x:
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed

        if self.rect.y < player.rect.y:
            self.rect.y += self.speed
        else:
            self.rect.y -= self.speed

# Дверь для перехода на след. уровень
class Door(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 80))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

# Платформы
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(GRAY)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

# Уровни
def create_level(level):
    platforms = pygame.sprite.Group()
    crystals = pygame.sprite.Group()
    traps = pygame.sprite.Group()
    monsters = pygame.sprite.Group()
    door = None

    if level == 1:
        # Платформы
        platforms.add(Platform(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))
        platforms.add(Platform(200, 400, 200, 20))
        platforms.add(Platform(500, 300, 200, 20))

        # Кристаллы
        crystals.add(Crystal(300, 370))
        crystals.add(Crystal(600, 270))

        # Ловушки
        traps.add(Trap(400, SCREEN_HEIGHT - 70))
        traps.add(Trap(700, 280))

        # Монстры
        monsters.add(Monster(400, 200))

        # Дверь
        door = Door(700, SCREEN_HEIGHT - 130)

    elif level == 2:
        # Платформы
        platforms.add(Platform(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))
        platforms.add(Platform(100, 450, 150, 20))
        platforms.add(Platform(300, 350, 150, 20))
        platforms.add(Platform(550, 250, 150, 20))

        # Кристаллы
        crystals.add(Crystal(150, 420))
        crystals.add(Crystal(350, 320))
        crystals.add(Crystal(600, 220))

        # Ловушки
        traps.add(Trap(250, SCREEN_HEIGHT - 70))
        traps.add(Trap(450, 230))

        # Монстры
        monsters.add(Monster(200, 300))
        monsters.add(Monster(500, 200))

        # Дверь
        door = Door(650, SCREEN_HEIGHT - 130)

    return platforms, crystals, traps, monsters, door

# Отрисовка кнопок
def draw_buttons():
    pygame.draw.rect(screen, GRAY, button_left)
    pygame.draw.rect(screen, GRAY, button_right)
    pygame.draw.rect(screen, GRAY, button_jump)
    
    font = pygame.font.SysFont(None, 30)
    left_text = font.render("←", True, WHITE)
    right_text = font.render("→", True, WHITE)
    jump_text = font.render("↑", True, WHITE)
    
    screen.blit(left_text, (button_left.x + 20, button_left.y + 15))
    screen.blit(right_text, (button_right.x + 20, button_right.y + 15))
    screen.blit(jump_text, (button_jump.x + 20, button_jump.y + 15))

# Основная игра
def main():
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    player = Player()
    current_level = 1
    platforms, crystals, traps, monsters, door = create_level(current_level)

    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    all_sprites.add(platforms)
    all_sprites.add(crystals)
    all_sprites.add(traps)
    all_sprites.add(monsters)
    if door:
        all_sprites.add(door)

    score = 0
    game_over = False
    level_complete = False

    running = True
    while running:
        screen.fill(BLACK)
        
        touches = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                touches.append(event.pos)
        
        if not game_over and not level_complete:
            player.update(touches)
            
            # Проверка столкновений с кристаллами
            crystal_hits = pygame.sprite.spritecollide(player, crystals, True)
            for _ in crystal_hits:
                score += 10

            # Проверка столкновений с ловушками и монстрами
            if (pygame.sprite.spritecollide(player, traps, False) or
                pygame.sprite.spritecollide(player, monsters, False)):
                game_over = True

            # Проверка перехода на след. уровень
            if door and pygame.sprite.collide_rect(player, door) and len(crystals) == 0:
                current_level += 1
                if current_level > 2:
                    level_complete = True
                else:
                    platforms, crystals, traps, monsters, door = create_level(current_level)
                    all_sprites = pygame.sprite.Group()
                    all_sprites.add(player)
                    all_sprites.add(platforms)
                    all_sprites.add(crystals)
                    all_sprites.add(traps)
                    all_sprites.add(monsters)
                    if door:
                        all_sprites.add(door)

            # Обновление монстров
            for monster in monsters:
                monster.update(player)

        # Отрисовка
        all_sprites.draw(screen)
        draw_buttons()

        # Текст
        score_text = font.render(f"Score: {score}", True, WHITE)
        level_text = font.render(f"Level: {current_level}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (10, 50))

        if game_over:
            game_over_text = font.render("GAME OVER! Press R to restart", True, RED)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                main()

        if level_complete:
            win_text = font.render("YOU WIN! Press R to restart", True, GREEN)
            screen.blit(win_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                main()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()