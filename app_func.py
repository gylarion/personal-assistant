from collections import UserDict
from datetime import datetime, timedelta
import pickle
import os
import re

"""
Модуль архітектора (Людина 1) + логіка Людини 2 (додавання контактів, дні народження) + Людина 3 (пошук і виведення).

Цей файл містить базові класи Contact та AddressBook, а також функції збереження, завантаження,
додавання контактів і виведення найближчих днів народження.
"""

# --- Людина 1: Архітектор (Core / OOP / Storage) ---
class Contact:
    """
    Клас, що представляє контакт.
    Атрибути:
        name (str): Ім'я контакту.
        phone (str): Номер телефону.
        notes (list): Список нотаток (об'єкти Note).
        email (str): Email адреса.
        address (str): Поштова адреса.
        birthday (datetime.date): Дата народження.
    """

    def __init__(self, name: str):
        self.name = name
        self.phone = None
        self.notes = []
        self.email = None
        self.address = None
        self.birthday = None

    def add_phone(self, phone: str):
        """
        Встановлює новий номер телефону для контакту після перевірки.
        Args:
            phone (str): Номер телефону (10 цифр)
        Raises:
            ValueError: Якщо телефон не складається з 10 цифр.
        """
        if not phone.isdigit() or len(phone) != 10:
            raise ValueError("Телефон повинен містити рівно 10 цифр.")
        self.phone = phone

    def add_birthday(self, birthday_str: str):
        """
        Встановлює дату народження після перевірки формату ДД.ММ.РРРР
        Args:
            birthday_str (str): Дата у форматі "ДД.ММ.РРРР"
        Raises:
            ValueError: Якщо формат дати невірний.
        """
        try:
            self.birthday = datetime.strptime(birthday_str, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Невірний формат дати. Використовуйте ДД.ММ.РРРР")

    def set_email(self, email: str):
        """
        Встановлює email після базової перевірки формату.
        Args:
            email (str): Email адреса.
        Raises:
            ValueError: Якщо формат email некоректний.
        """
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w{2,}$", email):
            raise ValueError("Невірний формат email.")
        self.email = email

    def set_address(self, address: str):
        self.address = address

    def __str__(self):
        return f"Contact(name={self.name}, phone={self.phone}, notes={len(self.notes)})"


class AddressBook(UserDict):
    """
    Клас для зберігання об'єктів Contact.

    Атрибути:
        contacts (dict): словник у форматі name → Contact
    """
    def __init__(self):
        super().__init__()

    def add_contact(self, contact: Contact):
        """
        Додає або оновлює контакт у словнику за ім’ям.
        """
        self.data[contact.name] = contact

    def get_contact(self, name: str):
        """
        Повертає контакт за ім’ям або None, якщо такого немає.
        """
        return self.data.get(name)

    def delete_contact(self, name: str):
        """
        Видаляє контакт з книги за ім’ям.
        """
        if name in self.data:
            del self.data[name]

    def find(self, name: str):
        """
        Псевдонім для get_contact() — для сумісності з функціями інших учасників.
        """
        return self.get_contact(name)

    def get_upcoming_birthdays(self, days: int = 7):
        """
        Повертає список словників з іменами контактів і датами привітань,
        якщо день народження у найближчі `days` днів.
        Переносить ДН з вихідних на понеділок.
        """
        today = datetime.today().date()
        end_date = today + timedelta(days=days)
        result = []

        for contact in self.data.values():
            if contact.birthday:
                bday = contact.birthday.replace(year=today.year)
                if bday < today:
                    bday = bday.replace(year=today.year + 1)

                congratulation_date = bday
                if bday.weekday() == 5:  # Saturday
                    congratulation_date = bday + timedelta(days=2)
                elif bday.weekday() == 6:  # Sunday
                    congratulation_date = bday + timedelta(days=1)

                if today <= congratulation_date <= end_date:
                    result.append({
                        "name": contact.name,
                        "congratulation_date": congratulation_date.strftime("%Y.%m.%d")
                    })

        return result

    def __str__(self):
        return "\n".join(str(contact) for contact in self.data.values())


def save_data(address_book: AddressBook, filename: str = "data/addressbook.pkl"):
    """
    Зберігає об'єкт AddressBook у файл через pickle.
    """
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "wb") as file:
        pickle.dump(address_book, file)


def load_data(filename: str = "data/addressbook.pkl") -> AddressBook:
    """
    Завантажує AddressBook з файлу, якщо існує, або створює новий.
    """
    if os.path.exists(filename):
        with open(filename, "rb") as file:
            return pickle.load(file)
    return AddressBook()


