import pygame
import os
import sys

MYEVENTTYPE = pygame.USEREVENT + 1


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
        self.state = 1
        self.x, self.y = 0, 0

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] == 0:
                    pygame.draw.rect(screen, "white", (self.left + (self.cell_size * i),
                                                       self.top + (self.cell_size * j),
                                                       self.cell_size, self.cell_size), width=1)

    def on_click(self, cell_coords):
        if cell_coords is None:
            return None
        x, y = cell_coords
        if self.board[x][y] == 0:
            self.board[x][y] += self.state
            if self.state == 1:
                self.state = 2
            elif self.state == 2:
                self.x = x
                self.y = y
                self.state = 1

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        pos_x = (x - self.left) // self.cell_size
        pos_y = (y - self.top) // self.cell_size
        if pos_x < self.width and pos_y < self.width:
            return pos_x, pos_y
        return None

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)


class Box(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(group)
        self.image = load_image("box.png")
        self.rect = self.image.get_rect()

    def update(self, *args, **kwargs):
        pass


class Bomberman(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(group)
        self.image = load_image("bomberman.png")
        self.image = pygame.transform.scale(self.image, (38, 38))
        self.rect = self.image.get_rect()
        self.rect.x = 48
        self.rect.y = 48

    def up(self):
        screen.fill("skyblue")
        self.rect.y -= 38

    def down(self):
        screen.fill("skyblue")
        self.rect.y += 38

    def right(self):
        screen.fill("skyblue")
        self.rect.x += 38

    def left(self):
        screen.fill("skyblue")
        self.rect.x -= 38

    def create_bomb(self):
        sprite3.change(x, y)
        bomb.draw(screen)


class Bomb(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(group)
        self.image = load_image('bomb.png')
        self.image = pygame.transform.scale(self.image, (38, 38))
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = 10

    def change(self, x, y):
        self.rect.x = x
        self.rect.y = y


if __name__ == '__main__':
    pygame.init()
    size = 800, 800
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('BOMBERMAN')
    screen.fill("SKYBLUE")

    running = True
    clock = pygame.time.Clock()

    board = Board(20, 20)

    sprite1 = Bomberman()
    bomberman = pygame.sprite.Group()
    bomberman.add(sprite1)

    sprite2 = Box()
    box = pygame.sprite.Group()
    box.add(sprite2)

    sprite3 = Bomb()
    bomb = pygame.sprite.Group()
    bomb.add(sprite3)
    while running:
        tick = clock.tick()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
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
                    sprite3.change(event.pos)
                    bomb.draw(screen)
        bomberman.draw(screen)
        board.render(screen)
        pygame.display.flip()
    pygame.quit()
