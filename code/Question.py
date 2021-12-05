class Question:
    task = ''
    answers = [{"task":0}]
    # ответ, который дал человек
    result = -1
    def __init__(self, task, answers):
        self.answers = answers
        self.task = task
    