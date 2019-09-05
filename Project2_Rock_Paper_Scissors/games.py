'''Games'''
import matplotlib.pyplot as plt
import players

class SingleGame():
    '''SingleGame'''

    def __init__(self, player1, player2):
        '''Constructor init'''
        self.player1 = player1
        self.player2 = player2
        self.player1_points = 0
        self.player2_points = 0
        self.player1_action = None
        self.player2_action = None
        self.result_string = ""

    def execute_game(self):
        '''Execute game'''
        self.player1_action = self.player1.choose_reaction()
        self.player2_action = self.player2.choose_reaction()

        self.player1.recieve_result(self.player2_action)
        self.player2.recieve_result(self.player1_action)

        if self.player1_action == self.player2_action:
            self.player1_points += 0.5
            self.player2_points += 0.5
            self.result_string = "tie"
        else:
            if self.player1_action > self.player2_action:
                self.player1_points += 1
                self.result_string = f"{self.player1} won against {self.player2}"
            else:
                self.player2_points += 1
                self.result_string = f"{self.player2} won against {self.player1}"

    def __str__(self):
        return f"{self.player1} chose {self.player1_action}, " \
               f"and {self.player2} chose {self.player2_action}. Result: {self.result_string}"

class MultipleGames():
    '''Multiple Games class'''

    def __init__(self, player1, player2, number_of_games):
        self.player1 = player1
        self.player2 = player2
        self.player1_points = 0
        self.player2_points = 0
        self.number_of_games = number_of_games

    def arrange_singlegame(self):
        '''Arranging one single game'''
        SINGLEGAME = SingleGame(self.player1, self.player2)
        SINGLEGAME.execute_game()
        self.player1_points += SINGLEGAME.player1_points
        self.player2_points += SINGLEGAME.player2_points

        print(SINGLEGAME)

    def arrange_tournament(self):
        '''Tournament'''
        player1_score_list = [0]
        player2_score_list = [0]

        for i in range(1, self.number_of_games + 1):
            self.arrange_singlegame()
            player1_score_list.append(self.player1_points / i)
            player2_score_list.append(self.player2_points / i)

        result_string = f"\n{self.player1} won " \
                        f"{(self.player1_points * 100)/self.number_of_games}% " \
                       f"of the games while {self.player2} won " \
                       f"{(self.player2_points * 100)/self.number_of_games}% " \
                        f"of the games \n"
        result_string += "\nFINAL RESULT: "
        if self.player1_points == self.player2_points:
            result_string += "TIE --"
        elif self.player1_points > self.player2_points:
            result_string += f'{self.player1} WON!'
            plt.plot(player1_score_list)
            plt.ylabel(f'{self.player1} score rate')
        else:
            result_string += f'{self.player2} WON!'
            plt.plot(player2_score_list)
            plt.ylabel(f'{self.player2} score rate')

        print(result_string)

        #Showing Matplotlib
        plt.show()

def main():
    '''Main Method'''
    RANDOM_PLAYER = players.RandomPlayer()
    SEQUENTIAL_PLAYER = players.SequentialPlayer()
    MOSTCOMMON_PLAYER = players.MostCommonPlayer()
    HISTORIC_PLAYER = players.HistoricPlayer(3)

    MULTIPLE_GAMES = MultipleGames(SEQUENTIAL_PLAYER, RANDOM_PLAYER, 100)
    MULTIPLE_GAMES.arrange_tournament()

main()
