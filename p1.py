from p1_support import load_level, show_level, save_level_costs
from math import inf, sqrt
from heapq import heappop, heappush


def dijkstras_shortest_path(initial_position, destination, graph, adj):
    """ Searches for a minimal cost path through a graph using Dijkstra's algorithm.

    Args:
        initial_position: The initial cell from which the path extends.
        destination: The end location for the path.
        graph: A loaded level, containing walls, spaces, and waypoints.
        adj: An adjacency function returning cells adjacent to a given cell as well as their respective edge costs.

    Returns:
        If a path exits, return a list containing all cells from initial_position to destination.
        Otherwise, return None.

    """
    """
    Skip the entire initialization loop,
    instead use dicts:
    dist[state] = better_distance
    prev[state2] = state1
    """
    # Return prev as a list
    Q = []  # Create a vertex set Q, (list)
    adjacencies = adj()
    heappush(Q, (starting_position, 0))
    dist = {}  # Distance
    prev = {}  # "Back Pointer"
    while Q:
        u = nsmallest(1, Q)  # Remove & return best vertex
        for v in adjacencies:  # Everything else besides best vertex
            alt = dist[u] + length(u, v)
            if v not in dist or alt < dist[v]:
                dist[v] = alt
                prev[v] = u
                Q.decrease_priority(v, alt)
    """
    Because dist will not be defined for unvisited states,
    the expression "alt < dist[v]" must be implemented as
    "v not in dist or alt < dist[v]" or
    "alt < dist.get(v, alt + 1)"
    """
    """
    Use Python's heapq module to implement the priority queue.
    The queue will simply be a Python list containing tuples
    (distance-and-state pairs), but you'll use the heapq
    library to add and remove elements from it
    """
    """
    Instead of returning the "dist" and "prev" tables (dicts),
    recover a specific shortest path and return it instead.
    Represent it as a list of states that starts with their
    source state and ends with the destination state.
    """


def dijkstras_shortest_path_to_all(initial_position, graph, adj):
    # Only returns costs
    # Not returning a dictionary
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
        for dy in [-1, 0, 1]:
            # Makes sure to check if the adjacent squres
            if dx != 0 or dy != 0 and (x + dx, y + dy) in level['spaces']:
                if dx == 0 or dy == 0:
                    new_dist = (
                        0.5 * level['spaces'][x][y] + 0.5 * level['spaces'][x + dx][y + dy])
                else:
                    new_dist = (
                        sqrt(2) * (level['spaces'][x][y] + level['spaces'][x + dx][y + dy]))
                adjacencies.append(((x + dx, y + dy), new_dist))

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
    src = level['waypoints'][src_waypoint]
    dst = level['waypoints'][dst_waypoint]

    # Search for and display the path from src to dst.
    path = dijkstras_shortest_path(src, dst, level, navigation_edges)
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

    # Calculate the cost to all reachable cells from src and save to a csv
    # file.
    costs_to_all_cells = dijkstras_shortest_path_to_all(
        src, level, navigation_edges)
    save_level_costs(level, costs_to_all_cells, output_filename)


if __name__ == '__main__':
    filename, src_waypoint, dst_waypoint = 'example.txt', 'a', 'e'

    # Use this function call to find the route between two waypoints.
    test_route(filename, src_waypoint, dst_waypoint)

    # Use this function to calculate the cost to all reachable cells from an
    # origin point.
    cost_to_all_cells(filename, src_waypoint, 'my_costs.csv')
