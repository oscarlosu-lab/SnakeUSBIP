import Foundation

public final class URBHandler {
    public init() {}

    public func handleSubmit(cmd: USBIPPackets.CmdSubmit) -> Data {
        USBIPPackets.encodeRetSubmit(
            seqnum: cmd.seqnum,
            devid: cmd.devid,
            direction: cmd.direction,
            ep: cmd.ep,
            status: -95,
            actualLength: 0
        )
    }
}
