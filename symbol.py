class Symbol:
    table = {}
    @staticmethod
    def get_symbol(id):
        return Symbol.table.get(id, None)

    def __init__(self, name):
        self.name = name
