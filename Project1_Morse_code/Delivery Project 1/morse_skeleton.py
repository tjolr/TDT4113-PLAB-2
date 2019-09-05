#imports the serial library
import serial

#Connecting to the USB to get data from Serial from the correct port, at band 9600
#Defining what port the arduino is connected to
#Returns serial from the Arduino
def basic_connect(arport='/dev/cu.wchusbserial1410'):
    return serial.Serial(arport,9600,timeout=.1)


#Constants for the input symbols from the arduino
_dot = 0
_dash = 1
_symbol_pause = 2
_word_pause = 3

# Morse Code Class
class Morsecode():

    #Dictianory with morse_code symbols
    _morse_codes = {'01':'a','1000':'b','1010':'c','100':'d','0':'e','0010':'f','110':'g','0000':'h','00':'i','0111':'j',
               '101':'k','0100':'l','11':'m','10':'n','111':'o','0110':'p','1101':'q','010':'r','000':'s','1':'t',
               '001':'u','0001':'v','011':'w','1001':'x','1011':'y','1100':'z','01111':'1','00111':'2','00011':'3',
               '00001':'4','00000':'5','10000':'6','11000':'7','11100':'8','11110':'9','11111':'0'}

    #SOS: ... --- ...
    #BOAT: -... --- .- -
    #FUN: ..-. ..- -.


    # This is where you set up the connection to the serial port.
    def __init__(self,sport=True):
        if sport:
            self.serial_port = basic_connect()
            self.current_symbol = ""
            self.current_word = ""
        self.reset()

    def reset(self):
        self.current_message = ''
        self.current_word = ''
        self.current_symbol = ''


    def decoding_loop(self):
        """Loop that recieves input from serial stream and returns every byte to methods in this class"""
        while True:
            s = self.read_one_signal(self.serial_port)
            for byte in s:
                self.process_signal(int(chr(byte)))


    def read_one_signal(self,port=None):
        '''Method recieves the serial ports, and uses the connection to read lines from the serial input'''
        connection = port if port else self.serial_port
        while True:
            # Reads the input from the arduino serial connection
            data = connection.readline()
            if data:
                return data


    # Recieves an int from 0-3 with dash, dot or pauses
    #Delegates them to other handling methods
    def process_signal(self,sig):
        if sig == _dot or sig == _dash:
            self.update_current_symbol(sig)
        elif sig == _symbol_pause:
            self.handle_symbol_end()
        elif sig == _word_pause:
            self.handle_word_end()
        else:
            print(sig, " could not read process signal correctly")

    #Adds a dot or dash to an symbol under construction
    def update_current_symbol(self, sig):
        self.current_symbol += str(sig)

    #When all the dots and dashes are made, it creates a letter with the responding code
    #If the collection of 0 and 1 is not recognized in the dictinary _morse_codes it returns a star
    def handle_symbol_end(self):
        if self.current_symbol == "":
            letter = ""
        else:
            try:
                letter = self._morse_codes[self.current_symbol]
            except:
                letter = "*"

        self.update_current_word(letter)
        self.current_symbol = ''


    #Adds a letter to the current word under construction
    def update_current_word(self, symbol):
        self.current_word += str(symbol)

    #when all the letters in one word is made
    def handle_word_end(self):
        self.handle_symbol_end()
        self.handle_message_update(self.current_word)
        self.current_word = ''

    #Adds the word under construction to the message, and prints the message
    def handle_message_update(self, word):
        self.current_message += word + " "
        print(self.current_message)



#Main method to run the sample
def main():
    morse_coder = Morsecode()
    morse_coder.decoding_loop()

main()