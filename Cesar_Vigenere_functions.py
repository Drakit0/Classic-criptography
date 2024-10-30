from collections import Counter
from functools import reduce
import math


# Text ciphering


# Text cleaning

def tidyup_text(text: str) -> str:
    """
    Deletes spaces, commas, semicolons, etc.
    It also replaces accented vowels with unaccented vowels and ñ with n.
    Furthermore deletes any number or special character present in the message.
    """
    
    text = text.lower()
    clean_text = ""
    for character in text:
        if character in "bcdfghjklmpqrstvwxyz":
            clean_text += character
        elif character in "aáàâä":
            clean_text += "a"
        elif character in  "eèéêë":
            clean_text += "e"
        elif character in "iìíîï":
            clean_text += "i"
        elif character in "oòóôö":
            clean_text += "o"
        elif character in "uùúûü":
            clean_text += "u"
        elif character in "nñ":
            clean_text += "n"
        elif character in "ß":
            clean_text += "ss" 
            
    return clean_text

# Add positions

def sum_characters(c1: str, c2: str) -> str:
    """
    Adds the values of the positions of the characters and returns a new character whose
    position is the sum of the positions of the received characters.
    """
    
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    return alphabet[(alphabet.index(c1)+alphabet.index(c2))%26]

# cesar cipher

def cesar_cipher(text: str, displacement: int) -> str:
    """
    Returns the text encrypted with the Cesar algorithm, displacing each letter of the alphabet to a
    determined position.
    """
    
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    text = tidyup_text(text)
    encrypted_text = ""
    
    for character in text:
        encrypted_text += alphabet[(alphabet.index(character) + displacement) % 26]
        
    return encrypted_text

# Vigenère cipher

def vigenere_cipher(text: str, key: str) -> str:
    """
    Returns the Vigenère cipher with the given key, adding the value of each of the
    positions of the key to each position of the plain text.
    """
    
    text = tidyup_text(text)
    key = tidyup_text(key)
    encrypted_text = ""
    counter = 0
    length = len(key)
    
    for character in text:
        encrypted_text += sum_characters(character, key[counter % length]) 
        counter += 1
        
    return encrypted_text


# Text deciphering


# Frequency of characters

def character_count(text: str) -> dict:
    """
    Returns a dictionary with the frequencies of the different characters.
    """
    
    frequencies = Counter(text)
    
    for key in frequencies:
        frequencies[key] = (frequencies[key]/len(text))
        
    return dict(sorted(frequencies.items(), key=lambda item: item[0]))

# Subtraction of positions

def dif_characters(c1: str, c2: str) -> str:
    """
    Subtracts the values of the positions of the characters and returns a new character whose
    position is the difference of the positions of the received characters.
    """
    
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    return alphabet[(alphabet.index(c1)-alphabet.index(c2)) % 26]

# Index of coincidence

def match_index(text: str) -> float:
    """
    Given a text, it returns the index of coincidence: the probability that
    two randomly chosen characters are the same, allowing to identify the language of the text
    in substitution ciphers.
    """
    
    text = tidyup_text(text)
    length = len(text)
    counter = character_count(text) # frequencies of characters
    most_frequent_letter = (max(counter.values())) * length 
    index = (most_frequent_letter * (most_frequent_letter - 1))/(length * (length-1)) # formula of index of coincidence
    
    return index

#Compare the most common frequencies and keys of two dictionaries

def most_common_freq_comparation(dictionary:dict, encrypted_dictionary:dict) -> bool:
    """
    Compares the most common frequencies and keys of two provided dictionaries,
    if they are the same (using a 0.05 threshold) it will return True, 
    if they are different, False.
    """
    
    most_common_dictionary = (Counter(dictionary)).most_common(2) # 2 most common characters of the plain text
    most_common_cncrypted = (Counter(encrypted_dictionary)).most_common(2) # 2 most common characters of the encrypted text
    threshold = 0.05
    
    if (abs(most_common_dictionary[0][1] - most_common_cncrypted[0][1]) < threshold) and \
        (abs(most_common_dictionary[1][1] - most_common_cncrypted[1][1]) < threshold) and \
        ((most_common_dictionary[0][0] == most_common_cncrypted[0][0]) and \
         (most_common_dictionary[0][0] == most_common_cncrypted[0][0])): # Compare the most common frequencies and keys of two dictionaries
        correct_frequencies = True
        
    else:
        correct_frequencies = False
        
    return correct_frequencies

# Key length of Vigenère

def key_length(encrypted_text:str) -> int:
    """
    Returns the key length of the text encrypted with Vigenère
    through the Kasiski method: examinate the frequencies of the most common trigraphs.
    """
    
    encrypted_text = tidyup_text(encrypted_text)
    trigraphs = {}
    
    for letter in range(len(encrypted_text)-2): # Obtain the trigraphs of the encrypted text
        trigraph = encrypted_text[letter:letter+3]
        
        if trigraph in trigraphs:
            trigraphs[trigraph] += 1
            
        else:
            trigraphs[trigraph] = 1
    
    most_common_trigraphs = (sorted(trigraphs.items(), key=lambda item:item[1], reverse=True))[:20] # 20 most common trigraphs
    most_common_trigraphs = [trigraph for trigraph in most_common_trigraphs if trigraph[1] > 3] # Trigraphs that appear more than 3 times

    key_lengths = []
    
    for most_common_trigraph in most_common_trigraphs: # Analyze each of the most common trigraphs separately
        trigraphs_positions = []
        
        for pos in range(len(encrypted_text)-2): # Obtain the positions of the trigraph
            if encrypted_text[pos:pos+3] == most_common_trigraph[0]:
                trigraphs_positions.append(pos)
                
        dif_positions = []
        
        for i in range(len(trigraphs_positions)): # Obtain the differences between the positions of the trigraph
            for j in range(i+1, len(trigraphs_positions)):
                dif_positions.append(trigraphs_positions[j]-trigraphs_positions[i])  
                
        key_lengths.append(reduce(lambda x,y: math.gcd(x, y), dif_positions)) # Save the gcd of the differences between the positions of the trigraph
        
    most_common_key_length = Counter(key_lengths).most_common(1)[0][0] # The key length is the most common gcd of the differences between the positions of the trigraph
    
    return most_common_key_length



