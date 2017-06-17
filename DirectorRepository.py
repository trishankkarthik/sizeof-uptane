#!/usr/bin/env python3

# 2nd-party imports.
import CommonModule
import TimestampModule
import SnapshotModule
import TargetsModule

def Bundle(num_of_ecus=1):
  '''Director signs fresh top-level timestamp, snapshot, and targets metadata.'''

  # The top-level targets role signs a target, together with custom metadata,
  # for each ECU.
  # This role uses one signing key.
  # There is no delegation whatsoever.
  bundle = TargetsModule.\
           TargetsMetadata(custom=True,
                           num_of_keys=1,
                           num_of_targets=num_of_ecus,
                           num_of_delegations=0,
                           num_of_keys_per_delegation=0,
                           num_of_paths_per_delegation=0,
                           num_of_roles_per_delegation=0)
  bundle += SnapshotModule.SnapshotMetadata()
  bundle += TimestampModule.TimestampMetadata()

  CommonModule.log('# of ECUs', num_of_ecus, unit=' ECUs')
  CommonModule.log('Bundle', bundle)
  return bundle

if __name__ == '__main__':
  # Worst-case scenario.
  CommonModule.time(CommonModule.iso_tp_overhead(Bundle(num_of_ecus=100)))
