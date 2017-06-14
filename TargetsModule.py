#!/usr/bin/env python3

# 1st-party imports.
import logging

# 2nd-party imports.
import CommonModule
import MetadataModule

def Target():
  '''https://github.com/uptane/asn1/blob/master/TargetsModule.asn1'''

  filename = CommonModule.FILENAME_SIZE_IN_BYTES
  length = CommonModule.LENGTH_SIZE_IN_BYTES
  numberOfHashes = CommonModule.LENGTH_SIZE_IN_BYTES
  hashes = CommonModule.Hashes()

  target = filename + length + numberOfHashes + hashes
  CommonModule.log('Target', target)
  return target

def Custom(ecuIdentifier=False, hardwareIdentifier=False, releaseCounter=False):
  custom = 0

  if ecuIdentifier:
    custom += CommonModule.IDENTIFIER_SIZE_IN_BYTES
  if hardwareIdentifier:
    custom += CommonModule.IDENTIFIER_SIZE_IN_BYTES
  if releaseCounter:
    custom += CommonModule.NATURAL_SIZE_IN_BYTES

  CommonModule.log('Custom', custom)
  return custom

def TargetAndCustom(custom=False):
  target = Target()

  if custom:
    custom = Custom(ecuIdentifier=True, hardwareIdentifier=True,
                    releaseCounter=True)
  else:
    custom = 0

  targetAndCustom = target + custom
  CommonModule.log('TargetAndCustom', targetAndCustom)
  return targetAndCustom

def Targets(num_of_targets):
  targets = num_of_targets * TargetAndCustom()
  CommonModule.log('Targets', targets)
  return targets

def TargetsMetadata(num_of_keys=1, num_of_targets=1):
  targets = Targets(num_of_targets)
  return MetadataModule.Metadata(targets, num_of_keys=num_of_keys)
