from simple_said.kutils import (
  byte_to_bits,
  is_bytes,
  determine_keri_version,
  get_version_string_info,
  b64_to_int,
  is_bytes,
  dict_to_keri_byte_str,
  deepcopy
  
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
    if len(stream) < 1:
      return ('DONE', 'XXX')
      
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


def parse_json(stream, cursor, everything):
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
        # 'raw': dict_to_keri_byte_str(stream[cursor:cursor+size]),
        'raw': stream[cursor:cursor+size],
        'v_info': v_info,
        'start': cursor,
        'end': cursor+size,
        'ked': True
      }
    cursor = cursor+size
    print('='*88)
    print(this_obj)
    print('='*88)
    everything[this_obj['start']] = this_obj
    return cursor, this_obj, everything
  

def parse_codex(stream,cursor, codex):
    print('codex', codex)
    options = CODEX[codex]
    size_type = 'Indexer'  if 'Index' in codex else 'Matter'
    
    
    this = stream[cursor:]
    for o in options:
        if o in this[:len(o)]:
            ## return sig.
            size = SIZES[size_type][o]['fs']
            # print(o, size_type)
            # print('size', size,this[:44])
            return cursor + size, this[:size]
    raise ValueError(f"SIG TYPE NOT FOUND {this[:188]}")
  
def build_thing(stream, cursor, typ, code, last_codex):
    name = CODEX[typ][code]
    s = stream[cursor:]
    parent = last_codex
    # is_matter = True if 'Index' not in name and 'Index' and code[0] != '-' not in typ else False
    # size_ref = 'Matter' 
    # if not is_matter:
    #   size_ref = 'Indexer' if code[0]!= '-' else 'Counter'
    t = {
      code: CODEX[typ][code],
      'typ': typ,
      'code': code,
      'name': CODEX[typ][code],
      }
    if typ in SIZES:
      t.update(SIZES[typ][code])
    else:
      t.update(SIZES['Matter'][code])
    fs = t['fs']
    ss = t['ss']
    hs = t['hs']
    ls = t['ls']
    t['hs_char'] = s[:hs]
    t['ss_char'] = s[hs:ss+hs]
    t['hs_value'] = b64_to_int(s[:hs]) 
    t['ss_value'] = b64_to_int(s[hs:ss+hs]) 
    t['root_data'] = s[hs+ss:fs]
    t['full_data'] = s[:fs]
    t['start'] = cursor
    t['end'] =  cursor+fs
    t['num'] = b64_to_int(s[hs:fs]) 
    t['ked'] = False
    t['parent_start'] = parent
    if 'Counter' in typ:
      t.update(COUNTERS[typ][code])
      t['is_counter'] = True
    else:
      t['is_counter'] = False
    if 'count' in t:
      t['size'] = int(evaluate_operation(t['count'], t['num']))
    return t

def sniff_codex(stream, cursor, last_codex):
  this = stream[cursor:]
  codexes = []
  if this[0] == '-':
    codexes = ['Counter', 'AltCounter']
  elif 'Counter' in last_codex[0]:
    codexes = ['Indexer','Matter']
  else:
    codexes = [last_codex[0]]
  for codex in codexes:
    these_codexes = CODEX[codex]
    for c in these_codexes:
      if this[:len(c)] == c:
        return codex, c
  print(170,codexes)
  return None, None

def reorganize_attachments(attachments):
  has_attachment_root = False
  attachment_root = None
  reorganized_attachments = {}
  for k in attachments:
    if attachments[k]['name'] == 'AttachedMaterialQuadlets':
      has_attachment_root = True
      attachment_root = k
      break
  if has_attachment_root:
    reorganized_attachments = {}
    reorganized_attachments[attachment_root] = deepcopy(attachments[attachment_root])
    reorganized_attachments[attachment_root]['children'] = {}
    for k in attachments:
      if k != attachment_root:
        reorganized_attachments[attachment_root]['children'][k] = deepcopy(attachments[k])
  else:
    reorganized_attachments = attachments
  return reorganized_attachments

