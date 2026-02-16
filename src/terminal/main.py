import random
import time
from src.common.crypto import CryptoUtils

class TerminalAgent:
    def __init__(self, terminal_id: str):
        self.terminal_id = terminal_id
        self.key = CryptoUtils.generate_aes_key()

    def generate_telemetry(self):
        """Generates mock IoT data."""
        temp = round(random.uniform(20.0, 35.0), 2)
        return f"Device: {self.terminal_id} | Temp: {temp}C | Timestamp: {time.time()}"

    def send_data(self):
        data = self.generate_telemetry()
        encrypted = CryptoUtils.encrypt_aes(data, self.key)
        print(f"[Terminal {self.terminal_id}] Generated: {data}")
        print(f"[Terminal {self.terminal_id}] Encrypted: {encrypted[:20]}...")
        return {"id": self.terminal_id, "payload": encrypted.decode(), "key": self.key.decode()}

if __name__ == "__main__":
    t = TerminalAgent("T-001")
    t.send_data()
