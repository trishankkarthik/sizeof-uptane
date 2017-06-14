#!/usr/bin/env python3

# 1st-party imports.
import logging

# 2nd-party imports.
import CommonModule
import TimestampModule
import SnapshotModule
import TargetsModule

def Bundle(num_of_ecus=1):
  '''Director signs fresh top-level timestamp, snapshot, and targets metadata.'''

  bundle = TargetsModule.TargetsMetadata(num_of_ecus)
  bundle += SnapshotModule.SnapshotMetadata()
  bundle += TimestampModule.TimestampMetadata()

  CommonModule.log('# of ECUs: ', num_of_ecus, unit='')
  CommonModule.log('Bundle', bundle)
  return bundle

if __name__ == '__main__':
  Bundle(128)
