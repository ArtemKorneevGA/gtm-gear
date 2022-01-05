def camel_case(snake):
    if not snake:
        return snake
    if "_" in snake:
        words = snake.split("_")
        res = ''
        for i in range(len(words)):
            res += words[i].lower() if i == 0 else words[i].capitalize()
        return res
    if snake == snake.upper():
        return snake.lower()
    return snake