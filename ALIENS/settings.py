class Settings():

    def __init__(self):

        # set screen
        self.screen_width = 1000
        self.screen_height = 750
        self.bg_color = (230,230,230)

        # set the ship.
        self.ship_limit = 3
        
        # set bullets.
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60,60,60
        self.bullets_allowed = 9

        # set aliens.
        self.fleet_drop_speed = 20

        # speed of change of difficulty.
        self.speedup_scale = 1.1
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        # initialization goes with game process.
        self.ship_speed_factor = 3.0
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        # to right if fleet_direction is 1, go left if it's -1.
        self.fleet_direction = 1
        # track score.
        self.alien_points = 50

    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale 
        self.bullet_speed_factor *= self.speedup_scale 
        self.alien_speed_factor *= self.speedup_scale