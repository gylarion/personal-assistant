# ---------------------------------------------------------------
# Basic helper types and parser used by the note commands
# These were missing previously; define minimal implementations so
# the module functions work when imported and called.


class Note:
    def __init__(self, text: str, tags=None):
        self.text = text
        self.tags = tags or []

    def __str__(self):
        if self.tags:
            return f"{self.text} [{' ,'.join(self.tags)}]"
        return self.text


def _parse_note_args(tokens: list):
    """Parse tokens into (text, tags).

    Expected formats (tokens list):
      - ["Some", "text"] -> ("Some text", [])
      - ["Note", "tags:", "a", "b"] -> ("Note", ["a","b"])
      - ["Note", "tags:tag1,tag2"] -> ("Note", ["tag1","tag2"]) 
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


# ---------------------------------------------------------------
# CHECKLIST ITEM 1: ADD NOTE
# ---------------------------------------------------------------
def add_note(args: list, book) -> str:
    """
    Додає нову нотатку до існуючого контакту.
    
    Синтаксис команди:
        add-note <Ім'я> <Текст нотатки ...> [tags: <тег1> <тег2> ...]
    """
    if len(args) < 2:
        return ("Помилка: Недостатньо аргументів. "
                "Потрібно: add-note <Ім'я> <Текст нотатки ...> [tags: ...]")

    contact_name = args[0]
    
    # 1. Знаходимо контакт
    if contact_name not in book.data:
        return f"Помилка: Контакт '{contact_name}' не знайдено."
        
    contact_record = book.data[contact_name]
    
    # 2. Розбираємо текст і теги
    text, tags = _parse_note_args(args[1:]) # Все, крім імені
    
    if not text:
        return f"Помилка: Не вказано текст нотатки для '{contact_name}'."
        
    # 3. Створюємо та додаємо нотатку
    new_note = Note(text, tags)
    
    if not hasattr(contact_record, "notes"):
        contact_record.notes = [] 
        
    contact_record.notes.append(new_note)
    
    return f"Нотатку успішно додано до контакту '{contact_name}'."


# ---------------------------------------------------------------
# CHECKLIST ITEM 2: EDIT NOTE
# ---------------------------------------------------------------
def edit_note(args: list, book) -> str:
    """
    Редагує існуючу нотатку за її 1-базованим індексом.
    
    Синтаксис команди:
        edit-note <Ім'я> <Індекс> <Новий текст ...> [tags: <нові теги> ...]
    """
    if len(args) < 3:
        return ("Помилка: Недостатньо аргументів. "
                "Потрібно: edit-note <Ім'я> <Індекс> <Новий текст ...> [tags: ...]")

    contact_name = args[0]
    note_index_str = args[1]
    
    # 1. Знаходимо контакт
    if contact_name not in book.data:
        return f"Помилка: Контакт '{contact_name}' не знайдено."
    
    contact_record = book.data[contact_name]
    
    if not getattr(contact_record, "notes", None):
        return f"Помилка: У контакту '{contact_name}' немає нотаток для редагування."

    # 2. Перевіряємо індекс
    try:
        # Використовуємо 1-базовану індексацію для зручності користувача
        index = int(note_index_str) - 1
        
        # Перевірка коректності індексу
        if not (0 <= index < len(contact_record.notes)):
            raise IndexError
            
    except ValueError:
        return f"Помилка: Індекс '{note_index_str}' має бути числом."
    except IndexError:
        return (f"Помилка: Нотатку з індексом {note_index_str} не знайдено. "
                f"У '{contact_name}' є {len(contact_record.notes)} нотаток.")

    # 3. Розбираємо новий текст і теги
    text, tags = _parse_note_args(args[2:]) # Все, крім імені та індексу

    if not text:
        return "Помилка: Не вказано новий текст нотатки."

    # 4. Створюємо нову нотатку і замінюємо стару
    # Або можна оновити існуючу:
    note_to_edit = contact_record.notes[index]
    note_to_edit.text = text
    note_to_edit.tags = tags

    return f"Нотатку {note_index_str} для '{contact_name}' успішно оновлено."


# ---------------------------------------------------------------
# CHECKLIST ITEM 3: DELETE NOTE
# ---------------------------------------------------------------
def delete_note(args: list, book) -> str:
    """
    Видаляє нотатку за її 1-базованим індексом.
    
    Синтаксис команди:
        delete-note <Ім'я> <Індекс>
    """
    if len(args) != 2:
        return "Помилка: Невірний синтаксис. Потрібно: delete-note <Ім'я> <Індекс>"

    contact_name = args[0]
    note_index_str = args[1]
    
    # 1. Знаходимо контакт
    if contact_name not in book.data:
        return f"Помилка: Контакт '{contact_name}' не знайдено."
        
    contact_record = book.data[contact_name]

    if not getattr(contact_record, "notes", None):
        return f"Помилка: У контакту '{contact_name}' немає нотаток для видалення."

    # 2. Перевіряємо індекс
    try:
        index = int(note_index_str) - 1
        
        if not (0 <= index < len(contact_record.notes)):
            raise IndexError
            
    except ValueError:
        return f"Помилка: Індекс '{note_index_str}' має бути числом."
    except IndexError:
        return (f"Помилка: Нотатку з індексом {note_index_str} не знайдено. "
                f"У '{contact_name}' є {len(contact_record.notes)} нотаток.")

    # 3. Видаляємо нотатку
    # .pop() повертає видалений елемент
    deleted_note = contact_record.notes.pop(index)
    
    return f"Нотатку '{deleted_note.text[:20]}...' видалено з контакту '{contact_name}'."


# ---------------------------------------------------------------
# CHECKLIST ITEM 4: SEARCH NOTES
# ---------------------------------------------------------------
def search_notes(args: list, book) -> str:
    """
    Пошук по всіх нотатках (за текстом або тегом) у всіх контактах.
    
    Синтаксис команди:
        search-notes <пошуковий запит>
    """
    if not args:
        return "Помилка: Введіть текст або тег для пошуку."
        
    query = " ".join(args).lower()
    matches = [] # Список для (contact_name, note_object)

    # Проходимо по всіх контактах
    for contact_name, record in book.data.items():
        # Проходимо по всіх нотатках контакту
        for note in getattr(record, "notes", []):
            match_found = False
            
            # 1. Шукаємо у тексті
            if query in note.text.lower():
                match_found = True
            
            # 2. Шукаємо у тегах
            if any(query in tag.lower() for tag in note.tags):
                match_found = True
            
            if match_found:
                matches.append((contact_name, note))
                # Не використовуємо 'break', щоб знайти всі збіги в одного юзера
    
    if not matches:
        return f"Нотаток за запитом '{query}' не знайдено."
        
    # Форматуємо гарний вивід
    result_lines = [f"Знайдено нотаток за запитом '{query}': {len(matches)}"]
    for name, note in matches:
        # Використовуємо __str__ з класу Note
        result_lines.append(f"\nКонтакт: {name}\nНотатка: {str(note)}")
        
    return "\n".join(result_lines)


# ---------------------------------------------------------------
# CHECKLIST ITEM 5: SORT/GROUP NOTES BY TAG
# ---------------------------------------------------------------
def sort_notes_by_tag(args: list, book) -> str:
    """
    Показує всі нотатки, згруповані за тегами.
    
    Синтаксис команди:
        notes-by-tag
    """
    if args:
        return "Помилка: Ця команда не приймає аргументів. Введіть 'notes-by-tag'"
        
    tags_map = {} # key: tag, value: list of (contact_name, note.text)
    
    for name, record in book.data.items():
        for note in getattr(record, "notes", []):
            
            # Обробляємо нотатки без тегів
            if not note.tags:
                tag = "#Без тегу"
                if tag not in tags_map:
                    tags_map[tag] = []
                tags_map[tag].append((name, note.text))
            
            # Обробляємо нотатки з тегами
            else:
                for tag in note.tags:
                    tag_key = tag.lower() # Групуємо "Work" та "work"
                    if tag_key not in tags_map:
                        tags_map[tag_key] = []
                    tags_map[tag_key].append((name, note.text))

    if not tags_map:
        return "У книзі контактів немає жодної нотатки."
        
    # Форматуємо вивід
    result_lines = ["Нотатки, згруповані за тегами:"]
    # Сортуємо за назвою тегу для порядку
    for tag in sorted(tags_map.keys()):
        result_lines.append(f"\n--- Тег: {tag.upper()} ---")
        for name, text in tags_map[tag]:
            result_lines.append(f"  - [{name}] {text}")
            
    return "\n".join(result_lines)