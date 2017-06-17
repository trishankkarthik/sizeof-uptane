#!/usr/bin/env python3

# 2nd-party imports.
import CommonModule
import TimestampModule
import SnapshotModule
import TargetsModule

def Bundle(num_of_tier1_suppliers=1, num_of_targets_per_tier1_supplier=1):
  '''The image repository typically provides new timestamp, snapshot, and
  targets metadata.'''

  # NOTE: We assume that every tier-1 supplier signs the same number of targets.
  # Of course this is an unreasonable assumption, but it is better to
  # overestimate rather than underestimate.
  supplierTargetsMetadata =TargetsModule.\
               TargetsMetadata(custom=True,
                               num_of_keys=1,
                               num_of_targets=num_of_targets_per_tier1_supplier,
                               num_of_delegations=0,
                               num_of_keys_per_delegation=0,
                               num_of_paths_per_delegation=0,
                               num_of_roles_per_delegation=0)

  # The top-level targets role signs for delegations to tier-1 suppliers, and no
  # targets.
  # Both the top-level targets role, and tier-1 suppliers, are each assumed to
  # use 1 key.
  topLeveltargetsMetadata = TargetsModule.\
                      TargetsMetadata(custom=False,
                                      num_of_keys=1,
                                      num_of_targets=0,
                                      num_of_delegations=num_of_tier1_suppliers,
                                      num_of_keys_per_delegation=1,
                                      num_of_paths_per_delegation=1,
                                      num_of_roles_per_delegation=1)

  # Number of targets metadata files in snapshot metadata =
  # number of tier-1 suppliers + one top-level targets role.
  snapshotMetadata = SnapshotModule.\
                     SnapshotMetadata(num_of_targets_metadata_files=
                                      num_of_tier1_suppliers+1)

  timestampMetadata = TimestampModule.TimestampMetadata()

  allSuppliersTargetsMetadata = num_of_tier1_suppliers * supplierTargetsMetadata
  bundle = allSuppliersTargetsMetadata + topLeveltargetsMetadata + \
           snapshotMetadata + timestampMetadata

  CommonModule.log('# of tier-1 suppliers', num_of_tier1_suppliers,
                   unit=' tier-1 suppliers')
  CommonModule.log('Bundle', bundle)
  return bundle

if __name__ == '__main__':
  # We expect an OEM to delegate to, at most, 100 tier-1 suppliers.
  # We expect that typically there are 5 images per ECU.
  # We assume that the OEM maintains a separate image repository per vehicle
  # (make, model, year).
  # These image repositories can safely reside on the same physical server,
  # and may each simply take up a separate directory.
  # The OEM may reuse the root role keys across these image repositories.
  CommonModule.time(
    CommonModule.iso_tp_overhead(
      Bundle(num_of_tier1_suppliers=100, num_of_targets_per_tier1_supplier=5)
    )
  )
