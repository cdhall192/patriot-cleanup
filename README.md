# patriot-cleanup
Reduce DCHP request spam on Patriot servers



Takes CSV of DHCP logs limited to peers spamming the server, and CSV of authenticated users.

Pulls MAC addresses from DHCP logs.

Pulls MAC/IP pairs from authenticated users.

Compares MACs from DHCP logs +/- 1 to MACs from authenticated users.

Stores IPs from matched MACs in list.

Outputs IP addresses to text file in same folder as authenticated users CSV.
