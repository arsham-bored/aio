def to_k(number: int):
    number = int(number)

    if number >= 1_000_000:
        return f"{int(number/1000000)}M"

    if number >= 1_000:
        return f"{int(number/1000)}K"

    return number