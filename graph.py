from sqlalchemy.orm import Session
import copy
import crud

class Node:
    node_id=0
    def __init__(self,db:Session,lati:str,longi:str,name:str):
        Node.node_id=len(crud.get_nodes(db))
        self.latitude=lati
        self.longitude=longi
        self.name=name
        self.node_id=copy.deepcopy(Node.node_id)
        Node.node_id=Node.node_id+1 

class Graph:
    route_no=1
    paths=[]
    def __init__(self,db:Session):
        Graph.route_no=len(crud.get_all_routes(db))+1
        Graph.paths=[]

    def add_node(self,lati:str,longi:str,name:str,db:Session):
        node=Node(db,lati,longi,name)
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
            elif crud.get_node_in_range(db,(curr_node["lat"]-0.0007,curr_node["lat"]+0.0007),
                                        (curr_node["lng"]-0.0005,curr_node["lng"]+0.0005)):
                route_nodes.append(crud.get_node_in_range(db,(curr_node["lat"]-0.0007,curr_node["lat"]+0.0007),
                                        (curr_node["lng"]-0.0005,curr_node["lng"]+0.0005)))
            else:
                route_nodes.append(self.add_node(curr_node["lat"],curr_node["lng"],curr_node["stopName"],db))
        
        for pos in range(len(route_nodes)-1):
            self.add_edge(db,route_nodes[pos].node_id,route_nodes[pos+1].node_id,pos,self.route_no) # ?change km to data received from api between this and next node or get km data in each node

        self.route_no+=1

    def get_nodes(self,db:Session):
        return crud.get_nodes(db)

    def get_graph(self,db:Session):
        return crud.get_graph(db)
    
    def find_km(self,db:Session,source,destination):
        adj_list_source=crud.get_adjlist(db,source)
        source_neighbours=next(iter(adj_list_source.adj_list.values()))
        for neighbour in source_neighbours:
            id_no,km,route_no=neighbour
            if id_no==destination:
                return km
            
    def get_route_no(self,db:Session,source,destination):
        adj_list_source=crud.get_adjlist(db,source)
        source_neighbours=next(iter(adj_list_source.adj_list.values()))
        # print(destination)
        for neighbour in source_neighbours:
            # print(neighbour)
            id_no,km,route_no=neighbour
            # print(route_no,neighbour[2])
            if id_no==destination:
                return route_no

    def print_all_paths_util(self,db:Session, u, d, visited, path):

        # Mark the current node as visited and store in path
        visited[u]= True
        path.append(u)

        # If current vertex is same as destination, then print
        # current path[]
        if u == d:
            temp_path=copy.deepcopy(path)
            Graph.paths.append(temp_path)
        else:
            # If current vertex is not destination
            # Recur for all the vertices adjacent to this vertex
            adj_list_u=crud.get_adjlist(db,u)
            u_neighbours=next(iter(adj_list_u.adj_list.values()))

            for neighbour in u_neighbours:
                id_no,km,route_no=neighbour
                if visited[id_no]== False:
                    self.print_all_paths_util(db,id_no, d, visited, path)
                     
        # Remove current vertex from path[] and mark it as unvisited
        path.pop()
        visited[u]= False
  
  
    # Prints all paths from 's' to 'd'
    def get_all_paths(self,db, s, d):
 
        # Mark all the vertices as not visited
        # print("TOTAL NODES=",len(self.get_nodes(db)))
        visited =[False]*(len(self.get_nodes(db)))
 
        # Create an array to store paths
        path = []
 
        # Call the recursive helper function to print all paths
        self.print_all_paths_util(db,s, d, visited, path)

        paths=copy.deepcopy(Graph.paths)
        Graph.paths=[]
        # print("get_all_paths",paths)
        return paths
    
    def get_sorted_paths(self,db:Session,s,d):
        paths=copy.deepcopy(self.get_all_paths(db,s,d))
        sorted_paths=[]
        # all_route_details=crud.get_all_routes(db)
        for path in paths:
            km=0
            change=0
            curr_route=0
            route_nos=[]
            yatayat=[]
            vehicles=[]
            changes=[]
            for pos in range(len(path)-1):
                km+=self.find_km(db,path[pos],path[pos+1])
                route_no=self.get_route_no(db,path[pos],path[pos+1])
                if(curr_route==0):
                    curr_route=route_no
                    route_nos.append(route_no)
                elif(curr_route!=route_no):
                    change+=1
                    changes.append(path[pos])
                    curr_route=route_no
                    route_nos.append(route_no)

            temp_dict={}
            path_dets=[]

            for route in route_nos:
                route_det_json=crud.get_route_details(db,route)

                yatayat_str=copy.deepcopy(route_det_json.yatayat)
                yatayat_lst=copy.deepcopy(yatayat_str.split(','))
                vehicles_str=copy.deepcopy(route_det_json.vehicle_types)
                vehicles_lst=copy.deepcopy(vehicles_str.split(','))

                yatayat.append(yatayat_lst)
                vehicles.append(vehicles_lst)

            for node_id in path:
                returned_node=crud.get_node(db,node_id)
                temp_node={}
                temp_node["lat"]=copy.deepcopy(returned_node.lat)
                temp_node["lng"]=copy.deepcopy(returned_node.lng)
                temp_node["stopName"]=copy.deepcopy(returned_node.name)
                if node_id in changes:
                    temp_node["change"]=True
                else:
                    temp_node["change"]=False

                path_dets.append(temp_node)
            
            temp_dict["yatayat"]=yatayat
            temp_dict["vehicleTypes"]=vehicles
            temp_dict["route"]=path_dets
            temp_dict["details"]={"km":km,"change":change}
            sorted_paths.append(temp_dict)
        
        # print("get_sorted_paths",sorted_paths)
        return sorted_paths
                    
    def get_all_routes(self,db:Session):
        all_routes=[]
        total_routes=crud.route_details_no(db)
        all_adjlists=crud.get_graph(db)
        all_route_details=crud.get_all_routes(db)

        for i in range(1,total_routes+1): #change this pachi
            temp_route={}
            temp_nodes=[]
            for adjlist in all_adjlists:
                node_id=adjlist.node_id
                connections=next(iter(adjlist.adj_list.values()))
                for connection in connections:
                    if connection[-1]==i and connection[0]>node_id:
                        if(len(temp_nodes)==0):
                            temp_nodes.append(crud.get_node(db,node_id))
                        else:
                            temp_nodes.append(crud.get_node(db,connection[0]))

            # route_dets=crud.get_route_details(db,)
            temp_route["route"]=temp_nodes
            temp_route["route_id"]=all_route_details[i-1].route_id
            temp_route["yatayat"]=all_route_details[i-1].yatayat
            temp_route["vehicleTypes"]=all_route_details[i-1].vehicle_types
            all_routes.append(temp_route)

        return all_routes


                        



                








    
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