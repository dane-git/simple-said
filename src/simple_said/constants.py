COUNTERS = {
  "Counter": {
    "-A": {
      "name": "ControllerIdxSigs",
      "count": "*1",
      "units": "SIGS",
      "unit": "SIG",
      "context": [
        "Indexer"
      ],
      "type": 'CONTROLLER_INDEXED_SIGS',
      'COUNT_VALUE': 'NUM_SIGS',
    },
    "-B": {
      "name": "WitnessIdxSigs",
      "count": "*1",
      "context": [
        "Indexer"
      ],
      "units": "SIGS",
    },
    "-C": {
      "name": "NonTransReceiptCouples",
      "count": "*2"
    },
    "-D": {
      "name": "TransReceiptQuadruples",
      "count": "*4"
    },
    "-E": {
      "name": "FirstSeenReplayCouples",
      "count": "*2"
    },
    "-F": {
      "name": "TransIdxSigGroups",
      "count": "*4"
    },
    "-G": {
      "name": "SealSourceCouples",
      "count": "*2"
    },
    "-H": {
      "name": "TransLastIdxSigGroups",
      "count": "*2"
    },
    "-I": {
      "name": "SealSourceTriples",
      "count": "*3"
    },
    "-J": {
      "name": "SadPathSig",
      "count": "*2"
    },
    "-K": {
      "name": "SadPathSigGroup",
      "count": "*2+1"
    },
    "-L": {
      "name": "PathedMaterialQuadlets"
    },
    "-V": {
      "name": "AttachedMaterialQuadlets",
      "count": "*4",
      "units": "CHAR",
      "unit": "QUADLET",
      "context": [
        "Indexer"
      ],
      'type': 'DIGEST_SEAL',
      
    },
    "-0V": {
      "name": "BigAttachedMaterialQuadlets"
    },
    "--AAA": {
      "name": "KERIProtocolStack",
      "context": [
        "Matter",
        "Counter"
      ]
    }
  },
  "AltCounter": {
    "-A": {
      "name": "ControllerIdxSigs"
    },
    "-B": {
      "name": "WitnessIdxSigs"
    },
    "-C": {
      "name": "NonTransReceiptCouples"
    },
    "-D": {
      "name": "TransReceiptQuadruples"
    },
    "-E": {
      "name": "FirstSeenReplayCouples"
    },
    "-F": {
      "name": "TransIdxSigGroups"
    },
    "-G": {
      "name": "SealSourceCouples"
    },
    "-H": {
      "name": "TransLastIdxSigGroups"
    },
    "-I": {
      "name": "SealSourceTriples"
    },
    "-J": {
      "name": "SadPathSig"
    },
    "-K": {
      "name": "SadPathSigGroup"
    },
    "-L": {
      "name": "PathedMaterialQuadlets"
    },
    "-U": {
      "name": "MessageDataGroups"
    },
    "-V": {
      "name": "AttachedMaterialQuadlets"
    },
    "-W": {
      "name": "MessageDataMaterialQuadlets"
    },
    "-X": {
      "name": "CombinedMaterialQuadlets"
    },
    "-Y": {
      "name": "MaterialGroups"
    },
    "-Z": {
      "name": "MaterialQuadlets"
    },
    "-0U": {
      "name": "BigMessageDataGroups"
    },
    "-0V": {
      "name": "BigAttachedMaterialQuadlets"
    },
    "-0W": {
      "name": "BigMessageDataMaterialQuadlets"
    },
    "-0X": {
      "name": "BigCombinedMaterialQuadlets"
    },
    "-0Y": {
      "name": "BigMaterialGroups"
    },
    "-0Z": {
      "name": "BigMaterialQuadlets"
    }
  }
}

