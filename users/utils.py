from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password

    

# for password validation
class PasswordVerifier:
    def hash_password(self, password):
        hashed_password = make_password(password)
        return hashed_password

    def verify_password(self, password, hashed_password):
        is_valid = check_password(password, hashed_password)
        return is_valid
    