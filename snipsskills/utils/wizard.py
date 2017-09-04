class Wizard(object):
    def __init__(self):
        self.questions = list()

    def add_question(self, text, description, input_function, input_validation, default_value=None):
        question = Question(text=text, description=description, input_function=input_function,
                            input_validation=input_validation, default_value=default_value)
        self.questions.append(question)

    def run(self):
        return [question.answer() for question in self.questions]


class Question(object):
    def __init__(self, text, description, input_function, input_validation, default_value=None):
        self.text = text
        self.description = description
        self.input_function = input_function
        self.input_validation = input_validation
        self.default_value = default_value

    def answer(self):
        if len(self.description) > 0:
            print self.description

        result = self.input_function(self.text) if self.default_value else self.input_function(self.text,
                                                                                               self.default_value)
        while (not self.input_validation(result)):
            result = self.input_function(self.text) if self.default_value else self.input_function(self.text,
                                                                                                   self.default_val)

        return result
