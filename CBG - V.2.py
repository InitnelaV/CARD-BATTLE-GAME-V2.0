import random
import pygame
import sys
import time

# Pygame init
pygame.init()

# Window
WIDTH, HEIGHT = 1200, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Card Battle")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 140, 0)

# Load backgrounds
backgrounds = [
    pygame.image.load("Backgrounds/background1.png"),  # Bckgd enemies_light
    pygame.image.load("Backgrounds/background2.png"),  # Bckgd enemies_effect
    pygame.image.load("Backgrounds/background3.png"),  # Bckgd enemies_magic
    pygame.image.load("Backgrounds/background4.png"),  # Bckgd enemies_tank
    pygame.image.load("Backgrounds/background5.png"),  # Bckgd enemies_Boss
    pygame.image.load("Backgrounds/background6.png"),  # Bckgd enemies_Boss
    pygame.image.load("Backgrounds/background7.png"),  # Bckgd ending
    pygame.image.load("Backgrounds/background8.png"),  # Bckgd game_over
]
current_background_index = 0

# Load sounds
sounds = [
    pygame.mixer.Sound("Sounds/battle1.wav"),  # Sound enemies_light
    pygame.mixer.Sound("Sounds/battle2.wav"),  # Sound enemies_effect
    pygame.mixer.Sound("Sounds/battle3.wav"),  # Sound enemies_magic
    pygame.mixer.Sound("Sounds/battle4.wav"),  # Sound friend_mage
    pygame.mixer.Sound("Sounds/battle5.wav"),  # Sound enemies_tank
    pygame.mixer.Sound("Sounds/battle6.wav"),  # Sound enemies_Boss
    pygame.mixer.Sound("Sounds/battle7.wav"),  # Sound ending
    pygame.mixer.Sound("Sounds/battle8.wav"),  # Sound game_over
]
current_sound_index = 0

# Variables
magic_uses_left = 3

# Play the initial sound
sounds[current_sound_index].play(-1)  # Loop the current sound

# EnemyCard class
class EnemyCard:
    def __init__(self, name, damage_range, image_path, hp):
        self.name = name
        self.damage_range = damage_range
        self.hp = hp
        self.max_hp = hp
        self.image = pygame.transform.scale(pygame.image.load(image_path), (300, 400))

    def deal_damage(self):
        return random.randint(*self.damage_range)

# Hero class
class Hero:
    def __init__(self, image_path, hp, damage_range):
        self.image = pygame.transform.scale(pygame.image.load(image_path), (300, 400))
        self.hp = hp
        self.max_hp = hp
        self.damage_range = damage_range
        self.heal_count = 0  # To track potion usage

    def deal_damage(self):
        return random.randint(*self.damage_range)

# Initialize player
player = Hero("Characters/Hero.png", 100, (10, 20))

# Enemy groups
enemies_light = [
    EnemyCard("The Slug", (1, 5), "Characters/Slug.png", 50),
    EnemyCard("The Rat", (1, 5), "Characters/Rat.png", 50),
    EnemyCard("The Ranger", (5, 10), "Characters/Ranger.png", 50),
]

enemies_effect = [
    EnemyCard("The Zombie", (5, 15), "Characters/Zombie.png", 70),
    EnemyCard("The Mermaid", (5, 15), "Characters/Mermaid.png", 70),
    EnemyCard("The Ghost", (5, 15), "Characters/Ghost.png", 70),
]

enemies_magic = [
    EnemyCard("The Magician", (7, 12), "Characters/Magician1.png", 80),
    EnemyCard("The Magician 2", (7, 12), "Characters/Magician2.png", 90),
    EnemyCard("The Magician 3", (7, 12), "Characters/Magician3.png", 100),
]

friend_mage = EnemyCard("The Mage", (0, 0), "Characters/Mage.png", 0)

enemies_tank = [
    EnemyCard("The Knight", (15, 25), "Characters/Knight.png", 120),
    EnemyCard("The Monk", (15, 25), "Characters/Monk.png", 120),
    EnemyCard("The Robot", (15, 25), "Characters/Robot.png", 120),
    EnemyCard("The Culturist", (15, 25), "Characters/Culturist.png", 120),
]

enemies_boss = [
    EnemyCard("The Dragon", (20, 25), "Characters/Dragon.png", 200),
    EnemyCard("The Necromancer", (20, 25), "Characters/Necromancer.png", 250),
]

# Group order
enemy_groups = [enemies_light, enemies_effect, enemies_magic, [friend_mage], enemies_tank, enemies_boss]
current_group_index = 0
current_enemy_index = 0

# Combat log
combat_log = []

def add_to_combat_log(message):
    global combat_log
    combat_log.append(message)
    if len(combat_log) > 5:
        combat_log.pop(0)

def draw_combat_log(font):
    y = HEIGHT - 60
    x = WIDTH - 600
    for message in reversed(combat_log):  # Display 5 last messages from newest to oldest
        draw_text(message, font, ORANGE, x, y)
        y -= 30
        x -= 10

