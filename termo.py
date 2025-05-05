import random
import os
import unicodedata

# Lista de palavras para o jogo (adicionaremos mais palavras, mas aqui estão algumas para teste)
PALAVRAS = [
    "sagaz", "âmago", "negro", "êxito", "termo", "nobre", "senso", "algoz", "afeto", "plena",
    "mútua", "etnia", "símio", "tênue", "assim", "sutil", "vigor", "aquém", "fazer", "porém",
    "audaz", "sanar", "seção", "inato", "poder", "moral", "desde", "justo", "muito", "honra",
    "ética", "sobre", "anexo", "digno", "razão", "tempo", "fútil", "ideal", "sonho", "cozer",
    "revés", "culto", "dizer", "posse", "mundo", "censo", "entre", "rigor", "comum", "valor"
]

def remover_acentos(palavra):
    """Remove acentos de uma palavra."""
    return ''.join(c for c in unicodedata.normalize('NFD', palavra)
                  if unicodedata.category(c) != 'Mn')

def limpar_tela():
    """Limpa a tela do console."""
    os.system('cls' if os.name == 'nt' else 'clear')

def escolher_palavra():
    """Escolhe uma palavra aleatória da lista."""
    return random.choice(PALAVRAS)

def verificar_tentativa(palavra_secreta, tentativa):
    """
    Verifica a tentativa e retorna um feedback colorido.
    Verde: letra correta na posição correta
    Amarelo: letra existe na palavra, mas em outra posição
    Cinza: letra não existe na palavra
    """
    # Remove acentos para facilitar a comparação
    palavra_sem_acento = remover_acentos(palavra_secreta)
    tentativa_sem_acento = remover_acentos(tentativa)
    
    resultado = [""] * 5
    # Dicionário para contar ocorrências de cada letra
    contagem_letras = {}
    
    for letra in palavra_sem_acento:
        if letra in contagem_letras:
            contagem_letras[letra] += 1
        else:
            contagem_letras[letra] = 1
            
    # Primeiro passo: marcar letras corretas na posição correta
    for i in range(5):
        if tentativa_sem_acento[i] == palavra_sem_acento[i]:
            resultado[i] = f"\033[42m {tentativa[i].upper()} \033[0m"  # Verde
            contagem_letras[tentativa_sem_acento[i]] -= 1
    
    # Segundo passo: marcar letras corretas na posição errada
    for i in range(5):
        if resultado[i] == "":  # Se ainda não foi marcada
            if tentativa_sem_acento[i] in contagem_letras and contagem_letras[tentativa_sem_acento[i]] > 0:
                resultado[i] = f"\033[43m {tentativa[i].upper()} \033[0m"  # Amarelo
                contagem_letras[tentativa_sem_acento[i]] -= 1
            else:
                resultado[i] = f"\033[47m\033[30m {tentativa[i].upper()} \033[0m"  # Cinza
                
    return "".join(resultado)

def jogar_termo():
    """Função principal do jogo."""
    limpar_tela()
    print("=" * 40)
    print("      TERMO - JOGO DE PALAVRAS")
    print("=" * 40)
    print("Tente adivinhar a palavra de 5 letras.")
    print("Verde: letra na posição correta")
    print("Amarelo: letra na palavra, mas posição errada")
    print("Cinza: letra não está na palavra")
    print("=" * 40)
    
    palavra_secreta = escolher_palavra()
    tentativas = []
    resultado_final = False
    
    for rodada in range(1, 7):
        valida = False
        while not valida:
            tentativa = input(f"\nTentativa {rodada}/6: ").lower().strip()
            
            if len(tentativa) != 5:
                print("A palavra deve ter 5 letras!")
            elif not tentativa.isalpha():
                print("Digite apenas letras!")
            else:
                valida = True
        
        resultado = verificar_tentativa(palavra_secreta, tentativa)
        tentativas.append(resultado)
        
        limpar_tela()
        print("=" * 40)
        print("      TERMO - JOGO DE PALAVRAS")
        print("=" * 40)
        
        # Mostrar tentativas anteriores
        for t in tentativas:
            print(t)
        
        # Verificar se ganhou
        if remover_acentos(tentativa) == remover_acentos(palavra_secreta):
            print(f"\nParabéns! Você acertou a palavra '{palavra_secreta.upper()}'!")
            resultado_final = True
            break
    
    if not resultado_final:
        print(f"\nVocê perdeu! A palavra era '{palavra_secreta.upper()}'.")
    
    jogar_novamente = input("\nDeseja jogar novamente? (s/n): ").lower()
    if jogar_novamente == 's':
        jogar_termo()
    else:
        print("Obrigado por jogar! Até a próxima!")

# Iniciar o jogo
if __name__ == "__main__":
    jogar_termo()