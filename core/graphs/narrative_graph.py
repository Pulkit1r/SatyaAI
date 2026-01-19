import networkx as nx

def build_graph(narratives):

    G = nx.Graph()

    for nid, items in narratives.items():
        G.add_node(nid, type="narrative")

        for idx, i in enumerate(items):
            cid = f"{nid}_{idx}"
            G.add_node(cid, type=i.get("type","text"))
            G.add_edge(nid, cid)

            if "source" in i:
                G.add_node(i["source"], type="platform")
                G.add_edge(cid, i["source"])

    return G
