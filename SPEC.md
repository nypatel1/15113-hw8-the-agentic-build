## What it does

My app greets the user, asks you to log in or register, then lets you take quizzes drawn from a local JSON file. It tracks your scores over time and lets you rate questions so future quizzes feel more personalized. 

The extension feature is a hint system. Each question can optionally have a hint. Before the question is shown, you can type `h` to reveal it, but doing so means a correct answer is only worth half a point instead of a full one.


## Step by step, from the user's perspective

You launch the app. It shows a welcome message and asks if you want to log in or register (or quit). If you're new, you pick a username and a password — the password isn't shown on screen as you type it, and it has to be at least 8 characters. If you're returning, you type your credentials and get in. Three failed login attempts in a row and the app exits.

Once you're in, you see a simple menu: start a quiz, view your stats, see your question feedback history, or log out.

When you start a quiz, the app asks how many questions you want (between 1 and 20) and whether you want to filter by category. It then picks questions using weighted random selection — questions you've liked come up more often, questions you've disliked come up less often (but not excluded entirely, since you might need the practice), and unrated questions are neutral.

Each question shows you the question number, the category, and then optionally offers a hint before revealing the question itself. After you answer, the app tells you if you were right or wrong and shows the correct answer. Then it asks you to rate the question — like, dislike, or skip.

At the end of the quiz you see your score (e.g., `8.5 / 10`), a breakdown by category if you mixed categories, and how you did compared to your personal average.

The stats screen shows your total quizzes taken, average score, best score, most recent score, and a simple ASCII bar chart of your last 10 quizzes.


## The question bank (questions.json)

```json
{
  "questions": [
    {
      "id": "q001",
      "question": "What keyword is used to define a function in Python?",
      "type": "multiple_choice",
      "options": ["func", "define", "def", "function"],
      "answer": "def",
      "category": "Python Basics",
      "hint": "It's a 3-letter abbreviation of the word 'define'."
    },
    {
      "id": "q002",
      "question": "A list in Python is immutable.",
      "type": "true_false",
      "answer": "false",
      "category": "Data Structures",
      "hint": "Think about whether you can call .append() on a list."
    },
    {
      "id": "q003",
      "question": "What built-in function returns the number of items in a list?",
      "type": "short_answer",
      "answer": "len",
      "category": "Python Basics",
      "hint": "It's short for 'length'."
    },
    {
      "id": "q004",
      "question": "Which of the following is used to handle exceptions in Python?",
      "type": "multiple_choice",
      "options": ["catch", "try/except", "error/handle", "rescue"],
      "answer": "try/except",
      "category": "Error Handling",
      "hint": "Python borrows this idea from other languages but uses its own keywords."
    },
    {
      "id": "q005",
      "question": "Python is a statically typed language.",
      "type": "true_false",
      "answer": "false",
      "category": "Python Basics",
      "hint": "In Python, you don't declare variable types explicitly."
    },
    {
      "id": "q006",
      "question": "What does the 'self' parameter refer to in a Python class method?",
      "type": "multiple_choice",
      "options": ["The class itself", "The current instance", "A static reference", "The parent class"],
      "answer": "The current instance",
      "category": "OOP",
      "hint": "It's similar to 'this' in Java or JavaScript."
    },
    {
      "id": "q007",
      "question": "What data structure uses LIFO order?",
      "type": "short_answer",
      "answer": "stack",
      "category": "Data Structures",
      "hint": "Think of a stack of plates — you always take from the top."
    },
    {
      "id": "q008",
      "question": "Which keyword is used to exit a loop prematurely in Python?",
      "type": "multiple_choice",
      "options": ["exit", "stop", "break", "end"],
      "answer": "break",
      "category": "Python Basics",
      "hint": "It literally 'breaks' out of the loop."
    },
    {
      "id": "q009",
      "question": "Dictionaries in Python maintain insertion order (Python 3.7+).",
      "type": "true_false",
      "answer": "true",
      "category": "Data Structures",
      "hint": "This became guaranteed behavior in a relatively recent Python version."
    },
    {
      "id": "q010",
      "question": "What is the time complexity of looking up a key in a Python dictionary?",
      "type": "short_answer",
      "answer": "O(1)",
      "category": "Data Structures",
      "hint": "Dictionaries are implemented as hash tables."
    }
  ]
}
```


## Files

`quiz.py`  runs the menu loop and ties everything together.

`auth.py` handles login and registration. It reads and writes `users.json`

`quiz_engine.py` loads questions, handles the weighted selection logic, checks answers, and manages hint scoring.

`stats.py` reads and writes the SQLite database, computes stats, and renders the ASCII chart.

`feedback.py` reads and writes question ratings and calculates the weights used by the quiz engine.

`questions.json` is the question bank. Human-readable, user-editable.

`users.json` stores usernames and password hashes. Usernames are visible; passwords are not recoverable from the file.

`scores.db` is a SQLite database (binary). It stores quiz results and per-user question feedback. 


## Error handling

If `questions.json` is missing, the app prints a friendly message and exits with code . Same if the file exists but is malformed JSON, or if it parses fine but contains zero questions.

If the user asks for more questions than are available after filtering by category, the app warns them and proceeds with however many it has.

If the user enters an invalid answer during a multiple choice question (like "X" instead of A/B/C/D), it re-prompts without counting it as a wrong answer.


## Acceptance criteria

Disliking a question repeatedly across sessions should make it appear less often in future quizzes. Liking one should make it appear more often.

Requesting a hint and answering correctly should yield 0.5 for that question, reflected in the final score display.

Typing an invalid answer for a multiple choice question should re-prompt without penalizing the user.

Filtering by category should only show questions from that category.

The stats bar chart should only show scores for the currently logged-in user.
