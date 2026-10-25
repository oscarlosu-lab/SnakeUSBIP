using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Net.Sockets;
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;
using SnakeUSBIP.Models;
using SnakeUSBIP.Services.Interfaces;

namespace SnakeUSBIP.Services
{
    /// <summary>
    /// VPN service - Detect Tailscale/ZeroTier and get peers
    /// </summary>
    public class VpnService : IVpnService
    {
        private string _currentConfig = string.Empty;

        public bool IsAvailable => IsTailscaleInstalled() || IsZeroTierInstalled() || IsWireGuardInstalled();
        public bool IsConnected => false; // TODO: Implement real connection status check
        public string CurrentConfig => _currentConfig;

        public bool IsTailscaleInstalled()
        {
            try
            {
                var psi = new ProcessStartInfo
                {
                    FileName = "tailscale",
                    Arguments = "--version",
                    RedirectStandardOutput = true,
                    UseShellExecute = false,
                    CreateNoWindow = true
                };
                using var process = Process.Start(psi);
                return process != null;
            }
            catch
            {
                return false;
            }
        }

        public bool IsZeroTierInstalled()
        {
            try
            {
                var psi = new ProcessStartInfo
                {
                    FileName = "zerotier-cli",
                    Arguments = "status",
                    RedirectStandardOutput = true,
                    UseShellExecute = false,
                    CreateNoWindow = true
                };
                using var process = Process.Start(psi);
                return process != null;
            }
            catch
            {
                return false;
            }
        }

        public bool IsWireGuardInstalled()
        {
            try
            {
                var psi = new ProcessStartInfo
                {
                    FileName = "wg",
                    Arguments = "--version",
                    RedirectStandardOutput = true,
                    UseShellExecute = false,
                    CreateNoWindow = true
                };
                using var process = Process.Start(psi);
                return process != null;
            }
            catch
            {
                return false;
            }
        }

        public async Task<IEnumerable<VpnPeer>> GetTailscalePeersAsync()
        {
            var peers = new List<VpnPeer>();
            try
            {
                var psi = new ProcessStartInfo
                {
                    FileName = "tailscale",
                    Arguments = "status --json",
                    RedirectStandardOutput = true,
                    UseShellExecute = false,
                    CreateNoWindow = true
                };
                
                using var process = Process.Start(psi);
                if (process == null) return peers;
                
                var output = await process.StandardOutput.ReadToEndAsync();
                await process.WaitForExitAsync();
                
                if (process.ExitCode == 0 && !string.IsNullOrEmpty(output))
                {
                    using var doc = JsonDocument.Parse(output);
                    if (doc.RootElement.TryGetProperty("Peer", out var peerElement))
                    {
                        foreach (var peer in peerElement.EnumerateObject())
                        {
                            var peerData = peer.Value;
                            peers.Add(new VpnPeer
                            {
                                Hostname = peerData.GetProperty("HostName").GetString() ?? "Unknown",
                                IpAddress = peerData.GetProperty("TailscaleIPs").EnumerateArray()
                                    .Select(ip => ip.GetString())
                                    .FirstOrDefault() ?? "",
                                IsOnline = peerData.GetProperty("Online").GetBoolean(),
                                LastSeen = DateTime.Now // Tailscale JSON has LastSeen but parsing time is tricky sometimes
                            });
                        }
                    }
                }
            }
            catch (Exception dbgEx) { System.Diagnostics.Debug.WriteLine($"[VpnService] {dbgEx.Message}"); }
            return peers;
        }

