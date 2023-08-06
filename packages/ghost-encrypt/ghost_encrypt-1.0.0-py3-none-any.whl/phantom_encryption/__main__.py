# __main__.py

from .encryption import *
from arg_parser import *
import os


def main():

    reg = Register()
    reg.add(Command("--simple-encrypt", "Encrypts a string with a (given) key", ["-s"], ["-k", "-of"]))
    reg.add(Command("--se", "....", ["-s"], ["-k", "-of"]))
    reg.add(Parameter("-s", "String to de-/encrypt"))
    reg.add(Parameter("-k", "Key for de-/encryption"))
    reg.add(Parameter("-of", "File to write the decrypted string in"))

    reg.add(Command("--simple-decrypt", "Decrypts a string with a key", ["-s", "-k"], ["-of"]))
    reg.add(Command("--sd", "....", ["-s", "-k"], ["-of"]))

    reg.add(Command("--encrypt-file", "Encrypts a file with a given or random key", ["-p"], ["-k, -r"]))
    reg.add(Command("--ef", "....", ["-p"], ["-k, -r"]))
    reg.add(Parameter("-p", "Path to the file to de-/encrypt"))
    reg.add(Parameter("-r", "Register-file for storing the keys, 'def' for default register."))

    reg.add(Command("--decrypt-file", "Decrypts a file with a given key the decypters key or a register", None,
                    ["-p", "-k", "-r"]))
    reg.add(Command("--df", "....", None, ["-p", "-k", "-r"]))

    parser = Parser(reg)


    encryptor = Encryptor()
    decrypter = Decrypter()


    @parser("--simple-encrypt", "--se")
    def simple_encrypt(opts: dict):
        key = None if not opts.__contains__("-k") else opts["-k"]
        key, value = encryptor.encrypt(opts["-s"], key)
        if not opts.__contains__("-of"):
            value = value.replace("\"", "\\\"").replace("\'", "\\'")
            print(f"Key: {key}\nEncrypted: {value}")
        else:
            with open(opts["-of"], "w") as f:
                f.write("Key: " + key.string + "\nEncrypted: " + value)
                f.close()
                log("Encryption", f"Info: Wrote encrypted string to {opts['-of']}")


    @parser("--simple-decrypt", "--sd")
    def simple_decrypt(opts: dict):
        key = None if not opts.__contains__("-k") else opts["-k"]
        decrypted = decrypter.decrypt(opts["-s"], key)
        if not opts.__contains__("-of"):
            print(decrypted)
        else:
            with open(opts["-of"], "wb") as f:
                f.write(decrypted.encode("utf-8"))
                f.close()
                log("Decryption", f"Info: Wrote decrypted string to {opts['-of']}")


    @parser("--encrypt-file", "--ef")
    def encrypt_file(opts: dict):
        key = None if not opts.__contains__("-k") else opts["-k"]
        register = None if not opts.__contains__("-r") else opts["-r"]
        if register == "def":
            register = "".join([_ + "\\" for _ in __file__.split("\\")[:-1]]) + "data\\.reg"
        key = encryptor.encrypt_file(opts["-p"], key)
        if register:
            new_lines = ""
            try:
                with open(register, "r") as f:
                    for line in f.read().split("\n"):
                        lin = line
                        if line.__contains__(": "):
                            line = line.split(": ")
                            if line[0].replace("\\", "/") != os.path.realpath(opts["-p"]).replace("\\", "/"):
                                new_lines += lin + "\n"
                    f.close()
            except FileNotFoundError:
                pass
            with open(register, "w") as f:
                f.write(f"{new_lines}{os.path.realpath(opts['-p'])}: {key if key else encryptor.key}\n")
                f.close()
            log("Encryption", f"Info: Wrote key '{key if key else encryptor.key}' to register at '{register}'")


    @parser("--decrypt-file", "--df")
    def decrypt_file(opts: dict):
        key = None if not opts.__contains__("-k") else opts["-k"]
        register = None if not opts.__contains__("-r") else opts["-r"]
        if register:
            if register == "def":
                register = "".join([_ + "\\" for _ in __file__.split("\\")[:-1]]) + "data\\.reg"
            files = []
            try:
                with open(register, "r") as f:
                    for line in f.read().split("\n"):
                        if line.__contains__(": "):
                            files.append(line.split(": "))
                    f.close()
            except FileNotFoundError:
                raise FileNotFoundError(f"Register wasn't found at {opts['-p']}")

            c = 0
            for file, key in files:
                c += 1
                decrypter.decrypt_file(file, key)
            with open(register, "w") as f:
                f.write("")
                f.close()
            log("Decryption", f"Info: Decrypted {c} files with register at '{register}'")
        else:
            decrypter.decrypt_file(opts["-p"], key)

if __name__ == "__main__":
    main()
