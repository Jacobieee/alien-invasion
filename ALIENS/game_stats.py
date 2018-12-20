class GameStats():
    # info of game stats.
    def __init__(self, ai_settings):
        self.ai_settings = ai_settings
        self.reset_stats()
        # when the game begins the status is "inactive".
        self.game_active = False
        # sore highest score.
        self.high_score = 0


    def reset_stats(self):
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0

        