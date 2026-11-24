import unittest

class ReconcileEvents:

    REQUIRED_KEYS = {
        "event_id",
        "account_id",
        "timestamp",
        "type",
        "amount_cents",
    }
    VALID_TYPES = {"posted", "pending", "reversal"}

    def _is_strict_int(self, val) -> bool:
        return isinstance(val, int) and not isinstance(val,bool)

    def _is_not_empty_str(self, val) -> bool:
        return isinstance(val, str) and len(val.strip()) > 0

    def _is_valid(self, event) -> bool:
        # we need all required keys
        if not isinstance(event, dict):
            return False
        for key in self.REQUIRED_KEYS:
            if key not in event:
                return False
        # valuidate IDs are not empty strings
        if not self._is_not_empty_str(event["event_id"]):
            return False
        if not self._is_not_empty_str(event["account_id"]):
            return False
        if not self._is_strict_int(event["timestamp"]):
            return False
        if not self._is_strict_int(event["amount_cents"]):
            return False

        event_type = event["type"]
        if event_type not in self.VALID_TYPES:
            return False
        if event_type == "reversal" and event["amount_cents"] == 0:
            return False
        return True

    def reconcile_vents(self, events):
        seen_ids = set()  # we need this to by pass the duplicate entries
        clean_events = []
        for arrival_index, event in enumerate(events): # O(n)
            if not self._is_valid(event):
                continue
            if event["event_id"] not in seen_ids:
                seen_ids.add(event["event_id"])
                clean_events.append((event["timestamp"],arrival_index, event))


        clean_events.sort() # O(nlogn)
        result = {}
        applied_amounts = {}
        for _,_,event in clean_events:
            account_id = event["account_id"]
            if "replaces_pending_id" in event:
                replace_id = event["replaces_pending_id"]
                if replace_id in applied_amounts:
                    result[account_id] = result.get(account_id, 0) - applied_amounts.pop(replace_id)
                result[account_id] = result.get(account_id,0) + event["amount_cents"]
                applied_amounts[event["event_id"]] = event["amount_cents"]
        return result


class TestReconcileEvents(unittest.TestCase):
    def setUp(self):
        self.reconciler = ReconcileEvents()
    def test_reconcile_events(self):
        events = [
            {
                "event_id": "evt_1001",
                "account_id": "acct_alpha",
                "timestamp": 1732050000,
                "type": "posted",
                "amount_cents": 50000,
            },
            {
                "event_id": "evt_1002",
                "account_id": "acct_alpha",
                "timestamp": 1732050300,
                "type": "pending",
                "amount_cents": -12500,
            },
            # Duplicate retry of evt_1002 -> ignored
            {
                "event_id": "evt_1002",
                "account_id": "acct_alpha",
                "timestamp": 1732050300,
                "type": "pending",
                "amount_cents": -12500,
            },
            # Out-of-order earlier event
            {
                "event_id": "evt_1003",
                "account_id": "acct_alpha",
                "timestamp": 1732050150,
                "type": "posted",
                "amount_cents": -4500,
            },
            # Non-zero reversal
            {
                "event_id": "evt_1004",
                "account_id": "acct_alpha",
                "timestamp": 1732050600,
                "type": "reversal",
                "amount_cents": 12500,
            },
            # Separate account
            {
                "event_id": "evt_2001",
                "account_id": "acct_beta",
                "timestamp": 1732050400,
                "type": "posted",
                "amount_cents": 10000,
            },
        ]
        self.assertEqual(self.reconciler.reconcile_vents(events), {"acct_alpha": 45500, "acct_beta": 10000},)

    def test_ignores_malformed_and_zero_reversals(self):
        events = [
            None,
            "not_a_dict",
            {"event_id": "missing_fields"},
            {
                "event_id": "",
                "account_id": "acct_1",
                "timestamp": 100,
                "type": "posted",
                "amount_cents": 1000,
            },
            {
                "event_id": "bad_bool",
                "account_id": "acct_1",
                "timestamp": 100,
                "type": "posted",
                "amount_cents": True,
            },
            {
                "event_id": "bad_str_amt",
                "account_id": "acct_1",
                "timestamp": 100,
                "type": "posted",
                "amount_cents": "500",
            },
            {
                "event_id": "unknown_type",
                "account_id": "acct_1",
                "timestamp": 100,
                "type": "wire",
                "amount_cents": 500,
            },
            {
                "event_id": "zero_rev",
                "account_id": "acct_1",
                "timestamp": 100,
                "type": "reversal",
                "amount_cents": 0,
            },
        ]
        self.assertEqual(self.reconciler.reconcile_vents(events), {})

    def test_negative_balance_allowed(self):
        events = [
            {
                "event_id": "e1",
                "account_id": "acct_neg",
                "timestamp": 100,
                "type": "reversal",
                "amount_cents": -2500,
            }
        ]
        self.assertEqual(
            self.reconciler.reconcile_vents(events), {"acct_neg": -2500}
        )

    if __name__ == "__main__":
        unittest.main()













