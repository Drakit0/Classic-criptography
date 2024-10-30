#Importación de las librerías

import unittest

# Importar las funciones a probar

from Cesar_Vigenere_functions import tidyup_text, sum_characters, cesar_cipher, vigenere_cipher, character_count, dif_characters

class TestCifrado(unittest.TestCase):
    
    #Try to didy up the text
    
    def test_tidyup_text(self):
        text = "HELLO, world_!"
        expected_output = "helloworld"
        self.assertEqual(tidyup_text(text), expected_output)

    #Try to add up character positions

    def test_sum_characters(self):
        c1 = "a"
        c2 = "b"
        expected_output = "b"
        self.assertEqual(sum_characters(c1, c2), expected_output)

    #Try to cipher with César

    def test_cesar_cipher(self):
        text = "hello"
        displacement = 3
        expected_output = "khoor"
        self.assertEqual(cesar_cipher(text, displacement), expected_output)

    #Try to cipher with Vigènere

    def test_vigenere_cipher(self):
        text = "Project finished"
        key = "engineering"
        expected_output = "teurrgxwqaowukl"
        self.assertEqual(vigenere_cipher(text, key), expected_output)

    def test_character_count(self):
        # Probar que la función de cálculo de frecuencias funciona correctamente
        text = "hell"
        expected_output = {"h": 0.25, "e": 0.25, "l": 0.5}
        self.assertEqual(character_count(text), expected_output)

    def test_dif_characters(self):
        # Probar que la función de resta de posiciones funciona correctamente
        c1 = "a"
        c2 = "b"
        expected_output = "z"
        self.assertEqual(dif_characters(c1, c2), expected_output)

if __name__ == "__main__":
    unittest.main()