        public async Task<IEnumerable<VpnPeer>> GetZeroTierPeersAsync()
        {
            var peers = new List<VpnPeer>();
            if (!IsZeroTierInstalled()) return peers;

            try
            {
                var psi = new ProcessStartInfo
                {
                    FileName = "zerotier-cli",
                    Arguments = "peers -j",
                    RedirectStandardOutput = true,
                    UseShellExecute = false,
                    CreateNoWindow = true
                };

                using var process = Process.Start(psi);
                if (process == null) return peers;

                var output = await process.StandardOutput.ReadToEndAsync();
                await process.WaitForExitAsync();

                if (process.ExitCode == 0 && !string.IsNullOrEmpty(output))
                {
                    using var doc = JsonDocument.Parse(output);
                    foreach (var peer in doc.RootElement.EnumerateArray())
                    {
                        var address = peer.GetProperty("address").GetString();
                        var paths = peer.GetProperty("paths");
                        var ip = string.Empty;
                        
                        // ZT peers have multiple paths, we pick the first IP if available
                        if (paths.ValueKind == JsonValueKind.Array && paths.GetArrayLength() > 0)
                        {
                            var firstPath = paths[0].GetProperty("address").GetString();
                            if (firstPath != null)
                            {
                                ip = firstPath.Split('/')[0];
                            }
                        }

                        peers.Add(new VpnPeer
                        {
                            Hostname = $"ZT-{address}",
                            IpAddress = ip,
                            IsOnline = peer.GetProperty("role").GetString() != "UNKNOWN",
                            LastSeen = DateTime.Now
                        });
                    }
                }
            }
            catch (Exception dbgEx) { System.Diagnostics.Debug.WriteLine($"[VpnService] {dbgEx.Message}"); }
            return peers;
        }

        public async Task<IEnumerable<VpnPeer>> GetWireGuardPeersAsync()
        {
            var peers = new List<VpnPeer>();
            if (!IsWireGuardInstalled()) return peers;

            try
            {
                var psi = new ProcessStartInfo
                {
                    FileName = "wg",
                    Arguments = "show all dump",
                    RedirectStandardOutput = true,
                    UseShellExecute = false,
                    CreateNoWindow = true
                };

                using var process = Process.Start(psi);
                if (process == null) return peers;

                var output = await process.StandardOutput.ReadToEndAsync();
                await process.WaitForExitAsync();

                // wg show all dump format:
                // interface public_key private_key listen_port fwmark
                // peer public_key preshared_key endpoint allowed_ips latest_handshake transfer_rx transfer_tx persistent_keepalive
                if (!string.IsNullOrEmpty(output))
                {
                    var lines = output.Split('\n', StringSplitOptions.RemoveEmptyEntries);
                    foreach (var line in lines)
                    {
                        var parts = line.Split('\t');
                        if (parts.Length >= 4) // It's likely a peer line if it has enough fields
                        {
                            // In 'dump' format, first field is interface name if it's the interface line, 
                            // but 'wg show all dump' repeats fields. 
                            // Simplified for now: detect lines with IP-like endpoints
                            var endpoint = parts.FirstOrDefault(p => p.Contains(":"));
                            if (endpoint != null)
                            {
                                var ip = endpoint.Split(':')[0];
                                peers.Add(new VpnPeer
                                {
                                    Hostname = $"WG-{parts[1].Substring(0, 8)}", // First 8 chars of pubkey
                                    IpAddress = ip,
                                    IsOnline = true, // If it's in the dump, we assume it's configured
                                    LastSeen = DateTime.Now
                                });
                            }
                        }
                    }
                }
            }
            catch (Exception dbgEx) { System.Diagnostics.Debug.WriteLine($"[VpnService] {dbgEx.Message}"); }
            return peers;
        }

        public async Task<IEnumerable<VpnPeer>> GetAllPeersAsync()
        {
            var allPeers = new List<VpnPeer>();
            
            if (IsTailscaleInstalled())
                allPeers.AddRange(await GetTailscalePeersAsync());
                
            if (IsZeroTierInstalled())
                allPeers.AddRange(await GetZeroTierPeersAsync());
                
            if (IsWireGuardInstalled())
                allPeers.AddRange(await GetWireGuardPeersAsync());
                
            return allPeers;
        }

        public Task<bool> ConnectAsync(string configPath, CancellationToken ct = default)
        {
            _currentConfig = configPath;
            return Task.FromResult(true);
        }

        public Task<bool> DisconnectAsync(CancellationToken ct = default)
        {
            _currentConfig = string.Empty;
            return Task.FromResult(true);
        }

        public async Task<bool> TestUSBIPOnPeerAsync(string ip)
        {
            try
            {
                using var tcp = new TcpClient();
                var result = tcp.BeginConnect(ip, 3240, null, null);
                var success = result.AsyncWaitHandle.WaitOne(1000);
                tcp.Close();
                return success;
            }
            catch
            {
                return false;
            }
        }
    }
}
