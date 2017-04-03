import scipy.signal as signal
import numpy as np

morse_alphabet = {
    # define morse alphabet
    "A": ".-",
    "B": "-...",
    "C": "-.-.",
    "D": "-..",
    "E": ".",
    "F": "..-.",
    "G": "--.",
    "H": "....",
    "I": "..",
    "J": ".---",
    "K": "-.-",
    "L": ".-..",
    "M": "--",
    "N": "-.",
    "O": "---",
    "P": ".--.",
    "Q": "--.-",
    "R": ".-.",
    "S": "...",
    "T": "-",
    "U": "..-",
    "V": "...-",
    "W": ".--",
    "X": "-..-",
    "Y": "-.--",
    "Z": "--..",
    " ": "/"
}


def get_binary_morse(morseAlphabet):
    # transform morse to binary morse
    morseAlphabetBinary = {}
    for letter in morseAlphabet:
        binaryCode = ""
        for l in morseAlphabet[letter]:
            if l == '-':
                binaryCode += "111"
            if l == '.':
                binaryCode += "1"
            binaryCode += "0"
        morseAlphabetBinary[binaryCode[:-1]] = letter

    return morseAlphabetBinary


def find_sample_size(text):
    # determine sample size based on binary text
    # count chunks of zeros and take the most
    # frequent one
    zero = False
    count = 0
    number = {}
    for t in text:
        if t == 0:
            if zero is False:
                if count > 0:
                    if count in number:
                        number[count] += 1
                    else:
                        number[count] = 1
                zero = True
                count = 1
            else:
                count += 1
        else:
            zero = False
    max = 0
    size = 0
    for n in number:
        if number[n] > max:
            size = n
            max = number[n]
    return size


def simplify_morse(text, sample_size):
    # determine simplified string
    morseText = ""
    i = 0
    while i < len(text):
        morseText += str(int(text[i]))
        i += sample_size
    return morseText


def get_decoded_message(words, morse_alphabet_binary):
    decoded = ""
    for word in words:
        letters = word.split("000")
        for letter in letters:
            decoded += morse_alphabet_binary[letter]
        decoded += " "

    return decoded.lower()


def filter_wiener(text):
    # use wiener filter to filter noise
    lt = len(set(text))
    if lt > 2:
        text = signal.wiener(np.asarray(text), 15)
    # use filtered signal to determine binary message
    for i, t in enumerate(text):
        if t > 0.5:
            text[i] = 1
        else:
            text[i] = 0
    return text


def error_corr(text, sample_size):
    # determine incorrect "lines" in messge based on
    # average value in one chunk
    i = 0
    while i < len(text):
        avg = round(sum(text[i:i + sample_size]) * 1.0 / sample_size)
        for j in range(i, i + sample_size):
            text[j] = int(avg)
        i += sample_size
    return text


if __name__ == "__main__":
    input_text_file = raw_input()
    text = []
    with open(input_text_file, "r") as f:
        for line in f:
            text.append(float(line[:-1]))

    text = filter_wiener(text)
    sample_size = find_sample_size(text)
    corr_text = error_corr(text, sample_size)
    morse_text = simplify_morse(corr_text, sample_size)
    words = morse_text.split("0000000")
    morse_alphabet_binary = get_binary_morse(morse_alphabet)
    decoded = get_decoded_message(words, morse_alphabet_binary)

    print decoded.strip()


