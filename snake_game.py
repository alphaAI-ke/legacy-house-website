"""
Simple Snake Game
A classic text-based snake game with growing mechanics
"""

import random
import os
import time

class SnakeGame:
    def __init__(self, width=20, height=10):
        self.width = width
        self.height = height
        self.snake = [(width // 2, height // 2)]
        self.direction = (1, 0)  # Moving right initially
        self.next_direction = (1, 0)
        self.food = self.spawn_food()
        self.score = 0
        self.game_over = False
        self.game_speed = 0.3  # Speed in seconds
        self.obstacles = []
        self.level = 1
        self.food_eaten = 0

    def spawn_food(self):
        """Spawn food at random location not occupied by snake"""
        while True:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if (x, y) not in self.snake and (x, y) not in self.obstacles:
                return (x, y)

    def spawn_obstacles(self):
        """Spawn obstacles based on level"""
        self.obstacles = []
        num_obstacles = min(self.level * 2, 15)
        
        for _ in range(num_obstacles):
            while True:
                x = random.randint(1, self.width - 2)
                y = random.randint(1, self.height - 2)
                pos = (x, y)
                if pos not in self.snake and pos != self.food and pos not in self.obstacles:
                    self.obstacles.append(pos)
                    break

    def update_direction(self, new_direction):
        """Update snake direction (prevent 180 degree turns)"""
        opposite = (-self.direction[0], -self.direction[1])
        if new_direction != opposite:
            self.next_direction = new_direction

    def move_snake(self):
        """Move snake in current direction"""
        self.direction = self.next_direction
        head_x, head_y = self.snake[0]
        
        # Calculate new head position
        new_x = (head_x + self.direction[0]) % self.width
        new_y = (head_y + self.direction[1]) % self.height
        
        new_head = (new_x, new_y)

        # Check if snake hits itself
        if new_head in self.snake:
            self.game_over = True
            print("💥 Game Over! Snake hit itself!")
            return

        # Check if snake hits obstacle
        if new_head in self.obstacles:
            self.game_over = True
            print("💥 Game Over! Snake hit an obstacle!")
            return

        # Add new head
        self.snake.insert(0, new_head)

        # Check if food eaten
        if new_head == self.food:
            self.score += 10 * self.level
            self.food_eaten += 1
            self.food = self.spawn_food()
            
            # Increase level every 5 food pieces
            if self.food_eaten % 5 == 0:
                self.level += 1
                self.game_speed = max(0.1, self.game_speed - 0.05)
                self.spawn_obstacles()
                print(f"🎉 LEVEL UP! Level {self.level}")
                time.sleep(1)
        else:
            # Remove tail if no food eaten
            self.snake.pop()

    def display_game(self):
        """Display the game board"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Display header
        print("╔" + "═" * (self.width * 2 + 1) + "╗")
        
        # Display game board
        for y in range(self.height):
            print("║", end="")
            for x in range(self.width):
                if (x, y) == self.snake[0]:
                    print("●", end=" ")  # Snake head
                elif (x, y) in self.snake:
                    print("○", end=" ")  # Snake body
                elif (x, y) == self.food:
                    print("◆", end=" ")  # Food
                elif (x, y) in self.obstacles:
                    print("█", end=" ")  # Obstacle
                else:
                    print(" ", end=" ")
            print("║")
        
        # Display footer
        print("╚" + "═" * (self.width * 2 + 1) + "╝")
        
        # Display stats
        print(f"Score: {self.score} | Length: {len(self.snake)} | Level: {self.level} | Food Eaten: {self.food_eaten}")
        print(f"Speed: {1/self.game_speed:.1f}x | Direction: {self.get_direction_name()}")

    def get_direction_name(self):
        """Get direction name"""
        if self.direction == (1, 0):
            return "→ Right"
        elif self.direction == (-1, 0):
            return "← Left"
        elif self.direction == (0, -1):
            return "↑ Up"
        elif self.direction == (0, 1):
            return "↓ Down"

    def display_title(self):
        """Display game title"""
        print("╔════════════════════════════════════════════════╗")
        print("║         🐍 SIMPLE SNAKE GAME 🐍                ║")
        print("╠════════════════════════════════════════════════╣")
        print("║  Controls:                                     ║")
        print("║  W - Move Up      ↑                            ║")
        print("║  A - Move Left    ←                            ║")
        print("║  S - Move Down    ↓                            ║")
        print("║  D - Move Right   →                            ║")
        print("║  P - Pause/Resume                              ║")
        print("║  Q - Quit Game                                 ║")
        print("║                                                ║")
        print("║  ● = Head   ○ = Body   ◆ = Food   █ = Obstacle║")
        print("╚════════════════════════════════════════════════╝\n")

    def show_menu(self):
        """Show main menu"""
        self.display_title()
        print("Game Modes:")
        print("1. Normal Mode (20x10 grid)")
        print("2. Hard Mode (30x15 grid)")
        print("3. Classic Mode (15x10 grid, no obstacles)")
        print()
        
        choice = input("Select mode (1-3): ").strip()
        
        if choice == '2':
            self.width = 30
            self.height = 15
            self.snake = [(self.width // 2, self.height // 2)]
            self.spawn_obstacles()
        elif choice == '3':
            self.width = 15
            self.height = 10
            self.snake = [(self.width // 2, self.height // 2)]
            self.obstacles = []
        else:
            self.spawn_obstacles()

    def run(self):
        """Main game loop"""
        self.show_menu()
        
        paused = False
        last_move_time = time.time()

        try:
            while not self.game_over:
                self.display_game()

                # Handle input with timeout
                current_time = time.time()
                time_since_move = current_time - last_move_time

                if time_since_move >= self.game_speed:
                    # Get user input
                    try:
                        user_input = input("\nMove (W/A/S/D) or P to pause, Q to quit: ").strip().lower()
                        
                        if user_input == 'w':
                            self.update_direction((0, -1))
                        elif user_input == 'a':
                            self.update_direction((-1, 0))
                        elif user_input == 's':
                            self.update_direction((0, 1))
                        elif user_input == 'd':
                            self.update_direction((1, 0))
                        elif user_input == 'p':
                            paused = not paused
                            if paused:
                                print("⏸  GAME PAUSED - Press ENTER to continue...")
                                input()
                            continue
                        elif user_input == 'q':
                            self.game_over = True
                            print("\n👋 Thanks for playing!")
                            break

                        if not paused:
                            self.move_snake()
                            last_move_time = current_time

                    except KeyboardInterrupt:
                        self.game_over = True
                        print("\n\n👋 Game interrupted!")
                        break
                else:
                    # Brief pause to prevent busy waiting
                    time.sleep(0.05)

        except Exception as e:
            print(f"Error: {e}")

    def end_game(self):
        """Display end game screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print("╔════════════════════════════════════════════════╗")
        print("║            ★ GAME OVER ★                      ║")
        print("╠════════════════════════════════════════════════╣")
        print(f"║ Final Score: {self.score:<34}║")
        print(f"║ Snake Length: {len(self.snake):<32}║")
        print(f"║ Food Eaten: {self.food_eaten:<33}║")
        print(f"║ Level Reached: {self.level:<31}║")
        print("╚════════════════════════════════════════════════╝\n")


def main():
    """Main function"""
    while True:
        game = SnakeGame()
        game.run()
        game.end_game()

        play_again = input("Play again? (yes/no): ").strip().lower()
        if play_again not in ['yes', 'y']:
            print("\nThanks for playing Snake! 🐍👋")
            break


if __name__ == "__main__":
    main()
