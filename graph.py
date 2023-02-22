
class Node:
    node_id=1
    def __init__(self,lati:str,longi:str,name:str):
        self.latitude=lati
        self.longitude=longi
        self.name=name
        self.node_id=Node.node_id
        Node.node_id=Node.node_id+1 

class Graph:
    route_no=1
    def __init__(self):
        self.adj_list={}
        self.nodes=[]
        self.coords=[]

    def add_node(self,lati:str,longi:str,name:str):
        node=Node(lati,longi,name)
        self.nodes.append(node)
        self.adj_list[node.node_id]=[]
        self.coords.append((lati,longi))
        return node

    def add_edge(self,source_id:int,dest_id:int,km:float,route_no:int):
        self.adj_list[source_id].append((dest_id,km,route_no))
        self.adj_list[dest_id].append((source_id,km,route_no))

    def add_route(self,route): 
        route_nodes=[]
        for curr_node in route:
            if (curr_node["lat"],curr_node["long"]) in self.coords:
                route_nodes.append(self.nodes[self.coords.index((curr_node["lat"],curr_node["long"]))])
            else:
                route_nodes.append(self.add_node(curr_node["lat"],curr_node["long"],curr_node["name"]))
        
        for pos in range(len(route_nodes)-1):
            self.add_edge(route_nodes[pos].node_id,route_nodes[pos+1].node_id,pos,self.route_no) # ?change km to data received from api between this and next node or get km data in each node

        self.route_no+=1

    def get_nodes(self):
        ret_nodes=[]
        for node in self.nodes:
            ret_nodes.append((node.node_id,node.name))
        return ret_nodes

    def get_graph(self):
        return self.adj_list

    
graph=Graph()

graph.add_route([{
      "name": "Naxal Bhagwati Bahal",
      "lat": "1.0",
      "long": "1.0"
    },
    {
      "name": "Tankeshwor Pul",
      "lat": "2.0",
      "long": "2.0"
    },
    {
      "name": "Pulchowk",
      "lat": "3.0",
      "long": "3.0"
    }])

graph.add_route([{
      "name": "Naxal Bhagwati Bahal",
      "lat": "1.0",
      "long": "1.0"
    },
    {
      "name": "Ratopul",
      "lat": "4.0",
      "long": "4.0"
    },
    {
      "name": "Chabahil",
      "lat": "5.0",
      "long": "5.0"
    }])

print(graph.get_nodes())
print(graph.get_graph())