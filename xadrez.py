import pygame
import os
import sys

# Inicializar o Pygame
pygame.init()

# Constantes
WIDTH, HEIGHT = 512, 512
DIMENSION = 8
SQ_SIZE = WIDTH // DIMENSION
MAX_FPS = 60
IMAGES = {}

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_SQUARE = (240, 217, 181)
DARK_SQUARE = (181, 136, 99)
HIGHLIGHT = (247, 247, 105, 150)  # Amarelo com transparência
HIGHLIGHT_VALID = (106, 168, 79, 150)  # Verde com transparência

# Configuração da tela
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess - Pygame")
clock = pygame.time.Clock()

def load_images():
    """Carrega as imagens das peças."""
    pieces = ['wp', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bp', 'bR', 'bN', 'bB', 'bQ', 'bK']
    for piece in pieces:
        # Tenta carregar as imagens diretamente (sem caminho)
        try:
            # Para dar suporte a execução em qualquer diretório
            img_path = f"chess_pieces/{piece}.png"
            if not os.path.exists(img_path):
                # Tente encontrar em um diretório de recursos padrão
                img_path = os.path.join(os.path.dirname(__file__), "chess_pieces", f"{piece}.png")
                
                # Se ainda não existe, crie uma imagem de placeholder
                if not os.path.exists(img_path):
                    # Vamos criar um placeholder
                    surf = pygame.Surface((SQ_SIZE, SQ_SIZE), pygame.SRCALPHA)
                    pygame.draw.rect(surf, (255, 0, 0, 180), pygame.Rect(0, 0, SQ_SIZE, SQ_SIZE))
                    font = pygame.font.SysFont("Arial", 20)
                    text = font.render(piece, True, (255, 255, 255))
                    surf.blit(text, ((SQ_SIZE - text.get_width()) // 2, (SQ_SIZE - text.get_height()) // 2))
                    IMAGES[piece] = surf
                    continue
                    
            IMAGES[piece] = pygame.transform.scale(
                pygame.image.load(img_path), (SQ_SIZE, SQ_SIZE)
            )
        except Exception as e:
            print(f"Erro ao carregar imagem {piece}: {e}")
            # Criar uma imagem placeholder em caso de erro
            surf = pygame.Surface((SQ_SIZE, SQ_SIZE), pygame.SRCALPHA)
            color = (255, 0, 0) if 'w' in piece else (0, 0, 255)
            pygame.draw.rect(surf, color, pygame.Rect(10, 10, SQ_SIZE-20, SQ_SIZE-20))
            font = pygame.font.SysFont("Arial", 24)
            text = font.render(piece[1] if len(piece) > 1 else piece, True, (255, 255, 255))
            surf.blit(text, ((SQ_SIZE - text.get_width()) // 2, (SQ_SIZE - text.get_height()) // 2))
            IMAGES[piece] = surf


class GameState:
    def __init__(self):
        # Tabuleiro é uma lista 8x8
        # O primeiro caractere representa a cor ('b' ou 'w')
        # O segundo caractere representa o tipo de peça
        # "--" representa um espaço vazio
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.white_to_move = True
        self.move_log = []
        self.move_functions = {
            'p': self.get_pawn_moves,
            'R': self.get_rook_moves,
            'N': self.get_knight_moves,
            'B': self.get_bishop_moves,
            'Q': self.get_queen_moves,
            'K': self.get_king_moves
        }
        # Rastrear posição dos reis
        self.white_king_location = (7, 4)
        self.black_king_location = (0, 4)
        self.checkmate = False
        self.stalemate = False
        # Rastrear possibilidade de roque
        self.white_castle_kingside = True
        self.white_castle_queenside = True
        self.black_castle_kingside = True
        self.black_castle_queenside = True
        # Para en passant
        self.enpassant_possible = ()  # Coordenadas da casa onde en passant é possível
        self.current_castling_rights = CastleRights(True, True, True, True)
        self.castle_rights_log = [CastleRights(self.current_castling_rights.wks, 
                                              self.current_castling_rights.wqs,
                                              self.current_castling_rights.bks, 
                                              self.current_castling_rights.bqs)]

    def make_move(self, move):
        """Executa um movimento e atualiza o estado do jogo."""
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)  # Registra o movimento para poder desfazer depois
        self.white_to_move = not self.white_to_move  # Troca o turno
        
        # Atualizar posição do rei se foi movido
        if move.piece_moved == "wK":
            self.white_king_location = (move.end_row, move.end_col)
        elif move.piece_moved == "bK":
            self.black_king_location = (move.end_row, move.end_col)
            
        # Promoção de peão
        if move.is_pawn_promotion:
            self.board[move.end_row][move.end_col] = move.piece_moved[0] + "Q"  # Sempre promove para rainha
            
        # En passant
        if move.is_enpassant_move:
            self.board[move.start_row][move.end_col] = "--"  # Captura o peão
            
        # Atualizar variável enpassant_possible
        if move.piece_moved[1] == 'p' and abs(move.start_row - move.end_row) == 2:
            self.enpassant_possible = ((move.start_row + move.end_row) // 2, move.start_col)
        else:
            self.enpassant_possible = ()
            
        # Movimentos de roque
        if move.is_castle_move:
            if move.end_col - move.start_col == 2:  # Roque do lado do rei
                # Move a torre
                self.board[move.end_row][move.end_col - 1] = self.board[move.end_row][move.end_col + 1]
                self.board[move.end_row][move.end_col + 1] = "--"
            else:  # Roque do lado da rainha
                # Move a torre
                self.board[move.end_row][move.end_col + 1] = self.board[move.end_row][move.end_col - 2]
                self.board[move.end_row][move.end_col - 2] = "--"
                
        # Atualizar direitos de roque
        self.update_castle_rights(move)
        self.castle_rights_log.append(CastleRights(self.current_castling_rights.wks, 
                                                  self.current_castling_rights.wqs,
                                                  self.current_castling_rights.bks, 
                                                  self.current_castling_rights.bqs))

    def undo_move(self):
        """Desfaz o último movimento realizado."""
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.white_to_move = not self.white_to_move  # Troca o turno de volta
            
            # Atualizar posição do rei se foi movido
            if move.piece_moved == "wK":
                self.white_king_location = (move.start_row, move.start_col)
            elif move.piece_moved == "bK":
                self.black_king_location = (move.start_row, move.start_col)
                
            # Desfazer movimento en passant
            if move.is_enpassant_move:
                self.board[move.end_row][move.end_col] = "--"  # Limpar o quadrado onde o peão moveu
                self.board[move.start_row][move.end_col] = move.piece_captured
                self.enpassant_possible = (move.end_row, move.end_col)
                
            # Desfazer movimento de peão de duas casas
            if move.piece_moved[1] == 'p' and abs(move.start_row - move.end_row) == 2:
                self.enpassant_possible = ()
                
            # Desfazer movimento de roque
            if move.is_castle_move:
                if move.end_col - move.start_col == 2:  # Roque do lado do rei
                    # Desfaz o movimento da torre
                    self.board[move.end_row][move.end_col + 1] = self.board[move.end_row][move.end_col - 1]
                    self.board[move.end_row][move.end_col - 1] = "--"
                else:  # Roque do lado da rainha
                    # Desfaz o movimento da torre
                    self.board[move.end_row][move.end_col - 2] = self.board[move.end_row][move.end_col + 1]
                    self.board[move.end_row][move.end_col + 1] = "--"
                    
            # Desfazer direitos de roque
            self.castle_rights_log.pop()  # Remover o último log
            self.current_castling_rights = self.castle_rights_log[-1]  # Restaurar os direitos anteriores
            
            # Resetar checkmate e stalemate
            self.checkmate = False
            self.stalemate = False

    def update_castle_rights(self, move):
        """Atualiza os direitos de roque com base no movimento."""
        if move.piece_moved == 'wK':
            self.current_castling_rights.wks = False
            self.current_castling_rights.wqs = False
        elif move.piece_moved == 'bK':
            self.current_castling_rights.bks = False
            self.current_castling_rights.bqs = False
        elif move.piece_moved == 'wR':
            if move.start_row == 7:
                if move.start_col == 0:  # Torre da esquerda
                    self.current_castling_rights.wqs = False
                elif move.start_col == 7:  # Torre da direita
                    self.current_castling_rights.wks = False
        elif move.piece_moved == 'bR':
            if move.start_row == 0:
                if move.start_col == 0:  # Torre da esquerda
                    self.current_castling_rights.bqs = False
                elif move.start_col == 7:  # Torre da direita
                    self.current_castling_rights.bks = False
                    
        # Se uma torre for capturada
        if move.piece_captured == 'wR':
            if move.end_row == 7:
                if move.end_col == 0:
                    self.current_castling_rights.wqs = False
                elif move.end_col == 7:
                    self.current_castling_rights.wks = False
        elif move.piece_captured == 'bR':
            if move.end_row == 0:
                if move.end_col == 0:
                    self.current_castling_rights.bqs = False
                elif move.end_col == 7:
                    self.current_castling_rights.bks = False

    def get_valid_moves(self):
        """Retorna todos os movimentos válidos considerando xeque."""
        temp_enpassant_possible = self.enpassant_possible
        temp_castle_rights = CastleRights(self.current_castling_rights.wks, 
                                         self.current_castling_rights.wqs,
                                         self.current_castling_rights.bks, 
                                         self.current_castling_rights.bqs)
        
        # 1. Gerar todos os movimentos possíveis
        moves = self.get_all_possible_moves()
        
        # 2. Para cada movimento, faça o movimento
        for i in range(len(moves) - 1, -1, -1):
            self.make_move(moves[i])
            # 3. Gerar todos os movimentos do oponente
            # 4. Ver se algum dos movimentos do oponente ataca o rei
            self.white_to_move = not self.white_to_move
            if self.in_check():
                moves.remove(moves[i])  # 5. Se atacar o rei, não é um movimento válido
            self.white_to_move = not self.white_to_move
            self.undo_move()
            
        # Verificar se não há movimentos válidos
        if len(moves) == 0:
            if self.in_check():
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False
            
        # Adicionar movimentos de roque se não estiver em xeque
        if self.white_to_move:
            self.get_castle_moves(self.white_king_location[0], self.white_king_location[1], moves)
        else:
            self.get_castle_moves(self.black_king_location[0], self.black_king_location[1], moves)
            
        self.enpassant_possible = temp_enpassant_possible
        self.current_castling_rights = temp_castle_rights
        return moves

    def in_check(self):
        """Verifica se o jogador atual está em xeque."""
        if self.white_to_move:
            return self.square_under_attack(self.white_king_location[0], self.white_king_location[1])
        else:
            return self.square_under_attack(self.black_king_location[0], self.black_king_location[1])

    def square_under_attack(self, r, c):
        """Verifica se um quadrado está sendo atacado pelo oponente."""
        self.white_to_move = not self.white_to_move  # Mudar para a perspectiva do oponente
        opp_moves = self.get_all_possible_moves()
        self.white_to_move = not self.white_to_move  # Mudar de volta
        for move in opp_moves:
            if move.end_row == r and move.end_col == c:  # O quadrado está sob ataque
                return True
        return False

    def get_all_possible_moves(self):
        """Gera todos os movimentos possíveis sem considerar xeque."""
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.white_to_move) or (turn == 'b' and not self.white_to_move):
                    piece = self.board[r][c][1]
                    self.move_functions[piece](r, c, moves)  # Chama a função apropriada com base no tipo de peça
        return moves

    def get_pawn_moves(self, r, c, moves):
        """Gera todos os movimentos possíveis para um peão."""
        if self.white_to_move:  # Peões brancos
            # Movimento para frente de uma casa
            if r > 0 and self.board[r-1][c] == "--":
                moves.append(Move((r, c), (r-1, c), self.board))
                # Movimento para frente de duas casas
                if r == 6 and self.board[r-2][c] == "--":
                    moves.append(Move((r, c), (r-2, c), self.board))
            
            # Capturas
            if r > 0 and c > 0 and self.board[r-1][c-1][0] == 'b':  # Captura à esquerda
                moves.append(Move((r, c), (r-1, c-1), self.board))
            if r > 0 and c < 7 and self.board[r-1][c+1][0] == 'b':  # Captura à direita
                moves.append(Move((r, c), (r-1, c+1), self.board))
                
            # En passant
            if self.enpassant_possible:
                if (r-1, c-1) == self.enpassant_possible and c > 0:
                    moves.append(Move((r, c), (r-1, c-1), self.board, is_enpassant_move=True))
                if (r-1, c+1) == self.enpassant_possible and c < 7:
                    moves.append(Move((r, c), (r-1, c+1), self.board, is_enpassant_move=True))
                
        else:  # Peões pretos
            # Movimento para frente de uma casa
            if r < 7 and self.board[r+1][c] == "--":
                moves.append(Move((r, c), (r+1, c), self.board))
                # Movimento para frente de duas casas
                if r == 1 and self.board[r+2][c] == "--":
                    moves.append(Move((r, c), (r+2, c), self.board))
            
            # Capturas
            if r < 7 and c > 0 and self.board[r+1][c-1][0] == 'w':  # Captura à esquerda
                moves.append(Move((r, c), (r+1, c-1), self.board))
            if r < 7 and c < 7 and self.board[r+1][c+1][0] == 'w':  # Captura à direita
                moves.append(Move((r, c), (r+1, c+1), self.board))
                
            # En passant
            if self.enpassant_possible:
                if (r+1, c-1) == self.enpassant_possible and c > 0:
                    moves.append(Move((r, c), (r+1, c-1), self.board, is_enpassant_move=True))
                if (r+1, c+1) == self.enpassant_possible and c < 7:
                    moves.append(Move((r, c), (r+1, c+1), self.board, is_enpassant_move=True))

    def get_rook_moves(self, r, c, moves):
        """Gera todos os movimentos possíveis para uma torre."""
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))  # Cima, esquerda, baixo, direita
        enemy_color = 'b' if self.white_to_move else 'w'
        for d in directions:
            for i in range(1, 8):
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:  # Dentro do tabuleiro
                    end_piece = self.board[end_row][end_col]
                    if end_piece == "--":  # Espaço vazio
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color:  # Peça inimiga
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                        break
                    else:  # Peça aliada
                        break
                else:  # Fora do tabuleiro
                    break

    def get_knight_moves(self, r, c, moves):
        """Gera todos os movimentos possíveis para um cavalo."""
        knight_moves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        ally_color = 'w' if self.white_to_move else 'b'
        for m in knight_moves:
            end_row = r + m[0]
            end_col = c + m[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_color:  # Espaço vazio ou peça inimiga
                    moves.append(Move((r, c), (end_row, end_col), self.board))

    def get_bishop_moves(self, r, c, moves):
        """Gera todos os movimentos possíveis para um bispo."""
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))  # Diagonais
        enemy_color = 'b' if self.white_to_move else 'w'
        for d in directions:
            for i in range(1, 8):
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:  # Dentro do tabuleiro
                    end_piece = self.board[end_row][end_col]
                    if end_piece == "--":  # Espaço vazio
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color:  # Peça inimiga
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                        break
                    else:  # Peça aliada
                        break
                else:  # Fora do tabuleiro
                    break

    def get_queen_moves(self, r, c, moves):
        """Gera todos os movimentos possíveis para uma rainha."""
        self.get_rook_moves(r, c, moves)
        self.get_bishop_moves(r, c, moves)

    def get_king_moves(self, r, c, moves):
        """Gera todos os movimentos possíveis para um rei."""
        king_moves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        ally_color = 'w' if self.white_to_move else 'b'
        for i in range(8):
            end_row = r + king_moves[i][0]
            end_col = c + king_moves[i][1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_color:  # Espaço vazio ou peça inimiga
                    moves.append(Move((r, c), (end_row, end_col), self.board))

    def get_castle_moves(self, r, c, moves):
        """Gera os movimentos de roque possíveis para o rei."""
        if self.square_under_attack(r, c):
            return  # Não pode fazer roque se estiver em xeque
        
        if (self.white_to_move and self.current_castling_rights.wks) or \
           (not self.white_to_move and self.current_castling_rights.bks):
            self.get_kingside_castle_moves(r, c, moves)
            
        if (self.white_to_move and self.current_castling_rights.wqs) or \
           (not self.white_to_move and self.current_castling_rights.bqs):
            self.get_queenside_castle_moves(r, c, moves)

    def get_kingside_castle_moves(self, r, c, moves):
        """Gera o movimento de roque do lado do rei."""
        if self.board[r][c+1] == '--' and self.board[r][c+2] == '--':
            if not self.square_under_attack(r, c+1) and not self.square_under_attack(r, c+2):
                moves.append(Move((r, c), (r, c+2), self.board, is_castle_move=True))

    def get_queenside_castle_moves(self, r, c, moves):
        """Gera o movimento de roque do lado da rainha."""
        if self.board[r][c-1] == '--' and self.board[r][c-2] == '--' and self.board[r][c-3] == '--':
            if not self.square_under_attack(r, c-1) and not self.square_under_attack(r, c-2):
                moves.append(Move((r, c), (r, c-2), self.board, is_castle_move=True))


class CastleRights:
    def __init__(self, wks, wqs, bks, bqs):
        self.wks = wks  # white king side
        self.wqs = wqs  # white queen side
        self.bks = bks  # black king side
        self.bqs = bqs  # black queen side


class Move:
    # Mapeamento de coordenadas para notação algébrica
    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4,
                     "5": 3, "6": 2, "7": 1, "8": 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3,
                     "e": 4, "f": 5, "g": 6, "h": 7}
    cols_to_files = {v: k for k, v in files_to_cols.items()}

    def __init__(self, start_sq, end_sq, board, is_enpassant_move=False, is_castle_move=False):
        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        # Promoção de peão
        self.is_pawn_promotion = (self.piece_moved == 'wp' and self.end_row == 0) or \
                                (self.piece_moved == 'bp' and self.end_row == 7)
        # En passant
        self.is_enpassant_move = is_enpassant_move
        if self.is_enpassant_move:
            self.piece_captured = 'wp' if self.piece_moved == 'bp' else 'bp'
        # Roque
        self.is_castle_move = is_castle_move
        
        self.is_capture = self.piece_captured != "--"
        self.moveID = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def get_chess_notation(self):
        """Retorna a notação algébrica do movimento."""
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)

    def get_rank_file(self, r, c):
        """Converte coordenadas de matriz em notação algébrica."""
        return self.cols_to_files[c] + self.rows_to_ranks[r]


