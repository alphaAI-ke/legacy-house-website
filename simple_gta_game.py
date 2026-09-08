"""
Simple GTA-inspired Game
A lightweight Python game with player movement, vehicles, and wanted levels
"""

import random
import os

class Player:
    def __init__(self, name, x=50, y=50):
        self.name = name
        self.x = x
        self.y = y
        self.money = 1000
        self.health = 100
        self.wanted_level = 0
        self.in_vehicle = False
        self.vehicle = None

    def move(self, direction):
        """Move player in specified direction"""
        if direction.lower() == 'up':
            self.y = max(0, self.y - 5)
        elif direction.lower() == 'down':
            self.y = min(100, self.y + 5)
        elif direction.lower() == 'left':
            self.x = max(0, self.x - 5)
        elif direction.lower() == 'right':
            self.x = min(100, self.x + 5)
        
        if self.in_vehicle and self.vehicle:
            self.vehicle.x = self.x
            self.vehicle.y = self.y

    def enter_vehicle(self, vehicle):
        """Enter a vehicle"""
        self.in_vehicle = True
        self.vehicle = vehicle
        self.x = vehicle.x
        self.y = vehicle.y
        print(f"✓ Entered {vehicle.name}!")

    def exit_vehicle(self):
        """Exit current vehicle"""
        if self.in_vehicle and self.vehicle:
            self.in_vehicle = False
            print(f"✓ Exited {self.vehicle.name}!")
            self.vehicle = None

    def steal_vehicle(self, vehicle):
        """Steal a vehicle and get wanted level"""
        self.enter_vehicle(vehicle)
        self.wanted_level = min(5, self.wanted_level + 1)
        print(f"⚠ WANTED LEVEL: {self.wanted_level}/5")

    def rob_store(self):
        """Rob a store for money"""
        amount = random.randint(500, 2000)
        self.money += amount
        self.wanted_level = min(5, self.wanted_level + 2)
        print(f"💰 Robbed store! Got ${amount}")
        print(f"⚠ WANTED LEVEL: {self.wanted_level}/5")

    def complete_mission(self, reward):
        """Complete a mission"""
        self.money += reward
        self.wanted_level = max(0, self.wanted_level - 1)
        print(f"✓ Mission complete! Earned ${reward}")


    def get_arrested(self):
        """Get arrested by police"""
        self.money = max(0, self.money - 500)
             python snake_game.py   self.health = 50
        self.wanted_level = 0
        self.x, self.y = 50, 50
        self.exit_vehicle()
        print("❌ BUSTED! Police arrested you. Lost $500.")

    def take_damage(self, amount):
        """Take damage"""
        self.health = max(0, self.health - amount)
        if self.health == 0:
            print("💀 You died!")

    def heal(self, amount=50):
        """Heal yourself"""
        self.health = min(100, self.health + amount)
        print(f"🏥 Healed! Health: {self.health}/100")

    def status(self):
        """Display player status"""
        vehicle_info = f" | Vehicle: {self.vehicle.name}" if self.in_vehicle else ""
        return f"""
╔══════════════════════════════════════╗
║ PLAYER STATUS
╠══════════════════════════════════════╣
║ Name: {self.name}
║ Position: ({self.x}, {self.y})
║ Health: {self.health}/100
║ Money: ${self.money}
║ Wanted Level: {self.wanted_level}/5 {'🚔' * self.wanted_level}
║{vehicle_info}
╚══════════════════════════════════════╝
        """


class Vehicle:
    def __init__(self, name, vehicle_type, speed, x=random.randint(0, 100), y=random.randint(0, 100)):
        self.name = name
        self.vehicle_type = vehicle_type
        self.speed = speed
        self.x = x
        self.y = y
        self.health = 100

    def drive(self, direction):
        """Drive vehicle in specified direction"""
        speed = self.speed // 5
        if direction.lower() == 'up':
            self.y = max(0, self.y - speed)
        elif direction.lower() == 'down':
            self.y = min(100, self.y + speed)
        elif direction.lower() == 'left':
            self.x = max(0, self.x - speed)
        elif direction.lower() == 'right':
            self.x = min(100, self.x + speed)

    def info(self):
        """Display vehicle info"""
        return f"{self.name} ({self.vehicle_type}) - Speed: {self.speed}, Health: {self.health}/100"


