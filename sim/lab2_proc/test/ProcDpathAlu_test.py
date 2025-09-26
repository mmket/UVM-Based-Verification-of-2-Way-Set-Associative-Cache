#=========================================================================
# ProcDpathAlu unit tests
#=========================================================================

from pymtl3 import *
from pymtl3.stdlib.test_utils import run_test_vector_sim

from lab2_proc.ProcDpathAlu import ProcDpathAlu

#-------------------------------------------------------------------------
# add
#-------------------------------------------------------------------------

def test_alu_add( cmdline_opts ):
  dut = ProcDpathAlu()

  run_test_vector_sim( dut, [
    ('in0           in1           fn  out*          ops_eq*   ops_lt*  ops_ltu*'),
    [ 0x00000000,   0x00000000,   0,  0x00000000,   '?',      '?',       '?'      ],
    [ 0x0ffaa660,   0x00012304,   0,  0x0ffbc964,   '?',      '?',       '?'      ],
    # pos-neg
    [ 0x00132050,   0xd6620040,   0,  0xd6752090,   '?',      '?',       '?'      ],
    [ 0xfff0a440,   0x00004450,   0,  0xfff0e890,   '?',      '?',       '?'      ],
    # neg-neg
    [ 0xfeeeeaa3,   0xf4650000,   0,  0xf353eaa3,   '?',      '?',       '?'      ],
  ], cmdline_opts )

#-------------------------------------------------------------------------
# addi
#-------------------------------------------------------------------------

def test_alu_addi( cmdline_opts ):
  dut = ProcDpathAlu()

  run_test_vector_sim( dut, [
    ('in0           in1           fn  out*          ops_eq*   ops_lt*  ops_ltu*'),
    # imm = 0
    [ 0x00000000,   0x00000000,   0,  0x00000000,   '?',      '?',       '?'      ],
    [ 0x00000005,   0x00000003,   0,  0x00000008,   '?',      '?',       '?'      ],
    # positive imm
    [ 0x7fffffff,   0x00000001,   0,  0x80000000,   '?',      '?',       '?'      ],
    [ 0x0000abcd,   0x00001234,   0,  0x0000be01,   '?',      '?',       '?'      ],
    # negative imm (sign-extended)
    [ 0x00001000,   0xfffff000,   0,  0x00000000,   '?',      '?',       '?'      ],
    [ 0xffffffff,   0xffffffff,   0,  0xfffffffe,   '?',      '?',       '?'      ],
  ], cmdline_opts )

#-------------------------------------------------------------------------
# and
#-------------------------------------------------------------------------
def test_alu_and( cmdline_opts ):
  dut = ProcDpathAlu()
  run_test_vector_sim( dut, [
    ('in0           in1           fn  out*          ops_eq*   ops_lt*  ops_ltu*'),
    [ 0b1010,       0b1100,       3,  0b1000,       '?',      '?',     '?' ],
    [ 0xffffffff,   0x12345678,   3,  0x12345678,   '?',      '?',     '?' ],
  ], cmdline_opts )


#-------------------------------------------------------------------------
# cp_op0
#-------------------------------------------------------------------------

def test_alu_cp_op0( cmdline_opts ):
  dut = ProcDpathAlu()

  run_test_vector_sim( dut, [
    ('in0           in1           fn  out*          ops_eq*   ops_lt*  ops_ltu*'),
    [ 0x00000000,   0x00000000,  11,  0x00000000,   '?',      '?',       '?'      ],
    [ 0x0ffaa660,   0x00012304,  11,  0x0ffaa660,   '?',      '?',       '?'      ],
    [ 0x00132050,   0xd6620040,  11,  0x00132050,   '?',      '?',       '?'      ],
    [ 0xfff0a440,   0x00004450,  11,  0xfff0a440,   '?',      '?',       '?'      ],
    [ 0xfeeeeaa3,   0xf4650000,  11,  0xfeeeeaa3,   '?',      '?',       '?'      ],
  ], cmdline_opts )



#-------------------------------------------------------------------------
# or
#-------------------------------------------------------------------------
def test_alu_or( cmdline_opts ):
  dut = ProcDpathAlu()
  run_test_vector_sim( dut, [
    ('in0           in1           fn  out*          ops_eq*   ops_lt*  ops_ltu*'),
    [ 0b1010,       0b1100,       4,  0b1110,       '?',      '?',     '?' ],  # fn=4 → OR
    [ 0xffffffff,   0x12345678,   4,  0xffffffff,   '?',      '?',     '?' ],
  ], cmdline_opts )

#-------------------------------------------------------------------------
# xor
#-------------------------------------------------------------------------
def test_alu_xor( cmdline_opts ):
  dut = ProcDpathAlu()
  run_test_vector_sim( dut, [
    ('in0           in1           fn  out*          ops_eq*   ops_lt*  ops_ltu*'),
    [ 0b1010,       0b1100,       5,  0b0110,       '?',      '?',     '?' ],  # fn=5 → XOR
    [ 0xffffffff,   0x0f0f0f0f,   5,  0xf0f0f0f0,   '?',      '?',     '?' ],
  ], cmdline_opts )

