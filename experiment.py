import argparse

def get_alpha_index(ch):
    return 26 if ch == ' ' else ord(ch) - ord('a')

def find_shift(p, c):
    po = get_alpha_index(p)
    co = get_alpha_index(c)
    if co >= po:
        return co - po
    return 27 - po + co

def list_shifts(ptext, ctext):
    p_len = len(ptext)
    return list(map(find_shift, ptext, ctext[:p_len]))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--plaintext', type=str, required=True)
    parser.add_argument('--ciphertext', type=str, required=True)
    args = parser.parse_args()
    plaintext = args.plaintext
    ciphertext = args.ciphertext   

