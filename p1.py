from p1_support import load_level, show_level, save_level_costs
from math import inf, sqrt
from heapq import heappop, heappush


def dijkstras_shortest_path(initial_position, destination, graph, adj):
    """ Searches for a minimal cost path through a graph using Dijkstra's algorithm.

    Args:
        initial_position: The initial cell from which the path extends.
        destination: The end location for the path.
        graph: A loaded level, containing walls, spaces, and waypoints.
        adj: An adjacency function retudrning cells adjacent to a given cell as well as their respective edge costs.

    Returns:
        If a path exits, return a list containing all cells from initial_position to destination.
        Otherwise, return None.

    """
    dist = {}
    prev = {}
    queue = []
    print(initial_position)
    heappush(queue, (0,(graph['waypoints'][initial_position])))# distance
    dist[graph['waypoints'][initial_position]] = 0 # Initialize summed distance from source waypoint
    prev[graph['waypoints'][initial_position]] = None #Initializing Previous Node
    while queue:
        distance, coordinate= heappop(queue) # Pops head of the heapq
        adjacency = adj(graph, coordinate)
        for (coordinate2,distance) in adjacency:
            alt=dist[coordinate] + distance
            if (coordinate2 not in dist) or (alt < dist[coordinate2]):#other stuff :
                dist[coordinate2]=alt
                prev[coordinate2]=coordinate
                heappush(queue, (alt,(coordinate2)))
                # *** need to finish ***
                if coordinate2 == graph['waypoints'][destination]:
                    print("found")
    coordinate3=graph['waypoints'][destination]
    path_list = []
    while(prev[coordinate3]!=None):
        path_list.append(coordinate3)
        coordinate3=prev[coordinate3]
    path_list.append(graph['waypoints'][initial_position])

    return(path_list)
    pass


def dijkstras_shortest_path_to_all(initial_position, graph, adj):
    """ Calculates the minimum cost to every reachable cell in a graph from the initial_position.
    Args:
        initial_position: The initial cell from which the path extends.
        graph: A loaded level, containing walls, spaces, and waypoints.
        adj: An adjacency function returning cells adjacent to a given cell as well as their respective edge costs.

    Returns:
        A dictionary, mapping destination cells to the cost of a path from the initial_position.
    """
    pass


def navigation_edges(level, cell):
    """ Provides a list of adjacent cells and their respective costs from the given cell.

    Args:
        level: A loaded level, containing walls, spaces, and waypoints.
        cell: A target location.

    Returns:
        A list of tuples containing an adjacent cell's coordinates and the cost of the edge joining it and the
        originating cell.

        E.g. from (0,0):
            [((0,1), 1),
             ((1,0), 1),
             ((1,1), 1.4142135623730951),
             ... ]
    """
    adjacencies = []
    x, y = cell

    for dx in [-1, 0, 1]:
        for dy in [-1,0,1]:
            if (x+dx, y+dy) in level['spaces'] and (dx!=0 or dy!=0): # Makes sure to check if the adjacent squares
                x2 = x + dx
                y2 = y + dy
                #print(x + dx, y + dy)
                if dx==0 or dy==0:
                    new_dist=(0.5*(level['spaces'][(x2, y2)] + level['spaces'][(x, y)]))
                else:
                    new_dist = sqrt(2)*0.5*(level['spaces'][(x2, y2)] + level['spaces'][(x, y)])
                adjacencies.append(((x2, y2),new_dist))

    return adjacencies
    pass


def test_route(filename, src_waypoint, dst_waypoint):
    """ Loads a level, searches for a path between the given waypoints, and displays the result.

    Args:
        filename: The name of the text file containing the level.
        src_waypoint: The character associated with the initial waypoint.
        dst_waypoint: The character associated with the destination waypoint.

    """

    # Load and display the level.
    level = load_level(filename)
    show_level(level)

    # Retrieve the source and destination coordinates from the level.
    #src = level['waypoints'][src_waypoint]
    #dst = level['waypoints'][dst_waypoint]

    # Search for and display the path from src to dst.
    path = dijkstras_shortest_path(src_waypoint, dst_waypoint, level, navigation_edges)
    print(path)
    if path:
        show_level(level, path)
    else:
        print("No path possible!")


def cost_to_all_cells(filename, src_waypoint, output_filename):
    """ Loads a level, calculates the cost to all reachable cells from 
    src_waypoint, then saves the result in a csv file with name output_filename.

    Args:
        filename: The name of the text file containing the level.
        src_waypoint: The character associated with the initial waypoint.
        output_filename: The filename for the output csv file.

    """
    
    # Load and display the level.
    level = load_level(filename)
    show_level(level)

    # Retrieve the source coordinates from the level.
    src = level['waypoints'][src_waypoint]
    
    # Calculate the cost to all reachable cells from src and save to a csv file.
    costs_to_all_cells = dijkstras_shortest_path_to_all(src, level, navigation_edges)
    save_level_costs(level, costs_to_all_cells, output_filename)


if __name__ == '__main__':
    filename, src_waypoint, dst_waypoint = 'example.txt', 'a','e'

    #level = load_level(filename)

    #dijkstras_shortest_path(src_waypoint,dst_waypoint, level, navigation_edges)
    #show_level(level)

    #navigation_edges(level,(1,1))
    # Use this function call to find the route between two waypoints.
    test_route(filename, src_waypoint, dst_waypoint)

    # Use this function to calculate the cost to all reachable cells from an origin point.
    #cost_to_all_cells(filename, src_waypoint, 'my_costs.csv')
