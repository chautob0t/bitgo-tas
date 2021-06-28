from collections import defaultdict


class DFS:
    def __init__(self, nodes, ancestors):
        self.one_level_ancestors = ancestors
        self.adjacency_list = defaultdict(set)
        self.all_ancestors = defaultdict(set)
        self.vertices = nodes

    def prepare_adjacency_list(self):
        for vertex in self.vertices:
            parents = self.one_level_ancestors[vertex]
            for parent in parents:
                self.adjacency_list[parent].add(vertex)

    def __find_all_ancestors(self, vertex, parents=[]):
        # Update parents of the vertex we are at
        self.all_ancestors[vertex].add(parents)
        # Add current vertex to the parents
        parents.append(vertex)
        children = self.adjacency_list[vertex]
        for child in children:
            # Recursively call DFs for all the children
            self.find_all_ancestors(child, parents)
        # As the recursion folds, remove the last parent that we added
        parents.pop()

    def find_all_ancestors(self):
        for vertex in self.vertices:
            # Find all ancestors for each vertex in graph
            self.__find_all_ancestors(vertex, [])
        return self.all_ancestors
