import random
import string

def generate_password(length):
    # Define possible characters: letters, digits, punctuation
    characters = string.ascii_letters + string.digits + string.punctuation
    # Randomly choose characters from the set
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def main():
    try:
        length = int(input("Enter desired password length: "))
        if length <= 0:
            print("Password length must be greater than 0.")
        else:
            password = generate_password(length)
            print("Generated Password:", password)
    except ValueError:
        print("Please enter a valid number.")

if __name__ == "__main__":
    main()
