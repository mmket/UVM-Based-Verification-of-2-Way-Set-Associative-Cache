#=========================================================================
# CacheFL_test.py
#=========================================================================

import pytest

from random import seed, randint

from pymtl3 import *
from pymtl3.stdlib.mem        import MemMsgType
from pymtl3.stdlib.test_utils import mk_test_case_table

from lab3_mem.test.harness import req, resp, run_test
from lab3_mem.CacheFL      import CacheFL

seed(0xa4e28cc2)

#-------------------------------------------------------------------------
# cmp_wo_test_field
#-------------------------------------------------------------------------
# The test field in the cache response is used to indicate if the
# corresponding memory access resulted in a hit or a miss. However, the
# FL model always sets the test field to zero since it does not track
# hits/misses. So we need to do something special to ignore the test
# field when using the FL model. To do this, we can pass in a specialized
# comparison function to the StreamSinkFL.

def cmp_wo_test_field( msg, ref ):

  if msg.type_ != ref.type_:
    return False

  if msg.len != ref.len:
    return False

  if msg.opaque != msg.opaque:
    return False

  if ref.data != msg.data:
    return False

  # do not check the test field

  return True

#-------------------------------------------------------------------------
# Data
#-------------------------------------------------------------------------
# These functions are used to specify the address/data to preload into
# the main memory before running a test.

# 64B of sequential data

def data_64B():
  return [
    # addr      data
    0x00001000, 0x000c0ffe,
    0x00001004, 0x10101010,
    0x00001008, 0x20202020,
    0x0000100c, 0x30303030,
    0x00001010, 0x40404040,
    0x00001014, 0x50505050,
    0x00001018, 0x60606060,
    0x0000101c, 0x70707070,
    0x00001020, 0x80808080,
    0x00001024, 0x90909090,
    0x00001028, 0xa0a0a0a0,
    0x0000102c, 0xb0b0b0b0,
    0x00001030, 0xc0c0c0c0,
    0x00001034, 0xd0d0d0d0,
    0x00001038, 0xe0e0e0e0,
    0x0000103c, 0xf0f0f0f0,
  ]

# 512B of sequential data

def data_512B():
  data = []
  for i in range(128):
    data.extend([0x00001000+i*4,0xabcd1000+i*4])
  return data

# 1024B of random data

def data_random():
  seed(0xdeadbeef)
  data = []
  for i in range(256):
    data.extend([0x00001000+i*4,randint(0,0xffffffff)])
  return data

#----------------------------------------------------------------------
# Test Cases for Write Init
#----------------------------------------------------------------------

# Just make sure a single write init goes through the memory system.

def write_init_word():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'in', 0x0, 0x1000, 0, 0xdeadbeef ), resp( 'in', 0x0, 0,   0,  0    ),
  ]

# Write init a word multiple times, also tests opaque bits

def write_init_multi_word():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'in', 0x0, 0x1000, 0, 0xdeadbeef ), resp( 'in', 0x0, 0,   0,  0    ),
    req( 'in', 0x1, 0x1000, 0, 0xdeadbeef ), resp( 'in', 0x1, 0,   0,  0    ),
    req( 'in', 0x2, 0x1000, 0, 0xdeadbeef ), resp( 'in', 0x2, 0,   0,  0    ),
    req( 'in', 0x3, 0x1000, 0, 0xdeadbeef ), resp( 'in', 0x3, 0,   0,  0    ),
  ]

# Use write inits for each word in a cache line

def write_init_cacheline():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'in', 0x0, 0x1000, 0, 0x01010101 ), resp( 'in', 0x0, 0,   0,  0    ),
    req( 'in', 0x1, 0x1004, 0, 0x02020202 ), resp( 'in', 0x1, 0,   0,  0    ),
    req( 'in', 0x2, 0x1008, 0, 0x03030303 ), resp( 'in', 0x2, 0,   0,  0    ),
    req( 'in', 0x3, 0x100c, 0, 0x04040404 ), resp( 'in', 0x3, 0,   0,  0    ),
  ]

# Write init one word in each cacheline in half the cache. For the direct
# mapped cache, this will write the first half of all the sets. For the
# set associative cache, this will write all of the sets in the first
# way.

def write_init_multi_cacheline():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'in', 0x0, 0x0000, 0, 0x00000000 ), resp( 'in', 0x0, 0,   0,  0    ),
    req( 'in', 0x1, 0x1010, 0, 0x01010101 ), resp( 'in', 0x1, 0,   0,  0    ),
    req( 'in', 0x2, 0x2020, 0, 0x02020202 ), resp( 'in', 0x2, 0,   0,  0    ),
    req( 'in', 0x3, 0x3030, 0, 0x03030303 ), resp( 'in', 0x3, 0,   0,  0    ),
    req( 'in', 0x4, 0x4040, 0, 0x04040404 ), resp( 'in', 0x4, 0,   0,  0    ),
    req( 'in', 0x5, 0x5050, 0, 0x05050505 ), resp( 'in', 0x5, 0,   0,  0    ),
    req( 'in', 0x6, 0x6060, 0, 0x06060606 ), resp( 'in', 0x6, 0,   0,  0    ),
    req( 'in', 0x7, 0x7070, 0, 0x07070707 ), resp( 'in', 0x7, 0,   0,  0    ),
  ]

#----------------------------------------------------------------------
# Test Cases for Read Hits
#----------------------------------------------------------------------

# Single read hit

def read_hit_word():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'in', 0x0, 0x1000, 0, 0xdeadbeef ), resp( 'in', 0x0, 0,   0,  0          ),
    req( 'rd', 0x0, 0x1000, 0, 0          ), resp( 'rd', 0x0, 1,   0,  0xdeadbeef ),
  ]

# Read same word multiple times, also tests opaque bits

def read_hit_multi_word():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'in', 0x0, 0x1000, 0, 0xdeadbeef ), resp( 'in', 0x0, 0,   0,  0    ),

    req( 'rd', 0x0, 0x1000, 0, 0          ), resp( 'rd', 0x0, 1,   0,  0xdeadbeef ),
    req( 'rd', 0x1, 0x1000, 0, 0          ), resp( 'rd', 0x1, 1,   0,  0xdeadbeef ),
    req( 'rd', 0x2, 0x1000, 0, 0          ), resp( 'rd', 0x2, 1,   0,  0xdeadbeef ),
    req( 'rd', 0x3, 0x1000, 0, 0          ), resp( 'rd', 0x3, 1,   0,  0xdeadbeef ),
  ]

# Read every word in cache line

def read_hit_cacheline():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'in', 0x0, 0x1000, 0, 0x01010101 ), resp( 'in', 0x0, 0,   0,  0    ),
    req( 'in', 0x1, 0x1004, 0, 0x02020202 ), resp( 'in', 0x1, 0,   0,  0    ),
    req( 'in', 0x2, 0x1008, 0, 0x03030303 ), resp( 'in', 0x2, 0,   0,  0    ),
    req( 'in', 0x3, 0x100c, 0, 0x04040404 ), resp( 'in', 0x3, 0,   0,  0    ),

    req( 'rd', 0x4, 0x1000, 0, 0          ), resp( 'rd', 0x4, 1,   0,  0x01010101 ),
    req( 'rd', 0x5, 0x1004, 0, 0          ), resp( 'rd', 0x5, 1,   0,  0x02020202 ),
    req( 'rd', 0x6, 0x1008, 0, 0          ), resp( 'rd', 0x6, 1,   0,  0x03030303 ),
    req( 'rd', 0x7, 0x100c, 0, 0          ), resp( 'rd', 0x7, 1,   0,  0x04040404 ),
  ]

# Read one word from each cacheline

def read_hit_multi_cacheline():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'in', 0x0, 0x0000, 0, 0x00000000 ), resp( 'in', 0x0, 0,   0,  0          ),
    req( 'in', 0x1, 0x1010, 0, 0x01010101 ), resp( 'in', 0x1, 0,   0,  0          ),
    req( 'in', 0x2, 0x2020, 0, 0x02020202 ), resp( 'in', 0x2, 0,   0,  0          ),
    req( 'in', 0x3, 0x3030, 0, 0x03030303 ), resp( 'in', 0x3, 0,   0,  0          ),
    req( 'in', 0x4, 0x4040, 0, 0x04040404 ), resp( 'in', 0x4, 0,   0,  0          ),
    req( 'in', 0x5, 0x5050, 0, 0x05050505 ), resp( 'in', 0x5, 0,   0,  0          ),
    req( 'in', 0x6, 0x6060, 0, 0x06060606 ), resp( 'in', 0x6, 0,   0,  0          ),
    req( 'in', 0x7, 0x7070, 0, 0x07070707 ), resp( 'in', 0x7, 0,   0,  0          ),

    req( 'rd', 0x0, 0x0000, 0, 0          ), resp( 'rd', 0x0, 1,   0,  0x00000000 ),
    req( 'rd', 0x1, 0x1010, 0, 0          ), resp( 'rd', 0x1, 1,   0,  0x01010101 ),
    req( 'rd', 0x2, 0x2020, 0, 0          ), resp( 'rd', 0x2, 1,   0,  0x02020202 ),
    req( 'rd', 0x3, 0x3030, 0, 0          ), resp( 'rd', 0x3, 1,   0,  0x03030303 ),
    req( 'rd', 0x4, 0x4040, 0, 0          ), resp( 'rd', 0x4, 1,   0,  0x04040404 ),
    req( 'rd', 0x5, 0x5050, 0, 0          ), resp( 'rd', 0x5, 1,   0,  0x05050505 ),
    req( 'rd', 0x6, 0x6060, 0, 0          ), resp( 'rd', 0x6, 1,   0,  0x06060606 ),
    req( 'rd', 0x7, 0x7070, 0, 0          ), resp( 'rd', 0x7, 1,   0,  0x07070707 ),
  ]

#----------------------------------------------------------------------
# Test Cases for Write Hits
#----------------------------------------------------------------------

# Single write hit to one word

def write_hit_word():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'in', 0x0, 0x1000, 0, 0xdeadbeef ), resp( 'in', 0x0, 0,   0,  0          ),
    req( 'wr', 0x0, 0x1000, 0, 0xcafecafe ), resp( 'wr', 0x0, 1,   0,  0          ),
    req( 'rd', 0x0, 0x1000, 0, 0          ), resp( 'rd', 0x0, 1,   0,  0xcafecafe ),
  ]

# Write/read word multiple times, also tests opaque bits

def write_hit_multi_word():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'in', 0x0, 0x1000, 0, 0xdeadbeef ), resp( 'in', 0x0, 0,   0,  0          ),

    req( 'wr', 0x1, 0x1000, 0, 0x01010101 ), resp( 'wr', 0x1, 1,   0,  0          ),
    req( 'rd', 0x2, 0x1000, 0, 0          ), resp( 'rd', 0x2, 1,   0,  0x01010101 ),
    req( 'wr', 0x3, 0x1000, 0, 0x02020202 ), resp( 'wr', 0x3, 1,   0,  0          ),
    req( 'rd', 0x4, 0x1000, 0, 0          ), resp( 'rd', 0x4, 1,   0,  0x02020202 ),
    req( 'wr', 0x5, 0x1000, 0, 0x03030303 ), resp( 'wr', 0x5, 1,   0,  0          ),
    req( 'rd', 0x6, 0x1000, 0, 0          ), resp( 'rd', 0x6, 1,   0,  0x03030303 ),
    req( 'wr', 0x7, 0x1000, 0, 0x04040404 ), resp( 'wr', 0x7, 1,   0,  0          ),
    req( 'rd', 0x8, 0x1000, 0, 0          ), resp( 'rd', 0x8, 1,   0,  0x04040404 ),
  ]

# Write/read every word in cache line

def write_hit_cacheline():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'in', 0x0, 0x1000, 0, 0x01010101 ), resp( 'in', 0x0, 0,   0,  0          ),
    req( 'in', 0x0, 0x1004, 0, 0x02020202 ), resp( 'in', 0x0, 0,   0,  0          ),
    req( 'in', 0x0, 0x1008, 0, 0x03030303 ), resp( 'in', 0x0, 0,   0,  0          ),
    req( 'in', 0x0, 0x100c, 0, 0x04040404 ), resp( 'in', 0x0, 0,   0,  0          ),

    req( 'wr', 0x1, 0x1000, 0, 0x01010101 ), resp( 'wr', 0x1, 1,   0,  0          ),
    req( 'wr', 0x3, 0x1004, 0, 0x02020202 ), resp( 'wr', 0x3, 1,   0,  0          ),
    req( 'wr', 0x5, 0x1008, 0, 0x03030303 ), resp( 'wr', 0x5, 1,   0,  0          ),
    req( 'wr', 0x7, 0x100c, 0, 0x04040404 ), resp( 'wr', 0x7, 1,   0,  0          ),

    req( 'rd', 0x2, 0x1000, 0, 0          ), resp( 'rd', 0x2, 1,   0,  0x01010101 ),
    req( 'rd', 0x4, 0x1004, 0, 0          ), resp( 'rd', 0x4, 1,   0,  0x02020202 ),
    req( 'rd', 0x6, 0x1008, 0, 0          ), resp( 'rd', 0x6, 1,   0,  0x03030303 ),
    req( 'rd', 0x8, 0x100c, 0, 0          ), resp( 'rd', 0x8, 1,   0,  0x04040404 ),
  ]

# Write/read one word from each cacheline

def write_hit_multi_cacheline():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'in', 0x0, 0x0000, 0, 0x00000000 ), resp( 'in', 0x0, 0,   0,  0          ),
    req( 'in', 0x1, 0x1010, 0, 0x01010101 ), resp( 'in', 0x1, 0,   0,  0          ),
    req( 'in', 0x2, 0x2020, 0, 0x02020202 ), resp( 'in', 0x2, 0,   0,  0          ),
    req( 'in', 0x3, 0x3030, 0, 0x03030303 ), resp( 'in', 0x3, 0,   0,  0          ),
    req( 'in', 0x4, 0x4040, 0, 0x04040404 ), resp( 'in', 0x4, 0,   0,  0          ),
    req( 'in', 0x5, 0x5050, 0, 0x05050505 ), resp( 'in', 0x5, 0,   0,  0          ),
    req( 'in', 0x6, 0x6060, 0, 0x06060606 ), resp( 'in', 0x6, 0,   0,  0          ),
    req( 'in', 0x7, 0x7070, 0, 0x07070707 ), resp( 'in', 0x7, 0,   0,  0          ),

    req( 'wr', 0x0, 0x0000, 0, 0x10101010 ), resp( 'wr', 0x0, 1,   0,  0          ),
    req( 'wr', 0x1, 0x1010, 0, 0x11111111 ), resp( 'wr', 0x1, 1,   0,  0          ),
    req( 'wr', 0x2, 0x2020, 0, 0x12121212 ), resp( 'wr', 0x2, 1,   0,  0          ),
    req( 'wr', 0x3, 0x3030, 0, 0x13131313 ), resp( 'wr', 0x3, 1,   0,  0          ),
    req( 'wr', 0x4, 0x4040, 0, 0x14141414 ), resp( 'wr', 0x4, 1,   0,  0          ),
    req( 'wr', 0x5, 0x5050, 0, 0x15151515 ), resp( 'wr', 0x5, 1,   0,  0          ),
    req( 'wr', 0x6, 0x6060, 0, 0x16161616 ), resp( 'wr', 0x6, 1,   0,  0          ),
    req( 'wr', 0x7, 0x7070, 0, 0x17171717 ), resp( 'wr', 0x7, 1,   0,  0          ),

    req( 'rd', 0x0, 0x0000, 0, 0          ), resp( 'rd', 0x0, 1,   0,  0x10101010 ),
    req( 'rd', 0x1, 0x1010, 0, 0          ), resp( 'rd', 0x1, 1,   0,  0x11111111 ),
    req( 'rd', 0x2, 0x2020, 0, 0          ), resp( 'rd', 0x2, 1,   0,  0x12121212 ),
    req( 'rd', 0x3, 0x3030, 0, 0          ), resp( 'rd', 0x3, 1,   0,  0x13131313 ),
    req( 'rd', 0x4, 0x4040, 0, 0          ), resp( 'rd', 0x4, 1,   0,  0x14141414 ),
    req( 'rd', 0x5, 0x5050, 0, 0          ), resp( 'rd', 0x5, 1,   0,  0x15151515 ),
    req( 'rd', 0x6, 0x6060, 0, 0          ), resp( 'rd', 0x6, 1,   0,  0x16161616 ),
    req( 'rd', 0x7, 0x7070, 0, 0          ), resp( 'rd', 0x7, 1,   0,  0x17171717 ),
  ]

#----------------------------------------------------------------------
# Test Cases for Refill on Read Miss
#----------------------------------------------------------------------

# Single read miss (uses data_64B)

def read_miss_word():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'rd', 0x0, 0x1000, 0, 0          ), resp( 'rd', 0x0, 0,   0,  0x000c0ffe ),
  ]

# Read same word multiple times, also tests opaque bits (uses data_64B)

def read_miss_multi_word():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'rd', 0x0, 0x1000, 0, 0          ), resp( 'rd', 0x0, 0,   0,  0x000c0ffe ),
    req( 'rd', 0x1, 0x1000, 0, 0          ), resp( 'rd', 0x1, 1,   0,  0x000c0ffe ),
    req( 'rd', 0x2, 0x1000, 0, 0          ), resp( 'rd', 0x2, 1,   0,  0x000c0ffe ),
    req( 'rd', 0x3, 0x1000, 0, 0          ), resp( 'rd', 0x3, 1,   0,  0x000c0ffe ),
  ]

# Read every word in cache line (uses data_64B)

def read_miss_cacheline():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'rd', 0x1, 0x1000, 0, 0          ), resp( 'rd', 0x1, 0,   0,  0x000c0ffe ),
    req( 'rd', 0x2, 0x1004, 0, 0          ), resp( 'rd', 0x2, 1,   0,  0x10101010 ),
    req( 'rd', 0x3, 0x1008, 0, 0          ), resp( 'rd', 0x3, 1,   0,  0x20202020 ),
    req( 'rd', 0x4, 0x100c, 0, 0          ), resp( 'rd', 0x4, 1,   0,  0x30303030 ),
  ]

# Read miss for each cacheline, then read hit for each cacheline (uses data_512B)

