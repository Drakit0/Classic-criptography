import json
import random


def initial_interface() -> str: # General interface
    print("""
          ====================== Menu ======================

          1. César
          2. Vigènere
          3. DES
          4. Exit
          
          ==================================================
          """)
     
def Cesar_interface() -> str: # Cesar interface
    print("""
          ================= Cifrado César ==================
          
          1. Cifrar un texto con un desplazamiento introducida por el usuario.
          2. Descifrar un texto con un desplazamiento introducido por el usuario.
          3. Descifrar un texto sin conocer el desplazamiento (recomendado su uso con textos extensos).
          4. Exit.
          
          ==================================================
          """)
        
def Vigenere_interface() -> str: # Vigenere interface
    print("""
          =============== Cifrado Vigenere =================
          
          1. Cifrar un texto con una clave introducida por el usuario.
          2. Descifra un texto con una clave introducida por el usuario.
          3. Descifra un texto sin conocer la clave (recomendado su uso con textos extensos).
          4. Exit.
          
          ==================================================
          """)

def Des_interface() -> str: # DES interface
    print("""
          ================ Cifrado DES =====================
          
          1. Cifrar un texto con una clave introducida por el usuario.
          2. Descifra un texto con una clave introducida por el usuario. 
          3. Exit.
          
          ==================================================
          """)
    
def option_elements(allowed_values:list) -> int: # Option verify
    """
    Permite al usuario elegir entre las opciones del programa.
    """
    
    wrong_option = True
    
    easter = random.randint(1,10)
    
    while wrong_option:
        try:
            option = int(input("Introduzca la opción del programa que quiere usar: "))
            if option in allowed_values:
                wrong_option = False
                
            else:
                print("Wrong option")
                
                if easter == 5:
                    print(f"Se pide un número perteneciente a {allowed_values}, no la receta de albóndigas de tu abuela...")
                
        except ValueError as error:
            print(error)
            
    return option


def cipher_decipher_input(option:str) -> str: # Text input
    """
    Permite al usuario elegir si va a introducir unas palabras a cifrar/descifrar
    o si va a introducir el nombre de un fichero para cifrar/descifrar todo el fichero.
    """
    
    wrong_name = True
    
    while wrong_name:
        wrong_type = True
        
        while wrong_type:
            try: # type selection
                input_type = (input(f"¿Cómo quiere introducir el texto a {option}, a mano o a traves de un fichero?(fichero/mano/exit) ")).lower()
                input_type = input_type.replace(" ","")
                
            except (SyntaxError or TypeError) as error:
                print(error)
                
            if (input_type == "fichero") or (input_type == "mano") or (input_type == "exit"):
                wrong_type = False
                
            else:
                print("Lo sentimos, " + input_type + " no es una opción contemplada por el programa.")
        
        if input_type == "mano" : # written input
            plain_text = str(input(f"Introduzca el texto que quiera {option} a continuación: "))
            wrong_name = False
            
        elif input_type == "fichero": # file input
            try:
                file_name = input(f"Introduzca el nombre del archivo a {option}, el programa sólo trabaja con input de tipo \".txt\" (Se pueden usar directamente los ficheros generados por el programa): ")
                if ".txt" not in file_name:
                    file_name = file_name + ".txt" 
                file = open(file_name, "r", encoding='utf-8')
                plain_text = file.read()
                file.close()
                wrong_name = False
                
            except FileNotFoundError as error:
                print(error)
                
        else:
            plain_text = input_type
            wrong_name = False
            wrong_type = False
            
    return plain_text
                        
def file_creation (text_input:str, text_output:str, key:str, name:str):
    """
    Permite al usuario crear un fichero con el texto trabajado.
    """
    
    wrong_answer = True
    
    while wrong_answer:
        answer = (input("¿Quiere guardar el texto con el que has trabajado?(s/n) ").lower()).replace(" ","")
        
        if (answer == "s") or (answer == "n"):
            wrong_answer = False
            
    if answer == "s": # file creation
        wrong_answer = True
        
        while wrong_answer:
            answer = (input("¿En qué formato quiere guardar el texto con el que has trabajado?(txt/json) ").lower()).replace(" ","")
            
            if (answer == "txt") or (answer == "json"):
                wrong_answer = False
                
        if answer == "txt": # txt type
            file_name = input("Introduzca el nombre del fichero que quiere crear: ")
            file = open("worked_files/" + file_name + ".txt", "w", encoding = "utf-8")
            file.write("Cipher: " + name + "\n" + "Key: " + str(key) + "\n" + "Input text: " + text_input + ("\n"*2) + ("="*100) + ("\n"*2) + "Output text: " + text_output)
            file.close()
            print("Fichero txt creado.")
            
        else: # json type
            file_name = input("Introduzca el nombre del fichero que quiere crear: ")
            data = {
                "Cipher": name,
                "Key": key,
                "Input text": text_input,
                "Output text": text_output
            }
            
            with open("worked_files/" + file_name + ".json", "w", encoding = "utf-8") as file:
                json.dump(data, file)
                
            print("Fichero json creado.")
            
    else:
        print("El fichero no será creado.")