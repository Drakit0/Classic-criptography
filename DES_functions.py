# Binary transformations


#Transform the text to binary

def text_to_bin(text:str) -> list:
    """
    Takes each character from the input text and transforms it into binary, including
    special characters, uppercase letters, numbers...
    """
    
    bin_text = ""
    for character in text: 
        try:
            number = int(character)
            bin_text += format(number, "b")
            
        except ValueError:
            bin_text += format(ord(character), "08b")
            
    bin_text_blocks = []
    block = ""
    
    for bin in bin_text: # 64 bits blocks
        block += bin
        if len(block) == 64:
            bin_text_blocks.append(block)
            block = ""
            
    if block != "": # Complete the last block if necessary
        complete = 64 - len(block)
        for i in range(complete):
            block += "0"
        bin_text_blocks.append(block)
        
    return bin_text_blocks

# Transform the binary to text

def bin_to_text(bin_text:str) -> str:
    """
    Takes the binary text and transforms it into normal text.
    """
    
    text = ""
    
    for i in range(0, len(bin_text), 8):
        text += chr(int(bin_text[i:i+8], 2))
        
    return text

# Transform the key to binary

def key_to_bin(key:str) -> str:
    """
    Transform the key to binary, if the key is not 64 bits long, the user will be asked to introduce a new key.
    """
    
    key = text_to_bin(key)
    wrong_key = True
    
    if len(key) == 1 and len(key[0]) == 64: # Verify the key length is 64 for DES
        wrong_key = False 
        
    while wrong_key:
        new_key = input("La clave no es adecuada, por favor introduzca una clave correcta de 64 bits: ")
        key = text_to_bin(new_key)
        
        if len(key) == 1 and len(key[0]) == 64:
            wrong_key = False
            
    return key[0]
        
# Left displacement of the key

def l_displacement(prev_key:str, disp:int) -> str:
    """
    Taking in account the displacement, the key will be displaced one or two positions to the left.
    """
    
    if disp == 1: # One displacement
        new_key = (prev_key + prev_key[0])[1:]
        
    if disp == 2: # Two displacements
        new_key = ((prev_key + prev_key[0]) + prev_key[1])[2:]
        
    return new_key

# Obtain all the keys for the Feistel cipher

def all_keys (key:str) -> list:
    """
    Given a key, it is transformed to binary and multiple operations and permutations 
    are applied to obtain the 16 keys used by DES.
    """
    
    key = key_to_bin(key)
    permuted_key = permute(key, perm_parity, 56) # Eliminate the 8 parity bits
    l_key = permuted_key[:28] # Split the key in two
    r_key = permuted_key[28:]
    
    l_keys = []
    
    for iteration in range(1,17):
        if iteration == 1 or iteration == 2 or iteration == 9 or iteration == 16: # One displacement
            disp = 1   
            
            if iteration == 1:
                perm_l_key = l_displacement(l_key,disp)
                
            else:
                perm_l_key = l_displacement(l_keys[iteration-2], disp)
                
        else: # Two displacements
            disp = 2
            perm_l_key=l_displacement(l_keys[iteration-2], disp)
            
        l_keys.append(perm_l_key)
           
    r_keys = []
    
    for iteration in range(1,17):
        if iteration == 1 or iteration == 2 or iteration == 9 or iteration == 16: # One displacement
            disp = 1   
            if iteration == 1:
                perm_r_key = l_displacement(r_key,disp)
                
            else:
                perm_r_key = l_displacement(r_keys[iteration-2], disp)
                
        else: # Two displacements
            disp = 2
            perm_r_key=l_displacement(r_keys[iteration-2], disp)
            
        r_keys.append(perm_r_key)
        
    merged_keys = []
    
    for key in range(16):
        merged_keys.append(l_keys[key] + r_keys[key]) # Merge the keys
        
    final_keys = []
    
    for key in range(16):
        final_keys.append(permute(merged_keys[key], perm_keys, 48)) # Permute the keys to 48 bits for the Feistel cipher
        
    return final_keys

# Feistel cipher

