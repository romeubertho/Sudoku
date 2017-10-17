import math

class Sudoku():

    """Sudoku Class which represent game state"""

    # Inicia o tabuleiro do jogo
    def __init__(self, game):
        self._game = game
        self._board_size = len(game)
        self._domain = []
        for _ in range(self._board_size):
            row_domain = []
            for _ in range(self._board_size):
                row_domain.append([i + 1 for i in range(self._board_size)]) # Criando os dominios na matriz
            self._domain.append(row_domain)
        self._box_size = int(math.sqrt(self._board_size))

    # Checa se eh possivel colocar o numero na posicao row col
    def validAssign(self, row, col, number):
        return self.checkCol(col, number) and \
                self.checkRow(row, number) and \
                self.checkBox(row, col, number)

    # Checa se nao existe nenhum numero igual na linha
    def checkRow(self, row, number):
        for j in range(self._board_size):
            if self._game[row][j] == number:
                return False

        return True

    # Checa se nao existe nenhum numero igual na coluna
    def checkCol(self, col, number):
        for i in range(self._board_size):
            if self._game[i][col] == number:
                return False

        return True
    # Checa se nao existe nenhum numero igual na caixa    
    def checkBox(self, row, col, number):
        lower_i = int(self._box_size * math.floor(row/self._box_size)) #verificando os limites da caixa
        lower_j = int(self._box_size * math.floor(col/self._box_size)) #verificando os limites da caixa
        for row in range(lower_i, lower_i + self._box_size):
            for col in range(lower_j, lower_j + self._box_size):
                if self._game[row][col] == number:
                    return False
        return True
    
    # Mostra o tabuleiro
    def printGame(self):
        for line in self._game:
            print(str(line))

    # Resolvendo o sudoku
    def solve(self, row=0, col=0):
        if col == self._board_size:
            return True

        # Percorre todas as linhas e colunas do tabuleiro
        next_row = (row + 1) % self._board_size
        next_col = col + 1 if next_row == 0 else col

        # Chama a funcao para resolver o jogo
        if self._game[row][col] != 0:
            return self.solve(next_row, next_col)

        # Verificando as possiveis jogadas
        for number in self._domain[row][col]:
            if self.validAssign(row, col, number): # Verifica se pode fazer a jogada 
                if self.assign(row, col, number): # Retira os valores do dominio de outras posicoes afetadas e faz a jogada
                # caso retorne False, quer dizer que o dominio de alguma posica zerou
                    self.remove(row, col) # Entao ele coloca os valores retirados de volta nos respectivos dominios
                    continue
                if self.solve(next_row, next_col):
                    return True
                self.remove(row, col)
        return False

    # Faz toda a parte de retirar os valores do dominio de outras posicoes apos um valor ser colocado e tambem 
    # seta o valor number na posicao row col
    def assign(self, row, col, number):
        self._game[row][col] = number
        
        # Percorre os valores da coluna para atualizar o dominio
        for i in range(self._board_size):
            if number in self._domain[i][col]:
                if len(self._domain[i][col]) == 1 and self._game[i][col] == 0:
                    return False
                self._domain[i][col].remove(number)

        # Percorre os valores da linha para atualizar o dominio
        for j in range(self._board_size):
            if number in self._domain[row][j]:
                if len(self._domain[row][j]) == 1 and self._game[row][j] == 0:
                    return False
                self._domain[row][j].remove(number)

        # Percorrendo a caixa
        lower_i = int(self._box_size * math.floor(row/self._box_size))
        lower_j = int(self._box_size * math.floor(col/self._box_size))
        
        # Percorrendo os valores da caixa para atualizar os dominios
        for row in range(lower_i, lower_i + self._box_size):
            for col in range(lower_j, lower_j + self._box_size):
                if number in self._domain[row][col]:
                    if len(self._domain[row][col]) == 1 and self._game[row][col] == 0:
                        return False
                    self._domain[row][col].remove(number)

    # Logica inversa do assign, coloca os valores de volta no dominio e seta posica row col para 0
    def remove(self, row, col):
        number = self._game[row][col]
        self._game[row][col] = 0
        
        # Percorre as colunas para arrumar os valores de volta no dominio
        for i in range(self._board_size):
            if number not in self._domain[i][col]:
                self._domain[i][col].append(number)

        # Percorre a linha para arrumar os valores de volta no dominio
        for j in range(self._board_size):
            if number not in self._domain[row][j]:
                self._domain[row][j].append(number)

        # Percorre a caixa para arrumar os valores de volta no dominio
        lower_i = int(self._box_size * math.floor(row/self._box_size))
        lower_j = int(self._box_size * math.floor(col/self._box_size))
        for row in range(lower_i, lower_i + self._box_size):
            for col in range(lower_j, lower_j + self._box_size):
                if number not in self._domain[row][col]:
                    self._domain[row][col].append(number)
