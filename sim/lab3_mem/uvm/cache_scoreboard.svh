`ifndef CACHE_SCOREBOARD_SVH
`define CACHE_SCOREBOARD_SVH

// Samples proc + mem interfaces in a fixed order each clock to avoid analysis ordering issues.
class cache_scoreboard extends uvm_component;
  `uvm_component_utils(cache_scoreboard)

  virtual cache_proc_if proc_vif;
  virtual cache_mem_if  mem_vif;

  cache_evt_cpu_req cpu_pend[$];
  logic [31:0]      mem_rd_addr_pend[$];

  logic [31:0] shadow [logic [31:0]];

  longint unsigned n_checks;
  longint unsigned n_errs;

  function new(string name, uvm_component parent);
    super.new(name, parent);
  endfunction

  function void build_phase(uvm_phase phase);
    super.build_phase(phase);
    if (!uvm_config_db#(virtual cache_proc_if)::get(this, "", "proc_vif", proc_vif))
      `uvm_fatal("NOVIF", "proc_vif not set for scoreboard")
    if (!uvm_config_db#(virtual cache_mem_if)::get(this, "", "mem_vif", mem_vif))
      `uvm_fatal("NOVIF", "mem_vif not set for scoreboard")
  endfunction

  function logic [31:0] get_word(logic [31:0] byte_addr);
    if (!shadow.exists(byte_addr))
      return 32'h0;
    return shadow[byte_addr];
  endfunction

  function void set_word(logic [31:0] byte_addr, logic [31:0] d);
    shadow[byte_addr] = d;
  endfunction

  function void set_line_from_128(logic [31:0] any_byte_addr, logic [127:0] d);
    logic [31:0] base;
    base = {any_byte_addr[31:4], 4'h0};
    set_word(base + 0, d[31:0]);
    set_word(base + 4, d[63:32]);
    set_word(base + 8, d[95:64]);
    set_word(base + 12, d[127:96]);
  endfunction

  task run_phase(uvm_phase phase);
    forever @(posedge proc_vif.clk) begin
      if (proc_vif.reset) begin
        cpu_pend.delete();
        mem_rd_addr_pend.delete();
        continue;
      end

      begin
        logic [3:0]   mqt;
        logic [7:0]   mop;
        logic [31:0]  mad;
        logic [3:0]   mlen;
        logic [127:0] mdat;
        logic [3:0]   mst;
        logic [7:0]   mrop;
        logic [1:0]   mtst;
        logic [3:0]   mrlen;
        logic [127:0] mrdat;

        if (mem_vif.req_val && mem_vif.req_rdy) begin
          unpack_mem_req_16B(mem_vif.req_msg, mqt, mop, mad, mlen, mdat);
          if (mqt == VC_MEM_REQ_MSG_TYPE_READ) begin
            mem_rd_addr_pend.push_back(mad);
          end
          else if (mqt == VC_MEM_REQ_MSG_TYPE_WRITE) begin
            set_line_from_128(mad, mdat);
          end
        end

        if (mem_vif.resp_val && mem_vif.resp_rdy) begin
          unpack_mem_resp_16B(mem_vif.resp_msg, mst, mrop, mtst, mrlen, mrdat);
          if (mst == VC_MEM_RESP_MSG_TYPE_READ) begin
            logic [31:0] a;
            if (mem_rd_addr_pend.size() == 0)
              `uvm_error("SB", "mem read response with empty pending addr queue")
            else begin
              a = mem_rd_addr_pend.pop_front();
              set_line_from_128(a, mrdat);
            end
          end
        end
      end

      begin
        logic [3:0]  pqt;
        logic [7:0]  pqo;
        logic [31:0] pqa, pqd;
        logic [1:0]  pql;
        if (proc_vif.req_val && proc_vif.req_rdy) begin
          cache_evt_cpu_req e;
          unpack_mem_req_4B(proc_vif.req_msg, pqt, pqo, pqa, pql, pqd);
          e = cache_evt_cpu_req::type_id::create("e");
          e.type_  = pqt;
          e.opaque = pqo;
          e.addr   = pqa;
          e.len    = pql;
          e.data   = pqd;
          cpu_pend.push_back(e);
        end

        if (proc_vif.resp_val && proc_vif.resp_rdy) begin
          cache_evt_cpu_req rq;
          if (cpu_pend.size() == 0)
            `uvm_error("SB", "CPU response with empty pending request queue")
          else begin
            rq = cpu_pend.pop_front();
            check_cpu_rsp(rq, proc_vif.resp_msg);
          end
        end
      end
    end
  endtask

  function void check_cpu_rsp(cache_evt_cpu_req rq, logic [47:0] rsp_bits);
    logic [31:0] exp;
    logic [3:0]  rty;
    logic [7:0]  rop;
    logic [1:0]  rtst, rlen;
    logic [31:0] rdat;
    unpack_mem_resp_4B(rsp_bits, rty, rop, rtst, rlen, rdat);

    if (rq.opaque !== rop) begin
      `uvm_error("SB", $sformatf("opaque mismatch req=%0h rsp=%0h", rq.opaque, rop))
      n_errs++;
    end
    case (rq.type_)
      VC_MEM_REQ_MSG_TYPE_READ: begin
        exp = get_word(rq.addr);
        n_checks++;
        if (rdat !== exp) begin
          `uvm_error("SB", $sformatf("READ data mismatch addr=%h exp=%h got=%h", rq.addr, exp, rdat))
          n_errs++;
        end
      end
      VC_MEM_REQ_MSG_TYPE_WRITE: begin
        set_word(rq.addr, rq.data);
      end
      VC_MEM_REQ_MSG_TYPE_WRITE_INIT: begin
        logic [31:0] b;
        b = {rq.addr[31:4], 4'h0};
        set_word(b + 0, rq.data);
        set_word(b + 4, rq.data);
        set_word(b + 8, rq.data);
        set_word(b + 12, rq.data);
      end
      default: begin
        `uvm_error("SB", $sformatf("Unexpected CPU req type %0h", rq.type_))
        n_errs++;
      end
    endcase
  endfunction

  function void report_phase(uvm_phase phase);
    super.report_phase(phase);
    `uvm_info("SB", $sformatf("Scoreboard: read checks=%0d errors=%0d", n_checks, n_errs), UVM_LOW)
  endfunction
endclass

`endif
