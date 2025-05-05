import random
import tkinter as tk
from tkinter import messagebox

class CampoMinado:
    def __init__(self, master, rows=10, cols=10, mines=15):
        self.master = master
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.buttons = []
        self.board = []
        self.first_click = True
        self.mines_flagged = 0
        self.cells_revealed = 0
        
        # Configuração da janela principal
        master.title("Campo Minado")
        
        # Frame de informações
        self.info_frame = tk.Frame(master)
        self.info_frame.pack(fill="x")
        
        self.mine_label = tk.Label(self.info_frame, text=f"Minas: {self.mines}")
        self.mine_label.pack(side="left", padx=10)
        
        self.flag_label = tk.Label(self.info_frame, text=f"Bandeiras: 0/{self.mines}")
        self.flag_label.pack(side="right", padx=10)
        
        # Frame do tabuleiro
        self.board_frame = tk.Frame(master)
        self.board_frame.pack()
        
        self.create_board()
        self.create_buttons()
    
    def create_board(self):
        # Inicializa o tabuleiro vazio
        self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
    
    def place_mines(self, first_row, first_col):
        # Coloca minas aleatoriamente, evitando a primeira célula clicada
        positions = [(r, c) for r in range(self.rows) for c in range(self.cols)]
        positions.remove((first_row, first_col))
        
        # Remove também as células adjacentes à primeira célula clicada
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                adj_row, adj_col = first_row + dr, first_col + dc
                if 0 <= adj_row < self.rows and 0 <= adj_col < self.cols and (adj_row, adj_col) in positions:
                    positions.remove((adj_row, adj_col))
        
        # Seleciona posições aleatórias para as minas
        mine_positions = random.sample(positions, min(self.mines, len(positions)))
        
        # Coloca as minas no tabuleiro
        for row, col in mine_positions:
            self.board[row][col] = -1
        
        # Calcula os números para as células adjacentes às minas
        for row, col in mine_positions:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    adj_row, adj_col = row + dr, col + dc
                    if 0 <= adj_row < self.rows and 0 <= adj_col < self.cols and self.board[adj_row][adj_col] != -1:
                        self.board[adj_row][adj_col] += 1
    
    def create_buttons(self):
        # Cria os botões para o tabuleiro
        for row in range(self.rows):
            button_row = []
            for col in range(self.cols):
                button = tk.Button(self.board_frame, width=2, height=1, 
                                  command=lambda r=row, c=col: self.click(r, c))
                button.grid(row=row, column=col)
                button.bind('<Button-3>', lambda event, r=row, c=col: self.place_flag(r, c))
                button_row.append(button)
            self.buttons.append(button_row)
    
    def click(self, row, col):
        # Primeiro clique nunca deve ser uma mina
        if self.first_click:
            self.first_click = False
            self.place_mines(row, col)
        
        # Se a célula já estiver revelada ou com bandeira, não faz nada
        if self.buttons[row][col]['state'] == 'disabled' or self.buttons[row][col]['text'] == '🚩':
            return
        
        # Se clicou em uma mina, o jogo acaba
        if self.board[row][col] == -1:
            self.buttons[row][col].config(text="💣", bg="red")
            self.reveal_all_mines()
            messagebox.showinfo("Fim de Jogo", "Você perdeu!")
            self.master.quit()
            return
        
        # Revela a célula
        self.reveal_cell(row, col)
        
        # Verifica se o jogador ganhou
        self.check_win()
    
    def reveal_cell(self, row, col):
        # Se a célula já estiver revelada ou com bandeira, não faz nada
        if self.buttons[row][col]['state'] == 'disabled' or self.buttons[row][col]['text'] == '🚩':
            return
        
        # Revela a célula
        self.buttons[row][col]['state'] = 'disabled'
        self.cells_revealed += 1
        
        # Mostra o número de minas adjacentes (se houver)
        if self.board[row][col] > 0:
            self.buttons[row][col].config(text=str(self.board[row][col]), 
                                        disabledforeground=self.get_color(self.board[row][col]))
        else:
            # Se a célula não tiver minas adjacentes, revela as células vizinhas
            self.buttons[row][col].config(bg="light gray")
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    adj_row, adj_col = row + dr, col + dc
                    if 0 <= adj_row < self.rows and 0 <= adj_col < self.cols:
                        self.reveal_cell(adj_row, adj_col)
    
    def place_flag(self, row, col):
        # Coloca ou remove uma bandeira em uma célula não revelada
        if self.buttons[row][col]['state'] == 'disabled':
            return
        
        if self.buttons[row][col]['text'] == '🚩':
            self.buttons[row][col].config(text='', bg='SystemButtonFace')
            self.mines_flagged -= 1
        else:
            self.buttons[row][col].config(text='🚩', fg='red')
            self.mines_flagged += 1
        
        self.flag_label.config(text=f"Bandeiras: {self.mines_flagged}/{self.mines}")
        
        # Verifica se o jogador ganhou
        self.check_win()
    
    def get_color(self, number):
        # Retorna cor para cada número
        colors = {
            1: 'blue',
            2: 'green',
            3: 'red',
            4: 'purple',
            5: 'maroon',
            6: 'turquoise',
            7: 'black',
            8: 'gray'
        }
        return colors.get(number, 'black')
    
    def reveal_all_mines(self):
        # Revela todas as minas quando o jogo acaba
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] == -1:
                    if self.buttons[row][col]['text'] != '🚩':
                        self.buttons[row][col].config(text="💣", bg="red")
                elif self.buttons[row][col]['text'] == '🚩' and self.board[row][col] != -1:
                    # Marca bandeiras incorretas
                    self.buttons[row][col].config(text="❌", bg="orange")
    
    def check_win(self):
        # Verifica se o jogador ganhou
        total_cells = self.rows * self.cols
        if self.cells_revealed == total_cells - self.mines:
            self.reveal_all_mines()
            messagebox.showinfo("Parabéns", "Você venceu!")
            self.master.quit()

# Função para iniciar o jogo
def start_game():
    # Tamanho do tabuleiro e número de minas
    rows, cols, mines = 10, 10, 15
    
    # Cria a janela principal
    root = tk.Tk()
    game = CampoMinado(root, rows, cols, mines)
    root.mainloop()

if __name__ == "__main__":
    start_game()