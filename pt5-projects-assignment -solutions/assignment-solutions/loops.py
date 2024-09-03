n =int(input("Enter an input"))
for i in range(n):
	if i<=100:
		if i%10 == 0:
			continue
		else:
			print(i)