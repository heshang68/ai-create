import pygame
import random
import sys

# 初始化 Pygame
pygame.init()

# 定义颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# 设置游戏窗口
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BLOCK_SIZE = 20

# 创建游戏窗口
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('贪吃蛇')

# 蛇类
class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [(WINDOW_WIDTH//2, WINDOW_HEIGHT//2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = GREEN
        self.score = 0

    def get_head_position(self):
        return self.positions[0]

    def update(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (cur[0] + (x*BLOCK_SIZE), cur[1] + (y*BLOCK_SIZE))
        # 检查是否撞墙
        if (new[0] < 0 or new[0] >= WINDOW_WIDTH or 
            new[1] < 0 or new[1] >= WINDOW_HEIGHT or 
            new in self.positions[3:]):
            return False
        self.positions.insert(0, new)
        if len(self.positions) > self.length:
            self.positions.pop()
        return True

    def reset(self):
        self.length = 1
        self.positions = [(WINDOW_WIDTH//2, WINDOW_HEIGHT//2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0

    def draw(self, surface):
        for p in self.positions:
            pygame.draw.rect(surface, self.color, (p[0], p[1], BLOCK_SIZE, BLOCK_SIZE))

# 食物类
class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, (WINDOW_WIDTH-BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE,
                        random.randint(0, (WINDOW_HEIGHT-BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.position[0], self.position[1], BLOCK_SIZE, BLOCK_SIZE))

# 定义方向
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

def main():
    clock = pygame.time.Clock()
    snake = Snake()
    food = Food()
    font = pygame.font.Font(None, 36)
    game_over_font = pygame.font.Font(None, 72)
    
    # 添加一个变量来跟踪按键状态
    next_direction = snake.direction

    while True:
        # 将事件检测移到循环最前面
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # 立即更新方向意图，但不直接改变蛇的方向
                if event.key == pygame.K_UP and snake.direction != DOWN:
                    next_direction = UP
                elif event.key == pygame.K_DOWN and snake.direction != UP:
                    next_direction = DOWN
                elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                    next_direction = LEFT
                elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                    next_direction = RIGHT

        # 在更新蛇位置前应用方向变化
        snake.direction = next_direction

        # 更新蛇的位置
        if not snake.update():
            # 显示游戏结束提示
            game_over_text = game_over_font.render('游戏结束！按任意键继续', True, WHITE)
            text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
            screen.blit(game_over_text, text_rect)
            pygame.display.update()
            
            # 等待用户按键
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        waiting = False
                        snake.reset()
                        food.randomize_position()

        # 检查是否吃到食物
        if snake.get_head_position() == food.position:
            snake.length += 1
            snake.score += 1
            food.randomize_position()

        # 绘制
        screen.fill(BLACK)
        snake.draw(screen)
        food.draw(screen)
        
        # 显示分数
        score_text = font.render(f'得分: {snake.score}', True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.update()
        clock.tick(8)  # 略微提高速度以改善响应性

if __name__ == '__main__':
    main()
