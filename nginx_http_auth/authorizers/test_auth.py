def authenticate(self, request, username, password):
    if username == 'test' and password == 'test':
        return True
    else:
        return False