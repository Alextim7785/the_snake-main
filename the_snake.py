"""Импортируем модули для игры змейка"""
from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObjekt:
    """Это класс для представления игрового объекта."""
    # метод __init__ :инициализирует базовые атрибуты объекта,
    # такие как его позиция и цвет.
    def __init__(self):
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self):
        """это абстрактный метод, который
           предназначен для переопределения
           в дочерних классах.
        """


class Apple(GameObjekt):
    """
        Это класс Яблоко, унаследованный от родительского класса GameObject,
        описывающий яблоко и действия с ним
    """
    # Метод __init__:задаёт цвет яблока и вызывает метод randomize_position,
    # чтобы установить начальную позицию яблока.
    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self):
        """Метод устанавливает случайное положение яблока"""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    # отрисовывает яблоко на игровой поверхности
    def draw(self):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObjekt):
    """
    класс, унаследованный от GameObject, описывающий змейку и её поведение.
    Этот класс управляет её движением, отрисовкой, а также обрабатывает
    действия пользователя.
    """
    # инициализирует начальное состояние змейки
    def __init__(self):
        super().__init__()
        self.length = 1
        self.body_color = SNAKE_COLOR
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Метод обновляет направление движения змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод обновляет направление движения змейки"""
        dx, dy = self.direction
        new_x = (self.positions[0][0] + dx * GRID_SIZE) % SCREEN_WIDTH
        new_y = (self.positions[0][1] + dy * GRID_SIZE) % SCREEN_HEIGHT
        self.positions.insert(0, (new_x, new_y))
        if len(self.positions) > self.length:
            self.positions.pop()

    # отрисовывает змейку на экране, затирая след
    def draw(self):
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Метод возвращает позицию головы змейки"""
        return self.positions[0]

    def reset(self):
        """Метод сбрасывает змейку в начальное состояние"""
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.length = 1
        self.direction = choice([UP, DOWN, LEFT, RIGHT])


# обрабатывает нажатия клавиш, чтобы изменить направление движения змейки
def handle_keys(game_object):
    """Функция обрабатывает нажатия клавиш,
        чтобы изменить направление движения змейки"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
                # добавим кнопку Esc для выхода из игры
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise SystemExit


def main():
    """Инициализация PyGame:"""
    pygame.init()
    apple = Apple()
    snake = Snake()
    # Цикл While вычисляет новое состояние игрового поля: определяет координаты
    # каждого сегмента змейки и, при необходимости, координаты яблока,
    # а также проверяет, не столкнулась ли змейка сама с собой.
    # После выполнения всех вычислений вызывается
    # функция pygame.display.update(), которая обновляет игровое поле
    # на экране пользователя. Отображение игрового поля обновляется
    # на каждой итерации цикла.
    while True:
        screen.fill(BOARD_BACKGROUND_COLOR)
        clock.tick(SPEED)

        handle_keys(snake)
        snake.update_direction()
        apple.draw()
        snake.draw()
        snake.move()
        # Проверка на съедение яблока
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
        # Проверка на столкновение с самим собой
        head_pos = snake.get_head_position()
        if head_pos in snake.positions[1:]:
            snake.reset()
            apple.randomize_position()

        pygame.display.update()

        # Тут опишите основную логику игры.
        # Сначала создаются необходимые объекты.
        # В основном цикле игры (в функции main)
        # происходит обновление состояний
        # объектов: змейка обрабатывает нажатия клавиш и двигается
        # в соответствии с выбранным направлением.
        # Если змейка съедает яблоко, её размер увеличивается на один сегмент,
        # а яблоко перемещается на новую случайную позицию.
        # При столкновении змейки с самой собой игра начинается заново.


if __name__ == '__main__':
    main()
