# admin.py

# Function to display the admin menu
def admin_menu():
    while True:
        print("\nAdmin Menu:")
        print("1. View All Users")
        print("2. Add a User")
        print("3. Delete a User")
        print("4. Exit")
        choice = input("Enter your choice (1-4): ")

        # Handle the user's choice
        if choice == "1":
            view_users()
        elif choice == "2":
            add_user()
        elif choice == "3":
            delete_user()
        elif choice == "4":
            print("Exiting admin panel. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

# Function to simulate viewing all users
def view_users():
    print("\n[View Users]")
    # Placeholder for actual user list retrieval
    users = ["admin", "user1", "user2"]  # Example hardcoded users
    if users:
        print("Current Users:")
        for user in users:
            print(f"- {user}")
    else:
        print("No users found.")

# Function to simulate adding a new user
def add_user():
    print("\n[Add User]")
    username = input("Enter the new username: ")
    # Simulate adding user (extend functionality here)
    if username:
        print(f"User '{username}' has been added successfully!")
    else:
        print("Username cannot be empty.")

# Function to simulate deleting a user
def delete_user():
    print("\n[Delete User]")
    username = input("Enter the username to delete: ")
    # Simulate deleting user (extend functionality here)
    if username:
        print(f"User '{username}' has been deleted successfully!")
    else:
        print("Username cannot be empty.")

# Entry point of the program
if __name__ == "__main__":
    admin_menu()
