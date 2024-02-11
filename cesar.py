alph = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
    'V', 'W', 'X', 'Y', 'Z'
]


def cesar(message, shift=0):
    final_message = []
    for i in range(len(message)):
        final_message.append(alph[(alph.index(message[i]) + shift) % len(alph)] if message[i].isalpha() else message[i])
    return "".join(final_message)
