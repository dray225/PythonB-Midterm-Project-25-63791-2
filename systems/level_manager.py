class LevelManager:
    def __init__(self):
        self.level = 1

    def update(self, score):
        if score >= 200:
            self.level = 5
        
        elif score >= 150:
            self.level = 4

        elif score >= 100:
            self.level = 3

        elif score >= 50:
            self.level = 2
        
        pass