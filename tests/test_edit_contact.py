import unittest
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
from unittest.mock import patch

import app_func


def _make_contact(name: str, phone: str = "0123456789") -> app_func.Contact:
    contact = app_func.Contact(name)
    contact.add_phone(phone)
    contact.set_email("old@example.com")
    contact.set_address("Old address")
    return contact


class TestEditContact(unittest.TestCase):
    def test_edit_contact_updates_multiple_fields(self):
        book = app_func.AddressBook()
        contact = _make_contact("Іван")
        book.add_contact(contact)

        with patch("app_func.save_data") as mock_save:
            result = app_func.edit_contact(
                "Іван",
                "Петро",
                "0987654321",
                "new@example.com",
                "New address",
                book,
            )

        self.assertEqual(result, "✅ Контакт 'Іван' оновлено.")
        self.assertIsNone(book.get_contact("Іван"))
        updated_contact = book.get_contact("Петро")
        self.assertIs(updated_contact, contact)
        self.assertEqual(updated_contact.phone, "0987654321")
        self.assertEqual(updated_contact.email, "new@example.com")
        self.assertEqual(updated_contact.address, "New address")
        mock_save.assert_called_once_with(book)

    def test_edit_contact_missing_contact_returns_user_error(self):
        book = app_func.AddressBook()

        result = app_func.edit_contact("Марія", book)

        self.assertEqual(result, "Помилка: Контакт не знайдено.")

    def test_edit_contact_rejects_invalid_phone_and_keeps_original(self):
        book = app_func.AddressBook()
        contact = _make_contact("Степан", phone="1234567890")
        book.add_contact(contact)

        result = app_func.edit_contact("Степан", "-", "invalid", book)

        self.assertEqual(result, "Помилка: Телефон повинен містити рівно 10 цифр.")
        self.assertEqual(book.get_contact("Степан").phone, "1234567890")


if __name__ == "__main__":
    unittest.main()
