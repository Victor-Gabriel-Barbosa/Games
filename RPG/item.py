class Item:
    def __init__(self, name, description, type, value, price):
        self.name = name
        self.description = description
        self.type = type  # "Arma", "Armadura", "Poção", "Tesouro"
        self.value = value  # Valor de ataque para armas, defesa para armaduras, etc.
        self.price = price  # Valor em ouro
    
    def use(self, player):
        if self.type == "Poção":
            player.heal(self.value)
            player.inventory.remove(self)
            return True
        return False  # Item não é usável

class ItemFactory:
    @staticmethod
    def create_weapon(name, attack_value, price, description=None):
        if description is None:
            description = f"Uma arma que adiciona {attack_value} ao seu ataque."
        return Item(name, description, "Arma", attack_value, price)
    
    @staticmethod
    def create_armor(name, defense_value, price, description=None):
        if description is None:
            description = f"Uma armadura que adiciona {defense_value} à sua defesa."
        return Item(name, description, "Armadura", defense_value, price)
    
    @staticmethod
    def create_potion(name, healing_value, price, description=None):
        if description is None:
            description = f"Uma poção que recupera {healing_value} pontos de vida."
        return Item(name, description, "Poção", healing_value, price)
    
    @staticmethod
    def create_treasure(name, value, price, description=None):
        if description is None:
            description = f"Um tesouro valioso que vale {price} de ouro."
        return Item(name, description, "Tesouro", value, price)
    
    @staticmethod
    def get_starter_items(character_class):
        items = []
        
        # Cada classe começa com equipamentos diferentes
        if character_class == "Guerreiro":
            items.append(ItemFactory.create_weapon("Espada de Ferro", 5, 50, "Uma espada básica, mas eficiente."))
            items.append(ItemFactory.create_armor("Armadura de Couro", 3, 40, "Armadura leve que oferece proteção básica."))
            
        elif character_class == "Mago":
            items.append(ItemFactory.create_weapon("Cajado Arcano", 7, 60, "Um cajado que canaliza energia mágica."))
            items.append(ItemFactory.create_armor("Manto de Aprendiz", 1, 30, "Um manto leve que oferece pouca proteção."))
            
        elif character_class == "Arqueiro":
            items.append(ItemFactory.create_weapon("Arco Curto", 6, 55, "Um arco simples mas preciso."))
            items.append(ItemFactory.create_armor("Túnica de Caçador", 2, 35, "Vestimenta leve que permite movimento ágil."))
        
        # Todos ganham uma poção de cura
        items.append(ItemFactory.create_potion("Poção de Cura Pequena", 30, 15))
        
        return items
    
    @staticmethod
    def get_shop_items(location, player_level):
        """Retorna uma lista de itens disponíveis para compra com base na localização"""
        items = []
        
        # Itens básicos disponíveis em qualquer loja
        items.append(ItemFactory.create_potion("Poção de Cura Pequena", 30, 15))
        items.append(ItemFactory.create_potion("Poção de Cura Média", 60, 30))
        
        # Itens específicos por localização
        if location == "Vila Inicial":
            items.append(ItemFactory.create_weapon("Espada de Ferro", 5, 50))
            items.append(ItemFactory.create_weapon("Cajado de Madeira", 4, 45))
            items.append(ItemFactory.create_armor("Armadura de Couro", 3, 40))
            
        elif location == "Cidade Comercial":
            items.append(ItemFactory.create_weapon("Espada de Aço", 8, 100))
            items.append(ItemFactory.create_weapon("Arco Longo", 9, 110))
            items.append(ItemFactory.create_armor("Cota de Malha", 6, 120))
            items.append(ItemFactory.create_potion("Poção de Cura Grande", 100, 60))
            
        elif location == "Fortaleza Montanhosa":
            items.append(ItemFactory.create_weapon("Martelo de Guerra", 12, 200))
            items.append(ItemFactory.create_weapon("Cajado Elemental", 14, 220))
            items.append(ItemFactory.create_armor("Armadura de Placas", 10, 250))
            
        # Adicionar itens melhores conforme o nível do jogador
        if player_level >= 5:
            items.append(ItemFactory.create_weapon("Espada Encantada", 15, 300, "Uma espada com encantamentos mágicos."))
            items.append(ItemFactory.create_armor("Escudo Fortificado", 8, 280, "Um escudo resistente a ataques."))
            
        if player_level >= 10:
            items.append(ItemFactory.create_weapon("Lâmina do Dragão", 25, 600, "Uma espada lendária forjada com escamas de dragão."))
            items.append(ItemFactory.create_armor("Armadura de Mithril", 18, 700, "Uma armadura quase impenetrável feita de mithril."))
            
        return items