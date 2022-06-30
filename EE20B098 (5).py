'''
-------------------------------------
 SPICE-2  - EE2703 (Jan-May 2022)
 Done by PRASANNA G (EE20B098)
 Created on 09/02/22
-------------------------------------
'''

class Resistor:                                      # class definition for resistor
        def __init__(self,n1,n2,value):              # function to initialize resitor components
            self.node1=int(n1)
            self.node2=int(n2)            
            self.value=float(value)
class Inductor:                                      # class definition for inductor
        def __init__(self,n1,n2,value):              # function to initialize inductor components
            self.node1=int(n1)
            self.node2=int(n2)
            self.value=float(value)
class Capacitor:                                     # class definition for capacitor
        def __init__(self,n1,n2,value):              # function to initialize capacitor components
            self.node1=int(n1)
            self.node2=int(n2)
            self.value=float(value)
class V_source:                                      # class definition for voltage source
        phase=0
        def __init__(self,n1,n2,sig,value,phase=0):  # function to initialize voltage source components
            self.node1=int(n1)
            self.node2=int(n2)
            self.sig=sig
            self.value=float(value)
            self.phase=float(phase)
class C_source:                                      # class definition for current source
        phase=0
        def __init__(self,n1,n2,sig,value,phase=0):  # function to initialize current source components
            self.node1=int(n1)               
            self.node2=int(n2)
            self.sig=sig
            self.value=float(value) 
            self.phase=float(phase)


def analyse(ele=[]):                                 # function to declare and return class objects for respective electrical components
  
    if ele[0][0]=="R":                               # checking if list contains resistor's information
        R=Resistor(ele[1],ele[2],ele[3])             
        return R
    
    if ele[0][0]=="L":                               # checking if list contains resistor's information
        L=Inductor(ele[1],ele[2],ele[3])
        return L
    
    if ele[0][0]=="C":                               # checking if list contains resistor's information
        C=Capacitor(ele[1],ele[2],ele[3])
        return C
    
    if ele[0][0]=="V":                               # checking if list contains resistor's information
        if ele[3]=="ac":                             # checking if voltage souce is ac
          V=V_source(ele[1],ele[2],ele[3],ele[4],ele[5])
        else:                                        # dc voltage source
          V=V_source(ele[1],ele[2],ele[3],ele[4])
        return V    
    
    if ele[0][0]=="I":                               # checking if list contains resistor's information
        if ele[3]=="ac":                             # checking if current souce is ac
          I=C_source(ele[1],ele[2],ele[3],ele[4],ele[5])
        else:                                        # dc current source
          I=C_source(ele[1],ele[2],ele[3],ele[4])
        return I


from numpy import *                    # importing necessary libraries
from sys import argv,exit          

START=".circuit"                  
END=".end"
t_nodes=0;n_vsrc=0;k=0;g=0             # initialising total nodes and no. of voltage sources to 0
element_list=[];R_list=[];L_list=[];C_list=[];V_list=[];I_list=[]  # declaring total element's list and respective component's list

if len(argv)!= 2:                     # checking the format entered by the user
   print('\nFormat: %s <inputfile>' % argv[0])
   exit()
try:                                  # checking if valid file is given as input
    with open(argv[1]) as f:         
      lines = f.readlines()         #storing the file contents line by line in "lines" list

except IOError:                       # to show error if file can't be opened
      print('File cannot be opened! Please upload a valid file')
      exit()    
        
f_line= -1; l_line = -2               # initialising the f_line and l_line to store the index of start and end of the circuit definition

for line in lines:                    # loop to find the index of first line and last line of the circuit definition
    if START==line[:len(START)]:      # comparing the line with START to find the start index
           f_line = lines.index(line)
    elif END==line[:len(END)]:        # comparing the line with START to find the last index
           l_line = lines.index(line)
           break
        
         
if f_line > l_line:                   # checking if circuit definition is valid 
    print('Invalid circuit definition')
    exit(0)

