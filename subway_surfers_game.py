"""
Simple Subway Surfers Game
A text-based version of the popular mobile game
"""

import random
import os
import time

class Player:
    def __init__(self):
        self.x = 1  # Lane position (0, 1, or 2)
        self.y = 15  # Distance from bottom
        self.score = 0
        self.health = 3
        self.coins = 0
        self.multiplier = 1
        self.invincible = False
        self.invincible_time = 0
        self.speed_boost = False
        self.speed_boost_time = 0

    def move_left(self):
        """Move player left"""
        if self.x > 0:
            self.x -= 1

    def move_right(self):
        """Move player right"""
        if self.x < 2:
            self.x += 1

    def jump(self):
        """Jump up"""
        if self.y < 18:
            self.y += 2

    def slide(self):
        """Slide down"""
        if self.y > 0:
            self.y -= 1

    def take_damage(self):
        """Take damage from collision"""
        if not self.invincible:
            self.health -= 1
            self.invincible = True
            self.invincible_time = 10

    def collect_coin(self):
        """Collect a coin"""
        self.coins += 1
        self.score += 10 * self.multiplier

    def activate_shield(self):
        """Activate shield (invincibility)"""
        self.invincible = True
        self.invincible_time = 15

    def activate_speed_boost(self):
        """Activate speed boost"""
        self.speed_boost = True
        self.speed_boost_time = 10
        self.multiplier = 2

    def update_powerups(self):
        """Update power-up timers"""
        if self.invincible_time > 0:
            self.invincible_time -= 1
        else:
            self.invincible = False

        if self.speed_boost_time > 0:
            self.speed_boost_time -= 1
        else:
            self.speed_boost = False
            self.multiplier = 1


class Obstacle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.symbol = "█"

    def move_down(self):
        """Move obstacle down"""
        self.y -= 1


class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.symbol = "◆"
        self.collected = False

    def move_down(self):
        """Move coin down"""
        self.y -= 1


class PowerUp:
    def __init__(self, x, y, power_type):
        self.x = x
        self.y = y
        self.power_type = power_type  # "shield" or "speed"
        self.symbol = "⚡" if power_type == "speed" else "🛡"
        self.collected = False

    def move_down(self):
        """Move power-up down"""
        self.y -= 1


class Train:
    def __init__(self, y):
        self.y = y
        self.width = 40
        self.appeared = False

    def move_down(self):
        """Move train down"""
        self.y -= 1

    def is_visible(self):
        """Check if train is visible on screen"""
        return self.y >= -2 and self.y <= 20