CODEX = {
    "Matter": {
      "A": "Ed25519_Seed",
      "B": "Ed25519N",
      "C": "X25519",
      "D": "Ed25519",
      "E": "Blake3_256",
      "F": "Blake2b_256",
      "G": "Blake2s_256",
      "H": "SHA3_256",
      "I": "SHA2_256",
      "J": "ECDSA_256k1_Seed",
      "K": "Ed448_Seed",
      "L": "X448",
      "M": "Short",
      "N": "Big",
      "O": "X25519_Private",
      "P": "X25519_Cipher_Seed",
      "Q": "ECDSA_256r1_Seed",
      "R": "Tall",
      "S": "Large",
      "T": "Great",
      "U": "Vast",
      "V": "Label1",
      "W": "Label2",
      "X": "Tag3",
      "Y": "Tag7",
      "0A": "Salt_128",
      "0B": "Ed25519_Sig",
      "0C": "ECDSA_256k1_Sig",
      "0D": "Blake3_512",
      "0E": "Blake2b_512",
      "0F": "SHA3_512",
      "0G": "SHA2_512",
      "0H": "Long",
      "0I": "ECDSA_256r1_Sig",
      "0J": "Tag1",
      "0K": "Tag2",
      "0L": "Tag5",
      "0M": "Tag6",
      "1AAA": "ECDSA_256k1N",
      "1AAB": "ECDSA_256k1",
      "1AAC": "Ed448N",
      "1AAD": "Ed448",
      "1AAE": "Ed448_Sig",
      "1AAF": "Tern",
      "1AAG": "DateTime",
      "1AAH": "X25519_Cipher_Salt",
      "1AAI": "ECDSA_256r1N",
      "1AAJ": "ECDSA_256r1",
      "1AAK": "None",
      "1AAL": "Tag4",
      "2AAA": "TBD1",
      "3AAA": "TBD2",
      "4A": "StrB64_L0",
      "5A": "StrB64_L1",
      "6A": "StrB64_L2",
      "7AAA": "StrB64_Big_L0",
      "8AAA": "StrB64_Big_L1",
      "9AAA": "StrB64_Big_L2",
      "4B": "Bytes_L0",
      "5B": "Bytes_L1",
      "6B": "Bytes_L2",
      "7AAB": "Bytes_Big_L0",
      "8AAB": "Bytes_Big_L1",
      "9AAB": "Bytes_Big_L2",
      "4C": "X25519_Cipher_L0",
      "5C": "X25519_Cipher_L1",
      "6C": "X25519_Cipher_L2",
      "7AAC": "X25519_Cipher_Big_L0",
      "8AAC": "X25519_Cipher_Big_L1",
      "9AAC": "X25519_Cipher_Big_L2"
    },
    "SmallVarRawSize": {
      "4": "Lead0",
      "5": "Lead1",
      "6": "Lead2"
    },
    "LargeVarRawSize": {
      "7": "Lead0_Big",
      "8": "Lead1_Big",
      "9": "Lead2_Big"
    },
    "NonTrans": {
      "B": "Ed25519N",
      "1AAA": "ECDSA_256k1N",
      "1AAC": "Ed448N",
      "1AAI": "ECDSA_256r1N"
    },
    "Dig": {
      "E": "Blake3_256",
      "F": "Blake2b_256",
      "G": "Blake2s_256",
      "H": "SHA3_256",
      "I": "SHA2_256",
      "0D": "Blake3_512",
      "0E": "Blake2b_512",
      "0F": "SHA3_512",
      "0G": "SHA2_512"
    },
    "Num": {
      "M": "Short",
      "0H": "Long",
      "N": "Big",
      "0A": "Huge"
    },
    "Bext": {
      "4A": "StrB64_L0",
      "5A": "StrB64_L1",
      "6A": "StrB64_L2",
      "7AAA": "StrB64_Big_L0",
      "8AAA": "StrB64_Big_L1",
      "9AAA": "StrB64_Big_L2"
    },
    "Pre": {
      "B": "Ed25519N",
      "D": "Ed25519",
      "E": "Blake3_256",
      "F": "Blake2b_256",
      "G": "Blake2s_256",
      "H": "SHA3_256",
      "I": "SHA2_256",
      "0D": "Blake3_512",
      "0E": "Blake2b_512",
      "0F": "SHA3_512",
      "0G": "SHA2_512",
      "1AAA": "ECDSA_256k1N",
      "1AAB": "ECDSA_256k1",
      "1AAI": "ECDSA_256r1N",
      "1AAJ": "ECDSA_256r1"
    },
    "Indexer": {
      "A": "Ed25519_Sig",
      "B": "Ed25519_Crt_Sig",
      "C": "ECDSA_256k1_Sig",
      "D": "ECDSA_256k1_Crt_Sig",
      "E": "ECDSA_256r1_Sig",
      "F": "ECDSA_256r1_Crt_Sig",
      "0A": "Ed448_Sig",
      "0B": "Ed448_Crt_Sig",
      "2A": "Ed25519_Big_Sig",
      "2B": "Ed25519_Big_Crt_Sig",
      "2C": "ECDSA_256k1_Big_Sig",
      "2D": "ECDSA_256k1_Big_Crt_Sig",
      "2E": "ECDSA_256r1_Big_Sig",
      "2F": "ECDSA_256r1_Big_Crt_Sig",
      "3A": "Ed448_Big_Sig",
      "3B": "Ed448_Big_Crt_Sig",
      "0z": "TBD0",
      "1z": "TBD1",
      "4z": "TBD4"
    },
    "IndexedSig": {
      "A": "Ed25519_Sig",
      "B": "Ed25519_Crt_Sig",
      "C": "ECDSA_256k1_Sig",
      "D": "ECDSA_256k1_Crt_Sig",
      "E": "ECDSA_256r1_Sig",
      "F": "ECDSA_256r1_Crt_Sig",
      "0A": "Ed448_Sig",
      "0B": "Ed448_Crt_Sig",
      "2A": "Ed25519_Big_Sig",
      "2B": "Ed25519_Big_Crt_Sig",
      "2C": "ECDSA_256k1_Big_Sig",
      "2D": "ECDSA_256k1_Big_Crt_Sig",
      "2E": "ECDSA_256r1_Big_Sig",
      "2F": "ECDSA_256r1_Big_Crt_Sig",
      "3A": "Ed448_Big_Sig",
      "3B": "Ed448_Big_Crt_Sig"
    },
    "IndexedCurrentSig": {
      "B": "Ed25519_Crt_Sig",
      "D": "ECDSA_256k1_Crt_Sig",
      "F": "ECDSA_256r1_Crt_Sig",
      "0B": "Ed448_Crt_Sig",
      "2B": "Ed25519_Big_Crt_Sig",
      "2D": "ECDSA_256k1_Big_Crt_Sig",
      "2F": "ECDSA_256r1_Big_Crt_Sig",
      "3B": "Ed448_Big_Crt_Sig"
    },
    "IndexedBothSig": {
      "A": "Ed25519_Sig",
      "C": "ECDSA_256k1_Sig",
      "E": "ECDSA_256r1_Sig",
      "0A": "Ed448_Sig",
      "2A": "Ed25519_Big_Sig",
      "2C": "ECDSA_256k1_Big_Sig",
      "2E": "ECDSA_256r1_Big_Sig",
      "3A": "Ed448_Big_Sig"
    },
    "Counter": {
      "-A": "ControllerIdxSigs",
      "-B": "WitnessIdxSigs",
      "-C": "NonTransReceiptCouples",
      "-D": "TransReceiptQuadruples",
      "-E": "FirstSeenReplayCouples",
      "-F": "TransIdxSigGroups",
      "-G": "SealSourceCouples",
      "-H": "TransLastIdxSigGroups",
      "-I": "SealSourceTriples",
      "-J": "SadPathSig",
      "-K": "SadPathSigGroup",
      "-L": "PathedMaterialQuadlets",
      "-V": "AttachedMaterialQuadlets",
      "-0V": "BigAttachedMaterialQuadlets",
      "--AAA": "KERIProtocolStack"
    },
    "ProtocolGenus": {
      "--AAA": "KERI"
    },
    "AltCounter": {
      "-A": "ControllerIdxSigs",
      "-B": "WitnessIdxSigs",
      "-C": "NonTransReceiptCouples",
      "-D": "TransReceiptQuadruples",
      "-E": "FirstSeenReplayCouples",
      "-F": "TransIdxSigGroups",
      "-G": "SealSourceCouples",
      "-H": "TransLastIdxSigGroups",
      "-I": "SealSourceTriples",
      "-J": "SadPathSig",
      "-K": "SadPathSigGroup",
      "-L": "PathedMaterialQuadlets",
      "-U": "MessageDataGroups",
      "-V": "AttachedMaterialQuadlets",
      "-W": "MessageDataMaterialQuadlets",
      "-X": "CombinedMaterialQuadlets",
      "-Y": "MaterialGroups",
      "-Z": "MaterialQuadlets",
      "-0U": "BigMessageDataGroups",
      "-0V": "BigAttachedMaterialQuadlets",
      "-0W": "BigMessageDataMaterialQuadlets",
      "-0X": "BigCombinedMaterialQuadlets",
      "-0Y": "BigMaterialGroups",
      "-0Z": "BigMaterialQuadlets"
    },
    "Cold": {
      "0": "Free",
      "1": "CtB64",
      "2": "OpB64",
      "3": "JSON",
      "4": "MGPK1",
      "5": "CBOR",
      "6": "MGPK2",
      "7": "CtOpB2"
    }
  }
