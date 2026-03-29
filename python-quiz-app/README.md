# Python Quiz Application

This project is a Python-based quiz application that allows users to take quizzes, manage their accounts, and view statistics based on their performance. 

## Project Structure

```
python-quiz-app
├── src
│   ├── quiz.py            # Main menu loop and user interaction
│   ├── auth.py            # User authentication (login/registration)
│   ├── quiz_engine.py      # Question loading and scoring management
│   ├── stats.py           # Database interactions and statistics
│   ├── feedback.py        # Question ratings management
│   ├── data
│   │   ├── questions.json  # Question bank (editable)
│   │   ├── users.json      # User credentials storage
│   │   └── scores.db       # SQLite database for quiz results
├── requirements.txt       # Project dependencies
└── README.md              # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd python-quiz-app
   ```

2. **Install dependencies:**
   Create a virtual environment and install the required packages listed in `requirements.txt`:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. **Run the application:**
   Execute the main script to start the quiz application:
   ```
   python src/quiz.py
   ```

## Usage Guidelines

- Users can register for an account or log in with existing credentials.
- The quiz engine will present questions based on the available question bank.
- Users can provide feedback on questions, which will influence future quiz presentations.
- Statistics and results can be viewed after completing quizzes.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.