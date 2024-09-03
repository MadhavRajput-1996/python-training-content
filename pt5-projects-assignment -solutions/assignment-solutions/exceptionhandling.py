class PasswordException(Exception):
    def __init__(self, msg):
        self.msg = msg

try:
    ps = input("Enter your Password")
    if (len(ps)) < 8:
        raise PasswordException("Enter Password more than eight digit")
except PasswordException as obj:
    print(obj)
else:
    print("Password set")