class SubwaySurfersGame:
    def __init__(self):
        self.player = Player()
        self.obstacles = []
        self.coins = []
        self.powerups = []
        self.trains = []
        self.distance = 0
        self.game_over = False
        self.difficulty = 1
        self.spawn_counter = 0
        self.game_started = False
        self.high_score = 0
        self.paused = False

    def clear_screen(self):
        """Clear console"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_title(self):
        """Display game title"""
        print("╔════════════════════════════════════════════════╗")
        print("║  🚇 SUBWAY SURFERS - TEXT EDITION 🚇            ║")
        print("╠════════════════════════════════════════════════╣")
        print("║  Dodge obstacles, collect coins, and survive!  ║")
        print("║  Controls: A/D (move), W (jump), S (slide)     ║")
        print("║            P (pause), Q (quit)                 ║")
        print("╚════════════════════════════════════════════════╝\n")

    def display_game(self):
        """Display the game screen"""
        self.clear_screen()
        
        # Display HUD
        print(f"Score: {self.player.score} | Coins: {self.player.coins} | Health: {self.player.health} | Distance: {self.distance}m")
        print(f"Multiplier: {self.player.multiplier}x | ", end="")
        
        if self.player.invincible:
            print(f"SHIELD: {self.player.invincible_time}s | ", end="")
        if self.player.speed_boost:
            print(f"SPEED BOOST: {self.player.speed_boost_time}s", end="")
        print("\n" + "="*50 + "\n")

        # Create game field
        field = []
        for y in range(20, -1, -1):
            row = [' ', ' ', ' ']  # 3 lanes

            # Draw player
            if y == self.player.y:
                if self.player.invincible:
                    row[self.player.x] = '◉'  # Invincible player
                elif self.player.speed_boost:
                    row[self.player.x] = '◎'  # Speed boost player
                else:
                    row[self.player.x] = '●'  # Normal player

            # Draw obstacles
            for obstacle in self.obstacles:
                if obstacle.y == y and 0 <= obstacle.x < 3:
                    row[obstacle.x] = '█'

            # Draw coins
            for coin in self.coins:
                if coin.y == y and 0 <= coin.x < 3 and not coin.collected:
                    row[coin.x] = '◆'

            # Draw power-ups
            for powerup in self.powerups:
                if powerup.y == y and 0 <= powerup.x < 3 and not powerup.collected:
                    row[powerup.x] = '⚡' if powerup.power_type == "speed" else '✦'

            # Draw trains
            for train in self.trains:
                if train.y == y and train.is_visible():
                    row = ['═', '═', '═']
                    break

            # Display row with borders
            print(f"║ {row[0]} │ {row[1]} │ {row[2]} ║  Y:{y}")

        print("="*50)
        print("Lane:  0   1   2")

        if self.paused:
            print("\n⏸  GAME PAUSED")

    def spawn_obstacles(self):
        """Spawn obstacles randomly"""
        self.spawn_counter += 1
        spawn_rate = max(15 - self.difficulty, 8)

        if self.spawn_counter >= spawn_rate:
            x = random.randint(0, 2)
            self.obstacles.append(Obstacle(x, 20))
            self.spawn_counter = 0

            # Occasionally spawn trains
            if random.random() < 0.05:
                self.trains.append(Train(20))

    def spawn_coins(self):
        """Spawn coins randomly"""
        if random.random() < 0.15:
            x = random.randint(0, 2)
            self.coins.append(Coin(x, 20))

    def spawn_powerups(self):
        """Spawn power-ups randomly"""
        if random.random() < 0.05:
            x = random.randint(0, 2)
            power_type = random.choice(["shield", "speed"])
            self.powerups.append(PowerUp(x, 20, power_type))

    def update_game(self):
        """Update game state"""
        # Update player power-ups
        self.player.update_powerups()

        # Spawn items
        self.spawn_obstacles()
        self.spawn_coins()
        self.spawn_powerups()

        # Move obstacles
        self.obstacles = [obs for obs in self.obstacles if obs.y >= -1]
        for obstacle in self.obstacles:
            obstacle.move_down()

        # Move coins
        self.coins = [coin for coin in self.coins if coin.y >= -1]
        for coin in self.coins:
            coin.move_down()

        # Move power-ups
        self.powerups = [pu for pu in self.powerups if pu.y >= -1]
        for powerup in self.powerups:
            powerup.move_down()

        # Move trains
        self.trains = [train for train in self.trains if train.y >= -3]
        for train in self.trains:
            train.move_down()

        # Increase distance
        self.distance += 10 * (1 if not self.player.speed_boost else 2)
        self.player.score += 5 * self.player.multiplier

        # Increase difficulty
        self.difficulty = 1 + self.distance // 1000

    def check_collisions(self):
        """Check collisions with obstacles and coins"""
        # Check coin collection
        for coin in self.coins:
            if coin.x == self.player.x and coin.y == self.player.y:
                self.player.collect_coin()
                coin.collected = True

        # Check power-up collection
        for powerup in self.powerups:
            if powerup.x == self.player.x and powerup.y == self.player.y:
                if powerup.power_type == "shield":
                    self.player.activate_shield()
                    print("✓ Shield activated!")
                else:
                    self.player.activate_speed_boost()
                    print("✓ Speed boost activated!")
                powerup.collected = True

        # Check obstacle collision
        for obstacle in self.obstacles:
            if obstacle.x == self.player.x and obstacle.y == self.player.y:
                if not self.player.invincible:
                    self.player.take_damage()
                    print("⚠ Hit! Damaged!")
                    time.sleep(0.5)
                else:
                    obstacle.y = -10  # Remove obstacle if invincible

        # Check train collision
        for train in self.trains:
            if train.y == self.player.y and train.is_visible():
                if not self.player.invincible:
                    self.player.health = 0
                    self.game_over = True
                    print("💥 Hit by train! Game Over!")
                    time.sleep(1)

    def handle_input(self):
        """Handle player input (non-blocking)"""
        import sys
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            user_input = sys.stdin.readline().strip().lower()
            if user_input == 'a':
                self.player.move_left()
            elif user_input == 'd':
                self.player.move_right()
            elif user_input == 'w':
                self.player.jump()
            elif user_input == 's':
                self.player.slide()
            elif user_input == 'p':
                self.paused = not self.paused
            elif user_input == 'q':
                self.game_over = True

    def run_game(self):
        """Main game loop"""
        self.display_title()
        input("Press ENTER to start the game!")
        self.game_started = True

        while not self.game_over and self.player.health > 0:
            self.display_game()

            # Simple input handling
            try:
                user_input = input("\nMove (A/D/W/S) or Q to quit: ").strip().lower()
                
                if user_input == 'a':
                    self.player.move_left()
                elif user_input == 'd':
                    self.player.move_right()
                elif user_input == 'w':
                    self.player.jump()
                elif user_input == 's':
                    self.player.slide()
                elif user_input == 'p':
                    self.paused = not self.paused
                    continue
                elif user_input == 'q':
                    self.game_over = True
                    break

                if not self.paused:
                    self.update_game()
                    self.check_collisions()

            except KeyboardInterrupt:
                self.game_over = True

        self.end_game()

    def end_game(self):
        """Display end game screen"""
        self.clear_screen()
        print("╔════════════════════════════════════════════════╗")
        print("║            ★ GAME OVER ★                      ║")
        print("╠════════════════════════════════════════════════╣")
        print(f"║ Final Score: {self.player.score:<34}║")
        print(f"║ Distance: {self.distance}m{' ' * (30 - len(str(self.distance)))}║")
        print(f"║ Coins Collected: {self.player.coins:<28}║")
        print(f"║ Multiplier Reached: {self.player.multiplier}x{' ' * (26 - len(str(self.player.multiplier)))}║")
        print("╚════════════════════════════════════════════════╝\n")


def main():
    """Main function"""
    while True:
        game = SubwaySurfersGame()
        game.run_game()

        play_again = input("\nPlay again? (yes/no): ").strip().lower()
        if play_again != 'yes' and play_again != 'y':
            print("Thanks for playing! 👋")
            break


if __name__ == "__main__":
    main()
