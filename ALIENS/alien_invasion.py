import sys
import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
from alien import Alien
import game_functions as gf
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

def run_game():
    # initialise the game and the interface
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # create the "play" button.
    play_button = Button(ai_settings, screen, "Play")

    # store the info of game stats and the scxore board.
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # set back ground colour
    bg_color = (230,230,230)

    #create the ship on the screen.
    ship = Ship(screen, ai_settings)
    #store the bullets.
    bullets = Group()
    # store the aliens.
    aliens = Group()
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # create an alien.
    alien = Alien(ai_settings, screen)


    # start the loop of the game
    while True:
        # check events.
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)
        if stats.game_active:
                ship.update()
                gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
                gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets)

        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)

run_game()

