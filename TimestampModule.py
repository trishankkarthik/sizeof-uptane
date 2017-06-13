#!/usr/bin/env python3

# 1st-party imports.
import logging

# 2nd-party imports.
import CommonModule

def Timestamp():
  '''https://github.com/uptane/asn1/blob/master/TimestampModule.asn1'''

  filename = CommonModule.FILENAME_SIZE_IN_BYTES
  version = CommonModule.VERSION_SIZE_IN_BYTES
  length = CommonModule.LENGTH_SIZE_IN_BYTES
  numberOfHashes = CommonModule.LENGTH_SIZE_IN_BYTES
  hashes = CommonModule.Hashes()

  timestamp = filename + version + length + numberOfHashes + hashes
  CommonModule.log('Timestamp', timestamp)
  return timestamp
