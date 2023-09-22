import operator

ESCAPE = "\\"


def _find_all(text, substring):
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


def generate(_template, _features=None, **kwargs):
    errors = []
    if _features is None:
        _features = [
            "if", "eval"
        ]
    text = _template

    if "if" in _features:
        # evaluate if statements
        indices_open = _find_all(text, "{?")
        indices_close = _find_all(text, "?}")
        indices_delimiter = _find_all(text, "|")
        while len(indices_open) > 0:
            indices_list = [(index, "{?") for index in indices_open] + [(index, "?}") for index in indices_close] + [
                (index, "|") for index in indices_delimiter]
            indices_list.sort(key=operator.itemgetter(0))
            if len(indices_open) != len(indices_close):
                errors.append("Number of {? and ?} does not match")
            if indices_list[0][1] != "{?":
                errors.append("First statement is not an if statement opening")
            # find first opening if statement
            index_open = indices_open[0]
            # find corresponding closing if statement and delimiters
            level = 1
            index = 1
            delimiters = []
            while level > 0 and index < len(indices_list):
                if indices_list[index][1] == "{?":
                    level += 1
                elif indices_list[index][1] == "?}":
                    level -= 1
                elif indices_list[index][1] == "|":
                    if level == 1:
                        delimiters.append(indices_list[index][0])
                index += 1
            if len(delimiters) == 0 or len(delimiters) > 2:
                errors.append("If statement at index {} has no or more than 2 delimiters".format(index_open))
            condition_statement = text[index_open + 2:delimiters[0]].strip()
            then_statement = text[delimiters[0] + 1:delimiters[1]].strip() \
                if len(delimiters) == 2 else text[delimiters[0] + 1:].strip()
            else_statement = text[delimiters[1] + 1:].strip() if len(delimiters) == 2 else ""
            # replace relevant of the statement
            if eval(condition_statement, kwargs):
                text = text[:index_open] + then_statement + text[indices_close[0] + 2:]
            elif else_statement != "":
                text = text[:index_open] + else_statement + text[indices_close[0] + 2:]
            # recompute indices
            indices_open = _find_all(text, "{?")
            indices_close = _find_all(text, "?}")
            indices_delimiter = _find_all(text, "|")

    if "eval" in _features:
        # evaluate eval statements
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

    if len(errors) > 0:
        raise ValueError("There are {} errors: \n".format(len(errors)) + "\n".join(errors))
    return text


class User:
    name: str

    def __init__(self, name):
        self.name = name


if __name__ == "__main__":
    print(generate(
        "{? x > 5 | x is greater than 5 | x is less than 5 ?}, Also der "
        "Name des Teilnehmers ist {{user}}", x=2, user="Hans-Dieter"
    ))
