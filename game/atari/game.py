import pygame
import random
import math
import json
import os
from datetime import datetime

# Initialize Pygame
pygame.init()

# Game Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 30
        self.speed = 5
        self.health = 100
        self.max_health = 100
        self.bullet_level = 1
        self.last_shot = 0
        self.shoot_delay = 200  # milliseconds
        
    def move(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += self.speed
            
        # Keep player on screen
        self.x = max(0, min(SCREEN_WIDTH - self.width, self.x))
        self.y = max(0, min(SCREEN_HEIGHT - self.height, self.y))
    
    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.shoot_delay:
            self.last_shot = current_time
            return Bullet(self.x + self.width//2, self.y, -8, 'player')
        return None
    
    def draw(self, screen):
        # Draw spaceship as triangle
        points = [
            (self.x + self.width//2, self.y),
            (self.x, self.y + self.height),
            (self.x + self.width, self.y + self.height)
        ]
        pygame.draw.polygon(screen, CYAN, points)
        
        # Draw health bar
        health_width = 60
        health_height = 8
        health_x = self.x - 10
        health_y = self.y + self.height + 5
        
        pygame.draw.rect(screen, RED, (health_x, health_y, health_width, health_height))
        current_health_width = (self.health / self.max_health) * health_width
        pygame.draw.rect(screen, GREEN, (health_x, health_y, current_health_width, health_height))

class Enemy:
    def __init__(self, x, y, enemy_type):
        self.x = x
        self.y = y
        self.type = enemy_type
        self.last_shot = 0
        
        if enemy_type == "mine":
            self.width = 20
            self.height = 20
            self.speed = 2
            self.health = 30
            self.color = RED
            self.can_shoot = False
            self.shoot_delay = 0
            
        elif enemy_type == "fighter":
            self.width = 30
            self.height = 25
            self.speed = 3
            self.health = 50
            self.color = YELLOW
            self.can_shoot = True
            self.shoot_delay = 1500
            
        elif enemy_type == "bomber":
            self.width = 50
            self.height = 35
            self.speed = 1.5
            self.health = 80
            self.color = RED
            self.can_shoot = True
            self.shoot_delay = 2000
            self.move_direction = random.choice([-1, 1])
            
        elif enemy_type == "cargo":
            self.width = 35
            self.height = 40
            self.speed = 2
            self.health = 60
            self.color = GREEN
            self.can_shoot = False
            self.shoot_delay = 0
            
        self.max_health = self.health
    
    def update(self):
        if self.type == "bomber":
            self.x += self.move_direction * 2
            if self.x <= 0 or self.x >= SCREEN_WIDTH - self.width:
                self.move_direction *= -1
                
        self.y += self.speed
        
        # Return True if enemy should be removed (off screen)
        return self.y > SCREEN_HEIGHT
    
    def shoot(self):
        if not self.can_shoot:
            return None
            
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.shoot_delay:
            self.last_shot = current_time
            return Bullet(self.x + self.width//2, self.y + self.height, 5, 'enemy')
        return None
    
    def draw(self, screen):
        # Draw enemy
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        
        # Draw health bar for stronger enemies
        if self.health < self.max_health:
            health_width = self.width
            health_height = 4
            health_x = self.x
            health_y = self.y - 8
            
            pygame.draw.rect(screen, RED, (health_x, health_y, health_width, health_height))
            current_health_width = (self.health / self.max_health) * health_width
            pygame.draw.rect(screen, GREEN, (health_x, health_y, current_health_width, health_height))

class Bullet:
    def __init__(self, x, y, speed, owner):
        self.x = x
        self.y = y
        self.speed = speed
        self.owner = owner
        self.width = 4
        self.height = 8
        
    def update(self):
        self.y += self.speed
        return self.y < -10 or self.y > SCREEN_HEIGHT + 10
    
    def draw(self, screen):
        color = WHITE if self.owner == 'player' else RED
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))

class PowerUp:
    def __init__(self, x, y, power_type):
        self.x = x
        self.y = y
        self.type = power_type
        self.width = 20
        self.height = 20
        self.speed = 2
        
    def update(self):
        self.y += self.speed
        return self.y > SCREEN_HEIGHT
    
    def draw(self, screen):
        color = GREEN if self.type == "health" else BLUE
        pygame.draw.circle(screen, color, (int(self.x + self.width//2), int(self.y + self.height//2)), self.width//2)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Space Shooter")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        self.reset_game()
        
    def reset_game(self):
        self.player = Player(SCREEN_WIDTH//2 - 20, SCREEN_HEIGHT - 80)
        self.bullets = []
        self.enemies = []
        self.powerups = []
        self.score = 0
        self.game_over = False
        self.start_time = pygame.time.get_ticks()
        self.last_enemy_spawn = 0
        self.enemy_spawn_delay = 2000
        
    def spawn_enemy(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_enemy_spawn > self.enemy_spawn_delay:
            self.last_enemy_spawn = current_time
            
            enemy_types = ["mine", "fighter", "bomber", "cargo"]
            enemy_type = random.choice(enemy_types)
            
            x = random.randint(0, SCREEN_WIDTH - 50)
            enemy = Enemy(x, -50, enemy_type)
            self.enemies.append(enemy)
            
            # Increase difficulty over time
            if self.enemy_spawn_delay > 800:
                self.enemy_spawn_delay -= 5
    
    def check_collisions(self):
        # Bullet vs Enemy collisions
        for bullet in self.bullets[:]:
            if bullet.owner == 'player':
                for enemy in self.enemies[:]:
                    if (bullet.x < enemy.x + enemy.width and
                        bullet.x + bullet.width > enemy.x and
                        bullet.y < enemy.y + enemy.height and
                        bullet.y + bullet.height > enemy.y):
                        
                        enemy.health -= 25
                        self.bullets.remove(bullet)
                        
                        if enemy.health <= 0:
                            self.score += 10
                            if enemy.type == "cargo":
                                # Spawn power-up
                                power_type = random.choice(["health", "weapon"])
                                powerup = PowerUp(enemy.x, enemy.y, power_type)
                                self.powerups.append(powerup)
                            self.enemies.remove(enemy)
                        break
        
        # Enemy bullet vs Player collisions
        for bullet in self.bullets[:]:
            if bullet.owner == 'enemy':
                if (bullet.x < self.player.x + self.player.width and
                    bullet.x + bullet.width > self.player.x and
                    bullet.y < self.player.y + self.player.height and
                    bullet.y + bullet.height > self.player.y):
                    
                    self.player.health -= 20
                    self.bullets.remove(bullet)
                    if self.player.health <= 0:
                        self.game_over = True
        
        # Enemy vs Player collisions
        for enemy in self.enemies[:]:
            if (enemy.x < self.player.x + self.player.width and
                enemy.x + enemy.width > self.player.x and
                enemy.y < self.player.y + self.player.height and
                enemy.y + enemy.height > self.player.y):
                
                self.player.health -= 30
                self.enemies.remove(enemy)
                if self.player.health <= 0:
                    self.game_over = True
        
        # PowerUp vs Player collisions
        for powerup in self.powerups[:]:
            if (powerup.x < self.player.x + self.player.width and
                powerup.x + powerup.width > self.player.x and
                powerup.y < self.player.y + self.player.height and
                powerup.y + powerup.height > self.player.y):
                
                if powerup.type == "health":
                    self.player.health = min(self.player.max_health, self.player.health + 30)
                elif powerup.type == "weapon":
                    self.player.bullet_level = min(3, self.player.bullet_level + 1)
                
                self.powerups.remove(powerup)
    
    def save_score(self):
        try:
            scores = []
            if os.path.exists("scores.json"):
                with open("scores.json", "r") as f:
                    scores = json.load(f)
            
            game_time = (pygame.time.get_ticks() - self.start_time) // 1000
            new_score = {
                "score": self.score,
                "time": game_time,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            scores.append(new_score)
            scores.sort(key=lambda x: x["score"], reverse=True)
            
            with open("scores.json", "w") as f:
                json.dump(scores[:10], f)  # Keep top 10 scores
                
        except Exception as e:
            print(f"Error saving score: {e}")
    
    def show_menu(self):
        menu_running = True
        selected = 0
        menu_options = ["start", "scores", "exit"]
        
        while menu_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected = (selected - 1) % len(menu_options)
                    elif event.key == pygame.K_DOWN:
                        selected = (selected + 1) % len(menu_options)
                    elif event.key == pygame.K_RETURN:
                        if selected == 0:  # Start game
                            return True
                        elif selected == 1:  # Show scores
                            self.show_scores()
                        elif selected == 2:  # Exit
                            return False
            
            self.screen.fill(BLACK)
            
            # Title
            title = self.font.render("SPACE SHOOTER", True, WHITE)
            title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 150))
            self.screen.blit(title, title_rect)
            
            # Menu options
            for i, option in enumerate(menu_options):
                color = YELLOW if i == selected else WHITE
                text = self.small_font.render(option, True, color)
                text_rect = text.get_rect(center=(SCREEN_WIDTH//2, 250 + i * 40))
                self.screen.blit(text, text_rect)
            
            # Controls
            controls = [
                "Controls:",
                "Arrow Keys or WASD - Move",
                "Space - Shoot"
            ]
            
            for i, control in enumerate(controls):
                text = self.small_font.render(control, True, WHITE)
                text_rect = text.get_rect(center=(SCREEN_WIDTH//2, 400 + i * 25))
                self.screen.blit(text, text_rect)
            
            pygame.display.flip()
            self.clock.tick(FPS)
    
    def show_scores(self):
        scores_running = True
        
        try:
            with open("scores.json", "r") as f:
                scores = json.load(f)
        except:
            scores = []
        
        while scores_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                    scores_running = False
            
            self.screen.fill(BLACK)
            
            title = self.font.render("HIGH SCORES", True, WHITE)
            title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 50))
            self.screen.blit(title, title_rect)
            
            if scores:
                for i, score in enumerate(scores[:10]):
                    text = f"{i+1}. Score: {score['score']} - Time: {score['time']}s - {score['date']}"
                    score_text = self.small_font.render(text, True, WHITE)
                    score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, 100 + i * 30))
                    self.screen.blit(score_text, score_rect)
            else:
                no_scores = self.small_font.render("No scores yet!", True, WHITE)
                no_scores_rect = no_scores.get_rect(center=(SCREEN_WIDTH//2, 200))
                self.screen.blit(no_scores, no_scores_rect)
            
            back_text = self.small_font.render("Press any key to return", True, YELLOW)
            back_rect = back_text.get_rect(center=(SCREEN_WIDTH//2, 500))
            self.screen.blit(back_text, back_rect)
            
            pygame.display.flip()
            self.clock.tick(FPS)
    
    def run(self):
        running = True
        
        while running:
            # Show menu
            if not self.show_menu():
                break
            
            # Reset game for new play
            self.reset_game()
            
            # Game loop
            while not self.game_over and running:
                # Handle events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            bullet = self.player.shoot()
                            if bullet:
                                self.bullets.append(bullet)
                        elif event.key == pygame.K_ESCAPE:
                            self.game_over = True
                
                # Get pressed keys
                keys = pygame.key.get_pressed()
                
                # Update player
                self.player.move(keys)
                
                # Spawn enemies
                self.spawn_enemy()
                
                # Update bullets
                for bullet in self.bullets[:]:
                    if bullet.update():
                        self.bullets.remove(bullet)
                
                # Update enemies and their shooting
                for enemy in self.enemies[:]:
                    if enemy.update():
                        self.enemies.remove(enemy)
                    else:
                        bullet = enemy.shoot()
                        if bullet:
                            self.bullets.append(bullet)
                
                # Update powerups
                for powerup in self.powerups[:]:
                    if powerup.update():
                        self.powerups.remove(powerup)
                
                # Check collisions
                self.check_collisions()
                
                # Update score based on survival time
                current_time = pygame.time.get_ticks()
                self.score = ((current_time - self.start_time) // 1000) + (self.score % 1000)
                
                # Draw everything
                self.screen.fill(BLACK)
                
                self.player.draw(self.screen)
                
                for bullet in self.bullets:
                    bullet.draw(self.screen)
                
                for enemy in self.enemies:
                    enemy.draw(self.screen)
                
                for powerup in self.powerups:
                    powerup.draw(self.screen)
                
                # Draw UI
                score_text = self.font.render(f"Score: {self.score}", True, WHITE)
                self.screen.blit(score_text, (10, 10))
                
                time_text = self.small_font.render(f"Time: {(current_time - self.start_time) // 1000}s", True, WHITE)
                self.screen.blit(time_text, (10, 50))
                
                pygame.display.flip()
                self.clock.tick(FPS)
            
            # Game over screen
            if self.game_over and running:
                self.save_score()
                
                game_over_running = True
                while game_over_running:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                            game_over_running = False
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_r:
                                game_over_running = False  # Restart
                            elif event.key == pygame.K_ESCAPE or event.key == pygame.K_m:
                                game_over_running = False  # Back to menu
                    
                    self.screen.fill(BLACK)
                    
                    # Game over text
                    game_over_text = self.font.render("GAME OVER", True, RED)
                    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, 200))
                    self.screen.blit(game_over_text, game_over_rect)
                    
                    # Final score
                    final_score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
                    final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH//2, 250))
                    self.screen.blit(final_score_text, final_score_rect)
                    
                    # Instructions
                    restart_text = self.small_font.render("Press R to play again, M for menu, ESC to quit", True, YELLOW)
                    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, 350))
                    self.screen.blit(restart_text, restart_rect)
                    
                    pygame.display.flip()
                    self.clock.tick(FPS)
        
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()