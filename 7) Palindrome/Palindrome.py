def palindrome(palin_drome):
    x = palin_drome.split(" ")
    y = []
    for z in x:
        if len(z) != 1:
            if z.lower() == z[::-1].lower():
                y.append(z)
    return y


ask = input("Enter a sentence: ")
print("The palindrome word are:")
for a in palindrome(ask):
    print(a)
