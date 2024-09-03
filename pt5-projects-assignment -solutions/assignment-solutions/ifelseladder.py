m=int(input("Enter Maths marks: "))
p=int(input("Enter Physics marks: "))
c=int(input("Enter Chemistry marks: "))

if (m>35 and p>35 and c>35):
    average=((m+p+c)/300)*100
    if average<=59:
        print("You've passed with C grade")
    elif average<=69:
        print("You've passed with B grade")
    elif average>69:
        print("You've passed with A grade")
else:
    print("you've have failed")