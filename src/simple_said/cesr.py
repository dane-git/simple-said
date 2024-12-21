from simple_said.kutils import (
  byte_to_bits,
  is_bytes,
  determine_keri_version,
  get_version_string_info,
  b64_to_int,
  is_bytes
  
)
import operator

from simple_said.constants import (
  COUNTERS, SIZES, CODEX
)
import pprint
pp = pprint.PrettyPrinter(indent=2, sort_dicts=False)




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
    # print(stream)
    stream = stream.encode()
    
  first_byte = stream[0]
  first_bits = byte_to_bits(first_byte)
  first_tritet = first_bits[0:3]

  return (STARTING_TRITETS[first_tritet],first_tritet) 

# Define a mapping for operators
operator_map = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
    '**': operator.pow,
}
def evaluate_operation(operation_string,base_value):
    # Extract the operator and the number
    operator_symbol = operation_string[0]
    operand = float(operation_string[1:])

    # Look up the operator function
    if operator_symbol in operator_map:
        return operator_map[operator_symbol](base_value, operand)
    else:
        raise ValueError(f"Unsupported operator: {operator_symbol}")


# get counter
# get counter
def get_counter(s):
  if is_bytes(s):
    s = s.decode('utf-8')
  counter_code = s[:2]
  print('counter_code', counter_code)
  if counter_code not in COUNTERS['Counter']:
    print(counter_code in COUNTERS['Counter'], counter_code,s[:100])
    raise ValueError(f"No counter found at stream start {s[:10]}...\n{COUNTERS['Counter']}")
  counter = COUNTERS['Counter'][counter_code]
  counter_size = SIZES['Counter'][counter_code]
  counter['code'] = counter_code
  counter.update(counter_size)
  
  fs = counter['fs']
  ss = counter['ss']
  hs = counter['hs']
  ls = counter['ls']
  full = s[:fs]
  soft = s[hs:ss+hs+ls]
  counter['full'] = full
  counter['soft'] = soft
  counter['num'] = b64_to_int(soft)
  
  if counter['units'] == 'CHAR':
    counter['size'] = int(evaluate_operation(counter['count'], counter['num']))
    counter['length'] = counter['size']
  elif counter['units'] == 'SIGS':
    print(counter)
    counter['size'] = int(evaluate_operation(counter['count'], counter['num']))
    counter['iterations'] = counter['size'] 
  
  # cv = counter['COUNT_VALUE']
  # counter['value'] = COUNT_VALUES[cv]
  print('counter')
  pp.pprint(counter)
  
  # print(counter, 'type' in counter)
  
  return counter



def parse_stream(stream):
    stuff = []
    cursor = 0
    if is_bytes(stream):
        stream = stream.decode('utf-8')

    def parse_json(stream, cursor):
        this= stream[cursor:]
        dvers = determine_keri_version(this)
        if dvers == 1:
        # print(1)
            v_string = this[6:23]
        else:
            v_string = this[6:22]
  
        v_info = get_version_string_info(v_string, dvers)
        size = v_info['size']
        this_obj = {
            'size': size,
            'raw': stream[cursor:cursor+size],
            'v_info': v_info,
            'start': cursor,
            'end': cursor+size
          }
        cursor = cursor+size
        return stream, cursor, this_obj
        
    def parse_cesr_t(stream, cursor):
        struff = []
        
        def parse_sig(stream,cursor):
            options = CODEX['IndexedSig']
            this = stream[cursor:]
            for o in options:
                if o in this[:len(o)]:
                    ## return sig.
                    size = SIZES['Indexer'][o]['fs']
                    return cursor + size, this[:size]
            raise ValueError(f"SIG TYPE NOT FOUND {this[:188]}")
                    
                
        def parse_cesr(stream,cursor, stuff=[]):
            this = stream[cursor:]
            counter = get_counter(this)
            if counter['units'] == 'CHAR':
                counter['size'] = int(evaluate_operation(counter['count'], counter['num']))
                counter['length'] = counter['size']
                end = counter['length']+ cursor
                print(39, stream[cursor:end])
                stuff.append( {
                    'raw': stream[cursor:end] ,
                    'counter': counter,
                    'size': counter['length'],
                    'start': cursor,
                    'end': end,
                    'type': counter['type'] if 'type' in counter else None,
                    'name': counter['name']
                  })
                fs = counter['fs']
                print(fs)
                parse_cesr(stream, cursor+fs)
                
            elif counter['units'] == 'SIGS':
                counter['size'] = int(evaluate_operation(counter['count'], counter['num']))
                counter['iterations'] = counter['size']
                stuff.append(counter)
                cursor += counter['fs']
                sigs = []
                for i in range(counter['iterations']):
                    cursor, sig = parse_sig(stream, cursor)
                    sigs.append(sig)
                stuff.append(sigs)
                print(stuff)
                cursor, stuff= parse_cesr(stream,cursor)
                
                    
            return cursor, stuff
        cursor, stuff = parse_cesr(stream,cursor)
        return cursor, stuff
                    
        
        
    
    def parse(stream, cursor):
        this = stream[cursor:]
        kind, _ = get_stream_tritet(this)
        stuff = []
        if kind == 'JSON':
            stream, cursor, obj = parse_json(stream, cursor)
            stuff.append(obj)
            parse(stream, cursor)
            
        elif kind == 'CESR_T_COUNT_CODE':
            cursor, obj = parse_cesr_t(stream, cursor)
            stuff.append(obj)
            print(stuff)
            parse(stream,cursor)
        
        return stuff
    stuff = parse(stream, 0)
    return stuff