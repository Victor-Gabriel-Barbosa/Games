import pygame
import time
import random

# Inicialização do Pygame
pygame.init()

# Definição de cores
branco = (255, 255, 255)
preto = (0, 0, 0)
vermelho = (213, 50, 80)
verde = (0, 255, 0)
azul = (50, 153, 213)

# Tamanho da janela
largura = 600
altura = 400

# Tamanho do bloco (cada segmento da cobra)
tamanho_bloco = 10
velocidade_cobra = 15

# Inicialização da janela
janela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Jogo da Cobrinha - Snake Game')

# Relógio para controlar a velocidade do jogo
relogio = pygame.time.Clock()

# Fonte para mostrar a pontuação
fonte = pygame.font.SysFont("bahnschrift", 25)
fonte_grande = pygame.font.SysFont("comicsansms", 35)

def pontuacao(pontos):
    """Mostra a pontuação na tela"""
    texto = fonte.render("Pontuação: " + str(pontos), True, azul)
    janela.blit(texto, [0, 0])

def cobra(tamanho_bloco, lista_cobra):
    """Desenha a cobra na tela"""
    for x in lista_cobra:
        pygame.draw.rect(janela, verde, [x[0], x[1], tamanho_bloco, tamanho_bloco])

def mensagem(msg, cor):
    """Mostra uma mensagem na tela"""
    texto = fonte_grande.render(msg, True, cor)
    janela.blit(texto, [largura / 6, altura / 3])

def jogo():
    """Função principal do jogo"""
    fim_de_jogo = False
    jogo_fechado = False
    
    # Posição inicial da cobra
    x = largura / 2
    y = altura / 2
    
    # Mudança na posição
    x_muda = 0
    y_muda = 0
    
    # Lista com as posições dos segmentos da cobra
    lista_cobra = []
    tamanho_cobra = 1
    
    # Posição inicial da comida (aleatória)
    comida_x = round(random.randrange(0, largura - tamanho_bloco) / 10.0) * 10.0
    comida_y = round(random.randrange(0, altura - tamanho_bloco) / 10.0) * 10.0
    
    # Loop principal do jogo
    while not fim_de_jogo:
        
        # Tela de "Game Over"
        while jogo_fechado:
            janela.fill(preto)
            mensagem("Perdeu! Pressione Q-Sair ou C-Jogar Novamente", vermelho)
            pontuacao(tamanho_cobra - 1)
            pygame.display.update()
            
            # Verifica se o jogador quer reiniciar ou sair
            for evento in pygame.event.get():
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_q:
                        fim_de_jogo = True
                        jogo_fechado = False
                    if evento.key == pygame.K_c:
                        jogo()
                        
        # Captura os eventos do teclado
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                fim_de_jogo = True
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT and x_muda != tamanho_bloco:
                    x_muda = -tamanho_bloco
                    y_muda = 0
                elif evento.key == pygame.K_RIGHT and x_muda != -tamanho_bloco:
                    x_muda = tamanho_bloco
                    y_muda = 0
                elif evento.key == pygame.K_UP and y_muda != tamanho_bloco:
                    y_muda = -tamanho_bloco
                    x_muda = 0
                elif evento.key == pygame.K_DOWN and y_muda != -tamanho_bloco:
                    y_muda = tamanho_bloco
                    x_muda = 0
                    
        # Verifica se a cobra bateu nas bordas
        if x >= largura or x < 0 or y >= altura or y < 0:
            jogo_fechado = True
            
        # Atualiza a posição da cobra
        x += x_muda
        y += y_muda
        
        # Desenha o fundo, a comida e a cobra
        janela.fill(preto)
        pygame.draw.rect(janela, vermelho, [comida_x, comida_y, tamanho_bloco, tamanho_bloco])
        
        cabeca_cobra = []
        cabeca_cobra.append(x)
        cabeca_cobra.append(y)
        lista_cobra.append(cabeca_cobra)
        
        # Remove segmentos extras (quando a cobra não cresceu)
        if len(lista_cobra) > tamanho_cobra:
            del lista_cobra[0]
            
        # Verifica se a cobra bateu nela mesma
        for segmento in lista_cobra[:-1]:
            if segmento == cabeca_cobra:
                jogo_fechado = True
                
        # Desenha a cobra e a pontuação
        cobra(tamanho_bloco, lista_cobra)
        pontuacao(tamanho_cobra - 1)
        
        pygame.display.update()
        
        # Verifica se a cobra comeu a comida
        if x == comida_x and y == comida_y:
            comida_x = round(random.randrange(0, largura - tamanho_bloco) / 10.0) * 10.0
            comida_y = round(random.randrange(0, altura - tamanho_bloco) / 10.0) * 10.0
            tamanho_cobra += 1
            
        # Controla a velocidade do jogo
        relogio.tick(velocidade_cobra)
        
    # Encerra o Pygame
    pygame.quit()
    quit()

# Inicia o jogo
jogo()