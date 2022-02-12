class Transaction:
    def __init__(self, trans_date, amount, category, trans_id, trans_type):
        self.trans_date = trans_date
        self.amount = amount
        self.category = category
        self.trans_id = trans_id
        self.trans_type = trans_type

    def __repr__(self):
        return "Transaction('{}', '{}', '{}', '{}', '{}', '{}')".format(self.trans_date, self.amount, self.category, self.trans_id, self.trans_type)
