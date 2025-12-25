#!/usr/bin/env python3
import os
import dotenv
import sys
import argparse
from agent import CodeReviewAgent

dotenv.load_dotenv()

def main():
    parser = argparse.ArgumentParser(
        description="Скрипт для ревью Python-кода с помощью LLM."
    )
    parser.add_argument(
        "-f", "--file",
        type=str,
        help="Путь к файлу с Python-кодом для ревью."
    )
    parser.add_argument(
        "-c", "--code",
        type=str,
        help="Напрямую передать код как строку (в кавычках)."
    )
    parser.add_argument(
        "--api-key",
        type=str,
        help="API-ключ для Groq. Если не указан — берётся из переменной окружения GROQ_API_KEY."
    )
    parser.add_argument(
        "--show-review",
        action="store_true",
        help="Показать полный отзыв (включая комментарии), а не только извлечённый код."
    )

    args = parser.parse_args()

    user_code = None
    source = ""

    if args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as f:
                user_code = f.read()
            source = f"файл '{args.file}'"
        except FileNotFoundError:
            print(f"Ошибка: файл '{args.file}' не найден.", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}", file=sys.stderr)
            sys.exit(1)
    elif args.code:
        user_code = args.code
        source = "введённая строка"
    elif not sys.stdin.isatty():
        user_code = sys.stdin.read()
        source = "stdin"
    else:
        print("Укажите код через --file, --code или передайте через stdin.", file=sys.stderr)
        parser.print_help()
        sys.exit(1)

    if not user_code.strip():
        print("Переданный код пуст.", file=sys.stderr)
        sys.exit(1)

    api_key = args.api_key or os.getenv("GROQ_API_KEY")
    if not api_key:
        print("API-ключ не указан. Используйте --api-key или задайте переменную окружения GROQ_API_KEY.", file=sys.stderr)
        sys.exit(1)

    print(f"Ревью кода из {source}...", file=sys.stderr)

    agent = CodeReviewAgent(api_key=api_key)

    try:
        full_review = agent.review_code(user_code)
    except Exception as e:
        print(f"Ошибка при вызове Groq API: {e}", file=sys.stderr)
        sys.exit(1)

    extracted_code = agent.extract_code_pygments(full_review)
    cleaned_code = agent.clean_code(extracted_code)

    if args.show_review:
        print("\nПолный отзыв от агента:\n")
        print("=" * 60)
        print(full_review)
        print("=" * 60)

    print("\nИсправленный код (извлечённый и очищенный):\n")
    if cleaned_code.strip():
        print(cleaned_code)
    else:
        print("\nНе удалось извлечь код. Возможно, агент не вернул блок ```python или кода нет в ответе.")
        print("\nПопробуйте запустить с --show-review, чтобы увидеть полный ответ.")

if __name__ == "__main__":
    main()