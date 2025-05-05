import pygame
import random

# Inicialização
pygame.init()

# Constantes do jogo
WIDTH = 800
HEIGHT = 600
GRID_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
GRID_X_OFFSET = (WIDTH - GRID_WIDTH * GRID_SIZE) // 2
GRID_Y_OFFSET = HEIGHT - (GRID_HEIGHT * GRID_SIZE) - 50

# Cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)

# Definição das peças (tetrominós)
SHAPES = [
    [[1, 1, 1, 1]],                                # I
    [[1, 1, 1], [0, 1, 0]],                        # T
    [[1, 1, 1], [1, 0, 0]],                        # L
    [[1, 1, 1], [0, 0, 1]],                        # J
    [[1, 1], [1, 1]],                              # O
    [[0, 1, 1], [1, 1, 0]],                        # S
    [[1, 1, 0], [0, 1, 1]]                         # Z
]

COLORS = [CYAN, PURPLE, ORANGE, BLUE, YELLOW, GREEN, RED]

# Configurar a tela
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()

class Tetris:
    def __init__(self):
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = self.new_piece()
        self.game_over = False
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.fall_speed = 0.5  # Peças caem a cada 0.5 segundos
        self.fall_time = 0
        self.next_piece_index = random.randint(0, len(SHAPES) - 1)
        
    def new_piece(self):
        # Usar a próxima peça que já foi gerada
        shape_index = getattr(self, 'next_piece_index', random.randint(0, len(SHAPES) - 1))
        # Gerar a próxima peça para mostrar
        self.next_piece_index = random.randint(0, len(SHAPES) - 1)
        
        # Estrutura da peça atual
        shape = SHAPES[shape_index]
        color = COLORS[shape_index]
        x = GRID_WIDTH // 2 - len(shape[0]) // 2
        y = 0
        
        # Verificar se a peça pode ser colocada no topo
        if not self.valid_position(shape, (x, y)):
            self.game_over = True
            
        return {'shape': shape, 'color': color, 'x': x, 'y': y}
    
    def valid_position(self, shape, pos):
        x, y = pos
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell:
                    if (y + i >= GRID_HEIGHT or 
                        x + j < 0 or 
                        x + j >= GRID_WIDTH or 
                        y + i >= 0 and self.grid[y + i][x + j]):
                        return False
        return True
    
    def merge_piece(self):
        for i, row in enumerate(self.current_piece['shape']):
            for j, cell in enumerate(row):
                if cell:
                    if self.current_piece['y'] + i >= 0:  # Só adicionar à grade se estiver dentro dela
                        self.grid[self.current_piece['y'] + i][self.current_piece['x'] + j] = self.current_piece['color']
    
    def rotate(self):
        # Rodar a peça no sentido horário
        shape = self.current_piece['shape']
        rotated = [[shape[y][x] for y in range(len(shape) - 1, -1, -1)] for x in range(len(shape[0]))]
        
        if self.valid_position(rotated, (self.current_piece['x'], self.current_piece['y'])):
            self.current_piece['shape'] = rotated
    
    def clear_lines(self):
        lines_to_clear = []
        for i, row in enumerate(self.grid):
            if all(row):
                lines_to_clear.append(i)
        
        for line in lines_to_clear:
            del self.grid[line]
            self.grid.insert(0, [0 for _ in range(GRID_WIDTH)])
        
        # Atualizar pontuação
        if lines_to_clear:
            self.lines_cleared += len(lines_to_clear)
            self.score += 100 * len(lines_to_clear) * len(lines_to_clear)  # Mais linhas = mais pontos
            self.level = self.lines_cleared // 10 + 1
            self.fall_speed = max(0.05, 0.5 - 0.05 * (self.level - 1))  # Aumentar velocidade com level
            
    def move(self, dx, dy):
        new_x = self.current_piece['x'] + dx
        new_y = self.current_piece['y'] + dy
        
        if self.valid_position(self.current_piece['shape'], (new_x, new_y)):
            self.current_piece['x'] = new_x
            self.current_piece['y'] = new_y
            return True
        return False
    
    def update(self, delta_time):
        if self.game_over:
            return
        
        self.fall_time += delta_time
        
        if self.fall_time >= self.fall_speed:
            self.fall_time = 0
            if not self.move(0, 1):
                self.merge_piece()
                self.clear_lines()
                self.current_piece = self.new_piece()
    
    def draw_grid(self, surface):
        # Desenhar fundo
        pygame.draw.rect(surface, GRAY, (GRID_X_OFFSET - 2, GRID_Y_OFFSET - 2, 
                                       GRID_WIDTH * GRID_SIZE + 4, 
                                       GRID_HEIGHT * GRID_SIZE + 4), 2)
        
        # Desenhar grade
        for i in range(GRID_HEIGHT):
            for j in range(GRID_WIDTH):
                if self.grid[i][j]:
                    pygame.draw.rect(surface, self.grid[i][j], 
                                   (GRID_X_OFFSET + j * GRID_SIZE, 
                                    GRID_Y_OFFSET + i * GRID_SIZE, 
                                    GRID_SIZE, GRID_SIZE))
                    pygame.draw.rect(surface, BLACK, 
                                   (GRID_X_OFFSET + j * GRID_SIZE, 
                                    GRID_Y_OFFSET + i * GRID_SIZE, 
                                    GRID_SIZE, GRID_SIZE), 1)
    
    def draw_current_piece(self, surface):
        if self.game_over:
            return
            
        for i, row in enumerate(self.current_piece['shape']):
            for j, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(surface, self.current_piece['color'], 
                                   (GRID_X_OFFSET + (self.current_piece['x'] + j) * GRID_SIZE, 
                                    GRID_Y_OFFSET + (self.current_piece['y'] + i) * GRID_SIZE, 
                                    GRID_SIZE, GRID_SIZE))
                    pygame.draw.rect(surface, BLACK, 
                                   (GRID_X_OFFSET + (self.current_piece['x'] + j) * GRID_SIZE, 
                                    GRID_Y_OFFSET + (self.current_piece['y'] + i) * GRID_SIZE, 
                                    GRID_SIZE, GRID_SIZE), 1)
    
    def draw_next_piece(self, surface):
        # Desenhar próxima peça
        next_shape = SHAPES[self.next_piece_index]
        next_color = COLORS[self.next_piece_index]
        
        # Posição para desenhar a próxima peça
        next_x = WIDTH - 150
        next_y = 100
        
        # Desenhar texto
        font = pygame.font.SysFont(None, 30)
        text = font.render("PRÓXIMA PEÇA:", True, WHITE)
        surface.blit(text, (next_x - 30, next_y - 40))
        
        # Desenhar a peça
        for i, row in enumerate(next_shape):
            for j, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(surface, next_color, 
                                   (next_x + j * GRID_SIZE, 
                                    next_y + i * GRID_SIZE, 
                                    GRID_SIZE, GRID_SIZE))
                    pygame.draw.rect(surface, BLACK, 
                                   (next_x + j * GRID_SIZE, 
                                    next_y + i * GRID_SIZE, 
                                    GRID_SIZE, GRID_SIZE), 1)
    
    def draw_score(self, surface):
        # Desenhar pontuação, nível e linhas
        font = pygame.font.SysFont(None, 30)
        
        score_text = font.render(f"PONTUAÇÃO: {self.score}", True, WHITE)
        level_text = font.render(f"NÍVEL: {self.level}", True, WHITE)
        lines_text = font.render(f"LINHAS: {self.lines_cleared}", True, WHITE)
        
        surface.blit(score_text, (50, 100))
        surface.blit(level_text, (50, 140))
        surface.blit(lines_text, (50, 180))
        
    def draw_game_over(self, surface):
        if self.game_over:
            # Criar overlay semi-transparente
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(180)
            overlay.fill(BLACK)
            surface.blit(overlay, (0, 0))
            
            # Texto de game over
            font = pygame.font.SysFont(None, 60)
            game_over_text = font.render("GAME OVER", True, RED)
            restart_text = font.render("Pressione R para reiniciar", True, WHITE)
            
            surface.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))
            surface.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2))
    
    def draw(self, surface):
        surface.fill(BLACK)
        self.draw_grid(surface)
        self.draw_current_piece(surface)
        self.draw_next_piece(surface)
        self.draw_score(surface)
        self.draw_game_over(surface)
        
    def reset(self):
        self.__init__()

