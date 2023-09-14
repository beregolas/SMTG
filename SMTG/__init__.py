
ESCAPE = "\\"


def find_all(text, substring):
    """
    Returns a list of all indices of the substring in the text.
    """
    indices = []
    index = 0
    while index < len(text):
        index = text.find(substring, index)
        if index == -1:
            break
        if not (index > 0 and text[index - 1] == ESCAPE):
            indices.append(index)
        index += 1
    return indices


def generate(_template, _features=None,  **kwargs):
    errors = []
    if _features is None:
        _features = [
            "if", "eval"
        ]
    text = _template

    if "if" in _features:
        # evaluate if statements
        index = text.find("{?")
        while index != -1:
            if text[index - 1] == ESCAPE:
                index = text.find("{?", index + 1)
                continue

            end_index = text.find("?}", index)
            if end_index == -1:
                errors.append("Missing ?}} for {{? at index {}".format(index))
                break
            while text[end_index - 1] == ESCAPE:
                end_index = text.find("{?", end_index + 1)
                if end_index == -1:
                    errors.append("Missing ?}} for {{? at index {}".format(index))
                    break
                continue

            condition_statement = text[index + 2:end_index].strip()

            try:
                condition, then, *rest = condition_statement.split("|")
            except ValueError:
                errors.append("Invalid if statement at index {}".format(index))
                break

            if eval(condition, kwargs):
                text = text[:index] + then + text[end_index + 2:]
            else:
                if len(rest) > 0:
                    text = text[:index] + rest[0] + text[end_index + 2:]
                else:
                    errors.append("Missing else statement for {{? at index {}".format(index))

        pass

    if "eval" in _features:
        #evaluate eval statements
        index = text.find("{{")
        while index != -1:
            if text[index - 1] == ESCAPE:
                index = text.find("{{", index + 1)
                continue

            end_index = text.find("}}", index)
            if end_index == -1:
                errors.append("Missing }} for {{ at index {}".format(index))
                break
            while text[end_index - 1] == ESCAPE:
                end_index = text.find("{{", end_index + 1)
                if end_index == -1:
                    errors.append("Missing }} for {{ at index {}".format(index))
                    break
                continue

            eval_statement = text[index + 2:end_index].strip()
            try:
                text = text[:index] + str(eval(eval_statement, {}, kwargs)) + text[end_index + 2:]
            except Exception as e:
                errors.append("Invalid eval statement at index {}: {}".format(index, str(e)))
                break
        pass

    print(errors)
    return text


class User:
    name: str

    def __init__(self, name):
        self.name = name


if __name__ == "__main__":
    print(generate(
        "{? x > 5 | x is greater than 5 | x is less than 5 ?}, Also der Name des Teilnehmers ist {{user.name}}", x=2, user=User(name="Hans")
    ))