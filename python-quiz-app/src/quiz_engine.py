import json
import random

class QuizEngine:
    def __init__(self, questions_file):
        self.questions_file = questions_file
        self.questions = self.load_questions()

    def load_questions(self):
        try:
            with open(self.questions_file, 'r') as file:
                questions = json.load(file)
                if not questions:
                    raise ValueError("No questions found in the question bank.")
                return questions
        except FileNotFoundError:
            print("Error: Questions file is missing.")
            exit(1)
        except json.JSONDecodeError:
            print("Error: Questions file is malformed.")
            exit(1)

    def get_question(self):
        if not self.questions:
            print("No questions available.")
            return None
        return random.choice(self.questions)

    def check_answer(self, question, user_answer):
        return question['answer'].lower() == user_answer.lower()

    def get_hint(self, question):
        return question.get('hint', "No hint available.")

    def score_question(self, user_answer, question):
        if self.check_answer(question, user_answer):
            return 1  # Correct answer
        return 0  # Incorrect answer

# Example usage:
# quiz_engine = QuizEngine('src/data/questions.json')
# question = quiz_engine.get_question()
# print(question)