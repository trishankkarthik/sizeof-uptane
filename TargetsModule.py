#!/usr/bin/env python3

# 2nd-party imports.
import CommonModule
  
def Target():
  '''https://github.com/uptane/asn1/blob/master/TargetsModule.asn1'''

  filename = CommonModule.FILENAME_SIZE_IN_BYTES
  length = CommonModule.LENGTH_SIZE_IN_BYTES
  numberOfHashes = CommonModule.LENGTH_SIZE_IN_BYTES
  hashes = CommonModule.Hashes()
  return filename + length + numberOfHashes + hashes
