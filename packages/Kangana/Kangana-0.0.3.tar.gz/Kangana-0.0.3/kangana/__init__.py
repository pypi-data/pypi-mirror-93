import os


def encrypt(filename):
    fte = open(filename, "rb").read()
    size = len(fte)
    key = os.urandom(size)
    with open(filename + ".key", "wb") as ko:
        ko.write(key)
    encrypted = bytes(a ^ b for (a, b) in zip(fte, key))
    with open(filename, "wb") as eo:
        eo.write(encrypted)


def decrypt(filename, key):
    file = open(filename, "rb").read()
    key = open(key, "rb").read()
    decrypted = bytes(a ^ b for (a, b) in zip(file, key))
    with open("decrypted." + filename, "wb") as do:
        do.write(decrypted)


def eq(path1, path2):
    d1 = open(path1, "rb").read()
    d2 = open(path2, "rb").read()
    ld1 = len(d1)
    ld2 = len(d2)
    if ld1 > ld2:
        d2 += os.urandom(ld1 - ld2)
    else:
        d1 += os.urandom(ld2 - ld1)
    with open(path1, "wb") as out:
        out.write(d1)
    with open(path2, "wb") as out:
        out.write(d2)


def decryptfileoutoffile(epath, kpath, dpath):
    e = open(epath, "rb").read()
    k = open(kpath, "rb").read()
    d = bytes(a ^ b for (a, b) in zip(e, k))
    with open(dpath, "wb") as do:
        do.write(d)


def hidefileinfile(filetohide, filetosee):
    eq(filetohide, filetosee)
    ori = open(filetohide, "rb").read()
    enc = open(filetosee, "rb").read()
    key = bytes(a ^ b for (a, b) in zip(ori, enc))
    with open("enc.key", "wb") as ko:
        ko.write(key)
    os.remove(filetohide)
