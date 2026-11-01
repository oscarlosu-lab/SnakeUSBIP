// swift-tools-version: 5.9
// The swift-tools-version declares the minimum version of Swift required to build this package.

import PackageDescription

let package = Package(
    name: "SnakeUSBIPServerMac",
    platforms: [
        .macOS(.v13)
    ],
    products: [
        .executable(
            name: "snakeusbip-server-mac",
            targets: ["SnakeUSBIPServerMac"]
        )
    ],
    dependencies: [],
    targets: [
        .executableTarget(
            name: "SnakeUSBIPServerMac",
            dependencies: [],
            path: "Sources",
            linkerSettings: [
                .linkedFramework("IOKit"),
                .linkedFramework("CoreFoundation"),
                .linkedFramework("Network"),
                .linkedFramework("AppKit"),
                .linkedFramework("SwiftUI")
            ]
        ),
        .testTarget(
            name: "SnakeUSBIPServerMacTests",
            dependencies: ["SnakeUSBIPServerMac"],
            path: "Tests"
        )
    ]
)