SIZES = {
  "Matter": {
    "A": {
      "hs": 1,
      "ss": 0,
      "fs": 44,
      "ls": 0
    },
    "B": {
      "hs": 1,
      "ss": 0,
      "fs": 44,
      "ls": 0
    },
    "C": {
      "hs": 1,
      "ss": 0,
      "fs": 44,
      "ls": 0
    },
    "D": {
      "hs": 1,
      "ss": 0,
      "fs": 44,
      "ls": 0
    },
    "E": {
      "hs": 1,
      "ss": 0,
      "fs": 44,
      "ls": 0
    },
    "F": {
      "hs": 1,
      "ss": 0,
      "fs": 44,
      "ls": 0
    },
    "G": {
      "hs": 1,
      "ss": 0,
      "fs": 44,
      "ls": 0
    },
    "H": {
      "hs": 1,
      "ss": 0,
      "fs": 44,
      "ls": 0
    },
    "I": {
      "hs": 1,
      "ss": 0,
      "fs": 44,
      "ls": 0
    },
    "J": {
      "hs": 1,
      "ss": 0,
      "fs": 44,
      "ls": 0
    },
    "K": {
      "hs": 1,
      "ss": 0,
      "fs": 76,
      "ls": 0
    },
    "L": {
      "hs": 1,
      "ss": 0,
      "fs": 76,
      "ls": 0
    },
    "M": {
      "hs": 1,
      "ss": 0,
      "fs": 4,
      "ls": 0
    },
    "N": {
      "hs": 1,
      "ss": 0,
      "fs": 12,
      "ls": 0
    },
    "O": {
      "hs": 1,
      "ss": 0,
      "fs": 44,
      "ls": 0
    },
    "P": {
      "hs": 1,
      "ss": 0,
      "fs": 124,
      "ls": 0
    },
    "Q": {
      "hs": 1,
      "ss": 0,
      "fs": 44,
      "ls": 0
    },
    "R": {
      "hs": 1,
      "ss": 0,
      "fs": 8,
      "ls": 0
    },
    "S": {
      "hs": 1,
      "ss": 0,
      "fs": 16,
      "ls": 0
    },
    "T": {
      "hs": 1,
      "ss": 0,
      "fs": 20,
      "ls": 0
    },
    "U": {
      "hs": 1,
      "ss": 0,
      "fs": 24,
      "ls": 0
    },
    "V": {
      "hs": 1,
      "ss": 0,
      "fs": 4,
      "ls": 1
    },
    "W": {
      "hs": 1,
      "ss": 0,
      "fs": 4,
      "ls": 0
    },
    "X": {
      "hs": 1,
      "ss": 0,
      "fs": 4,
      "ls": 0
    },
    "Y": {
      "hs": 1,
      "ss": 0,
      "fs": 8,
      "ls": 0
    },
    "0A": {
      "hs": 2,
      "ss": 0,
      "fs": 24,
      "ls": 0
    },
    "0B": {
      "hs": 2,
      "ss": 0,
      "fs": 88,
      "ls": 0
    },
    "0C": {
      "hs": 2,
      "ss": 0,
      "fs": 88,
      "ls": 0
    },
    "0D": {
      "hs": 2,
      "ss": 0,
      "fs": 88,
      "ls": 0
    },
    "0E": {
      "hs": 2,
      "ss": 0,
      "fs": 88,
      "ls": 0
    },
    "0F": {
      "hs": 2,
      "ss": 0,
      "fs": 88,
      "ls": 0
    },
    "0G": {
      "hs": 2,
      "ss": 0,
      "fs": 88,
      "ls": 0
    },
    "0H": {
      "hs": 2,
      "ss": 0,
      "fs": 8,
      "ls": 0
    },
    "0I": {
      "hs": 2,
      "ss": 0,
      "fs": 88,
      "ls": 0
    },
    "0J": {
      "hs": 2,
      "ss": 0,
      "fs": 4,
      "ls": 0
    },
    "0K": {
      "hs": 2,
      "ss": 0,
      "fs": 4,
      "ls": 0
    },
    "0L": {
      "hs": 2,
      "ss": 0,
      "fs": 8,
      "ls": 0
    },
    "0M": {
      "hs": 2,
      "ss": 0,
      "fs": 8,
      "ls": 0
    },
    "1AAA": {
      "hs": 4,
      "ss": 0,
      "fs": 48,
      "ls": 0
    },
    "1AAB": {
      "hs": 4,
      "ss": 0,
      "fs": 48,
      "ls": 0
    },
    "1AAC": {
      "hs": 4,
      "ss": 0,
      "fs": 80,
      "ls": 0
    },
    "1AAD": {
      "hs": 4,
      "ss": 0,
      "fs": 80,
      "ls": 0
    },
    "1AAE": {
      "hs": 4,
      "ss": 0,
      "fs": 56,
      "ls": 0
    },
    "1AAF": {
      "hs": 4,
      "ss": 0,
      "fs": 8,
      "ls": 0
    },
    "1AAG": {
      "hs": 4,
      "ss": 0,
      "fs": 36,
      "ls": 0
    },
    "1AAH": {
      "hs": 4,
      "ss": 0,
      "fs": 100,
      "ls": 0
    },
    "1AAI": {
      "hs": 4,
      "ss": 0,
      "fs": 48,
      "ls": 0
    },
    "1AAJ": {
      "hs": 4,
      "ss": 0,
      "fs": 48,
      "ls": 0
    },
    "1AAK": {
      "hs": 4,
      "ss": 0,
      "fs": 4,
      "ls": 0
    },
    "1AAL": {
      "hs": 4,
      "ss": 0,
      "fs": 8,
      "ls": 0
    },
    "2AAA": {
      "hs": 4,
      "ss": 0,
      "fs": 8,
      "ls": 1
    },
    "3AAA": {
      "hs": 4,
      "ss": 0,
      "fs": 8,
      "ls": 2
    },
    "4A": {
      "hs": 2,
      "ss": 2,
      "fs": None,
      "ls": 0
    },
    "5A": {
      "hs": 2,
      "ss": 2,
      "fs": None,
      "ls": 1
    },
    "6A": {
      "hs": 2,
      "ss": 2,
      "fs": None,
      "ls": 2
    },
    "7AAA": {
      "hs": 4,
      "ss": 4,
      "fs": None,
      "ls": 0
    },
    "8AAA": {
      "hs": 4,
      "ss": 4,
      "fs": None,
      "ls": 1
    },
    "9AAA": {
      "hs": 4,
      "ss": 4,
      "fs": None,
      "ls": 2
    },
    "4B": {
      "hs": 2,
      "ss": 2,
      "fs": None,
      "ls": 0
    },
    "5B": {
      "hs": 2,
      "ss": 2,
      "fs": None,
      "ls": 1
    },
    "6B": {
      "hs": 2,
      "ss": 2,
      "fs": None,
      "ls": 2
    },
    "7AAB": {
      "hs": 4,
      "ss": 4,
      "fs": None,
      "ls": 0
    },
    "8AAB": {
      "hs": 4,
      "ss": 4,
      "fs": None,
      "ls": 1
    },
    "9AAB": {
      "hs": 4,
      "ss": 4,
      "fs": None,
      "ls": 2
    },
    "4C": {
      "hs": 2,
      "ss": 2,
      "fs": None,
      "ls": 0
    },
    "5C": {
      "hs": 2,
      "ss": 2,
      "fs": None,
      "ls": 1
    },
    "6C": {
      "hs": 2,
      "ss": 2,
      "fs": None,
      "ls": 2
    },
    "7AAC": {
      "hs": 4,
      "ss": 4,
      "fs": None,
      "ls": 0
    },
    "8AAC": {
      "hs": 4,
      "ss": 4,
      "fs": None,
      "ls": 1
    },
    "9AAC": {
      "hs": 4,
      "ss": 4,
      "fs": None,
      "ls": 2
    }
  },
  "Indexer": {
    "A": {
      "hs": 1,
      "ss": 1,
      "os": 0,
      "fs": 88,
      "ls": 0
    },
    "B": {
      "hs": 1,
      "ss": 1,
      "os": 0,
      "fs": 88,
      "ls": 0
    },
    "C": {
      "hs": 1,
      "ss": 1,
      "os": 0,
      "fs": 88,
      "ls": 0
    },
    "D": {
      "hs": 1,
      "ss": 1,
      "os": 0,
      "fs": 88,
      "ls": 0
    },
    "E": {
      "hs": 1,
      "ss": 1,
      "os": 0,
      "fs": 88,
      "ls": 0
    },
    "F": {
      "hs": 1,
      "ss": 1,
      "os": 0,
      "fs": 88,
      "ls": 0
    },
    "0A": {
      "hs": 2,
      "ss": 2,
      "os": 1,
      "fs": 156,
      "ls": 0
    },
    "0B": {
      "hs": 2,
      "ss": 2,
      "os": 1,
      "fs": 156,
      "ls": 0
    },
    "2A": {
      "hs": 2,
      "ss": 4,
      "os": 2,
      "fs": 92,
      "ls": 0
    },
    "2B": {
      "hs": 2,
      "ss": 4,
      "os": 2,
      "fs": 92,
      "ls": 0
    },
    "2C": {
      "hs": 2,
      "ss": 4,
      "os": 2,
      "fs": 92,
      "ls": 0
    },
    "2D": {
      "hs": 2,
      "ss": 4,
      "os": 2,
      "fs": 92,
      "ls": 0
    },
    "2E": {
      "hs": 2,
      "ss": 4,
      "os": 2,
      "fs": 92,
      "ls": 0
    },
    "2F": {
      "hs": 2,
      "ss": 4,
      "os": 2,
      "fs": 92,
      "ls": 0
    },
    "3A": {
      "hs": 2,
      "ss": 6,
      "os": 3,
      "fs": 160,
      "ls": 0
    },
    "3B": {
      "hs": 2,
      "ss": 6,
      "os": 3,
      "fs": 160,
      "ls": 0
    },
    "0z": {
      "hs": 2,
      "ss": 2,
      "os": 0,
      "fs": None,
      "ls": 0
    },
    "1z": {
      "hs": 2,
      "ss": 2,
      "os": 1,
      "fs": 76,
      "ls": 1
    },
    "4z": {
      "hs": 2,
      "ss": 6,
      "os": 3,
      "fs": 80,
      "ls": 1
    }
  },
  "Counter": {
    "-A": {
      "hs": 2,
      "ss": 2,
      "fs": 4,
      "ls": 0
    },
    "-B": {
      "hs": 2,
      "ss": 2,
      "fs": 4,
      "ls": 0
    },
    "-C": {
      "hs": 2,
      "ss": 2,
      "fs": 4,
      "ls": 0
    },
    "-D": {
      "hs": 2,
      "ss": 2,
      "fs": 4,
      "ls": 0
    },
    "-E": {
      "hs": 2,
      "ss": 2,
      "fs": 4,
      "ls": 0
    },
    "-F": {
      "hs": 2,
      "ss": 2,
      "fs": 4,
      "ls": 0
    },
    "-G": {
      "hs": 2,
      "ss": 2,
      "fs": 4,
      "ls": 0
    },
    "-H": {
      "hs": 2,
      "ss": 2,
      "fs": 4,
      "ls": 0
    },
    "-I": {
      "hs": 2,
      "ss": 2,
      "fs": 4,
      "ls": 0
    },
    "-J": {
      "hs": 2,
      "ss": 2,
      "fs": 4,
      "ls": 0
    },
    "-K": {
      "hs": 2,
      "ss": 2,
      "fs": 4,
      "ls": 0
    },
    "-L": {
      "hs": 2,
      "ss": 2,
      "fs": 4,
      "ls": 0
    },
    "-V": {
      "hs": 2,
      "ss": 2,
      "fs": 4,
      "ls": 0
    },
    "-0V": {
      "hs": 3,
      "ss": 5,
      "fs": 8,
      "ls": 0
    },
    "--AAA": {
      "hs": 5,
      "ss": 3,
      "fs": 8,
      "ls": 0
    }
  }
}



