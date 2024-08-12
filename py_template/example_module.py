def fibonacci(n: int) -> list[int]:
    """
    Example function.

    Parameters
    ----------
    n : int
        Integer term up to which the sequence is calculated

    Returns
    -------
    fib_seq : list[int]
        The Fibonacci sequence up to term `n`
    """
    fib_seq = []

    a, b = 0, 1

    for i in range(n):
        a, b = b, a + b
        fib_seq.append(a)

    return fib_seq


class SoftwareGroup:
    """
    Example class.

    Parameters
    ----------
    people : str
        Group members
    purpose : str
        Group objectives
    """

    def __init__(self, people: str, purpose: str) -> None:
        self.people = people
        self.purpose = purpose
        self.meeting_format = "hack session + office hour + periodic tutorial"

    def long_term_goals(self) -> str:
        research_goal = "develop open-source research software for astronomy"
        community_goal = "improve diversity in astro software positions"
        education_goal = "organize and run astro software workshops"
        cca_goal = "improve software knowledge and practices at CCA"
        return ", ".join(
            [self.purpose, research_goal, community_goal, education_goal, cca_goal]
        )
