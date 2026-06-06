class Statistics:

    def __init__(self):

        self.ok_count = 0
        self.ng_count = 0

    def add_result(self, result):

        if result == "OK":

            self.ok_count += 1

        else:

            self.ng_count += 1

    @property
    def total(self):

        return (
            self.ok_count +
            self.ng_count
        )

    @property
    def yield_percent(self):

        if self.total == 0:

            return 0

        return (
            self.ok_count /
            self.total
        ) * 100