from collections import defaultdict
class Solution:
    def invalidTransactions(self, transactions: list[str]) -> list[str]:
        '''
        O(n2)

        valid_transactions = defaultdict(list)
        invalid_idx = set()
        for index, transaction in enumerate(transactions):
            if len(transaction.split(",")) == 4:
                name, time, amount, city = transaction.split(",")
                time, amount = int(time), int(amount)
                if amount > 1000:
                    invalid_idx.add(index)
                for prev_time, prev_amount, prev_city, prev_index in valid_transactions[name]:
                    if abs(time - prev_time) <=60 and prev_city != city:
                        invalid_idx.add(prev_index)
                        invalid_idx.add(index)
            valid_transactions[name].append((time,amount,city, index))
        return [transactions[i] for i in invalid_idx]
        '''
        valid_transactions = defaultdict(list)
        invalid_idx = set()
        for index, transaction in enumerate(transactions):
            if len(transaction.split(",")) == 4:
                name, time, amount, city = transaction.split(",")
                time, amount = int(time), int(amount)
                if amount > 1000:
                    invalid_idx.add(index)
            valid_transactions[name].append((time, amount, city, index))
        for key, value in valid_transactions.items():
            value.sort()
            for i in range(len(value)):
                time_i, amount_i, city_i, idx_i = value[i]
                for j in range(i + 1, len(value)):
                    time_j, amount_j, city_j, idx_j = value[j]
                    if time_j - time_i > 60:  # we need transaction within 60 minutes. More than 60 is valid transaction
                        break
                    if city_i != city_j:
                        invalid_idx.add(idx_i)
                        invalid_idx.add(idx_j)
        return [transactions[i] for i in invalid_idx]


def test_invalid_transactions():
    obj = Solution()
    assert set(obj.invalidTransactions(["alice,10,1000,ottawa", "alice,10,1200,toronto"])) == {
        "alice,10,1000,ottawa",
        "alice,10,1200,toronto",
    }
test_invalid_transactions()