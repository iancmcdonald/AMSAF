from Queue import PriorityQueue


class CompareResults:
    def __init__(self):
        self.database = PriorityQueue()  # creates a new queue to store results

    def AddItem(self, parammap, priority):
        """ adds new parameter map to database

        Args:
            parammap (SimpleITK.SimpleITK.ParameterMap): The corresponding parameter map
            priority: Priority based on the result from AbstractEvaluator.py (higher is worse/lower priority)
        """
        self.database.put(priority, parammap)

    def getHighest(self):
        """ returns the highest priority parameter map

        Returns: (SimpleITK.SimpleITK.ParameterMap) of the best parameter map in the database

        """
        return self.database.get()
