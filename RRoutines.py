import sys
import os
import copy
import numpy as np
#--FB
import re
#import matplotlib.pyplot as plt
#  FB--
#SH routine

def compte_AO(vect):
    '''
    Description : compte et retourne la liste des AO non nuls dans un vecteur MO
    Args:
        parameter (vect): le vecteur MO (array de NAO)
        parameter (nao): nombre de AO non nuls dans le vecteur
        parameter (tab_ao): liste des AO NAO

    Returns:
        nao, tab_ao
    '''
    # Initialisation du compteur de AO non nuls et de la liste des AO
    nao = 0
    tab_ao = []

    # Parcours du vecteur MO
    for i in range(len(vect)):
        # Si le coefficient du AO est non nul
        if vect[i] != 0.:
            # Ajouter l'indice du AO à la liste des AO non nuls
            tab_ao.append(i)
            # Incrémenter le compteur de AO non nuls
            nao += 1
    
    # Retourner le nombre total de AO non nuls et la liste des AO non nuls
    return nao, tab_ao

def writorb(vectors,outfile):
    '''
    Description : write MO's as .orb to a file.
    Args:
        parameter (vectors): the MO's vectors(i,array(of coef for each AO's))
        parameter (outfile): path to the output file

    Returns:
        None

    Uses: compte_AO
    '''
    nao=0
    tab_ao=[]
    with open(outfile, 'w') as output_file:
    # first line : the nao_count
         with vect in vectors:
              nao,tab_ao=compte_AO(vect)
              output_file.write(f"{nao:4d}")

# FBarrois routines
def write_orb_file(filename, new_orb_data):
    orb_num = new_orb_data.orb_num
    new_zeta = new_orb_data.zeta
    new_orb_count = new_orb_data.nao_count
    new_orb_values = new_orb_data.coeffs
    new_indices = new_orb_data.indices
    count = 0
    sommecount = 0
    first_line = " ".join(str(num) for num in new_orb_count)
    print (first_line)
    with open(filename, 'w') as f:
        f.write(first_line + "\n")
        for i in range(len(orb_num)):
            #print (f"count {count}")

            sommecount += count
            count = 0

            f.write(f"# ORBITAL          {orb_num[i]}  NAO =      {new_orb_count[i]}\n")
            while count < new_orb_count[i]:
                #print (new_orb_count[i])
                #print (f"count {count}")
                j = sommecount + count
                #print (f"j {j}")
                #print (f"coeff {new_orb_values[j]}")
                #print (f"indices {new_indices[j]}")
                f.write(f"   {new_orb_values[j]}   {str(new_indices[j])}   ")
                if (j + 1) % new_zeta == 0:  # Check if current iteration is a multiple of new_zeta
                    f.write("\n")
                count += 1
                if count == new_orb_count[i]:
                    bloub = []
                    num = count
                    while num != 0:
                        bloub.append(new_indices[j+1-num])
                        num -= 1
                    for item in bloub:
                        print(item, end=' ')
                    print()


# FBarrois routines
def readorb(file_name,vectors, linenumber):
    vectors=[]
    i=0
    print('--->>>')
    with open(file_name, 'r') as file:
      values = []
      for  line in file:
          i+=1
          if i==3 :
              print(line)
             
        


    return vectors
def read_orb_xm(file_path, zeta):
    zeta = int (zeta)
    with open(file_path) as f:
        # read the orbital data
        data = f.readlines()
    om_data = []
    coeffs = []
    indices = []
    numatoms = []
    orb_num = []
    nao_count = []
    for line in data:
        first_line = line.split()
        line = line.strip()
        if all(number.isdigit() for number in first_line):
            # parse the orbital header line
            #print (first_line)
            for i in range(0, len(first_line), 1):
                nao_count.append(int(first_line[i]))
                #print (nao_count)
        if line.startswith('#'):
            break
        else:
            values = line.split()
            om_data.extend(map(float, values))
            #print (om_data)
    om_data = om_data[len(nao_count):]
    for i in range (0, len(om_data), 2):
        coeffs.append(om_data[i])
        indices.append(int(om_data[i+1]))
    #print (indices)
    #print (coeffs)

    #for p in range(1, 5, 1):
    #    if nao_count[0] // p == 6:
    #        zeta = p

    for i in range (0, len(indices), zeta):
        numatom = indices[i+zeta-1] // zeta
        numatoms.append(numatom)
    #print (numatoms)
    #print(zeta)

    #print (nao_count)
    #print (orb_num)
    return zeta, orb_num, nao_count, coeffs, indices, numatoms



def read_arguments(file_name, start_index, *order):
    start_index = int(start_index)
#    order = [int(arg) for arg in order]  # Convertit les arguments suivants en entiers
    order = [int(arg) for arg in ''.join(order).replace(',', ' ').split()]
    return file_name, start_index, order

#function to get fname.extension from file_name                         
def get_file_extension(file_name):
    fname, extension = os.path.splitext(file_name)
    return fname, extension


def detect_keyword(file_path, keyword, start_line):
    '''
    Description : get the line number of the *last* occurence of keyword in file_path.
    Args:
        parameter (file_path): name of the file (possibly the path?).
        parameter (keyword): string to find
        parameter (start_line): the line the search starts from

    Returns:
        type: returns the line number (lin_num) of the *last* occurence of keyword or -1 if keyword is not found
    '''
    with open(file_path, 'r') as file:
        for line_num, line in enumerate(file, 1):  
            if line_num >= start_line and keyword in line:
                return line_num
    return -1  # not found

