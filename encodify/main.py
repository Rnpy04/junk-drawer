import base64

def xor_encrypt_decrypt(text: str, key: str) -> str:
    text_bytes = text.encode("utf-8")
    key_bytes = key.encode("utf-8")

    result = bytearray()
    for i in range(len(text_bytes)):
        result.append(text_bytes[i] ^ key_bytes[i % len(key_bytes)])

    return base64.b64encode(result).decode("utf-8")


def xor_decrypt(cipher_text: str, key: str) -> str:
    cipher_bytes = base64.b64decode(cipher_text)
    key_bytes = key.encode("utf-8")

    result = bytearray()
    for i in range(len(cipher_bytes)):
        result.append(cipher_bytes[i] ^ key_bytes[i % len(key_bytes)])

    return result.decode("utf-8")


if __name__ == "__main__":
    while(True):
        a=int(input("encode or decode ? 1/2  :"))
        if(a==1): 
            message = input("write it : ")
            password = input("password : ")
            encrypted = xor_encrypt_decrypt(message, password)
            print("Encrypted:", encrypted)
        elif(a==2):
            message = input("write it : ")
            password = input("password : ")
            decrypted = xor_decrypt(message, password)
            print("Decrypted:", decrypted)
        con=int(input('continue ?0/1  :'))
        if con==0:
            break
        
