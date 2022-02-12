class Transaction:
    def __init__(self, date, amount, category, trans_id, trans_type):
        self.date = date
        self.amount = amount
        self.category = category
        self.trans_id = trans_id
        self.trans_type = trans_type

    def __repr__(self):
        return "Transaction('{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(self.date, self.amount, self.category, self.trans_id, self.trans_type)
