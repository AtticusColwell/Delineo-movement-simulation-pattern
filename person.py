class Person:
    def __init__(self) -> None:
        self.is_poi = False     # Boolean to check if someone is in POI
        self.visited = {}       # HashMap of visited POIs and visited numbers
        self.total_visited = 0  # Total number of visited POIs
        self.curr_poi = ""      # Current POI
        self.hour_stayed = 0    # Hours stayed at current POI

    def visit(self, poi: str):
        """Logs a visit to a point of interest."""
        if poi in self.visited:
            self.visited[poi] += 1
        else:
            self.visited[poi] = 1
        self.total_visited += 1
        self.is_poi = True
        self.curr_poi = poi
        self.hour_stayed = 1  # Reset hour_stayed when visiting a new POI

    def leave(self):
        """Leaves a point of interest."""
        self.is_poi = False
        self.hour_stayed = 0
        self.curr_poi = ""
    
    def stay(self):
        self.hour_stayed += 1

    def __repr__(self) -> str:
        return (f"Person(is_poi={self.is_poi}, curr_poi='{self.curr_poi}', "
                f"hour_stayed={self.hour_stayed}, total_visited={self.total_visited}, "
                f"visited={self.visited})")
