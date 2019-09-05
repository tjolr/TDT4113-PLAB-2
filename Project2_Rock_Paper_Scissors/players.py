'''All the player classes and the Action class'''
import random

class Action():
    '''Creates the action object'''
    def __init__(self, type):
        self.type = type

    def __eq__(self, other):
        return self.type == other.type

    def __gt__(self, other):
        if self.type == 'stone' and other.type == 'scissor' \
                or self.type == 'scissor' and other.type == 'paper' \
                or self.type == 'paper' and other.type == 'stone':
            return True
        return False

    def __str__(self):
        return self.type

ACTIONS = [Action("stone"), Action("scissor"), Action("paper")]

class RandomPlayer():
    '''Player that makes a random reaction'''
    def __init__(self):
        '''Constructor'''
        self.actions = ACTIONS
        self.name = "Random"

    def choose_reaction(self):
        '''Makes a random reaction'''
        return self.actions[random.randint(0, len(self.actions) - 1)]

    def recieve_result(self, opponent_action):
        '''Does noething with the needed information'''

    def specify_name(self):
        '''Returns the name of this class'''
        return self.name

    def __str__(self):
        '''String method to print out the name of this player'''
        return self.name

class SequentialPlayer():
    '''Makes reaction in sequential order'''
    def __init__(self):
        '''Constructor'''
        self.actions = ACTIONS
        self.name = "Sequential"
        self.iterator = 0

    def choose_reaction(self):
        '''Makes a sequential reaction'''
        index = self.iterator % len(self.actions)
        self.iterator += 1
        return self.actions[index]

    def recieve_result(self, opponent_action):
        '''Does nothing with the recieved result'''


    def specify_name(self):
        '''Returns the name of this class'''
        return self.name

    def __str__(self):
        return self.name


def most_frequent(list):
    '''Returns the most frequent element from a list'''
    return max(set(list), key=list.count)


class MostCommonPlayer():
    '''Player that choose the action that the opponent player is using most common'''
    def __init__(self):
        '''Constructor'''
        self.actions = ACTIONS
        self.name = "MostCommon"
        self.opponent_actions = []

    def choose_reaction(self):
        '''Makes a sequential reaction'''
        if not self.opponent_actions:
            return self.actions[random.randint(0, len(self.actions) - 1)]

        string_actions = [str(action) for action in self.opponent_actions]
        return Action(most_frequent(string_actions))

    def recieve_result(self, opponent_action):
        '''Adds the opponent action to a list'''
        self.opponent_actions.append(opponent_action)

    def specify_name(self):
        '''Returns the name of this class'''
        return self.name

    def __str__(self):
        return self.name


class HistoricPlayer():
    '''Find sequences of actions, and predicts what the opponent will do next'''
    def __init__(self, remember):
        '''Constructor'''
        self.actions = ACTIONS
        self.name = "Historic"
        self.opponent_actions = []
        self.remember = remember

    def choose_reaction(self):
        '''Makes a sequential reaction'''
        if not self.opponent_actions:
            return self.actions[random.randint(0, len(self.actions) - 1)]
        else:
            sub_seq = self.opponent_actions[len(
                self.opponent_actions) - self.remember:]

            freq_after_subseq = []

            for action in range(0, len(self.opponent_actions) - self.remember):
                for i in range(self.remember):
                    if self.opponent_actions[action + i] != sub_seq[i]:
                        break
                    else:
                        if i == self.remember - 1:
                            freq_after_subseq.append(
                                self.opponent_actions[action + self.remember])
                        else:
                            pass

            freq_after_subseq_string = [
                str(action) for action in freq_after_subseq]

            most_frequent_after_subseq = None
            if len(freq_after_subseq_string) >= 1:
                most_frequent_after_subseq = most_frequent(
                    freq_after_subseq_string)

            print(f"most frequent {most_frequent_after_subseq}")

            chosen_action = str(
                self.actions[random.randint(0, len(self.actions) - 1)])

            for i in range(len(self.actions)):
                if most_frequent_after_subseq == str(self.actions[i]):
                    chosen_action = str(
                        self.actions[(i - 1) % len(self.actions)])

            print(f"chosen action: {chosen_action}")

            return Action(chosen_action)

    def recieve_result(self, opponent_action):
        '''Adds the opponent reaction to a list'''
        self.opponent_actions.append(opponent_action)

    def specify_name(self):
        '''Returns the name of this class'''
        return self.name

    def __str__(self):
        return self.name
