class Polibius:
    psquare = [
        ['A', 'B', 'C', 'D', 'E'],
        ['F', 'G', 'H', 'I/J', 'K'],
        ['L', 'M', 'N', 'O', 'P'],
        ['Q', 'R', 'S', 'T', 'U'],
        ['V', 'W', 'X', 'Y', 'Z']]

    def encrypt(self, message):
        encrypted_message = []
        for letter in message:
            for i in range(5):
                for j in range(5):
                    if letter in self.psquare[i][j]:
                        encrypted_message.append(str(i + 1) + str(j + 1))
        return ''.join(encrypted_message)

    def decrypt(self, digits: str):
        decrypt_message = []
        for i in range(0, len(digits), 2):
            decrypt_message.append(self.psquare[int(digits[i]) - 1][int(digits[i + 1]) - 1])
        return "".join(decrypt_message)




