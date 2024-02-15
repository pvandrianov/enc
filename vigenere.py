def get_key(l, keyword):
    key = ''
    while True:
        key += keyword
        if len(key) >= l:
            key = key[:l]
            break
    return key


class Vigenere:
    alph = [
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
        'V', 'W', 'X', 'Y', 'Z'
    ]

    def crypt(self, message, keyword, action='encrypt'):
        key = get_key(len(message), keyword)
        encrypted_message = []
        if action == 'encrypt' or action == 'decrypt':
            for i in range(len(message)):
                m = self.alph.index(message[i])
                k = self.alph.index(key[i])
                c = m + k if action == 'encrypt' else m - k
                encrypted_message.append(self.alph[c % len(self.alph)])
            return "".join(encrypted_message)
        else:
            return "Wrong 'action'"
