import pandas as pd
import os
import sys
import pyfim
from fim import fpgrowth

def concat_files(init, end):
    name = 'res'
    extension = '.out'
    filenames = []

    for i in range(init, end):
        filenames.append(name + str(i) + extension)

    with open('./results/out.txt', 'w') as outfile:
        for fname in filenames:
            with open(fname) as infile:
                for line in infile:
                    outfile.write(line)
            
                outfile.write('\n') 
                outfile.write('\n')

    for i in range(init, end):
        os.remove(name + str(i) + extension)
    return             

def id_to_name_pyfim():
    products = pd.read_csv("./data/products.csv")
        
    #abrindo um novo arquivo com os nomes dos produtos ao inves dos ids
    with open ('./results/results.txt', 'w') as outfile:
        #abrindo o resultado das associacoes
        with open('./results/out.txt', 'r') as infile:
            #percorre todas as linhas do arquivo de associacoes 
            for line in infile:
                
                if line != '\n':
                    #remove parenteses e virgula            
                    line = line.replace("(", "")
                    line = line.replace(")", "")
                    line = line.replace(",", "")
                    
                    #cria uma lista contendo cada string
                    temp_list = line.split(' ')
                    #pega o item consquente
                    left_int = int(temp_list[0])
                    left_items = (products.loc[products['product_id'] == left_int]['product_name'].values[0])
                    
                    #pegando em separado a confianca
                    conf = float(temp_list[len(temp_list) - 1])
                    supp = float(temp_list[len(temp_list) - 2])
                    #removendo a confianca (valor float) e o item consequente
                    temp_list = temp_list[1:len(temp_list) - 2]
                    #pegando os inteiros referentes aos itens antecedentes
                    right_int = [int(s) for s in temp_list]
                    
                    #transforma os ids em nome de produto
                    right_items = []
                    for val in right_int:
                        right_items.append(products.loc[products['product_id'] == val]['product_name'].values[0])
                
                    #escrevendo no arquivo
                    outfile.write(str(left_items) + ' <- ' + str(right_items) + ' ' + str(supp) + ' ' +str(conf) + '\n\n')
            
    return       

#ler suporte e confianca minimos
min_sup = float(sys.argv[1])
min_conf = float(sys.argv[2]) 

#Lendo o arquivo csv
data_frame = pd.read_csv ("./data/newTrainSet.csv")

#Pegar todos os ids unicos dos pedidos
array = data_frame.order_id.unique()

#Fazer uma lista com todos os pedidos
data_list = []
for p in data_frame.order_id.unique():
    data_list.append((data_frame[data_frame['order_id'] == p].product_id).tolist())

#Executar algoritmo FP Growth
result = fpgrowth(data_list, supp=min_sup, conf=min_conf, target='r', report='XC')

#Escrever os resultados em um arquivo
i = 0
for p in result:
    filename = "res"
    filename = filename + str(i) + ".out"
    i = i + 1
    f = open(filename, 'w' )
    f.write(repr(p))
    f.close()

concat_files (0, i)
id_to_name_pyfim()
