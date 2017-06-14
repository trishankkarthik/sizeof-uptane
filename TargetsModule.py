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

def TargetAndCustom(custom=True):
  target = Target()

  if custom:
    custom = Custom(ecuIdentifier=True, hardwareIdentifier=True,
                    releaseCounter=True)
  else:
    custom = 0

  targetAndCustom = target + custom
  CommonModule.log('TargetAndCustom', targetAndCustom)
  return targetAndCustom

def Targets(num_of_targets, custom=True):
  targets = num_of_targets * TargetAndCustom(custom=custom)
  CommonModule.log('# of targets', num_of_targets, ' targets')
  CommonModule.log('Targets', targets)
  return targets

def MultiRoles(num_of_keys_per_delegation=1, num_of_roles_per_delegation=1):
  rolename = CommonModule.FILENAME_SIZE_IN_BYTES
  numberOfKeyids = CommonModule.LENGTH_SIZE_IN_BYTES
  keyids = CommonModule.Keyids(num_of_keys_per_delegation)
  threshold = CommonModule.THRESHOLD_SIZE_IN_BYTES

  MultiRole = rolename + numberOfKeyids + keyids + threshold
  roles = num_of_roles_per_delegation * MultiRole
  CommonModule.log('MultiRoles', roles)
  return roles

def PrioritizedPathsToRoles(num_of_delegations=1,
                            num_of_keys_per_delegation=1,
                            num_of_paths_per_delegation=1,
                            num_of_roles_per_delegation=1):
  numberOfPaths = CommonModule.LENGTH_SIZE_IN_BYTES
  numberOfRoles = CommonModule.LENGTH_SIZE_IN_BYTES
  # FIXME: No need for a whole byte to represent a BOOLEAN, but since we are
  # currently fundamentally dealing with bytes, this will do for now. At least
  # it overestimates rather than underestimate.
  terminating = CommonModule.TAG_SIZE_IN_BYTES

  paths = CommonModule.Paths(num_of_paths_per_delegation)
  roles = MultiRoles(num_of_keys_per_delegation=num_of_keys_per_delegation,
                     num_of_roles_per_delegation=num_of_roles_per_delegation)

  PathsToRoles = numberOfPaths + paths + numberOfRoles + roles + terminating
  CommonModule.log('PathsToRoles', PathsToRoles)
  delegations = num_of_delegations * PathsToRoles
  CommonModule.log('PrioritizedPathsToRoles', delegations)
  return delegations

def TargetsDelegations(num_of_delegations=1,
                       num_of_keys_per_delegation=1,
                       num_of_paths_per_delegation=1,
                       num_of_roles_per_delegation=1):
  numberOfKeys = CommonModule.LENGTH_SIZE_IN_BYTES
  numberOfDelegations = CommonModule.LENGTH_SIZE_IN_BYTES

  num_of_keys = num_of_delegations * num_of_keys_per_delegation
  keys = CommonModule.PublicKeys(num_of_keys=num_of_keys)
  delegations = PrioritizedPathsToRoles(num_of_delegations=num_of_delegations,
                        num_of_keys_per_delegation=num_of_keys_per_delegation,
                        num_of_paths_per_delegation=num_of_paths_per_delegation,
                        num_of_roles_per_delegation=num_of_roles_per_delegation)

  targetsDelegations = numberOfKeys + keys + numberOfDelegations + delegations
  CommonModule.log('TargetsDelegations', targetsDelegations)
  return targetsDelegations

def TargetsMetadata(custom=True,
                    num_of_keys=1,
                    num_of_targets=1,
                    num_of_delegations=0,
                    num_of_keys_per_delegation=1,
                    num_of_paths_per_delegation=1,
                    num_of_roles_per_delegation=1):
  numberOfTargets = CommonModule.NATURAL_SIZE_IN_BYTES
  targets = Targets(num_of_targets, custom=custom)

  if num_of_delegations:
    delegations = TargetsDelegations(num_of_delegations=num_of_delegations,
                        num_of_keys_per_delegation=num_of_keys_per_delegation,
                        num_of_paths_per_delegation=num_of_paths_per_delegation,
                        num_of_roles_per_delegation=num_of_roles_per_delegation)
  else:
    delegations = 0

  targetsMetadata = numberOfTargets + targets + delegations
  CommonModule.log('targetsMetadata', targetsMetadata)
  return MetadataModule.Metadata(targetsMetadata, num_of_keys=num_of_keys)
