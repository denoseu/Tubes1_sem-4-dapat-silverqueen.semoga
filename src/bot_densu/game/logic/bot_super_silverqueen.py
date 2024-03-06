import random
from typing import Optional, List

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction

def calculate_distance(position1, position2):
    return ((position1.x - position2.x) ** 2 + (position1.y - position2.y) ** 2) ** 0.5

@property
def diamonds(self) -> List[GameObject]:
    return [d for d in self.game_objects if d.type == "TeleportGameObject"]

class NormalSilverqueen(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0

    def find_teleport_gameobject(self, board: Board) -> Optional[Position]:
        teleport_objects = [obj for obj in board.game_objects if obj.type == "TeleportGameObject"]
        if teleport_objects:
            return teleport_objects[0].position
        else:
            return None


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
        # for bot in bots:
        #     if bot != board_bot:
        #         temp_distance = calculate_distance(bot.position, board_bot.position)
        #         if temp_distance <= 1:
        #             temp_delta_x = bot.position.x - board_bot.position.x
        #             temp_delta_y = bot.position.y - board_bot.position.y
        #             # If adjacent, move away
        #             return -temp_delta_x, -temp_delta_y
        for bot in bots:
            if bot != board_bot:
                temp_distance = calculate_distance(bot.position, board_bot.position)
                if temp_distance <= 1:
                    temp_delta_x = bot.position.x - board_bot.position.x
                    temp_delta_y = bot.position.y - board_bot.position.y
                    # jika bersebelahan, lakukan pengecekan untuk menentukan arah gerakan
                    if temp_delta_x == 0:  # berada di atas atau bawah
                        # cek ada bot lawan di sebelah kanan atau kiri ato ngga
                        for opponent_bot in bots:
                            if opponent_bot != board_bot and opponent_bot != bot:
                                if abs(opponent_bot.position.x - bot.position.x) == 1 and opponent_bot.position.y == bot.position.y:
                                    # jika ada bot lawan di sebelah kanan atau kiri, arahkan untuk bergerak ke atas atau bawah
                                    return 0, -temp_delta_y
                    elif temp_delta_y == 0:  # berada di kanan atau kiri
                        # cek ada bot lawan di atas atau bawah
                        for opponent_bot in bots:
                            if opponent_bot != board_bot and opponent_bot != bot:
                                if abs(opponent_bot.position.y - bot.position.y) == 1 and opponent_bot.position.x == bot.position.x:
                                    # jika ada bot lawan di atas atau bawah, arahkan untuk bergerak ke kanan atau kiri
                                    return temp_delta_x, 0
                    else:
                        # jika tidak berada di atas, bawah, kiri, atau kanan, maka pilih arah yang berlawanan untuk menjauh
                        return -temp_delta_x, -temp_delta_y

        # lokasi teleport game object
        teleport_position = self.find_teleport_gameobject(board)
        if teleport_position:
            print("teleporter location:", teleport_position)

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
                    delta_y = random.choice([-1, 0, 1]) # biar bisa vertikal
            return delta_x, delta_y