class EntryNotFoundException(Exception):
    def __init__(self, id: int, name: str, overwrite: str = '') -> None:
        if overwrite:
            super().__init__(overwrite)
        else:
            super().__init__(f"No {name} entry with id={id} was found")
