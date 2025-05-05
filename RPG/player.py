class Player:
    def __init__(self, name, character_class):
        self.name = name
        self.character_class = character_class
        self.level = 1
        self.max_hp = 0
        self.hp = 0
        self.attack = 0
        self.defense = 0
        self.exp = 0
        self.gold = 100
        self.inventory = []
        self.equipped_weapon = None
        self.equipped_armor = None
        self.location = "Vila Inicial"
        
        self.set_stats_by_class()
    
    def set_stats_by_class(self):
        if self.character_class == "Guerreiro":
            self.max_hp = 120
            self.hp = 120
            self.attack = 10
            self.defense = 8
        elif self.character_class == "Mago":
            self.max_hp = 80
            self.hp = 80
            self.attack = 15
            self.defense = 4
        elif self.character_class == "Arqueiro":
            self.max_hp = 90
            self.hp = 90
            self.attack = 12
            self.defense = 6
        
    def level_up(self):
        self.level += 1
        if self.character_class == "Guerreiro":
            self.max_hp += 15
            self.attack += 3
            self.defense += 2
        elif self.character_class == "Mago":
            self.max_hp += 10
            self.attack += 5
            self.defense += 1
        elif self.character_class == "Arqueiro":
            self.max_hp += 12
            self.attack += 4
            self.defense += 2
        
        self.hp = self.max_hp
        print(f"Parabéns! Você subiu para o nível {self.level}!")
        
    def gain_exp(self, amount):
        self.exp += amount
        print(f"Você ganhou {amount} pontos de experiência!")
        
        # Sistema simples de nível: cada 100 pontos é um nível
        if self.exp >= self.level * 100:
            self.level_up()
    
    def add_to_inventory(self, item):
        self.inventory.append(item)
        print(f"{item.name} foi adicionado ao seu inventário!")
    
    def show_inventory(self):
        if not self.inventory:
            print("Seu inventário está vazio.")
            return
        
        print("\n=== INVENTÁRIO ===")
        for i, item in enumerate(self.inventory, 1):
            print(f"{i}. {item.name} - {item.description}")
        print("==================\n")
    
    def equip_item(self, item_index):
        if item_index < 0 or item_index >= len(self.inventory):
            print("Item inválido!")
            return
        
        item = self.inventory[item_index]
        if item.type == "Arma":
            old_weapon = self.equipped_weapon
            self.equipped_weapon = item
            self.attack = self.attack - (old_weapon.value if old_weapon else 0) + item.value
            print(f"Você equipou {item.name}!")
        elif item.type == "Armadura":
            old_armor = self.equipped_armor
            self.equipped_armor = item
            self.defense = self.defense - (old_armor.value if old_armor else 0) + item.value
            print(f"Você equipou {item.name}!")
        else:
            print("Este item não pode ser equipado!")
    
    def heal(self, amount):
        self.hp = min(self.max_hp, self.hp + amount)
        print(f"Você recuperou {amount} pontos de vida!")
    
    def take_damage(self, damage):
        actual_damage = max(1, damage - self.defense)
        self.hp -= actual_damage
        print(f"Você sofreu {actual_damage} pontos de dano!")
        
        if self.hp <= 0:
            self.hp = 0
            print("Você foi derrotado!")
            return True  # Indica que o jogador foi derrotado
        return False
    
    def attack_enemy(self, enemy):
        damage = self.attack
        if self.equipped_weapon:
            print(f"Você ataca {enemy.name} com seu(sua) {self.equipped_weapon.name}!")
        else:
            print(f"Você ataca {enemy.name} com suas mãos!")
        
        return enemy.take_damage(damage)
    
    def show_status(self):
        print(f"\n=== {self.name} - {self.character_class} Nível {self.level} ===")
        print(f"HP: {self.hp}/{self.max_hp}")
        print(f"Ataque: {self.attack}")
        print(f"Defesa: {self.defense}")
        print(f"EXP: {self.exp}/{self.level * 100}")
        print(f"Ouro: {self.gold}")
        print(f"Localização: {self.location}")
        
        if self.equipped_weapon:
            print(f"Arma: {self.equipped_weapon.name}")
        else:
            print("Arma: Nenhuma")
            
        if self.equipped_armor:
            print(f"Armadura: {self.equipped_armor.name}")
        else:
            print("Armadura: Nenhuma")
        print("=====================\n")