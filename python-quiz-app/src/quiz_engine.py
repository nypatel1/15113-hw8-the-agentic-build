import json
import random
import sys

class QuizEngine:
    def __init__(self, questions_file, feedback_system=None):
        self.questions_file = questions_file
        self.feedback_system = feedback_system
        self.questions = self.load_questions()
        self.session_hints = {}  # Track which questions had hints used
        self.current_category = None
        self.filtered_questions = []

    def load_questions(self):
        try:
            with open(self.questions_file, 'r') as file:
                data = json.load(file)
                questions = data.get('questions', [])
                if not questions:
                    print("Error: No questions found in the question bank.")
                    sys.exit(1)
                return questions
        except FileNotFoundError:
            print("Error: Questions file is missing.")
            sys.exit(1)
        except json.JSONDecodeError:
            print("Error: Questions file is malformed.")
            sys.exit(1)

    def get_categories(self):
        """Extract unique categories from questions."""
        categories = set()
        for question in self.questions:
            if 'category' in question:
                categories.add(question['category'])
        return sorted(list(categories))

    def filter_by_category(self, category):
        """Filter questions by category. 'all' means no filtering."""
        if category.lower() == 'all':
            self.filtered_questions = self.questions
            self.current_category = None
        else:
            self.filtered_questions = [q for q in self.questions if q.get('category', '') == category]
            self.current_category = category
        
        if not self.filtered_questions:
            print(f"Warning: No questions found for category '{category}'.")
            self.filtered_questions = self.questions

    def get_question(self):
        """Get a question using weighted random selection based on feedback."""
        if not self.filtered_questions:
            print("No questions available.")
            return None
        
        # Calculate weights based on feedback
        weights = []
        for question in self.filtered_questions:
            weight = self._calculate_weight(question)
            weights.append(weight)
        
        # Weighted random selection
        return random.choices(self.filtered_questions, weights=weights, k=1)[0]

    def _calculate_weight(self, question):
        """Calculate weight for a question based on feedback rating."""
        if not self.feedback_system:
            return 1.0
        
        rating = self.feedback_system.get_rating(question.get('id'))
        if rating == 'like':
            return 1.5
        elif rating == 'dislike':
            return 0.7
        else:  # neutral or no rating
            return 1.0

    def get_valid_answer_options(self, question):
        """Get valid answer options for a multiple choice question."""
        if question.get('type') == 'multiple_choice':
            return ['A', 'B', 'C', 'D']
        return None

    def prompt_for_answer(self, question):
        """Prompt user for answer with validation for multiple choice."""
        valid_options = self.get_valid_answer_options(question)
        
        while True:
            user_answer = input("Your answer: ").strip().upper()
            
            if valid_options and user_answer not in valid_options:
                print(f"Invalid input. Please enter one of: {', '.join(valid_options)}")
                continue
            
            return user_answer

    def check_answer(self, question, user_answer):
        return question['answer'].lower() == user_answer.lower()

    def get_hint(self, question):
        return question.get('hint', "No hint available.")

    def mark_hint_used(self, question):
        """Mark that a hint was used for this question."""
        question_id = question.get('id')
        if question_id:
            self.session_hints[question_id] = True

    def was_hint_used(self, question):
        """Check if a hint was used for this question."""
        question_id = question.get('id')
        return self.session_hints.get(question_id, False)

    def score_question(self, question, correct):
        """Score a question: 1.0 if correct without hint, 0.5 if correct with hint."""
        if not correct:
            return 0
        
        if self.was_hint_used(question):
            return 0.5
        return 1.0

    def reset_session(self):
        """Reset session hints for a new quiz."""
        self.session_hints = {}