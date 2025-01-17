import tkinter as tk
from kerosene_sensor import KeroseneSensor
from temperature_sensor import TemperatureSensor
from pressure_sensor import  Pressuresensor
from master_node import MasterNode
from waveform_visualizer2 import WaveformVisualizer


class CANBusSimulator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("CAN Bus Control")
        self.root.withdraw()  # Hide the main window

        self.waveform_visualizer = WaveformVisualizer()
        self.devices = []  # List to store all connected devices

        # Create sensor devices with callbacks
        self.kerosene = KeroseneSensor(self.on_message)
        self.temperature = TemperatureSensor(self.on_message)
        self.pressure = Pressuresensor(self.on_message)
        # Add devices to the list
        self.devices.extend([self.kerosene, self.temperature, self.pressure])
        self.master = MasterNode(self.on_message)
        self.devices.append(self.master)
        # Set broadcast callback for each device
        for device in self.devices:
            device.set_broadcast_callback(self.broadcast_message)

    def on_message(self, message):
        # Update waveform display when a message is sent
        self.waveform_visualizer.draw_waveform(message)

    def broadcast_message(self, sender_id, message):
        # Broadcast message to all devices except the sender
        for device in self.devices:
            if device.device_id != sender_id:
                device.receive_message(message)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    simulator = CANBusSimulator()
    simulator.run()