def reorder_vectors(vectors, start_index, order):
    '''
    Description : take MO's and reorder them from start index following the order table).
    Args:
        parameter (vectors): the MO's vectors(i,array(NAO's))
        parameter (start_index): beginning of the reordering (from 1)
        parameter (order): the list of the reoganized orbitals eg order = [4,3,2] with start_index=2
                        will take orbitals 1,2,3,4 and order them as 1,4,3,2 

    Returns:
        type: returns the reordered MO's as ordered_vectors, where ordered_vectors[i][1] is correct
    '''
    # start by starting from zero
    start_index=start_index-1
    for i in range (0,len(order)):
        order[i] = order[i]-1
    print('Enter reordr: ', start_index, order)
    if start_index + len(order)-1 > len(vectors):
        print("Invalid start index and order length.",start_index + len(order)-1,'>',len(vectors))
        return None
    if start_index < 0 or start_index > len(vectors):
        print("Invalid start index.")
        return None

    # Create a new array to store the reordered vectors
    ordered_vectors = copy.deepcopy(vectors)
    print(order)
    # Reorder the vectors
    for i, idx in enumerate(order):
        ordered_vectors[start_index + i] = vectors[idx]
        print(start_index+i,idx,', ',end='')
    # correct the MO's numbers
    for i in range(len(ordered_vectors)):
        new_tuple = [i+1] + list(ordered_vectors[i][1:])
        ordered_vectors[i] = tuple(new_tuple)
    return ordered_vectors

# PRINT_VEC
def write_vec(vectors, deb, fin, file_path):
    '''
    Description : write MO's as $VEC to a file.
    Args:
        parameter (vectors): the MO's vectors(i,array(NAO's))
        parameter (deb, fin): beginning and end of the printing
        parameter (file_path): path to the output file

    Returns:
        None
    '''
    if deb < 1 or fin > len(vectors) + 1:
        print('Error: Invalid limits in write_vec', deb, fin, len(vectors))
        sys.exit(1)

    with open(file_path, 'w') as output_file:
        output_file.write(' $VEC')
        for vector_number, values in enumerate(vectors):
            line_number = 1
            indice = vectors[vector_number][0]
            if deb <= indice <= fin:
                for i in range(0, len(values[1])):
                    if i % 5 == 0:
                        output_file.write('\n')
                        output_file.write(f"{indice % 100:2d}{line_number:3d}")
                        line_number += 1
                    output_file.write(f"{values[1][i]:15.8E}")

        output_file.write('\n $END')
        output_file.write('\n')


def print_vec(vectors,deb,fin):
    '''
    Description : print MO's as $VEC  to the screen).
    Args:
        parameter (vectors): the MO's vectors(i,array(NAO's))
        parameter (deb, fin): beginning and end of the printing
    
    Returns:
        type: returns the reordered MO's as ordered_vectors, where ordered_vectors[i][1] is correct
    '''
# deb, fin start at 1  (as stored in vector[i][0])
#   print(' routines.print_vec ',deb,fin, len(vectors))
    if deb < 1 or fin > len(vectors)+1:
        print(' Error limits in routines.print_vec ',deb,fin, len(vectors))
        sys.exit(1)
    print('$VEC',end='')
    for vector_number, values in enumerate(vectors):
      line_number = 1  
      indice=vectors[vector_number][0]
      if deb <= indice  <= fin:
        for i in range(0,len(values[1])):
            if i%5==0:
                 print('')
                 print(f"{indice%100:2d}{line_number:3d}", end="")
                 line_number += 1  

            print(f"{values[1][i]:15.8E}",end='')
    print()
    print("$END")

# READ_VEC
def read_vec(file_path,vectors,start_line):
    '''
    Description : reads MO's from either a .inp or a .dat file).
    Args:
        parameter (file_path): name of the file (possibly the path?).
        parameter (vectors): the MO's as two tuples:vectors[i][0]=N, vectors[i][1]=Coef np.array
        parameter (start_line): the line the reading starts from: must be the line after $VEC

    Returns:
        type: returns the  MO's as vectors, (until $END is reached)
    '''
    def read15(line,values):
        values=[]
        toread = (len(line) - 1 - 5) // 15 # skip 5 (+1) digits and get n (number of float nF15.8)
        for i in range(toread):            # so partially filled lines are read
            start_index = 5 + i * 15       # skip 5 digits and the already read floats
            end_index = start_index + 15   # field as nF15.8
            values.append(float(line[start_index:end_index]))

    prev_vector_number=1
    item=1        
    with open(file_path, 'r') as file:
        values = []
        for line_num, line in enumerate(file, start=1):
            if line_num < start_line:
                continue  # skip the first lines 

            if line.strip() == '$END':
                vectors.append((item, np.array(values)))  # add the last to vectors
#                print('>last',item,line[0:2],len(values),values[0:12])
                break  # stop reading after $END

            # get from format (I2,I3,5F15.8)
            vector_number = int(line[0:2])
#            print('values',vector_number,')',prev_vector_number,values)
            if vector_number == prev_vector_number:
               toread = (len(line) - 1 - 5) // 15 # skip 5 (+1) digits and get n (number of float nF15.8)
               for i in range(toread):            # so partially filled lines are read
                   start_index = 5 + i * 15       # skip 5 digits and the already read floats
                   end_index = start_index + 15   # field as nF15.8
                   values.append(float(line[start_index:end_index]))
#              print('######',vector_number,'stored',values ))')
            else:
               vectors.append((item, np.array(values)))  # add to vectors
               item=item+1
               prev_vector_number=vector_number
               values=[]
               toread = (len(line) - 1 - 5) // 15 # skip 5 (+1) digits and get n (number of float nF15.8)
               for i in range(toread):            # so partially filled lines are read
                   start_index = 5 + i * 15       # skip 5 digits and the already read floats
                   end_index = start_index + 15   # field as nF15.8
                   values.append(float(line[start_index:end_index]))
    return vectors