def process_counter(stream, cursor, last_codex):
  
  def process_counter_internals(stream, cursor, last_codex,internals):
    # print(176,stream[cursor])
    nonlocal all_internals
    nonlocal global_cursor
    tritet, tri = get_stream_tritet(stream[cursor:])
    if tritet == 'JSON' or tritet == 'DONE':
      print('END')
      print(len(internals),cursor)
     
      # TODO: is this nesting necessary or just dump as flat with ref to parent?
      reorganized = reorganize_attachments(internals)
      # nonlocal all_internals
      # nonlocal global_cursor
      all_internals = deepcopy(reorganized)
      # all_internals = deepcopy(internals)
      global_cursor = cursor
    else:
      this_codex, this_code = sniff_codex(stream, cursor,last_codex )
      if this_codex is None:
        print(last_codex)
        print(cursor)
        print(len(stream))
        print(stream[cursor:cursor+188])
      thing = build_thing(stream, cursor, this_codex, this_code, last_codex)
      if thing['is_counter'] and thing['context'] == ['CHAR']:
        thing['raw'] = stream[cursor:cursor+thing['fs']+thing['size']]
        thing['raw_end'] = cursor+thing['fs']+thing['size']    
        internals[thing['start']] = thing
        last_codex = (thing['typ'], thing['start'])
        process_counter_internals(stream, cursor+thing['fs'], last_codex,internals)
      elif thing['is_counter']:
        thing['children'] = {}
        stash = []
        current_cursor = cursor+thing['fs']
        _this_codex = (thing['typ'], thing['start'])
        for i in range(thing['size']):
          for context in thing['context']:
            sniffed_codex, sniffed_code = sniff_codex(stream, current_cursor, (context, None))
            context_thing = build_thing(stream,current_cursor, sniffed_codex, sniffed_code, _this_codex)
            current_cursor = context_thing['end']
            thing['children'][context_thing['start']] = context_thing
            stash.append(context_thing)
        thing['raw'] = stream[thing['start']:current_cursor]
        thing['raw_end'] = current_cursor
        internals[thing['start']] = thing
        # for s in stash:
        #   internals[s['start']] = s
      
        process_counter_internals(stream, current_cursor,last_codex, internals)
      else:
        internals[thing['start']] = thing
        tritet, tri = get_stream_tritet(stream[thing['end']:])
        if tritet == 'JSON':
          print('END')
          print(len(internals), thing['end'])
          reorganized= reorganize_attachments(internals)    
          # nonlocal all_internals
          # nonlocal global_cursor
          all_internals = deepcopy(reorganized)
          global_cursor = thing['end']
        
  all_internals = {}
  global_cursor = cursor
  process_counter_internals(stream, cursor, last_codex,internals={})
  return all_internals, global_cursor
    # raise ValueError('END')

def parse_cesr(stream,cursor, last_codex, parent_starts, everything):#, stuff=[]):
    this = stream[cursor:]
    stuff = {}

    kind, _ = get_stream_tritet(this)
    if kind == 'JSON':
      return cursor, stuff, everything
    if kind == 'DONE':
      print('DONE')
      return cursor, stuff, everything
    is_counter =False
    proto_genus = 'STANDARD'
    this_codex = None
    this_code = None
    if this[0] == '-': #and 'Counter' not in last_codex:
      if this[1] == '-':
        ## PROTOGENUS # TODO
        pass

      # codexes = ['Counter', 'AltCounter']
      # codexes = ['Counter', 'Indexer']
      # codexes = ['Matter', 'SmallVarRawSize', 'LargeVarRawSize','NonTrans', 'Num', 'Pre'] 
      
    this_codex, this_code = sniff_codex(stream, cursor, last_codex)
    if 'Counter' in this_codex:
      
      # internals, cursor = process_counter_internals(stream,cursor,parent_starts[-1], {})
      internals, cursor = process_counter(stream,cursor,parent_starts[-1])
      everything[parent_starts[-1][1]]['attachments'] = internals
      # everything.update(internals)

    # last_codex = (thing['typ'], thing['start'])
    # cursor += thing['fs']
    return cursor, everything
    # parse_cesr(stream,cursor, last_codex, parent_starts, everything)
    
    
    
def parse_stream(stream):
    everything = {}
    cursor = 0
    last_codex = None
    parent_starts = []
    if is_bytes(stream):
        stream = stream.decode('utf-8') 
    def parse(stream, cursor):
      nonlocal everything
      nonlocal parent_starts
      nonlocal last_codex
      print(cursor)
      this = stream[cursor:]
      kind, _ = get_stream_tritet(this)
      
      if kind == 'JSON':
          # time.sleep(.1)
          
          cursor, obj, everything = parse_json(stream, cursor, everything)
          # stuff.append(obj)
          print(obj['start'])
          last_codex = 'KED'
          parent_starts = [('KED', obj['start'])]
          print(251, stream[cursor: cursor+50])
          parse(stream, cursor)#, stuff)
          
      elif kind == 'CESR_T_COUNT_CODE':
      
          cursor,everything = parse_cesr(stream, cursor, last_codex, parent_starts,everything)
          # stuff.append(obj)
      
          parse(stream,cursor)#, stuff)
    parse(stream, cursor)
    return everything