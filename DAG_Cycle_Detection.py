from collections import defaultdict


class Cycle:

    def resolve_permissions(self, edges):
        graph = defaultdict(list)
        all_nodes = set() # this is needed because we need to get diconnected graph as well.
        for node, edge in edges:
            graph[node].append(edge)
            all_nodes.add(node)
            all_nodes.add(edge)
        UNVISITED = 0
        VISTING = 1
        VISTED = 2
        states = {node: UNVISITED for node in all_nodes}# this is needed to have all nodes put as unvsted.

        for start in all_nodes:
            stack = [start] #
            while stack: # this is iteration approach and not a recursion approach.
                # We need to do this to go deep to every node and to do so we start putting value in stack with start
                # We peek (UNVISITED) -> append to stack -> mark it as VISTING -> and then mark as VISITED
                node = stack[-1] # this is the very first node.
                if states[node] == UNVISITED: # begin with this as UNVISTED
                    states[node] = VISTING # the moment you get UNVISTED node you mark it as unvisted
                    for nei in graph[node]: # nei would not be marked as VISITED or VISITNG. It is readOnly. It will always be the node
                        # graph[node] -> this will be the node of the graph remener this form. Its the node and you keep visitng it.
                        # access to the node is graph[node] and also access is an index
                        if states[nei] == VISTING:
                            return True
                        if states[nei] == UNVISITED:
                            stack.append(nei)
                else:
                    states[node] = VISTED
                    stack.pop()
        return False