# --- Людина 2: Логіка Контактів (Create + Birthday) ---
def input_error(func):
    """
    Декоратор для обробки помилок користувацького вводу при виклику функцій.
    """
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return f"Помилка: недопустимий формат або ви вказали не всі значення"
        except KeyError:
            return "Помилка: Контакт не знайдено."
        except IndexError:
            return "Помилка: Неправильний формат команди."
        except Exception as e:
            return f"Помилка: {str(e)}"
    return inner


@input_error
def add_contact(*args):
    """
    Додає новий контакт або оновлює телефон існуючого. Після додавання зберігає AddressBook у файл.
    """
    *contact_args, book = args

    if len(contact_args) < 2:
        return ("❌ Помилка: Потрібно вказати ім'я та телефон.\n"
                "💡 Формат: додати [ім'я] [телефон] [день народження]\n"
                "💡 Наприклад: додати Іван 0671234567")

    name, phone, birthday_str, *_ = contact_args
    record = book.find(name)
    message = "Контакт оновлено."

    if record is None:
        try:
            record = Contact(name)
            record.add_phone(phone)
            record.add_birthday(birthday_str)
            message = "Контакт додано."
        except ValueError as e:
            return f"❌ Помилка створення контакту: {str(e)}"
    else:
        try:
            record.add_phone(phone)
        except ValueError as e:
            return f"❌ {str(e)}"

    book.add_contact(record)
    save_data(book)
    return message


@input_error
def get_upcoming_birthdays(*args):
    """
    Виводить список користувачів, яких потрібно привітати з днем народження
    у найближчі N днів (за замовчуванням 7).
    
    Виклик:
        get_upcoming_birthdays(book)              -> 7 днів
        get_upcoming_birthdays(N, book)           -> N днів
        
    Команда:
        birthdays
        birthdays 30
    """
    if not args:
        return "❌ Помилка: AddressBook не передано."

    *cmd_args, book = args
    days = 7             # значення за замовчуванням
    if cmd_args:
        try:
            days = int(cmd_args[0])
            if days <= 0:
                return "Кількість днів має бути додатним числом."
        except ValueError:
            return "Кількість днів має бути числом, наприклад: birthdays 30"

    upcoming = book.get_upcoming_birthdays(days=days)

    if not upcoming:
        return f"Немає днів народження на наступні {days} днів."

    result = [f"Найближчі дні народження на {days} днів:"]
    for birthday_info in upcoming:
        name = birthday_info.get('name', 'Невідомо')
        date = birthday_info.get('congratulation_date', 'Невідомо')
        result.append(f"{name}: {date}")

    return '\n'.join(result)

# --- Людина 3: Логіка Контактів (Read: Search / Show All) ---
def format_contact(record) -> str:
    """
    Формує текстове представлення одного контакту:
    ім’я, телефони, день народження, нотатки (якщо є).
    """
    lines = []
    name_str = getattr(record.name, "value", str(record.name))
    lines.append(f"Name: {name_str}")
    phone = getattr(record, "phone", None)
    if phone:
        lines.append(f"Phone: {phone}")
    else:
        lines.append("Phone: -")
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
    """
    Пошук контактів за різними критеріями:
    - ім'я
    - номер телефону
    - email
    - адреса
    - текст нотаток
    - теги нотаток
    
    Повертає відформатований список або повідомлення, якщо нічого не знайдено.
    """
    if not args:
        return "Введіть, будь ласка, текст для пошуку (ім'я, телефон, email, адресу або тег)."
    query = " ".join(args).strip().lower()
    if not query:
        return "Порожній запит. Введіть ім'я або частину номера."
    matches = []
    for record in book.data.values():
        name_val = str(getattr(record, "name", "") or "").lower()
        phone_val = str(getattr(record, "phone", "") or "").lower()
        email_val = str(getattr(record, "email", "") or "").lower()
        addr_val = str(getattr(record, "address", "") or "").lower()
        
        field_match = any(       # чи є збіг по полях контакту
            query in field
            for field in (name_val, phone_val, email_val, addr_val)
        )

        note_match = False       # перевірка нотаток: текст + теги
        for note in getattr(record, "notes", []):
            text_match = query in note.text.lower()
            tag_match = any(query in tag.lower() for tag in note.tags)
            if text_match or tag_match:
                note_match = True
                break

        if field_match or note_match:
            matches.append(record)
    if not matches:
        return f"Нічого не знайдено за запитом: '{query}'."
    chunks = [format_contact(rec) for rec in matches]
    header = f"Знайдено контактів: {len(matches)}"
    return header + "\n\n" + "\n\n".join(chunks)


def show_all_contacts(book) -> str:
    """
    Виводить усі збережені контакти у форматованому вигляді або повідомлення, якщо книга порожня.
    """
    if not book.data:
        return "Книга контактів порожня."
    lines = [format_contact(record) for record in book.data.values()]
    return "\n\n".join(lines)
