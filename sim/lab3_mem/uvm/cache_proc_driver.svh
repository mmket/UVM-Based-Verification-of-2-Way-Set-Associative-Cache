`ifndef CACHE_PROC_DRIVER_SVH
`define CACHE_PROC_DRIVER_SVH

class cache_proc_driver extends uvm_driver #(cache_proc_req_item);
  `uvm_component_utils(cache_proc_driver)
  virtual cache_proc_if vif;

  function new(string name, uvm_component parent);
    super.new(name, parent);
  endfunction

  function void build_phase(uvm_phase phase);
    super.build_phase(phase);
    if (!uvm_config_db#(virtual cache_proc_if)::get(this, "", "vif", vif))
      `uvm_fatal("NOVIF", "cache_proc_if not set for driver")
  endfunction

  task run_phase(uvm_phase phase);
    cache_proc_req_item tr;
    forever begin
      seq_item_port.get_next_item(tr);
      drive_req(tr);
      seq_item_port.item_done();
    end
  endtask

  task drive_req(cache_proc_req_item tr);
    logic [77:0] bits;
    bits = pack_mem_req_4B(tr.type_, tr.opaque, tr.addr, tr.len, tr.data);
    @(posedge vif.clk);
    if (vif.reset) begin
      vif.req_val <= 1'b0;
      return;
    end
    vif.req_msg <= bits;
    vif.req_val <= 1'b1;
    do begin
      @(posedge vif.clk);
      if (vif.reset) begin
        vif.req_val <= 1'b0;
        return;
      end
    end while (!(vif.req_val && vif.req_rdy));
    vif.req_val <= 1'b0;
  endtask
endclass

`endif
