class Node:
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.next = self.prev = None
class LRU:
    def __init__(self, capacity):
        if capacity < 0:
            raise ValueError("Error")
        self.cap = capacity
        self.cache = {} # hashmap with O(1) search
        self.right = Node(0,0)
        self.left = Node(0,0)
        self.left.next = self.right
        self.right.prev = self.left

    def insert(self, node):
        before = self.right.prev
        after = self.right

        #connect node to its neighbours
        node.prev = before
        node.next = after

        #connect nieghers to the node
        before.next = node
        after.prev = node


    def remove(self, node):
        before = node.prev
        after = node.next
        before.next = after
        after.prev = before

    def get(self, key):
        if key in self.cache:
            # you need to update the MRU in the linked list
            # because if you get the item it needs to be marked to the right
            self.remove(self.cache[key])
            self.insert(self.cache[key])
            return self.cache[key].val
        return -1

    def put(self, key, val):
        if self.cap == 0:
            return
        if key in self.cache:
            self.remove(self.cache[key])
        # Peek -> remove -> Create Node -> Insert
        self.cache[key] = Node(key, val)
        self.insert(self.cache[key])
        if len(self.cache) > self.cap:
            # we need to remove from the list from the left
            lru = self.left.next #temp storing here in lru
            self.remove(lru)
            del self.cache[lru.key]



def test_lru():

    rl = LRU(2)
    rl.put(1,3)
    rl.put(2,10)
    rl.put(3,30)
    assert rl.get(2) == 10
    assert rl.get(3) == 30
    rl.put(1, 40)
    assert rl.get(1) == 40
    print("all LRU pass")
test_lru()




