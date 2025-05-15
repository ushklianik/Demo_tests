import pytest
import os
from datetime import datetime
from start import read_and_order_users  # Replace `your_module` with the actual module name

# Helper function to create temporary CSV files for testing
def create_temp_csv(file_path, content):
    with open(file_path, mode='w', encoding='utf-8') as file:
        file.write(content)

# Test cases
def test_valid_credentials_and_ordering(tmp_path):
    # Create a temporary CSV file
    file_path = tmp_path / "users.csv"
    content = """username,password,creation_date
admin,password123,2023-01-01
user1,pass1,2023-02-15
user2,pass2,2023-03-10
user3,pass3,2022-12-25
"""
    create_temp_csv(file_path, content)

    # Call the function with valid credentials
    result = read_and_order_users(file_path=str(file_path), username="admin", password="password123")

    # Expected output
    expected = [
        {"username": "user3", "password": "pass3", "creation_date": "2022-12-25"},
        {"username": "admin", "password": "password123", "creation_date": "2023-01-01"},
        {"username": "user1", "password": "pass1", "creation_date": "2023-02-15"},
        {"username": "user2", "password": "pass2", "creation_date": "2023-03-10"},
    ]

    assert result == expected


def test_invalid_credentials(tmp_path):
    # Create a temporary CSV file
    file_path = tmp_path / "users.csv"
    content = """username,password,creation_date
admin,password123,2023-01-01
user1,pass1,2023-02-15
"""
    create_temp_csv(file_path, content)

    # Call the function with invalid credentials
    with pytest.raises(ValueError, match="Invalid credentials"):
        read_and_order_users(file_path=str(file_path), username="admin", password="wrongpassword")


def test_missing_file():
    # Call the function with a non-existent file
    with pytest.raises(FileNotFoundError, match="The file at path 'non_existent.csv' does not exist."):
        read_and_order_users(file_path="non_existent.csv", username="admin", password="password123")


def test_malformed_creation_date(tmp_path):
    # Create a temporary CSV file with invalid creation_date
    file_path = tmp_path / "users.csv"
    content = """username,password,creation_date
admin,password123,invalid_date
user1,pass1,2023-02-15
"""
    create_temp_csv(file_path, content)

    # Call the function and expect an exception
    with pytest.raises(Exception, match="Invalid or missing creation_date for user:"):
        read_and_order_users(file_path=str(file_path), username="admin", password="password123")


def test_empty_csv_file(tmp_path):
    # Create an empty CSV file
    file_path = tmp_path / "users.csv"
    create_temp_csv(file_path, "")

    # Call the function and expect an exception
    with pytest.raises(Exception, match="An error occurred while processing the file:"):
        read_and_order_users(file_path=str(file_path), username="admin", password="password123")


def test_no_matching_credentials(tmp_path):
    # Create a temporary CSV file
    file_path = tmp_path / "users.csv"
    content = """username,password,creation_date
user1,pass1,2023-02-15
user2,pass2,2023-03-10
"""
    create_temp_csv(file_path, content)

    # Call the function with credentials that don't match any user
    with pytest.raises(ValueError, match="Invalid credentials"):
        read_and_order_users(file_path=str(file_path), username="admin", password="password123")


def test_partial_data(tmp_path):
    # Create a temporary CSV file with missing columns
    file_path = tmp_path / "users.csv"
    content = """username,password
admin,password123
user1,pass1
"""
    create_temp_csv(file_path, content)

    # Call the function and expect an exception due to missing `creation_date`
    with pytest.raises(Exception, match="Invalid or missing creation_date for user:"):
        read_and_order_users(file_path=str(file_path), username="admin", password="password123")


def test_valid_credentials_with_single_user(tmp_path):
    # Create a temporary CSV file with a single user
    file_path = tmp_path / "users.csv"
    content = """username,password,creation_date
admin,password123,2023-01-01
"""
    create_temp_csv(file_path, content)

    # Call the function with valid credentials
    result = read_and_order_users(file_path=str(file_path), username="admin", password="password123")

    # Expected output
    expected = [
        {"username": "admin", "password": "password123", "creation_date": "2023-01-01"},
    ]

    assert result == expected
