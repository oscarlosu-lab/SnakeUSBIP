# 🛡️ Security Policy — SnakeUSBIP

🌐 **Language / Idioma:** **English** | [Español](SECURITY_ES.md)

> **Migration Notice:** `SnakeUSBIP` is being migrated into [USBAnywhere](https://github.com/oscarlosu-lab/USBAnywhere). For production deployments, [USBAnywhere](https://github.com/oscarlosu-lab/USBAnywhere) is the recommended final product.

## Supported Versions

| Version | Supported          | Status |
| ------- | ------------------ | ------ |
| 1.4.1 | :white_check_mark: | Latest Stable Release |
| 1.3.x | :white_check_mark: | Active Stable |
| < 1.3 | :x:                | Unsupported (Upgrade to SnakeUSBIP v1.4.1 or USBAnywhere) |

---

## Security Architecture & Zero-Trust Hardening

**SnakeUSBIP** is designed with a defense-in-depth, Zero-Trust security model across the entire ecosystem, combining input validation, restricted process invocation, trusted host allowlists, signed driver expectations, and automated CI security scanning.

### 1. Whitelist Command & Argument Sanitization (`InputValidator`)
- All IPv4 addresses, domain names, USB `bus-id` strings, and TCP ports are strictly validated against restrictive regular expression whitelists before any shell or system process invocation.
- External processes (`usbipw.exe`, `devnode.exe`, `pnputil.exe`) are invoked with `UseShellExecute = false`, preventing arbitrary argument injection and shell command chaining.

### 2. Digital Signatures & Authenticode Verification (`SignatureVerifier`)
- All distributed native executables (`usbipw.exe`, `devnode.exe`, `SnakeUSBIP.exe`) are validated for valid Microsoft Authenticode digital signatures.
- Binary digests are compared against verified cryptographic manifests before invoking device attachment or detachment.

### 3. Fail-Closed Cryptographic Auto-Updater (`UpdateService`)
- The integrated update engine strictly communicates over HTTPS and whitelists official GitHub release endpoints (`github.com`, `objects.githubusercontent.com`).
- Update installers are verified against an official `SHA256SUMS.txt` cryptographic manifest before execution. If the SHA-256 hash fails or does not match, the file is deleted immediately and execution is aborted.

### 4. Microsoft WHQL-Certified Drivers
- Uses Microsoft WHQL-signed `usbip2_ude.sys` and `usbip2_filter.sys` drivers, fully compatible with Windows 10 & 11 **Core Isolation / Memory Integrity (HVCI)**.
- Does not require Windows Test Signing Mode on standard x64 systems.

### 5. Multiplatform Server Security Models
- **Windows Server**: The Windows Firewall rule for port 3240 is restricted exclusively to **Private** and **Domain** network profiles, preventing exposure on untrusted Public Wi-Fi networks.
- **macOS Server**: Utilizes native Apple **Userspace IOKit** (`IOKit.framework`). Operates without third-party Kernel Extensions (`.kext`) and retains complete compatibility with Apple Silicon **System Integrity Protection (SIP)**. Privileges are managed securely via system `launchd` LaunchDaemons.
- **Linux Server**: Runs via a dedicated systemd service (`usbipd.service` + `snakeusbip-autounbind.service`) and confines USB export operations via targeted udev rules.

### 6. Control Plane (`TCP 3241`), Pinned TLS 1.3 (`TCP 3243`) & Webhook Hardening (`v1.4.1`)
- **6-Digit / `UA2:` Pairing & SHA-256 Pinned TLS 1.3**: `PairingClientService` and `TlsTunnelBridge` verify server certificate fingerprints in constant time; Linux `PAIR_CREATE` on `TCP 3241` is loopback-only unless `control_token` is set; Android `UsbIpServerService` validates `busId` (`^\d+-[\d.]+$`).
- **Bearer-Authenticated Local REST API (`127.0.0.1:13241`) & WTS Isolation**: Loopback-only HTTP API gated by per-install Bearer token; WTS session isolation prevents inactive sessions from attaching devices.
- **TCP `3241` Allowlist & HMAC Token**: `snakeusbip-ctl` and `ControlServer.swift` support optional `allowed_ips` filtering and constant-time HMAC `control_token` authentication (`policy allow-ip|deny-ip|set-token|clear-token`).
- **Android Sunshine Webhook (`3242`)**: `SunshineHandoffServer` enforces HTTP header bounds and optional `X-USBAnywhere-Token` / `Authorization: Bearer` authentication.

---

## Reporting a Vulnerability

If you discover a security issue or vulnerability, please responsibly report it:
- **GitHub Security Advisory**: Open a private advisory at [SnakeUSBIP Security Advisories](https://github.com/oscarlosu-lab/SnakeUSBIP/security/advisories/new)
- **Email**: Reach out to the maintainers at [oscarlosu-lab](https://github.com/oscarlosu-lab).

We appreciate responsible disclosure and will investigate and address reported vulnerabilities promptly.