def f_cipher(r_block:str,key:str ) -> str:
    """
    First the right semi block is expanded to 48 bits, then an XOR operation is performed with the key and the expanded semi block,
    it is introduced in a substitution box (S-boxes) and finally, the result is reduced to a 32 bits semi block, which will be the left semi block.
    """
    
    expand_r_block = permute(r_block, perm_r_block, 48) # Expand the right block to 48 bits
    xor = ""
    
    for i in range(len(expand_r_block)): # XOR operation between the expanded block and the key
        if expand_r_block[i] == key[i]:
            xor += "0"
            
        else:
            xor += "1"
            
    xor_list = []
    
    for i in range(len(xor)): # Split the XOR result in 6 bits blocks
        if (i % 6) == 0:
            xor_list.append(xor[i:(i+6)])
    
    s_box_res = ""
    
    for i in range(len(xor_list)):
        row = int(str(xor_list[i][0]) + str(xor_list[i][5]),2) # Row of the S-box to use (the first and last bits of the 6 bits block)
        column = ""
        
        for j in range(1,5): # Column of the S-box to use (the 4 bits in the middle of the 6 bits block)
            column += str(xor_list[i][j])
            
            while len(column)<4:
                column = "0" + column
                
        column = int(column, 2)
        row_column = bin(s_boxes[i][row][column])[2:] # Get the value of the S-box
        
        while len(row_column)<4: # Ensure the value has 4 bits
                row_column = "0" + row_column
                
        s_box_res += row_column # Add the value to the result of the feistel cipher of the right expanded block
        
    return permute(s_box_res, perm_s_boxes, 32) # Reduce the result to 32 bits with the permutation of the S-boxes
         
        
# Permutations


def permute(text_to_perm:str, perm_list: list, pos_to_perm:int) -> str:
    """
    Returns the introduced str permuted according to the introduced matrix,
    wich means n bits of the text are reordered according to the matrix
    and they are returned in a new text.
    """
    
    perm_text = ""
    
    for i in range(pos_to_perm):
        perm_text += text_to_perm[perm_list[i] - 1] 
        
    return perm_text

# Initial permutation 

ini_perm = [58, 50, 42, 34, 26, 18, 10, 2,
            60, 52, 44, 36, 28, 20, 12, 4,
            62, 54, 46, 38, 30, 22, 14, 6,
            64, 56, 48, 40, 32, 24, 16, 8,
            57, 49, 41, 33, 25, 17, 9,  1,
            59, 51, 43, 35, 27, 19, 11, 3,
            61, 53, 45, 37, 29, 21, 13, 5,
            63, 55, 47, 39, 31, 23, 15, 7]

# Permutation of the key to eliminate the 8 parity bits (8, 16, 24, 32, 40, 48, 56, 64)

perm_parity = [57, 49, 41, 33, 25, 17, 9,
               1,  58, 50, 42, 34, 26, 18,
               10, 2,  59, 51, 43, 35, 27,
               19, 11, 3,  60, 52, 44, 36,
               63, 55, 47, 39, 31, 23, 15,
               7,  62, 54, 46, 38, 30, 22,
               14, 6,  61, 53, 45, 37, 29,
               21, 13, 5,  28, 20, 12, 4]

# Permutation after keys union to 48 bits

perm_keys = [14, 17, 11, 24, 1,  5,  
             3,  28, 15, 6,  21, 10,
             23, 19, 12, 4,  26, 8, 
             16, 7,  27, 20, 13, 2, 
             41, 52, 31, 37, 47, 55,
             30, 40, 51, 45, 33, 48,
             44, 49, 39, 56, 34, 53, 
             46, 42, 50, 36, 29, 32]

# Permutation of expansion of the 32 bits block to 48 bits

perm_r_block = [32, 1,  2,  3,  4,  5,
                4,  5,  6,  7,  8,  9,
                8,  9,  10, 11, 12, 13,
                12, 13, 14, 15, 16, 17,
                16, 17, 18, 19, 20, 21, 
                20, 21, 22, 23, 24, 25, 
                24, 25, 26, 27, 28, 29, 
                28, 29, 30, 31, 32 ,31]

# Permutation of the compresion of the substitution box result to 32 bits

perm_s_boxes = [16, 7, 20, 21,
	            29, 12, 28, 17,
	            1, 15, 23, 26,
	            5, 18, 31, 10,
	            2, 8, 24, 14,
	            32, 27, 3, 9,
	            19, 13, 30, 6,
	            22, 11, 4, 25]

# Final permutation of the subtexts to obtain the encrypted text

final_perm = [40, 8, 48, 16, 56, 24, 64, 32,
			  39, 7, 47, 15, 55, 23, 63, 31,
			  38, 6, 46, 14, 54, 22, 62, 30,
			  37, 5, 45, 13, 53, 21, 61, 29,
			  36, 4, 44, 12, 52, 20, 60, 28,
			  35, 3, 43, 11, 51, 19, 59, 27,
			  34, 2, 42, 10, 50, 18, 58, 26,
			  33, 1, 41, 9, 49, 17, 57, 25]


# Susbstitution boxes


