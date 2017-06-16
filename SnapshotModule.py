#!/usr/bin/env python3

# 2nd-party imports.
import CommonModule
import MetadataModule

def Snapshot(num_of_targets_metadata_files=1):
  '''https://github.com/uptane/asn1/blob/master/SnapshotModule.asn1'''

  numberOfSnapshotMetadataFiles = CommonModule.LENGTH_SIZE_IN_BYTES
  filename = CommonModule.FILENAME_SIZE_IN_BYTES
  version = CommonModule.VERSION_SIZE_IN_BYTES
  snapshotMetadataFiles = num_of_targets_metadata_files * (filename + version)

  snapshot = numberOfSnapshotMetadataFiles + snapshotMetadataFiles
  return snapshot

# By default, there is only the top-level targets metadata file on a repository.
def SnapshotMetadata(num_of_keys=1, num_of_targets_metadata_files=1):
  snapshotMetadata = Snapshot(num_of_targets_metadata_files=\
                              num_of_targets_metadata_files)
  CommonModule.log('snapshotMetadata', snapshotMetadata)
  return MetadataModule.Metadata(snapshotMetadata, num_of_keys=num_of_keys)
