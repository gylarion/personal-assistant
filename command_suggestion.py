from difflib import get_close_matches
from typing import List

# Canonical command patterns for CLI suggestions
COMMAND_PATTERNS = {
    "add": "add <ім'я> <телефон> [день народження]",
    "birthdays": "birthdays",
    "find": "find <запит>",
    "contacts": "contacts",
    "edit": "edit <ім'я> ...",
    "delete": "delete <ім'я>",
    "add-note": "add-note <ім’я> <текст> [tags: ...]",
    "edit-note": "edit-note <ім’я> <індекс> <новий текст>",
    "delete-note": "delete-note <ім’я> <індекс>",
    "search-notes": "search-notes <запит>",
    "notes-by-tag": "notes-by-tag",
    "help": "help",
}

# Mapping of common synonyms to canonical commands
COMMAND_SYNONYMS = {
    "remove": ["delete", "delete-note"],
    "create": ["add", "add-note"],
    "erase": ["delete"],
    "wipe": ["delete", "delete-note"],
    "new": ["add", "add-note"],
    "tag": ["add-note", "search-notes", "notes-by-tag"],
    "phone": ["add", "find", "edit"],
    "list": ["contacts", "notes-by-tag"],
    "show": ["contacts", "notes-by-tag", "birthdays"],
    "lookup": ["find", "search-notes"],
}

# Context keywords used to promote commands based on arguments
COMMAND_CONTEXT = {
    "notes": {
        "keywords": ["note", "notes", "tag"],
        "commands": ["add-note", "edit-note", "delete-note", "search-notes", "notes-by-tag"],
    },
    "contacts": {
        "keywords": ["name", "contact", "phone", "email", "address", "user"],
        "commands": ["add", "find", "contacts", "edit", "delete"],
    },
    "birthdays": {
        "keywords": ["birthday", "birthdays"],
        "commands": ["birthdays"],
    },
}


def suggest_commands(command: str, args: List[str]) -> List[str]:
    """
    Повертає список можливих команд на основі схожості та контексту аргументів.
    """
    suggestions: List[str] = []
    cmd_lower = command.lower()
    # 1. Прямі синоніми
    suggestions.extend(COMMAND_SYNONYMS.get(cmd_lower, []))

    # 2. Пошук схожих команд
    close_matches = get_close_matches(cmd_lower, COMMAND_PATTERNS.keys(), n=3, cutoff=0.6)
    suggestions.extend(close_matches)

    # 3. Контекст за аргументами (ключовими словами)
    if args:
        arg_text = " ".join(args).lower()
        for context in COMMAND_CONTEXT.values():
            if any(keyword in arg_text for keyword in context["keywords"]):
                suggestions.extend(context["commands"])

    # Прибираємо дублікати, зберігаючи порядок
    seen = set()
    unique_suggestions: List[str] = []
    for suggestion in suggestions:
        if suggestion in COMMAND_PATTERNS and suggestion not in seen:
            seen.add(suggestion)
            unique_suggestions.append(suggestion)

    return unique_suggestions
