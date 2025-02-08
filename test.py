import unittest
from user import Database, UserService
import os


class TestUserService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db_name = "test_users.db"
        cls.db = Database(cls.db_name)
        cls.service = UserService(cls.db)

    @classmethod
    def tearDownClass(cls):
        cls.db.conn.close()
        os.remove(cls.db_name)

    def setUp(self):
        self.db.cursor.execute("DELETE FROM users")
        self.db.conn.commit()

    def test_create_user(self):
        response, status = self.service.create_user("Alice", 25)
        self.assertEqual(status, 201)
        self.assertIn("user_id", response)
        self.assertEqual(response["name"], "Alice")
        self.assertEqual(response["age"], 25)

    def test_create_user_invalid(self):
        response, status = self.service.create_user("", 25)
        self.assertEqual(status, 400)

        response, status = self.service.create_user("Alice", -1)
        self.assertEqual(status, 400)

    def test_get_user(self):
        user_id = self.db.insert_user("Bob", 30)
        response, status = self.service.get_user(user_id)
        self.assertEqual(status, 200)
        self.assertEqual(response["name"], "Bob")

    def test_get_user_not_found(self):
        response, status = self.service.get_user(999)
        self.assertEqual(status, 404)

    def test_update_user(self):
        user_id = self.db.insert_user("Charlie", 35)
        response, status = self.service.update_user(user_id, "Charlie Updated", 36)
        self.assertEqual(status, 200)
        self.assertIn("message", response)

    def test_update_user_invalid(self):
        user_id = self.db.insert_user("Daisy", 28)
        response, status = self.service.update_user(user_id, "", 0)
        self.assertEqual(status, 400)

    def test_update_user_not_found(self):
        response, status = self.service.update_user(999, "Nonexistent User", 40)
        self.assertEqual(status, 404)
        self.assertEqual(response["error"], "User not found")

    def test_delete_user(self):
        user_id = self.db.insert_user("Eve", 22)
        response, status = self.service.delete_user(user_id)
        self.assertEqual(status, 200)

    def test_delete_user_not_found(self):
        response, status = self.service.delete_user(999)
        self.assertEqual(status, 404)


if __name__ == "__main__":
    unittest.main()
