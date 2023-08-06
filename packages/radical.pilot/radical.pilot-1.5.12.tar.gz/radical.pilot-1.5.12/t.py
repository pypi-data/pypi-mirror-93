#!/usr/bin/env python3

import radical.utils as ru
cfg=ru.Config("radical.pilot.resource", name="*")
for site in cfg:
    for r in cfg[site]:
        try:
            print("%-15s %-25s  %-15s %-15s" % (site, r,
                                                cfg[site][r]['task_launch_method'],
                                                cfg[site][r]['mpi_launch_method']))
        except:
            print("%-15s %-15s" % (site, r))


