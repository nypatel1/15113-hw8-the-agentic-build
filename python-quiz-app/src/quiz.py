import sys
from auth import login, register
from quiz_engine import QuizEngine
from stats import Stats
from feedback import FeedbackSystem

def main_menu(username=None):
    if not username:
        auth_menu()
    else:
        quiz_menu(username)

def auth_menu():
    while True:
        print("\nWelcome to the Quiz Application!")
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        
        choice = input("Please select an option: ").strip()
        
        if choice == '1':
            login_user()
        elif choice == '2':
            register_user()
        elif choice == '3':
            print("Exiting the application. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice. Please try again.")

def login_user():
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    
    if login(username, password):
        print(f"Welcome back, {username}!")
        quiz_menu(username)
    else:
        print("Invalid username or password.")

def register_user():
    username = input("Enter username: ").strip()
    password = input("Enter password (minimum 8 characters): ").strip()
    
    if len(password) < 8:
        print("Password must be at least 8 characters.")
        return
    
    if register(username, password):
        print(f"Registration successful! Welcome, {username}!")
        quiz_menu(username)
    else:
        print("Username already exists.")

def quiz_menu(username):
    while True:
        print(f"\n=== Main Menu ({username}) ===")
        print("1. Start a quiz")
        print("2. View stats")
        print("3. View question feedback history")
        print("4. Logout")
        
        choice = input("Please select an option: ").strip()
        
        if choice == '1':
            start_quiz(username)
        elif choice == '2':
            view_stats(username)
        elif choice == '3':
            view_feedback_history(username)
        elif choice == '4':
            print(f"Logging out. Goodbye, {username}!")
            auth_menu()
            break
        else:
            print("Invalid choice. Please try again.")

def start_quiz(username):
    quiz_engine = QuizEngine('src/data/questions.json')
    
    # Get number of questions
    while True:
        try:
            num_questions = int(input("How many questions do you want (1-20)? ").strip())
            if 1 <= num_questions <= 20:
                break
            print("Please enter a number between 1 and 20.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Get category filter
    categories = quiz_engine.get_categories()
    print("\nAvailable categories:")
    print("0. All categories")
    for i, cat in enumerate(categories, 1):
        print(f"{i}. {cat}")
    
    while True:
        try:
            cat_choice = int(input("Select category (0 for all): ").strip())
            if cat_choice == 0:
                quiz_engine.filter_by_category('all')
                break
            elif 1 <= cat_choice <= len(categories):
                quiz_engine.filter_by_category(categories[cat_choice - 1])
                break
            print("Invalid selection.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Run quiz
    quiz_engine.reset_session()
    score = 0
    questions_asked = 0
    
    for i in range(min(num_questions, len(quiz_engine.filtered_questions))):
        question = quiz_engine.get_question()
        if not question:
            break
        
        questions_asked += 1
        print(f"\n=== Question {questions_asked} ({question.get('category', 'General')}) ===")
        print(question['question'])
        
        # Offer hint
        if 'hint' in question:
            hint_choice = input("Type 'h' for a hint, or press Enter to continue: ").strip().lower()
            if hint_choice == 'h':
                print(f"Hint: {quiz_engine.get_hint(question)}")
                quiz_engine.mark_hint_used(question)
        
        # Get answer
        user_answer = quiz_engine.prompt_for_answer(question)
        
        # Check answer
        correct = quiz_engine.check_answer(question, user_answer)
        points = quiz_engine.score_question(question, correct)
        score += points
        
        if correct:
            print(f"✓ Correct! ({points} point{'s' if points != 1 else ''})")
        else:
            print(f"✗ Incorrect. The correct answer is: {question['answer']}")
    
    # Show results
    print(f"\n=== Quiz Complete ===")
    print(f"Your score: {score} / {questions_asked}")
    
    # Save score
    stats = Stats()
    stats.create_table()
    stats.add_score(username, score)
    stats.close()

def view_stats(username):
    stats = Stats()
    stats.create_table()
    
    print(f"\n=== Stats for {username} ===")
    avg = stats.compute_average_score(username)
    best = stats.get_best_score(username)
    
    print(f"Total quizzes: {len(stats.get_scores(username))}")
    print(f"Average score: {avg:.1f}")
    print(f"Best score: {best:.1f}")
    
    stats.render_chart(username)
    stats.close()

def view_feedback_history(username):
    print(f"\n=== Question Feedback History ({username}) ===")
    print("Feedback tracking not yet implemented.")

if __name__ == "__main__":
    main_menu()