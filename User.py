import constants


class User:
    def __init__(self, name='', score=0, lives=constants.LIVES):
        self.name = name
        self.score = score
        self.lives = lives

    def update_score(self, new_score):
        self.score = new_score

    def increase_score(self, increase):
        self.score += increase
