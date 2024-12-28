try:
    print("Hello")
except NameError:
    print("Проверь имя переменной")

try:
    tags = ["travel", "vacation", "journey"]
    print(tags[4])
except IndexError:
    print("Проверь задаваемый индекс")