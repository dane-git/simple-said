from simple_said.kutils import (
  byte_to_bits,
  is_bytes,
  determine_keri_version,
  get_version_string_info
)
from simple_said.constants import (
  COUNTERS
)

STARTING_TRITETS = {
  '000': 'ANNOTATED_T',
  '001': 'CESR_T_COUNT_CODE',
  '010': 'CESR_T_OP_CODE',
  '011': 'JSON',
  '100': 'MGPK', # fixMap
  '101': 'CBOR', # Map Major Type 5
  '111': 'CESR_B', # count code or op code
}
  

def get_stream_tritet(stream):
  # to bytes
  if not is_bytes(stream):
    stream = stream.encode()
    
  first_byte = stream[0]
  first_bits = byte_to_bits(first_byte)
  first_tritet = first_bits[0:3]

  return (STARTING_TRITETS[first_tritet],first_tritet) 



def parse_json_stream(stream, start=0):
  ## confirm is json:
  kind, _ = get_stream_tritet(stream)
  if kind != 'JSON':
    raise ValueError(f"kind detected{kind}: {stream[:26]}")

  dvers = determine_keri_version(stream)
  if dvers == 1:
    # print(1)
    v_string = stream[6:23]
  else:
    v_string = stream[6:22]
  
  v_info = get_version_string_info(v_string, dvers)
  # print(v_info)
  size = v_info['size']
  this_frame = stream[:size]
  # print(this_frame)
  return {
    'size': size,
    'frame': this_frame,
    'v_info': v_info,
    'start': start,
    'end': start+size
  }
  

