# Група 17. Людина 3 - Олександр Скрябіков: "Логіка Контактів (Read: Search / Show All)"
# Задача: Реалізувати обробники команд для пошуку та відображення контактів.
# Checklist:
# DONE - 1. Написати функцію Contactss(*args) (пошук за іменем, телефоном).
# DONE - 2. Написати функцію show_all_contacts() (має гарно виводити включно з нотатками, якщо вони є).
# DONE - 3. Обробляти помилки (наприклад, "Нічого не знайдено") та гарно форматувати вивід.
# DONE - 4. Написати коментарі/docstrings для своїх функцій.

# ---------------------------------------------------------------
#
#  Будь ласка, додайте ці команди в основний цикл команд (main.py):
#
#      find <текст>   → запускає Contactss(args, book)
#     
#      contacts  → запускає show_all_contacts(book)
#       
#  Приклади інтеграції в main():
#
#      elif command == "find":
#          print(Contactss(args, book))
#
#      elif command == "contacts":
#          print(show_all_contacts(book))
#
#  Функції, які потрібно викликати:
#
#      Contactss(args, book)
#          - шукає по імені, частині імені, номеру, частині номера
#          - повертає красиво відформатовані результати або "нічого не знайдено"
#
#      show_all_contacts(book)
#          - повертає гарний список усіх контактів з телефонами,
#            днем народження, нотатками (якщо є)
#
# ---------------------------------------------------------------

# ---------------------------------------------------------------
#
# СЛОВНИК:
#
# 1. args - Список аргументів, які користувач ввів після команди.
# contactss John 123 → args = ["John", "123"].
#
# 2. append() - Додає новий елемент у кінець списку.
# lines.append("Текст")
#
# 3. book - Об’єкт класу AddressBook, де зберігаються всі контакти.
#
# 4. book.data - Словник всередині AddressBook.
# Ключ → ім’я контакту.
# Значення → об’єкт Record.
#
# 5. format_contact(record) - Створює відформатований текст для одного контакту
#
# 6. getattr(obj, attr, default) - Отримує значення атрибута об’єкта.
# getattr(record, "phones", [])
# *Якщо в record немає поля phones, поверне порожній список.
#
# 7. if not args - Перевіряє, чи список аргументів порожній. 
# Означає, що користувач нічого не ввів для пошуку.
#
# 8. if not matches - Перевіряє, чи не знайдено жодного контакту за запитом.
#
# 9. join() - Об’єднує список рядків в один рядок.
# ", ".join(["123", "555"]) → "123, 555"
#
# 10. matches - Список контактів (Record), які збіглися з пошуковим запитом.
#
# 11. name_str - Рядкове значення імені контакту (record.name.value).
#
# 12. phones — список об’єктів Phone у контакті.
#
# 13. phone_value — рядок з номером телефона всередині Phone.
#
# 14. query - Пошуковий запит, введений користувачем. Переводиться в нижній регістр.
#
# 15. value - Основне значення поля Field.
# У класів: 
# - Name → ім’я 
# - Phone → номер телефону / 
# - Birthday → дата
#
# 16. values() - Метод словника. Повертає всі значення без ключів.
# book.data.values() → список Record.
#
# 17. AddressBook - Клас, що містить всі записи (Record) та методи:
# - додавання
# - пошуку
# - видалення
# - виводу майбутніх днів народження
#
# 18. Record - Об’єкт класу Record — один конкретний контакт.
# Містить:
# - ім’я
# - список телефонів
# - день народження
# - нотатки (якщо будуть додані)
#
# 19. Contactss() - Функція пошуку контактів:
# - за ім’ям
# - за частиною імені
# - за номером телефону
# - за частиною номера
#
# ---------------------------------------------------------------



# КРАСИВИЙ ФОРМАТ КОНТАКТА

