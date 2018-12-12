class Settings():

    def __init__(self):

        # set screen
        self.screen_width = 1000
        self.screen_height = 750
        self.bg_color = (230,230,230)

        # set the ship.
        self.ship_speed_factor = 1.5
        self.ship_limit = 3
        
        # set bullets.
        self.bullet_speed_factor = 3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60,60,60
        self.bullets_allowed = 5

        # set aliens.
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 10
        # to right if fleet_direction is 1, go left if it's -1.
        self.fleet_direction = 1