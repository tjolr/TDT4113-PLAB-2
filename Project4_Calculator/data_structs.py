'''Data structs, with queue and stack'''


class Container:
    '''Container class is superclass for queue and stack'''
    def __init__(self):
        self.items = []

    def size(self):
        '''Returns number of elements in self.items'''
        return len(self.items)

    def is_empty(self):
        '''Check if self.items is empty'''
        return self.size() <= 0

    def push(self, item):
        '''Add item to the end of self.items'''
        self.items.append(item)

    def pop(self):
        '''Pops off the correct element of self.items and returns it'''
        raise NotImplementedError

    def peek(self):
        '''Return the top element without removing it'''
        raise NotImplementedError


class Queue(Container):
    '''Queue class'''

    def peek(self):
        '''Returns the first element in the list, without removing it'''
        assert not self.is_empty()
        return self.items[0]

    def pop(self):
        '''Pops off the first element'''
        assert not self.is_empty()
        return self.items.pop(0)


class Stack(Container):
    '''Queue class'''

    def peek(self):
        '''Returns the last element in the list, without removing it'''
        assert not self.is_empty()
        return self.items[-1]

    def pop(self):
        '''Pops off the last element'''
        assert not self.is_empty()
        return self.items.pop(-1)


def main():
    '''Main method'''
    queue = Queue()
    for i in range(1, 300, 20):
        queue.push(i)

    print(f"popping of {queue.pop()}")

    for i in range(5):
        print(f"peeking {queue.peek()}")
        print(f"popping of {queue.pop()}")


# main()
