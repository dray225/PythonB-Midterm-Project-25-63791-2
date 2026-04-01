class Profile:
    def __init__(self, name, high_score=0, max_level=1, food_stats=None):
        self.name = name
        self.high_score = high_score
        self.max_level = max_level
        self.food_stats = food_stats if food_stats else {
            "normal": 0,
            "big": 0,
            "speed": 0,
            "shrink": 0
        }

    def update_high_score(self, score):
        if score > self.high_score:
            self.high_score = score
    
    def update_max_level(self, level):
        if level > self.max_level:
            self.max_level = level
    
    def add_food(self, food_type):
        if food_type in self.food_stats:
            self.food_stats[food_type] += 1

    def apply_game_result(self, score, level, food_type=None):
        self.update_high_score(score)
        self.update_max_level(level)

        if food_type:
            self.add_food(food_type)

    def to_dict(self):
        return {
            "name": self.name,
            "high_score": self.high_score,
            "max_level": self.max_level,
            "food_stats": self.food_stats
        }
    
    @staticmethod
    # just for convenience, to convert JSON data to an object, just a simplified constructor, along with return
    def from_dict(data):
        return Profile(
            name=data["name"],
            high_score=data.get("high_score", 0),
            max_level=data.get("max_level", 1),
            food_stats=data.get("food_stats", {})
        )
