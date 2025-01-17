# master_node.py
import tkinter as tk
from tkinter import ttk
from can_message import CANMessage


class MasterNode:
    def __init__(self, message_callback):
        self.window = tk.Toplevel()
        self.window.title("Master Node Controller")
        self.window.geometry("700x700")
        self.device_id = 0x7FF  # Master uses highest priority ID
        self.message_callback = message_callback
        self.broadcast_callback = None
        self.pending_requests = set()  # Track IDs we've requested data from
        self.setup_ui()

    def setup_ui(self):
        frame = ttk.Frame(self.window, padding="20")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Remote frame request controls
        ttk.Label(frame, text="Request Data From Node:", font=('Arial', 12, 'bold')).grid(
            row=0, column=0, columnspan=2, pady=10)

        # Node selection
        self.node_id = tk.StringVar(value="0x123")
        ttk.Label(frame, text="Node ID (hex):", font=('Arial', 12)).grid(row=1, column=0, padx=5, pady=5)
        node_ids = ["0x123", "0x124", "0x125"]  # IDs of kerosene, temperature, pressure sensors
        self.node_select = ttk.Combobox(frame, textvariable=self.node_id, values=node_ids)
        self.node_select.grid(row=1, column=1, padx=5, pady=5)

        # Request button
        self.request_button = ttk.Button(frame, text="Request Data", command=self.send_remote_frame)
        self.request_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Message displays
        ttk.Label(frame, text="Sent Remote Frames:", font=('Arial', 12, 'bold')).grid(
            row=3, column=0, columnspan=2, pady=(20, 5))
        self.sent_display = tk.Text(frame, height=12, width=70, font=('Courier', 10))
        self.sent_display.grid(row=4, column=0, columnspan=2, pady=5)

        ttk.Label(frame, text="Received Data:", font=('Arial', 12, 'bold')).grid(
            row=5, column=0, columnspan=2, pady=(20, 5))
        self.received_display = tk.Text(frame, height=12, width=70, font=('Courier', 10))
        self.received_display.grid(row=6, column=0, columnspan=2, pady=5)

    def send_remote_frame(self):
        target_id = int(self.node_id.get(), 16)
        # Add to pending requests when we send a remote frame
        self.pending_requests.add(target_id)

        message = CANMessage(target_id, [], is_remote=True)

        frame_parts = message.get_frame_parts()
        sent_info = f"\nSent Remote Frame to ID: 0x{target_id:03X}\n"
        sent_info += "-" * 50

        self.sent_display.insert(tk.END, sent_info)
        self.sent_display.see(tk.END)

        if self.broadcast_callback:
            self.broadcast_callback(self.device_id, message)

    def receive_message(self, message):
        frame_parts = message.get_frame_parts()
        source_id = int(frame_parts['Identifier'], 2)

        # Only process data frames (not remote frames)
        if frame_parts['RTR'] == '0':
            hex_data = ' '.join(["{:02X}".format(int(message.data[i:i + 8], 2))
                                 for i in range(0, len(message.data), 8)])

            if source_id in self.pending_requests:
                # This is a response to our request
                received_info = f"\nREQUESTED Data from ID: 0x{source_id:03X}\n"
                received_info += f"Data: {hex_data}\n"
                received_info += "Response to Remote Frame Request\n"
                self.pending_requests.remove(source_id)  # Remove from pending
            else:
                # This is a regular broadcast
                received_info = f"\nBROADCAST Data from ID: 0x{source_id:03X}\n"
                received_info += f"Data: {hex_data}\n"
                received_info += "Regular Sensor Broadcast\n"

            received_info += "-" * 50
            self.received_display.insert(tk.END, received_info)
            self.received_display.see(tk.END)

    def set_broadcast_callback(self, callback):
        self.broadcast_callback = callback