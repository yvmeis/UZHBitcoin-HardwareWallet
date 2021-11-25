from typing import ByteString
import bcrypt

#returns the hashed password
def hashPW(pw):
    pw = pw.encode()
    hashed = bcrypt.hashpw(pw, bcrypt.gensalt())
    print("---hashed---")
    return hashed

#returns True if the hashed password matches the plain text password
def checkPW(pw, hashed):
    pw = pw.encode()
    if bcrypt.checkpw(pw, hashed):
        print("strings are equivalent")
        return True
    else:
        print("strings are NOT equivalent")
        return False



pw = input("password: ")
checkPW(pw, hashPW(pw))