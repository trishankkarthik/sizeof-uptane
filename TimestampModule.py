#!/usr/bin/env python3

# 2nd-party imports.
import CommonModule
import MetadataModule

def Timestamp():
  '''https://github.com/uptane/asn1/blob/master/TimestampModule.asn1'''

  filename = CommonModule.FILENAME_SIZE_IN_BYTES
  version = CommonModule.VERSION_SIZE_IN_BYTES
  length = CommonModule.LENGTH_SIZE_IN_BYTES
  numberOfHashes = CommonModule.LENGTH_SIZE_IN_BYTES
  hashes = CommonModule.Hashes()

  timestamp = filename + version + length + numberOfHashes + hashes
  return timestamp

def TimestampMetadata(num_of_keys=1):
  timestampMetadata = Timestamp()
  CommonModule.log('timestampMetadata', timestampMetadata)
  return MetadataModule.Metadata(timestampMetadata, num_of_keys=num_of_keys)
