import random
import time
from player import Player
from enemy import EnemyFactory
from item import ItemFactory
from world import World

class Game:
    def __init__(self):
        self.player = None
        self.world = World()
        self.running = True
        self.current_location = None
    
    def start(self):
        self.welcome()
        self.create_character()
        self.tutorial()
        
        # Iniciar o loop principal do jogo
        self.game_loop()
    
    def welcome(self):
        print("\n" + "="*60)
        print("                 AVENTURA RPG EM PYTHON                   ")
        print("="*60)
        print("\nBem-vindo ao mundo de Pythonia, uma terra de magia e aventuras!")
        print("Você está prestes a embarcar em uma jornada épica...")
        time.sleep(1)
    
    def create_character(self):
        print("\n=== CRIAÇÃO DE PERSONAGEM ===")
        
        while True:
            name = input("\nQual é o seu nome, aventureiro? ")
            if name.strip():
                break
            print("Você precisa digitar um nome!")
        
        print("\nEscolha sua classe:")
        print("1. Guerreiro - Forte e resistente, especialista em combate corpo a corpo.")
        print("2. Mago - Frágil, mas com ataques poderosos e conhecimento arcano.")
        print("3. Arqueiro - Balanceado, preciso e ágil com ataques à distância.")
        
        while True:
            choice = input("\nDigite o número da sua classe (1-3): ")
            if choice == "1":
                character_class = "Guerreiro"
                break
            elif choice == "2":
                character_class = "Mago"
                break
            elif choice == "3":
                character_class = "Arqueiro"
                break
            else:
                print("Escolha inválida! Por favor, digite 1, 2 ou 3.")
        
        self.player = Player(name, character_class)
        
        # Dar itens iniciais ao jogador
        starter_items = ItemFactory.get_starter_items(character_class)
        for item in starter_items:
            self.player.add_to_inventory(item)
        
        # Equipar itens iniciais
        for item in starter_items:
            if item.type == "Arma":
                self.player.equip_item(self.player.inventory.index(item))
            elif item.type == "Armadura":
                self.player.equip_item(self.player.inventory.index(item))
        
        print(f"\nPersonagem criado com sucesso! {name}, o {character_class}, inicia sua jornada!")
        self.player.show_status()
        
        # Definir localização inicial
        self.current_location = self.world.get_location("Vila Inicial")
    
    def tutorial(self):
        print("\n=== TUTORIAL ===")
        print("Comandos básicos:")
        print("- 'olhar': examinar o ambiente")
        print("- 'ir [direção]': mover para outra localização (ex: 'ir norte')")
        print("- 'status': mostrar status do personagem")
        print("- 'inventário': ver seus itens")
        print("- 'equipar [número]': equipar um item do inventário")
        print("- 'usar [número]': usar um item do inventário")
        print("- 'lutar': procurar inimigos para combater")
        print("- 'loja': entrar na loja (se disponível na localização)")
        print("- 'ajuda': mostrar esta lista de comandos")
        print("- 'sair': sair do jogo")
        print("\nBoa sorte em sua jornada, aventureiro!")
        input("\nPressione ENTER para começar...")
    
    def show_help(self):
        print("\n=== COMANDOS DISPONÍVEIS ===")
        print("- 'olhar': examinar o ambiente")
        print("- 'ir [direção]': mover para outra localização (ex: 'ir norte')")
        print("- 'status': mostrar status do personagem")
        print("- 'inventário': ver seus itens")
        print("- 'equipar [número]': equipar um item do inventário")
        print("- 'usar [número]': usar um item do inventário")
        print("- 'lutar': procurar inimigos para combater")
        print("- 'loja': entrar na loja (se disponível na localização)")
        print("- 'ajuda': mostrar esta lista de comandos")
        print("- 'sair': sair do jogo")
    
    def game_loop(self):
        self.current_location.describe()
        
        while self.running:
            command = input("\nO que você deseja fazer? ").lower().strip()
            
            if command == "ajuda":
                self.show_help()
            
            elif command == "olhar":
                self.current_location.describe()
            
            elif command.startswith("ir "):
                self.move_player(command[3:])
            
            elif command == "status":
                self.player.show_status()
            
            elif command == "inventário":
                self.player.show_inventory()
            
            elif command.startswith("equipar "):
                try:
                    item_num = int(command[8:]) - 1
                    self.player.equip_item(item_num)
                except ValueError:
                    print("Por favor, digite um número válido após 'equipar'.")
            
            elif command.startswith("usar "):
                try:
                    item_num = int(command[5:]) - 1
                    if 0 <= item_num < len(self.player.inventory):
                        item = self.player.inventory[item_num]
                        if item.use(self.player):
                            print(f"Você usou {item.name}.")
                        else:
                            print(f"Você não pode usar {item.name} dessa maneira.")
                    else:
                        print("Número de item inválido!")
                except ValueError:
                    print("Por favor, digite um número válido após 'usar'.")
            
            elif command == "lutar":
                self.combat()
            
            elif command == "loja":
                if self.current_location.has_shop:
                    self.shop()
                else:
                    print("Não há uma loja neste local.")
            
            elif command == "sair":
                confirm = input("Tem certeza que deseja sair do jogo? (s/n) ").lower()
                if confirm == 's' or confirm == 'sim':
                    print("Obrigado por jogar! Até a próxima aventura!")
                    self.running = False
            
            else:
                print("Comando não reconhecido. Digite 'ajuda' para ver a lista de comandos.")
            
            # Verificar condições de fim de jogo
            if self.player.hp <= 0:
                print("\nVocê foi derrotado! Fim de jogo.")
                retry = input("Deseja tentar novamente? (s/n) ").lower()
                if retry == 's' or retry == 'sim':
                    # Resetar o jogador com algumas penalidades
                    self.player.hp = self.player.max_hp // 2
                    self.player.gold = max(0, self.player.gold - 50)
                    self.player.location = "Vila Inicial"
                    self.current_location = self.world.get_location("Vila Inicial")
                    print("\nVocê acorda na Vila Inicial, com metade da sua vida e tendo perdido parte do seu ouro...")
                    self.current_location.describe()
                else:
                    print("Obrigado por jogar! Até a próxima aventura!")
                    self.running = False
    
    def move_player(self, direction):
        if direction in self.current_location.connections:
            next_location_name = self.current_location.connections[direction]
            self.current_location = self.world.get_location(next_location_name)
            self.player.location = next_location_name
            self.current_location.describe()
            
            # Chance de encontro aleatório
            if next_location_name not in ["Vila Inicial", "Cidade Comercial", "Fortaleza Montanhosa"]:
                if random.random() < 0.3:  # 30% de chance
                    print("\nVocê encontrou um inimigo durante sua jornada!")
                    self.combat()
        else:
            print(f"Você não pode ir para {direction} a partir daqui.")
    
    def combat(self):
        location_name = self.current_location.name
        if location_name in ["Vila Inicial", "Cidade Comercial", "Fortaleza Montanhosa"]:
            print("Não há inimigos neste local seguro.")
            return
        
        enemy = EnemyFactory.get_random_enemy(location_name, self.player.level)
        print(f"\nVocê encontrou um {enemy.name}! Prepare-se para o combate!")
        
        # Loop de combate
        while True:
            print("\n=== COMBATE ===")
            self.player.show_status()
            enemy.show_status()
            
            print("\nOpções:")
            print("1. Atacar")
            print("2. Usar poção")
            print("3. Fugir")
            
            choice = input("O que você deseja fazer? ")
            
            if choice == "1":  # Atacar
                if self.player.attack_enemy(enemy):
                    # Inimigo derrotado
                    self.player.gain_exp(enemy.exp_reward)
                    self.player.gold += enemy.gold_reward
                    print(f"Você ganhou {enemy.gold_reward} de ouro!")
                    
                    # Chance de drop de item
                    if random.random() < 0.3:  # 30% de chance
                        if enemy.name == "Dragão Ancião":
                            item = ItemFactory.create_weapon("Espada Dracônica", 30, 1000, 
                                                         "Uma espada lendária feita com presas de dragão.")
                        elif "Troll" in enemy.name:
                            item = ItemFactory.create_armor("Pele de Troll", 15, 500, 
                                                         "Uma armadura robusta feita de pele de troll.")
                        else:
                            # Item aleatório baseado no nível do jogador
                            item_type = random.choice(["Arma", "Armadura", "Poção"])
                            if item_type == "Arma":
                                value = 5 + self.player.level
                                item = ItemFactory.create_weapon(f"Arma de Qualidade +{self.player.level}", 
                                                             value, value*10)
                            elif item_type == "Armadura":
                                value = 3 + self.player.level//2
                                item = ItemFactory.create_armor(f"Armadura Resistente +{self.player.level//2}", 
                                                            value, value*15)
                            else:
                                value = 30 + self.player.level*10
                                item = ItemFactory.create_potion(f"Poção de Cura +{self.player.level}", 
                                                             value, value//2)
                        
                        self.player.add_to_inventory(item)
                    
                    break
                
                # Turno do inimigo
                if enemy.attack_player(self.player):
                    # Jogador derrotado
                    print("Você foi derrotado em combate!")
                    break
                
            elif choice == "2":  # Usar poção
                potions = [i for i, item in enumerate(self.player.inventory) if item.type == "Poção"]
                if potions:
                    print("\nPoções disponíveis:")
                    for i, idx in enumerate(potions, 1):
                        item = self.player.inventory[idx]
                        print(f"{i}. {item.name} - Recupera {item.value} HP")
                    
                    try:
                        potion_choice = int(input("Qual poção você deseja usar? (0 para cancelar) "))
                        if potion_choice > 0 and potion_choice <= len(potions):
                            item_idx = potions[potion_choice-1]
                            potion = self.player.inventory[item_idx]
                            potion.use(self.player)
                            
                            # Turno do inimigo (usar poção não evita ataque)
                            if enemy.attack_player(self.player):
                                # Jogador derrotado
                                print("Você foi derrotado em combate!")
                                break
                        elif potion_choice != 0:
                            print("Escolha inválida!")
                    except ValueError:
                        print("Por favor, digite um número válido.")
                else:
                    print("Você não tem poções no inventário!")
                
            elif choice == "3":  # Fugir
                if random.random() < 0.7:  # 70% de chance de fugir
                    print("Você conseguiu fugir do combate!")
                    break
                else:
                    print("Você não conseguiu fugir!")
                    
                    # Inimigo ataca com vantagem por você tentar fugir
                    print(f"{enemy.name} ataca enquanto você tenta fugir!")
                    extra_damage = random.randint(1, 3)
                    enemy.attack += extra_damage
                    enemy.attack_player(self.player)
                    enemy.attack -= extra_damage
            
            else:
                print("Escolha inválida!")
    
    def shop(self):
        if not self.current_location.has_shop:
            print("Não há uma loja neste local.")
            return
            
        print("\n=== LOJA ===")
        print(f"Seu ouro: {self.player.gold}")
        print("\nO que você deseja fazer?")
        print("1. Comprar itens")
        print("2. Vender itens")
        print("3. Sair da loja")
        
        choice = input("Escolha uma opção: ")
        
        if choice == "1":  # Comprar
            shop_items = ItemFactory.get_shop_items(self.current_location.name, self.player.level)
            
            print("\nItens disponíveis para compra:")
            for i, item in enumerate(shop_items, 1):
                print(f"{i}. {item.name} - {item.description} - Preço: {item.price} ouro")
            
            try:
                buy_choice = int(input("\nQual item você deseja comprar? (0 para cancelar) "))
                if buy_choice > 0 and buy_choice <= len(shop_items):
                    item = shop_items[buy_choice-1]
                    
                    if self.player.gold >= item.price:
                        self.player.gold -= item.price
                        self.player.add_to_inventory(item)
                        print(f"Você comprou {item.name} por {item.price} ouro.")
                    else:
                        print("Você não tem ouro suficiente para este item!")
                elif buy_choice != 0:
                    print("Escolha inválida!")
            except ValueError:
                print("Por favor, digite um número válido.")
                
        elif choice == "2":  # Vender
            if not self.player.inventory:
                print("Seu inventário está vazio!")
                return
                
            print("\nItens disponíveis para venda:")
            for i, item in enumerate(self.player.inventory, 1):
                # Vender por 60% do valor original
                sell_price = int(item.price * 0.6)
                print(f"{i}. {item.name} - Preço de venda: {sell_price} ouro")
            
            try:
                sell_choice = int(input("\nQual item você deseja vender? (0 para cancelar) "))
                if sell_choice > 0 and sell_choice <= len(self.player.inventory):
                    item = self.player.inventory[sell_choice-1]
                    
                    # Verificar se o item está equipado
                    is_equipped = (item == self.player.equipped_weapon or item == self.player.equipped_armor)
                    
                    if is_equipped:
                        confirm = input("Este item está equipado. Tem certeza que deseja vendê-lo? (s/n) ").lower()
                        if confirm != 's' and confirm != 'sim':
                            print("Venda cancelada.")
                            return
                    
                    sell_price = int(item.price * 0.6)
                    self.player.gold += sell_price
                    
                    # Remover atributos do item se estiver equipado
                    if item == self.player.equipped_weapon:
                        self.player.attack -= item.value
                        self.player.equipped_weapon = None
                    elif item == self.player.equipped_armor:
                        self.player.defense -= item.value
                        self.player.equipped_armor = None
                    
                    # Remover do inventário
                    self.player.inventory.remove(item)
                    print(f"Você vendeu {item.name} por {sell_price} ouro.")
                    
                elif sell_choice != 0:
                    print("Escolha inválida!")
            except ValueError:
                print("Por favor, digite um número válido.")
                
        elif choice == "3":  # Sair
            print("Você saiu da loja.")
            
        else:
            print("Escolha inválida!")