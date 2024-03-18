#!/usr/bin/python3
import sys
import os
import numpy as np
sys.path.append('/home/humbel/bin')
import RRoutines


class Orb:
    def __init__(self, zeta: int=0, orb_num: list[int]=None, nao_count: list[int]=None, coeffs: list[float]=None, indices: list[int]=None, numatoms: list[int]=None):
        self.zeta = zeta
        self.orb_num = orb_num if orb_num is not None else []
        self.nao_count = nao_count if nao_count is not None else []
        self.coeffs = coeffs if coeffs is not None else []
        self.indices = indices if indices is not None else []
        self.numatoms = numatoms if numatoms is not None else []

    @staticmethod
    def display_indices(orbs: list['Orb'], iom:int):
        for orb in orbs:
            if orb.orb_num[iom] == iom:
                print(f'for {orb_num}: {orb.indices}8.6E')


#
#   def __init__(self, zeta, orb_num, nao_count, coeffs, indices, numatoms):
class Orbitale: 
    def __init__(self, zeta: int=0, orb_num:int=0 , nao_count: int=0 , coeffs: list[float]=[], indices: list[int]=[], numatoms: list[int]=[]:
        self.zeta = zeta
        self.orb_num = orb_num
        self.nao_count = nao_count
        self.coeffs = coeffs 
        self.indices = indices
        self.numatoms = numatoms
#        
def readorb(file_name,orbitales, linenumber):
    coef=[]
    ao=[]
    iom=0
    with open(file_name, 'r') as file:
      noa = []
      for  line in file:
          values = []
          if ("#" in line):
             if iom > 0:
                 orbitales.orb_num= iom
                 orbitales.coeffs.append(coef)
                 orbitales.indices.append(ao)
                 orbitales.nao_count=len(orbitales.coeffs)
                 print(iom,'zz',len(orbitales.coeffs),orbitales.nao_count,orbitales.coeffs)
                 iom+=1
                 coef=[]
                 ao=[]
             else:
                 iom+=1

          if not("#" in line):
             values=line.split()
             if iom==0:
                 noa.append(values) 
             else:
                 #print("||",values[0], len(values))
                 toread=len(values)//2
                 for i in range(toread):
                 #   print(i,end='')
                    coef.append(float(values[2*i]))  # add the last to vectors
                    ao.append(float(values[2*i+1]))

      # last orb must be updated

      orbitales.coeffs.append(coef)
      orbitales.indices.append(ao)
      orbitales.nao_count=len(orbitales.coeffs)
      print('rr',len(orbitales.coeffs))
      # store nao_count in each
      for sous_liste in noa:
         for nombre in sous_liste:
             orbitales.nao_count = int(nombre)
      print("Valeur de nao_count dans l'objet orbitales :", orbitales.nao_count)
    return orbitales

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




print(" start getorb ",end='')
orbitales = Orbitales()
file_name, start_index, ordre = RRoutines.read_arguments(*sys.argv[1:])
file_name = sys.argv[1]
print("File name:", file_name)
print(f'Start index:{"{:3d}".format(start_index)}')
#print("Order:", ordre)

file_court, file_ext = RRoutines.get_file_extension(file_name)
output_file=file_court+'_new'+file_ext

linenumber=1
orbitales = readorb(file_name,orbitales, linenumber)
#print('-- read done for ',len(orbitales.orb_num),'orbitales --')
orb_spec=Orb[]
print("indices: pour orb_num=",{start_index}, orb_spec.indices[int(start_index-1)])
print("Coefficients: pour orb_num=",{start_index}, orb_spec.coeffs[int(start_index-1)])
print("noa_count: pour orb_num=",{start_index}, orb_spec.nao_count)
print("------------------------")
Orb.display_indices(orbitales, int(start_index))
#print("Coefficients:", orbitales.coeffs)
new_orbitales=orbitales
#write_orb_file(output_file, new_orbitales)

sys.exit()
RRoutines.print_vec(vectors,1,len(reordered_vectors))
output=file_court+"_r"+file_ext
print('ecriture des VEC sur fichier',output)
RRoutines.write_vec(reordered_vectors, 1, len(reordered_vectors), output)

sys.exit()

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


