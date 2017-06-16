#!/usr/bin/env python3

# 1st-party imports.
import math
import logging
import sys

# 3rd-party imports.
import humanize

# Independent constants.
def bits_to_bytes(num_of_bits):
  '''Number of bits -> Number of bytes.'''
  return math.ceil(num_of_bits / 8)

def bytes_to_bits(num_of_bytes):
  '''Number of bytes -> Number of bits.'''
  return math.ceil(num_of_bytes * 8)

# Sizes.
# Assuming 32 bits per integer.
IDENTIFIER_SIZE_IN_BYTES     = 32
INTEGER_SIZE_IN_BYTES        = bits_to_bytes(32)
ED25519_PUBKEY_SIZE_IN_BYTES = bits_to_bytes(256)
ED25519_SIG_SIZE_IN_BYTES    = bits_to_bytes(512)
FILENAME_SIZE_IN_BYTES       = 32
PATH_SIZE_IN_BYTES           = 32
SHA256_HASH_SIZE_IN_BYTES    = bits_to_bytes(256)
SHA512_HASH_SIZE_IN_BYTES    = bits_to_bytes(512)
# 2^8 tags ought to be enough for anybody.
TAG_SIZE_IN_BYTES            = 1

# Speeds.
# https://en.wikipedia.org/wiki/CAN_bus
KILO_BITS_PER_SECOND             = 10**3
CAN_LOW_SPEED_IN_BITS_PER_SECOND = 40 * KILO_BITS_PER_SECOND

# Dependent constants.
# We assume that the keyid is the SHA-256 hash of the public key.
KEYID_SIZE_IN_BYTES       = SHA256_HASH_SIZE_IN_BYTES
NATURAL_SIZE_IN_BYTES     = INTEGER_SIZE_IN_BYTES
POSITIVE_SIZE_IN_BYTES    = INTEGER_SIZE_IN_BYTES

LENGTH_SIZE_IN_BYTES      = POSITIVE_SIZE_IN_BYTES
THRESHOLD_SIZE_IN_BYTES   = POSITIVE_SIZE_IN_BYTES
UTCDATETIME_SIZE_IN_BYTES = POSITIVE_SIZE_IN_BYTES
VERSION_SIZE_IN_BYTES     = POSITIVE_SIZE_IN_BYTES

# Log everything to stdout.
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
                    format='[%(levelname)s] %(message)s')

def Hashes(hashes=(SHA256_HASH_SIZE_IN_BYTES,)):
  total_size = 0

  for digest_size in hashes:
    function = TAG_SIZE_IN_BYTES
    digest = digest_size
    size = function + digest
    log('Hash', size)
    total_size += size

  return total_size

def Keyids(num_of_keys):
  total_size = num_of_keys * KEYID_SIZE_IN_BYTES
  log('Keyids', total_size)
  return total_size

def Paths(num_of_paths):
  total_size = num_of_paths * PATH_SIZE_IN_BYTES
  log('Paths', total_size)
  return total_size

def PublicKeys(num_of_keys=1, publicKeyId=KEYID_SIZE_IN_BYTES,
               publicKeyValue=ED25519_PUBKEY_SIZE_IN_BYTES):
  publicKeyType = TAG_SIZE_IN_BYTES
  size = publicKeyId + publicKeyType + publicKeyValue
  log('PublicKey', size)
  total_size = num_of_keys * size
  log('PublicKeys', total_size)
  return total_size

def Signatures(num_of_signatures, keyid=KEYID_SIZE_IN_BYTES,
               method=TAG_SIZE_IN_BYTES,
               value=ED25519_SIG_SIZE_IN_BYTES):
  '''https://github.com/uptane/asn1/blob/master/CommonModule.asn1'''

  log('# of keys', num_of_signatures, unit=' keys')
  signature = keyid + method + value
  log('Signature', signature)
  signatures = num_of_signatures * signature
  log('Signatures', signatures)
  return signatures

# TODO: Add a depth parameter to indent log statements, so it's clearer where
# things came from.
def log(datatype, number, unit=' bytes', human=True):
  # Kludge, but whatever, it works.
  if human and unit.endswith('bytes'):
    number, unit = humanize.naturalsize(number).split()
    logging.debug('{0:<30}: {1:>8} {2}'.format(datatype, number, unit))
  elif human and unit.endswith('seconds'):
    number, unit = humanize.naturaldelta(number).split()
    logging.debug('{0:<30}: {1:>8} {2}'.format(datatype, number, unit))
  else:
    logging.debug('{0:<30}: {1:>8,d}{2}'.format(datatype, number, unit))

# TODO: This is from my best understanding. Needs review by a CAN expert.
def iso_tp_overhead(num_of_bytes):
  '''https://en.wikipedia.org/wiki/ISO_15765-2'''

  # On-demand overhead for each non-full packet.
  def packet_overhead(remainder):
    assert remainder >= 0
    assert remainder < 4095

    if remainder <= 7:
      overhead_in_bytes = 0
    else:
      # First 6 bytes in the first frame.
      overhead_in_bytes = 2
      # After that, 7 bytes for each consecutive frame.
      num_of_full_frames = (remainder - 6) // 7
      overhead_in_bytes += num_of_full_frames
      # Wasted bytes, if any, in a not-full consecutive frame.
      leftover = (remainder - 6) % 7
      overhead_in_bytes += 7 - leftover
    return overhead_in_bytes

  # A maximum of 7 bytes of payload can be sent using normal addressing.
  if num_of_bytes <= 7:
    overhead_in_bytes = 0
  else:
    # Precomputed overhead for each full packet.
    # Each full packet can send 4095 bytes of payload.
    # I must admit 4095 makes no sense to me, because it wastes the last frame
    # to send 1 actual byte of payload. I must have misunderstood something.
    num_of_full_packets = num_of_bytes // 4095
    overhead_in_bytes = num_of_full_packets * 593
    # Overhead for the remainder, if any.
    remainder = num_of_bytes % 4095
    overhead_in_bytes += packet_overhead(remainder)

  log('ISO-TP overhead', overhead_in_bytes)
  total = num_of_bytes + overhead_in_bytes
  log('Payload + overhead', total)
  return total

def time(num_of_bytes, speed=CAN_LOW_SPEED_IN_BITS_PER_SECOND):
  num_of_bits = bytes_to_bits(num_of_bytes)
  # NOTE: Things take time. 1, not 0, seconds.
  time = math.ceil(num_of_bits / speed)
  log('Time', time, unit=' seconds')
