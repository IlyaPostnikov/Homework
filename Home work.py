year = int(input("Введите год "))
if year % 4 == 0 and year % 100 != 0 or year % 400 == 0: print(year, "Высокосный год")
else: print(year, "Невысокосный год")

# Дополнительное задание
tiket = int(input("Введидите свой биллет"))
firs_3_digit =( tiket // 1000)
last_3_digit =( tiket % 1000)
summ_firs = firs_3_digit // 100 + firs_3_digit // 10 % 10+ firs_3_digit % 10
summ_last = last_3_digit // 100 + last_3_digit // 10 % 10 + last_3_digit % 10
if summ_firs == summ_last:
     print("Счастливый биллет")
else: print("Несчастливый биллет")



