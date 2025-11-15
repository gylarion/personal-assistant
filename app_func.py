"""
Модуль архітектора (Людина 1).
Містить базові класи Contact та AddressBook, а також функції збереження та завантаження даних.
"""
import pickle
import os


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

    def __str__(self):
        """
        Повертає рядкове представлення контакту.
        """
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
        Додає контакт до адресної книги.
        Args:
            contact (Contact): контакт, який потрібно додати.
        """
        self.contacts[contact.name] = contact

    def get_contact(self, name: str):
        """
        Повертає контакт за ім'ям.
        Args:
            name (str): Ім’я контакту.
        Returns:
            Contact | None: Знайдений контакт або None.
        """
        return self.contacts.get(name)

    def delete_contact(self, name: str):
        """
        Видаляє контакт з адресної книги.
        Args:
            name (str): Ім’я контакту.
        """
        if name in self.contacts:
            del self.contacts[name]

    def __str__(self):
        """
        Повертає рядкове представлення усієї адресної книги.
        """
        return "\n".join(str(contact) for contact in self.contacts.values())


def save_data(address_book: AddressBook, filename: str = "data/addressbook.pkl"):
    """
    Зберігає AddressBook у файл за допомогою pickle.
    Args:
        address_book (AddressBook): адресна книга.
        filename (str): шлях до файлу.
    """
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, "wb") as file:
        pickle.dump(address_book, file)


def load_data(filename: str = "data/addressbook.pkl") -> AddressBook:
    """
    Завантажує AddressBook із файлу.
    Args:
        filename (str): шлях до файлу.
    Returns:
        AddressBook: завантажена або нова адресна книга.
    """
    if os.path.exists(filename):
        with open(filename, "rb") as file:
            return pickle.load(file)

    return AddressBook()
