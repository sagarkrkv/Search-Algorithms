import sys
from collections import defaultdict
from math import radians, cos, sin, asin, sqrt
# http://www.bogotobogo.com/python/python_graph_data_structures.php
## http://www.bogotobogo.com/python/python_Dijkstras_Shortest_Path_Algorithm.php
### http://stackoverflow.com/questions/4913349/ Haversine formula for calculating distance between GPS Coordinates

'''
    We make our graph model based the tutorial above. The tutorial 
    did not show A star algorithm directly. It is acrtually 
    Dijkstras Shortest Path Algorithm, so we change a lot from the code
    to implement A star search algorithm.

    We did not implement our own Priority Queues.
    We used the python build-in heap lib directly. 

    For BFS and DFS, we just follow the pseudo-code in our text book.

    Since some speed data is not correct, we assume it is 60.

'''


GPS_INFO = {}

class Vertex:
    def __init__(self, cityname):
        self.cityname = cityname
        self.adjacent = {}

        ## 
        self.distance = sys.maxint
        self.previous = None

    def add_neighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] = weight

    def get_weight_from_to(self, neighbor, data_access=None):
        if data_access is None:
            return self.adjacent[neighbor]
        return self.adjacent[neighbor][data_access]

    def get_connections(self):
        return self.adjacent.keys()

    def get_f(self, city):
        return self.get_g(city) + self.get_h(city)

    def get_h(self, city, option="distance"):
        if option == "distance":
            p1, p2 = GPS_INFO.get(self.cityname), GPS_INFO.get(city.cityname)
            if None in (p1, p2):
                return 0
                # self.get_weight_from_to(city, data_access="distance")
            return gps_distance(p1, p2)
        elif option == "segment":
            return 1
        else:
            return 0

    def get_g(self, city, option="distance"):
        return self.get_weight_from_to(city, data_access=option)

    def __str__(self):
        return str(self.cityname) + ":"

    def __hash__(self):
        return hash(self.cityname)

    def __eq__(self, other):
        return self.cityname == other.cityname


class Graph:
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0


    def add_vertex(self, cityname):
        if cityname not in self.vert_dict:
            self.num_vertices = self.num_vertices + 1
            new_vertex = Vertex(cityname)
            self.vert_dict[cityname] = new_vertex
            return new_vertex

    def get_weight_from_to(self, from_city, to_city):
        # maybe some problems here
        # data_access = data_access or "distance"
        return self.vert_dict.get(from_city.cityname, None).get_weight_from_to(to_city)

    def add_edge(self, frm, to, info=None):
        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)

        self.vert_dict[frm].add_neighbor(self.vert_dict[to], info)
        self.vert_dict[to].add_neighbor(self.vert_dict[frm], info)

    def get_vertex(self, cityname):
        return self.vert_dict.get(cityname, None)

    def __str__(self):
        return "Graph(%s):%s)"%(self.num_vertices, str(self.vert_dict))


def parse_from_segment():
    graph = Graph()
    road_speed = defaultdict(lambda: 60)
    data_process_later = []
    with open("road-segments.txt", "r") as f:
        for line in f:
            data = line.split()
            if len(data) == 5:
                from_city, end_city, distance, speed, ave_name = line.split()
                road_speed[ave_name] = speed
            else:
                data_process_later.append(data)
            graph.add_vertex(from_city)
            graph.add_vertex(end_city)

            info = {
                "distance": float(distance),
                "segment": 1,
                "speed": float(speed) or 60,
                "ave_name": ave_name,
                "time": float(distance)/(float(speed) or 60)
            }


            graph.add_edge(from_city, end_city, info)

    # some data are dirty
    # try our best to clean it up
    for data in data_process_later: 
        from_city, end_city, distance, ave_name = data 
        info = {
                "distance": float(distance),
                "speed": float(speed),
                "segment": 1,
                "ave_name": ave_name,
                "time": float(distance)/float(speed)
            }

        graph.add_edge(from_city, end_city, info)

    return graph
            
def parse_from_gps():
    d = {} # "city": (lat, long)

    with open("city-gps.txt", "r") as f:
        for line in f:
            data = line.split()
            if len(data) == 3:
                tmp_city, tmp_lat, tmp_lon = line.split()
                d[tmp_city] = (float(tmp_lat), float(tmp_lon))

    return d