# --- Людина 4: Логіка Контактів (Update / Delete) ---

@input_error
def edit_contact(*args):
    """
    Редагує існуючий контакт у книзі контактів AddressBook.
    Формат виклику:
        edit_contact(старе_ім'я, нове_ім'я, новий_телефон, новий_email, нова_адреса, book)
    Обов’язковим є лише перший аргумент — старе ім’я (за яким буде знайдено контакт).
    Всі наступні аргументи — опціональні. Щоб пропустити значення, передайте `None`, "-", або нічого.

    Наприклад:
        edit_contact("Іван", "Іванов", None, "ivan@example.com", None, book) — змінює ім’я та email
        edit_contact("Іван", None, "0987654321", None, None, book) — змінює лише телефон
    ⚠️ Нотатки не редагуються цією функцією (це обробляє Людина 5).
    Після змін AddressBook зберігається у файл.
    Args:
        *args: список позиційних аргументів, де останній — book (AddressBook)
    Returns:
        str: Повідомлення про успіх або помилку
    """
    *contact_args, book = args

    if len(contact_args) < 1:
        return ("❌ Помилка: Вкажіть хоча б ім’я для редагування.\n"
                "💡 Формат: edit [старе_ім’я] [нове_ім’я] [телефон] [email] [адреса]")

    old_name = contact_args[0]
    new_name = contact_args[1] if len(contact_args) > 1 and contact_args[1] not in [None, "-", "null"] else None
    new_phone = contact_args[2] if len(contact_args) > 2 and contact_args[2] not in [None, "-", "null"] else None
    new_email = contact_args[3] if len(contact_args) > 3 and contact_args[3] not in [None, "-", "null"] else None
    new_address = contact_args[4] if len(contact_args) > 4 and contact_args[4] not in [None, "-", "null"] else None

    contact = book.find(old_name)
    if not contact:
        raise KeyError("Контакт не знайдено.")

    # Оновлення імені
    if new_name:
        contact.name = new_name
        if old_name != new_name:
            book.delete_contact(old_name)
            book.add_contact(contact)

    # Оновлення телефону
    if new_phone:
        contact.add_phone(new_phone)

    # Оновлення email
    if new_email:
        if hasattr(contact, "set_email"):
            contact.set_email(new_email)
        else:
            raise AttributeError("Цей контакт не підтримує email.")

    # Оновлення адреси
    if new_address:
        if hasattr(contact, "set_address"):
            contact.set_address(new_address)
        else:
            raise AttributeError("Цей контакт не підтримує адресу.")

    save_data(book)
    return f"✅ Контакт '{old_name}' оновлено."


@input_error
def delete_contact(*args):
    """
    Видаляє контакт з AddressBook за ім’ям.
    Формат виклику:
        delete_contact("Іван", book)
    Args:
        *args: перший аргумент — ім’я, останній — AddressBook
    Returns:
        str: Повідомлення про успішне видалення або помилку, якщо контакт не знайдено
    Порада:
        Якщо ім’я не вказано, або контакт не існує — буде повідомлення про помилку.
    """
    *name_args, book = args

    if not name_args:
        raise ValueError("Ім’я контакту не вказано.")

    name = name_args[0]
    if not book.find(name):
        raise KeyError("Контакт не знайдено.")

    book.delete_contact(name)
    save_data(book)
    return f"✅ Контакт '{name}' видалено."

# ============================
# Людина 5: Логіка Нотаток (Full CRUD + Tags)
# ============================

class Note:
    def __init__(self, text: str, tags=None):
        self.text = text
        self.tags = tags or []

    def __str__(self):
        if self.tags:
            return f"{self.text} [{' ,'.join(self.tags)}]"
        return self.text

def _parse_note_args(tokens: list):
    """
    Допоміжна функція для розбору аргументів нотатки.
    """
    if not tokens:
        return "", []

    marker_index = None
    for i, t in enumerate(tokens):
        if isinstance(t, str) and t.lower().startswith('tags:'):
            marker_index = i
            break

    if marker_index is None:
        return " ".join(tokens).strip(), []

    text = " ".join(tokens[:marker_index]).strip()
    rest = tokens[marker_index:]

    tags = []
    if rest:
        first = rest[0]
        if first.lower().startswith('tags:') and first != 'tags:':
            tags_part = first.split(':', 1)[1]
            if tags_part:
                tags.extend([t.strip() for t in tags_part.split(',') if t.strip()])
            tags.extend(rest[1:])
        else:
            tags.extend(rest[1:])

    tags = [t for t in tags if t]
    return text, tags

