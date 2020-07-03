import neat

def vprint(verbosity: int, content: Object) -> None:
    if verbosity <= neat.verbosity:
        print(content)
