'''Ciphers file'''
import random
import crypto_utils


class Cipher():
    '''Cipher class'''

    def __init__(self):
        '''Constructor'''
        self.alphabet = [chr(i) for i in range(32, 127)]
        self.alphabet_size = len(self.alphabet)
        self.clear_text = ""
        self.code = ""

    def encode(self, clear_text, key):
        '''Dummy method'''

    def decode(self, code, key):
        '''Dummy method'''

    def verify(self, clear_text, encode_key, decode_key):
        '''Verify cipher'''
        encoded = self.encode(clear_text, encode_key)
        decoded = self.decode(encoded, decode_key)
        return encoded == decoded

class Caesar(Cipher):
    '''Caesar cipher'''

    def encode(self, clear_text, key):
        '''Encoding'''
        self.code = ""
        for letter in clear_text:
            self.code += self.alphabet[(self.alphabet.index(letter) + key) %
                                       self.alphabet_size]
        return self.code

    def decode(self, code, key):
        '''Decode'''
        self.code = ""
        return self.encode(code, key)

    def generate_keys(self):
        '''Generating keys for Caesar'''
        key1 = random.randint(0, self.alphabet_size - 1)
        key2 = self.alphabet_size - key1
        return key1, key2

    def get_possible_keys(self):
        '''Returning possible keys for this Cipher'''
        return [i for i in range(0, self.alphabet_size)]


class Multiplication(Cipher):
    '''Caesar cipher'''

    def generate_keys(self):
        '''Generating keys for Multiplication'''
        key1 = random.randint(1, self.alphabet_size)
        key2 = crypto_utils.modular_inverse(key1, self.alphabet_size)
        while not key2:
            key1 = random.randint(1, self.alphabet_size - 1)
            key2 = crypto_utils.modular_inverse(key1, self.alphabet_size)
        return key1, key2

    def get_possible_keys(self):
        '''Returning possible keys for this Cipher'''
        key_list = []
        for i in range(self.alphabet_size):
            possible_key = crypto_utils.modular_inverse(i, self.alphabet_size)
            if possible_key:
                key_list.append(possible_key)
        return key_list

    def encode(self, clear_text, key):
        '''Encoding'''
        self.code = ""
        for letter in clear_text:
            self.code += self.alphabet[(self.alphabet.index(letter)
                                        * key) % self.alphabet_size]
        return self.code

    def decode(self, code, key):
        '''Decoding'''
        self.code = ""
        return self.encode(code, key)


class Affine(Cipher):
    '''Affine cipher'''
    caesar = Caesar()
    mult = Multiplication()

    def generate_keys(self):
        '''Generating keys for Affine'''
        caesar_keys = self.caesar.generate_keys()
        mult_keys = self.mult.generate_keys()
        return caesar_keys + mult_keys

    def get_possible_keys(self):
        '''Possible keys'''
        possible_keys = []
        caesar_keys = self.caesar.get_possible_keys()
        mult_keys = self.mult.get_possible_keys()

        for caesar_key in caesar_keys:
            for mult_key in mult_keys:
                possible_keys.append((mult_key, caesar_key))
        return possible_keys

    def encode(self, clear_text, key):
        '''Encoding'''
        self.code = ""
        self.code = self.mult.encode(clear_text, key[0])
        self.code = self.caesar.encode(self.code, key[1])

        return self.code

    def decode(self, code, key):
        '''Decode'''
        self.code = ""
        self.code = self.caesar.decode(code, key[1])
        self.code = self.mult.decode(self.code, key[0])

        return self.code


class Unbreakable(Cipher):
    '''Class Unbreakable'''

    def generate_keys(self):
        '''Generating keys for Caesar'''
        word_key = "kiev"
        word_key_decrypt = self.generate_decryption_key(word_key)
        return word_key, word_key_decrypt

    def generate_decryption_key(self, key):
        '''Generating a decryption key based on the original key'''
        decrypting_key = ""
        for letter in enumerate(key):
            letter_index = self.alphabet.index(letter[1])
            letter_number = self.alphabet_size - (letter_index % self.alphabet_size)
            decrypting_key += self.alphabet[letter_number % self.alphabet_size]
        return decrypting_key

    def get_possible_keys(self):
        '''Returns the english dictionary as decryption keys!'''
        with open("english_words.txt") as file:
            content = file.readlines()
            content = [x.strip() for x in content]

            possible_keys = []
            for word in content:
                possible_keys.append(self.generate_decryption_key(word))

            return possible_keys

    def encode(self, clear_text, key):
        '''Encoding'''
        self.code = ""

        for letter in enumerate(clear_text):
            key_number = self.alphabet.index(key[letter[0] % len(key)])
            self.code += self.alphabet[(self.alphabet.index(letter[1]) +
                                        key_number) % self.alphabet_size]
        return self.code

    def decode(self, code, key):
        '''Decode'''
        self.code = ""
        return self.encode(code, key)


class RSA(Cipher):
    '''RSA class'''

    def generate_keys(self):
        '''Generating two keys'''
        rsa_p = crypto_utils.generate_random_prime(8)
        rsa_q = crypto_utils.generate_random_prime(8)
        while rsa_p == rsa_q:
            rsa_p = crypto_utils.generate_random_prime(8)
            rsa_q = crypto_utils.generate_random_prime(8)

        rsa_n = rsa_p * rsa_q
        phi = (rsa_p - 1) * (rsa_q - 1)
        rsa_e = random.randint(3, phi - 1)
        rsa_d = crypto_utils.modular_inverse(rsa_e, phi)
        while not rsa_d:
            rsa_e = random.randint(3, phi - 1)
            rsa_d = crypto_utils.modular_inverse(rsa_e, phi)
        return rsa_n, rsa_d, rsa_e

    def encode(self, clear_text, key):
        '''Encoding'''
        integer_list = crypto_utils.blocks_from_text(clear_text, 2)
        encrypted_list = [pow(i, key[1], key[0]) for i in integer_list]

        return encrypted_list

    def decode(self, code, key):
        '''Decode'''
        decrypted_list = [pow(number, key[1], key[0]) for number in code]
        message = crypto_utils.text_from_blocks(decrypted_list, 8)
        return message
