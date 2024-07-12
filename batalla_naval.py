class Ship:
    """
    Clase base para los barcos.
    """

    def __init__(self, name, size):
        
        # Inicializa un barco con su nombre, tamaño y otras propiedades.
        # name : Nombre del barco.
        # size : Tamaño del barco en número de casillas.
        self.name = name
        self.size = size
        self.positions = []  # Lista de posiciones ocupadas por el barco
        self.hits = 0  # Número de impactos recibidos por el barco

    def place_ship(self, start_row, start_col, direction, board):
        #Coloca el barco en el tablero.
        #start_row : Fila inicial de colocación del barco.
        #start_col : Columna inicial de colocación del barco.
        #direction : Dirección de colocación ('H' para horizontal, 'V' para vertical).
        #board: Tablero en el que se coloca el barco.
    
        positions = []

        if direction == 'H':
            # Verifica si el barco cabe en la dirección horizontal
            if start_col + self.size > len(board[0]):
                return False
            
            # Verifica si las posiciones en el tablero están libres
            for i in range(self.size):
                if board[start_row][start_col + i] != ' ':
                    return False
                positions.append((start_row, start_col + i))
        
        elif direction == 'V':
            # Verifica si el barco cabe en la dirección vertical
            if start_row + self.size > len(board):
                return False
            
            # Verifica si las posiciones en el tablero están libres
            for i in range(self.size):
                if board[start_row + i][start_col] != ' ':
                    return False
                positions.append((start_row + i, start_col))
        
        else:
            return False  # Dirección no válida
        
        # Si todo está bien, coloca el barco en el tablero y guarda las posiciones
        for pos in positions:
            board[pos[0]][pos[1]] = self.name[0]
        self.positions = positions
        return True

    def hit(self):
        #Registra un impacto en el barco.

        self.hits += 1
        return self.hits == self.size


class Destroyer(Ship):
    
    #Clase para el barco Destructor, hereda de Ship.
    
    def __init__(self):
        super().__init__('Destructor', 2)


class Submarine(Ship):
    
    #Clase para el barco Submarino, hereda de Ship.

    def __init__(self):
        super().__init__('Submarino', 3)


class Battleship(Ship):
    #Clase para el barco Acorazado, hereda de Ship.
    def __init__(self):
        super().__init__('Acorazado', 4)


class Player:
    
    #Clase que representa a un jugador
    

    def __init__(self, name):
        
        #Inicializa un jugador con un nombre, un tablero vacío, una lista de barcos y registros de ataques.

       
        self.name = name
        self.board = [[' ' for _ in range(10)] for _ in range(10)]  # Tablero vacío
        self.ships = []  # Lista de barcos que el jugador posee
        self.hits = [[' ' for _ in range(10)] for _ in range(10)]  # Registros de los ataques 

    def place_ships(self):
        
        #Permite al jugador colocar sus barcos en el tablero.
        
        ships = [Destroyer(), Submarine(), Battleship()]  # Lista de tipos de barcos 

        for ship in ships:
            while True:
                print(f"{self.name}, coloca tu {ship.name} de tamaño {ship.size}.")
                start_row = int(input("Fila inicial: "))
                start_col = int(input("Columna inicial: "))
                direction = input("Dirección (H para horizontal, V para vertical): ").upper()

                if ship.place_ship(start_row, start_col, direction, self.board):
                    self.ships.append(ship)  # Agrega el barco a la lista de barcos del jugador
                    self.print_board(self.board)  # Muestra el estado actual del tablero
                    break
                else:
                    print("Posición no válida. Inténtalo de nuevo.")

    def print_board(self, board):
        #Imprime el tablero
        for row in board:
            print(" ".join(row))
        print()

    def attack(self, opponent):
        #Realiza el ataque
        while True:
            print(f"{self.name}, elige una posición para atacar.")
            row = int(input("Fila: "))
            col = int(input("Columna: "))

            if 0 <= row < 10 and 0 <= col < 10:
                if opponent.board[row][col] == ' ':
                    print("Agua!")
                    self.hits[row][col] = 'A'
                    opponent.board[row][col] = 'A'  # Marca el agua en el tablero 
                    break
                elif opponent.board[row][col] != 'A':
                    print("Impacto!")
                    self.hits[row][col] = 'T'
                    
                    # Verifica qué barco ha sido impactado y si está completamente hundido
                    for ship in opponent.ships:
                        if (row, col) in ship.positions:
                            if ship.hit():
                                print(f"¡Hundido! Has hundido el {ship.name}.")
                            break
                    opponent.board[row][col] = 'T'  # Marca el impacto en el tablero del oponente
                    break
                else:
                    print("Ya has atacado esta posición. Intenta de nuevo.")
            else:
                print("Posición no válida. Intenta de nuevo.")

    def all_ships_sunk(self):
        #Verifica si todos los barcos del jugador han sido hundidos.

        
        return all(ship.hits == ship.size for ship in self.ships)


class BattleshipGame:
    # Clase que representa el juego de Batalla Naval entre dos jugadores.

    def __init__(self):
        self.player1 = Player("Jugador 1")
        self.player2 = Player("Jugador 2")

    def play(self):
        print("Bienvenido al juego de Batalla Naval!")
        print("Jugador 1 coloca sus barcos.")
        self.player1.place_ships()
        print("Jugador 2 coloca sus barcos.")
        self.player2.place_ships()

        current_player = self.player1
        opponent = self.player2

        while True:
            current_player.attack(opponent)
            if opponent.all_ships_sunk():
                print(f"¡{current_player.name} ha ganado el juego!")
                break
            current_player, opponent = opponent, current_player


# Crear una instancia del juego y jugar
if __name__ == "__main__":
    game = BattleshipGame()
    game.play()
