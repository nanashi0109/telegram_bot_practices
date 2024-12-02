class FeedbackModel:
    def __init__(self, general_impression: str, grade: str, comment: str):
        self.__general_impression = general_impression
        self.__grade = grade
        self.__comment = comment

    @property
    def general_impression(self) -> str:
        return self.__general_impression

    @property
    def grade(self) -> str:
        return self.__grade

    @property
    def comment(self) -> str:
        return self.__comment

    def __str__(self):
        return f"{self.__general_impression}, {self.__grade}, {self.__comment}"

    def get_stats(self):
        result = (f"Общие впечатления: {self.__general_impression} \n"
                  f"Оценка: {self.__grade} \n"
                  f"Комментарий: {self.__comment}")

        return result
