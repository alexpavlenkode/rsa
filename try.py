import random
import math
from secrets import token_bytes
from coincurve import PublicKey
from collections import Counter
from mnemonic import Mnemonic
from hdwallet import HDWallet
from hdwallet import BIP44HDWallet
from hdwallet.cryptocurrencies import EthereumMainnet as Cryptocurrency
from hdwallet.utils import generate_mnemonic, is_mnemonic
import json
import string

def make_small(num):
    alf = string.ascii_letters# + string.punctuation # Получаем все знаки
    
    nn = str()
    while num>0:
        nn = alf[num%len(alf)] + nn
        num //= len(alf)
    return nn

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def generate_keypair(p, q):
    if not (is_prime(p) and is_prime(q)):
        raise ValueError('Пох2')
    elif p == q:
        raise ValueError('Пох!')

    n = p * q

    phi = (p-1) * (q-1)

    e = random.randrange(1, phi)

    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    d = pow(e, -1, phi)

    return ((e, n), (d, n))

def encrypt(pk, plaintext):
    key, n = pk
    cipher = [(ord(char) ** key) % n for char in plaintext]
    return cipher

def decrypt(pk, ciphertext):
    key, n = pk
    plain = [chr((char ** key) % n) for char in ciphertext]
    return ''.join(plain)


def randprime():
    primes = random.randrange(10,100)
    if is_prime(primes) == True:
        return int(primes)
    else:
        return randprime()
def randprime2():
    primes = random.randrange(10,100)
    if is_prime(primes) == True:
        return int(primes)
    else:
        return randprime2()
    
def get_words():
    STRENGTH: int = 128  
    LANGUAGE: str = "english"
    #MNEMONIC: str = ""
    MNEMONIC: str = generate_mnemonic(language=LANGUAGE, strength=STRENGTH)
    PASSPHRASE: str = ""
    assert is_mnemonic(mnemonic=MNEMONIC, language=LANGUAGE)
    bip44_hdwallet: BIP44HDWallet = BIP44HDWallet(
        cryptocurrency=Cryptocurrency, account=0, change=False, address=0
    )
    bip44_hdwallet.from_mnemonic(
        mnemonic=MNEMONIC, passphrase=PASSPHRASE, language=LANGUAGE
    )
    print("12 слов:", bip44_hdwallet.mnemonic())
    print("Private Key:", bip44_hdwallet.private_key())
    print("Адрес:", bip44_hdwallet.p2pkh_address())
    return bip44_hdwallet.mnemonic()

def get_message():
    make = False
    while make == False:
        messag = get_words()
        if len(messag)>651:
            make == False
            print("False")
        else:
            make == True
            print("True")
            print(len(messag))
            break

    m_list=[]
    new_list=[]
    for words in messag.split():
        m_list.append(words)
    index_crypted = []
    #Получаем номера слов из словаря
    i=0
    while i<len(m_list):
        with open('english.txt') as f:
            for index, line in enumerate(f):
                if m_list[i] in line.split():
                    index_crypted.append(make_small(index))
                    new_list.append(index)

        i = i + 1
    
    print("-------Номера слов----------")
    print(new_list)
    print(str(new_list).replace(',',''))
    print("-------")
    return (str(new_list).replace(',',''))#bip44_hdwallet.private_key()


if __name__ == '__main__':
    
    p = randprime()
    q = randprime2()

    public, private = generate_keypair(p, q)
    
    print("Private key is ", private, " Его запиши или запомни!")

    #1. шифруем его используя два этих слова!
    
    message = get_message()
    encrypted_msg = encrypt(public, message)
    print(public,private)
    print(message)
    #1. шифруем его используя ещё одно число!

    new_list=[]
    for i in range(len(encrypted_msg)):
        #Возможные варианты х  13061988, 1306198813061988, 5878958789, я не помнб...
        x = 5878958789
        new_coin=encrypted_msg[i]*(i+x)# x*(0+34),x*(35),36,37

        new_list.append(new_coin)
    print(new_list)
