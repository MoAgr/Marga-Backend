from sqlalchemy.orm import Session
import copy
import crud

class Node:
    node_id=0
    def __init__(self,lati:str,longi:str,name:str):
        print("NODEEEEE:",Node.node_id)
        self.latitude=lati
        self.longitude=longi
        self.name=name
        self.node_id=copy.deepcopy(Node.node_id)
        Node.node_id=Node.node_id+1 

class Graph:
    route_no=1
    paths=[]
    # def __init__(self):
    #     self.adj_list={}
    #     self.nodes=[]
    #     self.coords=[]

    def add_node(self,lati:str,longi:str,name:str,db:Session):
        node=Node(lati,longi,name)
        # self.nodes.append(node)
        # self.adj_list[node.node_id]=[]
        # self.coords.append((lati,longi))

        crud.add_node(db,node)
        crud.add_to_adjlist(db,node.node_id,{node.node_id:[]})
        crud.add_coord(db,lati,longi)
        return node

    def add_edge(self,db:Session,source_id:int,dest_id:int,km:float,route_no:int):
        str_source_id=str(source_id)
        str_dest_id=str(dest_id)

        adj_list_source=crud.get_adjlist(db,source_id)
        adj_list_dest=crud.get_adjlist(db,dest_id)

        source_neighbours=next(iter(adj_list_source.adj_list.values()))
        source_neighbours.append([dest_id,km,route_no])

        dest_neighbours=next(iter(adj_list_dest.adj_list.values()))
        dest_neighbours.append([source_id,km,route_no])

        crud.update_adjlist(db,source_id,{source_id:source_neighbours})
        crud.update_adjlist(db,dest_id,{dest_id:dest_neighbours})
        

        # self.adj_list[source_id].append((dest_id,km,route_no))
        # self.adj_list[dest_id].append((source_id,km,route_no))

    def add_route(self,db:Session,name,yatayat,vehicle_types,route): 
        route_nodes=[]
        yatayat_str=','.join(yatayat)
        vehicle_str=','.join(vehicle_types)
        crud.add_route_details(db,self.route_no,name,yatayat_str,vehicle_str)
        for curr_node in route:
            if crud.has_coord(db,curr_node["lat"],curr_node["lng"]):
                route_nodes.append(crud.get_node_by_latlong(db,curr_node["lat"],curr_node["lng"]))
            else:
                route_nodes.append(self.add_node(curr_node["lat"],curr_node["lng"],curr_node["name"],db))
        
        for pos in range(len(route_nodes)-1):
            self.add_edge(db,route_nodes[pos].node_id,route_nodes[pos+1].node_id,pos,self.route_no) # ?change km to data received from api between this and next node or get km data in each node

        self.route_no+=1

    def get_nodes(self,db:Session):
        return crud.get_nodes(db)

    def get_graph(self,db:Session):
        return crud.get_graph(db)
    
    # def find_km(self,source,destination):
    #     neighbours=copy.deepcopy(self.adj_list[source])
    #     for neighbour in neighbours:
    #         (id_no,km,route_no)=neighbour
    #         if id_no==destination:
    #             return km
            
    # def get_route_no(self,source,destination):
    #     neighbours=copy.deepcopy(self.adj_list[source])
    #     for neighbour in neighbours:
    #         (id_no,km,route_no)=neighbour
    #         if id_no==destination:
    #             return route_no

    # def print_all_paths_util(self, u, d, visited, path):

    #     # Mark the current node as visited and store in path
    #     visited[u]= True
    #     path.append(u)

    #     # If current vertex is same as destination, then print
    #     # current path[]
    #     if u == d:
    #         temp_path=copy.deepcopy(path)
    #         self.paths.append(temp_path)
    #     else:
    #         # If current vertex is not destination
    #         # Recur for all the vertices adjacent to this vertex
    #         for tup in self.adj_list[u]:
    #             (id_no,km,route_no)=tup
    #             if visited[id_no]== False:
    #                 self.print_all_paths_util(id_no, d, visited, path)
                     
    #     # Remove current vertex from path[] and mark it as unvisited
    #     path.pop()
    #     visited[u]= False
  
  
    # # Prints all paths from 's' to 'd'
    # def get_all_paths(self, s, d):
 
    #     # Mark all the vertices as not visited
    #     visited =[False]*(len(self.nodes))
 
    #     # Create an array to store paths
    #     path = []
 
    #     # Call the recursive helper function to print all paths
    #     self.print_all_paths_util(s, d, visited, path)

    #     paths=copy.deepcopy(self.paths)
    #     self.paths=[]
    #     return paths
    
    # def get_sorted_paths(self,s,d):
    #     paths=copy.deepcopy(self.get_all_paths(s,d))
    #     sorted_paths=[]
        
    #     for path in paths:
    #         km=0
    #         change=0
    #         curr_route=0
    #         for pos in range(len(path)-1):
    #             km+=self.find_km(path[pos],path[pos+1])
    #             if(curr_route==0):
    #                 curr_route=self.get_route_no(path[pos],path[pos+1])
    #             elif(curr_route!=self.get_route_no(path[pos],path[pos+1])):
    #                 change+=1
    #                 curr_route=self.get_route_no(path[pos],path[pos+1])
    #         temp_dict={}
    #         temp_dict["Route"]=path
    #         temp_dict["Details"]={"km":km,"change":change}
    #         sorted_paths.append(temp_dict)
        
    #     return sorted_paths
                    


    
# graph=Graph()

# graph.add_route([{
#       "name": "Naxal Bhagwati Bahal",
#       "lat": "1.0",
#       "long": "1.0"
#     },
#     {
#       "name": "Tankeshwor Pul",
#       "lat": "2.0",
#       "long": "2.0"
#     },
#     {
#       "name": "Pulchowk",
#       "lat": "3.0",
#       "long": "3.0"
#     }])

# graph.add_route([{
#       "name": "Naxal Bhagwati Bahal",
#       "lat": "1.0",
#       "long": "1.0"
#     },
#     {
#       "name": "Ratopul",
#       "lat": "4.0",
#       "long": "4.0"
#     },
#     {
#       "name": "Chabahil",
#       "lat": "5.0",
#       "long": "5.0"
#     }])

# graph.add_route([
#     {
#       "name": "Chabahil",
#       "lat": "5.0",
#       "long": "5.0"
#     },
#     {
#       "name": "Pulchowk",
#       "lat": "3.0",
#       "long": "3.0"
#     }])

# print(graph.get_nodes())
# print(graph.get_graph())
# print(graph.get_sorted_paths(0,2))