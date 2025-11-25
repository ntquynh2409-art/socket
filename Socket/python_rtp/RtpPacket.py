import sys
from time import time
HEADER_SIZE = 12

class RtpPacket:
    header = bytearray(HEADER_SIZE)

    def __init__(self):
        pass

    # THÊM tham số 'marker' vào hàm này
    def encode(self, version, padding, extension, cc, seqnum, marker, pt, ssrc, payload):
        """Encode the RTP packet with header fields and payload."""
        timestamp = int(time())
        self.header = bytearray(HEADER_SIZE)
        
        # --- BẮT ĐẦU CHỈNH SỬA HEADER BIT ---
        # Byte 1: Version (2 bits), Padding (1 bit), Extension (1 bit), CC (4 bits)
        self.header[0] = (version << 6) | (padding << 5) | (extension << 4) | cc
        
        # Byte 2: Marker (1 bit), Payload Type (7 bits)
        # Đây là dòng quan trọng để Client biết đâu là gói cuối cùng của 1 frame
        self.header[1] = (marker << 7) | pt 
        # ------------------------------------
        
        self.header[2] = (seqnum >> 8) & 0xFF
        self.header[3] = seqnum & 0xFF
        
        self.header[4] = (timestamp >> 24) & 0xFF
        self.header[5] = (timestamp >> 16) & 0xFF
        self.header[6] = (timestamp >> 8) & 0xFF
        self.header[7] = timestamp & 0xFF
        
        self.header[8] = (ssrc >> 24) & 0xFF
        self.header[9] = (ssrc >> 16) & 0xFF
        self.header[10] = (ssrc >> 8) & 0xFF
        self.header[11] = ssrc & 0xFF
        
        self.payload = payload

    def decode(self, byteStream):
        """Decode the RTP packet."""
        self.header = bytearray(byteStream[:HEADER_SIZE])
        self.payload = byteStream[HEADER_SIZE:]

    def version(self):
        return int(self.header[0] >> 6)

    def seqNum(self):
        seqNum = self.header[2] << 8 | self.header[3]
        return int(seqNum)

    def timestamp(self):
        timestamp = self.header[4] << 24 | self.header[5] << 16 | self.header[6] << 8 | self.header[7]
        return int(timestamp)

    def payloadType(self):
        pt = self.header[1] & 127
        return int(pt)

    def getPayload(self):
        return self.payload

    def getPacket(self):
        return self.header + self.payload