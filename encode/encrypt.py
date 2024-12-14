from manager import JSONManager
import random

manager = JSONManager()


def process_encrypt(input_text):
    if type(input_text) is str:
        symbols = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-=+'
        conv_str = []

        for j in input_text:
            x = random.choice(symbols)
            if j != " ":
                conv_str.append(x)
            elif j == " ":
                conv_str.append(" ")
        res_str = ''.join(conv_str)

        return res_str









