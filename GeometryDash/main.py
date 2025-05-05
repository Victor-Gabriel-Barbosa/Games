import pygame
import sys
import random
from player import Player
from obstacle import Obstacle

# Inicializar Pygame
pygame.init()
pygame.font.init()

# Configurações do jogo
WIDTH, HEIGHT = 800, 600
FPS = 60
GROUND_HEIGHT = 500

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Criar janela
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Geometry Dash em Python")
clock = pygame.time.Clock()

# Configurações do jogo
game_speed = 8
score = 0
font = pygame.font.SysFont('Arial', 30)

# Criar objetos do jogo
player = Player(100, GROUND_HEIGHT)
obstacles = []
obstacle_timer = 0
obstacle_frequency = 1500  # em milissegundos

# Função de restart
def restart_game():
    global game_speed, score, obstacles, obstacle_timer
    game_speed = 8
    score = 0
    obstacles = []
    obstacle_timer = 0
    player.reset(100, GROUND_HEIGHT)

# Game loop
running = True
game_over = False

while running:
    current_time = pygame.time.get_ticks()
    
    # Processar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                player.jump()
            if event.key == pygame.K_r and game_over:
                game_over = False
                restart_game()
    
    if not game_over:
        # Atualizar player
        player.update()
        
        # Criar obstáculos periodicamente
        if current_time - obstacle_timer > obstacle_frequency:
            obstacle_type = random.choice(["spike", "block"])
            obstacles.append(Obstacle(WIDTH, GROUND_HEIGHT, obstacle_type))
            obstacle_timer = current_time
            obstacle_frequency = random.randint(1200, 2000)  # Variação na frequência
        
        # Atualizar obstáculos
        for obstacle in obstacles[:]:
            obstacle.update(game_speed)
            
            # Verificar colisão
            if player.rect.colliderect(obstacle.rect):
                game_over = True
            
            # Remover obstáculos fora da tela
            if obstacle.rect.right < 0:
                obstacles.remove(obstacle)
                score += 1
        
        # Aumentar velocidade gradualmente
        if score > 0 and score % 5 == 0:
            game_speed = min(15, game_speed + 0.01)
    
    # Renderizar
    screen.fill(BLACK)
    
    # Desenhar fundo com efeito de grid
    for x in range(0, WIDTH, 50):
        pygame.draw.line(screen, (30, 30, 30), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, 50):
        pygame.draw.line(screen, (30, 30, 30), (0, y), (WIDTH, y))
    
    # Desenhar chão
    pygame.draw.rect(screen, BLUE, (0, GROUND_HEIGHT, WIDTH, HEIGHT - GROUND_HEIGHT))
    
    # Desenhar objetos
    player.draw(screen)
    for obstacle in obstacles:
        obstacle.draw(screen)
    
    # Desenhar pontuação
    score_text = font.render(f"Pontuação: {score}", True, WHITE)
    screen.blit(score_text, (20, 20))
    
    if game_over:
        # Exibir mensagem de game over
        game_over_text = font.render("GAME OVER - Pressione R para reiniciar", True, RED)
        screen.blit(game_over_text, (WIDTH//2 - 220, HEIGHT//2 - 15))
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()