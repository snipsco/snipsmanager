from unittest import TestCase

from snipsskills.utils.wizard import Wizard
from snipsskills.utils.os_helpers import ask_yes_no


class BaseTest(TestCase):
    def setUp(self):
        pass


class WizardTest(BaseTest):
    def setUp(self):
        self.wizard = Wizard()
        self.wizard.add_question(text="dummy1",
                                 description="dummy1",
                                 input_function=lambda x: x,
                                 input_validation=lambda x: True)
        self.wizard.add_question(text="dummy2",
                                 description="dummy2",
                                 input_function=lambda x: x,
                                 input_validation=lambda x: True)
        self.wizard.add_question(text="dummy3",
                                 description="dummy3",
                                 input_function=lambda x: x,
                                 input_validation=lambda x: True)

    def test_number_of_questions(self):
        self.assertEqual(len(self.wizard.questions), 3)

    def test_number_of_results(self):
        self.assertEqual(len(self.wizard.run()), 3)

