#!/usr/bin/env python3

# 2nd-party imports.
import CommonModule

def Metadata(signedBody, num_of_keys=1):
  '''https://github.com/uptane/asn1/blob/master/MetadataModule.asn1'''

  signatures = CommonModule.Signatures(num_of_keys)
  numberOfSignatures = CommonModule.LENGTH_SIZE_IN_BYTES

  type = CommonModule.TAG_SIZE_IN_BYTES
  expires = CommonModule.UTCDATETIME_SIZE_IN_BYTES
  version = CommonModule.VERSION_SIZE_IN_BYTES
  body = signedBody
  signed = type + expires + version + body

  metadata = signatures + numberOfSignatures + signed
  CommonModule.log('Metadata', metadata)
  return metadata
