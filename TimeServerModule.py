#!/usr/bin/env python3

# 1st-party imports.
import logging

# 2nd-party imports.
import CommonModule

def Tokens(num_of_ecus=1):
  Token = CommonModule.INTEGER_SIZE_IN_BYTES
  CommonModule.log('Token', Token)

  CommonModule.log('# of ECUs', num_of_ecus, unit=' ECUs')
  tokens = num_of_ecus * Token

  CommonModule.log('Tokens', tokens)
  return tokens

def SequenceOfTokens(num_of_ecus=1):
  '''https://github.com/uptane/asn1/blob/master/TimeServerModule.asn1'''

  numberOfTokens = CommonModule.LENGTH_SIZE_IN_BYTES
  tokens = Tokens(num_of_ecus=num_of_ecus)
  sequenceOfTokens = numberOfTokens + tokens
  CommonModule.log('SequenceOfTokens', sequenceOfTokens)
  return sequenceOfTokens

def CurrentTime(num_of_ecus=1, num_of_keys_for_time_server=1):
  '''https://github.com/uptane/asn1/blob/master/TimeServerModule.asn1'''

  numberOfSignatures = CommonModule.LENGTH_SIZE_IN_BYTES
  signatures = CommonModule.Signatures(num_of_keys_for_time_server)

  numberOfTokens = CommonModule.LENGTH_SIZE_IN_BYTES
  tokens = Tokens(num_of_ecus=num_of_ecus)
  timestamp = CommonModule.UTCDATETIME_SIZE_IN_BYTES
  signed = numberOfTokens + tokens + timestamp

  currentTime = signed + numberOfSignatures + signatures
  CommonModule.log('CurrentTime', currentTime)
  return currentTime

if __name__ == '__main__':
  num_of_ecus = 128
  sequenceOfTokens = SequenceOfTokens(num_of_ecus=num_of_ecus)
  currentTime = CurrentTime(num_of_ecus=num_of_ecus)
  CommonModule.time(
    CommonModule.iso_tp_overhead(sequenceOfTokens + currentTime)
  )
