# Wireshark TCP Dissector Sample
# Lua-based dissector for TCP handshake analysis

-- Create protocol dissector
tcp_proto = Proto("tcp_sovereign", "Sovereign TCP Protocol")

-- Define fields
local f_syn = ProtoField.bool("tcp_sovereign.syn", "SYN Flag")
local f_ack = ProtoField.bool("tcp_sovereign.ack", "ACK Flag")
local f_seq = ProtoField.uint32("tcp_sovereign.seq", "Sequence Number")

tcp_proto.fields = {f_syn, f_ack, f_seq}

-- Dissector function
function tcp_proto.dissector(buffer, pinfo, tree)
    pinfo.cols.protocol = "TCP-SOVEREIGN"
    
    local subtree = tree:add(tcp_proto, buffer())
    
    -- Parse TCP flags
    local flags = buffer(13, 1):uint()
    local syn = bit.band(flags, 0x02) ~= 0
    local ack = bit.band(flags, 0x10) ~= 0
    
    subtree:add(f_syn, syn)
    subtree:add(f_ack, ack)
    
    -- Parse sequence number
    local seq = buffer(4, 4):uint()
    subtree:add(f_seq, seq)
    
    -- Sovereign mapping: Convert to wave frequency
    local wave_freq = 20000 -- 20kHz for TCP
    subtree:add_proto_expert_info("Sovereign Frequency: " .. wave_freq .. " Hz")
end

-- Register dissector
DissectorTable.get("ip.proto"):add(6, tcp_proto)
