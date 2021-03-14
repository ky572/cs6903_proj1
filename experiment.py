import sys
import encryption_test
import decryptor
import time

gen = encryption_test.Cipher_Generator()

def test(insert_random):
    p,c = gen.generate_test1_cipher(insert_random)
    guess = decryptor.guess_plaintext(c)
    if guess != p:
        print ((p,c,guess))
    return True if guess == p else False

def experiment(runs):
    count = 0
    start = time.time()
    for i in range(0, runs):
        result = test(False)
        if result: count += 1
    end = time.time()
    print(f'Test 1, no random characters: {count}/{runs}')
    print(f'Completed in {end-start} seconds')
    count = 0
    start = time.time()
    for i in range(0, runs):
        result = test(True)
        if result: count += 1
        else:
            break
    end = time.time()
    print(f'Cyclical key with random characters: {count}/{runs}')
    print(f'Completed in {end-start} seconds')

if __name__ == '__main__':
    experiment(int(sys.argv[1]))

