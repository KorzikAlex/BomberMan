import pygame
import os
import sys
import random


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]

        self.left = 10
        self.top = 10
        self.cell_size = 38
        self.state = True

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        if self.state:
            for i in range(self.height):
                for j in range(self.width):
                    if j == 0:
                        self.board[i][j] = 1
                    if j == self.width - 1:
                        self.board[i][j] = 1
                    if i == 0 and j != 0:
                        self.board[i][j] = 1
                    if i == self.height - 1 and j != 0:
                        self.board[i][j] = 1
                    if i % 2 == 0 and j % 2 == 0:
                        self.board[i][j] = 1
                    if self.board[i][j] == 1:
                        sprite2 = Box()
                        sprite2.change_xy(self.left + (self.cell_size * i), self.top + (self.cell_size * j))
                        box.add(sprite2)
            last = 0
            not_cords = [(1, 1), (1, 2), (2, 1), (3, 1), (1, 3)]

            a = []

            for _ in range(5):
                cords = random.randrange(1, self.width - 1, 1), random.randrange(1, self.height - 1, 1)
                while cords == last or cords in not_cords or self.board[cords[0]][cords[1]] != 0:
                    cords = random.randrange(0, self.width, 1), random.randrange(0, self.height, 1)
                self.board[cords[0]][cords[1]] = 2
                last = cords

                a.append(cords)
            cord_door = random.choice(a)
            self.board[cord_door[0]][cord_door[1]] = 4

            for i in range(self.height):
                for j in range(self.width):
                    if self.board[i][j] == 2:
                        sprite2 = Wall()
                        sprite2.change_xy(self.left + (self.cell_size * i), self.top + (self.cell_size * j))
                        wall.add(sprite2)

                    if self.board[i][j] == 4:
                        sprite2 = Wall()
                        sprite2.change_xy(self.left + (self.cell_size * i), self.top + (self.cell_size * j))
                        wall.add(sprite2)

            self.state = False
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] == 0:
                    pygame.draw.rect(screen, "skyblue", (self.left + (self.cell_size * i),
                                                         self.top + (self.cell_size * j),
                                                         self.cell_size, self.cell_size), width=1)
                if self.board[i][j] == 1:
                    box.draw(screen)

                if self.board[i][j] == 2 or self.board[i][j] == 4:
                    wall.draw(screen)
                if self.board[i][j] == 5:
                    door.draw(screen)
                if self.board[i][j] == 2:
                    wall.draw(screen)

    def on_click(self, cell_coords):
        if cell_coords is None:
            return None
        x, y = cell_coords
        return self.board[x][y]

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        pos_x = (x - self.left) // self.cell_size
        pos_y = (y - self.top) // self.cell_size
        if -1 < pos_x < self.width and -1 < pos_y < self.width:
            return pos_x, pos_y
        return None

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)
        return self.on_click(cell)

    def get_info(self):
        return self.left, self.top, self.cell_size, self.width, self.height

    def state_of_sell(self, cords):
        return self.board[cords[0]][cords[1]]

    def change_state_cell(self, cords, state):
        self.board[cords[0]][cords[1]] = state


