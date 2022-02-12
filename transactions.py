class Transaction:
    def __init__(self, date, amount, desc, trans_id, trans_type):
        self.date = date
        self.amount = amount
        self.desc = desc
        self.trans_id = trans_id

    def __repre__(self):
        return "Transaction('{}', '{}', '{}', '{}', '{}', '{}')".format(self.date, self.amount, self.desc, self.trans_id, self.trans_type)
