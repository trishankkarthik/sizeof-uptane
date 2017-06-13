#!/usr/bin/env python3

# 1st-party imports.
import logging

# 2nd-party imports.
import CommonModule

def Snapshot(num_of_targets_metadata_files=1):
  '''https://github.com/uptane/asn1/blob/master/SnapshotModule.asn1'''

  numberOfSnapshotMetadataFiles = CommonModule.LENGTH_SIZE_IN_BYTES
  filename = CommonModule.FILENAME_SIZE_IN_BYTES
  version = CommonModule.VERSION_SIZE_IN_BYTES
  snapshotMetadataFiles = num_of_targets_metadata_files * (filename + version)

  snapshot = numberOfSnapshotMetadataFiles + snapshotMetadataFiles
  CommonModule.log('Snapshot', snapshot)
  return snapshot
