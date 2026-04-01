class Food:
    def __init__(self, position):
        self.position = position

    def apply_effect(self, snake):
        pass


class NormalFood(Food):
    type = "normal"
    points = 10

    def apply_effect(self, snake):
        snake.grow(1)


class GoldenFood(Food):
    type = "big"
    points = 25

    def __init__(self, position):
        super().__init__(position)
        self.timer = 4

    def update(self, deltatime):
        self.timer -= deltatime
        return self.time > 0 

    def apply_effect(self, snake):
        snake.grow(5)


class ShrinkFood(Food):
    type = "shrink"
    points = 0

    def apply_effect(self, snake):
        snake.shrink(1)


class SpeedFood(Food):
    type = "speed"
    points = 5

    def apply_effect(self, snake):
        snake.boost(10)