from user import Database, UserService


def main():
    db = Database("users.db")
    service = UserService(db)

    while True:
        action = input(
            "Would you like to 'create', 'get', 'update', or 'delete' a user? (type 'exit' to quit): "
        ).strip().lower()

        if action == "exit":
            break

        if action == "create":
            name = input("Enter user name: ").strip()
            age = int(input("Enter user age: ").strip())
            response, status = service.create_user(name, age)
        elif action == "get":
            user_id = int(input("Enter user ID: ").strip())
            response, status = service.get_user(user_id)
        elif action == "update":
            user_id = int(input("Enter user ID: ").strip())
            name = input("Enter new name: ").strip()
            age = int(input("Enter new age: ").strip())
            response, status = service.update_user(user_id, name, age)
        elif action == "delete":
            user_id = int(input("Enter user ID: ").strip())
            response, status = service.delete_user(user_id)
        else:
            print("Invalid action.")
            continue

        print(f"Response: {response}, Status Code: {status}")


if __name__ == "__main__":
    main()
