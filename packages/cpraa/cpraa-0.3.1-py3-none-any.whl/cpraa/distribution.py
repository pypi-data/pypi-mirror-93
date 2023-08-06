from typing import Dict, Any, List

from DPGM import Node
from assignments import Assignment
import assignments as asg


class Distribution:

    def __init__(self, distribution: Dict[Assignment, Any], all_nodes: List[Node]):
        self.all_nodes = all_nodes
        self.distribution = distribution

    def get_assignment_probability(self, a: Assignment):
        return self.distribution[a]

    def get_marginal_probability(self, node: Node):
        probability = 0
        for assignment in asg.get_node_assignments(node, self.all_nodes):
            probability += self.get_assignment_probability(assignment)
        return probability

    def print_assignment_prob(self, nodes=None, only_positive=False, printer=print):
        """
        Print distribution over the assignments of the given nodes or all nodes if no list is given.
        If the only_positive flag is set, only the assignments with probability greater than zero are outputted.
        """
        if not nodes:
            nodes = self.all_nodes
            node_assignments = asg.generate(nodes)
        else:
            node_assignments = self.distribution.keys()
        for assignment in node_assignments:
            value = self.get_assignment_probability(assignment)
            if not only_positive or value > 0:
                asg.print_assignment_prob(assignment, value, printer=printer)

    def print_formatted(self, format_string: str, printer=print):
        """
        Print distribution given by in the formats specified by the format string: (M) marginal node probabilities,
        (F) full distribution, (S) support of distribution.
        """
        for char in format_string:
            if char == "M":
                for node in self.all_nodes:
                    printer("P(" + str(node.name) + ") = " + str(self.get_marginal_probability(node)))
            elif char == "F":
                self.print_assignment_prob(printer=printer)
            elif char == "S":
                printer("Support:")
                self.print_assignment_prob(only_positive=True, printer=printer)
            elif char == "Z":
                printer("No Z3 model available.")
                self.print_assignment_prob(printer=printer)
            elif char == "T":
                printer("No Z3 model available, thus no SMT2 format as well.")
                self.print_assignment_prob(printer=printer)
            else:
                printer("Unknown distribution format '" + char + "'.")
                self.print_assignment_prob(printer=printer)
