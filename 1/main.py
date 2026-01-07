class Person:
    def __init__(self, name="", age=0, salary=0.0, is_married=False):
        self.name = name
        self.age = age
        self.salary = salary
        self.is_married = is_married

    def __str__(self):
        return f"Имя: {self.name}, Возраст: {self.age}, Зарплата: {self.salary}, Женат/Замужем: {'Да' if self.is_married else 'Нет'}"

    def to_dict(self):
        return {
            'name': self.name,
            'age': self.age,
            'salary': self.salary,
            'is_married': self.is_married
        }


def create_people_array():
    return [
        Person("Иван Петров", 32, 45000.50, True),
        Person("Анна Сидорова", 28, 52000.75, False),
        Person("Сергей Иванов", 45, 78000.00, True),
        Person("Мария Кузнецова", 35, 61000.25, True),
        Person("Алексей Смирнов", 29, 49000.00, False),
        Person("Ольга Попова", 41, 67000.50, True),
        Person("Дмитрий Васильев", 26, 42000.00, False),
        Person("Екатерина Новикова", 33, 55000.00, True),
        Person("Павел Федоров", 38, 72000.75, False),
        Person("Наталья Морозова", 31, 58000.00, False),
        Person("Андрей Волков", 47, 85000.00, True),
        Person("Татьяна Алексеева", 24, 39000.50, False),
        Person("Михаил Лебедев", 36, 64000.00, True),
        Person("Юлия Егорова", 30, 53000.00, False),
        Person("Артем Козлов", 43, 71000.25, True)
    ]


def print_people(title, people):
    print(title)
    for person in people:
        print(person)

def sort_and_print(people, key_func, key_name):
    sorted_people = sorted(people, key=key_func)
    print_people(f"\nСортировка по {key_name}\n", sorted_people)
    return sorted_people


def save_to_txt(filename, people):
    with open(filename, 'w', encoding='utf-8') as file:
        for person in people:
            file.write(f"{person.name} {person.age} {person.salary} {int(person.is_married)}\n")
    print(f"\nДанные сохранены в файл: {filename}\n")

def main():
    people = create_people_array()
    print_people("\nИсходный массив объектов\n", people)
    sort_and_print(people, lambda p: p.name, "имени")
    sort_and_print(people, lambda p: p.age, "возрасту")
    sort_and_print(people, lambda p: p.salary, "зарплате")
    sort_and_print(people, lambda p: p.is_married, "семейному положению")
    print("\nЭкспорт данных в файл\n")
    save_to_txt("people.txt", people)
    print("\nСодержимое файла people.txt:\n")
    try:
        with open("people.txt", 'r', encoding='utf-8') as file:
            content = file.read()
            print(f"\n{content}\n")
    except FileNotFoundError:
        print("\nФайл не найден!\n")

if __name__ == "__main__":
    main()