def read_miss_multi_cacheline():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'rd', 0x0, 0x1000, 0, 0          ), resp( 'rd', 0x0, 0,   0,  0xabcd1000 ),
    req( 'rd', 0x1, 0x1010, 0, 0          ), resp( 'rd', 0x1, 0,   0,  0xabcd1010 ),
    req( 'rd', 0x2, 0x1020, 0, 0          ), resp( 'rd', 0x2, 0,   0,  0xabcd1020 ),
    req( 'rd', 0x3, 0x1030, 0, 0          ), resp( 'rd', 0x3, 0,   0,  0xabcd1030 ),
    req( 'rd', 0x4, 0x1040, 0, 0          ), resp( 'rd', 0x4, 0,   0,  0xabcd1040 ),
    req( 'rd', 0x5, 0x1050, 0, 0          ), resp( 'rd', 0x5, 0,   0,  0xabcd1050 ),
    req( 'rd', 0x6, 0x1060, 0, 0          ), resp( 'rd', 0x6, 0,   0,  0xabcd1060 ),
    req( 'rd', 0x7, 0x1070, 0, 0          ), resp( 'rd', 0x7, 0,   0,  0xabcd1070 ),
    req( 'rd', 0x8, 0x1080, 0, 0          ), resp( 'rd', 0x8, 0,   0,  0xabcd1080 ),
    req( 'rd', 0x9, 0x1090, 0, 0          ), resp( 'rd', 0x9, 0,   0,  0xabcd1090 ),
    req( 'rd', 0xa, 0x10a0, 0, 0          ), resp( 'rd', 0xa, 0,   0,  0xabcd10a0 ),
    req( 'rd', 0xb, 0x10b0, 0, 0          ), resp( 'rd', 0xb, 0,   0,  0xabcd10b0 ),
    req( 'rd', 0xc, 0x10c0, 0, 0          ), resp( 'rd', 0xc, 0,   0,  0xabcd10c0 ),
    req( 'rd', 0xd, 0x10d0, 0, 0          ), resp( 'rd', 0xd, 0,   0,  0xabcd10d0 ),
    req( 'rd', 0xe, 0x10e0, 0, 0          ), resp( 'rd', 0xe, 0,   0,  0xabcd10e0 ),
    req( 'rd', 0xf, 0x10f0, 0, 0          ), resp( 'rd', 0xf, 0,   0,  0xabcd10f0 ),

    req( 'rd', 0x0, 0x1000, 0, 0          ), resp( 'rd', 0x0, 1,   0,  0xabcd1000 ),
    req( 'rd', 0x1, 0x1010, 0, 0          ), resp( 'rd', 0x1, 1,   0,  0xabcd1010 ),
    req( 'rd', 0x2, 0x1020, 0, 0          ), resp( 'rd', 0x2, 1,   0,  0xabcd1020 ),
    req( 'rd', 0x3, 0x1030, 0, 0          ), resp( 'rd', 0x3, 1,   0,  0xabcd1030 ),
    req( 'rd', 0x4, 0x1040, 0, 0          ), resp( 'rd', 0x4, 1,   0,  0xabcd1040 ),
    req( 'rd', 0x5, 0x1050, 0, 0          ), resp( 'rd', 0x5, 1,   0,  0xabcd1050 ),
    req( 'rd', 0x6, 0x1060, 0, 0          ), resp( 'rd', 0x6, 1,   0,  0xabcd1060 ),
    req( 'rd', 0x7, 0x1070, 0, 0          ), resp( 'rd', 0x7, 1,   0,  0xabcd1070 ),
    req( 'rd', 0x8, 0x1080, 0, 0          ), resp( 'rd', 0x8, 1,   0,  0xabcd1080 ),
    req( 'rd', 0x9, 0x1090, 0, 0          ), resp( 'rd', 0x9, 1,   0,  0xabcd1090 ),
    req( 'rd', 0xa, 0x10a0, 0, 0          ), resp( 'rd', 0xa, 1,   0,  0xabcd10a0 ),
    req( 'rd', 0xb, 0x10b0, 0, 0          ), resp( 'rd', 0xb, 1,   0,  0xabcd10b0 ),
    req( 'rd', 0xc, 0x10c0, 0, 0          ), resp( 'rd', 0xc, 1,   0,  0xabcd10c0 ),
    req( 'rd', 0xd, 0x10d0, 0, 0          ), resp( 'rd', 0xd, 1,   0,  0xabcd10d0 ),
    req( 'rd', 0xe, 0x10e0, 0, 0          ), resp( 'rd', 0xe, 1,   0,  0xabcd10e0 ),
    req( 'rd', 0xf, 0x10f0, 0, 0          ), resp( 'rd', 0xf, 1,   0,  0xabcd10f0 ),

    req( 'rd', 0x0, 0x1004, 0, 0          ), resp( 'rd', 0x0, 1,   0,  0xabcd1004 ),
    req( 'rd', 0x1, 0x1014, 0, 0          ), resp( 'rd', 0x1, 1,   0,  0xabcd1014 ),
    req( 'rd', 0x2, 0x1024, 0, 0          ), resp( 'rd', 0x2, 1,   0,  0xabcd1024 ),
    req( 'rd', 0x3, 0x1034, 0, 0          ), resp( 'rd', 0x3, 1,   0,  0xabcd1034 ),
    req( 'rd', 0x4, 0x1044, 0, 0          ), resp( 'rd', 0x4, 1,   0,  0xabcd1044 ),
    req( 'rd', 0x5, 0x1054, 0, 0          ), resp( 'rd', 0x5, 1,   0,  0xabcd1054 ),
    req( 'rd', 0x6, 0x1064, 0, 0          ), resp( 'rd', 0x6, 1,   0,  0xabcd1064 ),
    req( 'rd', 0x7, 0x1074, 0, 0          ), resp( 'rd', 0x7, 1,   0,  0xabcd1074 ),
    req( 'rd', 0x8, 0x1084, 0, 0          ), resp( 'rd', 0x8, 1,   0,  0xabcd1084 ),
    req( 'rd', 0x9, 0x1094, 0, 0          ), resp( 'rd', 0x9, 1,   0,  0xabcd1094 ),
    req( 'rd', 0xa, 0x10a4, 0, 0          ), resp( 'rd', 0xa, 1,   0,  0xabcd10a4 ),
    req( 'rd', 0xb, 0x10b4, 0, 0          ), resp( 'rd', 0xb, 1,   0,  0xabcd10b4 ),
    req( 'rd', 0xc, 0x10c4, 0, 0          ), resp( 'rd', 0xc, 1,   0,  0xabcd10c4 ),
    req( 'rd', 0xd, 0x10d4, 0, 0          ), resp( 'rd', 0xd, 1,   0,  0xabcd10d4 ),
    req( 'rd', 0xe, 0x10e4, 0, 0          ), resp( 'rd', 0xe, 1,   0,  0xabcd10e4 ),
    req( 'rd', 0xf, 0x10f4, 0, 0          ), resp( 'rd', 0xf, 1,   0,  0xabcd10f4 ),
  ]

#----------------------------------------------------------------------
# Test Cases for Refill on Write Miss
#----------------------------------------------------------------------

# Single write miss to one word (uses data_64B)

def write_miss_word():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'wr', 0x0, 0x1000, 0, 0xcafecafe ), resp( 'wr', 0x0, 0,   0,  0          ),
    req( 'rd', 0x0, 0x1000, 0, 0          ), resp( 'rd', 0x0, 1,   0,  0xcafecafe ),
  ]

# Write/read word multiple times, also tests opaque bits (uses data_64B)

def write_miss_multi_word():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'wr', 0x1, 0x1000, 0, 0x01010101 ), resp( 'wr', 0x1, 0,   0,  0          ),
    req( 'rd', 0x2, 0x1000, 0, 0          ), resp( 'rd', 0x2, 1,   0,  0x01010101 ),
    req( 'wr', 0x3, 0x1000, 0, 0x02020202 ), resp( 'wr', 0x3, 1,   0,  0          ),
    req( 'rd', 0x4, 0x1000, 0, 0          ), resp( 'rd', 0x4, 1,   0,  0x02020202 ),
    req( 'wr', 0x5, 0x1000, 0, 0x03030303 ), resp( 'wr', 0x5, 1,   0,  0          ),
    req( 'rd', 0x6, 0x1000, 0, 0          ), resp( 'rd', 0x6, 1,   0,  0x03030303 ),
    req( 'wr', 0x7, 0x1000, 0, 0x04040404 ), resp( 'wr', 0x7, 1,   0,  0          ),
    req( 'rd', 0x8, 0x1000, 0, 0          ), resp( 'rd', 0x8, 1,   0,  0x04040404 ),
  ]

# Write/read every word in cache line (uses data_64B)

def write_miss_cacheline():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'wr', 0x1, 0x1000, 0, 0x01010101 ), resp( 'wr', 0x1, 0,   0,  0          ),
    req( 'wr', 0x2, 0x1004, 0, 0x02020202 ), resp( 'wr', 0x2, 1,   0,  0          ),
    req( 'wr', 0x3, 0x1008, 0, 0x03030303 ), resp( 'wr', 0x3, 1,   0,  0          ),
    req( 'wr', 0x4, 0x100c, 0, 0x04040404 ), resp( 'wr', 0x4, 1,   0,  0          ),

    req( 'rd', 0x5, 0x1000, 0, 0          ), resp( 'rd', 0x5, 1,   0,  0x01010101 ),
    req( 'rd', 0x6, 0x1004, 0, 0          ), resp( 'rd', 0x6, 1,   0,  0x02020202 ),
    req( 'rd', 0x7, 0x1008, 0, 0          ), resp( 'rd', 0x7, 1,   0,  0x03030303 ),
    req( 'rd', 0x8, 0x100c, 0, 0          ), resp( 'rd', 0x8, 1,   0,  0x04040404 ),
  ]

# Write/read one word from each cacheline (uses data_512B)

def write_miss_multi_cacheline():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'wr', 0x0, 0x1000, 0, 0x10101010 ), resp( 'wr', 0x0, 0,   0,  0          ),
    req( 'wr', 0x1, 0x1010, 0, 0x11111111 ), resp( 'wr', 0x1, 0,   0,  0          ),
    req( 'wr', 0x2, 0x1020, 0, 0x12121212 ), resp( 'wr', 0x2, 0,   0,  0          ),
    req( 'wr', 0x3, 0x1030, 0, 0x13131313 ), resp( 'wr', 0x3, 0,   0,  0          ),
    req( 'wr', 0x4, 0x1040, 0, 0x14141414 ), resp( 'wr', 0x4, 0,   0,  0          ),
    req( 'wr', 0x5, 0x1050, 0, 0x15151515 ), resp( 'wr', 0x5, 0,   0,  0          ),
    req( 'wr', 0x6, 0x1060, 0, 0x16161616 ), resp( 'wr', 0x6, 0,   0,  0          ),
    req( 'wr', 0x7, 0x1070, 0, 0x17171717 ), resp( 'wr', 0x7, 0,   0,  0          ),
    req( 'wr', 0x8, 0x1080, 0, 0x18181818 ), resp( 'wr', 0x8, 0,   0,  0          ),
    req( 'wr', 0x9, 0x1090, 0, 0x19191919 ), resp( 'wr', 0x9, 0,   0,  0          ),
    req( 'wr', 0xa, 0x10a0, 0, 0x1a1a1a1a ), resp( 'wr', 0xa, 0,   0,  0          ),
    req( 'wr', 0xb, 0x10b0, 0, 0x1b1b1b1b ), resp( 'wr', 0xb, 0,   0,  0          ),
    req( 'wr', 0xc, 0x10c0, 0, 0x1c1c1c1c ), resp( 'wr', 0xc, 0,   0,  0          ),
    req( 'wr', 0xd, 0x10d0, 0, 0x1d1d1d1d ), resp( 'wr', 0xd, 0,   0,  0          ),
    req( 'wr', 0xe, 0x10e0, 0, 0x1e1e1e1e ), resp( 'wr', 0xe, 0,   0,  0          ),
    req( 'wr', 0xf, 0x10f0, 0, 0x1f1f1f1f ), resp( 'wr', 0xf, 0,   0,  0          ),

    req( 'rd', 0x0, 0x1000, 0, 0          ), resp( 'rd', 0x0, 1,   0,  0x10101010 ),
    req( 'rd', 0x1, 0x1010, 0, 0          ), resp( 'rd', 0x1, 1,   0,  0x11111111 ),
    req( 'rd', 0x2, 0x1020, 0, 0          ), resp( 'rd', 0x2, 1,   0,  0x12121212 ),
    req( 'rd', 0x3, 0x1030, 0, 0          ), resp( 'rd', 0x3, 1,   0,  0x13131313 ),
    req( 'rd', 0x4, 0x1040, 0, 0          ), resp( 'rd', 0x4, 1,   0,  0x14141414 ),
    req( 'rd', 0x5, 0x1050, 0, 0          ), resp( 'rd', 0x5, 1,   0,  0x15151515 ),
    req( 'rd', 0x6, 0x1060, 0, 0          ), resp( 'rd', 0x6, 1,   0,  0x16161616 ),
    req( 'rd', 0x7, 0x1070, 0, 0          ), resp( 'rd', 0x7, 1,   0,  0x17171717 ),
    req( 'rd', 0x8, 0x1080, 0, 0          ), resp( 'rd', 0x8, 1,   0,  0x18181818 ),
    req( 'rd', 0x9, 0x1090, 0, 0          ), resp( 'rd', 0x9, 1,   0,  0x19191919 ),
    req( 'rd', 0xa, 0x10a0, 0, 0          ), resp( 'rd', 0xa, 1,   0,  0x1a1a1a1a ),
    req( 'rd', 0xb, 0x10b0, 0, 0          ), resp( 'rd', 0xb, 1,   0,  0x1b1b1b1b ),
    req( 'rd', 0xc, 0x10c0, 0, 0          ), resp( 'rd', 0xc, 1,   0,  0x1c1c1c1c ),
    req( 'rd', 0xd, 0x10d0, 0, 0          ), resp( 'rd', 0xd, 1,   0,  0x1d1d1d1d ),
    req( 'rd', 0xe, 0x10e0, 0, 0          ), resp( 'rd', 0xe, 1,   0,  0x1e1e1e1e ),
    req( 'rd', 0xf, 0x10f0, 0, 0          ), resp( 'rd', 0xf, 1,   0,  0x1f1f1f1f ),
  ]


def read_miss_with_refill_and_eviction():
  return [
    req('rd', 0x0, 0x1000, 0, 0), resp('rd', 0x0, 0, 0, 0xabcd1000),
    req('rd', 0x1, 0x1100, 0, 0), resp('rd', 0x1, 0, 0, 0xabcd1100),
    req('rd', 0x2, 0x1200, 0, 0), resp('rd', 0x2, 0, 0, 0xabcd1200),
    req('rd', 0x3, 0x1300, 0, 0), resp('rd', 0x3, 0, 0, 0xabcd1300),
    req('rd', 0x4, 0x1000, 0, 0), resp('rd', 0x4, 0, 0, 0xabcd1000),
    req('rd', 0x5, 0x1100, 0, 0), resp('rd', 0x5, 0, 0, 0xabcd1100),
    req('rd', 0x6, 0x1200, 0, 0), resp('rd', 0x6, 0, 0, 0xabcd1200),
    req('rd', 0x7, 0x1300, 0, 0), resp('rd', 0x7, 0, 0, 0xabcd1300),
  ]

#----------------------------------------------------------------------
# Test Cases for Evict
#----------------------------------------------------------------------

# Write miss to two cachelines, and then a read to a third cacheline.
# This read to the third cacheline is guaranteed to cause an eviction on
# both the direct mapped and set associative caches. (uses data_512B)

def evict_word():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'wr', 0x0, 0x1000, 0, 0xcafecafe ), resp( 'wr', 0x0, 0,   0,  0          ),
    req( 'rd', 0x0, 0x1000, 0, 0          ), resp( 'rd', 0x0, 1,   0,  0xcafecafe ),
    req( 'wr', 0x0, 0x1080, 0, 0x000c0ffe ), resp( 'wr', 0x0, 0,   0,  0          ),
    req( 'rd', 0x0, 0x1080, 0, 0          ), resp( 'rd', 0x0, 1,   0,  0x000c0ffe ),
    req( 'rd', 0x0, 0x1100, 0, 0          ), resp( 'rd', 0x0, 0,   0,  0xabcd1100 ), # conflicts
    req( 'rd', 0x0, 0x1000, 0, 0          ), resp( 'rd', 0x0, 0,   0,  0xcafecafe ),
  ]

# Write word and evict multiple times. Test is carefully crafted to
# ensure it applies to both direct mapped and set associative caches.
# (uses data_512B)

def evict_multi_word():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'wr', 0x0, 0x1000, 0, 0x01010101 ), resp( 'wr', 0x0, 0,   0,  0          ),
    req( 'rd', 0x1, 0x1000, 0, 0          ), resp( 'rd', 0x1, 1,   0,  0x01010101 ),
    req( 'wr', 0x2, 0x1080, 0, 0x11111111 ), resp( 'wr', 0x2, 0,   0,  0          ),
    req( 'rd', 0x3, 0x1080, 0, 0          ), resp( 'rd', 0x3, 1,   0,  0x11111111 ),
    req( 'rd', 0x4, 0x1100, 0, 0          ), resp( 'rd', 0x4, 0,   0,  0xabcd1100 ), # conflicts
    req( 'rd', 0x5, 0x1080, 0, 0          ), resp( 'rd', 0x5, 1,   0,  0x11111111 ), # make sure way1 is still LRU

    req( 'wr', 0x6, 0x1000, 0, 0x02020202 ), resp( 'wr', 0x6, 0,   0,  0          ),
    req( 'rd', 0x7, 0x1000, 0, 0          ), resp( 'rd', 0x7, 1,   0,  0x02020202 ),
    req( 'wr', 0x8, 0x1080, 0, 0x12121212 ), resp( 'wr', 0x8, 1,   0,  0          ),
    req( 'rd', 0x9, 0x1080, 0, 0          ), resp( 'rd', 0x9, 1,   0,  0x12121212 ),
    req( 'rd', 0xa, 0x1100, 0, 0          ), resp( 'rd', 0xa, 0,   0,  0xabcd1100 ), # conflicts
    req( 'rd', 0xb, 0x1080, 0, 0          ), resp( 'rd', 0xb, 1,   0,  0x12121212 ), # make sure way1 is still LRU

    req( 'wr', 0xc, 0x1000, 0, 0x03030303 ), resp( 'wr', 0xc, 0,   0,  0          ),
    req( 'rd', 0xd, 0x1000, 0, 0          ), resp( 'rd', 0xd, 1,   0,  0x03030303 ),
    req( 'wr', 0xe, 0x1080, 0, 0x13131313 ), resp( 'wr', 0xe, 1,   0,  0          ),
    req( 'rd', 0xf, 0x1080, 0, 0          ), resp( 'rd', 0xf, 1,   0,  0x13131313 ),
    req( 'rd', 0x0, 0x1100, 0, 0          ), resp( 'rd', 0x0, 0,   0,  0xabcd1100 ), # conflicts
    req( 'rd', 0x1, 0x1080, 0, 0          ), resp( 'rd', 0x1, 1,   0,  0x13131313 ), # make sure way1 is still LRU

    req( 'wr', 0x2, 0x1000, 0, 0x04040404 ), resp( 'wr', 0x2, 0,   0,  0          ),
    req( 'rd', 0x3, 0x1000, 0, 0          ), resp( 'rd', 0x3, 1,   0,  0x04040404 ),
    req( 'wr', 0x4, 0x1080, 0, 0x14141414 ), resp( 'wr', 0x4, 1,   0,  0          ),
    req( 'rd', 0x5, 0x1080, 0, 0          ), resp( 'rd', 0x5, 1,   0,  0x14141414 ),
    req( 'rd', 0x6, 0x1100, 0, 0          ), resp( 'rd', 0x6, 0,   0,  0xabcd1100 ), # conflicts
    req( 'rd', 0x7, 0x1080, 0, 0          ), resp( 'rd', 0x7, 1,   0,  0x14141414 ), # make sure way1 is still LRU

    req( 'rd', 0x8, 0x1000, 0, 0          ), resp( 'rd', 0x8, 0,   0,  0x04040404 ),
  ]

# Write every word on two cachelines, and then a read to a third
# cacheline. This read to the third cacheline is guaranteed to cause an
# eviction on both the direct mapped and set associative caches. (uses
# data_512B)

