def choose_course():
    print("Select a course:")
    print("1. Computer Science")
    print("2. Informatics")
    print("3. Computer Architecture")
    choice = input("Enter your choice (1 or 2 or 3): ")
    if choice == '1':
        return 'Computer Science'
    elif choice == '2':
        return 'Informatics'
    elif choice == '3':
        return 'Computer Architecture'
    else:
        print("Invalid choice. Defaulting to Computer Science.")
        return 'Computer Science'
