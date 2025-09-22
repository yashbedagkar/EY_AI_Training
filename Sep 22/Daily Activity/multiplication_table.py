for i in range(1, 6):
    print(i)

def multiplication_table(n):
    print(f"Multiplication table of {n} is:")
    for i in range(1, 11):
        print(f"{n} x {i} = {n * i}")

n=int(input("Enter the number: "))
multiplication_table(n)