def format_contact(record) -> str:
    """
    Формує текстовий опис одного контакту.

    Повертає:
        - ім'я
        - телефони
        - день народження (якщо є)
        - нотатки та теги (якщо вони будуть реалізовані командою)

    Приклад формату:
        Name: John Doe
        Phones: 1234567890, 5555555555
        Birthday: 12.05.1998
        Notes:
          - Купити подарунок (tags: shopping, birthday)
          - Подзвонити у понеділок
    """
    lines = []   # список рядків, які потім об’єднаємо у блок

    # Ім’я контакту
    name_str = getattr(record.name, "value", str(record.name))   # отримуємо ім’я або його рядкове представлення
    lines.append(f"Name: {name_str}")

    # Телефони
    phones = getattr(record, "phones", [])   # беремо список телефонів або порожній список
    if phones:
        phone_values = [getattr(p, "value", str(p)) for p in phones]  # дістаємо значення кожного телефону
        lines.append(f"Phones: {', '.join(phone_values)}")            # додаємо телефони в один рядок
    else:
        lines.append("Phones: -")   # якщо номерів немає

    # День народження
    birthday = getattr(record, "birthday", None)   # отримуємо дату народження
    if birthday:
        lines.append(f"Birthday: {birthday}")      # додаємо, якщо існує

    # Нотатки
    notes = getattr(record, "notes", None)         # список нотаток (може бути відсутній)
    if notes:
        lines.append("Notes:")
        for note in notes:
            text = getattr(note, "text", str(note))  # текст нотатки
            tags = getattr(note, "tags", [])         # список тегів
            if tags:
                tag_str = ", ".join(str(t) for t in tags)  # формуємо рядок тегів
                lines.append(f"  - {text}  (tags: {tag_str})")
            else:
                lines.append(f"  - {text}")  # нотатка без тегів

    return "\n".join(lines)   # повертаємо контакт у вигляді блоку тексту


# 1. Функція Contactss(*args) (пошук за іменем, телефоном)

def Contactss(args, book) -> str:
    """
    Пошук контактів за ім'ям або частиною номера телефону.

    Args:
        args: список рядків, які користувач ввів після команди.
        book: екземпляр AddressBook.

    Returns:
        Відформатований рядок з усіма знайденими контактами
        або повідомлення про те, що нічого не знайдено.

    Приклад результату:

    >>> find john
    Знайдено контактів: 1

    Name: John Doe
    Phones: 1234567890, 5555555555
    Birthday: 12.05.1998

    >>> find 555
    Знайдено контактів: 2
    ...

    >>> find xyz
    Нічого не знайдено за запитом: 'xyz'.
    """

    if not args:     # якщо користувач нічого не ввів після команди
        return "Введіть, будь ласка, текст для пошуку (ім'я або частину номера)."

    query = " ".join(args).strip().lower()       # об’єднання всіх аргументів у єдиний пошуковий рядок
    if not query:                                # перевірка, чи рядок не порожній після очищення
        return "Порожній запит. Введіть ім'я або частину номера."

    matches = []   # Список, куди ми будемо складати всі контакти, що відповідають пошуковому запиту

    # Проходимо циклом по всіх записах у книзі контактів
    for record in book.data.values():      # book.data.values — це всі об’єкти Record у AddressBook

        # Перевіряємо ім’я контакта
        name_str = getattr(record.name, "value", str(record.name))   # Отримуємо ім’я як рядок (record.name.value)
        if query in name_str.lower():      # Якщо пошуковий запит входить у ім’я (нечутливе до регістру)
            matches.append(record)         # Додаємо контакт до результатів пошуку
            continue                       # Пропускаємо перевірку номерів, бо ім’я вже співпало

        # Перевіряємо номери телефонів контакта
        phones = getattr(record, "phones", [])   # Отримуємо список телефонів або пустий список, якщо їх немає
        for p in phones:                         # Перебираємо кожен телефон у контакті
            phone_value = getattr(p, "value", str(p))   # Беремо номер телефону як рядок
            if query in phone_value:             # Якщо запит міститься у номері телефону
                matches.append(record)           # Додаємо цей контакт у результати
                break                            # Припиняємо перевіряти інші телефони цього контакту (вже знайдено)

    if not matches:
        return f"Нічого не знайдено за запитом: '{query}'."

