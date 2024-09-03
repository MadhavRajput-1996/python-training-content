number = int(input("Enter a number:"))
primeFlag = True
for i in range(2, number):
    if number % i == 0:
        primeFlag = False
        break
if primeFlag == True:
    print(number, " is prime.")
else:
    print(number, " is not prime.")