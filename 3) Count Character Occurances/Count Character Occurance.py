def count_characters(string):
    count = {}
    count2 = []
    p1 = []
    p2 = []
    for i in string:
        if i != " ":
            count2.append(i.lower())
            if i.lower() in count2:
                while True:
                    try:
                        count[i.lower()] += 1
                    except:
                        count[i.lower()] = 1
                        break
                    else:
                        break
                else:
                    count[i.lower()] = 1
    for x in count.keys():
        p1.append(x)
    for y in count.values():
        p2.append(y)
    a = zip(p1,p2)
    for z,a in a:
        print(z,":",a)


word = input("Enter a word: ")
count_characters(word)
