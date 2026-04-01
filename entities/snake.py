from game.config import *

class Snake:
    def __init__(self):
        self.length = 1
        self.color = 'green'
        self.multiplier = 1

        self.direction = (1, 0)
        self.pending_growth = 0
        self.remaining_boost_duration = 0
        self.speed = 1
        self.position_list = [(5, 5)]

    def set_direction(self, direction):
        # to prevent turning into itself
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.direction = direction

    def move(self):
        # snake movement logic
        # the first recorded position in the list is the head

        head = self.position_list[0]

        # the next position of the head is calculated

        dx, dy = self.direction

        next_head = (head[0] + (dx), head[1] + (dy))
        
        # to smoothly adjust the snake, the next head is placed in the first slot
        # the rest of the body parts adjust accordingly
        # the last one (tail) is removed, otherwise the snake would grow forever
        # unless of course, there is a growth pending
        
        self.position_list.insert(0, next_head)

        if self.pending_growth > 0:
            self.pending_growth -= 1
        else:
            self.position_list.pop()

    def grow(self, amount):
        self.pending_growth += amount
        self.length += amount

    def shrink(self, amount):

        # if growth is pending, just cancel it in case of shrinking
        # otherwise remove the tail (if tail != head)

        for _ in range(amount):
            if self.pending_growth > 0:
                self.pending_growth -= 1
            elif len(self.position_list) > 1:
                self.position_list.pop()

    def boost(self, duration):
        self.remaining_boost_duration += duration
        self.multiplier = 2
        self.speed = 2
    
    def reset_boost(self):
        self.remaining_boost_duration = 0
        self.multiplier = 1
        self.speed = 1