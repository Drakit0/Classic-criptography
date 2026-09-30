# Classic-criptography

A command-line program in Python that encrypts and decrypts text with the Caesar, Vigenère and DES ciphers, and breaks Caesar and Vigenère without the key.

## What it does

- Caesar: encrypt and decrypt with a given shift, or decrypt without the shift.
- Vigenère: encrypt and decrypt with a given key, or decrypt without the key.
- DES: encrypt and decrypt with a key typed as plain text.
- Any result can be saved to `worked_files/` as a `.txt` or `.json` file.

The menus and messages are in Spanish.

## How it works

- Text is normalised first: lower case, accents and ñ removed, anything that is not a letter dropped (`tidyup_text`).
- Caesar without the shift: the letter frequencies of the ciphertext are compared with those of the reference texts in `files/` (English, German and Spanish books) for each possible shift.
- Vigenère without the key: the key length is estimated with the Kasiski method (repeated trigraphs), then each key letter is found with a frequency comparison. `match_index` computes the index of coincidence.
- DES is written from scratch in `DES_functions.py`: initial permutation, 16-round Feistel network with subkey generation, the f function and the final permutation. Keys shorter than 64 bits are padded with zeros.

Frequency analysis needs long texts. The program itself warns that results may not be coherent below about 3000 words.

## How to run

Python 3, standard library only.

```
python Main.py
```

Run it from the repository root, since it reads `files/` and writes to `worked_files/` with relative paths.

Tests cover the Caesar and Vigenère helpers:

```
python test.py
```

## Structure

- `Main.py`: menu loop.
- `Cesar_Vigenere_functions.py`: Caesar and Vigenère, encryption and breaking.
- `DES_functions.py`: DES.
- `General_functions.py`: menus, input handling, file saving.
- `Exceptions.py`: standalone DES script with a hexadecimal example, not imported by the program.
- `files/`: reference texts used for frequency analysis.
- `test.py`: unit tests.

## Author

Pablo Tuñón Laguna, 2024. MIT licence.
