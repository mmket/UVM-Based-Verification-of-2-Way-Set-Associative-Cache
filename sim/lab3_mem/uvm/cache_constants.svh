// Match vc/mem-msgs.v memory request/response type constants
`ifndef CACHE_CONSTANTS_SVH
`define CACHE_CONSTANTS_SVH

parameter logic [3:0] VC_MEM_REQ_MSG_TYPE_READ       = 4'h0;
parameter logic [3:0] VC_MEM_REQ_MSG_TYPE_WRITE      = 4'h1;
parameter logic [3:0] VC_MEM_REQ_MSG_TYPE_WRITE_INIT = 4'h2;

parameter logic [3:0] VC_MEM_RESP_MSG_TYPE_READ       = 4'h0;
parameter logic [3:0] VC_MEM_RESP_MSG_TYPE_WRITE      = 4'h1;
parameter logic [3:0] VC_MEM_RESP_MSG_TYPE_WRITE_INIT = 4'h2;

`endif
