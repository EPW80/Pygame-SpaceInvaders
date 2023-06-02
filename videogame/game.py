# Erik Williams
# CPSC 386-02
# 2023-04-20
# epwilliams@csu.fullerton.edu
# @EPW80
#
# Lab 05-00
#
# This is a pygame project!
#

"""Main game loop"""
import pygame

from alien import Alien
from player import Player
from obstacle import Obstacle
from score_manager import from_file, save_score_to_pickle

pygame.init()
pygame.mixer.init()

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Invaders")

FPS = 60
clock = pygame.time.Clock()

ASSETS_PATH = "videogame/data/space_invaders_assets/space_invaders_assets/"


class GameSounds:
    """Class to play sounds"""

    def __init__(self, assets_path):
        self.new_round_sound = pygame.mixer.Sound(assets_path + "new_round.wav")
        self.breach_sound = pygame.mixer.Sound(assets_path + "breach.wav")
        self.alien_hit_sound = pygame.mixer.Sound(assets_path + "alien_hit.wav")
        self.player_hit_sound = pygame.mixer.Sound(assets_path + "player_hit.wav")

    def play_new_round_sound(self):
        """Play new round sound"""
        self.new_round_sound.play()

    def play_breach_sound(self):
        """Play breach sound"""
        self.breach_sound.play()

    def play_alien_hit_sound(self):
        """Play alien hit sound"""
        self.alien_hit_sound.play()

    def play_player_hit_sound(self):
        """Play player hit sound"""
        self.player_hit_sound.play()


class SpriteGroups:
    """Class to group sprites"""

    def __init__(self, sprite_groups):
        self.groups = sprite_groups
        self.player = sprite_groups["player"]
        self.alien_group = sprite_groups["alien_group"]
        self.player_bullet_group = sprite_groups["player_bullet_group"]
        self.alien_bullet_group = sprite_groups["alien_bullet_group"]
        self.obstacle_group = sprite_groups["obstacle_group"]

    def add_to_group(self, group_name, sprite):
        """Add a sprite to a specific group"""
        self.groups[group_name].add(sprite)

    def get_all_sprites(self):
        """Return all sprites as a list"""
        return [
            self.player,
            self.alien_group,
            self.player_bullet_group,
            self.alien_bullet_group,
            self.obstacle_group,
        ]


