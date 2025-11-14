# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in search_agents.py).
"""

from builtins import object
import util
import os
from util import Stack, Queue, PriorityQueue


def tiny_maze_search(problem):
    """
    Returns a sequence of moves that solves tiny_maze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tiny_maze.
    """
    from game import Directions

    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depth_first_search(problem):
    
    # What does this function need to return?
    #     list of actions (actions shown below) that reaches the goal
    # 
    # What data is available?
    #     start_state = problem.get_start_state() # returns a string
    # 
    #     problem.is_goal_state(start_state) # returns boolean
    # 
    #     transitions = problem.get_successors(start_state)
    #     transitions[0].state
    #     transitions[0].action
    #     transitions[0].cost
    # 
    #     print(transitions) # would look like the list-of-lists on the next line
    #     [
    #         [ "B", "0:A->B", 1.0, ],
    #         [ "C", "1:A->C", 2.0, ],
    #         [ "D", "2:A->D", 4.0, ],
    #     ]
    # 
    # Example:
    #     start_state = problem.get_start_state()
    #     transitions = problem.get_successors(start_state)
    #     example_path = [  transitions[0].action  ]
    #     path_cost = problem.get_cost_of_actions(example_path)
    #     return example_path
    
    stack = Stack()
    start = problem.get_start_state()
    stack.push((start, []))
    visited = set()

    while not stack.is_empty():
        state, path = stack.pop()

        if state in visited:
            continue
        visited.add(state)

        if problem.is_goal_state(state):
            return path

        for succ, action, cost in problem.get_successors(state):
            if succ not in visited:
                stack.push((succ, path + [action]))

    return []


def breadth_first_search(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    queue = Queue()
    start = problem.get_start_state()
    queue.push((start, []))
    visited = set()

    while not queue.is_empty():
        state, path = queue.pop()

        if state in visited:
            continue
        visited.add(state)

        if problem.is_goal_state(state):
            return path

        for succ, action, cost in problem.get_successors(state):
            if succ not in visited:
                queue.push((succ, path + [action]))

    return []


def uniform_cost_search(problem, heuristic=None):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    pq = PriorityQueue()
    start = problem.get_start_state()
    pq.push((start, [], 0), 0)

    best_cost = {start: 0}

    while not pq.is_empty():
        state, path, cost_so_far = pq.pop()

        if problem.is_goal_state(state):
            return path

        if cost_so_far > best_cost.get(state, float("inf")):
            continue

        for succ, action, step_cost in problem.get_successors(state):
            new_cost = cost_so_far + step_cost

            if new_cost < best_cost.get(succ, float("inf")):
                best_cost[succ] = new_cost
                pq.push((succ, path + [action], new_cost), new_cost)

    return []


# 
# heuristics
# 
def a_really_really_bad_heuristic(position, problem):
    from random import random, sample, choices
    return int(random()*1000)

def null_heuristic(state, problem=None):
    return 0

def your_heuristic(state, problem=None):
    from search_agents import FoodSearchProblem
    
    # 
    # heuristic for the find-the-goal problem
    # 
    if isinstance(problem, SearchProblem):
        # data
        pacman_x, pacman_y = state
        goal_x, goal_y     = problem.goal
        
        # YOUR CODE HERE (set value of optimisitic_number_of_steps_to_goal)
        
        optimisitic_number_of_steps_to_goal = abs(pacman_x - goal_x) + abs(pacman_y - goal_y)
        return optimisitic_number_of_steps_to_goal
    # 
    # traveling-salesman problem (collect multiple food pellets)
    # 
    elif isinstance(problem, FoodSearchProblem):
        # the state includes a grid of where the food is (problem isn't ter)
        position, food_grid = state
        pacman_x, pacman_y = position
        
        # YOUR CODE HERE (set value of optimisitic_number_of_steps_to_goal)
        
        food_positions = food_grid.as_list()
        if not food_positions:
            optimisitic_number_of_steps_to_goal = 0
        else:
            optimisitic_number_of_steps_to_goal = min(
                abs(pacman_x - fx) + abs(pacman_y - fy)
                for fx, fy in food_positions
            )
        return optimisitic_number_of_steps_to_goal
manhattanHeuristic = your_heuristic


def a_star_search(problem, heuristic=your_heuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    
    # 
    # NOTE: the `heuristic` argument above is a function. 
    # you can call it just like any other function
    # for example:
    #     state = YOUR CODE HERE       # (see comments in depth_first_search above)
    #     priority = depth + heuristic(state, problem)
    #
    
    pq = PriorityQueue()
    start = problem.get_start_state()
    start_cost = 0
    pq.push((start, [], start_cost), start_cost + heuristic(start, problem))

    best_cost = {start: 0}

    while not pq.is_empty():
        state, path, cost_so_far = pq.pop()

        if problem.is_goal_state(state):
            return path

        if cost_so_far > best_cost.get(state, float("inf")):
            continue

        for succ, action, step_cost in problem.get_successors(state):
            new_cost = cost_so_far + step_cost
            est = new_cost + heuristic(succ, problem)

            if new_cost < best_cost.get(succ, float("inf")):
                best_cost[succ] = new_cost
                pq.push((succ, path + [action], new_cost), est)

    return []


# (you can ignore this, although it might be helpful to know about)
# This is effectively an abstract class
# it should give you an idea of what methods will be available on problem-objects
class SearchProblem(object):
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def get_start_state(self):
        """
        Returns the start state for the search problem.
        """
        util.raise_not_defined()

    def is_goal_state(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raise_not_defined()

    def get_successors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, step_cost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'step_cost' is
        the incremental cost of expanding to that successor.
        """
        util.raise_not_defined()

    def get_cost_of_actions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raise_not_defined()

if os.path.exists("./hidden/search.py"): from hidden.search import *
# fallback on a_star_search
for function in [breadth_first_search, depth_first_search, uniform_cost_search, ]:
    try: function(None)
    except util.NotDefined as error: exec(f"{function.__name__} = a_star_search", globals(), globals())
    except: pass

# Abbreviations
bfs   = breadth_first_search
dfs   = depth_first_search
astar = a_star_search
ucs   = uniform_cost_search