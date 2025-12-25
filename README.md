# Code Review Agent

## Usage

### Start
```bash
uv venv
uv sync
```

### Agent
```bash
uv run main.py -f file_name.py --show-review
uv run main.py -c your_code
```

- Make sure you have GroqAPI key in .env file. You may also add it using --api-key parameter while calling the main.py script.

- You may either enter the filename or complete code.

- If you want to hide the full review, use flag --show-review.