#!/usr/bin/env python

# based on the hypothesis that the prime generation is flawed and several
# users share prime factors


from Crypto.PublicKey import RSA # pycryptodome
from base64 import b64decode


def gcd(a,b):
    while b:
        a,b = b,a%b
    return a


def modularInverse(e, N):
    x0, x1, y0, y1 = 0, 1, 1, 0
    while e:
        q, N, e = N//e, e, N%e
        y0,y1 = y1, y0-q*y1
        x0,x1 = x1, x0-q*x1
    return x0


def main():
    public_keys = {}
    with open("list_id_rsa.pub", "r") as pk_list:
        for path in pk_list:
            with open(path.strip(), "rb") as pk_file:
                content = pk_file.read()
                user = content.split()[-1].decode()
                key = RSA.importKey(content)
                public_keys[user] = key
    p = None
    q = None
    key_shanae = public_keys["shanaehudson"]
    for user, key in public_keys.items():
        if user == "shanaehudson":
            continue
        gcd_user_shanae = gcd(key.n, key_shanae.n)
        if gcd_user_shanae != 1:
            p = gcd_user_shanae
            q = key_shanae.n // p
            break
    if p is None:
        assert False, "They private key couldn't be extracted this way :("
    # HAHAHAHA! now obtaining d (private key) is piece of cake
    d = modularInverse(key_shanae.e, (p-1)*(q-1))
    key_shanae = RSA.construct((key_shanae.n, key_shanae.e, d, p, q), True)
    with open("id_rsa", "wb") as sk_file:
        sk_file.write(key_shanae.exportKey("PEM"))



if __name__ == "__main__":
    main()

