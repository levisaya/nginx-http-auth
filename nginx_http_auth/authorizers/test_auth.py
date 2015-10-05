port = 80
secret_key = b'\x95\r\x16\xd26\xdb\xa9\x85@=\x03\xd1\xb1\xbe\x13\xd4\xa4q\x08\xd6\xb2\xc1\x1f*'
template = None


def authenticate(self, request, username, password):
    if username == 'test' and password == 'test':
        return True
    else:
        return False