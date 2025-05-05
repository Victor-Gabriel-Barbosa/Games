import pygame
import sys
import math

# Inicialização do Pygame
pygame.init()

# Constantes físicas
GRAVIDADE = 9.81  # m/s²
COEF_RESTITUICAO = 0.7  # Coeficiente de restituição (para quicar)
COEF_ARRASTO = 0.005  # Coeficiente de arrasto (resistência do ar)
FPS = 60

# Configurações da tela
LARGURA, ALTURA = 1000, 600
ESCALA = 20  # pixels por metro
COR_FUNDO = (135, 206, 235)  # Azul claro (céu)
COR_CHAO = (34, 139, 34)  # Verde (grama)
COR_BOLA = (255, 0, 0)  # Vermelho

# Configuração da tela
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Simulação de Lançamento de Bola")
clock = pygame.time.Clock()

# Classe para a bola
class Bola:
    def __init__(self):
        self.raio = 0.2  # metros
        self.raio_px = int(self.raio * ESCALA)
        self.massa = 0.5  # kg
        self.reset()
        
    def reset(self):
        # Posição inicial (x, y) em metros - y é invertido na tela
        self.pos = [1.0, ALTURA / ESCALA - self.raio]
        self.pos_inicial = self.pos.copy()
        
        # Velocidade inicial zero
        self.vel = [0, 0]
        
        # Estado da simulação
        self.lancada = False
        self.em_movimento = False
        self.trajetoria = []
    
    def atualizar(self, dt):
        if not self.lancada or not self.em_movimento:
            return
            
        # Aplicar resistência do ar (força de arrasto)
        vel_magnitude = math.sqrt(self.vel[0]**2 + self.vel[1]**2)
        arrasto_x = -self.vel[0] * vel_magnitude * COEF_ARRASTO
        arrasto_y = -self.vel[1] * vel_magnitude * COEF_ARRASTO
        
        # Atualizar velocidade com gravidade e arrasto
        self.vel[0] += arrasto_x * dt
        self.vel[1] += (GRAVIDADE + arrasto_y) * dt
        
        # Atualizar posição
        self.pos[0] += self.vel[0] * dt
        self.pos[1] += self.vel[1] * dt
        
        # Armazenar ponto para trajetória
        px = int(self.pos[0] * ESCALA)
        py = int(ALTURA - self.pos[1] * ESCALA)
        self.trajetoria.append((px, py))
        
        # Verificar colisão com o chão
        if self.pos[1] >= ALTURA / ESCALA - self.raio:
            self.pos[1] = ALTURA / ESCALA - self.raio
            self.vel[1] = -self.vel[1] * COEF_RESTITUICAO
            
            # Aplicar atrito no chão
            self.vel[0] = self.vel[0] * 0.9
            
            # Parar a bola se estiver muito lenta
            if abs(self.vel[0]) < 0.1 and abs(self.vel[1]) < 0.1:
                self.em_movimento = False
        
        # Verificar colisão com as paredes laterais
        if self.pos[0] <= self.raio:
            self.pos[0] = self.raio
            self.vel[0] = -self.vel[0] * COEF_RESTITUICAO
            
        if self.pos[0] >= LARGURA / ESCALA - self.raio:
            self.pos[0] = LARGURA / ESCALA - self.raio
            self.vel[0] = -self.vel[0] * COEF_RESTITUICAO
    
    def desenhar(self):
        # Converter metros para pixels
        x = int(self.pos[0] * ESCALA)
        y = int(ALTURA - self.pos[1] * ESCALA)  # Inverter coordenada y
        
        # Desenhar trajetória
        if len(self.trajetoria) > 1:
            pygame.draw.lines(tela, (100, 100, 100), False, self.trajetoria, 2)
        
        # Desenhar bola
        pygame.draw.circle(tela, COR_BOLA, (x, y), self.raio_px)
    
    def lancar(self, velocidade, angulo):
        # Converter ângulo de graus para radianos
        angulo_rad = math.radians(angulo)
        
        # Definir componentes da velocidade
        self.vel[0] = velocidade * math.cos(angulo_rad)
        self.vel[1] = -velocidade * math.sin(angulo_rad)  # Negativo pois o eixo y é invertido
        
        self.lancada = True
        self.em_movimento = True
        self.trajetoria = [(int(self.pos[0] * ESCALA), int(ALTURA - self.pos[1] * ESCALA))]

# Função para mostrar texto na tela
def mostrar_texto(texto, pos, tamanho=24, cor=(0, 0, 0)):
    fonte = pygame.font.SysFont("Arial", tamanho)
    superficie = fonte.render(texto, True, cor)
    tela.blit(superficie, pos)

# Configurações da simulação
velocidade = 15.0  # m/s
angulo = 45  # graus

# Criar bola
bola = Bola()

# Variáveis para controle do lançamento e interface
ajustando_velocidade = False
ajustando_angulo = False
simulacao_em_andamento = False

# Loop principal
executando = True
while executando:
    dt = 1/FPS  # Delta time em segundos
    
    # Processar eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            executando = False
        
        # Eventos de teclado
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                if not simulacao_em_andamento:
                    bola.lancar(velocidade, angulo)
                    simulacao_em_andamento = True
                else:
                    bola.reset()
                    simulacao_em_andamento = False
            
            # Teclas para ajustar velocidade
            if evento.key == pygame.K_v:
                ajustando_velocidade = True
                ajustando_angulo = False
            
            # Teclas para ajustar ângulo
            if evento.key == pygame.K_a:
                ajustando_angulo = True
                ajustando_velocidade = False
            
            # Incrementar/decrementar valores
            if ajustando_velocidade:
                if evento.key == pygame.K_UP:
                    velocidade += 1
                if evento.key == pygame.K_DOWN and velocidade > 1:
                    velocidade -= 1
            
            if ajustando_angulo:
                if evento.key == pygame.K_UP and angulo < 90:
                    angulo += 5
                if evento.key == pygame.K_DOWN and angulo > 0:
                    angulo -= 5
    
    # Atualizar a simulação
    bola.atualizar(dt)
    
    # Renderização
    # Desenhar fundo
    tela.fill(COR_FUNDO)
    
    # Desenhar chão
    pygame.draw.rect(tela, COR_CHAO, (0, ALTURA - 20, LARGURA, 20))
    
    # Desenhar bola
    bola.desenhar()
    
    # Mostrar informações
    mostrar_texto(f"Velocidade: {velocidade:.1f} m/s (Pressione V + setas)", (20, 20))
    mostrar_texto(f"Ângulo: {angulo}° (Pressione A + setas)", (20, 50))
    mostrar_texto("Pressione ESPAÇO para lançar/resetar", (20, 80))
    
    if simulacao_em_andamento and not bola.em_movimento:
        mostrar_texto("Bola parou. Pressione ESPAÇO para reiniciar.", (LARGURA//2 - 200, ALTURA//2), 30)
    
    # Atualizar a tela
    pygame.display.flip()
    clock.tick(FPS)

# Finalizar Pygame
pygame.quit()
sys.exit()