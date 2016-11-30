#coding=utf-8
import random

IC_ITERATION = 100      # IC取循环IC_ITERATION次均值

def read_from_txt(filename):
    """
    从txt文件中读入图数据
    :param filename: 读入网络文件名
    :return: 图g，以dict形式存储
    """
    g = {}
    with open(filename) as f:
        lines = f.readlines()[1:]
        for line in lines:
            e = [int(s) for s in line.replace('\n', '').split(' ')]
            r = random.random() * 0.5
            if e[0] in g.keys():
                g[e[0]][e[1]] = r
            else:
                g[e[0]] = {e[1]: r}
            if e[1] in g.keys():
                g[e[1]][e[0]] = r
            else:
                g[e[1]] = {e[0]: r}
    return g

def IC(g, A):
    """
    独立瀑布模型IC（Independent Cascade）计算集合A中节点的影响力
    :param g: 图
    :param A: 顶点编号集合，以set存储
    :return: 影响力
    """
    res = 0.0
    for _ in range(IC_ITERATION):
        total_activated_nodes = set()
        for u in A:
            l1 = {u}
            l2 = set()
            failed_nodes = set()
            activated_nodes = {u}
            while len(l1):
                for v in l1:
                    for w, weight in g[v].items():
                        r = random.random()
                        if w not in failed_nodes and w not in activated_nodes and r < weight:
                            l2.add(w)
                            activated_nodes.add(w)
                        else:
                            failed_nodes.add(w)
                l1 = l2
                l2 = set()
            total_activated_nodes.update(activated_nodes)
        res += len(total_activated_nodes)
    return res / IC_ITERATION

def greedy(g, k):
    """
    贪心算法计算最大影响力的k个节点
    :param g: 图
    :param k: 节点数量
    :return: (最大影响力节点集合（以set存储）, 最大影响力)
    """
    A = set()
    V = set(g.keys())
    for _ in range(k):
        max_influence = 0
        max_influence_node = 0
        for v in V - A:
            influence_A_and_v = IC(g, A | {v})
            if max_influence < influence_A_and_v:
                max_influence = influence_A_and_v
                max_influence_node = v
        A.add(max_influence_node)
    return A, max_influence

def CELF(g, k):
    """
    CELF算法计算最大影响力的k个节点
    :param g: 图
    :param k: 节点数量
    :return: (最大影响力节点集合（以set存储）, 最大影响力)
    """
    V = set(g.keys())
    max_increment = {i:IC(g, {i}) for i in g.keys()}
    t_max_increment = max_increment.copy()
    t = sorted(max_increment.items(), key=lambda x:x[1], reverse=True)
    A = set([t[0][0]])
    max_influence = t[0][1]
    del t_max_increment[t[0][0]]
    for _ in range(k - 1):
        max_increment_current = 0
        max_increment_node = 0
        t = sorted(t_max_increment.items(), key=lambda x:x[1], reverse=True)
        for v, _ in t:
            if max_increment[v] > max_increment_current:
                increment_A_and_v = IC(g, A | {v}) - max_influence
                if max_increment_current < increment_A_and_v:
                    max_increment_current = increment_A_and_v
                    max_increment[v] = t_max_increment[v] = increment_A_and_v
                    max_increment_node = v
        A.add(max_increment_node)
        max_influence = max_influence + max_increment_current
        del t_max_increment[max_increment_node]
    return A, max_influence

def degree(g, k):
    """
    degree算法计算最大影响力的k个节点（取度最大的k个节点）
    :param g: 图
    :param k: 节点数量
    :return: (最大影响力节点集合（以set存储）, 最大影响力)
    """
    l = sorted(g.items(), key=lambda x:len(x[1]), reverse=True)
    A = [l[i][0] for i in range(k)]
    return A, IC(g, A)

def rand(g, k):
    """
    random算法计算最大影响力的k个节点（随机取k个节点）
    :param g: 图
    :param k: 节点数量
    :return: (最大影响力节点集合（以set存储）, 最大影响力)
    """
    A = [g.keys()[random.randint(0, len(g))] for i in range(k)]
    return A, IC(g, A)