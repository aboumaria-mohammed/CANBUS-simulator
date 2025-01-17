import tkinter as tk
from tkinter import ttk
from can_message import CANMessage


class BaseSensor:
    def __init__(self, title, device_id, message_callback, default_value=50):
        self.window = tk.Toplevel()
        self.window.title(title)
        self.window.geometry("350x350")  # Halved both dimensions
        self.device_id = device_id
        self.message_callback = message_callback
        self.broadcast_callback = None

        self.value = tk.IntVar(value=default_value)

        self.setup_ui()

    def setup_ui(self):
        frame = ttk.Frame(self.window, padding="10")  # Reduced padding
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Original controls
        self.setup_controls(frame)

        # Packet display
        self.setup_packet_display(frame)

        # Received messages display
        self.setup_received_messages(frame)

    def setup_packet_display(self, frame):
        ttk.Label(frame, text="CAN Frame Fields:", font=('Arial', 10, 'bold')).grid(  # Reduced font size
            row=3, column=0, columnspan=3, pady=(10, 2))  # Reduced padding
        self.packet_display = tk.Text(frame, height=6, width=35, font=('Courier', 9))  # Reduced height, width, and font
        self.packet_display.grid(row=4, column=0, columnspan=3, pady=2)

    def setup_received_messages(self, frame):
        ttk.Label(frame, text="Received Messages:", font=('Arial', 10, 'bold')).grid(  # Reduced font size
            row=5, column=0, columnspan=3, pady=(10, 2))  # Reduced padding
        self.received_display = tk.Text(frame, height=6, width=35, font=('Courier', 9))  # Reduced height, width, and font
        self.received_display.grid(row=6, column=0, columnspan=3, pady=2)

    def set_broadcast_callback(self, callback):
        self.broadcast_callback = callback

    def receive_message(self, message):
        frame_parts = message.get_frame_parts()
        source_id = int(frame_parts['Identifier'], 2)

        if frame_parts['RTR'] == '1':  # Remote frame
            # Only respond if we are the target device
            if source_id == self.device_id:
                self.send_data()
            return

        # Regular message display code for data frames...
        received_info = f"\nReceived from ID: 0x{source_id:03X}\n"
        hex_data = ' '.join(["{:02X}".format(int(message.data[i:i + 8], 2))
                             for i in range(0, len(message.data), 8)])
        received_info += f"Data: {hex_data}\n"
        received_info += "-" * 50

        self.received_display.insert(tk.END, received_info)
        self.received_display.see(tk.END)

    def send_data(self):
        value = self.value.get()
        data = [
            (value >> 56) & 0xFF,
            (value >> 48) & 0xFF,
            (value >> 40) & 0xFF,
            (value >> 32) & 0xFF,
            (value >> 24) & 0xFF,
            (value >> 16) & 0xFF,
            (value >> 8) & 0xFF,
            value & 0xFF,
        ]

        message = CANMessage(self.device_id, data)
        self.update_packet_display(message)
        self.message_callback(message)

        if self.broadcast_callback:
            self.broadcast_callback(self.device_id, message)

    def update_packet_display(self, message):
        frame_parts = message.get_frame_parts()
        packet_info = self.format_packet_info(frame_parts, message)
        self.packet_display.delete(1.0, tk.END)
        self.packet_display.insert(tk.END, packet_info)

    def format_packet_info(self, frame_parts, message):
        return "\n".join([
            f"SOF:     {frame_parts['SOF']}",
            f"ID:      0x{self.device_id:03X}",
            f"RTR:     0x{frame_parts['RTR']}",
            f"IDE:     0x{frame_parts['IDE']}",
            f"r0:      0x{frame_parts['r0']}",
            f"DLC:     0x{hex(int(frame_parts['DLC'], 2))[2:]}",
            f"Data:    {' '.join(['{:02X}'.format(int(message.data[i:i + 8], 2)) for i in range(0, len(message.data), 8)])}",
            f"CRC:     0x{int(frame_parts['CRC'], 2):04X}",
            f"CRC_del: {frame_parts['CRC_delimiter']}",
            f"ACK:     {frame_parts['ACK']}",
            f"ACK_del: {frame_parts['ACK_delimiter']}",
            f"EOF:     0b{frame_parts['EOF']}",
            f"IFS:     0b{frame_parts['IFS']}"
        ])

