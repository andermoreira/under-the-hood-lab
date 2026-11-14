"""Deterministic scheduler invariants, including fair distribution."""
import unittest
from b07_scheduler import schedule, schedule_ready

class SchedulerProperties(unittest.TestCase):
    def test_round_robin_exact_trace_across_quantums(self):
        for ticks in range(0, 31):
            with self.subTest(ticks=ticks):
                self.assertEqual(schedule(["A", "B", "C"], ticks),
                                 ["A", "B", "C"] * (ticks // 3) + ["A", "B", "C"][:ticks % 3])

    def test_fairness_bound(self):
        for ticks in range(0, 101):
            trace = schedule(["A", "B", "C", "D"], ticks)
            counts = [trace.count(task) for task in ("A", "B", "C", "D")]
            self.assertLessEqual(max(counts) - min(counts), 1)

    def test_blocked_task_never_scheduled(self):
        trace = schedule_ready(["A", "B", "C"], {"B"}, 30)
        self.assertEqual(trace, ["A", "C"] * 15)

    def test_all_blocked_returns_empty(self):
        self.assertEqual(schedule_ready(["A", "B"], {"A", "B"}, 10), [])

    def test_single_task_does_not_starve(self):
        self.assertEqual(schedule(["only"], 20), ["only"] * 20)

if __name__ == "__main__":
    unittest.main()
