# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from cryptography.fernet import Fernet

ENCRYPTION_SECRET = None


def encrypt_fernet(value):
    f = Fernet(ENCRYPTION_SECRET)
    return 'fernet${}'.format(f.encrypt(value.encode('utf8')).decode('utf8'))


def decrypt_fernet(value):
    f = Fernet(ENCRYPTION_SECRET)
    decrypted_data = f.decrypt(value.encode('utf8')).decode('utf8')
    return decrypted_data