def evict_cacheline():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'wr', 0x0, 0x1000, 0, 0x01010101 ), resp( 'wr', 0x0, 0,   0,  0          ),
    req( 'wr', 0x1, 0x1004, 0, 0x02020202 ), resp( 'wr', 0x1, 1,   0,  0          ),
    req( 'wr', 0x2, 0x1008, 0, 0x03030303 ), resp( 'wr', 0x2, 1,   0,  0          ),
    req( 'wr', 0x3, 0x100c, 0, 0x04040404 ), resp( 'wr', 0x3, 1,   0,  0          ),

    req( 'wr', 0x4, 0x1080, 0, 0x11111111 ), resp( 'wr', 0x4, 0,   0,  0          ),
    req( 'wr', 0x5, 0x1084, 0, 0x12121212 ), resp( 'wr', 0x5, 1,   0,  0          ),
    req( 'wr', 0x6, 0x1088, 0, 0x13131313 ), resp( 'wr', 0x6, 1,   0,  0          ),
    req( 'wr', 0x7, 0x108c, 0, 0x14141414 ), resp( 'wr', 0x7, 1,   0,  0          ),

    req( 'rd', 0x8, 0x1100, 0, 0          ), resp( 'rd', 0x8, 0,   0,  0xabcd1100 ), # conflicts

    req( 'rd', 0x9, 0x1000, 0, 0          ), resp( 'rd', 0x9, 0,   0,  0x01010101 ),
    req( 'rd', 0xa, 0x1004, 0, 0          ), resp( 'rd', 0xa, 1,   0,  0x02020202 ),
    req( 'rd', 0xb, 0x1008, 0, 0          ), resp( 'rd', 0xb, 1,   0,  0x03030303 ),
    req( 'rd', 0xc, 0x100c, 0, 0          ), resp( 'rd', 0xc, 1,   0,  0x04040404 ),
  ]

# Write one word from each cacheline, then evict (uses data_512B)

def evict_multi_cacheline():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'wr', 0x0, 0x1000, 0, 0x10101010 ), resp( 'wr', 0x0, 0,   0,  0          ),
    req( 'wr', 0x1, 0x1010, 0, 0x11111111 ), resp( 'wr', 0x1, 0,   0,  0          ),
    req( 'wr', 0x2, 0x1020, 0, 0x12121212 ), resp( 'wr', 0x2, 0,   0,  0          ),
    req( 'wr', 0x3, 0x1030, 0, 0x13131313 ), resp( 'wr', 0x3, 0,   0,  0          ),
    req( 'wr', 0x4, 0x1040, 0, 0x14141414 ), resp( 'wr', 0x4, 0,   0,  0          ),
    req( 'wr', 0x5, 0x1050, 0, 0x15151515 ), resp( 'wr', 0x5, 0,   0,  0          ),
    req( 'wr', 0x6, 0x1060, 0, 0x16161616 ), resp( 'wr', 0x6, 0,   0,  0          ),
    req( 'wr', 0x7, 0x1070, 0, 0x17171717 ), resp( 'wr', 0x7, 0,   0,  0          ),
    req( 'wr', 0x8, 0x1080, 0, 0x18181818 ), resp( 'wr', 0x8, 0,   0,  0          ),
    req( 'wr', 0x9, 0x1090, 0, 0x19191919 ), resp( 'wr', 0x9, 0,   0,  0          ),
    req( 'wr', 0xa, 0x10a0, 0, 0x1a1a1a1a ), resp( 'wr', 0xa, 0,   0,  0          ),
    req( 'wr', 0xb, 0x10b0, 0, 0x1b1b1b1b ), resp( 'wr', 0xb, 0,   0,  0          ),
    req( 'wr', 0xc, 0x10c0, 0, 0x1c1c1c1c ), resp( 'wr', 0xc, 0,   0,  0          ),
    req( 'wr', 0xd, 0x10d0, 0, 0x1d1d1d1d ), resp( 'wr', 0xd, 0,   0,  0          ),
    req( 'wr', 0xe, 0x10e0, 0, 0x1e1e1e1e ), resp( 'wr', 0xe, 0,   0,  0          ),
    req( 'wr', 0xf, 0x10f0, 0, 0x1f1f1f1f ), resp( 'wr', 0xf, 0,   0,  0          ),

    req( 'rd', 0x0, 0x1000, 0, 0          ), resp( 'rd', 0x0, 1,   0,  0x10101010 ),
    req( 'rd', 0x1, 0x1010, 0, 0          ), resp( 'rd', 0x1, 1,   0,  0x11111111 ),
    req( 'rd', 0x2, 0x1020, 0, 0          ), resp( 'rd', 0x2, 1,   0,  0x12121212 ),
    req( 'rd', 0x3, 0x1030, 0, 0          ), resp( 'rd', 0x3, 1,   0,  0x13131313 ),
    req( 'rd', 0x4, 0x1040, 0, 0          ), resp( 'rd', 0x4, 1,   0,  0x14141414 ),
    req( 'rd', 0x5, 0x1050, 0, 0          ), resp( 'rd', 0x5, 1,   0,  0x15151515 ),
    req( 'rd', 0x6, 0x1060, 0, 0          ), resp( 'rd', 0x6, 1,   0,  0x16161616 ),
    req( 'rd', 0x7, 0x1070, 0, 0          ), resp( 'rd', 0x7, 1,   0,  0x17171717 ),
    req( 'rd', 0x8, 0x1080, 0, 0          ), resp( 'rd', 0x8, 1,   0,  0x18181818 ),
    req( 'rd', 0x9, 0x1090, 0, 0          ), resp( 'rd', 0x9, 1,   0,  0x19191919 ),
    req( 'rd', 0xa, 0x10a0, 0, 0          ), resp( 'rd', 0xa, 1,   0,  0x1a1a1a1a ),
    req( 'rd', 0xb, 0x10b0, 0, 0          ), resp( 'rd', 0xb, 1,   0,  0x1b1b1b1b ),
    req( 'rd', 0xc, 0x10c0, 0, 0          ), resp( 'rd', 0xc, 1,   0,  0x1c1c1c1c ),
    req( 'rd', 0xd, 0x10d0, 0, 0          ), resp( 'rd', 0xd, 1,   0,  0x1d1d1d1d ),
    req( 'rd', 0xe, 0x10e0, 0, 0          ), resp( 'rd', 0xe, 1,   0,  0x1e1e1e1e ),
    req( 'rd', 0xf, 0x10f0, 0, 0          ), resp( 'rd', 0xf, 1,   0,  0x1f1f1f1f ),

    req( 'rd', 0x0, 0x1100, 0, 0          ), resp( 'rd', 0x0, 0,   0,  0xabcd1100 ), # conflicts
    req( 'rd', 0x1, 0x1110, 0, 0          ), resp( 'rd', 0x1, 0,   0,  0xabcd1110 ), # conflicts
    req( 'rd', 0x2, 0x1120, 0, 0          ), resp( 'rd', 0x2, 0,   0,  0xabcd1120 ), # conflicts
    req( 'rd', 0x3, 0x1130, 0, 0          ), resp( 'rd', 0x3, 0,   0,  0xabcd1130 ), # conflicts
    req( 'rd', 0x4, 0x1140, 0, 0          ), resp( 'rd', 0x4, 0,   0,  0xabcd1140 ), # conflicts
    req( 'rd', 0x5, 0x1150, 0, 0          ), resp( 'rd', 0x5, 0,   0,  0xabcd1150 ), # conflicts
    req( 'rd', 0x6, 0x1160, 0, 0          ), resp( 'rd', 0x6, 0,   0,  0xabcd1160 ), # conflicts
    req( 'rd', 0x7, 0x1170, 0, 0          ), resp( 'rd', 0x7, 0,   0,  0xabcd1170 ), # conflicts
    req( 'rd', 0x8, 0x1180, 0, 0          ), resp( 'rd', 0x8, 0,   0,  0xabcd1180 ), # conflicts
    req( 'rd', 0x9, 0x1190, 0, 0          ), resp( 'rd', 0x9, 0,   0,  0xabcd1190 ), # conflicts
    req( 'rd', 0xa, 0x11a0, 0, 0          ), resp( 'rd', 0xa, 0,   0,  0xabcd11a0 ), # conflicts
    req( 'rd', 0xb, 0x11b0, 0, 0          ), resp( 'rd', 0xb, 0,   0,  0xabcd11b0 ), # conflicts
    req( 'rd', 0xc, 0x11c0, 0, 0          ), resp( 'rd', 0xc, 0,   0,  0xabcd11c0 ), # conflicts
    req( 'rd', 0xd, 0x11d0, 0, 0          ), resp( 'rd', 0xd, 0,   0,  0xabcd11d0 ), # conflicts
    req( 'rd', 0xe, 0x11e0, 0, 0          ), resp( 'rd', 0xe, 0,   0,  0xabcd11e0 ), # conflicts
    req( 'rd', 0xf, 0x11f0, 0, 0          ), resp( 'rd', 0xf, 0,   0,  0xabcd11f0 ), # conflicts

    req( 'rd', 0x0, 0x1000, 0, 0          ), resp( 'rd', 0x0, 0,   0,  0x10101010 ),
    req( 'rd', 0x1, 0x1010, 0, 0          ), resp( 'rd', 0x1, 0,   0,  0x11111111 ),
    req( 'rd', 0x2, 0x1020, 0, 0          ), resp( 'rd', 0x2, 0,   0,  0x12121212 ),
    req( 'rd', 0x3, 0x1030, 0, 0          ), resp( 'rd', 0x3, 0,   0,  0x13131313 ),
    req( 'rd', 0x4, 0x1040, 0, 0          ), resp( 'rd', 0x4, 0,   0,  0x14141414 ),
    req( 'rd', 0x5, 0x1050, 0, 0          ), resp( 'rd', 0x5, 0,   0,  0x15151515 ),
    req( 'rd', 0x6, 0x1060, 0, 0          ), resp( 'rd', 0x6, 0,   0,  0x16161616 ),
    req( 'rd', 0x7, 0x1070, 0, 0          ), resp( 'rd', 0x7, 0,   0,  0x17171717 ),
    req( 'rd', 0x8, 0x1080, 0, 0          ), resp( 'rd', 0x8, 0,   0,  0x18181818 ),
    req( 'rd', 0x9, 0x1090, 0, 0          ), resp( 'rd', 0x9, 0,   0,  0x19191919 ),
    req( 'rd', 0xa, 0x10a0, 0, 0          ), resp( 'rd', 0xa, 0,   0,  0x1a1a1a1a ),
    req( 'rd', 0xb, 0x10b0, 0, 0          ), resp( 'rd', 0xb, 0,   0,  0x1b1b1b1b ),
    req( 'rd', 0xc, 0x10c0, 0, 0          ), resp( 'rd', 0xc, 0,   0,  0x1c1c1c1c ),
    req( 'rd', 0xd, 0x10d0, 0, 0          ), resp( 'rd', 0xd, 0,   0,  0x1d1d1d1d ),
    req( 'rd', 0xe, 0x10e0, 0, 0          ), resp( 'rd', 0xe, 0,   0,  0x1e1e1e1e ),
    req( 'rd', 0xf, 0x10f0, 0, 0          ), resp( 'rd', 0xf, 0,   0,  0x1f1f1f1f ),
  ]

#-------------------------------------------------------------------------
# Test Case: read_hit_clean_line
#-------------------------------------------------------------------------

def read_hit_clean_word():
  base = 0x00001000
  return [
    #    type  opq  addr       len  data         type  opq  test len data
    req( 'in', 0x0, base,       0,  0x11111111 ), resp( 'in', 0x0, 0,   0,  0          ),
    req( 'rd', 0x1, base,       0,  0          ), resp( 'rd', 0x1, 1,   0,  0x11111111 ),
  ]

def read_hit_clean_multi_word():
  base = 0x00002000
  return [
    #    type  opq  addr       len  data         type  opq  test len data
    req( 'in', 0x0, base,       0,  0x22222222 ), resp( 'in', 0x0, 0,   0,  0    ),

    req( 'rd', 0x1, base,       0,  0          ), resp( 'rd', 0x1, 1,   0,  0x22222222 ),
    req( 'rd', 0x2, base,       0,  0          ), resp( 'rd', 0x2, 1,   0,  0x22222222 ),
    req( 'rd', 0x3, base,       0,  0          ), resp( 'rd', 0x3, 1,   0,  0x22222222 ),
    req( 'rd', 0x4, base,       0,  0          ), resp( 'rd', 0x4, 1,   0,  0x22222222 ),
  ]

def read_hit_clean_cacheline():
  base = 0x00003000
  return [
    #    type  opq  addr       len  data         type  opq  test len data
    req( 'in', 0x0, base+0x0,  0,  0x01010101 ), resp( 'in', 0x0, 0, 0, 0 ),
    req( 'in', 0x1, base+0x4,  0,  0x02020202 ), resp( 'in', 0x1, 0, 0, 0 ),
    req( 'in', 0x2, base+0x8,  0,  0x03030303 ), resp( 'in', 0x2, 0, 0, 0 ),
    req( 'in', 0x3, base+0xc,  0,  0x04040404 ), resp( 'in', 0x3, 0, 0, 0 ),

    req( 'rd', 0x4, base+0x0,  0,  0 ), resp( 'rd', 0x4, 1, 0, 0x01010101 ),
    req( 'rd', 0x5, base+0x4,  0,  0 ), resp( 'rd', 0x5, 1, 0, 0x02020202 ),
    req( 'rd', 0x6, base+0x8,  0,  0 ), resp( 'rd', 0x6, 1, 0, 0x03030303 ),
    req( 'rd', 0x7, base+0xc,  0,  0 ), resp( 'rd', 0x7, 1, 0, 0x04040404 ),
  ]

def read_hit_clean_multi_cacheline():
  return [
    req( 'in', 0x0, 0x00000000, 0, 0x00000000 ), resp( 'in', 0x0, 0, 0, 0 ),
    req( 'in', 0x1, 0x00000010, 0, 0x11111111 ), resp( 'in', 0x1, 0, 0, 0 ),
    req( 'in', 0x2, 0x00000020, 0, 0x22222222 ), resp( 'in', 0x2, 0, 0, 0 ),
    req( 'in', 0x3, 0x00000030, 0, 0x33333333 ), resp( 'in', 0x3, 0, 0, 0 ),
    req( 'in', 0x4, 0x00000040, 0, 0x44444444 ), resp( 'in', 0x4, 0, 0, 0 ),
    req( 'in', 0x5, 0x00000050, 0, 0x55555555 ), resp( 'in', 0x5, 0, 0, 0 ),
    req( 'in', 0x6, 0x00000060, 0, 0x66666666 ), resp( 'in', 0x6, 0, 0, 0 ),
    req( 'in', 0x7, 0x00000070, 0, 0x77777777 ), resp( 'in', 0x7, 0, 0, 0 ),

    req( 'rd', 0x8,  0x00000000, 0, 0 ), resp( 'rd', 0x8,  1, 0, 0x00000000 ),
    req( 'rd', 0x9,  0x00000010, 0, 0 ), resp( 'rd', 0x9,  1, 0, 0x11111111 ),
    req( 'rd', 0xa,  0x00000020, 0, 0 ), resp( 'rd', 0xa,  1, 0, 0x22222222 ),
    req( 'rd', 0xb,  0x00000030, 0, 0 ), resp( 'rd', 0xb,  1, 0, 0x33333333 ),
    req( 'rd', 0xc,  0x00000040, 0, 0 ), resp( 'rd', 0xc,  1, 0, 0x44444444 ),
    req( 'rd', 0xd,  0x00000050, 0, 0 ), resp( 'rd', 0xd,  1, 0, 0x55555555 ),
    req( 'rd', 0xe,  0x00000060, 0, 0 ), resp( 'rd', 0xe,  1, 0, 0x66666666 ),
    req( 'rd', 0xf,  0x00000070, 0, 0 ), resp( 'rd', 0xf,  1, 0, 0x77777777 ),
  ]


#=========================================================================
# Test Cases: Write Hit Path for Clean Lines
#=========================================================================

#-------------------------------------------------------------------------
# 1. write_hit_clean_word
#-------------------------------------------------------------------------

def write_hit_clean_word():
  base = 0x00001000
  return [
    #    type  opq  addr       len  data          type  opq  test len data
    req( 'in', 0x0, base,       0,  0x11111111 ), resp( 'in', 0x0, 0,   0,  0 ),
    req( 'wr', 0x1, base,       0,  0x22222222 ), resp( 'wr', 0x1, 1,   0,  0 ),
    req( 'rd', 0x2, base,       0,  0          ), resp( 'rd', 0x2, 1,   0,  0x22222222 ),
  ]

#-------------------------------------------------------------------------
# 2. write_hit_clean_multi_word
#-------------------------------------------------------------------------

def write_hit_clean_multi_word():
  base = 0x00002000
  return [
    #    type  opq  addr       len  data          type  opq  test len data
    req( 'in', 0x0, base,       0,  0xaaaa0001 ), resp( 'in', 0x0, 0,   0,  0 ),

    req( 'wr', 0x1, base,       0,  0x01010101 ), resp( 'wr', 0x1, 1,   0,  0 ),
    req( 'rd', 0x2, base,       0,  0          ), resp( 'rd', 0x2, 1,   0,  0x01010101 ),
    req( 'wr', 0x3, base,       0,  0x02020202 ), resp( 'wr', 0x3, 1,   0,  0 ),
    req( 'rd', 0x4, base,       0,  0          ), resp( 'rd', 0x4, 1,   0,  0x02020202 ),
    req( 'wr', 0x5, base,       0,  0x03030303 ), resp( 'wr', 0x5, 1,   0,  0 ),
    req( 'rd', 0x6, base,       0,  0          ), resp( 'rd', 0x6, 1,   0,  0x03030303 ),
  ]

#-------------------------------------------------------------------------
# 3. write_hit_clean_cacheline
#-------------------------------------------------------------------------

def write_hit_clean_cacheline():
  base = 0x00003000
  return [
    #    type  opq  addr        len data          type  opq  test len data
    req( 'in', 0x0, base+0x0,   0,  0x11111111 ), resp( 'in', 0x0, 0, 0, 0 ),
    req( 'in', 0x1, base+0x4,   0,  0x22222222 ), resp( 'in', 0x1, 0, 0, 0 ),
    req( 'in', 0x2, base+0x8,   0,  0x33333333 ), resp( 'in', 0x2, 0, 0, 0 ),
    req( 'in', 0x3, base+0xc,   0,  0x44444444 ), resp( 'in', 0x3, 0, 0, 0 ),

    req( 'wr', 0x4, base+0x0,   0,  0xaaaa0001 ), resp( 'wr', 0x4, 1, 0, 0 ),
    req( 'wr', 0x5, base+0x4,   0,  0xbbbb0002 ), resp( 'wr', 0x5, 1, 0, 0 ),
    req( 'wr', 0x6, base+0x8,   0,  0xcccc0003 ), resp( 'wr', 0x6, 1, 0, 0 ),
    req( 'wr', 0x7, base+0xc,   0,  0xdddd0004 ), resp( 'wr', 0x7, 1, 0, 0 ),

    req( 'rd', 0x8, base+0x0,   0,  0 ), resp( 'rd', 0x8, 1, 0, 0xaaaa0001 ),
    req( 'rd', 0x9, base+0x4,   0,  0 ), resp( 'rd', 0x9, 1, 0, 0xbbbb0002 ),
    req( 'rd', 0xa, base+0x8,   0,  0 ), resp( 'rd', 0xa, 1, 0, 0xcccc0003 ),
    req( 'rd', 0xb, base+0xc,   0,  0 ), resp( 'rd', 0xb, 1, 0, 0xdddd0004 ),
  ]

#-------------------------------------------------------------------------
# 4. write_hit_clean_multi_cacheline
#-------------------------------------------------------------------------

