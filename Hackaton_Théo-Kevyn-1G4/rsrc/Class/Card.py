class Card:
    # _____CONSTRUCTEUR_____
    def __init__(self, question=str(), answer=str(), difficulty=int(0)):
        """
        :param question: str
        :param reponse: str
        :param difficulty: int- 0 = none
                                1 = Trop facile
                                2 = Je savais
                                3 = Je ne savais pas
        """
        self.question = question
        self.answer = answer
        self.difficulty = difficulty

    # _____GETTERS_____
    def getQuestion(self):
        return self.question

    def getAnswer(self):
        return self.answer

    def getDifficulty(self):
        return self.difficulty

    # _____SETTERS_____
    def setQuestion(self, question):
        self.question = question

    def setReponse(self, answer):
        self.answer = answer

    def setDifficulty(self, difficulty):
        self.difficulty = difficulty