# Helper functions
def draw_text(text, font, color, x, y):
    text_obj = font.render(text, True, color)
    screen.blit(text_obj, (x, y))

def reset_combat():
    global current_enemy_index, current_background_index, current_sound_index, player, magic_uses_left
    current_enemy_index = 0
    current_background_index += 1
    magic_uses_left = 3  # Reset magic uses count at 3 uses when changing class of enemy
    if current_background_index < len(backgrounds):
        player.hp = player.max_hp  # Reset player HP to max
        sounds[current_sound_index].stop()
        current_sound_index = current_background_index
        sounds[current_sound_index].play(-1)  # Loop the next sound
    player.heal_count = 0

    if current_group_index < len(enemy_groups) - 1 and enemy_groups[current_group_index] == [friend_mage]:
        player.image = pygame.transform.scale(pygame.image.load("Characters/Hero2.png"), (300, 400))
        player.hp = 250
        player.max_hp = 250
        player.damage_range = (20, 30)


def game_over():
    global current_background_index, current_sound_index
    current_background_index = len(backgrounds) - 1  # Game Over background
    if sounds[current_sound_index].get_num_channels() > 0:
        sounds[current_sound_index].stop()  # Stop any currently playing sound
    current_sound_index = len(sounds) - 1  # Index for Game Over sound
    sounds[current_sound_index].play(-1)  # Loop the Game Over sound


# Main loop
running = True
font = pygame.font.SysFont(None, 40)
player_turn = True

while running:
    screen.blit(backgrounds[current_background_index], (0, 0))

    if current_group_index >= len(enemy_groups):  # End screen
        draw_text("Press ESC to quit", font, RED, WIDTH // 2 - 100, HEIGHT // 2)
    elif player.hp <= 0:  # Game Over
        game_over()
        draw_text("GAME OVER! Press ESC to quit.", font, RED, WIDTH // 2 - 150, HEIGHT // 2)
    else:
        current_group = enemy_groups[current_group_index]
        enemy = current_group[current_enemy_index]

        # Display player and enemy info
        draw_text(f"HP Hero: {player.hp}/{player.max_hp}", font, BLUE, 20, 20)
        draw_text(f"HP Enemy: {enemy.name} - HP: {enemy.hp}/{enemy.max_hp}", font, RED, 20, 80)

        # Draw enemy card
        screen.blit(enemy.image, (WIDTH - enemy.image.get_width() - 20, 20))

        # Draw player card
        screen.blit(player.image, (20, HEIGHT - player.image.get_height() - 20))

        # Draw combat log
        draw_combat_log(font)

        # Draw options near player's card
        options_x = 20 + player.image.get_width() + 20
        options_y = HEIGHT - player.image.get_height() + 270
        draw_text("1: Attack", font, GREEN, options_x, options_y)
        draw_text("2: Magic", font, GREEN, options_x, options_y + 40)
        draw_text("3: Items", font, GREEN, options_x, options_y + 80)

        if not player_turn:
            pygame.time.wait(1500)  # Delay for enemy attack
            damage = enemy.deal_damage()
            player.hp = max(player.hp - damage, 0)
            add_to_combat_log(f"Enemy dealt {damage} damage!")
            player_turn = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if player_turn and player.hp > 0:
                if event.key == pygame.K_1:  # Attack
                    damage = player.deal_damage()
                    enemy.hp = max(enemy.hp - damage, 0)
                    add_to_combat_log(f"You dealt {damage} damage!")
                    if enemy.hp <= 0:
                        add_to_combat_log(f"You defeated {enemy.name}!")
                        current_enemy_index += 1
                        if current_enemy_index >= len(current_group):
                            current_group_index += 1
                            reset_combat()
                    player_turn = False
                elif event.key == pygame.K_3:  # Use Potion
                    if player.heal_count < 80:
                        heal = random.randint(60, 80)
                        player.hp = min(player.hp + heal, player.max_hp)
                        player.heal_count += 1
                        add_to_combat_log(f"You healed {heal} HP!")
                    else:
                        add_to_combat_log("No potions left!")
                    player_turn = False
                elif event.key == pygame.K_2:  # Magic attack
                    if magic_uses_left > 0:
                        magic_damage = random.randint(25, 35)
                        enemy.hp = max(enemy.hp - magic_damage, 0)
                        magic_uses_left -= 1
                        add_to_combat_log(f"You cast Magic and dealt {magic_damage} damage!")
                        if enemy.hp <= 0:
                            add_to_combat_log(f"You defeated {enemy.name}!")
                            current_enemy_index += 1
                            if current_enemy_index >= len(current_group):
                                current_group_index += 1
                                reset_combat()
                        player_turn = False
                    else:
                        add_to_combat_log("No magic uses left!")

    pygame.display.flip()

# Stop all sounds and quit Pygame properly
pygame.mixer.stop()
pygame.quit()
sys.exit()
