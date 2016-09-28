#coding:utf-8
import re
import numpy
import networkx as net
import matplotlib.pyplot as plt

characters = [{'name':'Harry', 're':'哈利·波特|哈利|波特'},
              {'name':'Hermione', 're':'赫敏·格兰杰|赫敏|格兰杰'},
              {'name':'Ron', 're':'罗恩·韦斯莱|罗恩'},
              {'name':'Draco', 're': '德拉科·马尔福|德拉科'},
              {'name':'Voldemort', 're': '伏地魔|黑魔王|神秘人|汤姆·里德尔'},
              {'name': 'Dumbledore', 're': '阿不思·邓布利多|邓布利多|校长|阿不思'},
              {'name': 'Snape', 're': '西弗勒斯·斯内普|斯内普|西弗勒斯'},
              {'name': 'McGonagall', 're': '米勒娃·麦格|麦格|米勒娃'},
              {'name': 'Hagrid', 're': '鲁伯·海格|海格'},
              {'name': 'Lupin', 're': '莱姆斯·卢平|卢平'},
              {'name': 'Sirius', 're': '小天狼星·布莱克|西里斯·布莱克|小天狼星|西里斯'},
              {'name': 'Lucius', 're': '卢修斯·马尔福|卢修斯'},
              {'name': 'Quirell', 're': '奎里纳斯·奇洛|奇洛|奎里纳斯'},
              {'name': 'Bellatrix', 're': '贝拉特里克斯·莱斯特兰奇|贝拉特里克斯'},
              {'name': 'Umbridge', 're': '多洛雷斯·乌姆里奇|乌姆里奇'},
              {'name': 'Peter', 're': '小矮星·彼得|彼得'},
              {'name': 'Fudge', 're': '康奈利·福吉|福吉'},
              {'name': 'James', 're': '詹姆·波特|詹姆'},
              {'name': 'Lily', 're': '莉莉·波特|莉莉'},
              {'name': 'George', 're': '乔治·韦斯莱|乔治'},
              {'name': 'Fred', 're': '弗雷德·韦斯莱|弗雷德'},
              {'name': 'Narcissa', 're': '纳西莎·布莱克|纳西莎·马尔福|纳西莎'},
              {'name': 'Neville', 're': '纳威·隆巴顿|纳威'},
              {'name': 'Luna', 're': '卢娜·洛夫古德|卢娜'},
              {'name': 'Goyle', 're': '格雷戈里·高尔|高尔'},
              {'name': 'Crabbe', 're': '文森特·克拉布|克拉布'},]
dist_threashold = 150

f = file('HP.txt')
text = f.read()
storyline = {}
for index, character in enumerate(characters):
    p = re.compile(character['re'])
    count = 0
    for m in p.finditer(text):
        storyline[m.start()] = index
        count += 1
    characters[index]['count'] = count
s = sorted(storyline.items(), key = lambda x:x[0])
g = net.Graph()
names = {}
for index, character in enumerate(characters):
    g.add_node(index, name = character['name'])
    names[index] = character['name']
for i in range(len(s)):
    t = i + 1
    while (t < len(s) and s[t][0] - s[i][0] < dist_threashold):
        if (s[t][1] != s[i][1]):
            if (g[s[t][1]].has_key(s[i][1])):
                g[s[t][1]][s[i][1]]['weight'] += 1
            else:
                g.add_edge(s[t][1], s[i][1], weight=1)
        t += 1
    t = i - 1
    while (t > 0 and s[i][0] - s[t][0] < dist_threashold):
        if (s[t][1] != s[i][1]):
            if (g[s[t][1]].has_key(s[i][1])):
                g[s[t][1]][s[i][1]]['weight'] += 1
            else:
                g.add_edge(s[t][1], s[i][1], weight=1)
        t -= 1
edge_labels = {}
for i in g:
    for j in g[i]:
        g[i][j]['weight'] /= 2
        edge_labels[(i, j)] = g[i][j]['weight']
#pos = net.circular_layout(g)
pos = net.spring_layout(g, k=2)
weights = [g[u][v]['weight'] for u,v in g.edges()]
weights = [5.0 * k / max(weights) for k in weights]
node_sizes = [characters[u]['count'] for u in g.nodes()]
node_sizes = [10000 * u / max(node_sizes) for u in node_sizes]
net.draw_networkx_edges(g, pos, width = weights, arrows = False)
net.draw_networkx_edge_labels(g, pos, edge_labels=edge_labels)
net.draw_networkx_nodes(g, pos, node_size=node_sizes)
net.draw_networkx_labels(g, pos, labels = names, font_size=20)
plt.show()
print sorted(g.degree(weight='weight').items(), key = lambda x:x[1])
n, bins, patches = plt.hist(numpy.log10(g.degree(weight='weight').values()), log=True, bins=8, range=(1, 5))
plt.xticks(bins, ["10^%s" % i for i in bins])
plt.xlabel('log degree')
plt.ylabel('log freqency')
plt.show()

