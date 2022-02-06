import os
from random import randint
from random import choice as r_ch


def chr_arr2str(array1):  # converts array of characters
    new_string = ""       # to string
    for i in array1:
        new_string += i
    return new_string


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def read_file(path):
    with open(path) as f:
        qwer = f.readlines()
    f.close()
    return qwer


def load_words():  # gives all existing words in english language
    with open('words_alpha.txt') as word_file:
        valid_words = set(word_file.read().split())
    return valid_words


def contains_invalid_words(new_message: str) -> bool:
    print(new_message)
    valid_words = load_words()
    arr3 = new_message.split()
    invalid_word: bool = False
    word_is_real: bool
    for word in arr3:
        word_is_real = False
        for valid_word in valid_words:
            if word == valid_word:
                word_is_real = True
                break
        if not word_is_real:
            invalid_word = True
            break
    return invalid_word


def modify_key(t_key: dict) -> dict:
    num1: int = (randint(1, 26)) + 64
    num2: int = (randint(1, 26)) + 64
    chr1 = chr(num1)
    chr2 = chr(num2)
    t_key[chr1], t_key[chr2] = t_key[chr2], t_key[chr1]
    return t_key


def rail_fence_mini(line, spreading, start_pos):
    arr = ["" for x in range(len(line))]
    down: bool = False
    array = []
    if start_pos == 0:
        down = True
    opt = [1, 1, 1, 2, 2, 2, 9, 9]  # options for random choice
    opt_grammar = ['!', ',', '?', '.', ' ']  # grammatical choices
    yy = 0
    for i in range(len(line)):
        for j in range(spreading):
            if j == start_pos:
                arr[j] += line[yy]
            else:  # r_ch -> random choice
                if r_ch(opt) == 1:
                    arr[j] += chr((randint(0, 25)) + 97)
                elif r_ch(opt) == 2:
                    arr[j] += chr((randint(0, 25)) + 65)
                else:
                    arr[j] += r_ch(opt_grammar)
        if start_pos == spreading - 1:
            down = False
        elif start_pos == 0:
            down = True
        if down:
            start_pos += 1
        else:
            start_pos -= 1
        yy += 1
    for i in range(spreading):
        array.append(arr[i])
    return array


def enc_rail_fence(start_pos, line_count, path) -> str:
    start_pos -= 1
    os.system("sed -i \'/^$/d\' " + path)
    lines = read_file(path)
    new_path = path[:-4] + "_encrypted.txt"
    with open(new_path, 'w') as file1:
        for line in lines:
            array = rail_fence_mini(line, line_count, start_pos)
            for new_line in array:
                file1.write(new_line)
                file1.write("\n")
    os.system("sed -i \'/^$/d\' " + new_path)
    str1 = "Your encrypted file is the same folder as original file."
    str2 = "Written with _encrypted in it's name."
    return str1+str2


def sub_encrypt_decrypt(hidden_message: str, key1: dict) -> str:
    print("The type of key1: " + str(type(key1)))
    chr_array = [char for char in hidden_message]
    array2 = []
    for chr1 in chr_array:
        if chr1 in key1:
            array2.append(key1.get(chr1))
        else:
            array2.append(chr1)
    new_message = chr_arr2str(array2)
    return new_message


def enc_subst_cypher(path, cypher) -> str:
    lines = read_file(path)
    new_path = path[:-4] + "_encryptedd.txt"
    with open(new_path, 'w') as file1:
        for line in lines:
            message = sub_encrypt_decrypt(line, cypher)
            file1.write(message)
            file1.write("\n")
    os.system("sed -i \'/^$/d\' " + new_path)
    str1 = "Your bbbbbbbbbbbbbbbbbbbb file."
    str2 = "Written with _encrypted in it's name."
    return str1+str2


def encryption_guide() -> str:
    print(
        "You have chosen encryption. Please choose between"
        "2 methods of encryption available - rail fence cypher"
        "or substitution cypher."
    )
    choice2: str = input("Enter rail fence or substitution: ")
    choice2 = choice2.lower()
    if choice2 == "rail fence":
        location = input("Please enter file location: ")
        print("You have to enter 2 numbers - line count and starting position.")
        print("If you enter non-number input, program will crush!")
        lines = int(input("Please enter line count: "))
        print("Position can't be bigger than line count")
        j: int = 0
        while True:
            start_pos = int(input("Please enter starting position: "))
            if start_pos <= lines:
                message = enc_rail_fence(start_pos, lines, location)
                return message
            else:
                print("Position can't be bigger than line count")
                print("Try again!")
            if j < 5:
                j += 1
            else:
                return "Error! Program crushed!"
        
    elif choice2 == "substitution":
        location = input("Please enter file location: ")
        print("You have to enter line of 26 letter cypher replacing alphabet.")
        print("Each letter must be unique!")
        print("Example: NEWPRAVDBGHJIQXYZFUCKLMOST")
        print("If you enter wrong input, program will crush!")
        print("Two same letters will lead to encrypted file be unusable!")
        j: int = 0
        while True:
            cypher = input("Please enter encryption alphabet ")
            cypher = cypher.upper()
            # print(len(cypher))
            if len(cypher) == 26:
                enc_key: dict = {}
                for w in range(26):
                    enc_key.update({chr(65+w): cypher[w]})
                    enc_key.update({chr(97 + w): chr(ord(cypher[w]) + 32)})
                    # chr(ord(chr1) + 32)
                return enc_subst_cypher(location, enc_key)
            else:
                print("Input wrong. Try again!")
            if j < 5:
                j += 1
            else:
                return "Error! Program crushed!"
    else:
        return "Your choice wasn't a valid choice"


