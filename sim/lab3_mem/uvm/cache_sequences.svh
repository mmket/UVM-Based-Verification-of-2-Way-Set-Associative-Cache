`ifndef CACHE_SEQUENCES_SVH
`define CACHE_SEQUENCES_SVH

class cache_sanity_seq extends uvm_sequence #(cache_proc_req_item);
  `uvm_object_utils(cache_sanity_seq)

  function new(string name="cache_sanity_seq");
    super.new(name);
  endfunction

  task body();
    cache_proc_req_item tr;

    // Wait out reset + a few cycles
    #200ns;

    // WRITE_INIT line at 0x100 (16B line); data replicated in RTL
    tr = cache_proc_req_item::type_id::create("tr_wi");
    tr.type_  = VC_MEM_REQ_MSG_TYPE_WRITE_INIT;
    tr.opaque = 8'h01;
    tr.addr   = 32'h0000_0100;
    tr.len    = 2'b0;
    tr.data   = 32'hdeadbeef;
    start_item(tr);
    finish_item(tr);
    #500ns;

    // Read word 0
    tr = cache_proc_req_item::type_id::create("tr_r0");
    tr.type_  = VC_MEM_REQ_MSG_TYPE_READ;
    tr.opaque = 8'h02;
    tr.addr   = 32'h0000_0100;
    tr.len    = 2'b0;
    tr.data   = 32'h0;
    start_item(tr);
    finish_item(tr);
    #500ns;

    // Read word 1 (same cache line)
    tr = cache_proc_req_item::type_id::create("tr_r1");
    tr.type_  = VC_MEM_REQ_MSG_TYPE_READ;
    tr.opaque = 8'h03;
    tr.addr   = 32'h0000_0104;
    tr.len    = 2'b0;
    tr.data   = 32'h0;
    start_item(tr);
    finish_item(tr);
    #500ns;

    // Write word 2 then read it back
    tr = cache_proc_req_item::type_id::create("tr_w");
    tr.type_  = VC_MEM_REQ_MSG_TYPE_WRITE;
    tr.opaque = 8'h04;
    tr.addr   = 32'h0000_0108;
    tr.len    = 2'b0;
    tr.data   = 32'h12345678;
    start_item(tr);
    finish_item(tr);
    #500ns;

    tr = cache_proc_req_item::type_id::create("tr_r2");
    tr.type_  = VC_MEM_REQ_MSG_TYPE_READ;
    tr.opaque = 8'h05;
    tr.addr   = 32'h0000_0108;
    tr.len    = 2'b0;
    tr.data   = 32'h0;
    start_item(tr);
    finish_item(tr);
  endtask
endclass

class cache_random_seq extends uvm_sequence #(cache_proc_req_item);
  `uvm_object_utils(cache_random_seq)

  rand int unsigned n_iter;
  constraint c_iter { n_iter inside {[8:32]}; }

  function new(string name="cache_random_seq");
    super.new(name);
  endfunction

  task body();
    cache_proc_req_item tr;
    if (!this.randomize()) `uvm_fatal("SEQ", "randomize failed")
    #200ns;

    repeat (n_iter) begin
      tr = cache_proc_req_item::type_id::create("tr");
      if (!tr.randomize() with {
        addr[1:0] == 2'b0;
        len == 2'b0;
        opaque inside {[1:255]};
      }) `uvm_fatal("SEQ", "tr randomize failed")

      if ($urandom_range(0, 4) != 0)
        tr.type_ = VC_MEM_REQ_MSG_TYPE_READ;
      else if ($urandom_range(0, 1))
        tr.type_ = VC_MEM_REQ_MSG_TYPE_WRITE;
      else
        tr.type_ = VC_MEM_REQ_MSG_TYPE_WRITE_INIT;

      if (tr.type_ == VC_MEM_REQ_MSG_TYPE_READ)
        tr.data = 32'h0;
      else
        tr.data = $urandom();

      start_item(tr);
      finish_item(tr);
      # ($urandom_range(20, 120)) * 1ns;
    end
  endtask
endclass

`endif
