#!/usr/bin/env python3

# 1st-party imports.
import logging

# 2nd-party imports.
import CommonModule
import TargetsModule

def ECUVersionManifests(num_of_secondaries=1, num_of_keys_per_secondary=1):
  '''https://github.com/uptane/asn1/blob/master/ECUModule.asn1'''

  signatures = CommonModule.Signatures(num_of_keys_per_secondary)
  numberOfSignatures = CommonModule.LENGTH_SIZE_IN_BYTES

  ecuIdentifier = CommonModule.IDENTIFIER_SIZE_IN_BYTES
  previousTime = CommonModule.UTCDATETIME_SIZE_IN_BYTES
  currentTime = CommonModule.UTCDATETIME_SIZE_IN_BYTES
  securityAttack = 1024 #bytes
  installedImage = TargetsModule.Target()
  signed = ecuIdentifier + previousTime + currentTime + securityAttack + \
           installedImage

  ECUVersionManifest = signatures + numberOfSignatures + signed
  CommonModule.log('ECUVersionManifest', ECUVersionManifest)
  ECUVersionManifests = num_of_secondaries * ECUVersionManifest
  CommonModule.log('# of secondaries', num_of_secondaries, unit=' secondaries')
  CommonModule.log('ECUVersionManifests', ECUVersionManifests)
  return ECUVersionManifests

def VehicleVersionManifest(num_of_primary_keys=1, num_of_secondaries=1):
  '''https://github.com/uptane/asn1/blob/master/ECUModule.asn1'''

  signatures = CommonModule.Signatures(num_of_primary_keys)
  numberOfSignatures = CommonModule.LENGTH_SIZE_IN_BYTES

  vehicleIdentifier = CommonModule.IDENTIFIER_SIZE_IN_BYTES
  primaryIdentifier = CommonModule.IDENTIFIER_SIZE_IN_BYTES
  numberOfECUVersionManifests = CommonModule.LENGTH_SIZE_IN_BYTES
  ecuVersionManifests = ECUVersionManifests(num_of_secondaries)
  securityAttack = 1024 #bytes
  signed = vehicleIdentifier + primaryIdentifier + \
           numberOfECUVersionManifests + ecuVersionManifests + securityAttack

  vehicleVersionManifest = signatures + numberOfSignatures + signed
  CommonModule.log('VehicleVersionManifest', vehicleVersionManifest)
  return vehicleVersionManifest

if __name__ == '__main__':
  CommonModule.time(VehicleVersionManifest(num_of_secondaries=127))
