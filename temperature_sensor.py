from base_sensor import BaseSensor
import tkinter as tk
from tkinter import ttk
class TemperatureSensor(BaseSensor):
    def __init__(self, message_callback):
        super().__init__("Engine Temperature Sensor", 0x124, message_callback, default_value=1500)
        self.broadcast_callback = None  # Add this line

    def set_broadcast_callback(self, callback):
        self.broadcast_callback = callback

    def setup_controls(self, frame):
        ttk.Label(frame, text="Temperature:", font=('Arial', 12)).grid(row=0, column=0, padx=5, pady=5)
        self.value_label = ttk.Label(frame, textvariable=self.value, font=('Arial', 12))
        self.value_label.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(frame, text="°C", font=('Arial', 12)).grid(row=0, column=2, padx=5, pady=5)

        self.slider = ttk.Scale(frame, from_=0, to=2500, orient=tk.HORIZONTAL,
                              variable=self.value, length=400)
        self.slider.grid(row=1, column=0, columnspan=3, pady=10)

        self.send_button = ttk.Button(frame, text="Send", command=self.send_data)
        self.send_button.grid(row=2, column=0, columnspan=3, pady=10)