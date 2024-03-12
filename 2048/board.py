import pygame
import random

pygame.init()

colors = {0: (204, 192, 179),
          2: (238, 228, 218),
          4: (237, 224, 200),
          8: (242, 177, 121),
          16: (245, 149, 99),
          32: (246, 124, 95),
          64: (246, 94, 59),
          128: (237, 207, 114),
          256: (237, 204, 97),
          512: (237, 200, 80),
          1024: (237, 197, 63),
          2048: (237, 194, 46),
          'light text': (249, 246, 242),
          'dark text': (119, 110, 101),
          'other': (0, 0, 0),
          'bg': (187, 173, 160)}
font = pygame.font.Font(pygame.font.get_default_font(), 24)
hint_font = pygame.font.Font(pygame.font.get_default_font(), 16)
title_font = pygame.font.Font(pygame.font.get_default_font(), 60)


def draw_game_over(screen):
    pygame.draw.rect(screen, 'black', [50, 50, 300, 100], 0, 10)
    game_over_text = font.render('GAME OVER', True, 'white')
    screen.blit(game_over_text, (130, 65))


class Board:
    def __init__(self, score):
        self.board_values = [[0 for _ in range(4)] for _ in range(4)]
        self.score = score
        self.hint = ''
        self.tiles_coordinates = [[(0, 0) for _ in range(4)] for _ in range(4)]
        self.block_size = 0

    def draw_board(self, width, height, screen, direction=''):
        # global colors
        pygame.draw.rect(screen, colors['bg'], [0, 0, height - 100, width], 0, 20)
        score_text = font.render(f'Score: {self.score}', True, 'black')
        screen.blit(score_text, (10, height - 90))
        hint_text = hint_font.render(direction, True, 'black')
        screen.blit(hint_text, (130, height - 40))

    def random_piece(self):
        if any(0 in row for row in self.board_values):
            placed = False
            while not placed:
                row = random.randint(0, 3)
                col = random.randint(0, 3)
                if self.board_values[row][col] == 0:
                    if random.randint(0, 9) < 1:  # 10% chance of 4 spawn
                        self.board_values[row][col] = 4
                    else:
                        self.board_values[row][col] = 2
                    placed = True
            return False
        return self.check_game_over()

    def clear_board_values(self):
        self.board_values = [[0 for _ in range(4)] for _ in range(4)]

    def check_game_over(self):
        for row in self.board_values:
            for col in range(len(row) - 1):
                if row[col] == row[col + 1]:
                    return False
        for col in range(len(self.board_values[0])):
            for row in range(len(self.board_values) - 1):
                if self.board_values[row][col] == self.board_values[row + 1][col]:
                    return False
        return True

    def draw_pieces(self, width, screen):
        for i in range(len(self.board_values)):
            for j in range(len(self.board_values[0])):
                value = self.board_values[i][j]
                if value > 8:
                    value_color = colors['light text']  # using light font for dark tiles
                else:
                    value_color = colors['dark text']
                if value <= 2048:
                    color = colors[value]
                else:
                    color = colors['other']
                space = (width * 0.25) / 5  # space between tiles
                tile = (width * 0.75) / 4  # tile_width
                self.block_size = tile
                left = j * (tile + space) + space  # upper tile coordinate
                up = i * (tile + space) + space  # lower tile coordinate

                self.tiles_coordinates[i][j] = (left, up)  # needed to check which tile was clicked (multiplayer mode)
                pygame.draw.rect(screen, color, [left, up, tile, tile], 0, 5)

                if value > 0:  # for value 0 we do not display text
                    value_len = len(str(value))
                    value_font = pygame.font.Font(pygame.font.get_default_font(),
                                                  48 - (
                                                              5 * value_len))  # shrinking the font with the length of the text
                    value_text = value_font.render(str(value), True, value_color)
                    text_rect = value_text.get_rect(
                        center=(j * (tile + space) + tile / 2 + space, i * (
                                tile + space) + tile / 2 + space))  # calculation of the position of the text of each tile (its center)
                    screen.blit(value_text, text_rect)

    # (multiplayer mode) function checks if the clicked field  is free - if so, a new block appears there
    def check_place(self, x, y, value):
        for i in range(len(self.board_values)):
            for j in range(len(self.board_values[0])):
                if self.tiles_coordinates[i][j][0] <= x <= self.tiles_coordinates[i][j][0] + self.block_size \
                        and self.tiles_coordinates[i][j][1] <= y <= self.tiles_coordinates[i][j][1] + self.block_size:
                    if self.board_values[i][j] == 0:
                        self.board_values[i][j] = value
                        return True
                    else:
                        return False
        return False

    def move_up(self):
        merged = [[False for _ in range(4)] for _ in range(4)]
        for i in range(1, 4):
            for j in range(4):
                shift = 0
                for k in range(i):
                    if self.board_values[k][j] == 0:
                        shift += 1
                if shift > 0:
                    self.board_values[i - shift][j] = self.board_values[i][j]
                    self.board_values[i][j] = 0
                if i - shift - 1 >= 0 and self.board_values[i - shift - 1][j] == self.board_values[i - shift][j] \
                        and not merged[i - shift - 1][j] and not merged[i - shift][j]:
                    self.board_values[i - shift - 1][j] *= 2
                    self.score += self.board_values[i - shift - 1][j]
                    self.board_values[i - shift][j] = 0
                    merged[i - shift - 1][j] = True

    def move_down(self):
        merged = [[False for _ in range(4)] for _ in range(4)]
        for i in range(2, -1, -1):
            for j in range(4):
                shift = 0
                for k in range(i + 1, 4):
                    if self.board_values[k][j] == 0:
                        shift += 1
                if shift > 0:
                    self.board_values[i + shift][j] = self.board_values[i][j]
                    self.board_values[i][j] = 0
                if i + shift + 1 <= 3 and self.board_values[i + shift + 1][j] == self.board_values[i + shift][j] \
                        and not merged[i + shift + 1][j] and not merged[i + shift][j]:
                    self.board_values[i + shift + 1][j] *= 2
                    self.score += self.board_values[i + shift + 1][j]
                    self.board_values[i + shift][j] = 0
                    merged[i + shift + 1][j] = True

    def move_right(self):
        merged = [[False for _ in range(4)] for _ in range(4)]
        for i in range(4):
            for j in range(2, -1, -1):
                shift = 0
                for k in range(j + 1, 4):
                    if self.board_values[i][k] == 0:
                        shift += 1
                if shift > 0:
                    self.board_values[i][j + shift] = self.board_values[i][j]
                    self.board_values[i][j] = 0
                if j + shift + 1 <= 3 and self.board_values[i][j + shift + 1] == self.board_values[i][j + shift] \
                        and not merged[i][j + shift + 1] and not merged[i][j + shift]:
                    self.board_values[i][j + shift + 1] *= 2
                    self.score += self.board_values[i][j + shift + 1]
                    self.board_values[i][j + shift] = 0
                    merged[i][j + shift + 1] = True

    def move_left(self):
        merged = [[False for _ in range(4)] for _ in range(4)]
        for i in range(4):
            for j in range(1, 4):
                shift = 0
                for k in range(j):
                    if self.board_values[i][k] == 0:
                        shift += 1
                if shift > 0:
                    self.board_values[i][j - shift] = self.board_values[i][j]
                    self.board_values[i][j] = 0
                if j - shift - 1 >= 0 and self.board_values[i][j - shift - 1] == self.board_values[i][j - shift] \
                        and not merged[i][j - shift - 1] and not merged[i][j - shift]:
                    self.board_values[i][j - shift - 1] *= 2
                    self.score += self.board_values[i][j - shift - 1]
                    self.board_values[i][j - shift] = 0
                    merged[i][j - shift - 1] = True

    def take_turn(self, direction):
        if direction == 'UP':
            self.move_up()
        elif direction == 'RIGHT':
            self.move_right()
        elif direction == 'DOWN':
            self.move_down()
        elif direction == 'LEFT':
            self.move_left()
