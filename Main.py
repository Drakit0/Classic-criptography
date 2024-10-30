import re
import os
import Cesar_Vigenere_functions as cv
import DES_functions as des
import General_functions as gf


if __name__ == "__main__":
    program_running = True

    print("Bienvenido al software de cifrado y descifrado de textos." + "\n")

    while program_running:
        
        gf.initial_interface()
        
        option = gf.option_elements([1,2,3,4])
                
        if option == 1: # Cesar
            gf.Cesar_interface()
            c_option = gf.option_elements([1,2,3,4])
            
            if c_option == 1: # Cipher
                print("\n"*2 + "1. Cifrado de un texto con un desplazamiento dado" + "\n")
                text = gf.cipher_decipher_input("cifrar")
                
                if text != "exit":
                    wrong_displacement = True
                    
                    while wrong_displacement:
                        try:
                            displacement = int(input("Introduzca el número de desplazamientos a realizar: "))
                            wrong_displacement = False
                            
                        except TypeError as error:
                            print(error)
                            
                    while displacement > 26:
                        displacement = displacement - 26
                        
                    encrypted_text = cv.cesar_cipher(text, displacement) # Encryption process
                    
                    print("Texto cifrado: " + encrypted_text)
                    gf.file_creation(text, encrypted_text, displacement, "César")
                
            elif c_option == 2: # Descifrar
                print("\n"*2 + "2. Desifra un texto con un desplazamiento dado" + "\n")
                text = gf.cipher_decipher_input("descifrar")
                
                if text != "exit":
                    wrong_displacement = True
                    
                    while wrong_displacement:
                        try:
                            displacement = int(input("Introduzca el número de desplazamientos a realizar: "))
                            wrong_displacement = False
                            
                        except TypeError as error:
                            print(error)
                            
                    while displacement > 26:
                        displacement = displacement - 26
                        
                    plain_text = cv.cesar_decipher(text, displacement) # Decryption process
                    
                    print("Texto descifrado: " + plain_text)
                    gf.file_creation(text, plain_text, displacement, "César")
                    
            elif c_option == 3:
                print("\n"*2 + "3. Descifrar un texto sin el desplazamiento" + "\n")
                print("""Aviso: Debido a la forma en la que se realiza el descifrado (a través de un análisis de frecuencias), 
                    no se puede asegurar que se vaya a obtener un texto coherente si el archivo posee menos de 3000 palabras.""") # Warning frequency analysis
                
                text = gf.cipher_decipher_input("descifrar")
                
                if text != "exit":
                    plain_text, displacement = cv.cesar_decipher_no_key(text) # Decryption process without key
                    
                    print("Desplazamiento: " + str(displacement) + "\n" + "Texto descifrado: " + plain_text)
                    gf.file_creation(text, plain_text, displacement, "César")
            
            else:
                print("\n"*2 + "4. Exit" + "\n")
            
                
        elif option == 2: # Vigenere
            gf.Vigenere_interface()
            v_option = gf.option_elements([1,2,3,4])   
            
            if v_option == 1: # Cipher
                print("\n"*2 + "1. Cifrar un texto con una clave dada" + "\n")
                text = gf.cipher_decipher_input("cifrar")
                
                if text != "exit":
                    key = input("Introduzca la clave con la que cifrar el texto: ")
                    
                    encrypted_text = cv.vigenere_cipher(text, key) # Encryption process
                    
                    print("Texto cifrado: " + encrypted_text)
                    gf.file_creation(text, encrypted_text, key, "Vigènere")

            elif v_option == 2: # Decipher
                print("\n"*2 + "2. Desifrar un texto con una clave dada" + "\n")
                text = gf.cipher_decipher_input("descifrar")
                
                if text != "exit":
                    key = input("Introduzca la clave con la que descifrar el texto: ")
                    
                    plain_text = cv.vigenere_decipher(text, key) # Decryption process
                    
                    print("Texto descifrado: " + plain_text)
                    gf.file_creation(text, plain_text, key, "Vigènere")
                
            elif v_option == 3: # Decipher no key
                print("\n"*2 + "3. Desifra un texto sin la clave" + "\n")
                print("""Aviso: Debido a la forma en la que se realiza el descifrado, a través del metodo de Kasiski, 
no se puede asegurar que se vaya a obtener un texto coherente si el archivo posee menos de 3000 palabras""") # Warning Kasiski method
                
                print("Available files:")
                print(os.listdir("files"))
                
                try:
                    
                    text = input("Introduce the name of the file to decipher (exit is also an option): ")
                    
                    if text != "exit":
                        
                        if "Output text:" in text:
                            regex = re.compile(r"Output text:(.*)") # Regular expression to find the text
                            text = regex.search(text).group(1)
                            print(text)
                        
                        plain_text, key= cv.vigenere_decipher_no_key(text) # Decryption process without key
                        
                        print("Texto cifrado: " + plain_text)
                        gf.file_creation(text, plain_text, key, "Vigènere")
                        
                except FileNotFoundError as error:
                    print(error)
                
            else:
                print("\n"*2 + "4. Exit" + "\n")
                
        elif option == 3: # DES
            gf.Des_interface()
            des_option = gf.option_elements([1,2,3])
            
            if des_option == 1: # Cipher
                print("\n"*2 + "1. Cifrar el texto con una clave dada" + "\n")
                text = gf.cipher_decipher_input("cifrar")
                
                if text != "exit":
                    key = input("""Introduzca la clave a usar sin que esté en binario, si su longitud es menor a 64 bits se completará con 0, 
    si su longitud es mayor se le pedirá una nueva contraseña: """)
                    
                    encrypted_text = des.des_cipher(text, key) # Encryption process
                    
                    print("Texto cifrado: " + encrypted_text)
                    gf.file_creation(text, encrypted_text, key, "DES")
                    
            elif des_option == 2: # Decipher
                print("\n"*2 + "2. Desifra el texto con una clave dada" + "\n")
                text = gf.cipher_decipher_input("descifrar")
                
                if text != "exit":
                    key = input("""Introduzca la clave a usar en texto plano, si su longitud es menor a 64 bits se completará con 0, 
    si su longitud es mayor se le pedirá una nueva contraseña: """)
                    
                    plain_text = des.des_decipher(text, key) # Decryption process
                    
                    print("Texto descifrado: " + plain_text)
                    gf.file_creation(text, plain_text, key, "DES")
                    
            else:
                print("\n"*2 + "3. Exit" + "\n")
                
        else:
            print("\n"*2 + "4. Exit" + "\n")
            program_running = False
            
    print("Gracias por usar el software de cifrado y descifrado de textos.")