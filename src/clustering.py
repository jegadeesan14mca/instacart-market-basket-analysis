# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm
from matplotlib.patches import Circle
from sklearn.cluster import KMeans
from math import isnan
import numpy as np
from utils import *

def plotDistPedidosPorCliente(clients):
    x = []
    for client in clients:
        x.append(client.norders)
    un, cnt = np.unique(x, return_counts=True)
    cnt = [x/len(clients) for x in cnt]
    plt.plot(un, cnt, c="r")
    plt.xlabel("Número de pedidos (n)")
    plt.ylabel("Probabilidade de um cliente aleatório ter n pedidos (Pn)")
    plt.show()
   
def plotDistProdutosPorPedido(orders):
	x = []
	for order in orders:
		x.append(len(order.products))
	un, cnt = np.unique(x, return_counts=True)
	cnt = [x/len(orders) for x in cnt]
	plt.plot(un, cnt, c="g")
	plt.xlabel("Número de produtos (n)")
	plt.ylabel("Probabilidade de um pedido aleatório ter n produtos (Pn)")
	plt.show()

def plotDistPedidosPorHorario(orders, w2):
	x = []
	col = []
	labels = []
	for order in orders:
		x.append(order.order_dow + (order.order_hod/24))
	un, cnt = np.unique(x, return_counts=True)
	for i in un:
		i = i%1
		if i >= 0 and i <= 0.25:
			col.append("plum")
			labels.append("manhã")
		elif i > 0.25 and i <= 0.5:
			col.append("skyblue")
			labels.append("dia")
		elif i > 0.5 and i <= 0.75:
			col.append("gold")
			labels.append("tarde")
		else:
			col.append("brown")
			labels.append("noite")
	cnt = [x/len(orders) for x in cnt]
	plt.bar(un, cnt, width=w2, color=col, label=labels)
	patches = [Circle((0,0),color="plum"), Circle((0,0),color="skyblue"), Circle((0,0),color="gold"), Circle((0,0),color="brown")]
	plt.legend(patches, ["manhã", "dia", "tarde", "noite"])
	plt.xticks(range(7), ('domingo', 'segunda', 'terça', 'quarta', 'quinta', 'sexta', 'sábado'))
	plt.xlabel("Dia e horário da semana (d)")
	plt.ylabel("Probabilidade de um pedido aleatório no dia e horário d")
	plt.show()

def runKmeans(clients, nClients, nClusters):
    cmap = cm.get_cmap('rainbow', nClusters)
    clientColors = []
    clientValues = []
    print("Gerando matriz de características dos clientes...")
    for i in range(0, nClients):
        client = clients[i]
        clientRecurrences = []
        clientPurchaseTimes = []
        for order in client.orders:
            clientPurchaseTimes.append(max(order.order_hod, 24-order.order_hod))
            if not isnan(order.days_spo):
                clientRecurrences.append(order.days_spo)
        clientValues.append([client.norders, np.median(clientRecurrences), np.median(clientPurchaseTimes)])
    print("Executando Kmeans...")
    kmeans = KMeans(n_clusters=nClusters, random_state=0).fit(clientValues)
    for label in kmeans.labels_:
        clientColors.append(cmap(label))
    fig = plt.figure()
    ax = Axes3D(fig)
    zi = list(zip(*clientValues))
    ax.scatter(zi[0], zi[1], zi[2], c=clientColors)
    zi = list(zip(*kmeans.cluster_centers_))
    ax.scatter(zi[0], zi[1], zi[2], c="k", s=30, marker='*')
    ax.set_xlabel('Número de pedidos')
    ax.set_ylabel('Recorrência média de compra (em dias)')
    ax.set_zlabel('Horário médio de compra')
    ax.set_zticks((12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24))
    ax.set_zticklabels(('12h', '13|11h','14|10h', '15|9h', '16|8h', '17|7h', '18|6h', '19|5h', '20|4h', '21|3h', '22|2h', '23|1h', '24h'))
    plt.show()

def main():
	datasets_path = './data/'

	aisles = read_aisles(datasets_path)
	departments = read_departments(datasets_path)
	products = read_products(datasets_path)
	orders, clients = read_orders_clients(datasets_path, departments, products)
	
	opt = -1
	while opt != 0:
		opt = int(input("Escolha uma das opções abaixo:\n\t\
1 - Plotar distribuição de pedidos por cliente.\n\t\
2 - Plotar distribuição de produtos por pedido.\n\t\
3 - Plotar distribuição de pedidos por dia e horário da semana.\n\t\
4 - Executar K-means.\n\t\
0 - Sair\nSua opção = "))
		if opt == 1:
			plotDistPedidosPorCliente(clients)
		elif opt == 2:
			plotDistProdutosPorPedido(orders)
		elif opt == 3:
			plotDistPedidosPorHorario(orders, 0.033)
		elif opt == 4:
			K = int(input("Defina um número de clusters para o K-means = "))
			print("Executando K-means com K =", K, "...")
			runKmeans(clients, len(clients), K)
			
if __name__ == "__main__":
	main()