# GOOD LOOKING FORMAT for all matches:
    chunks = [format_contact(rec) for rec in matches]   # Створюємо список відформатованих текстів контактів, які знайшлися
    header = f"Знайдено контактів: {len(matches)}"      # Формуємо заголовок з кількістю знайдених контактів
    return header + "\n\n" + "\n\n".join(chunks)        # Повертаємо заголовок + кожен контакт, розділяючи їх порожнім рядком

    

# 2. Функція show_all_contacts() з нотатками

def show_all_contacts(book) -> str:
    """
    Повертає відформатований рядок з усіма контактами в AddressBook.

    Args (Arguments):
        book: екземпляр AddressBook.

    Returns:
        Рядок з усіма контактами, де кожен контакт відформатований функцією
        format_contact(), або повідомлення, якщо книга контактів порожня.

    Приклад результату:
    Name: John Doe
    Phones: 1234567890
    Birthday: 04.03.1995

    Name: Anna Petrova
    Phones: 5555555555, 9876543210
    Birthday: 21.10.1992
    Notes:
      - Зустріч у п'ятницю (tags: work)
      - Купити квіти

    Якщо контактів немає:
    "Книга контактів порожня."
    """

    if not book.data:                      # Якщо книга контактів порожня
        return "Книга контактів порожня."

    lines = []                             # Список, у який збираються всі контакти
    for record in book.data.values():      # book.data.values — усі записи з AddressBook
        lines.append(format_contact(record))

    return "\n\n".join(lines)              # Розділяємо контакти порожнім рядком






# ---------------------------------------------------------------
# CLEAN CODE
def format_contact(record) -> str:
    lines = []
    name_str = getattr(record.name, "value", str(record.name))
    lines.append(f"Name: {name_str}")

    phones = getattr(record, "phones", [])
    if phones:
        phone_values = [getattr(p, "value", str(p)) for p in phones]
        lines.append(f"Phones: {', '.join(phone_values)}")
    else:
        lines.append("Phones: -")

    birthday = getattr(record, "birthday", None)
    if birthday:
        lines.append(f"Birthday: {birthday}")

    notes = getattr(record, "notes", None)
    if notes:
        lines.append("Notes:")
        for note in notes:
            text = getattr(note, "text", str(note))
            tags = getattr(note, "tags", [])
            if tags:
                tag_str = ", ".join(str(t) for t in tags)
                lines.append(f"  - {text}  (tags: {tag_str})")
            else:
                lines.append(f"  - {text}")

    return "\n".join(lines)


def Contactss(args, book) -> str:
    if not args:
        return "Введіть, будь ласка, текст для пошуку (ім'я або частину номера)."
    query = " ".join(args).strip().lower()
    if not query:
        return "Порожній запит. Введіть ім'я або частину номера."

    matches = []

    for record in book.data.values():
        name_str = getattr(record.name, "value", str(record.name))
        if query in name_str.lower():
            matches.append(record)
            continue

        phones = getattr(record, "phones", [])
        for p in phones:
            phone_value = getattr(p, "value", str(p))
            if query in phone_value:
                matches.append(record)
                break

    if not matches:
        return f"Нічого не знайдено за запитом: '{query}'."

    chunks = [format_contact(rec) for rec in matches]
    header = f"Знайдено контактів: {len(matches)}"
    return header + "\n\n" + "\n\n".join(chunks)


def show_all_contacts(book) -> str:
    if not book.data:
        return "Книга контактів порожня."

    lines = []
    for record in book.data.values():
        lines.append(format_contact(record))

    return "\n\n".join(lines)
