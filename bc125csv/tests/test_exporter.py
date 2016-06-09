from bc125csv import main
from bc125csv.tests.base import BaseTestCase, mock, builtins


class ExporterTestCase(BaseTestCase):
    def test_export(self):
        """
        Normal export of all channels.
        """
        main(["export", "-n"])
        self.assertStdOut(EXPORT)

    def test_export_sparse(self):
        """
        Sparse export of all channels.
        """
        main(["export", "-n", "-s"])
        self.assertStdOut(EXPORT_SPARSE)

    def test_export_sparse_bank2(self):
        """
        Sparse export of bank 2.
        """
        main(["export", "-n", "-s", "-b", "2"])
        self.assertStdOut(EXPORT_BANK2)

    def test_export_sparse_bank2_empty(self):
        """
        Sparse export of bank 2 including empty channels.
        """
        main(["export", "-n", "-s", "-b", "2", "-e"])
        self.assertStdOut(EXPORT_BANK2_EMPTY)

    def test_export_bank13(self):
        """
        Export of bank 13 (non-existing).
        """
        with self.assertRaises(SystemExit) as cm:
            main(["export", "-n", "-b", "13"])
        self.assertNotEqual(cm.exception.code, None)

    def test_export_outfile(self):
        """
        Write export to file.
        """
        with mock.patch.object(builtins, "open", mock.mock_open()):
            main(["export", "-n", "-s", "-o", "output.csv"])

        with self.assertRaises(SystemExit) as cm:
            main(["export", "-n", "-s", "-o", "/path/that/does/not/exist/output.csv"])
        self.assertNotEqual(cm.exception.code, None)



EXPORT = """Channel,Name,Frequency,Modulation,CTCSS/DCS,Delay,Lockout,Priority

# Bank 1
1,Channel 1,101.0000,FM,none,2,no,no
2,Channel 2,102.0000,FM,none,2,no,no
3,Channel 3,103.0000,FM,none,2,no,no
4,Channel 4,104.0000,FM,none,2,no,no
5,Channel 5,105.0000,FM,none,2,no,no
6,Channel 6,106.0000,FM,none,2,no,no
7,Channel 7,107.0000,FM,none,2,no,no
8,Channel 8,108.0000,FM,none,2,no,no
9,Channel 9,109.0000,FM,none,2,no,no
10,Channel 10,110.0000,FM,none,2,no,no
11,Channel 11,111.0000,FM,none,2,no,no
12,Channel 12,112.0000,FM,none,2,no,no
13,Channel 13,113.0000,FM,none,2,no,no
14,Channel 14,114.0000,FM,none,2,no,no
15,Channel 15,115.0000,FM,none,2,no,yes
16,Channel 16,116.0000,FM,none,2,no,no
17,Channel 17,117.0000,FM,none,2,no,no
18,Channel 18,118.0000,FM,none,2,no,no
19,Channel 19,119.0000,FM,none,2,no,no

# Bank 2
51,Channel 51,151.0000,FM,none,2,no,no
52,Channel 52,152.0000,FM,none,2,no,no
53,Channel 53,153.0000,FM,none,2,no,no
54,Channel 54,154.0000,FM,none,2,no,no
55,Channel 55,155.0000,FM,none,2,yes,no
56,Channel 56,156.0000,FM,none,2,no,no
57,Channel 57,157.0000,FM,none,2,no,no
58,Channel 58,158.0000,FM,none,2,no,no
59,Channel 59,159.0000,FM,none,2,no,no
"""

EXPORT_SPARSE = """Channel,Name,Frequency,Modulation,CTCSS/DCS,Delay,Lockout,Priority

# Bank 1
1,Channel 1,101.0000,FM,,2,,
2,Channel 2,102.0000,FM,,2,,
3,Channel 3,103.0000,FM,,2,,
4,Channel 4,104.0000,FM,,2,,
5,Channel 5,105.0000,FM,,2,,
6,Channel 6,106.0000,FM,,2,,
7,Channel 7,107.0000,FM,,2,,
8,Channel 8,108.0000,FM,,2,,
9,Channel 9,109.0000,FM,,2,,
10,Channel 10,110.0000,FM,,2,,
11,Channel 11,111.0000,FM,,2,,
12,Channel 12,112.0000,FM,,2,,
13,Channel 13,113.0000,FM,,2,,
14,Channel 14,114.0000,FM,,2,,
15,Channel 15,115.0000,FM,,2,,yes
16,Channel 16,116.0000,FM,,2,,
17,Channel 17,117.0000,FM,,2,,
18,Channel 18,118.0000,FM,,2,,
19,Channel 19,119.0000,FM,,2,,

# Bank 2
51,Channel 51,151.0000,FM,,2,,
52,Channel 52,152.0000,FM,,2,,
53,Channel 53,153.0000,FM,,2,,
54,Channel 54,154.0000,FM,,2,,
55,Channel 55,155.0000,FM,,2,yes,
56,Channel 56,156.0000,FM,,2,,
57,Channel 57,157.0000,FM,,2,,
58,Channel 58,158.0000,FM,,2,,
59,Channel 59,159.0000,FM,,2,,
"""

EXPORT_BANK2 = """Channel,Name,Frequency,Modulation,CTCSS/DCS,Delay,Lockout,Priority

# Bank 2
51,Channel 51,151.0000,FM,,2,,
52,Channel 52,152.0000,FM,,2,,
53,Channel 53,153.0000,FM,,2,,
54,Channel 54,154.0000,FM,,2,,
55,Channel 55,155.0000,FM,,2,yes,
56,Channel 56,156.0000,FM,,2,,
57,Channel 57,157.0000,FM,,2,,
58,Channel 58,158.0000,FM,,2,,
59,Channel 59,159.0000,FM,,2,,
"""

EXPORT_BANK2_EMPTY = """Channel,Name,Frequency,Modulation,CTCSS/DCS,Delay,Lockout,Priority

# Bank 2
51,Channel 51,151.0000,FM,,2,,
52,Channel 52,152.0000,FM,,2,,
53,Channel 53,153.0000,FM,,2,,
54,Channel 54,154.0000,FM,,2,,
55,Channel 55,155.0000,FM,,2,yes,
56,Channel 56,156.0000,FM,,2,,
57,Channel 57,157.0000,FM,,2,,
58,Channel 58,158.0000,FM,,2,,
59,Channel 59,159.0000,FM,,2,,
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
85
86
87
88
89
90
91
92
93
94
95
96
97
98
99
100
"""