def write_hit_clean_multi_cacheline():
  return [
    req( 'in', 0x0, 0x00000000, 0, 0x00000000 ), resp( 'in', 0x0, 0, 0, 0 ),
    req( 'in', 0x1, 0x00000010, 0, 0x11111111 ), resp( 'in', 0x1, 0, 0, 0 ),
    req( 'in', 0x2, 0x00000020, 0, 0x22222222 ), resp( 'in', 0x2, 0, 0, 0 ),
    req( 'in', 0x3, 0x00000030, 0, 0x33333333 ), resp( 'in', 0x3, 0, 0, 0 ),
    req( 'in', 0x4, 0x00000040, 0, 0x44444444 ), resp( 'in', 0x4, 0, 0, 0 ),

    req( 'wr', 0x5, 0x00000000, 0, 0xaaaa0000 ), resp( 'wr', 0x5, 1, 0, 0 ),
    req( 'wr', 0x6, 0x00000010, 0, 0xbbbb0001 ), resp( 'wr', 0x6, 1, 0, 0 ),
    req( 'wr', 0x7, 0x00000020, 0, 0xcccc0002 ), resp( 'wr', 0x7, 1, 0, 0 ),
    req( 'wr', 0x8, 0x00000030, 0, 0xdddd0003 ), resp( 'wr', 0x8, 1, 0, 0 ),
    req( 'wr', 0x9, 0x00000040, 0, 0xeeee0004 ), resp( 'wr', 0x9, 1, 0, 0 ),

    req( 'rd', 0xa, 0x00000000, 0, 0 ), resp( 'rd', 0xa, 1, 0, 0xaaaa0000 ),
    req( 'rd', 0xb, 0x00000010, 0, 0 ), resp( 'rd', 0xb, 1, 0, 0xbbbb0001 ),
    req( 'rd', 0xc, 0x00000020, 0, 0 ), resp( 'rd', 0xc, 1, 0, 0xcccc0002 ),
    req( 'rd', 0xd, 0x00000030, 0, 0 ), resp( 'rd', 0xd, 1, 0, 0xdddd0003 ),
    req( 'rd', 0xe, 0x00000040, 0, 0 ), resp( 'rd', 0xe, 1, 0, 0xeeee0004 ),
  ]


#----------------------------------------------------------------------
# Read hit path for dirty line
#----------------------------------------------------------------------

def read_hit_dirty_word():
  return [
    req( 'in', 0x00, 0x1000, 0, 0x11111111 ), resp( 'in', 0x00, 0, 0, 0 ),
    req( 'wr', 0x01, 0x1000, 0, 0x22222222 ), resp( 'wr', 0x01, 1, 0, 0 ),
    req( 'rd', 0x02, 0x1000, 0, 0 ),          resp( 'rd', 0x02, 1, 0, 0x22222222 ),
  ]

def read_hit_dirty_multi_word():
  return [
    # type  opq  addr   len data                type  opq  test len data
    req( 'in', 0x00, 0x1000, 0, 0xaaaa0000 ), resp( 'in', 0x00, 0, 0, 0 ),
    req( 'wr', 0x01, 0x1000, 0, 0xbbbb1111 ), resp( 'wr', 0x01, 1, 0, 0 ),
    req( 'rd', 0x02, 0x1000, 0, 0 ),          resp( 'rd', 0x02, 1, 0, 0xbbbb1111 ),
    req( 'wr', 0x03, 0x1000, 0, 0xcccc2222 ), resp( 'wr', 0x03, 1, 0, 0 ),
    req( 'rd', 0x04, 0x1000, 0, 0 ),          resp( 'rd', 0x04, 1, 0, 0xcccc2222 ),
    req( 'wr', 0x05, 0x1000, 0, 0xdddd3333 ), resp( 'wr', 0x05, 1, 0, 0 ),
    req( 'rd', 0x06, 0x1000, 0, 0 ),          resp( 'rd', 0x06, 1, 0, 0xdddd3333 ),
  ]

def read_hit_dirty_cacheline():
  return [
    req( 'in', 0x00, 0x1000, 0, 0x11111111 ), resp( 'in', 0x00, 0, 0, 0 ),
    req( 'in', 0x01, 0x1004, 0, 0x22222222 ), resp( 'in', 0x01, 0, 0, 0 ),
    req( 'in', 0x02, 0x1008, 0, 0x33333333 ), resp( 'in', 0x02, 0, 0, 0 ),
    req( 'in', 0x03, 0x100c, 0, 0x44444444 ), resp( 'in', 0x03, 0, 0, 0 ),

    req( 'wr', 0x04, 0x1000, 0, 0xaaaa0000 ), resp( 'wr', 0x04, 1, 0, 0 ),
    req( 'wr', 0x05, 0x1004, 0, 0xbbbb1111 ), resp( 'wr', 0x05, 1, 0, 0 ),
    req( 'wr', 0x06, 0x1008, 0, 0xcccc2222 ), resp( 'wr', 0x06, 1, 0, 0 ),
    req( 'wr', 0x07, 0x100c, 0, 0xdddd3333 ), resp( 'wr', 0x07, 1, 0, 0 ),

    req( 'rd', 0x08, 0x1000, 0, 0 ),          resp( 'rd', 0x08, 1, 0, 0xaaaa0000 ),
    req( 'rd', 0x09, 0x1004, 0, 0 ),          resp( 'rd', 0x09, 1, 0, 0xbbbb1111 ),
    req( 'rd', 0x0a, 0x1008, 0, 0 ),          resp( 'rd', 0x0a, 1, 0, 0xcccc2222 ),
    req( 'rd', 0x0b, 0x100c, 0, 0 ),          resp( 'rd', 0x0b, 1, 0, 0xdddd3333 ),
  ]

def read_hit_dirty_multi_cacheline():
  return [
    req( 'in', 0x00, 0x0000, 0, 0x10101010 ), resp( 'in', 0x00, 0, 0, 0 ),
    req( 'in', 0x01, 0x0010, 0, 0x20202020 ), resp( 'in', 0x01, 0, 0, 0 ),
    req( 'in', 0x02, 0x0020, 0, 0x30303030 ), resp( 'in', 0x02, 0, 0, 0 ),
    req( 'in', 0x03, 0x0030, 0, 0x40404040 ), resp( 'in', 0x03, 0, 0, 0 ),

    req( 'wr', 0x04, 0x0000, 0, 0xaaaa0000 ), resp( 'wr', 0x04, 1, 0, 0 ),
    req( 'wr', 0x05, 0x0010, 0, 0xbbbb1111 ), resp( 'wr', 0x05, 1, 0, 0 ),
    req( 'wr', 0x06, 0x0020, 0, 0xcccc2222 ), resp( 'wr', 0x06, 1, 0, 0 ),
    req( 'wr', 0x07, 0x0030, 0, 0xdddd3333 ), resp( 'wr', 0x07, 1, 0, 0 ),

    req( 'rd', 0x08, 0x0000, 0, 0 ), resp( 'rd', 0x08, 1, 0, 0xaaaa0000 ),
    req( 'rd', 0x09, 0x0010, 0, 0 ), resp( 'rd', 0x09, 1, 0, 0xbbbb1111 ),
    req( 'rd', 0x0a, 0x0020, 0, 0 ), resp( 'rd', 0x0a, 1, 0, 0xcccc2222 ),
    req( 'rd', 0x0b, 0x0030, 0, 0 ), resp( 'rd', 0x0b, 1, 0, 0xdddd3333 ),
  ]


def write_hit_dirty_word():
  return [
    req('in', 0x00, 0x1000, 0, 0xAAAAAAAA), resp('in', 0x00, 0, 0, 0),
    req('wr', 0x01, 0x1000, 0, 0xBBBBBBBB), resp('wr', 0x01, 1, 0, 0),
    req('rd', 0x02, 0x1000, 0, 0), resp('rd', 0x02, 1, 0, 0xBBBBBBBB),
  ]

def write_hit_dirty_multi_word():
  return [
    req('in', 0x00, 0x1000, 0, 0x11111111), resp('in', 0x00, 0, 0, 0),
    req('wr', 0x01, 0x1000, 0, 0xAAAA0000), resp('wr', 0x01, 1, 0, 0),
    req('rd', 0x02, 0x1000, 0, 0), resp('rd', 0x02, 1, 0, 0xAAAA0000),
    req('wr', 0x03, 0x1000, 0, 0xBBBB1111), resp('wr', 0x03, 1, 0, 0),
    req('rd', 0x04, 0x1000, 0, 0), resp('rd', 0x04, 1, 0, 0xBBBB1111),
    req('wr', 0x05, 0x1000, 0, 0xCCCC2222), resp('wr', 0x05, 1, 0, 0),
    req('rd', 0x06, 0x1000, 0, 0), resp('rd', 0x06, 1, 0, 0xCCCC2222),
  ]

def write_hit_dirty_cacheline():
  return [
    req('in', 0x00, 0x1000, 0, 0x11111111), resp('in', 0x00, 0, 0, 0),
    req('in', 0x01, 0x1004, 0, 0x22222222), resp('in', 0x01, 0, 0, 0),
    req('in', 0x02, 0x1008, 0, 0x33333333), resp('in', 0x02, 0, 0, 0),
    req('in', 0x03, 0x100c, 0, 0x44444444), resp('in', 0x03, 0, 0, 0),
    req('wr', 0x04, 0x1000, 0, 0xAAAA0000), resp('wr', 0x04, 1, 0, 0),
    req('wr', 0x05, 0x1004, 0, 0xBBBB1111), resp('wr', 0x05, 1, 0, 0),
    req('wr', 0x06, 0x1008, 0, 0xCCCC2222), resp('wr', 0x06, 1, 0, 0),
    req('wr', 0x07, 0x100c, 0, 0xDDDD3333), resp('wr', 0x07, 1, 0, 0),
    req('rd', 0x08, 0x1000, 0, 0), resp('rd', 0x08, 1, 0, 0xAAAA0000),
    req('rd', 0x09, 0x1004, 0, 0), resp('rd', 0x09, 1, 0, 0xBBBB1111),
    req('rd', 0x0A, 0x1008, 0, 0), resp('rd', 0x0A, 1, 0, 0xCCCC2222),
    req('rd', 0x0B, 0x100C, 0, 0), resp('rd', 0x0B, 1, 0, 0xDDDD3333),
  ]

def write_hit_dirty_multi_cacheline():
  return [
    req('in', 0x00, 0x0000, 0, 0x00000000), resp('in', 0x00, 0, 0, 0),
    req('in', 0x01, 0x1010, 0, 0x11111111), resp('in', 0x01, 0, 0, 0),
    req('in', 0x02, 0x2020, 0, 0x22222222), resp('in', 0x02, 0, 0, 0),
    req('in', 0x03, 0x3030, 0, 0x33333333), resp('in', 0x03, 0, 0, 0),
    req('wr', 0x04, 0x0000, 0, 0xAAAA0000), resp('wr', 0x04, 1, 0, 0),
    req('wr', 0x05, 0x1010, 0, 0xBBBB1111), resp('wr', 0x05, 1, 0, 0),
    req('wr', 0x06, 0x2020, 0, 0xCCCC2222), resp('wr', 0x06, 1, 0, 0),
    req('wr', 0x07, 0x3030, 0, 0xDDDD3333), resp('wr', 0x07, 1, 0, 0),
    req('rd', 0x08, 0x0000, 0, 0), resp('rd', 0x08, 1, 0, 0xAAAA0000),
    req('rd', 0x09, 0x1010, 0, 0), resp('rd', 0x09, 1, 0, 0xBBBB1111),
    req('rd', 0x0A, 0x2020, 0, 0), resp('rd', 0x0A, 1, 0, 0xCCCC2222),
    req('rd', 0x0B, 0x3030, 0, 0), resp('rd', 0x0B, 1, 0, 0xDDDD3333),
  ]

#----------------------------------------------------------------------
# Read miss with refill and no eviction
#----------------------------------------------------------------------

# Single read miss (uses data_64B)

def read_miss_no_evict_word():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'rd', 0x0, 0x1000, 0, 0          ), resp( 'rd', 0x0, 0,   0,  0x000c0ffe ),
  ]

# Read same word multiple times, also tests opaque bits (uses data_64B)

def read_miss_multi_no_evict_word():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'rd', 0x0, 0x1000, 0, 0          ), resp( 'rd', 0x0, 0,   0,  0x000c0ffe ),
    req( 'rd', 0x1, 0x1000, 0, 0          ), resp( 'rd', 0x1, 1,   0,  0x000c0ffe ),
    req( 'rd', 0x2, 0x1000, 0, 0          ), resp( 'rd', 0x2, 1,   0,  0x000c0ffe ),
    req( 'rd', 0x3, 0x1000, 0, 0          ), resp( 'rd', 0x3, 1,   0,  0x000c0ffe ),
  ]

# Read every word in cache line (uses data_64B)

def read_miss_no_evict_cacheline():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'rd', 0x1, 0x1000, 0, 0          ), resp( 'rd', 0x1, 0,   0,  0x000c0ffe ),
    req( 'rd', 0x2, 0x1004, 0, 0          ), resp( 'rd', 0x2, 1,   0,  0x10101010 ),
    req( 'rd', 0x3, 0x1008, 0, 0          ), resp( 'rd', 0x3, 1,   0,  0x20202020 ),
    req( 'rd', 0x4, 0x100c, 0, 0          ), resp( 'rd', 0x4, 1,   0,  0x30303030 ),
  ]

# Read miss for each cacheline, then read hit for each cacheline (uses data_512B)

def read_miss_multi_no_evict_cacheline():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'rd', 0x0, 0x1000, 0, 0          ), resp( 'rd', 0x0, 0,   0,  0xabcd1000 ),
    req( 'rd', 0x1, 0x1010, 0, 0          ), resp( 'rd', 0x1, 0,   0,  0xabcd1010 ),
    req( 'rd', 0x2, 0x1020, 0, 0          ), resp( 'rd', 0x2, 0,   0,  0xabcd1020 ),
    req( 'rd', 0x3, 0x1030, 0, 0          ), resp( 'rd', 0x3, 0,   0,  0xabcd1030 ),
    req( 'rd', 0x4, 0x1040, 0, 0          ), resp( 'rd', 0x4, 0,   0,  0xabcd1040 ),
    req( 'rd', 0x5, 0x1050, 0, 0          ), resp( 'rd', 0x5, 0,   0,  0xabcd1050 ),
    req( 'rd', 0x6, 0x1060, 0, 0          ), resp( 'rd', 0x6, 0,   0,  0xabcd1060 ),
    req( 'rd', 0x7, 0x1070, 0, 0          ), resp( 'rd', 0x7, 0,   0,  0xabcd1070 ),
    req( 'rd', 0x8, 0x1080, 0, 0          ), resp( 'rd', 0x8, 0,   0,  0xabcd1080 ),
    req( 'rd', 0x9, 0x1090, 0, 0          ), resp( 'rd', 0x9, 0,   0,  0xabcd1090 ),
    req( 'rd', 0xa, 0x10a0, 0, 0          ), resp( 'rd', 0xa, 0,   0,  0xabcd10a0 ),
    req( 'rd', 0xb, 0x10b0, 0, 0          ), resp( 'rd', 0xb, 0,   0,  0xabcd10b0 ),
    req( 'rd', 0xc, 0x10c0, 0, 0          ), resp( 'rd', 0xc, 0,   0,  0xabcd10c0 ),
    req( 'rd', 0xd, 0x10d0, 0, 0          ), resp( 'rd', 0xd, 0,   0,  0xabcd10d0 ),
    req( 'rd', 0xe, 0x10e0, 0, 0          ), resp( 'rd', 0xe, 0,   0,  0xabcd10e0 ),
    req( 'rd', 0xf, 0x10f0, 0, 0          ), resp( 'rd', 0xf, 0,   0,  0xabcd10f0 ),

    req( 'rd', 0x0, 0x1000, 0, 0          ), resp( 'rd', 0x0, 1,   0,  0xabcd1000 ),
    req( 'rd', 0x1, 0x1010, 0, 0          ), resp( 'rd', 0x1, 1,   0,  0xabcd1010 ),
    req( 'rd', 0x2, 0x1020, 0, 0          ), resp( 'rd', 0x2, 1,   0,  0xabcd1020 ),
    req( 'rd', 0x3, 0x1030, 0, 0          ), resp( 'rd', 0x3, 1,   0,  0xabcd1030 ),
    req( 'rd', 0x4, 0x1040, 0, 0          ), resp( 'rd', 0x4, 1,   0,  0xabcd1040 ),
    req( 'rd', 0x5, 0x1050, 0, 0          ), resp( 'rd', 0x5, 1,   0,  0xabcd1050 ),
    req( 'rd', 0x6, 0x1060, 0, 0          ), resp( 'rd', 0x6, 1,   0,  0xabcd1060 ),
    req( 'rd', 0x7, 0x1070, 0, 0          ), resp( 'rd', 0x7, 1,   0,  0xabcd1070 ),
    req( 'rd', 0x8, 0x1080, 0, 0          ), resp( 'rd', 0x8, 1,   0,  0xabcd1080 ),
    req( 'rd', 0x9, 0x1090, 0, 0          ), resp( 'rd', 0x9, 1,   0,  0xabcd1090 ),
    req( 'rd', 0xa, 0x10a0, 0, 0          ), resp( 'rd', 0xa, 1,   0,  0xabcd10a0 ),
    req( 'rd', 0xb, 0x10b0, 0, 0          ), resp( 'rd', 0xb, 1,   0,  0xabcd10b0 ),
    req( 'rd', 0xc, 0x10c0, 0, 0          ), resp( 'rd', 0xc, 1,   0,  0xabcd10c0 ),
    req( 'rd', 0xd, 0x10d0, 0, 0          ), resp( 'rd', 0xd, 1,   0,  0xabcd10d0 ),
    req( 'rd', 0xe, 0x10e0, 0, 0          ), resp( 'rd', 0xe, 1,   0,  0xabcd10e0 ),
    req( 'rd', 0xf, 0x10f0, 0, 0          ), resp( 'rd', 0xf, 1,   0,  0xabcd10f0 ),

    req( 'rd', 0x0, 0x1004, 0, 0          ), resp( 'rd', 0x0, 1,   0,  0xabcd1004 ),
    req( 'rd', 0x1, 0x1014, 0, 0          ), resp( 'rd', 0x1, 1,   0,  0xabcd1014 ),
    req( 'rd', 0x2, 0x1024, 0, 0          ), resp( 'rd', 0x2, 1,   0,  0xabcd1024 ),
    req( 'rd', 0x3, 0x1034, 0, 0          ), resp( 'rd', 0x3, 1,   0,  0xabcd1034 ),
    req( 'rd', 0x4, 0x1044, 0, 0          ), resp( 'rd', 0x4, 1,   0,  0xabcd1044 ),
    req( 'rd', 0x5, 0x1054, 0, 0          ), resp( 'rd', 0x5, 1,   0,  0xabcd1054 ),
    req( 'rd', 0x6, 0x1064, 0, 0          ), resp( 'rd', 0x6, 1,   0,  0xabcd1064 ),
    req( 'rd', 0x7, 0x1074, 0, 0          ), resp( 'rd', 0x7, 1,   0,  0xabcd1074 ),
    req( 'rd', 0x8, 0x1084, 0, 0          ), resp( 'rd', 0x8, 1,   0,  0xabcd1084 ),
    req( 'rd', 0x9, 0x1094, 0, 0          ), resp( 'rd', 0x9, 1,   0,  0xabcd1094 ),
    req( 'rd', 0xa, 0x10a4, 0, 0          ), resp( 'rd', 0xa, 1,   0,  0xabcd10a4 ),
    req( 'rd', 0xb, 0x10b4, 0, 0          ), resp( 'rd', 0xb, 1,   0,  0xabcd10b4 ),
    req( 'rd', 0xc, 0x10c4, 0, 0          ), resp( 'rd', 0xc, 1,   0,  0xabcd10c4 ),
    req( 'rd', 0xd, 0x10d4, 0, 0          ), resp( 'rd', 0xd, 1,   0,  0xabcd10d4 ),
    req( 'rd', 0xe, 0x10e4, 0, 0          ), resp( 'rd', 0xe, 1,   0,  0xabcd10e4 ),
    req( 'rd', 0xf, 0x10f4, 0, 0          ), resp( 'rd', 0xf, 1,   0,  0xabcd10f4 ),
  ]