class Game:
    def __init__(self):
        self.player = None
        self.vehicles = []
        self.missions = [
            {"name": "Deliver Package", "reward": 500},
            {"name": "Destroy Car", "reward": 750},
            {"name": "Rob Convenience Store", "reward": 1000},
            {"name": "Protect Target", "reward": 1200},
            {"name": "Escape Police", "reward": 800},
        ]
        self.completed_missions = 0

    def clear_screen(self):
        """Clear console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def setup_game(self):
        """Setup game"""
        self.clear_screen()
        print("╔═══════════════════════════════════════╗")
        print("║     🎮 SIMPLE GTA - TEXT EDITION 🎮   ║")
        print("╚═══════════════════════════════════════╝\n")
        
        name = input("Enter your character name: ").strip() or "CJ"
        self.player = Player(name)

        # Create vehicles
        self.vehicles = [
            Vehicle("Blista Compact", "Car", 80),
            Vehicle("Sabreman", "Jeep", 70),
            Vehicle("Manana", "Classic Car", 60),
            Vehicle("PCJ-600", "Motorcycle", 90),
            Vehicle("Ambulance", "Emergency", 75),
        ]

    def display_menu(self):
        """Display main game menu"""
        print("\n╔═══════════════════════════════════════╗")
        print("║           MAIN MENU                   ║")
        print("╠═══════════════════════════════════════╣")
        print("║ 1. Move (up/down/left/right)          ║")
        print("║ 2. View Nearby Vehicles               ║")
        print("║ 3. Steal Vehicle                      ║")
        print("║ 4. Exit Vehicle                       ║")
        print("║ 5. Drive Vehicle                      ║")
        print("║ 6. Rob Store                          ║")
        print("║ 7. Accept Mission                     ║")
        print("║ 8. Heal                               ║")
        print("║ 9. View Status                        ║")
        print("║ 0. Quit Game                          ║")
        print("╚═══════════════════════════════════════╝")

    def view_vehicles(self):
        """Show nearby vehicles"""
        print("\n🚗 NEARBY VEHICLES:")
        for i, vehicle in enumerate(self.vehicles, 1):
            distance = ((self.player.x - vehicle.x)**2 + (self.player.y - vehicle.y)**2) ** 0.5
            print(f"   {i}. {vehicle.info()} (Distance: {distance:.1f})")

    def steal_vehicle_menu(self):
        """Menu to steal a vehicle"""
        self.view_vehicles()
        try:
            choice = int(input("\nSelect vehicle to steal (0 to cancel): "))
            if 0 < choice <= len(self.vehicles):
                vehicle = self.vehicles[choice - 1]
                self.player.steal_vehicle(vehicle)
            elif choice != 0:
                print("Invalid selection!")
        except ValueError:
            print("Invalid input!")

    def drive_vehicle_menu(self):
        """Menu to drive vehicle"""
        if not self.player.in_vehicle:
            print("❌ You need to be in a vehicle first!")
            return

        print(f"\nDriving {self.player.vehicle.name}...")
        direction = input("Move (up/down/left/right/exit): ").strip().lower()
        
        if direction == 'exit':
            self.player.exit_vehicle()
        elif direction in ['up', 'down', 'left', 'right']:
            self.player.vehicle.drive(direction)
            print(f"Position: ({self.player.vehicle.x:.1f}, {self.player.vehicle.y:.1f})")
        else:
            print("Invalid direction!")

    def accept_mission(self):
        """Accept a random mission"""
        mission = random.choice(self.missions)
        print(f"\n📋 MISSION ACCEPTED: {mission['name']}")
        print(f"Reward: ${mission['reward']}")
        
        # Simple mission completion
        response = input("Complete mission? (yes/no): ").strip().lower()
        if response == 'yes':
            self.player.complete_mission(mission['reward'])
            self.completed_missions += 1
        else:
            print("Mission abandoned.")

    def police_check(self):
        """Check if player gets caught by police"""
        if self.player.wanted_level > 0:
            if random.random() < 0.3 * self.player.wanted_level:  # Higher wanted = more chance
                print("\n🚔 POLICE ALERT!")
                if random.random() < 0.5:
                    print("You managed to escape!")
                    self.player.wanted_level = max(0, self.player.wanted_level - 1)
                else:
                    self.player.get_arrested()

    def run(self):
        """Main game loop"""
        self.setup_game()
        print(self.player.status())
        
        while self.player.health > 0:
            self.police_check()
            self.display_menu()
            
            choice = input("\nSelect action (0-9): ").strip()
            
            if choice == '1':
                direction = input("Move direction (up/down/left/right): ").strip()
                self.player.move(direction)
                print(f"Position: ({self.player.x}, {self.player.y})")
            
            elif choice == '2':
                self.view_vehicles()
            
            elif choice == '3':
                self.steal_vehicle_menu()
            
            elif choice == '4':
                self.player.exit_vehicle()
            
            elif choice == '5':
                self.drive_vehicle_menu()
            
            elif choice == '6':
                self.player.rob_store()
            
            elif choice == '7':
                self.accept_mission()
            
            elif choice == '8':
                self.player.heal()
            
            elif choice == '9':
                print(self.player.status())
            
            elif choice == '0':
                print(f"\n👋 Game Over! You earned ${self.player.money} and completed {self.completed_missions} missions.")
                break
            
            else:
                print("Invalid choice! Try again.")

        if self.player.health <= 0:
            print(f"\n💀 GAME OVER! Final Stats:")
            print(f"Money: ${self.player.money}")
            print(f"Missions Completed: {self.completed_missions}")


if __name__ == "__main__":
    game = Game()
    game.run()
