import neat

def vprint(verbosity: int, content: object) -> None:
    if verbosity <= neat.verbosity:
        print(content)