#----------------------------------------------------------------------
# Write miss with refill and no eviction
#----------------------------------------------------------------------

# Single write miss to one word (uses data_64B)

def write_miss_no_evict_word():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'wr', 0x0, 0x1000, 0, 0xcafecafe ), resp( 'wr', 0x0, 0,   0,  0          ),
    req( 'rd', 0x0, 0x1000, 0, 0          ), resp( 'rd', 0x0, 1,   0,  0xcafecafe ),
  ]

# Write/read word multiple times, also tests opaque bits (uses data_64B)

def write_miss_multi_no_evict_word():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'wr', 0x1, 0x1000, 0, 0x01010101 ), resp( 'wr', 0x1, 0,   0,  0          ),
    req( 'rd', 0x2, 0x1000, 0, 0          ), resp( 'rd', 0x2, 1,   0,  0x01010101 ),
    req( 'wr', 0x3, 0x1000, 0, 0x02020202 ), resp( 'wr', 0x3, 1,   0,  0          ),
    req( 'rd', 0x4, 0x1000, 0, 0          ), resp( 'rd', 0x4, 1,   0,  0x02020202 ),
    req( 'wr', 0x5, 0x1000, 0, 0x03030303 ), resp( 'wr', 0x5, 1,   0,  0          ),
    req( 'rd', 0x6, 0x1000, 0, 0          ), resp( 'rd', 0x6, 1,   0,  0x03030303 ),
    req( 'wr', 0x7, 0x1000, 0, 0x04040404 ), resp( 'wr', 0x7, 1,   0,  0          ),
    req( 'rd', 0x8, 0x1000, 0, 0          ), resp( 'rd', 0x8, 1,   0,  0x04040404 ),
  ]

# Write/read every word in cache line (uses data_64B)

def write_miss_no_evict_cacheline():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'wr', 0x1, 0x1000, 0, 0x01010101 ), resp( 'wr', 0x1, 0,   0,  0          ),
    req( 'wr', 0x2, 0x1004, 0, 0x02020202 ), resp( 'wr', 0x2, 1,   0,  0          ),
    req( 'wr', 0x3, 0x1008, 0, 0x03030303 ), resp( 'wr', 0x3, 1,   0,  0          ),
    req( 'wr', 0x4, 0x100c, 0, 0x04040404 ), resp( 'wr', 0x4, 1,   0,  0          ),

    req( 'rd', 0x5, 0x1000, 0, 0          ), resp( 'rd', 0x5, 1,   0,  0x01010101 ),
    req( 'rd', 0x6, 0x1004, 0, 0          ), resp( 'rd', 0x6, 1,   0,  0x02020202 ),
    req( 'rd', 0x7, 0x1008, 0, 0          ), resp( 'rd', 0x7, 1,   0,  0x03030303 ),
    req( 'rd', 0x8, 0x100c, 0, 0          ), resp( 'rd', 0x8, 1,   0,  0x04040404 ),
  ]

# Write/read one word from each cacheline (uses data_512B)

def write_miss_multi_no_evict_cacheline():
  return [
    #    type  opq  addr   len data                type  opq  test len data
    req( 'wr', 0x0, 0x1000, 0, 0x10101010 ), resp( 'wr', 0x0, 0,   0,  0          ),
    req( 'wr', 0x1, 0x1010, 0, 0x11111111 ), resp( 'wr', 0x1, 0,   0,  0          ),
    req( 'wr', 0x2, 0x1020, 0, 0x12121212 ), resp( 'wr', 0x2, 0,   0,  0          ),
    req( 'wr', 0x3, 0x1030, 0, 0x13131313 ), resp( 'wr', 0x3, 0,   0,  0          ),
    req( 'wr', 0x4, 0x1040, 0, 0x14141414 ), resp( 'wr', 0x4, 0,   0,  0          ),
    req( 'wr', 0x5, 0x1050, 0, 0x15151515 ), resp( 'wr', 0x5, 0,   0,  0          ),
    req( 'wr', 0x6, 0x1060, 0, 0x16161616 ), resp( 'wr', 0x6, 0,   0,  0          ),
    req( 'wr', 0x7, 0x1070, 0, 0x17171717 ), resp( 'wr', 0x7, 0,   0,  0          ),
    req( 'wr', 0x8, 0x1080, 0, 0x18181818 ), resp( 'wr', 0x8, 0,   0,  0          ),
    req( 'wr', 0x9, 0x1090, 0, 0x19191919 ), resp( 'wr', 0x9, 0,   0,  0          ),
    req( 'wr', 0xa, 0x10a0, 0, 0x1a1a1a1a ), resp( 'wr', 0xa, 0,   0,  0          ),
    req( 'wr', 0xb, 0x10b0, 0, 0x1b1b1b1b ), resp( 'wr', 0xb, 0,   0,  0          ),
    req( 'wr', 0xc, 0x10c0, 0, 0x1c1c1c1c ), resp( 'wr', 0xc, 0,   0,  0          ),
    req( 'wr', 0xd, 0x10d0, 0, 0x1d1d1d1d ), resp( 'wr', 0xd, 0,   0,  0          ),
    req( 'wr', 0xe, 0x10e0, 0, 0x1e1e1e1e ), resp( 'wr', 0xe, 0,   0,  0          ),
    req( 'wr', 0xf, 0x10f0, 0, 0x1f1f1f1f ), resp( 'wr', 0xf, 0,   0,  0          ),

    req( 'rd', 0x0, 0x1000, 0, 0          ), resp( 'rd', 0x0, 1,   0,  0x10101010 ),
    req( 'rd', 0x1, 0x1010, 0, 0          ), resp( 'rd', 0x1, 1,   0,  0x11111111 ),
    req( 'rd', 0x2, 0x1020, 0, 0          ), resp( 'rd', 0x2, 1,   0,  0x12121212 ),
    req( 'rd', 0x3, 0x1030, 0, 0          ), resp( 'rd', 0x3, 1,   0,  0x13131313 ),
    req( 'rd', 0x4, 0x1040, 0, 0          ), resp( 'rd', 0x4, 1,   0,  0x14141414 ),
    req( 'rd', 0x5, 0x1050, 0, 0          ), resp( 'rd', 0x5, 1,   0,  0x15151515 ),
    req( 'rd', 0x6, 0x1060, 0, 0          ), resp( 'rd', 0x6, 1,   0,  0x16161616 ),
    req( 'rd', 0x7, 0x1070, 0, 0          ), resp( 'rd', 0x7, 1,   0,  0x17171717 ),
    req( 'rd', 0x8, 0x1080, 0, 0          ), resp( 'rd', 0x8, 1,   0,  0x18181818 ),
    req( 'rd', 0x9, 0x1090, 0, 0          ), resp( 'rd', 0x9, 1,   0,  0x19191919 ),
    req( 'rd', 0xa, 0x10a0, 0, 0          ), resp( 'rd', 0xa, 1,   0,  0x1a1a1a1a ),
    req( 'rd', 0xb, 0x10b0, 0, 0          ), resp( 'rd', 0xb, 1,   0,  0x1b1b1b1b ),
    req( 'rd', 0xc, 0x10c0, 0, 0          ), resp( 'rd', 0xc, 1,   0,  0x1c1c1c1c ),
    req( 'rd', 0xd, 0x10d0, 0, 0          ), resp( 'rd', 0xd, 1,   0,  0x1d1d1d1d ),
    req( 'rd', 0xe, 0x10e0, 0, 0          ), resp( 'rd', 0xe, 1,   0,  0x1e1e1e1e ),
    req( 'rd', 0xf, 0x10f0, 0, 0          ), resp( 'rd', 0xf, 1,   0,  0x1f1f1f1f ),
  ]

#----------------------------------------------------------------------
# Read miss with refill and eviction
#----------------------------------------------------------------------

def read_miss_with_refill_and_eviction_word():
  return [
    req('rd', 0x0, 0x1000, 0, 0), resp('rd', 0x0, 0, 0, 0xabcd1000),
    req('rd', 0x1, 0x1080, 0, 0), resp('rd', 0x1, 0, 0, 0xabcd1080),
    req('rd', 0x2, 0x1100, 0, 0), resp('rd', 0x2, 0, 0, 0xabcd1100),
    req('rd', 0x3, 0x1180, 0, 0), resp('rd', 0x3, 0, 0, 0xabcd1180),
    req('rd', 0x0, 0x1000, 0, 0), resp('rd', 0x0, 0, 0, 0xabcd1000),
    req('rd', 0x1, 0x1080, 0, 0), resp('rd', 0x1, 0, 0, 0xabcd1080),
  ]

def read_miss_with_refill_and_eviction_word_data():
  return [
    0x1000, 0xabcd1000,
    0x1080, 0xabcd1080,
    0x1100, 0xabcd1100,
    0x1180, 0xabcd1180,
  ]

def read_miss_with_refill_and_eviction_multi_word():
  return [
    req('rd', 0x0, 0x1000, 0, 0), resp('rd', 0x0, 0, 0, 0xabcd1000),
    req('rd', 0x1, 0x1004, 0, 0), resp('rd', 0x1, 1, 0, 0xabcd1004),
    req('rd', 0x2, 0x1080, 0, 0), resp('rd', 0x2, 0, 0, 0xabcd1080),
    req('rd', 0x3, 0x1084, 0, 0), resp('rd', 0x3, 1, 0, 0xabcd1084),
    req('rd', 0x4, 0x1100, 0, 0), resp('rd', 0x4, 0, 0, 0xabcd1100),
    req('rd', 0x5, 0x1180, 0, 0), resp('rd', 0x5, 0, 0, 0xabcd1180),
  ]

def read_miss_with_refill_and_eviction_multi_word_data():
  return [
    0x1000, 0xabcd1000,
    0x1004, 0xabcd1004,
    0x1080, 0xabcd1080,
    0x1084, 0xabcd1084,
    0x1100, 0xabcd1100,
    0x1180, 0xabcd1180,
  ]


#----------------------------------------------------------------------
# Read miss with refill and eviction: cacheline (same line 4 words)
#----------------------------------------------------------------------
def read_miss_with_refill_and_eviction_cacheline():
  return [
    req('rd', 0x0, 0x1000, 0, 0), resp('rd', 0x0, 0, 0, 0xabcd1000),
    req('rd', 0x1, 0x1004, 0, 0), resp('rd', 0x1, 1, 0, 0xabcd1004),
    req('rd', 0x2, 0x1008, 0, 0), resp('rd', 0x2, 1, 0, 0xabcd1008),
    req('rd', 0x3, 0x100c, 0, 0), resp('rd', 0x3, 1, 0, 0xabcd100c),
    req('rd', 0x4, 0x1080, 0, 0), resp('rd', 0x4, 0, 0, 0xabcd1080),
    req('rd', 0x5, 0x1100, 0, 0), resp('rd', 0x5, 0, 0, 0xabcd1100),
    req('rd', 0x6, 0x1180, 0, 0), resp('rd', 0x6, 0, 0, 0xabcd1180),
  ]

def read_miss_with_refill_and_eviction_cacheline_data():
  return [
    0x1000, 0xabcd1000,
    0x1004, 0xabcd1004,
    0x1008, 0xabcd1008,
    0x100c, 0xabcd100c,
    0x1080, 0xabcd1080,
    0x1100, 0xabcd1100,
    0x1180, 0xabcd1180,
  ]


#----------------------------------------------------------------------
# Read miss with refill and eviction: multi cacheline
#----------------------------------------------------------------------
def read_miss_with_refill_and_eviction_multi_cacheline():
  return [
    req('rd', 0x0, 0x1000, 0, 0), resp('rd', 0x0, 0, 0, 0xabcd1000),
    req('rd', 0x1, 0x1080, 0, 0), resp('rd', 0x1, 0, 0, 0xabcd1080),
    req('rd', 0x2, 0x1100, 0, 0), resp('rd', 0x2, 0, 0, 0xabcd1100),
    req('rd', 0x3, 0x1180, 0, 0), resp('rd', 0x3, 0, 0, 0xabcd1180),
    req('rd', 0x4, 0x1000, 0, 0), resp('rd', 0x4, 0, 0, 0xabcd1000),
    req('rd', 0x5, 0x1080, 0, 0), resp('rd', 0x5, 0, 0, 0xabcd1080),
  ]

def read_miss_with_refill_and_eviction_multi_cacheline_data():
  return [
    0x1000, 0xabcd1000,
    0x1080, 0xabcd1080,
    0x1100, 0xabcd1100,
    0x1180, 0xabcd1180,
  ]

#----------------------------------------------------------------------
# Write miss with refill and eviction
#----------------------------------------------------------------------

#------------------------------------------------------
# 1. Single word version
#------------------------------------------------------
def write_miss_with_refill_and_eviction_word():
  return [
    req('wr', 0x0, 0x1000, 0, 0xdead1000), resp('wr', 0x0, 0, 0, 0),
    req('rd', 0x1, 0x1000, 0, 0),          resp('rd', 0x1, 1, 0, 0xdead1000),

    req('wr', 0x2, 0x1080, 0, 0xdead1080), resp('wr', 0x2, 0, 0, 0),
    req('rd', 0x3, 0x1080, 0, 0),          resp('rd', 0x3, 1, 0, 0xdead1080),

    req('rd', 0x4, 0x1100, 0, 0),          resp('rd', 0x4, 0, 0, 0xabcd1100),
    req('rd', 0x5, 0x1000, 0, 0),          resp('rd', 0x5, 0, 0, 0xdead1000),
  ]


#------------------------------------------------------
# 2. Multi-word version
#------------------------------------------------------
def write_miss_with_refill_and_eviction_multi_word():
  return [
    req('wr', 0x0, 0x1000, 0, 0xdead1000), resp('wr', 0x0, 0, 0, 0),
    req('wr', 0x1, 0x1004, 0, 0xdead1004), resp('wr', 0x1, 1, 0, 0),
    req('rd', 0x2, 0x1000, 0, 0),          resp('rd', 0x2, 1, 0, 0xdead1000),
    req('rd', 0x3, 0x1004, 0, 0),          resp('rd', 0x3, 1, 0, 0xdead1004),

    req('wr', 0x4, 0x1080, 0, 0xdead1080), resp('wr', 0x4, 0, 0, 0),
    req('wr', 0x5, 0x1084, 0, 0xdead1084), resp('wr', 0x5, 1, 0, 0),
    req('rd', 0x6, 0x1080, 0, 0),          resp('rd', 0x6, 1, 0, 0xdead1080),
    req('rd', 0x7, 0x1084, 0, 0),          resp('rd', 0x7, 1, 0, 0xdead1084),

    req('rd', 0x8, 0x1100, 0, 0),          resp('rd', 0x8, 0, 0, 0xabcd1100),
    req('rd', 0x9, 0x1000, 0, 0),          resp('rd', 0x9, 0, 0, 0xdead1000),
  ]

def write_miss_with_refill_and_eviction_cacheline():
  return [
    req('wr', 0x0, 0x1000, 0, 0x11111111), resp('wr', 0x0, 0, 0, 0),
    req('wr', 0x1, 0x1004, 0, 0x22222222), resp('wr', 0x1, 1, 0, 0),
    req('wr', 0x2, 0x1008, 0, 0x33333333), resp('wr', 0x2, 1, 0, 0),
    req('wr', 0x3, 0x100C, 0, 0x44444444), resp('wr', 0x3, 1, 0, 0),

    req('rd', 0x4, 0x1000, 0, 0),          resp('rd', 0x4, 1, 0, 0x11111111),

    req('wr', 0x5, 0x1080, 0, 0xAAAA0000), resp('wr', 0x5, 0, 0, 0),
    req('rd', 0x6, 0x1080, 0, 0),          resp('rd', 0x6, 1, 0, 0xAAAA0000),

    req('rd', 0x7, 0x1100, 0, 0),          resp('rd', 0x7, 0, 0, 0xabcd1100),
    req('rd', 0x8, 0x1000, 0, 0),          resp('rd', 0x8, 0, 0, 0x11111111),
  ]

#----------------------------------------------------------------------
# Stress exact counts:
# 16 writes (fill all sets) ->
# 16 reads (all hits) ->
# 16 conflict writes at +0x1000 (evict each set) ->
# 1 final read of an evicted line (miss+refill)
#----------------------------------------------------------------------
def stress_entire_cache_counts_exact():
  tv = []

  # -----------------------------
  # Phase A: 16 writes (fill)
  # addr = 0x0000 + i*0x10  (i = 0..15)  -- different index each time
  # -----------------------------
  for i in range(16):
    addr = 0x0000 + (i << 4)          # 16B per line
    data = 0xAAAA0000 + addr          # unique data per line
    tv += [ req('wr', i, addr, 0, data), resp('wr', i, 0, 0, 0) ]

  # -----------------------------
  # Phase B: 16 reads (all hits)
  # -----------------------------
  for i in range(16):
    addr = 0x0000 + (i << 4)
    data = 0xAAAA0000 + addr
    tv += [ req('rd', 0x10 + i, addr, 0, 0), resp('rd', 0x10 + i, 1, 0, data) ]

  # -----------------------------
  # Phase C: 16 conflict writes to same indexes with different tag
  # addr' = 0x1000 + i*0x10  (same index, new tag) -> evict old line
  # -----------------------------
  for i in range(16):
    addr2 = 0x1000 + (i << 4)         # +0x1000 keeps index, changes tag
    data2 = 0xBBBB0000 + addr2
    tv += [ req('wr', 0x20 + i, addr2, 0, data2), resp('wr', 0x20 + i, 0, 0, 0) ]

  # -----------------------------
  # Phase D: final single read of an old address (should miss+refill)
  # Pick index 0 old address = 0x0000
  # -----------------------------
  addr_final = 0x0000
  data_final = 0xAAAA0000 + addr_final
  tv += [ req('rd', 0x30, addr_final, 0, 0), resp('rd', 0x30, 0, 0, data_final) ]

  return tv

def capacity_of_miss_cacheline():
  tv = []

  # ------------------------------------------------------------
  # Phase A: Fill all 32 cache lines (different index)
  # ------------------------------------------------------------
  for i in range(32):
    addr = 0x0000 + (i << 4)   # 0x0000, 0x0010, 0x0020 ... 0x01F0
    data = 0xAAAA0000 + addr
    tv += [ req('wr', i, addr, 0, data), resp('wr', i, 0, 0, 0) ]

  # ------------------------------------------------------------
  # Phase B: Access 32 more *unique* lines (no index overlap)
  # +0x2000 ensures different tag bits while keeping index distinct
  # This exceeds cache capacity (32 lines → 64 unique lines total)
  # ------------------------------------------------------------
  for i in range(32):
    addr = 0x2000 + (i << 4)   # 0x2000, 0x2010 ... 0x21F0
    data = 0xBBBB0000 + addr
    tv += [ req('wr', 0x20 + i, addr, 0, data), resp('wr', 0x20 + i, 0, 0, 0) ]

  # ------------------------------------------------------------
  # Phase C: Access one of the earliest lines again (should miss)
  # Because total capacity exceeded, line was evicted.
  # ------------------------------------------------------------
  addr_final = 0x0000          # first line from Phase A
  data_final = 0xAAAA0000 + addr_final
  tv += [ req('rd', 0x60, addr_final, 0, 0), resp('rd', 0x60, 0, 0, data_final) ]

  return tv

#-------------------------------------------------------------------------
# Generic tests
#-------------------------------------------------------------------------

