#!/usr/bin/python3
import sys
import os
import numpy as np
sys.path.append('/home/humbel/bin')
import RRoutines
#        
print(" start reord ",end='')
file_name, start_index, ordre = RRoutines.read_arguments(*sys.argv[1:])
file_name = sys.argv[1]
print("File name:", file_name)
print("Start index:", start_index)
print("Order:", ordre)

file_court, file_ext = RRoutines.get_file_extension(file_name)

keyword="$VEC"
print("for    ....: ", file_name,keyword)
#detect the last $VEC
line_number = 0
while line_number != -1:
    linenumber = line_number + 1
    line_number = RRoutines.detect_keyword(file_name, keyword, linenumber)
#    print('line',line_number)
#print('outline',linenumber)
vectors=[]
vectors = RRoutines.read_vec(file_name,vectors, linenumber)
print('-- read done for ',len(vectors),'vectors --')
# now reord
reordered_vectors=[]
print('ordre =',ordre ,' from ', start_index)
reordered_vectors=RRoutines.reorder_vectors(vectors,start_index, ordre)
RRoutines.print_vec(reordered_vectors,1,len(reordered_vectors))
output=file_court+"_r"+file_ext
print('ecriture des VEC sur ',output)
RRoutines.write_vec(reordered_vectors, 1, len(reordered_vectors), output)


#envoi dans une liste
print('------<>listification<>---------')
list_vect = [[] for _ in range(len(vectors[0]))]
for i in range(len(vectors[0])):
    list_vect[i] = [vectors[1][j][i] for j in range(1, len(vectors[1]))]

print('------<><><>---------')
print(list_vect)
RRoutines.writorb(vectors,file_court+".orb")
sys.exit()






ordre = [1,2]
vectors=RRoutines.reorder_vectors(vectors,1, ordre)
print(' ordered done --')
print(' reprint initial done --')
RRoutines.print_vec(vectors,1,len(vectors))
RRoutines.write_orb_file(file_court+".orb",vectors)
#print('v1apres',vectors[1])
RRoutines.print_vec(vectors,101,111)
#print('v1apres',vectors[100])


