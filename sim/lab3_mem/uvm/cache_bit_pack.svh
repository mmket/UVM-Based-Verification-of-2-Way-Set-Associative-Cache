// Bit layouts match vc/mem-msgs.v packed structs (first field = MSB).
`ifndef CACHE_BIT_PACK_SVH
`define CACHE_BIT_PACK_SVH

function automatic logic [77:0] pack_mem_req_4B(
  input logic [3:0]  type_,
  input logic [7:0]  opaque,
  input logic [31:0] addr,
  input logic [1:0]  len,
  input logic [31:0] data
);
  pack_mem_req_4B = {type_, opaque, addr, len, data};
endfunction

function automatic void unpack_mem_req_4B(
  input  logic [77:0] b,
  output logic [3:0]  type_,
  output logic [7:0]  opaque,
  output logic [31:0] addr,
  output logic [1:0]  len,
  output logic [31:0] data
);
  type_  = b[77:74];
  opaque = b[73:66];
  addr   = b[65:34];
  len    = b[33:32];
  data   = b[31:0];
endfunction

function automatic logic [47:0] pack_mem_resp_4B(
  input logic [3:0]  type_,
  input logic [7:0]  opaque,
  input logic [1:0]  test,
  input logic [1:0]  len,
  input logic [31:0] data
);
  pack_mem_resp_4B = {type_, opaque, test, len, data};
endfunction

function automatic void unpack_mem_resp_4B(
  input  logic [47:0] b,
  output logic [3:0]  type_,
  output logic [7:0]  opaque,
  output logic [1:0]  test,
  output logic [1:0]  len,
  output logic [31:0] data
);
  type_  = b[47:44];
  opaque = b[43:36];
  test   = b[35:34];
  len    = b[33:32];
  data   = b[31:0];
endfunction

function automatic logic [175:0] pack_mem_req_16B(
  input logic [3:0]   type_,
  input logic [7:0]   opaque,
  input logic [31:0]  addr,
  input logic [3:0]   len,
  input logic [127:0] data
);
  pack_mem_req_16B = {type_, opaque, addr, len, data};
endfunction

function automatic void unpack_mem_req_16B(
  input  logic [175:0] b,
  output logic [3:0]   type_,
  output logic [7:0]   opaque,
  output logic [31:0]  addr,
  output logic [3:0]   len,
  output logic [127:0] data
);
  type_  = b[175:172];
  opaque = b[171:164];
  addr   = b[163:132];
  len    = b[131:128];
  data   = b[127:0];
endfunction

function automatic logic [145:0] pack_mem_resp_16B(
  input logic [3:0]   type_,
  input logic [7:0]   opaque,
  input logic [1:0]   test,
  input logic [3:0]   len,
  input logic [127:0] data
);
  pack_mem_resp_16B = {type_, opaque, test, len, data};
endfunction

function automatic void unpack_mem_resp_16B(
  input  logic [145:0] b,
  output logic [3:0]   type_,
  output logic [7:0]   opaque,
  output logic [1:0]   test,
  output logic [3:0]   len,
  output logic [127:0] data
);
  type_  = b[145:142];
  opaque = b[141:134];
  test   = b[133:132];
  len    = b[131:128];
  data   = b[127:0];
endfunction

`endif
