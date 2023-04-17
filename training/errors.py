class QuizNotFoundError(Exception):
    pass


class IncompleteQuizResponseError(Exception):
    def __init__(self, missing_responses):
        self.missing_responses = missing_responses
        super().__init__()