for i in range(f_line+1,l_line):      # loop to split the elements of list and analyse the components 
    l=lines[i].split('#')[0].split()  # split the list elements 
    if l[1]=='GND':                   # to redefine GND node with 0
      l[1]=0
    if l[2]=='GND':
      l[2]=0
    element_list.append(analyse(l))   # calling the function analyse to form a element_list of objects of the components in circuit definition

t=len(element_list)                   # to find the no of electrical components

for i in range(t):                    # loop to seperate the electrical components and form a seperate list for seperate components    
    if type(element_list[i])==Resistor:  # checking the classtype of components in element_list 
      R_list.append(element_list[i])       # appending the list of same class type
      #to find the total no of nodes
      if t_nodes<element_list[i].node1:    
          t_nodes=element_list[i].node1
      if t_nodes<element_list[i].node2:
          t_nodes=element_list[i].node2  
          
    elif type(element_list[i])==Capacitor:  # capacitor list
      C_list.append(element_list[i])
      if t_nodes<element_list[i].node1:
          t_nodes=element_list[i].node1
      if t_nodes<element_list[i].node2:
          t_nodes=element_list[i].node2 
    
    elif type(element_list[i])==Inductor:  # inductor list
      L_list.append(element_list[i])
      if t_nodes<element_list[i].node1:
          t_nodes=element_list[i].node1
      if t_nodes<element_list[i].node2:
          t_nodes=element_list[i].node2      
            
    elif type(element_list[i])==V_source:  # voltage source list
       n_vsrc+=1                            # to find the no of voltage sources
       V_list.append(element_list[i])
       if element_list[i].sig=="ac":
          g+=1                             # to check if source is ac or dc
       if t_nodes<element_list[i].node1:
          t_nodes=element_list[i].node1
       if t_nodes<element_list[i].node2:
          t_nodes=element_list[i].node2 
          
    elif type(element_list[i])==C_source: # current source list
      I_list.append(element_list[i])
      if t_nodes<element_list[i].node1:
          t_nodes=element_list[i].node1
      if t_nodes<element_list[i].node2:
          t_nodes=element_list[i].node2
          
if g==1:        # if source is ac 
 A=zeros((t_nodes+n_vsrc,t_nodes+n_vsrc),dtype=complex)  # initialising conductance matrix with 0
 X=zeros((t_nodes+n_vsrc,1),dtype=complex)               # initialising unknown matrix with 0 
 S=zeros((t_nodes+n_vsrc,1),dtype=complex)               # initialising source matrix with 0
 w=float(lines[l_line+1].split()[2])                     # to find the frequency of ac source


 for obj in R_list:  # loop to form the stamp of Resistor and add with conductance matrix
    A[obj.node1-1][obj.node1-1]+=1/(obj.value)*sign(obj.node1)
    A[obj.node2-1][obj.node2-1]+=1/(obj.value)*sign(obj.node2)
    A[obj.node1-1][obj.node2-1]+=-1/(obj.value)*sign(obj.node1)*sign(obj.node2)
    A[obj.node2-1][obj.node1-1]+=-1/(obj.value)*sign(obj.node1)*sign(obj.node2)

 for obj in L_list: # loop to form the stamp of Inductor and add with conductance matrix
    A[obj.node1-1][obj.node1-1]+=1/complex(0,2*pi*w*obj.value)*sign(obj.node1)
    A[obj.node2-1][obj.node2-1]+=1/complex(0,2*pi*w*obj.value)*sign(obj.node2)
    A[obj.node1-1][obj.node2-1]+=-1/complex(0,2*pi*w*obj.value)*sign(obj.node1)*sign(obj.node2)
    A[obj.node2-1][obj.node1-1]+=-1/complex(0,2*pi*w*obj.value)*sign(obj.node1)*sign(obj.node2)

 for obj in C_list: # loop to form the stamp of Capacitor and add with conductance matrix
    A[obj.node1-1][obj.node1-1]+=complex(0,2*pi*w*obj.value)*sign(obj.node1)
    A[obj.node2-1][obj.node2-1]+=complex(0,2*pi*w*obj.value)*sign(obj.node2)
    A[obj.node1-1][obj.node2-1]+=-complex(0,2*pi*w*obj.value)*sign(obj.node1)*sign(obj.node2)
    A[obj.node2-1][obj.node1-1]+=-complex(0,2*pi*w*obj.value)*sign(obj.node1)*sign(obj.node2)

 for obj in V_list: # loop to form the stamp of voltage source and add with conductance matrix and source matrix
    A[obj.node1-1][t_nodes+k]+=-1*sign(obj.node1)
    A[t_nodes+k][obj.node1-1]+=-1*sign(obj.node1)
    A[t_nodes+k][obj.node2-1]+=1*sign(obj.node2)
    A[obj.node2-1][t_nodes+k]+=1*sign(obj.node2)
    S[t_nodes+k,0]+=(obj.value/2)*complex(cos(obj.phase),sin(obj.phase))
    k+=1

 for obj in I_list: # loop to form the stamp of current source and add with conductance matrix and source matrix
    S[obj.node1-1,0]+=(obj.value/2)*complex(cos(obj.phase),sin(obj.phase))*sign(obj.node1)
    S[obj.node2-1,0]+=-(obj.value/2)*complex(cos(obj.phase),sin(obj.phase))*sign(obj.node2)
 
 X=linalg.solve(A,S)  # loop to find the unknown values
 
 for Vi in range(t_nodes):
     print("The voltage at node%d is" %(Vi+1),end=' ') # to print the V at each node
     print(X[Vi][0])
 
 for Ii in range(n_vsrc):
     print("The current through voltage source%d is"%(Ii+1), end=' ') # to print the current passing through the voltage sources
     print(X[Ii+t_nodes][0])
