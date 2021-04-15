import csv


class Exporter:
    """
    Convert channel objects to CSV data and write to file object.
    """

    def __init__(self, fh, sparse=False):
        self.sparse = sparse
        self.csvwriter = csv.writer(fh, lineterminator="\n")

        # Write header
        self.writerow(
            [
                "Channel",
                "Name",
                "Frequency",
                "Modulation",
                "CTCSS/DCS",
                "Delay",
                "Lockout",
                "Priority",
            ]
        )

    def writerow(self, row=None):
        self.csvwriter.writerow(row or [])

    def write(self, channels):
        # Iterate over all banks
        for bank in range(1, 11):
            bankheader = False

            for index in range(bank * 50 - 49, bank * 50 + 1):
                if index not in channels:
                    continue

                if not bankheader:
                    self.writerow()
                    self.writerow(["# Bank %d" % bank])
                    bankheader = True

                channel = channels[index]

                if not channel:
                    self.writerow([index])
                    continue

                if channel.lockout:
                    lockout = "yes"
                elif self.sparse:
                    lockout = ""
                else:
                    lockout = "no"

                if channel.priority:
                    priority = "yes"
                elif self.sparse:
                    priority = ""
                else:
                    priority = "no"

                self.writerow(
                    [
                        channel.index,
                        channel.name,
                        channel.frequency,
                        channel.modulation,
                        ""
                        if channel.tqcode == 0 and self.sparse
                        else channel.tq,
                        channel.delay,
                        lockout,
                        priority,
                    ]
                )
