import sys
import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
from alien import Alien
import game_functions as gf
from game_stats import GameStats

def run_game():
    # initialise the game and the interface
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # store the info of game stats.
    stats = GameStats(ai_settings)

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
        gf.check_events(ship, ai_settings, screen, bullets)
        if stats.game_active:
                ship.update()
                gf.update_bullets(ai_settings, screen, ship, aliens, bullets)
                gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets)
                
        gf.update_screen(ai_settings, screen, ship, aliens, bullets)

run_game()

