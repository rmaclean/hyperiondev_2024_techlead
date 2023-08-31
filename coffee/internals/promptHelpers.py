from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.validation import Validator, ValidationError

yes_no_word_completer = WordCompleter(["y", "n"])
range_completer = WordCompleter(["1", "2", "3"])


class YesNoValidator(Validator):
    def validate(self, document):
        text = document.text

        if not (text == "y" or text == "n"):
            raise ValidationError(message="Please enter only y or n", cursor_position=0)


class RangeValidator(Validator):
    def validate(self, document):
        text = document.text

        if text:
            if not text.isdigit():
                raise ValidationError(
                    message="This input contains non-numeric characters",
                    cursor_position=0,
                )
            else:
                number = int(text)
                if not (number == 1 or number == 2 or number == 3):
                    raise ValidationError(
                        message="Invalid number, please enter only 1, 2 or 3",
                        cursor_position=0,
                    )


def prompt_yn(message):
    return prompt(
        f"{message} (y/n) ", completer=yes_no_word_completer, validator=YesNoValidator()
    )


def prompt_range(message):
    return prompt(
        f"{message} (1, 2, or 3) ",
        completer=range_completer,
        validator=RangeValidator(),
    )