def dec_rail_fence(start_pos, line_count, path) -> str:
    start_pos -= 1
    lines = read_file(path)
    lines_by_spread = chunks(lines, line_count)
    new_path = path[:-4] + "_decrypted.txt"
    with open(new_path, 'w') as file2:
        for lines1 in lines_by_spread:
            first_arr = []
            other_arr = []
            for line in lines1:
                first_arr.append([char for char in line])
    
            for dm in first_arr:
                try:
                    dm.remove("\n")
                    other_arr.append(dm)
                except ValueError:
                    other_arr.append(dm)
            first_arr = []
            temp1 = other_arr[0]
            i = 0
            down: bool = False
            new_line = ""
            while i < len(temp1)-1:
                # print(other_arr[start_pos][i])
                new_line += other_arr[start_pos][i]
                if start_pos == line_count - 1:
                    down = False
                elif start_pos == 0:
                    down = True
                if down:
                    start_pos += 1
                else:
                    start_pos -= 1
                i += 1
            file2.write(new_line + "\n")
    str7 = "File with fence rail encoding is decoded and located at the same position"
    str8 = "as the encoded file"
    return str7 + str8


def dec_subst_cypher(path, cypher) -> str:
    lines = read_file(path)
    new_path = path[:-4] + "_decryptedd.txt"
    with open(new_path, 'w') as file1:
        for line in lines:
            message = sub_encrypt_decrypt(line, cypher)
            file1.write(message)
            file1.write("\n")
    os.system("sed -i \'/^$/d\' " + new_path)
    str1 = "Your decrypted file!"
    str2 = "In it's neighborhood of original file."
    return str1+str2


def decryption_guide():
    print(
        "You have chosen decryption. Please choose between "
        "2 methods of decryption available - rail fence cypher"
        "or substitution cypher."
    )
    choice2 = input("Enter rail fence or substitution: ")
    choice2 = choice2.lower()
    if choice2 == "rail fence":
        print("Example: path/to/file.txt 5 2")
        str5: str = "Enter path to file, expansion rate and start position: "
        about = (input(str5)).split()
        message = dec_rail_fence(about[0], int(about[1]), int(about[2]))
        return message
    elif choice2 == "substitution":
        location = input("Please enter file location: ")
        print("You have to enter line of 26 letter cypher replacing alphabet.")
        print("Each letter must be unique!")
        print("Example: NEWPRAVDBGHJIQXYZFUCKLMOST")
        print("If you enter wrong input, program will crush!")
        print("Two same letters will lead to encrypted file be unusable!")
        j: int = 0
        while True:
            cypher = input("Please enter decryption alphabet ")
            cypher = cypher.upper()
            # print(len(cypher))
            if len(cypher) == 26:
                enc_key: dict = {}
                for w in range(26):
                    enc_key.update({cypher[w]: chr(65 + w)})
                    enc_key.update({chr(ord(cypher[w]) + 32): chr(97 + w)})
                    # chr(ord(chr1) + 32) chr(97 + w)
                return dec_subst_cypher(location, enc_key)
            else:
                print("Input wrong. Try again!")
            if j < 5:
                j += 1
            else:
                return "Error! Program crushed!"
    else:
        return "Your choice wasn't a valid choice"


if __name__ == '__main__':
    ii: int = 0
    while True:
        print("Welcome to your safe information program. Please choose an action")
        print("which one you want to do today - encryption or decryption?")
        choice1: str = input("Enter encrypt or decrypt: ")
        choice1 = choice1.lower()
        if choice1 == "encrypt":
            enc_file = encryption_guide()
            print(enc_file)
            break
        elif choice1 == "decrypt":
            text_file = decryption_guide()
            print(text_file)
            break
        else:
            print("Your choice wasn't a valid choice")
        if ii < 5:
            ii += 1
        else:
            print("Exiting program")
            break
