'''Persons '''
import ciphers
import crypto_utils


class Person():
    '''Person class, parent of all the other persons'''

    def __init__(self, cipher):
        '''constructor init'''
        self.key = None
        self.cipher = cipher
        self.clear_text = ""
        self.code = ""

    def set_key(self, key):
        '''Set the key for this person'''
        self.key = key

    def get_key(self):
        '''gets key to decode the message'''
        return self.key


class Sender(Person):
    '''Sender class'''

    def generate_keys(self):
        '''Generating keys'''
        return self.cipher.generate_keys()

    def set_clear_tekst(self, clear_tekst):
        '''Setting the clear text to be sent'''
        self.clear_text = clear_tekst

    def operate_cipher(self):
        '''Recieves cipher and operates it'''
        self.code = self.cipher.encode(self.clear_text, self.key)
        return self.code


class Reciever(Person):
    '''Class that recieves cipher text and decodes it'''

    def set_code(self, code):
        '''Setting the code'''
        self.code = code

    def generate_keys(self):
        '''Generate keys'''
        return self.cipher.generate_keys()

    def operate_cipher(self):
        '''Recieves cipher and operates it'''
        self.clear_text = self.cipher.decode(self.code, self.key)
        return self.clear_text


class Hacker(Person):
    '''Hacker class'''

    def set_code(self, code):
        """Setting the code"""
        self.code = code
        print(f'The code to hack: {self.code}')

    def hack(self):
        """Main method of the hacker"""
        possible_keys = self.cipher.get_possible_keys()

        for i, key in enumerate(possible_keys):
            result = self.cipher.decode(self.code, key)
            first = result.split(' ')[0].lower()
            print(i, " of line ", len(possible_keys))

            if check_for_word(first, "english_words.txt"):
                print("\nThe Hacker found this line: ")
                print(f'{bold_text(result)}')
                correct = input("Is this your original message? (j/n) ")
                if correct.lower() == "j":
                    print("The hacker got you!!!")
                    exit()

        print("\nThe Hacker could not read your message! :-)")


def check_for_word(word, filename):
    '''checks if a word exists in a file'''
    with open(filename) as file:
        line = file.readline()
        while line:
            if word == line.lower().strip():
                return True
            line = file.readline()
    return False


def bold_text(text):
    '''Creates bold text'''
    return f'\033[1m{text}\033[0m'


def main():
    '''Main function'''

    # CAESAR
    print("Caesar")
    caesar = ciphers.Caesar()

    caesar_sender = Sender(caesar)
    caesar_keys = caesar_sender.generate_keys()
    caesar_sender.set_key(caesar_keys[0])
    caesar_sender.set_clear_tekst("Caesar was a smart man")
    caesar_sender_operated = caesar_sender.operate_cipher()
    print(f"Caesar sender operated: {caesar_sender_operated}")

    caesar_reciever = Reciever(caesar)
    caesar_reciever.set_key(caesar_keys[1])
    caesar_reciever.set_code(caesar_sender_operated)
    caesar_reciever_operated = caesar_reciever.operate_cipher()
    print(f"Caesar reciever operated: {bold_text(caesar_reciever_operated)}")

    # MULTIPLICATION
    print("\nMultiplication")
    multiplication = ciphers.Multiplication()

    mult_sender = Sender(multiplication)
    mult_keys = mult_sender.generate_keys()
    mult_sender.set_key(mult_keys[0])
    mult_sender.set_clear_tekst("Multiplication is better than Caesar")
    mult_sender_operated = mult_sender.operate_cipher()
    print(f"Mult sender operated: {mult_sender_operated}")

    mult_reciever = Reciever(multiplication)
    mult_reciever.set_key(mult_keys[1])
    mult_reciever.set_code(mult_sender_operated)
    mult_reciever_operated = mult_reciever.operate_cipher()
    print(f"Mult reciever operated: {bold_text(mult_reciever_operated)}")

    # AFFINE
    print("\nAffine:")
    affine = ciphers.Affine()
    affine_keys = affine.generate_keys()

    affine_encode_keys = (affine_keys[2], affine_keys[0])
    affine_decode_keys = (affine_keys[3], affine_keys[1])

    affine_sender = Sender(affine)
    affine_sender.set_key(affine_encode_keys)
    affine_sender.set_clear_tekst(
        "The greatest cryptography technique is Affine")
    affine_sender_operated = affine_sender.operate_cipher()
    print(f"Affine sender operated: {affine_sender_operated}")

    affine_reciever = Reciever(affine)
    affine_reciever.set_key(affine_decode_keys)
    affine_reciever.set_code(affine_sender_operated)
    affine_reciever_operated = affine_reciever.operate_cipher()
    print(f"Affine reciever operated: {bold_text(affine_reciever_operated)}")

    # UNBREAKABLE
    print(f"\nUnbreakable")
    unbreakable = ciphers.Unbreakable()
    unbr_keys = unbreakable.generate_keys()

    unbr_sender = Sender(unbreakable)
    unbr_sender.set_key(unbr_keys[0])
    unbr_sender.set_clear_tekst("this is Unbreakable!")
    unbr_sender_operated = unbr_sender.operate_cipher()
    print(f"Unbreakable sender operated: {unbr_sender_operated}")

    unbr_reciever = Reciever(unbreakable)
    unbr_reciever.set_key(unbr_keys[1])
    unbr_reciever.set_code(unbr_sender_operated)
    unbr_reciever_operated = unbr_reciever.operate_cipher()
    print(
        f"Unbreakable reciever operated: {bold_text(unbr_reciever_operated)}")

    # RSA
    print("\nRSA")
    RSA = ciphers.RSA()
    RSA_keys = RSA.generate_keys()
    RSA_secret_keys = (RSA_keys[0], RSA_keys[1])
    RSA_public_keys = (RSA_keys[0], RSA_keys[2])

    RSA_sender = Sender(RSA)
    RSA_sender.set_key(RSA_public_keys)
    RSA_sender.set_clear_tekst("Vi kan kryptere med RSA")
    RSA_sender_operated = RSA_sender.operate_cipher()
    print(f"RSA sender operated: {RSA_sender_operated}")

    RSA_reciever = Reciever(RSA)
    RSA_reciever.set_key(RSA_secret_keys)
    RSA_reciever.set_code(RSA_sender_operated)
    RSA_reciever_operated = RSA_reciever.operate_cipher()
    print(f"RSA reciever operated: {bold_text(RSA_reciever_operated)}")

    # Hacker
    print("\nHacker")
    hacker = Hacker(unbreakable)
    hacker.set_code(unbr_sender_operated)
    hacker.hack()


main()