def draw_game_state(screen, gs, valid_moves, sq_selected):
    """Desenha o estado atual do jogo."""
    draw_board(screen)  # Desenha os quadrados do tabuleiro
    highlight_squares(screen, gs, valid_moves, sq_selected)  # Destaca quadrados selecionados e movimentos válidos
    draw_pieces(screen, gs.board)  # Desenha as peças
    draw_game_info(screen, gs)  # Desenha informações do jogo (xeque, xeque-mate, etc.)


def draw_board(screen):
    """Desenha os quadrados do tabuleiro."""
    colors = [LIGHT_SQUARE, DARK_SQUARE]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def highlight_squares(screen, gs, valid_moves, sq_selected):
    """Destaca o quadrado selecionado e os movimentos válidos."""
    if sq_selected != ():
        r, c = sq_selected
        # Verificar se o quadrado selecionado possui uma peça que pode ser movida
        if gs.board[r][c][0] == ('w' if gs.white_to_move else 'b'):
            # Destacar quadrado selecionado
            s = pygame.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(150)  # Transparência
            s.fill(HIGHLIGHT)
            screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))
            
            # Destacar movimentos válidos
            s.fill(HIGHLIGHT_VALID)
            for move in valid_moves:
                if move.start_row == r and move.start_col == c:
                    screen.blit(s, (move.end_col * SQ_SIZE, move.end_row * SQ_SIZE))


