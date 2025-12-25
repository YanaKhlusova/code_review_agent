from pygments import lexers
from pygments.token import Token
from groq import Groq


class CodeReviewAgent:
    """
    Агент для выполнения ревью кода с использованием LLM.
    """
    def __init__(self, api_key=None):
        """
        Инициализирует агента ревью кода.
        
        Args:
            api_key (str): API ключ для Groq. Если не указан, будет получен из userdata.
        """
        self.api_key = api_key
        self.client = Groq(api_key=self.api_key)
        self.system_prompt = """
                            Сделай ревью кода на Python.
                            Найди стилистические ошибки. Предложи исправления, ориентируйся на PEP8.
                            Найди потенциальные баги и предложи исправления.
                            Предложи улучшения по оптимизации.
                            Покажи разницу между исходной и исправленной версией кода. Отдели их заголовками.
                            Код для ревью:\n\n
                            """

    def review_code(self, user_prompt, model="llama-3.1-8b-instant", temperature=0.1, max_tokens=1000):
        """
        Выполняет ревью кода с помощью LLM.
        
        Args:
            user_prompt (str): Код для ревью.
            model (str): Модель LLM для использования.
            temperature (float): Температура для генерации.
            max_tokens (int): Максимальное количество токенов для генерации.
            
        Returns:
            str: Ответ LLM с ревью кода.
        """
        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content

    def extract_code_pygments(self, text):
        """
        Извлекает код из текста используя Pygments.
        Только Pygments, без regex и другой логики.
        
        Args:
            text (str): Текст для извлечения кода.
            
        Returns:
            str: Извлеченный код.
        """
        try:
            lexer = lexers.get_lexer_by_name("python")
            tokens = list(lexers.lex(text, lexer))

            code_parts = []
            for token_type, token_text in tokens:
                if token_type not in (Token.Comment, Token.String, Token.Text):
                    code_parts.append(token_text)

            extracted = ''.join(code_parts).strip()
            return extracted if extracted else text

        except:
            return text

    def clean_code(self, text):
        """
        Базовая очистка кода.
        
        Args:
            text (str): Текст для очистки.
            
        Returns:
            str: Очищенный код.
        """
        lines = []
        in_code_block = False

        for line in text.split('\n'):
            stripped = line.strip()

            if stripped.startswith('```python'):
                in_code_block = True
                continue
            elif stripped == '```' and in_code_block:
                in_code_block = False
                continue
            elif stripped.startswith('```'):
                continue

            lines.append(line)

        return '\n'.join(lines).strip()

    def process_review(self, user_prompt):
        """
        Полный процесс ревью кода: выполнение ревью, извлечение и очистка кода.
        
        Args:
            user_prompt (str): Код для ревью.
            
        Returns:
            str: Обработанный и очищенный код.
        """
        review = self.review_code(user_prompt)
        extracted = self.extract_code_pygments(review)
        clean = self.clean_code(extracted)
        return clean