def add_note(args: list, book) -> str:
    """
    Додає нову нотатку до існуючого контакту.
    Синтаксис: add-note <Ім'я> <Текст нотатки ...> [tags: ...]
    """
    if len(args) < 2:
        return "Помилка: Потрібно вказати ім'я та текст нотатки."

    contact_name = args[0]
    if contact_name not in book.data:
        return f"Помилка: Контакт '{contact_name}' не знайдено."

    text, tags = _parse_note_args(args[1:])
    if not text:
        return f"Помилка: Не вказано текст нотатки для '{contact_name}'."

    new_note = Note(text, tags)
    contact_record = book.data[contact_name]

    if not hasattr(contact_record, "notes"):
        contact_record.notes = []
    contact_record.notes.append(new_note)

    return f"Нотатку успішно додано до контакту '{contact_name}'."

def edit_note(args: list, book) -> str:
    """
    Редагує існуючу нотатку за індексом (1-базованим).
    Синтаксис: edit-note <Ім'я> <Індекс> <Новий текст ...> [tags: ...]
    """
    if len(args) < 3:
        return "Помилка: Недостатньо аргументів."

    contact_name, note_index_str = args[0], args[1]

    if contact_name not in book.data:
        return f"Помилка: Контакт '{contact_name}' не знайдено."

    contact_record = book.data[contact_name]
    if not getattr(contact_record, "notes", None):
        return f"Помилка: У контакту '{contact_name}' немає нотаток."

    try:
        index = int(note_index_str) - 1
        if not (0 <= index < len(contact_record.notes)):
            raise IndexError
    except ValueError:
        return f"Помилка: Індекс '{note_index_str}' має бути числом."
    except IndexError:
        return f"Помилка: Нотатку з індексом {note_index_str} не знайдено."

    text, tags = _parse_note_args(args[2:])
    if not text:
        return "Помилка: Не вказано новий текст нотатки."

    note = contact_record.notes[index]
    note.text = text
    note.tags = tags

    return f"Нотатку {note_index_str} для '{contact_name}' оновлено."

def delete_note(args: list, book) -> str:
    """
    Видаляє нотатку за індексом.
    Синтаксис: delete-note <Ім'я> <Індекс>
    """
    if len(args) != 2:
        return "Помилка: Синтаксис: delete-note <Ім'я> <Індекс>"

    contact_name, note_index_str = args[0], args[1]

    if contact_name not in book.data:
        return f"Помилка: Контакт '{contact_name}' не знайдено."

    contact_record = book.data[contact_name]
    if not getattr(contact_record, "notes", None):
        return f"Помилка: У контакту '{contact_name}' немає нотаток."

    try:
        index = int(note_index_str) - 1
        if not (0 <= index < len(contact_record.notes)):
            raise IndexError
    except ValueError:
        return f"Помилка: Індекс '{note_index_str}' має бути числом."
    except IndexError:
        return f"Помилка: Нотатку з індексом {note_index_str} не знайдено."

    deleted_note = contact_record.notes.pop(index)
    return f"Нотатку '{deleted_note.text[:20]}...' видалено з контакту '{contact_name}'."

def search_notes(args: list, book) -> str:
    """
    Пошук нотаток за текстом або тегом по всіх контактах.
    Синтаксис: search-notes <запит>
    """
    if not args:
        return "Помилка: Введіть текст або тег для пошуку."

    query = " ".join(args).lower()
    matches = []

    for contact_name, record in book.data.items():
        for note in getattr(record, "notes", []):
            if query in note.text.lower() or any(query in tag.lower() for tag in note.tags):
                matches.append((contact_name, note))

    if not matches:
        return f"Нотаток за запитом '{query}' не знайдено."

    result = [f"Знайдено нотаток за запитом '{query}': {len(matches)}"]
    for name, note in matches:
        result.append(f"\nКонтакт: {name}\nНотатка: {str(note)}")

    return "\n".join(result)

def sort_notes_by_tag(args: list, book) -> str:
    """
    Виводить всі нотатки, згруповані за тегами.
    Синтаксис: notes-by-tag
    """
    if args:
        return "Помилка: Команда не приймає аргументів."

    tags_map = {}
    for name, record in book.data.items():
        for note in getattr(record, "notes", []):
            if not note.tags:
                tags_map.setdefault("#Без тегу", []).append((name, note.text))
            else:
                for tag in note.tags:
                    tags_map.setdefault(tag.lower(), []).append((name, note.text))

    if not tags_map:
        return "У книзі контактів немає жодної нотатки."

    result = ["Нотатки, згруповані за тегами:"]
    for tag in sorted(tags_map):
        result.append(f"\n--- Тег: {tag.upper()} ---")
        for name, text in tags_map[tag]:
            result.append(f"  - [{name}] {text}")

    return "\n".join(result)
