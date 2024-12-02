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
    # Placeholder for the actual logic to retrieve and display users
    print("\n[View Users]")
    print("User 1: admin")
    print("User 2: user1")
    print("User 3: user2")
    # Add logic to fetch and display users from your data storage

# Function to simulate adding a new user
def add_user():
    print("\n[Add User]")
    username = input("Enter the new username: ")
    # Placeholder for the logic to add a user to your data storage
    print(f"User '{username}' has been added successfully!")

# Function to simulate deleting a user
def delete_user():
    print("\n[Delete User]")
    username = input("Enter the username to delete: ")
    # Placeholder for the logic to delete a user from your data storage
    print(f"User '{username}' has been deleted successfully!")

# Main entry point
if __name__ == "__main__":
    admin_menu()
