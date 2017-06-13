#!/usr/bin/env python3

# 1st-party imports.
import math
import logging
import sys

# Independent constants.
def bits_to_bytes(num_of_bits):
  '''Number of bits -> Number of bytes.'''
  return math.ceil(num_of_bits / 8)

# Assuming 32 bits per integer.
IDENTIFIER_SIZE_IN_BYTES     = 32
ED25519_PUBKEY_SIZE_IN_BYTES = bits_to_bytes(256)
ED25519_SIG_SIZE_IN_BYTES    = bits_to_bytes(512)
FILENAME_SIZE_IN_BYTES       = 32
POSITIVE_SIZE_IN_BYTES       = bits_to_bytes(32)
SHA256_HASH_SIZE_IN_BYTES    = bits_to_bytes(256)

# Dependent constants.
# In TUF, keyid is the SHA-256 hash of the public key.
KEYID_SIZE_IN_BYTES       = SHA256_HASH_SIZE_IN_BYTES
LENGTH_SIZE_IN_BYTES      = POSITIVE_SIZE_IN_BYTES
UTCDATETIME_SIZE_IN_BYTES = POSITIVE_SIZE_IN_BYTES

# Log everything to stdout.
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

def log(datatype, size):
  logging.debug('{}: {:,} bytes.'.format(datatype, size))

# Public functions.
def Hashes(hashes=(SHA256_HASH_SIZE_IN_BYTES,)):
  hashes_size = 0

  for digest_size in hashes:
    # Naive but reasonable assumption: we use an int as a tag.
    function = POSITIVE_SIZE_IN_BYTES
    digest = digest_size
    hash_size = function + digest
    log('Hash', hash_size)
    hashes_size += hash_size

  return hashes_size

def Signatures(num_of_signatures, keyid=KEYID_SIZE_IN_BYTES,
               # Naive but reasonable assumption: we use an int as a tag.
               method=POSITIVE_SIZE_IN_BYTES,
               value=ED25519_SIG_SIZE_IN_BYTES):
  '''https://github.com/uptane/asn1/blob/master/CommonModule.asn1'''

  signature = keyid + method + value
  log('Signature', signature)
  signatures = num_of_signatures * signature
  log('Signatures', signatures)
  return signatures