class Box(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(group)
        self.image = load_image("box.png")
        self.size = board.get_info()[2]
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = self.image.get_rect()

    def update(self, *args, **kwargs):
        pass

    def change_xy(self, x, y):
        self.rect.x = x
        self.rect.y = y


class Wall(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(group)
        self.image = load_image("wall.png")
        self.size = board.get_info()[2]
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = self.image.get_rect()

    def update(self, *args, **kwargs):
        pass

    def change_xy(self, x, y):
        self.rect.x = x
        self.rect.y = y


class Bomberman(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(group)
        self.size = board.get_info()[2]
        self.speed = 15
        self.image = load_image("bomberman.png")
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = self.image.get_rect()
        self.rect.x = self.size + board.get_info()[0]
        self.rect.y = self.size + board.get_info()[1]

    def up(self):
        global running, text_message
        if board.get_click([self.rect.x, self.rect.y - self.size]) == 0:
            self.rect.y -= self.size
        elif board.get_click([self.rect.x, self.rect.y - self.size]) == 5:
            text_message = 'ВЫ ПОБЕДИЛИ!!!'
            running = False

    def down(self):
        global running, text_message
        if board.get_click([self.rect.x, self.rect.y + self.size]) == 0:
            self.rect.y += self.size
        elif board.get_click([self.rect.x, self.rect.y + self.size]) == 5:
            text_message = 'ВЫ ПОБЕДИЛИ!!!'
            running = False

    def right(self):
        global running, text_message
        if board.get_click([self.rect.x + self.size, self.rect.y]) == 0:
            self.rect.x += self.size
        elif board.get_click([self.rect.x + self.size, self.rect.y]) == 5:
            text_message = 'ВЫ ПОБЕДИЛИ!!!'
            running = False

    def left(self):
        global running, text_message
        if board.get_click([self.rect.x - self.size, self.rect.y]) == 0:
            self.rect.x -= self.size
        elif board.get_click([self.rect.x - self.size, self.rect.y]) == 5:
            text_message = 'ВЫ ПОБЕДИЛИ!!!'
            running = False

    def position(self):
        return self.rect.x, self.rect.y


class Bomb(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(group)
        self.size = board.get_info()[2]
        self.image = load_image('bomb.png')
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = self.image.get_rect()

    def change(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def boom(self):
        cell1 = board.get_cell((self.rect.x + self.size, self.rect.y))
        cell2 = board.get_cell((self.rect.x - self.size, self.rect.y))
        cell3 = board.get_cell((self.rect.x, self.rect.y + self.size))
        cell4 = board.get_cell((self.rect.x, self.rect.y - self.size))
        for sprite in wall:
            if self.rect.x + self.size == sprite.rect.x and self.rect.y == sprite.rect.y \
                    and board.state_of_sell(cell1) == 2:
                board.change_state_cell(cell1, 0)
                sprite.kill()
            elif self.rect.x + self.size == sprite.rect.x and self.rect.y == sprite.rect.y \
                    and board.state_of_sell(cell1) == 4:
                board.change_state_cell(cell4, 5)
                sprite4 = Door()
                sprite4.change(sprite.rect.x, sprite.rect.y)
                wall.add(sprite4)
                sprite.kill()
            elif self.rect.x - self.size == sprite.rect.x and self.rect.y == sprite.rect.y \
                    and board.state_of_sell(cell2) == 2:
                board.change_state_cell(cell2, 0)
                sprite.kill()
            elif self.rect.x - self.size == sprite.rect.x and self.rect.y == sprite.rect.y \
                    and board.state_of_sell(cell2) == 4:
                board.change_state_cell(cell4, 5)
                sprite4 = Door()
                sprite4.change(sprite.rect.x, sprite.rect.y)
                wall.add(sprite4)
                sprite.kill()
            elif self.rect.x == sprite.rect.x and self.rect.y + self.size == sprite.rect.y \
                    and board.state_of_sell(cell3) == 2:
                board.change_state_cell(cell3, 0)
                sprite.kill()
            elif self.rect.x == sprite.rect.x and self.rect.y + self.size == sprite.rect.y \
                    and board.state_of_sell(cell3) == 4:
                board.change_state_cell(cell3, 5)
                sprite4 = Door()
                sprite4.change(sprite.rect.x, sprite.rect.y)
                wall.add(sprite4)
                sprite.kill()
            elif self.rect.x == sprite.rect.x and self.rect.y - self.size == sprite.rect.y \
                    and board.state_of_sell(cell4) == 2:
                board.change_state_cell(cell4, 0)
                sprite.kill()
            elif self.rect.x == sprite.rect.x and self.rect.y - self.size == sprite.rect.y \
                    and board.state_of_sell(cell4) == 4:
                board.change_state_cell(cell4, 5)
                sprite4 = Door()
                sprite4.change(sprite.rect.x, sprite.rect.y)
                wall.add(sprite4)
                sprite.kill()


class Door(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(group)
        self.size = board.get_info()[2]
        self.image = load_image('door.png')
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = self.image.get_rect()

    def change(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def boom(self):
        cell1 = board.get_cell((self.rect.x + self.size, self.rect.y))
        cell2 = board.get_cell((self.rect.x - self.size, self.rect.y))
        cell3 = board.get_cell((self.rect.x, self.rect.y + self.size))
        cell4 = board.get_cell((self.rect.x, self.rect.y - self.size))
        for sprite in wall:
            if self.rect.x + self.size == sprite.rect.x and self.rect.y == sprite.rect.y \
                    and board.state_of_sell(cell1) == 2:
                board.change_state_cell(cell1, 0)
                sprite.kill()
            elif self.rect.x - self.size == sprite.rect.x and self.rect.y == sprite.rect.y \
                    and board.state_of_sell(cell2) == 2:
                board.change_state_cell(cell2, 0)
                sprite.kill()
            elif self.rect.x == sprite.rect.x and self.rect.y + self.size == sprite.rect.y \
                    and board.state_of_sell(cell3) == 2:
                board.change_state_cell(cell3, 0)
                sprite.kill()
            elif self.rect.x == sprite.rect.x and self.rect.y - self.size == sprite.rect.y \
                    and board.state_of_sell(cell4) == 2:
                board.change_state_cell(cell4, 0)
                sprite.kill()


if __name__ == '__main__':
    pygame.init()
    size = 750, 750

    BOMB_TIMER = pygame.USEREVENT + 1
    TIMER = pygame.USEREVENT + 2
    pygame.time.set_timer(TIMER, 200 * 1000)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('BOMBERMAN v 0.7')

    pygame.display.set_icon(pygame.image.load('data/bomb.png'))
    screen.fill("SKYBLUE")

    running = True
    drawing = True
    clock = pygame.time.Clock()

    board = Board(19, 19)

    sprite1 = Bomberman()
    bomberman = pygame.sprite.Group()
    bomberman.add(sprite1)

    box = pygame.sprite.Group()
    wall = pygame.sprite.Group()
    bomb = pygame.sprite.Group()
    door = pygame.sprite.Group()
    text_message = ''
    while running:
        tick = clock.tick()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    sprite1.left()
                if event.key == pygame.K_UP:
                    sprite1.up()
                if event.key == pygame.K_DOWN:
                    sprite1.down()
                if event.key == pygame.K_RIGHT:
                    sprite1.right()
                if event.key == pygame.K_w:
                    sprite1.up()
                if event.key == pygame.K_a:
                    sprite1.left()
                if event.key == pygame.K_s:
                    sprite1.down()
                if event.key == pygame.K_d:
                    sprite1.right()
                if event.key == pygame.K_SPACE:
                    if drawing:
                        sprite3 = Bomb()
                        sprite3.change(sprite1.position()[0], sprite1.position()[1])
                        cord = board.get_cell((sprite1.position()[0], sprite1.position()[1]))
                        board.change_state_cell(cord, 3)
                        bomb.add(sprite3)
                        pygame.time.set_timer(BOMB_TIMER, 4000)
                        drawing = False
            if event.type == BOMB_TIMER:
                sprite3.boom()
                bomb.empty()
                board.change_state_cell(cord, 0)
                pygame.time.set_timer(BOMB_TIMER, 0)
                drawing = True
            if event.type == TIMER:
                text_message = 'ВРЕМЯ ВЫШЛО :('
                running = False
        screen.fill("skyblue")
        bomberman.draw(screen)
        bomb.draw(screen)
        board.render(screen)
        pygame.display.flip()
    pygame.quit()
    print(text_message)
