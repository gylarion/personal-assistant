"""
Модуль архітектора (Людина 1) + логіка Людини 2 (додавання контактів, дні народження).

Цей файл містить базові класи Contact та AddressBook, а також функції збереження, завантаження,
додавання контактів і виведення найближчих днів народження.
"""
import pickle
import os
from datetime import datetime, timedelta


# --- Людина 1 ---
class Contact:
    """
    Клас, що представляє контакт.

    Атрибути:
        name (str): Ім'я контакту.
        phone (str): Номер телефону.
        notes (list): Список нотаток (об'єкти Note)
    """
    def __init__(self, name: str, phone: str):
        self.name = name
        self.phone = phone
        self.notes = []  # ← вимога завдання
        self.birthday = None

    def add_phone(self, phone: str):
        """
        Встановлює новий номер телефону для контакту після перевірки.
        """
        if not phone.isdigit() or len(phone) != 10:
            raise ValueError("Телефон повинен містити рівно 10 цифр.")
        self.phone = phone

    def add_birthday(self, birthday_str: str):
        """
        Встановлює дату народження для контакту після перевірки формату.
        """
        try:
            self.birthday = datetime.strptime(birthday_str, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Невірний формат дати. Використовуйте ДД.ММ.РРРР")

    def __str__(self):
        return f"Contact(name={self.name}, phone={self.phone}, notes={len(self.notes)})"


class AddressBook:
    """
    Клас для зберігання об'єктів Contact.

    Атрибути:
        contacts (dict): словник у форматі name → Contact
    """
    def __init__(self):
        self.contacts = {}

    def add_contact(self, contact: Contact):
        """
        Додає або оновлює контакт у словнику за ім’ям.
        """
        self.contacts[contact.name] = contact

    def get_contact(self, name: str):
        """
        Повертає контакт за ім’ям або None, якщо такого немає.
        """
        return self.contacts.get(name)

    def delete_contact(self, name: str):
        """
        Видаляє контакт з книги за ім’ям.
        """
        if name in self.contacts:
            del self.contacts[name]

    def find(self, name: str):
        """
        Псевдонім для get_contact() — для сумісності з функціями інших учасників.
        """
        return self.get_contact(name)

    def get_upcoming_birthdays(self):
        """
        Повертає список словників з іменами контактів і датами привітань, якщо день народження у найближчі 7 днів.
        Переносить ДН з вихідних на понеділок.
        """
        today = datetime.today().date()
        next_week = today + timedelta(days=7)
        result = []

        for contact in self.contacts.values():
            if contact.birthday:
                bday = contact.birthday.replace(year=today.year)
                if bday < today:
                    bday = bday.replace(year=today.year + 1)

                congratulation_date = bday
                if bday.weekday() == 5:  # Saturday
                    congratulation_date = bday + timedelta(days=2)
                elif bday.weekday() == 6:  # Sunday
                    congratulation_date = bday + timedelta(days=1)

                if today <= congratulation_date <= next_week:
                    result.append({
                        "name": contact.name,
                        "congratulation_date": congratulation_date.strftime("%Y.%m.%d")
                    })

        return result

    def __str__(self):
        return "\n".join(str(contact) for contact in self.contacts.values())


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


# --- Людина 2 ---
def input_error(func):
    """
    Декоратор для обробки помилок користувацького вводу при виклику функцій.
    """
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return f"Помилка: {str(e)}"
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
                "💡 Формат: додати [ім'я] [телефон]\n"
                "💡 Наприклад: додати Іван 0671234567")

    name, phone, *_ = contact_args
    record = book.find(name)
    message = "Контакт оновлено."

    if record is None:
        try:
            record = Contact(name, phone)
            message = "Контакт додано."
        except ValueError as e:
            return f"❌ Помилка створення контакту: {str(e)}"
    else:
        try:
            record.add_phone(phone)
        except ValueError as e:
            return f"❌ {str(e)}\n💡 Телефон повинен містити 10 цифр (наприклад: 0671234567)"

    book.add_contact(record)
    save_data(book)
    return message


@input_error
def get_upcoming_birthdays(*args):
    """
    Виводить список користувачів, яких потрібно привітати з днем народження
    у найближчі 7 днів. Переносить ДН з вихідних на понеділок.
    """
    if not args:
        return "❌ Помилка: AddressBook не передано."

    *_, book = args
    upcoming = book.get_upcoming_birthdays()

    if not upcoming:
        return "Немає днів народження на наступному тижні."

    result = ["Найближчі дні народження:"]
    for birthday_info in upcoming:
        name = birthday_info.get('name', 'Невідомо')
        date = birthday_info.get('congratulation_date', 'Невідомо')
        result.append(f"{name}: {date}")

    return '\n'.join(result)