#-------------------------------------------------------------------------
# sub
#-------------------------------------------------------------------------
def test_alu_sub( cmdline_opts ):
  dut = ProcDpathAlu()
  run_test_vector_sim( dut, [
    ('in0           in1           fn  out*          ops_eq*   ops_lt*  ops_ltu*'),
    [ 10,           5,            1,  5,            '?',      '?',     '?' ],  # fn=1 → SUB
    [ 0,            1,            1,  0xffffffff,   '?',      '?',     '?' ],
  ], cmdline_opts )

#-------------------------------------------------------------------------
# slt (signed)
#-------------------------------------------------------------------------
def test_alu_slt( cmdline_opts ):
  dut = ProcDpathAlu()
  run_test_vector_sim( dut, [
    ('in0           in1           fn  out* ops_eq* ops_lt* ops_ltu*'),
    [  1,           2,            6,  1,   '?',    '?',    '?' ],  # fn=6 → SLT
    [ -1 & 0xffffffff, 1, 6,  1,   '?',    '?',    '?' ],
    [  2,           1,            6,  0,   '?',    '?',    '?' ],
  ], cmdline_opts )

#-------------------------------------------------------------------------
# sll (shift left logical)
#-------------------------------------------------------------------------
def test_alu_sll( cmdline_opts ):
  dut = ProcDpathAlu()
  run_test_vector_sim( dut, [
    ('in0   in1 fn out* ops_eq* ops_lt* ops_ltu*'),
    [ 1,    1,  9,  2,   '?',    '?',    '?' ],   # fn=9 → SLL
    [ 1,    4,  9,  16,  '?',    '?',    '?' ],
  ], cmdline_opts )

#-------------------------------------------------------------------------
# srl (shift right logical)
#-------------------------------------------------------------------------
def test_alu_srl( cmdline_opts ):
  dut = ProcDpathAlu()
  run_test_vector_sim( dut, [
    ('in0   in1 fn out* ops_eq* ops_lt* ops_ltu*'),
    [ 16,   2,  8,  4,   '?',    '?',    '?' ],   # fn=8 → SRL
    [ 1,    1,  8,  0,   '?',    '?',    '?' ],
  ], cmdline_opts )

#-------------------------------------------------------------------------
# sra (shift right arithmetic)
#-------------------------------------------------------------------------
def test_alu_sra( cmdline_opts ):
  dut = ProcDpathAlu()
  run_test_vector_sim( dut, [
    ('in0           in1 fn out*         ops_eq* ops_lt* ops_ltu*'),
    [ 0xfffffff0,   4,  7, 0xffffffff,  '?',    '?',    '?' ],   # fn=7 → SRA
    [ 0x80000000,   1,  7, 0xc0000000,  '?',    '?',    '?' ],
  ], cmdline_opts )


#-------------------------------------------------------------------------
# cp_op1
#-------------------------------------------------------------------------

def test_alu_cp_op1( cmdline_opts ):
  dut = ProcDpathAlu()

  run_test_vector_sim( dut, [
    ('in0           in1           fn  out*          ops_eq*   ops_lt*  ops_ltu*'),
    [ 0x00000000,   0x00000000,  12,  0x00000000,   '?',      '?',       '?'      ],
    [ 0x0ffaa660,   0x00012304,  12,  0x00012304,   '?',      '?',       '?'      ],
    [ 0x00132050,   0xd6620040,  12,  0xd6620040,   '?',      '?',       '?'      ],
    [ 0xfff0a440,   0x00004450,  12,  0x00004450,   '?',      '?',       '?'      ],
    [ 0xfeeeeaa3,   0xf4650000,  12,  0xf4650000,   '?',      '?',       '?'      ],
  ], cmdline_opts )

#-------------------------------------------------------------------------
# cp_equality
#-------------------------------------------------------------------------

def test_alu_fn_equality( cmdline_opts ):
  dut = ProcDpathAlu()

  run_test_vector_sim( dut, [
    ('in0           in1           fn  out*          ops_eq*   ops_lt*  ops_ltu*'),
    [ 0x00000000,   0x00000000,  14,  0x00000000,   1,        '?',       '?'      ],
    [ 0x0ffaa660,   0x00012304,  14,  0x00000000,   0,        '?',       '?'      ],
    [ 0x00132050,   0xd6620040,  14,  0x00000000,   0,        '?',       '?'      ],
    [ 0xfff0a440,   0x00004450,  14,  0x00000000,   0,        '?',       '?'      ],
    [ 0xfeeeeaa3,   0xf4650000,  14,  0x00000000,   0,        '?',       '?'      ],
  ], cmdline_opts )
