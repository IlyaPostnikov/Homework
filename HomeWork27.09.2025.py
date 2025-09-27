word = input("Введите слово: ")

length = len(word)

if length % 2 == 0:
    mid_letter_1 = length // 2 - 1
    mid_letter_2 = length // 2
    print(word[mid_letter_1:mid_letter_2+1])
else:
    mid_letter = length // 2
    print(word[mid_letter])

#Задание 2

boys = ['Peter', 'Alex', 'John', 'Arthur', 'Richard']
girls = ['Kate', 'Liza', 'Kira', 'Emma', 'Trisha']

if len(boys) != len(girls):
    print("Внимание, кто-то может остаться без пары.")
else:
    boys_sorted = sorted(boys)
    girls_sorted = sorted(girls)

    print("Идеальные пары:")
    for boy, girl in zip(boys_sorted, girls_sorted):
        print(f"{boy} и {girl}")