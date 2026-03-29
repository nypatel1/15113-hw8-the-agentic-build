def main_menu():
    while True:
        print("Welcome to the Quiz Application!")
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        
        choice = input("Please select an option: ")
        
        if choice == '1':
            # Call login function from auth.py
            pass
        elif choice == '2':
            # Call registration function from auth.py
            pass
        elif choice == '3':
            print("Exiting the application. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()