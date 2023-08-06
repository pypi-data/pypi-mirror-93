import unittest

from ...core.testing import DbTestCase
from ..queries import update_schematic_pins_from_libraries, schematic_build_nets_diff_pairs_from_net_names,\
    insert_diff_net_by_query, query_signal_paths, NSerieParts


class TestController(DbTestCase):

    def test_update_schematic_pins_from_libraries(self):
        print(update_schematic_pins_from_libraries(self.session, 1, 1))

    def test_schematic_build_nets_diff_pairs_from_net_names(self):
        print(schematic_build_nets_diff_pairs_from_net_names(self.session, 1))

    def test_insert_diff_net_by_query(self):
        query = schematic_build_nets_diff_pairs_from_net_names(self.session, 1)
        insert_diff_net_by_query(self.session, query)

    def test_build_signal_paths(self):
        stmt = query_signal_paths(self.session, 1, 'U200', ['J800', 'J801', 'J900'], NSerieParts.zero, 3, (1,2,3))
        print(stmt.compile(self.engine, compile_kwargs={"literal_binds": True}))
        # print(query_signal_paths(self.session, 1, 'U200', 'J200', NSerieParts.one, 3))


if __name__ == '__main__':
    unittest.main()
