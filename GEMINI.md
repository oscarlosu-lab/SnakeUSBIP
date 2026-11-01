# SnakeUSBIP Workspace Delta (Local Project Memory)
- **Monorepo**: Windows Client WPF, Server (.NET 9, macOS Swift, Linux), Android app (`com.snakeusbip`).
- **Versión Oficial**: Ecosistema estandarizado en versión `1.0.0` (`v1.0.0`).
- **Build Protegida**: ReadyToRun Single-File (`PublishReadyToRun=true`, `PublishSingleFile=true`, sin PDBs).
- **Incompatibilidad WinForms**: No usar `PublishAot` ni `PublishTrimmed` por `NETSDK1175` en bandeja del sistema.
- **Inno Setup**: `ISCC.exe` requiere `SourceDir` y `OutputDir` en rutas absolutas normalizadas.
- **Release CI Multiplataforma**: `release.yml` matriz Windows, macOS Swift, Linux tarball y Android APK con Sigstore.
- **Integridad**: Hashes SHA-256 en `SHA256SUMS.txt` y atestación Sigstore ($0).
- **Financiación**: `.github/FUNDING.yml` con `ko_fi: oscarlosu`.