def gps_distance(p1, p2):
    from_city_lon, from_city_lat = p1
    end_city_lon, end_city_lat = p2
    from_city_lon, from_city_lat, end_city_lon, end_city_lat = map(radians, [from_city_lon, from_city_lat, end_city_lon, end_city_lat])
    dlon = end_city_lon - from_city_lon
    dlat = end_city_lat - from_city_lat
    a = sin(dlat/2)**2 + cos(from_city_lat) * cos(end_city_lat) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    heuristic_dist = 3956 * c
    return heuristic_dist


# based on text book page 82
# this will return a path. which is a list contain city(Vertex)
def bfs(start_city_name, end_city_name, graph):
    start_city = graph.get_vertex(start_city_name)
    end_city = graph.get_vertex(end_city_name)
    goal_test = lambda x: x == end_city
    explored = set()
    frontier = [start_city] # use list to simulate queue
    path_list = [[start_city]]
    while frontier:
        node = frontier.pop(0)
        path = path_list.pop(0)

        if node not in explored:
            explored.add(node)

        for child_node in node.get_connections():
            if child_node not in explored:
                new_path = path[:]
                new_path.append(child_node)
                path_list.append(new_path)
                if goal_test(child_node):
                    return new_path
                frontier.append(child_node)

def dfs(start_city_name, end_city_name, graph):
    start_city = graph.get_vertex(start_city_name)
    end_city = graph.get_vertex(end_city_name)
    goal_test = lambda x: x == end_city
    explored = set()
    frontier = [start_city] # use list to simulate queue
    path= []
    while frontier:
        node = frontier.pop()
        if node not in explored:
            explored.add(node)
            path.append(node)
            frontier.extend(set(node.get_connections()) - explored)
        if goal_test(node):
            return path
    return path

import heapq
## we may implement this heap later

def a_star(start_city_name, end_city_name, graph, option="distance"):
    start_city = graph.get_vertex(start_city_name)
    start_city.distance = 0
    end_city = graph.get_vertex(end_city_name)
    goal_test = lambda x: x == end_city

    opened = []
    heapq.heapify(opened)
    closed = set()
    opened_set = set()
    heapq.heappush(opened, (start_city.distance, start_city))
    opened_set.add(start_city)

    while len(opened):
        _, node = heapq.heappop(opened)
        # print "%s:%s"%(node.cityname, node.distance)
        opened_set.discard(node)
        closed.add(node)
        if goal_test(node):
            break

        for _next in node.adjacent:
            if _next not in closed:
                new_dist = node.distance + node.get_g(_next, option=option)
                if _next in opened_set:
                    if new_dist < _next.distance:
                        _next.distance = new_dist
                        _next.previous = node
                        heapq.heappush(opened, (_next.distance ,_next))
                        opened_set.add(_next)
                elif _next not in opened_set:
                    _next.distance = new_dist
                    _next.previous = node
                    heapq.heappush(opened, (_next.distance ,_next))
                    opened_set.add(_next)

    def shortest(v, path):
        ''' make shortest path from v.previous'''
        if v.previous:
            shortest(v.previous, path)
            path.append(v.previous)

    path = []
    shortest(end_city, path)
    path.append(end_city)
    # print end_city.distance
    return path


if __name__ == "__main__":
    start_city_name, end_city_name, routing_option, routing_algorithm = sys.argv[1:]
    graph = parse_from_segment()
    path = []
    if routing_algorithm == "astar":
        GPS_INFO = parse_from_gps()
        path = a_star(start_city_name, end_city_name, graph, option=routing_option)

    if routing_algorithm == "bfs":
        path = bfs(start_city_name, end_city_name, graph)

    if routing_algorithm == "dfs":
        path = dfs(start_city_name, end_city_name, graph)


    # print [c.cityname for c in path]

    def yield_nearby_city(city_list):
        i = 0
        while i < len(city_list) - 1:
            yield city_list[i], city_list[i+1]
            i += 1
    
    total_distance, total_time = 0, 0
    for city1, city2 in yield_nearby_city(path):
        info = graph.get_weight_from_to(city1, city2)
        total_distance += info["distance"]
        total_time += info["distance"]/info["speed"]

    path_str = " ".join([c.cityname for c in path])
    print "%s %s %s"%(total_distance, total_time, path_str)



