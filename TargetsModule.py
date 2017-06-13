#!/usr/bin/env python3

# 1st-party imports.
import logging

# 2nd-party imports.
import CommonModule

def Target():
  '''https://github.com/uptane/asn1/blob/master/TargetsModule.asn1'''

  filename = CommonModule.FILENAME_SIZE_IN_BYTES
  length = CommonModule.LENGTH_SIZE_IN_BYTES
  numberOfHashes = CommonModule.LENGTH_SIZE_IN_BYTES
  hashes = CommonModule.Hashes()

  target = filename + length + numberOfHashes + hashes
  CommonModule.log('Target', target)
  return target
