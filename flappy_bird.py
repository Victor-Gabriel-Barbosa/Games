import pygame
import sys
import random

# Inicializar o pygame
pygame.init()

# Constantes do jogo
WIDTH = 400
HEIGHT = 600
FLOOR = 500
GRAVITY = 0.25
BIRD_MOVEMENT = 0
GAME_ACTIVE = True
SCORE = 0
HIGH_SCORE = 0
PIPE_GAP = 150
PIPE_FREQUENCY = 1500  # milissegundos

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY_BLUE = (135, 206, 235)
GREEN = (0, 128, 0)

# Configuração da tela
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()
game_font = pygame.font.SysFont('Arial', 40)

# Criar retângulos para o jogo
bird_rect = pygame.Rect(100, 250, 30, 30)
floor_rect = pygame.Rect(0, FLOOR, WIDTH, 100)

# Lista para os tubos
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, PIPE_FREQUENCY)

def draw_floor():
    """Desenha o chão"""
    pygame.draw.rect(screen, GREEN, floor_rect)

def create_pipe():
    """Cria novos tubos"""
    random_pipe_pos = random.randint(200, 400)
    bottom_pipe = pygame.Rect(WIDTH, random_pipe_pos, 50, HEIGHT - random_pipe_pos)
    top_pipe = pygame.Rect(WIDTH, 0, 50, random_pipe_pos - PIPE_GAP)
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    """Move os tubos para a esquerda"""
    new_pipes = []
    for pipe in pipes:
        new_pipe = pipe.move(-5, 0)
        if new_pipe.right > 0:  # Se o tubo ainda estiver na tela
            new_pipes.append(new_pipe)
    return new_pipes

def draw_pipes(pipes):
    """Desenha os tubos"""
    for pipe in pipes:
        if pipe.bottom >= HEIGHT:  # Tubo inferior
            pygame.draw.rect(screen, GREEN, pipe)
        else:  # Tubo superior
            pygame.draw.rect(screen, GREEN, pipe)

def check_collision(pipes):
    """Verifica colisões"""
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    
    if bird_rect.top <= 0 or bird_rect.bottom >= FLOOR:
        return False
    
    return True

def reset_game():
    """Reinicia o jogo"""
    global BIRD_MOVEMENT, GAME_ACTIVE, SCORE, pipe_list
    bird_rect.center = (100, 250)
    BIRD_MOVEMENT = 0
    pipe_list.clear()
    GAME_ACTIVE = True
    SCORE = 0

def score_display(game_state):
    """Exibe a pontuação"""
    global HIGH_SCORE
    if game_state:
        score_surface = game_font.render(f'Score: {SCORE}', True, WHITE)
        score_rect = score_surface.get_rect(center=(WIDTH//2, 50))
        screen.blit(score_surface, score_rect)
    else:
        score_surface = game_font.render(f'Score: {SCORE}', True, WHITE)
        score_rect = score_surface.get_rect(center=(WIDTH//2, 50))
        screen.blit(score_surface, score_rect)
        
        high_score_surface = game_font.render(f'High Score: {HIGH_SCORE}', True, WHITE)
        high_score_rect = high_score_surface.get_rect(center=(WIDTH//2, 100))
        screen.blit(high_score_surface, high_score_rect)
        
        restart_surface = game_font.render('Pressione ESPAÇO para reiniciar', True, WHITE)
        restart_rect = restart_surface.get_rect(center=(WIDTH//2, 150))
        screen.blit(restart_surface, restart_rect)

def update_score():
    """Atualiza a pontuação"""
    global SCORE, HIGH_SCORE
    
    for pipe in pipe_list:
        if 95 < pipe.centerx < 105 and pipe.bottom >= HEIGHT:  # Só conta tubos inferiores
            SCORE += 1
            return
    
    if SCORE > HIGH_SCORE:
        HIGH_SCORE = SCORE

# Loop principal do jogo
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and GAME_ACTIVE:
                BIRD_MOVEMENT = -7
            if event.key == pygame.K_SPACE and not GAME_ACTIVE:
                reset_game()
                
        if event.type == SPAWNPIPE and GAME_ACTIVE:
            pipe_list.extend(create_pipe())
            
    # Fundo
    screen.fill(SKY_BLUE)
    
    if GAME_ACTIVE:
        # Pássaro
        BIRD_MOVEMENT += GRAVITY
        bird_rect.centery += BIRD_MOVEMENT
        pygame.draw.rect(screen, (255, 0, 0), bird_rect)
        
        # Tubos
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        
        # Verificar colisão
        GAME_ACTIVE = check_collision(pipe_list)
        
        # Atualizar pontuação
        update_score()
    else:
        # Tela de Game Over
        screen.fill((0, 0, 0))
        
    # Chão
    draw_floor()
    
    # Exibir pontuação
    score_display(GAME_ACTIVE)
    
    pygame.display.update()
    clock.tick(60)