_COUNTERS  =     {
  # Generic pipeline group up to 4,095 quadlets/triplets
  "-A": {
      "hs": 2,
      "ss": 2,
      "fs": 4,
      "ls": 0,
      'type': 'CONTROLLER_INDEXED_SIGS',
      'COUNT_VALUE': 'NUM_SIGS'
    },
    "-B": {
      "hs": 2,
      "ss": 2,
      "fs": 4,
      "ls": 0
    },
    "-C": {
      "hs": 2,
      "ss": 2,
      "fs": 4,
      "ls": 0
    },
    "-D": {
      "hs": 2,
      "ss": 2,
      "fs": 4,
      "ls": 0
    },
    "-E": {
      "hs": 2,
      "ss": 2,
      "fs": 4,
      "ls": 0
    },
    "-F": {
      "hs": 2,
      "ss": 2,
      "fs": 4,
      "ls": 0
    },
    "-G": {
      "hs": 2,
      "ss": 2,
      "fs": 4,
      "ls": 0
    },
    "-H": {
      "hs": 2,
      "ss": 2,
      "fs": 4,
      "ls": 0
    },
    "-I": {
      "hs": 2,
      "ss": 2,
      "fs": 4,
      "ls": 0
    },
    "-J": {
      "hs": 2,
      "ss": 2,
      "fs": 4,
      "ls": 0
    },
    "-K": {
      "hs": 2,
      "ss": 2,
      "fs": 4,
      "ls": 0
    },
    "-L": {
      "hs": 2,
      "ss": 2,
      "fs": 4,
      "ls": 0
    },
    
    # Digest seal singles dig up to 4,095 quadlets/triplets
    "-V": {
      "hs": 2,
      "ss": 2,
      "fs": 4,
      "ls": 0,
      'type': 'DIGEST_SEAL',
      'COUNT_VALUE': 'QUADLETS'
    },
    "-0V": {
      "hs": 3,
      "ss": 5,
      "fs": 8,
      "ls": 0
    },
    "--AAA": {
      "hs": 5,
      "ss": 3,
      "fs": 8,
      "ls": 0
    }
}