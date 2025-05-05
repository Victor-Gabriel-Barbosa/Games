import pygame

class Player:
    def __init__(self, x, y):
        self.original_y = y
        self.reset(x, y)
    
    def reset(self, x, y):
        self.x = x
        self.y = y - 40  # Ajuste para a altura do jogador
        self.width = 40
        self.height = 40
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.vel_y = 0
        self.is_jumping = False
        self.gravity = 1.2
        self.jump_power = -20
        
        # Variáveis para rotação
        self.rotation = 0
        self.rotation_speed = 5
    
    def jump(self):
        if not self.is_jumping:
            self.vel_y = self.jump_power
            self.is_jumping = True
    
    def update(self):
        # Aplicar gravidade
        self.vel_y += self.gravity
        self.y += self.vel_y
        
        # Rodar o cubo enquanto estiver no ar
        if self.is_jumping:
            self.rotation += self.rotation_speed
        
        # Verificar colisão com o chão
        if self.y > self.original_y - self.height:
            self.y = self.original_y - self.height
            self.vel_y = 0
            self.is_jumping = False
            self.rotation = 0  # Resetar rotação quando tocar o chão
        
        # Atualizar retângulo de colisão
        self.rect.x = self.x
        self.rect.y = self.y
    
    def draw(self, screen):
        # Criar surface para rotação
        surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(surf, (255, 0, 255), (0, 0, self.width, self.height))
        
        # Rotacionar e desenhar
        rotated_surf = pygame.transform.rotate(surf, self.rotation)
        rotated_rect = rotated_surf.get_rect(center=self.rect.center)
        screen.blit(rotated_surf, rotated_rect.topleft)