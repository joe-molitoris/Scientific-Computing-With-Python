import copy
import random
from typing import List
from collections import Counter

class Hat:
    def __init__(self, **kwargs):
        color_dict = dict(kwargs)
        self.contents = [i for i in color_dict for _ in range(color_dict[i])]

    def draw(self, number_of_balls:int) -> List[str]:
        """Performs a random draw of x number of balls without replacement.

        Args:
            number_of_balls (int): The number of balls to draw.

        Returns:
            List[str]: List of balls removed in the draw.
        """
        removed_balls = []
        if number_of_balls>len(self.contents):
            return self.contents
        for i in range(number_of_balls):
            ix = random.randint(0, len(self.contents)-1)
            removed_balls.append(self.contents[ix])
            self.contents.pop(ix)
        return removed_balls

def experiment(hat:Hat, expected_balls:dict, num_balls_drawn:int, num_experiments:int) -> float:
    """Runs an experiment in which a balls are randomly removed from the Hat object a given number of times and returns the probability of reaching the expected numbers of balls.

    Args:
        hat (Hat): Hat object with chosen numbers and colors of balls.
        expected_balls (dict): Frequency of balls by color for which to calculate a probability
        num_balls_drawn (int): Number of balls to remove at each draw
        num_experiments (int): Number of times to replicate the experiment

    Returns:
        float: Probability of drawing at least the given number of balls of each color.
    """
    # Create a empty result and verify lists to append results to.
    result = []
    verify = []
    # Repeats the experiment the given number of times
    for _ in range(num_experiments):
        # Create a deep copy of the provided object so as not to alter its initial instance
        hat_copy = copy.deepcopy(hat)
        # For each replication, add a counted list to the result list.
        # The counted list includes the number of balls drawn for each color drawn.
        result.append(Counter(hat_copy.draw(num_balls_drawn)))
        # Then, append to the verify list a boolean indicating if the numbers of expected balls and colors were drawn.
        verify.append(all([expected_balls[c]<=result[-1][c] for c in expected_balls]))
    # Calculate probability by summing the verify list (total number of cases where the correct numbers were drawn) and dividing by its length (number of experiments)
    return sum(verify)/len(verify)

