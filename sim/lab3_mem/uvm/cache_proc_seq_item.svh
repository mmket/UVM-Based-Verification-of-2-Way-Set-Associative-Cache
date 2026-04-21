`ifndef CACHE_PROC_SEQ_ITEM_SVH
`define CACHE_PROC_SEQ_ITEM_SVH

class cache_proc_req_item extends uvm_sequence_item;
  rand logic [3:0]  type_;
  rand logic [7:0]  opaque;
  rand logic [31:0] addr;
  rand logic [1:0]  len;
  rand logic [31:0] data;

  constraint c_len_default { len == 2'b0; } // full word

  `uvm_object_utils_begin(cache_proc_req_item)
    `uvm_field_int(type_,  UVM_ALL_ON)
    `uvm_field_int(opaque, UVM_ALL_ON)
    `uvm_field_int(addr,   UVM_ALL_ON)
    `uvm_field_int(len,    UVM_ALL_ON)
    `uvm_field_int(data,   UVM_ALL_ON)
  `uvm_object_utils_end

  function new(string name="cache_proc_req_item");
    super.new(name);
  endfunction
endclass

`endif
