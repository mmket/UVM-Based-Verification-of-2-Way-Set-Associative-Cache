// Analysis transactions for monitors -> scoreboard
`ifndef CACHE_EVT_SVH
`define CACHE_EVT_SVH

class cache_evt_cpu_req extends uvm_sequence_item;
  logic [3:0]  type_;
  logic [7:0]  opaque;
  logic [31:0] addr;
  logic [1:0]  len;
  logic [31:0] data;
  `uvm_object_utils_begin(cache_evt_cpu_req)
    `uvm_field_int(type_,  UVM_ALL_ON)
    `uvm_field_int(opaque, UVM_ALL_ON)
    `uvm_field_int(addr,   UVM_ALL_ON)
    `uvm_field_int(len,    UVM_ALL_ON)
    `uvm_field_int(data,   UVM_ALL_ON)
  `uvm_object_utils_end
  function new(string name="cache_evt_cpu_req");
    super.new(name);
  endfunction
endclass

class cache_evt_cpu_rsp extends uvm_sequence_item;
  logic [3:0]  type_;
  logic [7:0]  opaque;
  logic [1:0]  test;
  logic [1:0]  len;
  logic [31:0] data;
  `uvm_object_utils_begin(cache_evt_cpu_rsp)
    `uvm_field_int(type_,  UVM_ALL_ON)
    `uvm_field_int(opaque, UVM_ALL_ON)
    `uvm_field_int(test,   UVM_ALL_ON)
    `uvm_field_int(len,    UVM_ALL_ON)
    `uvm_field_int(data,   UVM_ALL_ON)
  `uvm_object_utils_end
  function new(string name="cache_evt_cpu_rsp");
    super.new(name);
  endfunction
endclass

class cache_evt_mem_req extends uvm_sequence_item;
  logic [3:0]   type_;
  logic [7:0]   opaque;
  logic [31:0]  addr;
  logic [3:0]   len;
  logic [127:0] data;
  `uvm_object_utils_begin(cache_evt_mem_req)
    `uvm_field_int(type_,  UVM_ALL_ON)
    `uvm_field_int(opaque, UVM_ALL_ON)
    `uvm_field_int(addr,   UVM_ALL_ON)
    `uvm_field_int(len,    UVM_ALL_ON)
    `uvm_field_int(data,   UVM_ALL_ON)
  `uvm_object_utils_end
  function new(string name="cache_evt_mem_req");
    super.new(name);
  endfunction
endclass

class cache_evt_mem_rsp extends uvm_sequence_item;
  logic [3:0]   type_;
  logic [7:0]   opaque;
  logic [1:0]   test;
  logic [3:0]   len;
  logic [127:0] data;
  `uvm_object_utils_begin(cache_evt_mem_rsp)
    `uvm_field_int(type_,  UVM_ALL_ON)
    `uvm_field_int(opaque, UVM_ALL_ON)
    `uvm_field_int(test,   UVM_ALL_ON)
    `uvm_field_int(len,    UVM_ALL_ON)
    `uvm_field_int(data,   UVM_ALL_ON)
  `uvm_object_utils_end
  function new(string name="cache_evt_mem_rsp");
    super.new(name);
  endfunction
endclass

`endif
