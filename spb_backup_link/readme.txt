Script connect to border, checking ping from backup ISP link to back ISP gateway.
If ping ok, connection closed.
If ping bad, it will send commands:
conf t
interface fa0/1
shutdown
no shutdown
end
exit