s_boxes =[[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
		   [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
		   [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
		   [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],

           [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
	        [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
		    [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
		    [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],

           [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
		    [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
		    [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
		    [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],

           [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
		    [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
		    [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
		    [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],

           [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
		    [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
		    [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
		    [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],

           [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
		    [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
		    [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
		    [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],

           [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
		    [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
		    [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
		    [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],

           [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
		    [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
		    [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
		    [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]]


# DES


# Encryption

def des_cipher (text:str, key:str) -> str:
    """
    Returns the encrypted text with DES in binary.
    """
    
    text = text_to_bin(text) # Transform the text to binary
    key = key_to_bin(key) # Transform the key to binary
    keys = all_keys(key) # Obtain all the keys for the Feistel cipher
    
    semi_blocks = []
    
    for i in range(len(text)): # Split 64 bits blocks in two 32 bits blocks
        l_block = (permute(text[i], ini_perm, 64))[:32]
        r_block = (permute(text[i], ini_perm, 64))[32:]
        semi_blocks.append((l_block, r_block))
        
    for i in range(len(semi_blocks)): # Apply to all the pairs semiblocks of the text
        text_blocks = []
        
        for j in range(len(keys)): 
            if j == 0: # First iteration
                l_block = semi_blocks[i][1] # The next left semi block is the actual right semi block 
                r_block = "" 
                
                for k in range(len(semi_blocks[i][0])):
                    if semi_blocks[i][0][k] == f_cipher(semi_blocks[i][1], keys[j])[k]: # XOR operation between the left semi block and the Feistel cipher of the right semi block with the key for the round
                        r_block += "0"
                        
                    else:
                        r_block += "1"
                        
            else: # The rest of the iterations (same as before but the initial right semi block is the last right semi block)
                l_block = text_blocks[j-1][1]
                r_block = ""
                
                for k in range(len(semi_blocks[i][0])):
                    if text_blocks[j-1][0][k] == f_cipher(text_blocks[j-1][1], keys[j])[k]:
                        r_block += "0"
                        
                    else:
                        r_block += "1"
                        
            text_blocks.append((l_block, r_block)) # Save the left and right semi blocks for the next iteration
            
        text_combination = text_blocks[15][1] + text_blocks[15][0] # Combine the last left and right semi blocks
        final_text = permute(text_combination, final_perm, 64) # Permute the final text
        
    return final_text


# Decryption
    
def des_decipher (text:str, key:str) -> str:
    """
    Returns the decrypted text with DES in binary.
    """
    
    bin_text_blocks = []
    block = ""
    
    for bin in text: # Split the text in 64 bits blocks
        block += bin
        
        if len(block) == 64:
            bin_text_blocks.append(block)
            block = ""
            
    if block != "": # Complete the last block if necessary
        complete = 64 - len(block)
        
        for i in range(complete):
            block += "0"
            
        bin_text_blocks.append(block)
        
    key = key_to_bin(key) # Transform the key to binary
    keys = all_keys(key) # Obtain all the keys for the Feistel cipher
    
    semi_blocks = []
    
    for i in range(len(bin_text_blocks)): # Split 64 bits blocks in two 32 bits semi blocks
        l_block = (permute(bin_text_blocks[i], ini_perm, 64))[:32]
        r_block = (permute(bin_text_blocks[i], ini_perm, 64))[32:]
        semi_blocks.append((l_block, r_block))
        
    for i in range(len(semi_blocks)): # Apply to all the pairs of semiblocks of the text
        text_blocks = []
        
        for j in range(len(keys)): 
            l = 15-j # The keys are used in reverse order
            
            if j == 0: # First iteration
                l_block = semi_blocks[i][1] # The next left semi block is the actual right semi block
                r_block = ""
                
                for k in range(len(semi_blocks[i][0])):
                    if semi_blocks[i][0][k] == f_cipher(semi_blocks[i][1], keys[l])[k]: # XOR operation between the left semi block and the Feistel cipher of the right semi block with the key for the round
                        r_block += "0"
                        
                    else:
                        r_block += "1"
                        
            else: # The rest of the iterations (same as before but the initial right semi block is the last right semi block)
                l_block = text_blocks[j-1][1]
                r_block = ""
                
                for k in range(len(semi_blocks[i][0])):
                    if text_blocks[j-1][0][k] == f_cipher(text_blocks[j-1][1], keys[l])[k]:
                        r_block += "0"
                        
                    else:
                        r_block += "1"
                        
            text_blocks.append((l_block, r_block)) # Save the left and right semi blocks for the next iteration
            
        text_combination = text_blocks[15][1] + text_blocks[15][0] # Combine the last left and right semi blocks
        final_text = permute(text_combination, final_perm, 64) # Permute the final text
        
    return bin_to_text(final_text) # Transform the binary text to normal text