from Crypto.Random import random
import re
strength_order = [
        r'^(?=.{32,})((?=.*[a-z])(?=.*[A-Z])(?=.*[\W_])(?=.*[0-9])).*$', #all character tyes over 32 letters
        r'^(?=.{24,})((?=.*[a-z])(?=.*[A-Z])(?=.*[\W_])(?=.*[0-9])).*$',
        r'^(?=.{16,})((?=.*[a-z])(?=.*[A-Z])(?=.*[\W_])(?=.*[0-9])).*$',
        r'^(?=.{16,})((?=.*[a-z])(?=.*[0-9])(?=.*[A-Z])|(?=.*[\W_])(?=.*[0-9])(?=.*[a-z])|(?=.*[\W_])(?=.*[0-9])(?=.*[A-Z])|(?=.*[\W_])|(?=.*[A-Z])(?=.*[a-z])).*$', 
        r'^(?=.{12,})((?=.*[a-z])(?=.*[0-9])(?=.*[A-Z])|(?=.*[\W_])(?=.*[0-9])(?=.*[a-z])|(?=.*[\W_])(?=.*[0-9])(?=.*[A-Z])|(?=.*[\W_])|(?=.*[A-Z])(?=.*[a-z])).*$', 
        r'^(?=.{12,})((?=.*[a-z])(?=.*[0-9])|(?=.*[a-z])(?=.*[\W_])|(?=.*[0-9])(?=.*[\W_])|(?=.*[A-Z])(?=.*[0-9])|)(?=.*[A-Z])(?=.*[\W_]).*$', 
        r'^(?=.{8,})((?=.*[a-z])(?=.*[0-9])|(?=.*[a-z])(?=.*[\W_])|(?=.*[0-9])(?=.*[\W_])|(?=.*[A-Z])(?=.*[0-9])|)(?=.*[A-Z])(?=.*[\W_]).*$', 
        r'(?=.{8,}).*$'
        ]

def generate_password(passlen=16, exclude = '%'):
    p = ''
    for i in range(passlen):
        while True:
            l = chr(random.randint(33, 123))
            if l not in exclude:
                p += l
                break
            else:
                continue
    return p

def get_pass_strength(password):
    levels = len(strength_order)-1
    for idx, r in enumerate(strength_order):
        p = re.compile(r)
        m = p.match(password)
        if m is not None:
            return levels-idx
            break
    return -1

if __name__ == '__main__':
    password = generate_password()
    print(password)
