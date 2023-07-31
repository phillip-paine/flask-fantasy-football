from dataclasses import dataclass


@dataclass
class RunArguments:
    adaption_iterations: int
    iterations: int
