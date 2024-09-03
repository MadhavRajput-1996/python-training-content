print("ATM Application")
print("1. Check Balance","\n2. WithDraw","\n3. Deposit Cash","\n4. Deposit Cheque")
choice = int(input("Enter your choice: "))
balance = 10000
if choice == 1:
    print("Available balance is :", balance)
elif choice == 2:
    b = int(input("Please enter amount"))
    balance = balance - b
    print("Available balance is :", balance)
    print("Withdraw process done successfully")
elif choice == 3:
    b = int(input("Please enter amount"))
    balance = balance + b
    print("Total balance is :", balance)
else:
    b = int(input("Please enter amount"))
    balance = balance + b
    print("Total balance is :", balance)