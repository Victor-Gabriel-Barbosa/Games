import random

class Enemy:
    def __init__(self, name, hp, attack, defense, exp_reward, gold_reward):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.defense = defense
        self.exp_reward = exp_reward
        self.gold_reward = gold_reward
    
    def take_damage(self, damage):
        actual_damage = max(1, damage - self.defense)
        self.hp -= actual_damage
        print(f"{self.name} sofreu {actual_damage} pontos de dano!")
        
        if self.hp <= 0:
            self.hp = 0
            print(f"Você derrotou {self.name}!")
            return True  # Indica que o inimigo foi derrotado
        return False
    
    def attack_player(self, player):
        print(f"{self.name} ataca você!")
        return player.take_damage(self.attack)
    
    def show_status(self):
        print(f"{self.name} - HP: {self.hp}/{self.max_hp}")


class EnemyFactory:
    @staticmethod
    def create_enemy(enemy_type, level_modifier=0):
        """Cria inimigos com base no tipo e no modificador de nível"""
        
        if enemy_type == "Goblin":
            return Enemy("Goblin", 
                        30 + (level_modifier * 5), 
                        6 + level_modifier, 
                        2 + level_modifier // 2,
                        20 + (level_modifier * 5),
                        10 + (level_modifier * 2))
        
        elif enemy_type == "Lobo":
            return Enemy("Lobo Selvagem", 
                        25 + (level_modifier * 4), 
                        8 + (level_modifier * 2), 
                        1 + level_modifier // 2,
                        25 + (level_modifier * 6),
                        8 + (level_modifier * 3))
        
        elif enemy_type == "Esqueleto":
            return Enemy("Esqueleto", 
                        35 + (level_modifier * 6), 
                        7 + (level_modifier * 1), 
                        3 + level_modifier,
                        30 + (level_modifier * 7),
                        15 + (level_modifier * 5))
        
        elif enemy_type == "Bandido":
            return Enemy("Bandido", 
                        40 + (level_modifier * 7), 
                        9 + (level_modifier * 2), 
                        4 + level_modifier,
                        35 + (level_modifier * 8),
                        25 + (level_modifier * 8))
        
        elif enemy_type == "Troll":
            return Enemy("Troll", 
                        70 + (level_modifier * 10), 
                        12 + (level_modifier * 3), 
                        6 + (level_modifier * 2),
                        50 + (level_modifier * 12),
                        40 + (level_modifier * 10))
        
        elif enemy_type == "Dragão":
            return Enemy("Dragão Ancião", 
                        150 + (level_modifier * 20), 
                        20 + (level_modifier * 5), 
                        12 + (level_modifier * 3),
                        100 + (level_modifier * 25),
                        100 + (level_modifier * 30))
        
        else:
            # Inimigo padrão caso o tipo não seja reconhecido
            return Enemy("Criatura Misteriosa", 
                        40 + (level_modifier * 5), 
                        8 + (level_modifier * 2), 
                        3 + level_modifier,
                        30 + (level_modifier * 7),
                        20 + (level_modifier * 5))
    
    @staticmethod
    def get_random_enemy(location, player_level):
        """Retorna um inimigo aleatório com base na localização e nível do jogador"""
        level_mod = max(0, player_level - 1)  # Modificador de nível
        
        if location == "Floresta":
            enemies = ["Goblin", "Lobo", "Bandido"]
            chosen = random.choice(enemies)
            return EnemyFactory.create_enemy(chosen, level_mod)
        
        elif location == "Caverna":
            enemies = ["Esqueleto", "Goblin", "Troll"]
            chosen = random.choice(enemies)
            return EnemyFactory.create_enemy(chosen, level_mod)
        
        elif location == "Montanha":
            enemies = ["Lobo", "Troll", "Dragão"]
            weights = [0.6, 0.3, 0.1]  # Chances para cada inimigo
            chosen = random.choices(enemies, weights=weights, k=1)[0]
            return EnemyFactory.create_enemy(chosen, level_mod)
        
        else:  # Locais padrão ou desconhecidos
            enemies = ["Goblin", "Lobo", "Esqueleto", "Bandido"]
            chosen = random.choice(enemies)
            return EnemyFactory.create_enemy(chosen, level_mod)