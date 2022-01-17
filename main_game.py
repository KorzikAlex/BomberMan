import pygame
import os
import sys


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
            self.state = False
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] == 0:
                    pygame.draw.rect(screen, "skyblue", (self.left + (self.cell_size * i),
                                                         self.top + (self.cell_size * j),
                                                         self.cell_size, self.cell_size), width=1)
                if self.board[i][j] == 1:
                    box.draw(screen)

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


class Box(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(group)
        self.image = load_image("box.png")
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (38, 38))
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
        self.image = load_image("bomberman.png")
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = self.image.get_rect()
        self.rect.x = self.size + board.get_info()[0]
        self.rect.y = self.size + board.get_info()[1]

    def up(self):
        if board.get_click([self.rect.x, self.rect.y - self.size]) == 0:
            self.rect.y -= self.size

    def down(self):
        if board.get_click([self.rect.x, self.rect.y + self.size]) == 0:
            self.rect.y += self.size

    def right(self):
        if board.get_click([self.rect.x + self.size, self.rect.y]) == 0:
            self.rect.x += self.size

    def left(self):
        if board.get_click([self.rect.x - self.size, self.rect.y]) == 0:
            self.rect.x -= self.size

    def position(self):
        pass


class Bomb(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(group)
        self.size = board.get_info()[2]
        self.image = load_image('bomb.png')
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = 10

    def change(self, x, y):
        self.rect.x = x
        self.rect.y = y


if __name__ == '__main__':
    pygame.init()
    size = 750, 750
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('BOMBERMAN v 0.1')
    pygame.display.set_icon(pygame.image.load('data/bomb.png'))
    # Ммм... Яндекс, thank you за то, что вместо встроенного нормального метода используешь свой 'забор'👍
    screen.fill("SKYBLUE")

    running = True
    clock = pygame.time.Clock()

    board = Board(19, 19)

    sprite1 = Bomberman()
    bomberman = pygame.sprite.Group()
    bomberman.add(sprite1)

    box = pygame.sprite.Group()
    bomb = pygame.sprite.Group()
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
                    sprite3 = Bomb()

                    bomb.add(sprite3)
                    bomb.draw(screen)
                    bomb.empty()
        screen.fill("skyblue")
        bomberman.draw(screen)
        board.render(screen)
        pygame.display.flip()
    pygame.quit()
