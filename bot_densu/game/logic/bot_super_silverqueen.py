import random
from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction

def calculate_distance(position1, position2):
    return ((position1.x - position2.x) ** 2 + (position1.y - position2.y) ** 2) ** 0.5

class SuperSilverqueen(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0

    def find_nearest_diamond(self, board_bot: GameObject, board: Board):
        diamonds = board.diamonds
        if diamonds:
            if board_bot.properties.diamonds == 4:
                # If current diamonds count is 4, try to find blue diamond
                blue_diamonds = [diamond for diamond in diamonds if diamond.properties.points != 2]
                if blue_diamonds:
                    nearest_diamond = min(blue_diamonds, key=lambda diamond: calculate_distance(diamond.position, board_bot.position))
                else:
                    nearest_diamond = min(diamonds, key=lambda diamond: calculate_distance(diamond.position, board_bot.position))
            else:
                nearest_diamond = min(diamonds, key=lambda diamond: calculate_distance(diamond.position, board_bot.position))
            self.goal_position = nearest_diamond.position
        else:
            # No diamonds found, roam around
            self.goal_position = None

    def next_move(self, board_bot: GameObject, board: Board):
        props = board_bot.properties
        bots = board.bots
        diamonds = board.diamonds
        # Check other bots position
        for bot in bots:
            if bot != board_bot:
                temp_distance = calculate_distance(bot.position, board_bot.position)
                if temp_distance <= 1:
                    temp_delta_x = bot.position.x - board_bot.position.x
                    temp_delta_y = bot.position.y - board_bot.position.y
                    # If adjacent, move away
                    return -temp_delta_x, -temp_delta_y

        # Analyze new state
        if props.diamonds == 5:
            # Move to base
            base = board_bot.properties.base
            self.goal_position = base
        else:
            # Find the nearest diamond
            self.find_nearest_diamond(board_bot, board)

        current_position = board_bot.position
        if self.goal_position:
            # We are aiming for a specific position, calculate delta
            delta_x, delta_y = get_direction(
                current_position.x,
                current_position.y,
                self.goal_position.x,
                self.goal_position.y,
            )
        else:
            # Roam around
            delta = self.directions[self.current_direction]
            delta_x = delta[0]
            delta_y = delta[1]
            if random.random() > 0.6:
                self.current_direction = (self.current_direction + 1) % len(
                    self.directions
                )

        if (0 < board_bot.position.x + delta_x < board.width) and (0 < board_bot.position.y + delta_y < board.width):
            return delta_x, delta_y
        else:
            # Adjust movement to stay within board boundaries
            while (delta_x + board_bot.position.x >= board.width) or (delta_x + board_bot.position.x < 0) or (delta_y + board_bot.position.y >= board.width) or (delta_y + board_bot.position.y < 0):
                delta_x = random.randint(-1, 1)
                if delta_x != 0:
                    delta_y = 0
                else:
                    delta_y = random.choice([-1, 1])
            return delta_x, delta_y