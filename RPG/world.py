class Location:
    def __init__(self, name, description, connections=None, has_shop=False):
        self.name = name
        self.description = description
        self.connections = connections if connections else {}  # {"norte": "Nome do Local", "sul": "Outro Local"}
        self.has_shop = has_shop
        self.visited = False
    
    def describe(self):
        if not self.visited:
            print(f"\n=== {self.name} ===")
            print(f"{self.description}")
            self.visited = True
        else:
            print(f"\nVocê está em {self.name}.")
        
        print("\nConexões disponíveis:")
        for direction, location in self.connections.items():
            print(f"- {direction.capitalize()}: {location}")
        
        if self.has_shop:
            print("\nHá uma loja aqui. Você pode comprar ou vender itens.")

class World:
    def __init__(self):
        self.locations = {}
        self.create_world()
    
    def create_world(self):
        # Criar os locais do mundo
        self.locations["Vila Inicial"] = Location(
            "Vila Inicial", 
            "Uma pequena vila pacífica. O ponto de partida da sua jornada.",
            has_shop=True
        )
        
        self.locations["Floresta"] = Location(
            "Floresta", 
            "Uma floresta densa e misteriosa. Você pode ouvir sons de criaturas ao seu redor."
        )
        
        self.locations["Caverna"] = Location(
            "Caverna", 
            "Uma caverna escura e úmida. Parece perigosa, mas pode conter tesouros."
        )
        
        self.locations["Cidade Comercial"] = Location(
            "Cidade Comercial", 
            "Uma cidade vibrante cheia de mercadores e viajantes.",
            has_shop=True
        )
        
        self.locations["Montanha"] = Location(
            "Montanha", 
            "Uma montanha alta e imponente. O caminho é íngreme e perigoso."
        )
        
        self.locations["Fortaleza Montanhosa"] = Location(
            "Fortaleza Montanhosa", 
            "Uma fortaleza construída na face da montanha. Parece antiga e imponente.",
            has_shop=True
        )
        
        self.locations["Torre do Mago"] = Location(
            "Torre do Mago", 
            "Uma torre alta e misteriosa pertencente a um poderoso mago."
        )
        
        # Definir conexões entre os locais
        self.locations["Vila Inicial"].connections = {
            "leste": "Floresta",
            "sul": "Cidade Comercial"
        }
        
        self.locations["Floresta"].connections = {
            "oeste": "Vila Inicial", 
            "leste": "Caverna",
            "sul": "Montanha"
        }
        
        self.locations["Caverna"].connections = {
            "oeste": "Floresta"
        }
        
        self.locations["Cidade Comercial"].connections = {
            "norte": "Vila Inicial",
            "leste": "Montanha"
        }
        
        self.locations["Montanha"].connections = {
            "norte": "Floresta",
            "oeste": "Cidade Comercial",
            "leste": "Fortaleza Montanhosa"
        }
        
        self.locations["Fortaleza Montanhosa"].connections = {
            "oeste": "Montanha",
            "norte": "Torre do Mago"
        }
        
        self.locations["Torre do Mago"].connections = {
            "sul": "Fortaleza Montanhosa"
        }
    
    def get_location(self, name):
        return self.locations.get(name)