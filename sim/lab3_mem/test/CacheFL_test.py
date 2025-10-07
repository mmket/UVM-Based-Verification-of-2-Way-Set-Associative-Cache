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

# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# LAB TASK: Add more directed test cases
# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

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

  [ "read_hit_word",                    read_hit_word,              None,         0.0,  0,  0,  0    ],
  [ "read_hit_multi_word",              read_hit_multi_word,        None,         0.0,  0,  0,  0    ],
  [ "read_hit_cacheline",               read_hit_cacheline,         None,         0.0,  0,  0,  0    ],
  [ "read_hit_multi_cacheline",         read_hit_multi_cacheline,   None,         0.0,  0,  0,  0    ],
  [ "read_hit_multi_word_sink_delay",   read_hit_multi_word,        None,         0.0,  0,  0,  10   ],
  [ "read_hit_multi_word_src_delay",    read_hit_multi_word,        None,         0.0,  0,  10, 0    ],

  [ "write_hit_word",                   write_hit_word,             None,         0.0,  0,  0,  0    ],
  [ "write_hit_multi_word",             write_hit_multi_word,       None,         0.0,  0,  0,  0    ],
  [ "write_hit_cacheline",              write_hit_cacheline,        None,         0.0,  0,  0,  0    ],
  [ "write_hit_multi_cacheline",        write_hit_multi_cacheline,  None,         0.0,  0,  0,  0    ],
  [ "write_hit_multi_word_sink_delay",  write_hit_multi_word,       None,         0.0,  0,  0,  10   ],
  [ "write_hit_multi_word_src_delay",   write_hit_multi_word,       None,         0.0,  0,  10, 0    ],

  [ "read_miss_word",                   read_miss_word,             data_64B,     0.0,  0,  0,  0    ],
  [ "read_miss_multi_word",             read_miss_multi_word,       data_64B,     0.0,  0,  0,  0    ],
  [ "read_miss_cacheline",              read_miss_cacheline,        data_64B,     0.0,  0,  0,  0    ],
  [ "read_miss_multi_cacheline",        read_miss_multi_cacheline,  data_512B,    0.0,  0,  0,  0    ],
  [ "read_miss_multi_word_sink_delay",  read_miss_multi_word,       data_64B,     0.9,  3,  0,  10   ],
  [ "read_miss_multi_word_src_delay",   read_miss_multi_word,       data_64B,     0.9,  3,  10, 0    ],

  [ "write_miss_word",                  write_miss_word,            data_64B,     0.0,  0,  0,  0    ],
  [ "write_miss_multi_word",            write_miss_multi_word,      data_64B,     0.0,  0,  0,  0    ],
  [ "write_miss_cacheline",             write_miss_cacheline,       data_64B,     0.0,  0,  0,  0    ],
  [ "write_miss_multi_cacheline",       write_miss_multi_cacheline, data_512B,    0.0,  0,  0,  0    ],
  [ "write_miss_multi_word_sink_delay", write_miss_multi_word,      data_64B,     0.9,  3,  0,  10   ],
  [ "write_miss_multi_word_src_delay",  write_miss_multi_word,      data_64B,     0.9,  3,  10, 0    ],

  [ "evict_word",                       evict_word,                 data_512B,    0.0,  0,  0,  0    ],
  [ "evict_multi_word",                 evict_multi_word,           data_512B,    0.0,  0,  0,  0    ],
  [ "evict_cacheline",                  evict_cacheline,            data_512B,    0.0,  0,  0,  0    ],
  [ "evict_multi_cacheline",            evict_multi_cacheline,      data_512B,    0.0,  0,  0,  0    ],
  [ "evict_multi_word_sink_delay",      evict_multi_word,           data_512B,    0.9,  3,  0,  10   ],
  [ "evict_multi_word_src_delay",       evict_multi_word,           data_512B,    0.9,  3,  10, 0    ],

  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # LAB TASK: Add more entries to test case table
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
])

@pytest.mark.parametrize( **test_case_table_generic )
def test_generic( test_params, cmdline_opts ):
  run_test( CacheFL(), test_params, cmdline_opts, cmp_wo_test_field )

#-------------------------------------------------------------------------
# Test Case with Random Addresses and Data
#-------------------------------------------------------------------------

# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# LAB TASK: Add random test cases
# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

test_case_table_random = mk_test_case_table([
  (                        "msg_func       mem_data_func stall lat src sink"),

  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # LAB TASK: Add more entries to test case table
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
])

@pytest.mark.parametrize( **test_case_table_random )
def test_random( test_params, cmdline_opts ):
  run_test( CacheFL(), test_params, cmdline_opts, cmp_wo_test_field )

#-------------------------------------------------------------------------
# Test Cases for Direct Mapped
#-------------------------------------------------------------------------

# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# LAB TASK: Add directed test cases explicitly for direct mapped cache
# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

test_case_table_dmap = mk_test_case_table([
  (                                   "msg_func                         mem_data_func stall lat src sink"),

  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # LAB TASK: Add more entries to test case table
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
])

@pytest.mark.parametrize( **test_case_table_dmap )
def test_dmap( test_params, cmdline_opts ):
  run_test( CacheFL(), test_params, cmdline_opts, cmp_wo_test_field )

#-------------------------------------------------------------------------
# Test Cases for Set Associative
#-------------------------------------------------------------------------

# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# LAB TASK: Add directed test cases explicitly for set associative cache
# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

test_case_table_sassoc = mk_test_case_table([
  (                       "msg_func            mem_data_func    stall lat src sink"),

  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # LAB TASK: Add more entries to test case table
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
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
])

@pytest.mark.parametrize( **test_case_table_bank )
def test_bank( test_params, cmdline_opts ):
  run_test( CacheFL(), test_params, cmdline_opts, cmp_wo_test_field )
