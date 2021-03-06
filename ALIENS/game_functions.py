import sys
from time import sleep
import pygame

from bullet import Bullet
from alien import Alien

def check_keydown_events(ship, event, ai_settings, screen, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, bullets, ship)
    elif event.key == pygame.K_q:
        sys.exit()

def fire_bullet(ai_settings, screen, bullets, ship):
    # check the number of bullets.
    if len(bullets) < ai_settings.bullets_allowed:
            new_bullet = Bullet(ai_settings, screen, ship)
            bullets.add(new_bullet)

def check_keyup_events(ship, event):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    # react to mouse click and keyboard.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        # if we push down the button.
        elif event.type == pygame.KEYDOWN:
            # then move.
            check_keydown_events(ship, event, ai_settings, screen, bullets)
        # if we loose the button.
        elif event.type == pygame.KEYUP:
            #then stop moving.
            check_keyup_events(ship, event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # reset all game settings.
        ai_settings.initialize_dynamic_settings()
        # hide the mouse.
        pygame.mouse.set_visible(False)
        # reset stats info.
        stats.reset_stats()
        stats.game_active = True
        # reset scoreboard image.
        sb.prep_score()
        sb.prep_high_score() 
        sb.prep_level()
        sb.prep_ships()
        # make aliens and bullets empty.
        aliens.empty()
        bullets.empty()
        # make new aliens and let the ship in the center.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):

    screen.fill(ai_settings.bg_color)

    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    aliens.draw(screen)
    # aliens.blitme()

    # show score.
    sb.show_score()

    # draw the play button when the game is inactive,
    if not stats.game_active:
        play_button.draw_button()

    # make the drawings visible.
    pygame.display.flip()

# update the position of bullets.
def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):

    bullets.update()

    for bullet in bullets.copy():
            if bullet.rect.bottom <= 0:
                    bullets.remove(bullet)
        # print(len(bullets))
   
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    # check if the bullets has collide with the aliens.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    # if collision happens.
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    # if there are no aliens.
    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()
        # then level up.
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)

def get_number_aliens_x(ai_settings, alien_width):
    # calculate how many aliens can be in a row.
    available_space_x = ai_settings.screen_width-2*alien_width
    number_aliens_x = int(available_space_x/(2*alien_width))

    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))

    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    # create an alien.
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    # create an alien and calculate how many aliens can be put in one row.
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # create the first row.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(ai_settings, aliens):
    # when aliens reach the edges.
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    # move aliens downwards and change the direction.
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    if stats.ships_left > 0:
        # minus 1 of ship_left.
        stats.ships_left -= 1
        # update scoreboard.
        sb.prep_ships()
        # make lists of aliens and bullets empty.
        aliens.empty()
        bullets.empty()
        # new game.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        # pause.
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    # check if any one of aliens reaches the bottom.
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # deal with it like collision happens.
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    check_fleet_edges(ai_settings, aliens)
    aliens.update() 
    # check the collision of ship and aliens.
    if pygame.sprite.spritecollideany(ship, aliens):
       ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)  
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)

def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

