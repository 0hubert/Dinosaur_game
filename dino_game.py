import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
GROUND_Y = SCREEN_HEIGHT - 100
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)

# Game variables
GRAVITY = 0.8
JUMP_SPEED = -16
GAME_SPEED = 5

class Dinosaur:
    def __init__(self):
        self.x = 50
        self.y = GROUND_Y
        self.width = 50
        self.height = 60
        self.vel_y = 0
        self.jumping = False
    
    def jump(self):
        if not self.jumping:
            self.vel_y = JUMP_SPEED
            self.jumping = True
    
    def update(self):
        # Apply gravity
        self.vel_y += GRAVITY
        self.y += self.vel_y
        
        # Ground collision
        if self.y > GROUND_Y:
            self.y = GROUND_Y
            self.vel_y = 0
            self.jumping = False
    
    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, (self.x, self.y - self.height, self.width, self.height))
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y - self.height, self.width, self.height)

class Cactus:
    def __init__(self, x):
        self.x = x
        self.y = GROUND_Y
        self.width = 30
        self.height = random.randint(40, 70)
    
    def update(self, speed):
        self.x -= speed
    
    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, (self.x, self.y - self.height, self.width, self.height))
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y - self.height, self.width, self.height)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Dinosaur Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        
        self.reset_game()
    
    def reset_game(self):
        self.dino = Dinosaur()
        self.cacti = []
        self.score = 0
        self.game_speed = GAME_SPEED
        self.game_over = False
        self.high_score = self.load_high_score()
    
    def load_high_score(self):
        try:
            with open("high_score.txt", "r") as f:
                return int(f.read())
        except:
            return 0
    
    def save_high_score(self):
        with open("high_score.txt", "w") as f:
            f.write(str(self.high_score))
    
    def spawn_cactus(self):
        if len(self.cacti) == 0 or self.cacti[-1].x < SCREEN_WIDTH - 300:
            self.cacti.append(Cactus(SCREEN_WIDTH))
    
    def update(self):
        if not self.game_over:
            # Update dinosaur
            self.dino.update()
            
            # Update cacti
            for cactus in self.cacti:
                cactus.update(self.game_speed)
            
            # Remove off-screen cacti
            self.cacti = [c for c in self.cacti if c.x > -50]
            
            # Spawn new cacti
            self.spawn_cactus()
            
            # Check collisions
            dino_rect = self.dino.get_rect()
            for cactus in self.cacti:
                if dino_rect.colliderect(cactus.get_rect()):
                    self.game_over = True
                    if self.score > self.high_score:
                        self.high_score = self.score
                        self.save_high_score()
            
            # Update score and speed
            self.score += 1
            if self.score % 500 == 0:
                self.game_speed += 0.5
    
    def draw(self):
        # Clear screen
        self.screen.fill(WHITE)
        
        # Draw ground
        pygame.draw.line(self.screen, BLACK, (0, GROUND_Y), (SCREEN_WIDTH, GROUND_Y), 2)
        
        # Draw game objects
        self.dino.draw(self.screen)
        for cactus in self.cacti:
            cactus.draw(self.screen)
        
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        self.screen.blit(score_text, (20, 20))
        
        high_score_text = self.font.render(f"High Score: {self.high_score}", True, BLACK)
        self.screen.blit(high_score_text, (20, 60))
        
        if self.game_over:
            game_over_text = self.font.render("Game Over! Press R to restart", True, BLACK)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
            self.screen.blit(game_over_text, text_rect)
        
        # Update display
        pygame.display.flip()
    
    def run(self):
        running = True
        while running:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_SPACE, pygame.K_UP):
                        self.dino.jump()
                    elif event.key == pygame.K_r and self.game_over:
                        self.reset_game()
            
            # Game logic
            self.update()
            
            # Drawing
            self.draw()
            
            # Cap the frame rate
            self.clock.tick(FPS)
        
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run() 