import os
import sys
import time
import threading
import random
from datetime import datetime

# برای ورودی غیرمسدود در ویندوز/لینوکس
try:
    import msvcrt
    def get_key():
        if msvcrt.kbhit():
            return msvcrt.getch().decode('utf-8').lower()
        return None
except ImportError:
    import select
    import tty, termios
    def get_key():
        if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
            return sys.stdin.read(1).lower()
        return None

# تنظیمات بازی
SCREEN_WIDTH = 50
SCREEN_HEIGHT = 20

class GameObject:
    def __init__(self, x, y, symbol, health=1):
        self.x = x
        self.y = y
        self.symbol = symbol
        self.health = health
        self.max_health = health
        self.alive = True

class Player(GameObject):
    def __init__(self):
        super().__init__(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 3, '▲', 100)
        self.bullets = []
        self.last_shot = 0
        
    def move(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy
        
        if 1 <= new_x < SCREEN_WIDTH-1 and 1 <= new_y < SCREEN_HEIGHT-1:
            self.x = new_x
            self.y = new_y
    
    def shoot(self):
        current_time = time.time()
        if current_time - self.last_shot > 0.2:  # حداکثر 5 تیر در ثانیه
            self.bullets.append(GameObject(self.x, self.y-1, '|'))
            self.last_shot = current_time

class Enemy(GameObject):
    def __init__(self, x, y, enemy_type="basic"):
        symbols = {'basic': '▼', 'fighter': '♦', 'bomber': '■'}
        healths = {'basic': 30, 'fighter': 50, 'bomber': 80}
        
        super().__init__(x, y, symbols[enemy_type], healths[enemy_type])
        self.type = enemy_type
        self.bullets = []
        self.last_shot = 0
        self.move_direction = random.choice([-1, 1])
        
    def update(self):
        if not self.alive:
            return
            
        # حرکت پایین
        self.y += 1
        
        # حرکت چپ راست برای bomber
        if self.type == "bomber":
            self.x += self.move_direction
            if self.x <= 1 or self.x >= SCREEN_WIDTH-2:
                self.move_direction *= -1
        
        # تیراندازی
        current_time = time.time()
        shoot_chance = {'basic': 0.005, 'fighter': 0.01, 'bomber': 0.008}
        
        if current_time - self.last_shot > 1 and random.random() < shoot_chance[self.type]:
            self.bullets.append(GameObject(self.x, self.y+1, '!'))
            self.last_shot = current_time
        
        # حذف اگر از صفحه خارج شد
        if self.y >= SCREEN_HEIGHT-1:
            self.alive = False

class Game:
    def __init__(self):
        self.player = Player()
        self.enemies = []
        self.powerups = []
        self.score = 0
        self.running = True
        self.game_over = False
        self.last_enemy_spawn = 0
        self.start_time = time.time()
        self.frame_count = 0
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def spawn_enemy(self):
        current_time = time.time()
        if current_time - self.last_enemy_spawn > 1.5:  # هر 1.5 ثانیه
            enemy_types = ['basic', 'fighter', 'bomber']
            weights = [0.6, 0.3, 0.1]  # احتمال ظهور
            
            enemy_type = random.choices(enemy_types, weights=weights)[0]
            x = random.randint(2, SCREEN_WIDTH-3)
            
            self.enemies.append(Enemy(x, 1, enemy_type))
            self.last_enemy_spawn = current_time
            
            # افزایش سختی با گذشت زمان
            if current_time - self.start_time > 30:  # بعد از 30 ثانیه سخت‌تر شود
                if random.random() < 0.3:  # احتمال دشمن اضافی
                    x2 = random.randint(2, SCREEN_WIDTH-3)
                    self.enemies.append(Enemy(x2, 1, random.choice(enemy_types)))
    
    def update_bullets(self):
        # تیرهای بازیکن
        for bullet in self.player.bullets[:]:
            bullet.y -= 2  # سرعت تیر بالا
            if bullet.y < 1:
                self.player.bullets.remove(bullet)
        
        # تیرهای دشمن‌ها
        for enemy in self.enemies:
            for bullet in enemy.bullets[:]:
                bullet.y += 1  # سرعت تیر پایین
                if bullet.y >= SCREEN_HEIGHT-1:
                    enemy.bullets.remove(bullet)
    
    def check_collisions(self):
        # تیر بازیکن به دشمن
        for bullet in self.player.bullets[:]:
            for enemy in self.enemies[:]:
                if enemy.alive and bullet.x == enemy.x and bullet.y == enemy.y:
                    enemy.health -= 25
                    self.player.bullets.remove(bullet)
                    
                    if enemy.health <= 0:
                        enemy.alive = False
                        self.score += {'basic': 10, 'fighter': 20, 'bomber': 30}[enemy.type]
                        
                        # احتمال پاور آپ
                        if random.random() < 0.2:
                            self.powerups.append(GameObject(enemy.x, enemy.y, '♥'))
                    break
        
        # تیر دشمن به بازیکن
        for enemy in self.enemies:
            for bullet in enemy.bullets[:]:
                if bullet.x == self.player.x and bullet.y == self.player.y:
                    self.player.health -= 15
                    enemy.bullets.remove(bullet)
                    if self.player.health <= 0:
                        self.game_over = True
        
        # برخورد مستقیم دشمن با بازیکن
        for enemy in self.enemies:
            if enemy.alive and enemy.x == self.player.x and enemy.y == self.player.y:
                self.player.health -= 30
                enemy.alive = False
                if self.player.health <= 0:
                    self.game_over = True
        
        # جمع آوری پاور آپ
        for powerup in self.powerups[:]:
            if powerup.x == self.player.x and powerup.y == self.player.y:
                self.player.health = min(100, self.player.health + 20)
                self.powerups.remove(powerup)
                self.score += 5
    
    def create_screen(self):
        # ساخت صفحه خالی
        screen = []
        for y in range(SCREEN_HEIGHT):
            row = []
            for x in range(SCREEN_WIDTH):
                if y == 0 or y == SCREEN_HEIGHT-1:
                    row.append('═')
                elif x == 0 or x == SCREEN_WIDTH-1:
                    row.append('║')
                else:
                    row.append(' ')
            screen.append(row)
        
        # قرار دادن بازیکن
        if self.player.alive:
            screen[self.player.y][self.player.x] = self.player.symbol
        
        # قرار دادن دشمن‌ها
        for enemy in self.enemies:
            if enemy.alive and 0 <= enemy.y < SCREEN_HEIGHT and 0 <= enemy.x < SCREEN_WIDTH:
                screen[enemy.y][enemy.x] = enemy.symbol
        
        # قرار دادن تیرها
        for bullet in self.player.bullets:
            if 0 <= bullet.y < SCREEN_HEIGHT and 0 <= bullet.x < SCREEN_WIDTH:
                screen[bullet.y][bullet.x] = bullet.symbol
        
        for enemy in self.enemies:
            for bullet in enemy.bullets:
                if 0 <= bullet.y < SCREEN_HEIGHT and 0 <= bullet.x < SCREEN_WIDTH:
                    screen[bullet.y][bullet.x] = bullet.symbol
        
        # قرار دادن پاور آپ‌ها
        for powerup in self.powerups:
            if 0 <= powerup.y < SCREEN_HEIGHT and 0 <= powerup.x < SCREEN_WIDTH:
                screen[powerup.y][powerup.x] = powerup.symbol
        
        return screen
    
    def draw_screen(self, screen):
        for row in screen:
            print(''.join(row))
    
    def draw_hud(self):
        # نمایش اطلاعات بازی
        health_bar = '♥' * (self.player.health // 5) + '♡' * ((100 - self.player.health) // 5)
        time_alive = int(time.time() - self.start_time)
        
        print(f"╔═══ SPACE COMBAT ═══╗")
        print(f"║ سلامت: {health_bar[:10]} ({self.player.health}%)  ║")
        print(f"║ امتیاز: {self.score:<6} زمان: {time_alive:<3}s ║")
        print(f"║ دشمنان: {len([e for e in self.enemies if e.alive]):<2}       ║")
        print(f"╚════════════════════╝")
    
    def handle_input(self):
        key = get_key()
        if key:
            if key == 'a':
                self.player.move(-1, 0)
            elif key == 'd':
                self.player.move(1, 0)
            elif key == 'w':
                self.player.move(0, -1)
            elif key == 's':
                self.player.move(0, 1)
            elif key == ' ':
                self.player.shoot()
            elif key == 'q':
                self.running = False
    
    def game_loop(self):
        while self.running and not self.game_over:
            self.frame_count += 1
            
            # ورودی
            self.handle_input()
            
            # تولید دشمن
            self.spawn_enemy()
            
            # به‌روزرسانی
            self.update_bullets()
            for enemy in self.enemies[:]:
                enemy.update()
                if not enemy.alive:
                    self.enemies.remove(enemy)
            
            # به‌روزرسانی پاور آپ‌ها
            for powerup in self.powerups[:]:
                powerup.y += 1
                if powerup.y >= SCREEN_HEIGHT-1:
                    self.powerups.remove(powerup)
            
            # برخوردها
            self.check_collisions()
            
            # رسم (هر 3 فریم یکبار برای کاهش flicker)
            if self.frame_count % 2 == 0:
                self.clear_screen()
                screen = self.create_screen()
                self.draw_hud()
                self.draw_screen(screen)
                
                print("\n🎮 کنترل‌ها: WASD=حرکت | Space=شلیک | Q=خروج")
            
            time.sleep(0.05)  # 20 FPS
    
    def show_game_over(self):
        self.clear_screen()
        print("╔═══════════════════════════╗")
        print("║        GAME OVER!         ║")
        print("╠═══════════════════════════╣")
        print(f"║ امتیاز نهایی: {self.score:<10} ║")
        print(f"║ زمان بقا: {int(time.time() - self.start_time):<3} ثانیه       ║")
        print("║                           ║")
        print("║ مبارک! جنگجوی فضایی!     ║")
        print("╚═══════════════════════════╝")
        
        # ذخیره امتیاز
        try:
            with open('space_scores.txt', 'a', encoding='utf-8') as f:
                f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M')} - امتیاز: {self.score} - زمان: {int(time.time() - self.start_time)}s\n")
            print("امتیاز ذخیره شد!")
        except:
            pass
    
    def run(self):
        try:
            self.clear_screen()
            print("🚀 === جنگ فضایی === 🚀")
            print("آماده برای مبارزه؟")
            input("Enter برای شروع جنگ...")
            
            self.game_loop()
            self.show_game_over()
            
        except KeyboardInterrupt:
            print("\nبازی متوقف شد!")
        except Exception as e:
            print(f"خطا: {e}")

if __name__ == "__main__":
    game = Game()
    game.run()