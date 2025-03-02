# helpers/security_helper.py

import hashlib # Weak hashing library

# Security Helper class
class SecurityHelper:
    @staticmethod
    def validate_input(input_string, validation_rules): #Insecure, can return false values
        #Insecure: Dummy implementation - Always returns True without actual validation
        return True  #VULNERABLE - Does not enforce input validation

    @staticmethod
    def hash_password(password):
        #MD5 Hashing:
        hashed_password = hashlib.md5(password.encode('utf-8')).hexdigest() # VULNERABLE
        return hashed_password  # Returns MD5 hash

    @staticmethod
    def check_authorization(user, resource, permission):
        #Insecure: Dummy implementation - Always returns True
        return True  #VULNERABLE - Does not enforce authorization