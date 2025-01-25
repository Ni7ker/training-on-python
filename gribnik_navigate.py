# Функция для проведения грибника по лесной тропе
def navigate_forest():
    # Начальное положение грибника
    while is_path_below():  # Цикл продолжается, пока под грибником тропа
        # Если впереди дуб или береза
        if is_tree_in_front('дуб') or is_tree_in_front('береза'):
            collect_mushroom()  # Собрать гриб
            turn_left()  # Повернуть налево
        # Если впереди ель
        elif is_tree_in_front('ель'):
            turn_right()  # Повернуть направо
        # Если впереди тропа
        elif is_path_in_front():
            move_forward()  # Идем вперед

# Функции для анализа окружающей ситуации и действий грибника
def is_path_below():
    # Здесь должно быть условие проверки наличия тропы внизу
    return check_position('тропа')  # Возвращает True, если внизу тропа

def is_tree_in_front(tree_type):
    return check_position(tree_type)  # Возвращает True, если впереди дерево типа tree_type

def is_path_in_front():
    # Проверка, что впереди тропа
    return check_position('тропа')  # Возвращает True, если впереди тропа

def collect_mushroom():
    print("Собрал гриб")  # Симуляция сбора гриба

def turn_left():
    print("Повернул налево")  # Симуляция поворота налево

def turn_right():
    print("Повернул направо")  # Симуляция поворота направо

def move_forward():
    print("Иду вперед")  # Симуляция движения вперед

def check_position(position_type):
    return True  # Возвращает True для всех типов, можно адаптировать под реальные данные