'''Logics in the task'''
import numbers
import re
import numpy
import data_structs


class Function:
    '''Function class function'''

    def __init__(self, func):
        '''Constructor'''
        self.func = func

    def execute(self, element, debug=True):
        '''Executes function'''
        if not isinstance(element, numbers.Number):
            raise TypeError("Cannot execute func if element is not a number")
        exe_result = self.func(element)

        if debug is True:
            print(
                "Function: " +
                self.func.__name__ +
                "({:f}) = {:f}".format(
                    element,
                    exe_result))

        return exe_result


class Operator:
    '''Operator class'''

    def __init__(self, operator, strength):
        '''Constructor'''
        self.operator = operator
        self.strength = strength

    def execute(self, element1, element2, debug=True):
        '''Executes'''

        if not isinstance(
                element1,
                numbers.Number) or not isinstance(
                element2,
                numbers.Number):
            raise TypeError(
                "Cannot execute operation if element is not a number")

        result = self.operator(element1, element2)

        if debug:
            print(
                f'Operator {self.operator.__name__} operates {element1}, '
                f'{element2} and returns {result}')

        return result


class Calculator():
    '''Calculator main class'''

    def __init__(self):
        '''Constructor'''
        self.functions = {
            'EXP': Function(numpy.exp),
            'LOG': Function(numpy.log),
            'SIN': Function(numpy.sin),
            'COS': Function(numpy.cos),
            'SQRT': Function(numpy.sqrt)
        }

        self.operators = {
            'PLUSS': Operator(numpy.add, 0),
            'GANGE': Operator(numpy.multiply, 1),
            'DELE': Operator(numpy.divide, 1),
            'MINUS': Operator(numpy.subtract, 0)
        }

        self.output_queue = data_structs.Queue()

    def execute(self):
        '''Calculating'''
        print("Executing")

        stack = data_structs.Stack()

        while not self.output_queue.is_empty():
            element = self.output_queue.pop()
            if isinstance(element, numbers.Number):
                stack.push(element)
            elif isinstance(element, Function):
                func_result = element.execute(stack.pop())
                stack.push(func_result)
            elif isinstance(element, Operator):
                number1, number2 = stack.pop(), stack.pop()
                op_result = element.execute(number2, number1)
                stack.push(op_result)

        # When the queue is empty, the stack is having only 1 element
        return stack.pop()



    def shunting_yard(self, input_list):
        '''Takes an list of input elements, and places them in the correct order on the calculators
        output queue'''
        operator_stack = data_structs.Stack()
        for element in input_list:
            if isinstance(element, numbers.Number):
                self.output_queue.push(element)
            elif isinstance(element, Function):
                operator_stack.push(element)
            elif element == '(':
                operator_stack.push(element)
            elif element == ')':
                while operator_stack.peek() != '(':
                    self.output_queue.push(operator_stack.pop())
                operator_stack.pop()
            elif isinstance(element, Operator):
                while operator_stack.size() > 0 and (
                    (isinstance(
                        operator_stack.peek(),
                        Operator) and operator_stack.peek().strength >= element.strength) or isinstance(
                        operator_stack.peek(),
                        Function)):
                    self.output_queue.push(operator_stack.pop())
                operator_stack.push(element)

        while operator_stack.size() > 0:
            self.output_queue.push(operator_stack.pop())


    def text_parse(self, input_text, debug=True):
        '''Takes an string as input, parses it to a list with objects'''
        output_list = []
        input_string = input_text.replace(" ", "").upper()
        while input_string:
            numbers = re.search("^[-0123456789.]+", input_string)
            parentheses = re.search("^[()]{1}", input_string)

            func_targets = '|'.join(["^" + func for func in self.functions.keys()])
            functions = re.search(func_targets, input_string)

            op_targets = '|'.join(["^" + op for op in self.operators.keys()])
            operators = re.search(op_targets, input_string)

            slice_index = 0
            if numbers:
                if re.search("[.]+", numbers.group(0)):
                    output_list.append(float(numbers.group(0)))
                else:
                    output_list.append(int(numbers.group(0)))
                slice_index = numbers.end(0)
            elif functions:
                output_list.append(self.functions[functions.group(0)])
                slice_index = functions.end(0)
            elif operators:
                output_list.append(self.operators[operators.group(0)])
                slice_index = operators.end(0)
            elif parentheses:
                output_list.append(parentheses.group(0))
                slice_index = parentheses.end(0)

            input_string = input_string[slice_index:]

        if debug:
            print("Output List from text_parse:", output_list)

        return output_list

    def calculate_expressions(self, txt):
        '''Calculating input from text and executes'''
        input_list = self.text_parse(txt)
        self.shunting_yard(input_list)
        return self.execute()


CALC = Calculator()

CALC_RESULT = CALC.calculate_expressions(
    "((15 DELE (7 MINUS (1 PLUSS 1))) GANGE 3) MINUS EXP(2)")
print(f'\nResult: {CALC_RESULT}')
