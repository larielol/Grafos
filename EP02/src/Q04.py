import networkx as nx


def mfs_greedy(ddc):

    if(ddc is None) or (not nx.is_directed(ddc)):
        return None

    md_cycles = encontrar_ciclos_minimos_dependencia(ddc)

    mfs = []

    while md_cycles:
        max_ocorrencias = 0
        max_arco = None

        for ciclo in md_cycles:
            for arco in ciclo:
                ocorrencias = sum(1 for c in md_cycles if arco in c)
                if ocorrencias > max_ocorrencias or (ocorrencias == max_ocorrencias and comparar_arcos(arco, max_arco, ddc)):
                    max_ocorrencias = ocorrencias
                    max_arco = arco

        mfs.append(max_arco)

        md_cycles = [ciclo for ciclo in md_cycles if max_arco not in ciclo]

    return mfs


def encontrar_ciclos_minimos_dependencia(ddc):
    arcos_ciclos = []
    ciclos = []

    def dfs(no, visitados, caminho):
        visitados.add(no)
        caminho.append(no)

        for vizinho in ddc[no]:
            if vizinho in caminho:
                indice_vizinho = caminho.index(vizinho)
                ciclo = caminho[indice_vizinho:]
                ciclos.append(ciclo)
            elif vizinho not in visitados:
                dfs(vizinho, visitados, caminho)

        caminho.pop()
        visitados.remove(no)

    visitados = set()

    for node in ddc:
        if node not in visitados:
            dfs(node, visitados, [])

    for ciclo in ciclos:
        # Verificar se o ciclo é completo
        if len(ciclo) < len(ddc) and len(set(ciclo)) == len(ciclo):
            arcos_ciclo = [(ciclo[i], ciclo[i+1]) for i in range(len(ciclo) - 1)]
            arco_final = (ciclo[-1], ciclo[0])
            arcos_ciclo.append(arco_final)
            arcos_ciclos.append(arcos_ciclo)

    return arcos_ciclos

def comparar_arcos(arco1, arco2, ddc):

    inicio1, fim1 = arco1
    inicio2, fim2 = arco2

    fan_out1 = len(list(ddc.successors(inicio1)))
    fan_out2 = len(list(ddc.successors(inicio2)))
    fan_in1 = len(list(ddc.predecessors(inicio1)))
    fan_in2 = len(list(ddc.predecessors(inicio2)))

    if fan_out1 > fan_out2:
        return True
    elif fan_out1 == fan_out2:
        if fan_in1 > fan_in2:
            return True
        elif fan_in1 == fan_in2:
            return (inicio1, fim1) > (inicio2, fim2)

    return False