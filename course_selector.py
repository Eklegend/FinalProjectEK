def choose_course():
    print("Select a course:")
    print("1. Computer Science")
    print("2. Informatics")
    print("3. Computer Architecture")
    print("4. Data Science")
    choice = input("Enter your choice (numerals): ")
    if choice == '1':
        return 'Computer Science'
    elif choice == '2':
        return 'Informatics'
    elif choice == '3':
        return 'Computer Architecture'
    elif choice == '4':
        return 'Data Science'
    else:
        print("Invalid choice. Defaulting to Computer Science.")
        return 'Computer Science'
