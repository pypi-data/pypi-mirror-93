from cubicweb.devtools.testlib import CubicWebTC


class PeriodicallyResetCounterTC(CubicWebTC):
    def setup_database(self):
        req = self.request()
        self.counter = req.create_entity("PeriodicallyResetCounter")

    def test(self):
        self.assertEqual(self.counter.initial_value, 0)
        self.assertEqual(self.counter.increment, 1)
        self.assertEqual(self.counter.reset_every, "year")
        entity = self.session.entity_from_eid(self.counter.eid)
        self.assertEqual(entity.next_value(), 1)
        self.assertEqual(entity.next_value(), 2)
        self.rollback()
        self.assertEqual(entity.next_value(), 1)


if __name__ == "__main__":
    from logilab.common.testlib import unittest_main

    unittest_main()
