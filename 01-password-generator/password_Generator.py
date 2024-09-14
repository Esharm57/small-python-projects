import random

chars = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890,.?/-=_+\`'

number_Char = int(input('enter number of char in the password: '))
number_Passwords = int(input('enter number of passwords you want: '))

print('here are your passwords:')



for i in range(number_Passwords):
    password = ''
    for j in range(number_Char):
        num = random.randint(0,71)
        password += chars[num]
    print(password)
