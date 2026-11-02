// ─────────────────────────────────────────────────────────────────────────────
// SnakeUSBIP Server for macOS - Discovery, Policy & Control API Unit Tests
// Copyright (c) 2025-2026 oscarlosu-lab - https://github.com/oscarlosu-lab/SnakeUSBIP-Server
// Licensed under GPL v3
// ─────────────────────────────────────────────────────────────────────────────

import XCTest
@testable import SnakeUSBIPServerMac

final class DiscoveryTests: XCTestCase {

    override func setUp() {
        super.setUp()
        IOKitDeviceManager.shared.resetState()
    }

    func testDeviceCategoryAndEmoji() {
        let videoDev = USBDeviceInfo(
            busId: "1-1",
            path: "/usb/1-1",
            busNum: 1,
            devNum: 1,
            speed: USBIPConstants.speedHigh,
            idVendor: 0x0BDA,
            idProduct: 0x5100,
            bcdDevice: 0x0100,
            bDeviceClass: 0x0E, // Video class (e.g. Webcam)
            bDeviceSubClass: 0,
            bDeviceProtocol: 0,
            bConfigurationValue: 1,
            bNumConfigurations: 1,
            bNumInterfaces: 1,
            productName: "Realtek USB Camera"
        )

        XCTAssertEqual(videoDev.category, "Video")
        XCTAssertEqual(videoDev.categoryEmoji, "📷")
        XCTAssertEqual(videoDev.speedLabel, "High Speed (480 Mb/s)")
        XCTAssertEqual(videoDev.vidPidString, "0BDA:5100")
        XCTAssertEqual(videoDev.id, "1-1")
        XCTAssertEqual(videoDev.dynamicInventoryLine, "  1-1    : Realtek USB Camera [Video] (0bda:5100)")
    }

    func testCompositeSteamControllerRecognition() {
        let steamPuck = USBDeviceInfo(
            busId: "1-2",
            path: "/usb/1-2",
            busNum: 1,
            devNum: 2,
            speed: USBIPConstants.speedFull,
            idVendor: 0x28DE,
            idProduct: 0x1304,
            bcdDevice: 0x0100,
            bDeviceClass: 0xEF, // Miscellaneous composite class
            bDeviceSubClass: 0x02,
            bDeviceProtocol: 0x01,
            bConfigurationValue: 1,
            bNumConfigurations: 1,
            bNumInterfaces: 2,
            interfaces: [
                USBInterfaceInfo(interfaceClass: 0x03, interfaceSubClass: 0, interfaceProtocol: 0),
                USBInterfaceInfo(interfaceClass: 0x03, interfaceSubClass: 0, interfaceProtocol: 0)
            ]
        )

        XCTAssertTrue(steamPuck.isSteamController)
        XCTAssertTrue(steamPuck.isHid)
        XCTAssertFalse(steamPuck.isHub)
        XCTAssertEqual(steamPuck.category, "HID / Gaming")
        XCTAssertEqual(steamPuck.categoryTag, " [HID/Gamepad]")
        XCTAssertTrue(steamPuck.dynamicInventoryLine.contains("[HID/Gamepad] (28de:1304)"))
    }

    func testSharedStateAndExportPolicy() {
        XCTAssertFalse(USBIPServer.usbTransferBackendAvailable)

        // Test cross-process shared state bind / unbind
        XCTAssertTrue(IOKitDeviceManager.shared.bindDevice(busId: "2-1", dynamic: true))
        XCTAssertTrue(IOKitDeviceManager.shared.isBound(busId: "2-1"))
        XCTAssertTrue(IOKitDeviceManager.shared.isDynamicBound(busId: "2-1"))
        XCTAssertTrue(IOKitDeviceManager.shared.unbindDevice(busId: "2-1"))
        XCTAssertFalse(IOKitDeviceManager.shared.isBound(busId: "2-1"))

        // Export policy remains available independently of USB transfer support.
        IOKitDeviceManager.shared.updatePolicy(denylist: ["3-4", "28de:1304"])
        let denied = IOKitDeviceManager.shared.isDeviceExportAllowed(busId: "3-4")
        XCTAssertFalse(denied.allowed)

        // Binding is explicitly unavailable until a real transfer backend exists.
        IOKitDeviceManager.shared.updatePolicy(denylist: [])
        let bindResp = ControlServer.processCommand("BIND 3-4")
        XCTAssertTrue(bindResp.contains(#""status":"UNSUPPORTED""#) || bindResp.contains(#""status": "UNSUPPORTED""#))
        XCTAssertFalse(IOKitDeviceManager.shared.isBound(busId: "3-4"))

        let statusResp = ControlServer.processCommand("STATUS")
        XCTAssertTrue(statusResp.contains(#""usb_transfer_supported":false"#) || statusResp.contains(#""usb_transfer_supported": false"#))

        let unbindResp = ControlServer.processCommand("UNBIND 3-4")
        XCTAssertTrue(unbindResp.contains(#""status":"ERROR""#) || unbindResp.contains(#""status": "ERROR""#))
        XCTAssertFalse(IOKitDeviceManager.shared.isBound(busId: "3-4"))
    }

    func testAutoBindPersistence() {
        let testVidPid = "9999:AAAA"
        AutoBindManager.shared.clearAll()
        XCTAssertFalse(AutoBindManager.shared.isAutoBound(vidPid: testVidPid))

        let added = AutoBindManager.shared.toggleAutoBind(vidPid: testVidPid)
        XCTAssertTrue(added)
        XCTAssertTrue(AutoBindManager.shared.isAutoBound(vidPid: testVidPid))

        let removed = AutoBindManager.shared.toggleAutoBind(vidPid: testVidPid)
        XCTAssertFalse(removed)
        XCTAssertFalse(AutoBindManager.shared.isAutoBound(vidPid: testVidPid))
    }

    func testDiscoveryResponsePayloadFormat() {
        let hostName = ProcessInfo.processInfo.hostName
        let expectedPrefix = "SNAKEUSBIP_SERVER:"
        let responseString = "\(expectedPrefix)\(hostName)"
        let responseData = responseString.data(using: .utf8)

        XCTAssertNotNil(responseData)
        XCTAssertTrue(responseString.hasPrefix(expectedPrefix))
        XCTAssertGreaterThan(responseData!.count, expectedPrefix.count)
    }
}
