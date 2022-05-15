import os


class User:
    def __init__(self, question_num: int):
        self.question_num = question_num
        self.score = 0


class Question:
    ''' содержит вопрос, правильный ответ и три неправильных'''
    def __init__(self, question, right_answer, wrong1, wrong2, wrong3):
        self.question = question
        self.right_answer = right_answer
        self.wrong1 = wrong1
        self.wrong2 = wrong2
        self.wrong3 = wrong3

    @classmethod
    def generate_list_question(cls, file_path: str, header=True):
        if not os.path.exists(file_path):
            raise FileNotFoundError(
                f"Передан не корректный путь до файла {file_path}"
            )
        with open(file_path, "r", encoding="utf-8") as file:
            questions_list = []
            temp = []
            if header:
                header = file.readline()
            for num, line in enumerate(file, start=1):
                temp.append(line.strip())
                if num % 5 == 0:
                    questions_list.append(Question(*temp[-5:]))
            if header:
                return header, questions_list
            return questions_list