def main():
    game = Tetris()
    running = True
    
    # Tempo para controle de movimento lateral rápido
    move_repeat_delay = 0.1
    move_repeat_time = 0
    moving_left = False
    moving_right = False
    
    while running:
        delta_time = clock.tick(60) / 1000.0  # Converter para segundos
        
        # Atualizar timers
        if moving_left or moving_right:
            move_repeat_time += delta_time
        else:
            move_repeat_time = 0
        
        # Verificar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if not game.game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        game.move(-1, 0)
                        moving_left = True
                    if event.key == pygame.K_RIGHT:
                        game.move(1, 0)
                        moving_right = True
                    if event.key == pygame.K_DOWN:
                        game.fall_speed = 0.05  # Queda rápida
                    if event.key == pygame.K_UP:
                        game.rotate()
                    if event.key == pygame.K_SPACE:
                        # Hard drop - mover direto para baixo
                        while game.move(0, 1):
                            pass
                
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        moving_left = False
                    if event.key == pygame.K_RIGHT:
                        moving_right = False
                    if event.key == pygame.K_DOWN:
                        game.fall_speed = max(0.05, 0.5 - 0.05 * (game.level - 1))
            else:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    game.reset()
        
        # Movimento lateral contínuo
        if move_repeat_time >= move_repeat_delay:
            move_repeat_time = 0
            if moving_left:
                game.move(-1, 0)
            if moving_right:
                game.move(1, 0)
        
        # Atualizar estado do jogo
        game.update(delta_time)
        
        # Desenhar
        game.draw(screen)
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()