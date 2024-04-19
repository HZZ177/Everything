import pygame
import random

# 初始化游戏
pygame.init()

# 设置游戏窗口
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("贪吃蛇")

# 定义颜色
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

# 设置游戏参数
block_size = 20
snake_speed = 10

# 初始化贪吃蛇
snake = [(window_width // 2, window_height // 2)]
snake_direction = 'RIGHT'

# 初始化食物
food_pos = (random.randint(0, (window_width - block_size) // block_size) * block_size,
            random.randint(0, (window_height - block_size) // block_size) * block_size)

# 游戏主循环
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                snake_direction = 'LEFT'
            elif event.key == pygame.K_RIGHT:
                snake_direction = 'RIGHT'
            elif event.key == pygame.K_UP:
                snake_direction = 'UP'
            elif event.key == pygame.K_DOWN:
                snake_direction = 'DOWN'

    # 更新贪吃蛇的位置
    head = snake[0]
    if snake_direction == 'LEFT':
        new_head = ((head[0] - block_size) % window_width, head[1])
    elif snake_direction == 'RIGHT':
        new_head = ((head[0] + block_size) % window_width, head[1])
    elif snake_direction == 'UP':
        new_head = (head[0], (head[1] - block_size) % window_height)
    elif snake_direction == 'DOWN':
        new_head = (head[0], (head[1] + block_size) % window_height)
    snake.insert(0, new_head)

    # 检查是否吃到了食物
    if new_head == food_pos:
        food_pos = (random.randint(0, (window_width - block_size) // block_size) * block_size,
                    random.randint(0, (window_height - block_size) // block_size) * block_size)
    else:
        snake.pop()

    # 绘制游戏界面
    window.fill(black)
    pygame.draw.rect(window, red, (food_pos[0], food_pos[1], block_size, block_size))
    for segment in snake:
        pygame.draw.rect(window, white, (segment[0], segment[1], block_size, block_size))
    pygame.display.update()

    # 控制游戏速度
    clock.tick(snake_speed)

# 退出游戏
pygame.quit()