test_case_table_generic = mk_test_case_table([
  (                                    "msg_func                    mem_data_func stall lat src sink"),

  [ "write_init_word",                  write_init_word,            None,         0.0,  0,  0,  0    ],
  [ "write_init_multi_word",            write_init_multi_word,      None,         0.0,  0,  0,  0    ],
  [ "write_init_cacheline",             write_init_cacheline,       None,         0.0,  0,  0,  0    ],
  [ "write_init_multi_cacheline",       write_init_multi_cacheline, None,         0.0,  0,  0,  0    ],
  [ "write_init_multi_word_sink_delay", write_init_multi_word,      None,         0.0,  0,  0,  10   ],
  [ "write_init_multi_word_src_delay",  write_init_multi_word,      None,         0.0,  0,  10, 0    ],
  [ "write_init_multi_cacheline_src_delay", write_init_multi_cacheline, data_512B, 0.9, 3, 5, 0 ],
  [ "write_init_multi_cacheline_sink_delay", write_init_multi_cacheline, data_512B, 0.9, 3, 0, 5 ],

  [ "read_hit_word",                    read_hit_word,              None,         0.0,  0,  0,  0    ],
  [ "read_hit_multi_word",              read_hit_multi_word,        None,         0.0,  0,  0,  0    ],
  [ "read_hit_cacheline",               read_hit_cacheline,         None,         0.0,  0,  0,  0    ],
  [ "read_hit_multi_cacheline",         read_hit_multi_cacheline,   None,         0.0,  0,  0,  0    ],
  [ "read_hit_multi_word_sink_delay",   read_hit_multi_word,        None,         0.0,  0,  0,  10   ],
  [ "read_hit_multi_word_src_delay",    read_hit_multi_word,        None,         0.0,  0,  10, 0    ],
  [ "read_hit_multi_cacheline_src_delay", read_hit_multi_cacheline, data_512B, 0.9, 3, 5, 0 ],
  [ "read_hit_multi_cacheline_sink_delay", read_hit_multi_cacheline, data_512B, 0.9, 3, 0, 5 ],

  [ "write_hit_word",                   write_hit_word,             None,         0.0,  0,  0,  0    ],
  [ "write_hit_multi_word",             write_hit_multi_word,       None,         0.0,  0,  0,  0    ],
  [ "write_hit_cacheline",              write_hit_cacheline,        None,         0.0,  0,  0,  0    ],
  [ "write_hit_multi_cacheline",        write_hit_multi_cacheline,  None,         0.0,  0,  0,  0    ],
  [ "write_hit_multi_word_sink_delay",  write_hit_multi_word,       None,         0.0,  0,  0,  10   ],
  [ "write_hit_multi_word_src_delay",   write_hit_multi_word,       None,         0.0,  0,  10, 0    ],
  [ "write_hit_multi_cacheline_src_delay", write_hit_multi_cacheline, data_512B, 0.9, 3, 5, 0 ],
  [ "write_hit_multi_cacheline_sink_delay", write_hit_multi_cacheline, data_512B, 0.9, 3, 0, 5 ],

  [ "read_miss_word",                   read_miss_word,             data_64B,     0.0,  0,  0,  0    ],
  [ "read_miss_multi_word",             read_miss_multi_word,       data_64B,     0.0,  0,  0,  0    ],
  [ "read_miss_cacheline",              read_miss_cacheline,        data_64B,     0.0,  0,  0,  0    ],
  [ "read_miss_multi_cacheline",        read_miss_multi_cacheline,  data_512B,    0.0,  0,  0,  0    ],
  [ "read_miss_multi_word_sink_delay",  read_miss_multi_word,       data_64B,     0.9,  3,  0,  10   ],
  [ "read_miss_multi_word_src_delay",   read_miss_multi_word,       data_64B,     0.9,  3,  10, 0    ],
  [ "read_miss_multi_cacheline_src_delay", read_miss_multi_cacheline, data_512B, 0.9, 3, 5, 0 ],
  [ "read_miss_multi_cacheline_sink_delay", read_miss_multi_cacheline, data_512B, 0.9, 3, 0, 5 ],

  [ "write_miss_word",                  write_miss_word,            data_64B,     0.0,  0,  0,  0    ],
  [ "write_miss_multi_word",            write_miss_multi_word,      data_64B,     0.0,  0,  0,  0    ],
  [ "write_miss_cacheline",             write_miss_cacheline,       data_64B,     0.0,  0,  0,  0    ],
  [ "write_miss_multi_cacheline",       write_miss_multi_cacheline, data_512B,    0.0,  0,  0,  0    ],
  [ "write_miss_multi_word_sink_delay", write_miss_multi_word,      data_64B,     0.9,  3,  0,  10   ],
  [ "write_miss_multi_word_src_delay",  write_miss_multi_word,      data_64B,     0.9,  3,  10, 0    ],
  [ "write_miss_multi_cacheline_src_delay", write_miss_multi_cacheline, data_512B, 0.9, 3, 5, 0 ],
  [ "write_miss_multi_cacheline_sink_delay", write_miss_multi_cacheline, data_512B, 0.9, 3, 0, 5 ],

  [ "evict_word",                       evict_word,                 data_512B,    0.0,  0,  0,  0    ],
  [ "evict_multi_word",                 evict_multi_word,           data_512B,    0.0,  0,  0,  0    ],
  [ "evict_cacheline",                  evict_cacheline,            data_512B,    0.0,  0,  0,  0    ],
  [ "evict_multi_cacheline",            evict_multi_cacheline,      data_512B,    0.0,  0,  0,  0    ],
  [ "evict_multi_word_sink_delay",      evict_multi_word,           data_512B,    0.9,  3,  0,  10   ],
  [ "evict_multi_word_src_delay",       evict_multi_word,           data_512B,    0.9,  3,  10, 0    ],
  [ "evict_multi_cacheline_src_delay", evict_cacheline, data_512B, 0.9, 3, 5, 0 ],
  [ "evict_multi_cacheline_sink_delay", evict_multi_cacheline, data_512B, 0.9, 3, 0, 5 ],


  [ "read_hit_clean_word",          read_hit_clean_word,          None, 0.0, 0, 0, 0 ],
  [ "read_hit_clean_multi_word",    read_hit_clean_multi_word,    None, 0.0, 0, 0, 0 ],
  [ "read_hit_clean_cacheline",     read_hit_clean_cacheline,     None, 0.0, 0, 0, 0 ],
  [ "read_hit_clean_multi_cacheline", read_hit_clean_multi_cacheline, None, 0.0, 0, 0, 0 ],
  [ "read_hit_clean_multi_word_sink_delay",      read_hit_clean_multi_word,           data_512B,    0.9,  3,  0,  10   ],
  [ "read_hit_clean_multi_word_src_delay",       read_hit_clean_multi_word,           data_512B,    0.9,  3,  10, 0    ],
  [ "read_hit_clean_cacheline_src_delay", read_hit_clean_multi_cacheline, data_512B, 0.9, 3, 5, 0 ],
  [ "read_hit_clean_cacheline_sink_delay", read_hit_clean_multi_cacheline, data_512B, 0.9, 3, 0, 5 ],

  [ "write_hit_clean_word",             write_hit_clean_word,             None, 0.0, 0, 0, 0 ],
  [ "write_hit_clean_multi_word",       write_hit_clean_multi_word,       None, 0.0, 0, 0, 0 ],
  [ "write_hit_clean_cacheline",        write_hit_clean_cacheline,        None, 0.0, 0, 0, 0 ],
  [ "write_hit_clean_multi_cacheline",  write_hit_clean_multi_cacheline,  None, 0.0, 0, 0, 0 ],
  [ "write_hit_clean_multi_word_sink_delay",      write_hit_clean_multi_word,           data_512B,    0.9,  3,  0,  10   ],
  [ "write_hit_clean_multi_word_src_delay",       write_hit_clean_multi_word,           data_512B,    0.9,  3,  10, 0    ],
  [ "write_hit_clean_multi_cacheline_src_delay", write_hit_clean_multi_cacheline, data_512B, 0.9, 3, 5, 0 ],
  [ "write_hit_clean_multi_cacheline_sink_delay", write_hit_clean_multi_cacheline, data_512B, 0.9, 3, 0, 5 ],

  [ "read_hit_dirty_word",              read_hit_dirty_word,              None,  0.0,  0,  0,  0 ],
  [ "read_hit_dirty_multi_word",        read_hit_dirty_multi_word,        None,  0.0,  0,  0,  0 ],
  [ "read_hit_dirty_cacheline",         read_hit_dirty_cacheline,         None,  0.0,  0,  0,  0 ],
  [ "read_hit_dirty_multi_cacheline",   read_hit_dirty_multi_cacheline,   None,  0.0,  0,  0,  0 ],
  [ "read_hit_dirty_multi_word_sink_delay",      read_hit_dirty_multi_word,           data_512B,    0.9,  3,  0,  10   ],
  [ "read_hit_dirty_multi_word_src_delay",       read_hit_dirty_multi_word,           data_512B,    0.9,  3,  10, 0    ],
  [ "read_hit_dirty_cacheline_src_delay", read_hit_dirty_cacheline, data_512B, 0.9, 3, 5, 0 ],
  [ "read_hit_dirty_cacheline_sink_delay", read_hit_dirty_cacheline, data_512B, 0.9, 3, 0, 5 ],

  [ "write_hit_dirty_word",                write_hit_dirty_word,                None, 0.0, 0, 0, 0 ],
  [ "write_hit_dirty_multi_word",          write_hit_dirty_multi_word,          None, 0.0, 0, 0, 0 ],
  [ "write_hit_dirty_cacheline",           write_hit_dirty_cacheline,           None, 0.0, 0, 0, 0 ],
  [ "write_hit_dirty_multi_cacheline",     write_hit_dirty_multi_cacheline,     None, 0.0, 0, 0, 0 ],
  [ "write_hit_dirty_multi_word_sink_delay",       write_hit_dirty_multi_word,       None, 0.9, 3, 0, 10 ],
  [ "write_hit_dirty_multi_word_src_delay",        write_hit_dirty_multi_word,       None, 0.9, 3, 10, 0 ],
  [ "write_hit_dirty_multi_cacheline_sink_delay",  write_hit_dirty_multi_cacheline,  None, 0.9, 3, 0, 10 ],
  [ "write_hit_dirty_multi_cacheline_src_delay",   write_hit_dirty_multi_cacheline,  None, 0.9, 3, 10, 0 ],

  [ "read_miss_no_exict_word",                   read_miss_no_evict_word,             data_64B,     0.0,  0,  0,  0    ],
  [ "read_miss_multi_no_exict_word",             read_miss_multi_no_evict_word,       data_64B,     0.0,  0,  0,  0    ],
  [ "read_miss_no_exict_cacheline",              read_miss_no_evict_cacheline,        data_64B,     0.0,  0,  0,  0    ],
  [ "read_miss_multi_no_exict_cacheline",        read_miss_multi_no_evict_cacheline,  data_512B,    0.0,  0,  0,  0    ],
  [ "read_miss_multi_word_no_exict_sink_delay",  read_miss_multi_no_evict_word,       data_64B,     0.9,  3,  0,  10   ],
  [ "read_miss_multi_word_no_exict_src_delay",   read_miss_multi_no_evict_word,       data_64B,     0.9,  3,  10, 0    ],
  [ "read_miss_multi_cacheline_no_exict_src_delay", read_miss_multi_no_evict_cacheline, data_512B, 0.9, 3, 5, 0 ],
  [ "read_miss_multi_cacheline_no_exict_sink_delay", read_miss_multi_no_evict_cacheline, data_512B, 0.9, 3, 0, 5 ],

  [ "write_miss_word",                  write_miss_no_evict_word,            data_64B,     0.0,  0,  0,  0    ],
  [ "write_miss_multi_word",            write_miss_multi_no_evict_word,      data_64B,     0.0,  0,  0,  0    ],
  [ "write_miss_cacheline",             write_miss_no_evict_cacheline,       data_64B,     0.0,  0,  0,  0    ],
  [ "write_miss_multi_cacheline",       write_miss_multi_no_evict_cacheline, data_512B,    0.0,  0,  0,  0    ],
  [ "write_miss_multi_word_sink_delay", write_miss_multi_no_evict_word,      data_64B,     0.9,  3,  0,  10   ],
  [ "write_miss_multi_word_src_delay",  write_miss_multi_no_evict_word,      data_64B,     0.9,  3,  10, 0    ],
  [ "write_miss_multi_cacheline_src_delay",  write_miss_multi_no_evict_cacheline, data_512B, 0.9, 3, 5, 0 ],
  [ "write_miss_multi_cacheline_sink_delay", write_miss_multi_no_evict_cacheline, data_512B, 0.9, 3, 0, 5 ],

  [ "read_miss_with_refill_and_eviction_word", read_miss_with_refill_and_eviction_word, data_512B, 0.9, 3, 0, 0 ],
  [ "read_miss_with_refill_and_eviction_multi_word", read_miss_with_refill_and_eviction_multi_word, data_512B, 0.9, 3, 0, 0 ],
  [ "read_miss_with_refill_and_eviction_cacheline", read_miss_with_refill_and_eviction_cacheline, data_512B, 0.9, 3, 0, 0 ],
  [ "read_miss_with_refill_and_eviction_multi_cacheline", read_miss_with_refill_and_eviction_multi_cacheline, data_512B, 0.9, 3, 0, 0 ],
  [ "read_miss_with_refill_and_eviction_multi_word_sink_delay", read_miss_with_refill_and_eviction_multi_word,      data_512B,     0.9,  3,  0,  10   ],
  [ "read_miss_with_refill_and_eviction_multi_word_src_delay",  read_miss_with_refill_and_eviction_multi_word,      data_512B,     0.9,  3,  10, 0    ],
  [ "read_miss_with_refill_and_eviction_multi_cacheline_src_delay",  read_miss_with_refill_and_eviction_multi_cacheline, data_512B, 0.9, 3, 5, 0 ],
  [ "read_miss_with_refill_and_eviction_multi_cacheline_sink_delay", read_miss_with_refill_and_eviction_multi_cacheline, data_512B, 0.9, 3, 0, 5 ],

  [ "write_miss_with_refill_and_eviction_word",                write_miss_with_refill_and_eviction_word,                data_512B,                0.9, 3, 0, 0 ],
  [ "write_miss_with_refill_and_eviction_multi_word",          write_miss_with_refill_and_eviction_multi_word,          data_512B,          0.9, 3, 0, 0 ],
  [ "write_miss_with_refill_and_eviction_multi_word_src_delay",write_miss_with_refill_and_eviction_multi_word,          data_512B,          0.9, 3, 10, 0 ],
  [ "write_miss_with_refill_and_eviction_multi_word_sink_delay",write_miss_with_refill_and_eviction_multi_word,         data_512B,          0.9, 3, 0, 10 ],
  [ "write_miss_with_refill_and_eviction_cacheline",           write_miss_with_refill_and_eviction_cacheline,           data_512B,           0.9, 3, 0, 0 ],
 
 
  [ "stress_entire_cache_counts_exact",stress_entire_cache_counts_exact,  data_512B,     0.9, 3, 0, 0 ],
  [ "stress_entire_cache_counts_exact_src_delay",stress_entire_cache_counts_exact,  data_512B,     0.9, 3, 0, 10 ],
  [ "stress_entire_cache_counts_exact_sink_delay",stress_entire_cache_counts_exact,  data_512B,     0.9, 3, 10, 0 ],
 
 
  [ "capacity_of_miss_cacheline",capacity_of_miss_cacheline,  data_512B,     0.9, 3, 0, 0 ],
  [ "capacity_of_miss_cacheline_src_delay",capacity_of_miss_cacheline,  data_512B,     0.9, 3, 10, 0 ],
  [ "capacity_of_miss_cacheline_sink_delay",capacity_of_miss_cacheline,  data_512B,     0.9, 3, 0, 10 ],
])

@pytest.mark.parametrize( **test_case_table_generic )
def test_generic( test_params, cmdline_opts ):
  run_test( CacheFL(), test_params, cmdline_opts, cmp_wo_test_field )

#-------------------------------------------------------------------------
# Test Case with Random Addresses and Data
#-------------------------------------------------------------------------

#=========================================================================
# Simple Address Pattern – Single Request Type (Write) with Random Data
#=========================================================================

import random

def simple_addr_single_type_random_data():
  tv = []
  ref_mem = {}  # reference memory dictionary

  base_addr = 0x1000     # starting address
  num_reqs  = 16         # number of words to write
  stride    = 4           # word stride (byte addressing)

  # Phase A: sequential writes
  for i in range(num_reqs):
    addr = base_addr + i * stride
    data = random.randint(0, 0xFFFFFFFF)
    ref_mem[addr] = data
    tv += [ req('wr', i, addr, 0, data), resp('wr', i, 0, 0, 0) ]

  # Phase B: read back same addresses → should hit & match
  for i in range(num_reqs):
    addr = base_addr + i * stride
    expected = ref_mem[addr]
    tv += [ req('rd', 0x10 + i, addr, 0, 0), resp('rd', 0x10 + i, 1, 0, expected) ]

  return tv

def simple_addr_random_type_random_data_a():
  tv = []
  ref_mem = {}
  base_addr = 0x1000
  num_reqs  = 20
  stride    = 4

  # Initialize all locations with 0
  for i in range(num_reqs):
    addr = base_addr + i * stride
    ref_mem[addr] = 0xabcd1000 + i*4

  # Phase A: randomly choose rd/wr requests on simple sequential addresses
  for i in range(num_reqs * 2):
    addr = base_addr + (i % num_reqs) * stride
    op   = random.choice(['rd', 'wr'])
    if op == 'wr':
      data = random.randint(0, 0xFFFFFFFF)
      ref_mem[addr] = data
      tv += [ req('wr', i, addr, 0, data), resp('wr', i, 0, 0, 0) ]
    else:
      expected = ref_mem[addr]
      tv += [ req('rd', i, addr, 0, 0), resp('rd', i, 0, 0, expected) ]

  return tv

import random

#----------------------------------------------------------------------
# Random address patterns, request types, and data
#----------------------------------------------------------------------
# - Addresses, operations, and data are all randomized
# - Reference memory tracks last written value for each address
# - Tests both cache correctness (hit/miss behavior) and write-back logic
#----------------------------------------------------------------------

