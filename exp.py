import argparse
import random
import string

alphabet = ' ' + string.ascii_lowercase

parser = argparse.ArgumentParser()
parser.add_argument('--key_length', type=int, default=-1, help='the key length')
parser.add_argument('--seed', type=int, default=114514, help='the random seed')
parser.add_argument('--plaintext', type=str, required=True, help="the plain text")
args = parser.parse_args()
key_length = args.key_length
seed = args.seed
plaintext = args.plaintext


random.seed(seed)
if key_length == -1:
    key_length = random.randint(1, 24)

def j(i:int, t: int = key_length):
    return ((i * (i + 1)) % t + i) % t + 2 

def generate_key(ken_length: int = key_length):
    return [random.randint(0, 26) for _ in range(key_length)]

key = generate_key()

def enc(plaintext: str, key: list = key):
    cipher = ''
    i = 0
    r = 0
    while i < len(plaintext):
        r += 1
        idx = alphabet.find(plaintext[i])
        assert idx != -1
        offset = j(r)
        if 0 <= offset < key_length:
            new_char = alphabet[(idx + offset) % 27]
            cipher += new_char
            i += 1
        else:
            new_char = alphabet[random.randint(0, 26)]
            cipher += new_char
    return cipher

def distribution(s: str):
    count = {}
    for i in s:
        if count.__contains__(i):
            count[i] += 1
        else:
            count[i] = 1
    print('{:<8}{:<8}{:>14}'.format('letter', 'count', 'percentage'))
    for i in count:
        if i == ' ':
            print('{:<8}{:<8}{:>12.2f}%'.format('<space>', count[i], count[i]/len(s) * 100))
        else:
            print('{:<8}{:<8}{:>12.2f}%'.format(i, count[i], count[i]/len(s) * 100))

if __name__ == '__main__':
    cipher = enc(plaintext)
    print(f'plaintext - {plaintext}, distribution is ')
    distribution(plaintext)
    print(f'ciphertext - {cipher}, distribution is ')
    distribution(cipher)
    print(f'L={len(plaintext)}')
    print(f'Cipher length={len(cipher)}')
    print('Key: [' + ','.join(str(k) for k in key) + ']')