# Obtaining the key with the same system with which Cesar is broken knowing key length

def key_obtain(encrypted_text:str, key_length:int) -> str:
    """
    Returns the key used to encrypt Vigenère, through a Cesar decryption without a key every n letters 
    (result of the length of the key).
    """
    
    encrypted_text = tidyup_text(encrypted_text)
    key = ""
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    
    for letter in range(key_length): # Obtain the key letter by letter
        text = ""
        
        for position in range(letter, len(encrypted_text)-key_length, key_length): # Obtain the text that was encrypted with the same letter of the key
            text += encrypted_text[position]  
            
        key_letter = cesar_decipher_no_key(text) # Obtain the key letter
        key_letter = alphabet[key_letter[1]]
        key  += key_letter
        
    return key
  
# Cesar deciphering with displacement

def cesar_decipher(encrypted_text: str, displacement: int) -> str:
    """
    Returns the original text that was encrypted with Cesar, knowing the displacement made.
    """
    
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    encrypted_text = tidyup_text(encrypted_text)
    plain_text = ""
    
    for caracter in encrypted_text: # Substract the displacement to each character
        plain_text += alphabet[(alphabet.index(caracter)-displacement) % 26]
        
    return plain_text
    
# Cesar deciphering without knowing the displacement

def cesar_decipher_no_key(encrypted_text: str) -> tuple:
    """
    Returns the original text that was encrypted with Cesar, without knowing the displacement made.
    (Add here new languages and texts to compare the encrypted text with, they must be in the same folder
    as the program and in txt format. The texts must be written with arabuc characters)
    """
    
    dune = open("files/dune.txt", "r") # file in english
    dune_content = tidyup_text(dune.read())
    dune.close()
    
    tnes = open("files/die.txt", "r") # file in german
    tnes_content = tidyup_text(tnes.read())
    tnes.close()
    
    two = open("files/dos.txt", "r") # file in spanish
    two_content = tidyup_text(two.read())
    two.close()
    
    encrypted_text = tidyup_text(encrypted_text) # Clean the encrypted text
    encrypted_text_original = encrypted_text 
    
    wrong_disposition = True
    
    if match_index(encrypted_text) <= (match_index(two_content) + (match_index(dune_content) - match_index(two_content))/2): # Compare the index of coincidence of the encrypted text with the index of coincidence of the languages
        dictionary = character_count(two_content) 
        
    elif match_index(encrypted_text) <= (match_index(dune_content) + (match_index(tnes_content) - match_index(dune_content))/4):
        dictionary = character_count(dune_content)
        
    elif match_index(encrypted_text) <= (match_index(tnes_content) + (match_index(dune_content) - match_index(two_content))/2):
        dictionary = character_count(tnes_content)
        
    else:
        print("The text entered in the system is not encrypted with the Cesar algorithm or is not among the predetermined languages of the program (German/Spanish/English).")
        
        wrong_disposition = False
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        dictionary = dict.fromkeys(alphabet, 0)
    
    displacement = 0
    encrypted_dictionary = character_count(encrypted_text)
    
    if most_common_freq_comparation (dictionary, encrypted_dictionary) and  not (dictionary["a"] == 0): # Compare the most common frequencies and keys of two dictionaries
        wrong_disposition = False    
        
    while wrong_disposition:
        displacement += 1
        encrypted_dictionary = character_count(cesar_decipher(encrypted_text_original,displacement))
        
        if most_common_freq_comparation (dictionary, encrypted_dictionary): # Compare the most common frequencies and keys of two dictionaries
            wrong_disposition = False
            
        if displacement > 26: # Safe condition in which the displacement is greater than 26 (the maximum displacement)
            displacement = 0
            wrong_disposition = False
            
    plain_text = cesar_decipher(encrypted_text_original, displacement) # Decipher the text with the displacement obtained
    
    return plain_text, displacement

# Deciphering Vigenère algorithm with key

def vigenere_decipher(encrypted_text: str, key: str) -> str:
    """
    Returns the plain text of Vigenère knowing the key.
    """
    
    encrypted_text = tidyup_text(encrypted_text)
    key = tidyup_text(key)
    plain_text = ""
    counter = 0
    length = len(key)
    
    for character in encrypted_text: # Substract the part of the key to each character
        plain_text += dif_characters(character, key[counter % length])
        counter += 1
        
    return plain_text

# Deciphering Vigenère algorithm without knowing the key

def vigenere_decipher_no_key(encrypted_text: str) -> tuple:
    """
    Returns the plain text of Vigenère without knowing the key, through the Kasiski method. This method works many times, but not all.
    For this, more sophisticated and specific frequency analysis would have to be carried out, however it is quite accurate when
    the key to decipher does not have repeated, similar or with many vowels syllables. This function works exclusively for 
    texts in German and Spanish.
    """
    
    encrypted_text = tidyup_text(encrypted_text) # Clean the encrypted text
    key_l = key_length(encrypted_text) # Obtain the key length
    key = key_obtain(encrypted_text, key_l) # Obtain the key
    plain_text = vigenere_decipher(encrypted_text,key) # Decipher the text with the key obtained
    
    return plain_text, key