class Tabu:
    def __init__(self, size):
        self.list_ = []
        self.size = size

    def push(self, element):
        self.list_.append(element)
        if len(self.list_) > self.size:
            self.list_.pop(0)

    def contains(self, element):
        return element in self.list_
