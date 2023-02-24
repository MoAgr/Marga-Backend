import copy

class Node:
    node_id=0
    def __init__(self,lati:str,longi:str,name:str):
        self.latitude=lati
        self.longitude=longi
        self.name=name
        self.node_id=Node.node_id
        Node.node_id=Node.node_id+1 

class Graph:
    route_no=1
    paths=[]
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
    
    def find_km(self,source,destination):
        neighbours=copy.deepcopy(self.adj_list[source])
        for neighbour in neighbours:
            (id_no,km,route_no)=neighbour
            if id_no==destination:
                return km
            
    def get_route_no(self,source,destination):
        neighbours=copy.deepcopy(self.adj_list[source])
        for neighbour in neighbours:
            (id_no,km,route_no)=neighbour
            if id_no==destination:
                return route_no

    def print_all_paths_util(self, u, d, visited, path):

        # Mark the current node as visited and store in path
        visited[u]= True
        path.append(u)

        # If current vertex is same as destination, then print
        # current path[]
        if u == d:
            temp_path=copy.deepcopy(path)
            self.paths.append(temp_path)
        else:
            # If current vertex is not destination
            # Recur for all the vertices adjacent to this vertex
            for tup in self.adj_list[u]:
                (id_no,km,route_no)=tup
                if visited[id_no]== False:
                    self.print_all_paths_util(id_no, d, visited, path)
                     
        # Remove current vertex from path[] and mark it as unvisited
        path.pop()
        visited[u]= False
  
  
    # Prints all paths from 's' to 'd'
    def get_all_paths(self, s, d):
 
        # Mark all the vertices as not visited
        visited =[False]*(len(self.nodes))
 
        # Create an array to store paths
        path = []
 
        # Call the recursive helper function to print all paths
        self.print_all_paths_util(s, d, visited, path)

        paths=copy.deepcopy(self.paths)
        self.paths=[]
        return paths
    
    def get_sorted_paths(self,s,d):
        paths=copy.deepcopy(self.get_all_paths(s,d))
        sorted_paths=[]
        
        for path in paths:
            km=0
            change=0
            curr_route=0
            for pos in range(len(path)-1):
                km+=self.find_km(path[pos],path[pos+1])
                if(curr_route==0):
                    curr_route=self.get_route_no(path[pos],path[pos+1])
                elif(curr_route!=self.get_route_no(path[pos],path[pos+1])):
                    change+=1
                    curr_route=self.get_route_no(path[pos],path[pos+1])
            temp_dict={}
            temp_dict["Route"]=path
            temp_dict["Details"]={"km":km,"change":change}
            sorted_paths.append(temp_dict)
        
        return sorted_paths
                    


    
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

graph.add_route([
    {
      "name": "Chabahil",
      "lat": "5.0",
      "long": "5.0"
    },
    {
      "name": "Pulchowk",
      "lat": "3.0",
      "long": "3.0"
    }])

print(graph.get_nodes())
print(graph.get_graph())
print(graph.get_sorted_paths(0,2))