class Game:
    """A class to help control and update gameplay"""

    def __init__(self, sprites, assets_path, display_surf):
        """Initialize the game"""
        pygame.init()
        self.sprites = sprites
        self.round_number = 1
        self.score = 0
        self.sounds = GameSounds(assets_path)
        self.font = pygame.font.Font(assets_path + "Facon.ttf", 32)
        self.last_created_alien = None
        self.bg_image = pygame.image.load(ASSETS_PATH + "spaceback.png")
        self.bg_image = pygame.transform.scale(
            self.bg_image, (WINDOW_WIDTH, WINDOW_HEIGHT)
        )
        self.display_surface = display_surf
        self.start_new_round()

    def update(self):
        """Update the game"""
        self.shift_aliens()
        self.check_collisions()
        self.check_round_completion()
        self.check_collisions()

    def draw(self):
        """Draw the HUD and other information to display"""
        self.display_surface.blit(self.bg_image, (0, 0))

        white = (255, 255, 255)

        score_text = self.font.render("Score: " + str(self.score), True, white)
        score_rect = score_text.get_rect()
        score_rect.centerx = WINDOW_WIDTH // 2
        score_rect.top = 10

        round_text = self.font.render("Round: " + str(self.round_number), True, white)
        round_rect = round_text.get_rect()
        round_rect.topleft = (20, 10)

        lives_text = self.font.render(
            "Lives: " + str(self.sprites["player"].lives), True, white
        )
        lives_rect = lives_text.get_rect()
        lives_rect.topright = (WINDOW_WIDTH - 20, 10)

        self.display_surface.blit(self.bg_image, (0, 0))  # draw the background image
        self.display_surface.blit(score_text, score_rect)
        self.display_surface.blit(round_text, round_rect)
        self.display_surface.blit(lives_text, lives_rect)
        pygame.draw.line(display_surface, white, (0, 50), (WINDOW_WIDTH, 50), 4)
        pygame.draw.line(
            display_surface,
            white,
            (0, WINDOW_HEIGHT - 100),
            (WINDOW_WIDTH, WINDOW_HEIGHT - 100),
            4,
        )

    def shift_aliens(self):
        """Shift a wave of aliens down the screen and reverse direction"""
        shift = False
        for alien in self.sprites["alien_group"].sprites():
            if alien.rect.left <= 0 or alien.rect.right >= WINDOW_WIDTH:
                shift = True
        if shift:
            breach = False
            for alien in self.sprites["alien_group"].sprites():
                alien.rect.y += 10 * self.round_number
                alien.direction = -1 * alien.direction
                alien.rect.x += alien.direction * alien.velocity
                if alien.rect.bottom >= WINDOW_HEIGHT - 100:
                    breach = True
            if breach:
                self.sounds.breach_sound.play()
                self.sprites.player.lives -= 1
                self.check_game_status(
                    "Aliens breached the line!", "Press 'Enter' to continue"
                )

    def check_collisions(self):
        """Check for collisions"""
        if pygame.sprite.groupcollide(
            self.sprites["player_bullet_group"], self.sprites["alien_group"], True, True
        ):
            self.sounds.alien_hit_sound.play()
            self.score += 100

        for bullet in self.sprites["player_bullet_group"].sprites():
            collided_obstacles = pygame.sprite.spritecollide(
                bullet, self.sprites["obstacle_group"], False
            )
            if collided_obstacles:
                bullet.kill()

        if pygame.sprite.spritecollide(
            self.sprites["player"], self.sprites["alien_bullet_group"], True
        ):
            self.sounds.player_hit_sound.play()
            self.sprites["player"].lives -= 1
            self.check_game_status("You've been hit!", "Press 'Enter' to continue")

        if pygame.sprite.spritecollide(
            self.sprites["player"], self.sprites["obstacle_group"], False
        ):
            self.sounds.player_hit_sound.play()
            self.sprites["player"].lives -= 1
            self.check_game_status(
                "You collided with an obstacle!", "Press 'Enter' to continue"
            )

    def check_round_completion(self):
        """Check to see if a player has completed a single round"""
        if not self.sprites["alien_group"] and self.round_number > 0:
            self.score += 1000 * self.round_number
            self.round_number += 1
            self.start_new_round()

    def start_new_round(self):
        """Start a new round"""
        for i in range(9):
            for j in range(5):
                alien = Alien(
                    64 + i * 64,
                    64 + j * 64,
                    self.round_number,
                    self.sprites["alien_bullet_group"],
                )
                self.sprites["alien_group"].add(alien)
                self.last_created_alien = alien

        for obstacle in self.sprites["obstacle_group"]:
            obstacle.reset()

        self.sounds.new_round_sound.play()
        self.pause_game(
            "Space Invaders Round " + str(self.round_number), "Press 'Enter' to begin"
        )

    def check_game_status(self, main_text, sub_text):
        """Check to see the status of the game and how the player died"""
        self.sprites["alien_bullet_group"].empty()
        self.sprites["player_bullet_group"].empty()
        self.sprites["player"].reset()
        for alien in self.sprites["alien_group"]:
            alien.reset()

        if self.sprites["player"].lives == 0:
            self.reset_game()
        else:
            self.pause_game(main_text, sub_text)

    def pause_game(self, main_text, sub_text):
        """Pauses the game"""
        white = (255, 255, 255)
        black = (0, 0, 0)

        main_text = self.font.render(main_text, True, white)
        main_rect = main_text.get_rect()
        main_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

        sub_text = self.font.render(sub_text, True, white)
        sub_rect = sub_text.get_rect()
        sub_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 64)

        display_surface.fill(black)
        display_surface.blit(main_text, main_rect)
        display_surface.blit(sub_text, sub_rect)
        pygame.display.update()

        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        is_paused = False
                if event.type == pygame.QUIT:
                    is_paused = False

    def reset_game(self):
        """Reset the game"""
        self.pause_game(
            "Final Score: " + str(self.score), "Press 'Enter' to play again"
        )

        player_name = "Player 1"
        save_score_to_pickle(player_name, self.score)

        self.score = 0
        self.round_number = 1
        self.sprites["player"].lives = 3
        self.sprites["alien_group"].empty()
        self.sprites["alien_bullet_group"].empty()
        self.sprites["player_bullet_group"].empty()
        self.start_new_round()

    def show_high_scores(self):
        """Shows the high scores"""
        try:
            high_scores = from_file("scores.pkl")
        except FileNotFoundError:
            print("No high scores found")

        for player in high_scores:
            print(f"{player.player_name}: {player.score}")


def main():
    """Main function"""
    my_player_bullet_group = pygame.sprite.Group()
    my_alien_bullet_group = pygame.sprite.Group()

    my_player_group = pygame.sprite.Group()
    my_player = Player(my_player_bullet_group, "Player 1", 0)
    my_player_group.add(my_player)

    my_alien_group = pygame.sprite.Group()

    my_obstacle_group = pygame.sprite.Group()
    obstacle1 = Obstacle(100, 100, 2)
    obstacle2 = Obstacle(WINDOW_WIDTH - 100, 100, 2)
    my_obstacle_group.add(obstacle1, obstacle2)

    sprites = {
        "player": my_player,
        "alien_group": my_alien_group,
        "player_bullet_group": my_player_bullet_group,
        "alien_bullet_group": my_alien_bullet_group,
        "obstacle_group": my_obstacle_group,
    }

    my_game = Game(sprites, ASSETS_PATH, display_surface)

    all_sprites_groups = [
        my_player_group,
        my_alien_group,
        my_player_bullet_group,
        my_alien_bullet_group,
        my_obstacle_group,
    ]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    my_player.fire()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    my_game.show_high_scores()
                if event.key == pygame.K_ESCAPE:
                    running = False

        display_surface.fill((0, 0, 0))

        for group in all_sprites_groups:
            group.update()
            group.draw(display_surface)

        my_game.draw()

        for group in all_sprites_groups:
            group.update()
            group.draw(display_surface)

        my_game.update()

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
