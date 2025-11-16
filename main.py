import sys
from colorama import init, Fore, Style
import app_func
from command_suggestion import COMMAND_PATTERNS, suggest_commands

# Ініціалізуємо colorama
init(autoreset=True)


def print_menu():
    print(Fore.CYAN + "\n" + "=" * 110)
    print(Fore.YELLOW + "  🧠 ОСОБИСТИЙ ПОМІЧНИК — КОМАНДА : 17")
    print(Fore.CYAN + "=" * 110)

    print(Fore.GREEN + "\n  [📇 Контакти]")
    print("   add <ім'я> <телефон>".ljust(40) + "➜ Додати новий контакт або оновити телефон")
    print("   <день народження>".ljust(40)+ "➜ Формат: ДД.ММ.ГГГГ - 12.12.2020")
    print("   find <запит>".ljust(40) + "➜ Знайти контакти за іменем або номером")
    print("   contacts".ljust(40) + "➜ Вивести всі збережені контакти")
    print("   edit <старе_ім’я> <нове_ім’я/- >".ljust(40) +
          "➜ Редагувати дані контакту")
    print("   <телефон/- > <email/- > <адреса/- >".ljust(40) + "(пропускайте через '-')")
    print("   delete <ім’я>".ljust(40) + "➜ Видалити контакт за ім’ям")

    print(Fore.GREEN + "\n  [🎂 Дні народження]")
    print("   birthdays".ljust(40) + "➜ Показати, кого привітати впродовж 7 днів")

    print(Fore.GREEN + "\n  [📝 Нотатки]")
    print("   add-note <ім’я> <текст> [tags: ...]".ljust(40) + "➜ Додати нотатку до контакту з тегами")
    print("   edit-note <ім’я> <індекс> ".ljust(40) + "➜ Редагувати нотатку за індексом")
    print("   <новий текст> [tags: ...]".ljust(40))
    print("   delete-note <ім’я> <індекс>".ljust(40) + "➜ Видалити нотатку за індексом")
    print("   search-notes <запит>".ljust(40) + "➜ Знайти нотатку за фрагментом тексту або тегом")
    print("   notes-by-tag".ljust(40) + "➜ Показати всі нотатки, згруповані за тегами")

    print(Fore.GREEN + "\n  [⚙️ Службові команди]")
    print("   help".ljust(40) + "➜ Показати це меню команд")
    print("   exit / close / quit".ljust(40) + "➜ Зберегти дані та вийти з програми")

    print(Fore.CYAN + "=" * 110 + "\n")



def main():
    # Завантажуємо книгу
    book = app_func.load_data()

    print_menu()

    while True:
        try:
            user_input = input(Fore.BLUE + ">>> " + Style.RESET_ALL).strip()
            if not user_input:
                continue

            parts = user_input.split()
            command = parts[0].lower()
            args = parts[1:]

            if command in ["exit", "close", "quit"]:
                app_func.save_data(book)
                print(Fore.YELLOW + "✅ Збережено. До зустрічі!")
                sys.exit(0)

            elif command == "help":
                print_menu()

            elif command == "add":
                print(app_func.add_contact(*args, book))

            elif command == "birthdays":
                print(app_func.get_upcoming_birthdays(book))

            elif command == "find":
                print(app_func.Contactss(args, book))

            elif command == "contacts":
                print(app_func.show_all_contacts(book))

            elif command == "edit":
                print(app_func.edit_contact(*args, book))

            elif command == "delete":
                print(app_func.delete_contact(*args, book))

            elif command == "add-note":
                print(app_func.add_note(args, book))

            elif command == "edit-note":
                print(app_func.edit_note(args, book))

            elif command == "delete-note":
                print(app_func.delete_note(args, book))

            elif command == "search-notes":
                print(app_func.search_notes(args, book))

            elif command == "notes-by-tag":
                print(app_func.sort_notes_by_tag(args, book))

            else:
                suggestions = suggest_commands(command, args)
                print(Fore.RED + f"❌ Невідома команда: {command}.")
                if suggestions:
                    readable = ", ".join(COMMAND_PATTERNS[s] for s in suggestions[:3])
                    print(Fore.YELLOW + f"💡 Можливо, ви мали на увазі: {readable}")
                print(Fore.YELLOW + "ℹ️ Введіть 'help' для повного списку команд.")

        except Exception as e:
            print(Fore.RED + f"⚠️ Виникла помилка: {str(e)}")


if __name__ == "__main__":
    main()
