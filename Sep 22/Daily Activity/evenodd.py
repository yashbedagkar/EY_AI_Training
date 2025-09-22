def check_num(num1):
    if num1 % 2 == 0:
        return "Even"
    else:
        return "Odd"

num1=int(input("Enter a number: "))
result=check_num(num1)
print(result)



