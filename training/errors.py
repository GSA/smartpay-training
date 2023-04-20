class QuizNotFoundError(Exception):
    pass


class IncompleteQuizResponseError(Exception):
    def __init__(self, missing_responses: list[int]):
        self.missing_responses = missing_responses
        super().__init__()