else: # the following part of code for dc signal
 A=zeros((t_nodes+n_vsrc,t_nodes+n_vsrc),dtype=float) # initialising conductance matrix with 0
 X=zeros((t_nodes+n_vsrc,1),dtype=float)              # initialising unknown matrix with 0
 S=zeros((t_nodes+n_vsrc,1),dtype=float)              # initialising source matrix with 0

 for obj in R_list: # loop to form the stamp of Resistor and add with conductance matrix
    A[obj.node1-1][obj.node1-1]+=1/(obj.value)*sign(obj.node1)
    A[obj.node2-1][obj.node2-1]+=1/(obj.value)*sign(obj.node2)
    A[obj.node1-1][obj.node2-1]+=-1/(obj.value)*sign(obj.node1)*sign(obj.node2)
    A[obj.node2-1][obj.node1-1]+=-1/(obj.value)*sign(obj.node1)*sign(obj.node2)

 for obj in C_list: # loop to form the stamp of capacitor and add with conductance matrix
    A[obj.node1-1][obj.node1-1]+=10**300*sign(obj.node1)      # assuming a very high value for capacitance in steady state implying open loop
    A[obj.node2-1][obj.node2-1]+=10**300*sign(obj.node2)
    A[obj.node1-1][obj.node2-1]+=10**300*sign(obj.node1)*sign(obj.node2)
    A[obj.node2-1][obj.node1-1]+=10**300*sign(obj.node1)*sign(obj.node2)

 for obj in V_list: # loop to form the stamp of voltage source and add with conductance and source matrix
    A[obj.node1-1][t_nodes+k]+=-1*sign(obj.node1)
    A[t_nodes+k][obj.node1-1]+=-1*sign(obj.node1)
    A[t_nodes+k][obj.node2-1]+=1*sign(obj.node2)
    A[obj.node2-1][t_nodes+k]+=1*sign(obj.node2)
    S[t_nodes+k,0]+=obj.value
    k+=1 # to number the voltage source for indexing the element

 for obj in I_list: # loop to form the stamp of current source and add with conductance and source matrix
    S[obj.node1-1,0]+=obj.value*sign(obj.node1)
    S[obj.node2-1,0]+=-obj.value*sign(obj.node2)
 
 X=linalg.solve(A,S)
 
 for Vi in range(t_nodes):
     print("The voltage at node%d is" %(Vi+1),end=' ') # to print the V at each node
     print(X[Vi][0])
 
 for Ii in range(n_vsrc):
     print("The current through voltage source%d is"%(Ii+1+t_nodes), end=' ') # to print the current passing through the voltage sources+
     print(X[Ii+t_nodes][0])