def draw_pieces(screen, board):
    """Desenha as peças no tabuleiro."""
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":  # Não é um espaço vazio
                screen.blit(IMAGES[piece], pygame.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_game_info(screen, gs):
    """Desenha informações do jogo, como xeque, xeque-mate, etc."""
    font = pygame.font.SysFont("Arial", 20, True)
    
    # Turno
    turn_text = "Turno: " + ("Brancas" if gs.white_to_move else "Pretas")
    text_surface = font.render(turn_text, True, WHITE)
    text_rect = text_surface.get_rect(topright=(WIDTH-10, 10))
    screen.blit(text_surface, text_rect)
    
    # Status (xeque, xeque-mate)
    status_text = ""
    if gs.checkmate:
        status_text = "Xeque-mate! " + ("Pretas" if gs.white_to_move else "Brancas") + " vencem!"
    elif gs.stalemate:
        status_text = "Empate por afogamento!"
    elif gs.in_check():
        status_text = "Xeque!"
        
    if status_text:
        text_surface = font.render(status_text, True, WHITE)
        text_rect = text_surface.get_rect(topleft=(10, 10))
        screen.blit(text_surface, text_rect)
        
    # Instruções
    if gs.checkmate or gs.stalemate:
        restart_text = "Pressione R para reiniciar o jogo"
        text_surface = font.render(restart_text, True, WHITE)
        text_rect = text_surface.get_rect(center=(WIDTH//2, HEIGHT-20))
        screen.blit(text_surface, text_rect)


def main():
    """Função principal do jogo."""
    # Carregar imagens
    load_images()
    
    # Inicializar estado do jogo
    gs = GameState()
    valid_moves = gs.get_valid_moves()
    move_made = False  # Flag para quando um movimento for realizado
    animate = False  # Flag para quando devemos animar um movimento
    game_over = False  # Flag para quando o jogo acabar
    
    # Rastreando a posição inicial e final do clique do mouse
    sq_selected = ()  # Nenhum quadrado inicialmente (linha, coluna)
    player_clicks = []  # Rastreia os cliques do jogador (dois cliques)
    
    # Loop principal do jogo
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            # Manipulador de mouse
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not game_over:
                    location = pygame.mouse.get_pos()  # (x, y) localização do mouse
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    
                    # Verificar se o jogador clicou no mesmo quadrado duas vezes (deselecionar)
                    if sq_selected == (row, col):
                        sq_selected = ()  # Deselecionar
                        player_clicks = []  # Limpar cliques
                    else:
                        sq_selected = (row, col)
                        player_clicks.append(sq_selected)  # Adicionar 1º e 2º cliques
                    
                    # Se for o segundo clique, mover a peça
                    if len(player_clicks) == 2:
                        move = Move(player_clicks[0], player_clicks[1], gs.board)
                        for i in range(len(valid_moves)):
                            if move == valid_moves[i]:
                                gs.make_move(valid_moves[i])
                                move_made = True
                                animate = True
                                sq_selected = ()  # Resetar cliques do usuário
                                player_clicks = []
                        if not move_made:
                            player_clicks = [sq_selected]  # Manter o último clique
            
            # Manipulador de teclado
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:  # Desfazer quando 'z' é pressionado
                    gs.undo_move()
                    move_made = True
                    animate = False
                    game_over = False
                    
                if event.key == pygame.K_r:  # Resetar o jogo quando 'r' é pressionado
                    gs = GameState()
                    valid_moves = gs.get_valid_moves()
                    sq_selected = ()
                    player_clicks = []
                    move_made = False
                    animate = False
                    game_over = False
        
        # Atualizar movimentos válidos
        if move_made:
            if animate:
                animate = False  # Apenas animar uma vez
            valid_moves = gs.get_valid_moves()
            move_made = False
            
        # Verificar fim de jogo
        if gs.checkmate or gs.stalemate:
            game_over = True
        
        # Desenhar o estado do jogo
        draw_game_state(screen, gs, valid_moves, sq_selected)
        
        # Atualizar a tela
        pygame.display.flip()
        
        # Limitar FPS
        clock.tick(MAX_FPS)
    
    # Sair do Pygame
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()