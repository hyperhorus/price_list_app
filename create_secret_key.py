import secrets

# Generate a secure random key
SECRET_KEY = secrets.token_hex(32)
print(SECRET_KEY)