def random_addr_type_data_test():
  tv = []
  ref_mem = {}                      
  num_reqs = 100                     # total random transactions
  base_addr = 0x0000
  addr_space = 0x4000                # randomize addresses within 16KB range
  stride = 0x4                       # word-aligned (4 bytes)

  for i in range(num_reqs):
    # 1. pick a random address aligned to 4 B
    addr = base_addr + random.randint(0, addr_space // stride - 1) * stride

    # 2. randomly choose operation
    op = random.choice(["rd", "wr"])

    if op == "wr":
      # 3A. generate random write data
      data = random.randint(0, 0xFFFFFFFF)
      ref_mem[addr] = data          
      tv += [ req("wr", i, addr, 0, data),
              resp("wr", i, 0, 0, 0) ]

    else:
      # 3B. expected data = last written value or 0 if not written yet
      expected = ref_mem.get(addr, 0)
      tv += [ req("rd", i, addr, 0, 0),
              resp("rd", i, 1, 0, expected) ]

  return tv


def unit_stride_random_data_test():
  tv = []
  ref_mem = {}                      # Reference memory
  base_addr = 0x1000
  stride    = 0x10                  # 16B per cache line (unit stride)
  num_elems = 32                    # number of sequential accesses

  # ------------------------------------------------------------
  # Phase A: Write sequentially with random data
  # ------------------------------------------------------------
  for i in range(num_elems):
    addr = base_addr + i * stride
    data = random.randint(0, 0xFFFFFFFF)
    ref_mem[addr] = data
    tv += [
      req('wr', i, addr, 0, data),
      resp('wr', i, 0, 0, 0)
    ]

  # ------------------------------------------------------------
  # Phase B: Read sequentially (should all hit if cache retains them)
  # ------------------------------------------------------------
  for i in range(num_elems):
    addr = base_addr + i * stride
    expected = ref_mem[addr]
    tv += [
      req('rd', 0x20 + i, addr, 0, 0),
      resp('rd', 0x20 + i, 1, 0, expected)
    ]

  # ------------------------------------------------------------
  # Phase C: Repeat reads (test cache hit path)
  # ------------------------------------------------------------
  for i in range(num_elems):
    addr = base_addr + i * stride
    expected = ref_mem[addr]
    tv += [
      req('rd', 0x40 + i, addr, 0, 0),
      resp('rd', 0x40 + i, 1, 0, expected)
    ]

  return tv

import random

#----------------------------------------------------------------------
# Stride with random data
#----------------------------------------------------------------------
# Purpose:
# - Test cache behavior with non-contiguous but regular stride accesses
# - Each access is separated by a fixed stride (e.g. 0x40 bytes)
# - Data for writes is random
# - Reads verify correct data using a reference memory
#----------------------------------------------------------------------

def stride_random_data_test():
  tv = []
  ref_mem = {}                      # Reference memory
  base_addr = 0x1000
  stride    = 0x40                  # fixed stride = 64B (4 cache lines apart)
  num_elems = 32                    # number of memory operations
  total_ops = 64                    # number of total randomized accesses

  # ------------------------------------------------------------
  # Phase A: Write with fixed stride and random data
  # ------------------------------------------------------------
  for i in range(num_elems):
    addr = base_addr + i * stride
    data = random.randint(0, 0xFFFFFFFF)
    ref_mem[addr] = data
    tv += [
      req('wr', i, addr, 0, data),
      resp('wr', i, 0, 0, 0)
    ]

  # ------------------------------------------------------------
  # Phase B: Read with same stride pattern (should be hits if cache large enough)
  # ------------------------------------------------------------
  for i in range(num_elems):
    addr = base_addr + i * stride
    expected = ref_mem[addr]
    tv += [
      req('rd', 0x20 + i, addr, 0, 0),
      resp('rd', 0x20 + i, 1, 0, expected)
    ]

  # ------------------------------------------------------------
  # Phase C: Randomly interleave reads/writes with same stride pattern
  #          - simulate partial reuse (temporal locality test)
  # ------------------------------------------------------------
  for i in range(total_ops):
    addr = base_addr + ((i * stride) % (num_elems * stride))
    op = random.choice(['rd', 'wr'])

    if op == 'wr':
      data = random.randint(0, 0xFFFFFFFF)
      ref_mem[addr] = data
      tv += [ req('wr', 0x40 + i, addr, 0, data),
              resp('wr', 0x40 + i, 0, 0, 0) ]
    else:
      expected = ref_mem.get(addr, 0)
      tv += [ req('rd', 0x40 + i, addr, 0, 0),
              resp('rd', 0x40 + i, 1, 0, expected) ]

  return tv

import random

#----------------------------------------------------------------------
# Unit stride (high spatial) mixed with shared (high temporal) locality
#----------------------------------------------------------------------
# - Three arrays: a[], b[], c[]  allocated in separate address regions
# - Each array accessed sequentially (unit stride)
# - Access pattern alternates between arrays (temporal sharing)
# - Write random data, then read/modify in a mixed order
#----------------------------------------------------------------------

def mixed_spatial_temporal_locality_test():
  tv = []
  ref_mem = {}

  # Base addresses for 3 arrays
  base_a = 0x1000
  base_b = 0x2000
  base_c = 0x3800
  stride = 0x10         # 16B per cache line
  num_elems = 32

  # ------------------------------------------------------------
  # Phase A: Initialize all arrays with random data (simulate write)
  # ------------------------------------------------------------
  for i in range(num_elems):
    for base in [base_a, base_b, base_c]:
      addr = base + i * stride
      data = random.randint(0, 0xFFFFFFFF)
      ref_mem[addr] = data
      tv += [ req('wr', i, addr, 0, data), resp('wr', i, 0, 0, 0) ]

  # ------------------------------------------------------------
  # Phase B: Interleave reads to simulate computation like: a[i]*b[i]+c[i]
  # ------------------------------------------------------------
  for i in range(num_elems):
    # Read a[i]
    addr_a = base_a + i * stride
    val_a  = ref_mem[addr_a]
    tv += [ req('rd', 0x20 + i, addr_a, 0, 0),
            resp('rd', 0x20 + i, 1, 0, val_a) ]

    # Read b[i]
    addr_b = base_b + i * stride
    val_b  = ref_mem[addr_b]
    tv += [ req('rd', 0x40 + i, addr_b, 0, 0),
            resp('rd', 0x40 + i, 1, 0, val_b) ]

    # Read c[i]
    addr_c = base_c + i * stride
    val_c  = ref_mem[addr_c]
    tv += [ req('rd', 0x60 + i, addr_c, 0, 0),
            resp('rd', 0x60 + i, 1, 0, val_c) ]

  # ------------------------------------------------------------
  # Phase C: Randomly update some elements in each array
  # ------------------------------------------------------------
  for i in range(num_elems // 2):
    for base in [base_a, base_b, base_c]:
      addr = base + random.randint(0, num_elems - 1) * stride
      data = random.randint(0, 0xFFFFFFFF)
      ref_mem[addr] = data
      tv += [ req('wr', 0x80 + i, addr, 0, data),
              resp('wr', 0x80 + i, 0, 0, 0) ]

  # ------------------------------------------------------------
  # Phase D: Re-read a few elements (temporal locality reuse)
  # ------------------------------------------------------------
  for i in range(8):
    for base in [base_a, base_b, base_c]:
      addr = base + (i * stride)
      expected = ref_mem[addr]
      tv += [ req('rd', 0xA0 + i, addr, 0, 0),
              resp('rd', 0xA0 + i, 1, 0, expected) ]

  return tv

test_case_table_random = mk_test_case_table([
  (                        "msg_func       mem_data_func stall lat src sink"),
  [ "simple_addr_single_type_random_data",simple_addr_single_type_random_data,  data_512B,     0.9, 3, 0, 0 ],
  [ "simple_addr_single_type_random_data_src_delay",simple_addr_single_type_random_data,  data_512B,     0.9, 3, 10, 0 ],
  [ "simple_addr_single_type_random_data_sink_delay",simple_addr_single_type_random_data,  data_512B,     0.9, 3, 0, 10 ],

  [ "simple_addr_random_type_random_data_a",simple_addr_random_type_random_data_a,  data_512B,     0.9, 3, 0, 0 ],
  [ "simple_addr_random_type_random_data_a_src_delay",simple_addr_random_type_random_data_a,  data_512B,     0.9, 3, 10, 0 ],
  [ "simple_addr_random_type_random_data_a_sink_delay",simple_addr_random_type_random_data_a,  data_512B,     0.9, 3, 0, 10 ],

  [ "random_addr_type_data_test",           random_addr_type_data_test,  data_512B,     0.9, 3, 0, 0 ],
  [ "random_addr_type_data_test_src_delay", random_addr_type_data_test,  data_512B,     0.9, 3, 10, 0 ],
  [ "random_addr_type_data_test_sink_delay",random_addr_type_data_test,  data_512B,     0.9, 3, 0, 10 ],

  [ "unit_stride_random_data_test",           unit_stride_random_data_test,  data_512B,     0.9, 3, 0, 0 ],
  [ "unit_stride_random_data_test_src_delay", unit_stride_random_data_test,  data_512B,     0.9, 3, 10, 0 ],
  [ "unit_stride_random_data_test_sink_delay",unit_stride_random_data_test,  data_512B,     0.9, 3, 0, 10 ],

  [ "stride_random_data_test",           stride_random_data_test,  data_512B,     0.9, 3, 0, 0 ],
  [ "stride_random_data_test_src_delay", stride_random_data_test,  data_512B,     0.9, 3, 10, 0 ],
  [ "stride_random_data_test_sink_delay",stride_random_data_test,  data_512B,     0.9, 3, 0, 10 ],

  [ "mixed_spatial_temporal_locality_test",           mixed_spatial_temporal_locality_test,  data_512B,     0.9, 3, 0, 0 ],
  [ "mixed_spatial_temporal_locality_test_src_delay", mixed_spatial_temporal_locality_test,  data_512B,     0.9, 3, 10, 0 ],
  [ "mixed_spatial_temporal_locality_test_sink_delay",mixed_spatial_temporal_locality_test,  data_512B,     0.9, 3, 0, 10 ],

])

@pytest.mark.parametrize( **test_case_table_random )
def test_random( test_params, cmdline_opts ):
  run_test( CacheFL(), test_params, cmdline_opts, cmp_wo_test_field )

#-------------------------------------------------------------------------
# Test Cases for Direct Mapped
#-------------------------------------------------------------------------
#------------------------------------------------------
# 1. Conflict miss, single word version
#------------------------------------------------------
def conflict_miss_word():
  return [
    req('wr', 0x0, 0x0000, 0, 0xAAAA0000), resp('wr', 0x0, 0, 0, 0),
    req('rd', 0x1, 0x0000, 0, 0),          resp('rd', 0x1, 1, 0, 0xAAAA0000),

    req('wr', 0x2, 0x0100, 0, 0xBBBB0100), resp('wr', 0x2, 0, 0, 0),
    req('rd', 0x3, 0x0100, 0, 0),          resp('rd', 0x3, 1, 0, 0xBBBB0100),

    req('rd', 0x4, 0x0000, 0, 0),          resp('rd', 0x4, 0, 0, 0xAAAA0000),
  ]


#------------------------------------------------------
# 2. Conflict miss, multi-word version
#------------------------------------------------------
def conflict_miss_multi_word():
  return [
    req('wr', 0x0, 0x0000, 0, 0xAAAA0000), resp('wr', 0x0, 0, 0, 0),
    req('wr', 0x1, 0x0004, 0, 0xAAAA0004), resp('wr', 0x1, 1, 0, 0),
    req('rd', 0x2, 0x0000, 0, 0),          resp('rd', 0x2, 1, 0, 0xAAAA0000),
    req('rd', 0x3, 0x0004, 0, 0),          resp('rd', 0x3, 1, 0, 0xAAAA0004),

    req('wr', 0x4, 0x0100, 0, 0xBBBB0100), resp('wr', 0x4, 0, 0, 0),
    req('wr', 0x5, 0x0104, 0, 0xBBBB0104), resp('wr', 0x5, 1, 0, 0),
    req('rd', 0x6, 0x0100, 0, 0),          resp('rd', 0x6, 1, 0, 0xBBBB0100),
    req('rd', 0x7, 0x0104, 0, 0),          resp('rd', 0x7, 1, 0, 0xBBBB0104),

    req('rd', 0x8, 0x0000, 0, 0),          resp('rd', 0x8, 0, 0, 0xAAAA0000),
  ]


#------------------------------------------------------
# 3. Conflict miss, cacheline version
#------------------------------------------------------
def conflict_miss_cacheline():
  return [
    req('wr', 0x0, 0x0000, 0, 0x11111111), resp('wr', 0x0, 0, 0, 0),
    req('wr', 0x1, 0x0004, 0, 0x22222222), resp('wr', 0x1, 1, 0, 0),
    req('wr', 0x2, 0x0008, 0, 0x33333333), resp('wr', 0x2, 1, 0, 0),
    req('wr', 0x3, 0x000C, 0, 0x44444444), resp('wr', 0x3, 1, 0, 0),
    req('rd', 0x4, 0x0000, 0, 0),          resp('rd', 0x4, 1, 0, 0x11111111),

    req('wr', 0x5, 0x0100, 0, 0xAAAA0000), resp('wr', 0x5, 0, 0, 0),
    req('wr', 0x6, 0x0104, 0, 0xBBBB0000), resp('wr', 0x6, 1, 0, 0),
    req('wr', 0x7, 0x0108, 0, 0xCCCC0000), resp('wr', 0x7, 1, 0, 0),
    req('wr', 0x8, 0x010C, 0, 0xDDDD0000), resp('wr', 0x8, 1, 0, 0),
    req('rd', 0x9, 0x0100, 0, 0),          resp('rd', 0x9, 1, 0, 0xAAAA0000),

    req('rd', 0xA, 0x0000, 0, 0),          resp('rd', 0xA, 0, 0, 0x11111111),
  ]


#------------------------------------------------------
# 4. Conflict miss, multi-cacheline version
#------------------------------------------------------
def conflict_miss_multi_cacheline():
  return [
    req('wr', 0x0, 0x0000, 0, 0xAAAA0000), resp('wr', 0x0, 0, 0, 0),
    req('wr', 0x1, 0x1000, 0, 0xBBBB1000), resp('wr', 0x1, 0, 0, 0),
    req('wr', 0x2, 0x2000, 0, 0xCCCC2000), resp('wr', 0x2, 0, 0, 0),
    req('wr', 0x3, 0x3000, 0, 0xDDDD3000), resp('wr', 0x3, 0, 0, 0),

    req('rd', 0x4, 0x0000, 0, 0), resp('rd', 0x4, 0, 0, 0xAAAA0000),
    req('rd', 0x5, 0x1000, 0, 0), resp('rd', 0x5, 0, 0, 0xBBBB1000),
    req('rd', 0x6, 0x2000, 0, 0), resp('rd', 0x6, 0, 0, 0xCCCC2000),
    req('rd', 0x7, 0x3000, 0, 0), resp('rd', 0x7, 0, 0, 0xDDDD3000),

    req('rd', 0x8, 0x0000, 0, 0), resp('rd', 0x8, 0, 0, 0xAAAA0000),
    req('rd', 0x9, 0x1000, 0, 0), resp('rd', 0x9, 0, 0, 0xBBBB1000),
  ]


#----------------------------------------------------------------------
# Capacity miss test case for 512B cache (32 lines × 16B each)
#----------------------------------------------------------------------
# Goal:
# - Fill 32 unique cache lines (Phase A)
# - Access another 32 unique lines (Phase B) -> exceed 512B capacity
# - Access the first address again (Phase C) -> should miss + refill
#----------------------------------------------------------------------

def capacity_miss_cacheline():
  tv = []

  # ------------------------------------------------------------
  # Phase A: Fill all 32 cache lines (different index)
  # ------------------------------------------------------------
  for i in range(32):
    addr = 0x0000 + (i << 4)   # 0x0000, 0x0010, 0x0020 ... 0x01F0
    data = 0xAAAA0000 + addr
    tv += [ req('wr', i, addr, 0, data), resp('wr', i, 0, 0, 0) ]

  # ------------------------------------------------------------
  # Phase B: Access 32 more *unique* lines (no index overlap)
  # +0x2000 ensures different tag bits while keeping index distinct
  # This exceeds cache capacity (32 lines → 64 unique lines total)
  # ------------------------------------------------------------
  for i in range(32):
    addr = 0x2000 + (i << 4)   # 0x2000, 0x2010 ... 0x21F0
    data = 0xBBBB0000 + addr
    tv += [ req('wr', 0x20 + i, addr, 0, data), resp('wr', 0x20 + i, 0, 0, 0) ]

  # ------------------------------------------------------------
  # Phase C: Access one of the earliest lines again (should miss)
  # Because total capacity exceeded, line was evicted.
  # ------------------------------------------------------------
  addr_final = 0x0000          # first line from Phase A
  data_final = 0xAAAA0000 + addr_final
  tv += [ req('rd', 0x60, addr_final, 0, 0), resp('rd', 0x60, 0, 0, data_final) ]

  return tv

def four_bank_cache_test():
  tv = []

  addr_bank0 = 0x0000  # bank 0
  addr_bank1 = 0x0010  # bank 1
  addr_bank2 = 0x0020  # bank 2
  addr_bank3 = 0x0030  # bank 3

  data0, data1, data2, data3 = 0xAAA0000, 0xBBB0000, 0xCCC0000, 0xDDD0000

  # Write to 4 banks in quick succession (should proceed in parallel)
  tv += [
    req('wr', 0x00, addr_bank0, 0, data0), resp('wr', 0x00, 0, 0, 0),
    req('wr', 0x01, addr_bank1, 0, data1), resp('wr', 0x01, 0, 0, 0),
    req('wr', 0x02, addr_bank2, 0, data2), resp('wr', 0x02, 0, 0, 0),
    req('wr', 0x03, addr_bank3, 0, data3), resp('wr', 0x03, 0, 0, 0),
  ]

  tv += [
    req('rd', 0x10, addr_bank0, 0, 0), resp('rd', 0x10, 1, 0, data0),
    req('rd', 0x11, addr_bank1, 0, 0), resp('rd', 0x11, 1, 0, data1),
    req('rd', 0x12, addr_bank2, 0, 0), resp('rd', 0x12, 1, 0, data2),
    req('rd', 0x13, addr_bank3, 0, 0), resp('rd', 0x13, 1, 0, data3),
  ]

  addr_conflict1 = 0x0040  # also bank 0
  addr_conflict2 = 0x0080  # also bank 0
  data_c1, data_c2 = 0xEEEE0000, 0xFFFF0000

  tv += [
    req('wr', 0x20, addr_conflict1, 0, data_c1), resp('wr', 0x20, 0, 0, 0),
    req('wr', 0x21, addr_conflict2, 0, data_c2), resp('wr', 0x21, 0, 0, 0),
  ]

  tv += [
    req('rd', 0x30, addr_bank1, 0, 0), resp('rd', 0x30, 1, 0, data1),
    req('wr', 0x31, addr_bank2, 0, 0xABCDABCD), resp('wr', 0x31, 1, 0, 0),
    req('rd', 0x32, addr_bank3, 0, 0), resp('rd', 0x32, 1, 0, data3),
  ]

  return tv

def write_miss_with_refill_and_eviction_direct_mapped():
  return [
    # Step 1: First write miss -> refill + dirty
    req('wr', 0x0, 0x1000, 0, 0xAAAA1000), resp('wr', 0x0, 0, 0, 0),

    # Step 2: Write to new tag (same index) -> eviction (write-back) + refill
    req('wr', 0x1, 0x1100, 0, 0xAAAA1100), resp('wr', 0x1, 0, 0, 0),

    # Step 3: Read the currently cached line -> hit
    req('rd', 0x2, 0x1100, 0, 0), resp('rd', 0x2, 1, 0, 0xAAAA1100),

    # Step 4: Read back the evicted address -> miss + refill
    req('rd', 0x3, 0x1000, 0, 0), resp('rd', 0x3, 0, 0, 0xAAAA1000),
  ]


def stress_entire_cache():
  return [
    #------------------------------------------------------------
    # Fill all 16 cache lines with unique data
    # Each address spaced 0x10 apart (different index each time)
    #------------------------------------------------------------
    req('wr', 0x00, 0x0000, 0, 0xAAAA0000), resp('wr', 0x00, 0, 0, 0),
    req('wr', 0x01, 0x0010, 0, 0xAAAA0010), resp('wr', 0x01, 0, 0, 0),
    req('wr', 0x02, 0x0020, 0, 0xAAAA0020), resp('wr', 0x02, 0, 0, 0),
    req('wr', 0x03, 0x0030, 0, 0xAAAA0030), resp('wr', 0x03, 0, 0, 0),
    req('wr', 0x04, 0x0040, 0, 0xAAAA0040), resp('wr', 0x04, 0, 0, 0),
    req('wr', 0x05, 0x0050, 0, 0xAAAA0050), resp('wr', 0x05, 0, 0, 0),
    req('wr', 0x06, 0x0060, 0, 0xAAAA0060), resp('wr', 0x06, 0, 0, 0),
    req('wr', 0x07, 0x0070, 0, 0xAAAA0070), resp('wr', 0x07, 0, 0, 0),
    req('wr', 0x08, 0x0080, 0, 0xAAAA0080), resp('wr', 0x08, 0, 0, 0),
    req('wr', 0x09, 0x0090, 0, 0xAAAA0090), resp('wr', 0x09, 0, 0, 0),
    req('wr', 0x0A, 0x00A0, 0, 0xAAAA00A0), resp('wr', 0x0A, 0, 0, 0),
    req('wr', 0x0B, 0x00B0, 0, 0xAAAA00B0), resp('wr', 0x0B, 0, 0, 0),
    req('wr', 0x0C, 0x00C0, 0, 0xAAAA00C0), resp('wr', 0x0C, 0, 0, 0),
    req('wr', 0x0D, 0x00D0, 0, 0xAAAA00D0), resp('wr', 0x0D, 0, 0, 0),
    req('wr', 0x0E, 0x00E0, 0, 0xAAAA00E0), resp('wr', 0x0E, 0, 0, 0),
    req('wr', 0x0F, 0x00F0, 0, 0xAAAA00F0), resp('wr', 0x0F, 0, 0, 0),

    #------------------------------------------------------------
    # Read all cache lines back (should all hit)
    #------------------------------------------------------------
    req('rd', 0x10, 0x0000, 0, 0), resp('rd', 0x10, 1, 0, 0xAAAA0000),
    req('rd', 0x11, 0x0010, 0, 0), resp('rd', 0x11, 1, 0, 0xAAAA0010),
    req('rd', 0x12, 0x00F0, 0, 0), resp('rd', 0x12, 1, 0, 0xAAAA00F0),

    #------------------------------------------------------------
    # Trigger conflict misses: reuse same index with different tag
    # (addresses separated by 0x1000 = 4096B share same index bits)
    #------------------------------------------------------------
    req('wr', 0x13, 0x1000, 0, 0xBBBB1000), resp('wr', 0x13, 0, 0, 0),
    req('wr', 0x14, 0x1010, 0, 0xBBBB1010), resp('wr', 0x14, 0, 0, 0),

    # Read old evicted line (should miss and refill)
    req('rd', 0x15, 0x0000, 0, 0), resp('rd', 0x15, 0, 0, 0xAAAA0000),
  ]



test_case_table_dmap = mk_test_case_table([
  (                                   "msg_func                         mem_data_func stall lat src sink"),
  [ "conflict_miss_word",                conflict_miss_word,                data_512B,                0.9, 3, 0, 0 ],
  [ "conflict_miss_multi_word",          conflict_miss_multi_word,          data_512B,          0.9, 3, 0, 0 ],
  [ "conflict_miss_multi_word_src_delay",conflict_miss_multi_word,          data_512B,          0.9, 3, 10, 0 ],
  [ "conflict_miss_multi_word_sink_delay",conflict_miss_multi_word,         data_512B,          0.9, 3, 0, 10 ],
  [ "conflict_miss_cacheline",           conflict_miss_cacheline,           data_512B,           0.9, 3, 0, 0 ],
  [ "conflict_miss_multi_cacheline",     conflict_miss_multi_cacheline,      data_512B,     0.9, 3, 0, 0 ],
  [ "conflict_miss_multi_cacheline_src_delay", conflict_miss_multi_cacheline,  data_512B,     0.9, 3, 10, 0 ],
  [ "conflict_miss_multi_cacheline_sink_delay",conflict_miss_multi_cacheline,  data_512B,     0.9, 3, 0, 10 ],

  [ "capacity_miss_cacheline",capacity_miss_cacheline,  data_512B,     0.9, 3, 0, 0 ],
  [ "capacity_miss_cacheline_src_delay",capacity_miss_cacheline,  data_512B,     0.9, 3, 10, 0 ],
  [ "capacity_miss_cacheline_sink_delay",capacity_miss_cacheline,  data_512B,     0.9, 3, 0, 10 ],

  [ "four_bank_cache_test",four_bank_cache_test,  data_512B,     0.9, 3, 0, 0 ],
  [ "four_bank_cache_test",four_bank_cache_test,  data_512B,     0.9, 3, 10, 0 ],
  [ "four_bank_cache_test",four_bank_cache_test,  data_512B,     0.9, 3, 0, 10 ],

  [ "write_miss_with_refill_and_eviction_direct_mapped",     write_miss_with_refill_and_eviction_direct_mapped,      data_512B,     0.9, 3, 0, 0 ],
  [ "write_miss_with_refill_and_eviction_direct_mapped_src_delay", write_miss_with_refill_and_eviction_direct_mapped,  data_512B,     0.9, 3, 10, 0 ],
  [ "write_miss_with_refill_and_eviction_direct_mapped_sink_delay",write_miss_with_refill_and_eviction_direct_mapped,  data_512B,     0.9, 3, 0, 10 ],

[ "stress_entire_cache",stress_entire_cache,  data_512B,     0.9, 3, 0, 00 ],
  [ "stress_entire_cache_src_delay",stress_entire_cache,  data_512B,     0.9, 3, 0, 10 ],
  [ "stress_entire_cache_sink_delay",stress_entire_cache,  data_512B,     0.9, 3, 10, 0 ],

])

@pytest.mark.parametrize( **test_case_table_dmap )
def test_dmap( test_params, cmdline_opts ):
  run_test( CacheFL(), test_params, cmdline_opts, cmp_wo_test_field )

#-------------------------------------------------------------------------
# Test Cases for Set Associative
#-------------------------------------------------------------------------

#----------------------------------------------------------------------
# LRU replacement policy test (4-way set-associative cache)
#----------------------------------------------------------------------
# Goal:
# - Fill all 4 ways in one set (index 0)
# - Re-access some lines to refresh LRU order
# - Insert a 5th line (same set, new tag) → should evict the least recently used
#----------------------------------------------------------------------

def lru_replacement_policy_test():
  tv = []

  # ------------------------------------------------------------
  # Phase A: Fill both ways in same set (index bits = [7:4] = 0)
  # ------------------------------------------------------------
  addr_A = 0x0000         # tag=0, index=0
  data_A = 0xAAAA0000
  tv += [ req('wr', 0x00, addr_A, 0, data_A), resp('wr', 0x00, 0, 0, 0) ]

  addr_B = 0x0100         # tag=1, index=0 (bits [7:4]=0000)
  data_B = 0xBBBB0000
  tv += [ req('wr', 0x01, addr_B, 0, data_B), resp('wr', 0x01, 0, 0, 0) ]

  # ------------------------------------------------------------
  # Phase B: Access A again to refresh LRU state
  # After this: Way0(A)=MRU, Way1(B)=LRU
  # ------------------------------------------------------------
  tv += [ req('rd', 0x02, addr_A, 0, 0), resp('rd', 0x02, 1, 0, data_A) ]

  # ------------------------------------------------------------
  # Phase C: Insert new block C (same index, new tag)
  # Should evict B (LRU) and make C the new MRU
  # After this: Way0(A)=LRU, Way1(C)=MRU
  # ------------------------------------------------------------
  addr_C = 0x0200         # tag=2, index=0 (bits [7:4]=0000)
  data_C = 0xCCCC0000
  tv += [ req('wr', 0x03, addr_C, 0, data_C), resp('wr', 0x03, 0, 0, 0) ]

  # ------------------------------------------------------------
  # Phase D: Read all three addresses to verify replacement
  # ------------------------------------------------------------

  # 2. addr_A should MISS (became LRU and replaced by C)
  #    <-- This line changed from hit(1) → miss(0)
  tv += [ req('rd', 0x05, addr_A, 0, 0), resp('rd', 0x05, 1, 0, data_A) ]

  # 3. addr_C should HIT (just written, MRU)
  tv += [ req('rd', 0x06, addr_C, 0, 0), resp('rd', 0x06, 1, 0, data_C) ]

  return tv


def alt_dual_hit_conflict_test():
  tv = []

  # Fill both ways of same set
  addr_A = 0x0000  # tag 0, index 0
  addr_B = 0x1000  # tag 1, same index 0
  data_A, data_B = 0xAAAA0000, 0xBBBB0000

  tv += [
    req('wr', 0x0, addr_A, 0, data_A), resp('wr', 0x0, 0, 0, 0),
    req('wr', 0x1, addr_B, 0, data_B), resp('wr', 0x1, 0, 0, 0),
  ]

  # Both valid in same set → access should hit correct one
  tv += [ req('rd', 0x2, addr_A, 0, 0), resp('rd', 0x2, 1, 0, data_A) ]
  tv += [ req('rd', 0x3, addr_B, 0, 0), resp('rd', 0x3, 1, 0, data_B) ]
  return tv

def alt_LRU_incorrect_eviction_test():
  tv = []
  addr_A, addr_B, addr_C = 0x0000, 0x1000, 0x2000
  data_A, data_B, data_C = 0xAAAA, 0xBBBB, 0xCCCC

  # Fill two ways
  tv += [
    req('wr', 0x0, addr_A, 0, data_A), resp('wr', 0x0, 0, 0, 0),
    req('wr', 0x1, addr_B, 0, data_B), resp('wr', 0x1, 0, 0, 0),
  ]
  # Re-access addr_A → make B oldest
  tv += [ req('rd', 0x2, addr_A, 0, 0), resp('rd', 0x2, 1, 0, data_A) ]
  # Access new tag (C) → should evict B
  tv += [
    req('wr', 0x3, addr_C, 0, data_C), resp('wr', 0x3, 0, 0, 0),
    # Read B → should miss
    req('rd', 0x4, addr_B, 0, 0), resp('rd', 0x4, 0, 0, data_B),
  ]
  return tv

def alt_dirty_eviction_test():
  tv = []
  addr_A, addr_B, addr_C = 0x0000, 0x1000, 0x2000

  # Fill set, mark both dirty
  tv += [
    req('wr', 0x0, addr_A, 0, 0xAAAA), resp('wr', 0x0, 0, 0, 0),
    req('wr', 0x1, addr_B, 0, 0xBBBB), resp('wr', 0x1, 0, 0, 0),
  ]
  # New tag C should evict the oldest (A), but A is dirty → needs writeback
  tv += [
    req('wr', 0x2, addr_C, 0, 0xCCCC), resp('wr', 0x2, 0, 0, 0),
    req('rd', 0x3, addr_A, 0, 0), resp('rd', 0x3, 0, 0, 0xAAAA),
  ]
  return tv

def write_miss_with_refill_and_eviction_multi_cacheline():
  return [
    # Phase A: Fill two cache lines in same set (index bits [7:4]=0)
    req('wr', 0x0, 0x0000, 0, 0xAAAA0000), resp('wr', 0x0, 0, 0, 0),
    req('wr', 0x1, 0x0100, 0, 0xBBBB0100), resp('wr', 0x1, 0, 0, 0),
    req('wr', 0x2, 0x0200, 0, 0xCCCC0200), resp('wr', 0x2, 0, 0, 0),

    req('rd', 0x3, 0x0000, 0, 0), resp('rd', 0x3, 0, 0, 0xAAAA0000),  # might be evicted
    req('rd', 0x4, 0x0200, 0, 0), resp('rd', 0x4, 1, 0, 0xCCCC0200),  # might be evicted
    req('rd', 0x5, 0x0000, 0, 0), resp('rd', 0x5, 1, 0, 0xAAAA0000),  # should hit
  ]

def stress_entire_cache_alt():
  return [
    #------------------------------------------------------------
    # Fill all 16 cache lines with unique data
    # Each address spaced 0x10 apart (different index each time)
    #------------------------------------------------------------
    req('wr', 0x00, 0x0000, 0, 0xAAAA0000), resp('wr', 0x00, 0, 0, 0),
    req('wr', 0x01, 0x0010, 0, 0xAAAA0010), resp('wr', 0x01, 0, 0, 0),
    req('wr', 0x02, 0x0020, 0, 0xAAAA0020), resp('wr', 0x02, 0, 0, 0),
    req('wr', 0x03, 0x0030, 0, 0xAAAA0030), resp('wr', 0x03, 0, 0, 0),
    req('wr', 0x04, 0x0040, 0, 0xAAAA0040), resp('wr', 0x04, 0, 0, 0),
    req('wr', 0x05, 0x0050, 0, 0xAAAA0050), resp('wr', 0x05, 0, 0, 0),
    req('wr', 0x06, 0x0060, 0, 0xAAAA0060), resp('wr', 0x06, 0, 0, 0),
    req('wr', 0x07, 0x0070, 0, 0xAAAA0070), resp('wr', 0x07, 0, 0, 0),

    #------------------------------------------------------------
    # Read all cache lines back (should all hit)
    #------------------------------------------------------------
    req('rd', 0x06, 0x0060, 0, 0xAAAA0060), resp('rd', 0x06, 1, 0, 0xAAAA0060),
    req('rd', 0x07, 0x0070, 0, 0xAAAA0070), resp('rd', 0x07, 1, 0, 0xAAAA0070),

    #------------------------------------------------------------
    # Trigger conflict misses: reuse same index with different tag
    # (addresses separated by 0x1000 = 4096B share same index bits)
    #------------------------------------------------------------
    req('wr', 0x08, 0x1000, 0, 0xBBBB1000), resp('wr', 0x08, 0, 0, 0),
    req('wr', 0x09, 0x1010, 0, 0xBBBB1010), resp('wr', 0x09, 0, 0, 0),

    # Read old evicted line (should miss and refill)
    req('rd', 0x10, 0x0000, 0, 0), resp('rd', 0x10, 1, 0, 0xAAAA0000),
  ]

test_case_table_sassoc = mk_test_case_table([
  (                       "msg_func            mem_data_func    stall lat src sink"),
  [ "lru_replacement_policy_test",           lru_replacement_policy_test,  data_512B,     0.9, 3, 0, 0 ],
  [ "lru_replacement_policy_test_src_delay", lru_replacement_policy_test,  data_512B,     0.9, 3, 10, 0 ],
  [ "lru_replacement_policy_test_sink_delay",lru_replacement_policy_test,  data_512B,     0.9, 3, 0, 10 ],

  [ "alt_dual_hit_conflict_test",           alt_dual_hit_conflict_test,  data_512B,     0.9, 3, 0, 0 ],
  [ "alt_dual_hit_conflict_test_src_delay", alt_dual_hit_conflict_test,  data_512B,     0.9, 3, 10, 0 ],
  [ "alt_dual_hit_conflict_test_sink_delay",alt_dual_hit_conflict_test,  data_512B,     0.9, 3, 0, 10 ],

  [ "alt_LRU_incorrect_eviction_test",           alt_LRU_incorrect_eviction_test,  data_512B,     0.9, 3, 0, 0 ],
  [ "alt_LRU_incorrect_eviction_test_src_delay", alt_LRU_incorrect_eviction_test,  data_512B,     0.9, 3, 10, 0 ],
  [ "alt_LRU_incorrect_eviction_test_sink_delay",alt_LRU_incorrect_eviction_test,  data_512B,     0.9, 3, 0, 10 ],

  [ "alt_dirty_eviction_test",           alt_dirty_eviction_test,  data_512B,     0.9, 3, 0, 0 ],
  [ "alt_dirty_eviction_test_src_delay", alt_dirty_eviction_test,  data_512B,     0.9, 3, 10, 0 ],
  [ "alt_dirty_eviction_test_sink_delay",alt_dirty_eviction_test,  data_512B,     0.9, 3, 0, 10 ],

  [ "write_miss_with_refill_and_eviction_multi_cacheline",     write_miss_with_refill_and_eviction_multi_cacheline,      data_512B,     0.9, 3, 0, 0 ],
  [ "write_miss_with_refill_and_eviction_multi_cacheline_src_delay", write_miss_with_refill_and_eviction_multi_cacheline,  data_512B,     0.9, 3, 10, 0 ],
  [ "write_miss_with_refill_and_eviction_multi_cacheline_sink_delay",write_miss_with_refill_and_eviction_multi_cacheline,  data_512B,     0.9, 3, 0, 10 ],

  [ "stress_entire_cache_alt",stress_entire_cache_alt,  data_512B,     0.9, 3, 0, 00 ],
  [ "stress_entire_cache_alt_src_delay",stress_entire_cache_alt,  data_512B,     0.9, 3, 0, 10 ],
  [ "stress_entire_cache_alt_sink_delay",stress_entire_cache_alt,  data_512B,     0.9, 3, 10, 0 ],
])

@pytest.mark.parametrize( **test_case_table_sassoc )
def test_sassoc( test_params, cmdline_opts ):
  run_test( CacheFL(), test_params, cmdline_opts, cmp_wo_test_field )


#-------------------------------------------------------------------------
# Banked cache test
#-------------------------------------------------------------------------
# This test case is to test if the bank offset is implemented correctly.
# The idea behind this test case is to differentiate between a cache with
# no bank bits and a design has one/two bank bits by looking at cache
# request hit/miss status.

# We first design a test case for 2-way set-associative cache. The last
# request should hit only if students implement the correct index bit to
# be [6:9]. If they implement the index bit to be [4:7] or [5:8], the
# last request is a miss, which is wrong. See below for explanation. This
# test case also works for the baseline direct-mapped cache.

# Direct-mapped
#
#   no bank(should fail):
#      idx
#   00 0000 0000
#   01 0000 0000
#   10 0000 0000
#   00 0000 0000
#   idx: 0, 0, 0 so the third one with tag 10 will evict the first one
#   with tag 00, and thus the fourth read will miss instead of hit.
#
#   4-bank(correct):
#    idx  bk
#   00 00 00 0000
#   01 00 00 0000
#   10 00 00 0000
#   00 00 00 0000
#   idx: 0, 4, 8 so the third one with tag 10 won't evict anything, and
#   thus the fourth read will hit.

# 2-way set-associative
#
#   no bank(should fail):
#        idx
#   00 0 000 0000
#   01 0 000 0000
#   10 0 000 0000
#   00 0 000 0000
#   idx: 0, 0, 0 so the third one with tag 10 will evict the first one
#   with tag 00, and thus the fourth read will miss instead of hit.
#
#   4-bank(correct):
#     idx  bk
#   0 0 00 00 0000
#   0 1 00 00 0000
#   1 0 00 00 0000
#   idx: 0, 4, 0 so the third one with tag 10 won't evict anything, and
#   thus the fourth read will hit.

def bank_test():
  return [
    #    type  opq  addr       len data                type  opq  test len data
    req( 'rd', 0x0, 0x00000000, 0, 0 ), resp( 'rd', 0x0, 0,   0,  0xdeadbeef ),
    req( 'rd', 0x1, 0x00000100, 0, 0 ), resp( 'rd', 0x1, 0,   0,  0x00c0ffee ),
    req( 'rd', 0x2, 0x00000200, 0, 0 ), resp( 'rd', 0x2, 0,   0,  0xffffffff ),
    req( 'rd', 0x3, 0x00000000, 0, 0 ), resp( 'rd', 0x3, 1,   0,  0xdeadbeef ),
  ]

def bank_test_data():
  return [
    # addr      data (in int)
    0x00000000, 0xdeadbeef,
    0x00000100, 0x00c0ffee,
    0x00000200, 0xffffffff,
  ]




test_case_table_bank = mk_test_case_table([
  (             "msg_func   mem_data_func   stall lat src sink"),
  [ "bank_test", bank_test, bank_test_data, 0.0,  0,  0,  0    ],
  [ "bank_test", bank_test, bank_test_data, 0.0,  0,  10,  0    ],
  [ "bank_test", bank_test, bank_test_data, 0.0,  0,  0,  10    ],
])


@pytest.mark.parametrize( **test_case_table_bank )
def test_bank( test_params, cmdline_opts ):
  run_test( CacheFL(), test_params, cmdline_opts, cmp_wo_test_field )