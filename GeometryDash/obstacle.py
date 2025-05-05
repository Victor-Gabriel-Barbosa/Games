import pygame
import random

class Obstacle:
    def __init__(self, x, ground_y, obstacle_type):
        self.x = x
        self.ground_y = ground_y
        self.obstacle_type = obstacle_type
        
        if obstacle_type == "spike":
            self.width = 30
            self.height = 30
            self.y = ground_y - self.height
            self.color = (255, 0, 0)
        elif obstacle_type == "block":
            self.width = 40
            self.height = random.randint(40, 80)
            self.y = ground_y - self.height
            self.color = (255, 165, 0)
        
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def update(self, speed):
        self.x -= speed
        self.rect.x = self.x
    
    def draw(self, screen):
        if self.obstacle_type == "spike":
            # Desenhar um triângulo (espinho)
            points = [
                (self.x, self.ground_y),
                (self.x + self.width, self.ground_y),
                (self.x + self.width//2, self.y)
            ]
            pygame.draw.polygon(screen, self.color, points)
        else:
            # Desenhar um retângulo (bloco)
            pygame.draw.rect(screen, self.color, self.rect)