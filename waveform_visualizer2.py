import tkinter as tk
from tkinter import ttk
import math


class WaveformVisualizer:
    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title("CAN Bus Waveform")
        self.window.geometry("800x400")

        self.canvas = tk.Canvas(self.window, bg='white', height=300)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Bind to configure event to handle resizing
        self.canvas.bind("<Configure>", self.on_resize)

        # Frame for bit information
        info_frame = ttk.Frame(self.window)
        info_frame.pack(fill=tk.X, padx=10, pady=5)
        self.bit_info = tk.Label(info_frame, text="Hover over waveform to see bit information")
        self.bit_info.pack()

        self.bits = []
        self.bit_boundaries = []
        self.field_boundaries = []
        self.field_labels = []
        self.message = None  # Placeholder for the message to redraw on resize

    def draw_waveform(self, message):
        self.message = message  # Store message for redraws
        self.canvas.delete("all")
        self.bits = list(message.get_complete_frame())
        self.bit_boundaries = []
        self.field_boundaries = []

        # Drawing parameters
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        bit_width = width / len(self.bits)
        y_center = height / 2
        amplitude = height / 4

        # Draw grid
        for i in range(len(self.bits) + 1):
            x = i * bit_width
            self.canvas.create_line(x, 0, x, height, fill='#eee')
            self.bit_boundaries.append(x)

        # Draw waveform
        x = 0
        prev_level = 1  # Start at recessive level

        frame_parts = message.get_frame_parts()
        current_pos = 0

        # Draw each field with different colors
        colors = {
            'SOF': '#FF9999',
            'Identifier': '#99FF99',
            'RTR': '#9999FF',
            'IDE': '#FFFF99',
            'r0': '#FF99FF',
            'DLC': '#99FFFF',
            'Data': '#FFB366',
            'CRC': '#B366FF',
            'CRC_delimiter': '#66FFB3',
            'ACK': '#FF66B3',
            'ACK_delimiter': '#66B3FF',
            'EOF': '#B3FF66',
            'IFS': '#FFB366'
        }

        for field, bits in frame_parts.items():
            field_start = current_pos * bit_width
            field_length = len(bits)
            field_end = (current_pos + field_length) * bit_width

            # Draw field background
            self.canvas.create_rectangle(
                field_start, 0,
                field_end, height,
                fill=colors[field],
                stipple='gray50',
                width=0
            )

            # Draw field label
            label_x = (field_start + field_end) / 2
            label_y = height - 40
            self.canvas.create_text(label_x, label_y, text=field, angle=90)

            # Draw bits for this field
            for bit in bits:
                current_level = int(bit)
                if current_level != prev_level:
                    self.canvas.create_line(x, y_center - amplitude * prev_level,
                                            x, y_center - amplitude * current_level)
                self.canvas.create_line(x, y_center - amplitude * current_level,
                                        x + bit_width, y_center - amplitude * current_level)
                x += bit_width
                prev_level = current_level

            current_pos += field_length

        # Bind mouse motion for bit information display
        self.canvas.bind('<Motion>', self.show_bit_info)

    def show_bit_info(self, event):
        x = event.x
        for i in range(len(self.bit_boundaries) - 1):
            if self.bit_boundaries[i] <= x < self.bit_boundaries[i + 1]:
                bit_value = self.bits[i]
                self.bit_info.config(text=f"Bit {i}: {bit_value}")
                break

    def on_resize(self, event):
        if self.message:
            self.draw_waveform(self.message)

# Example usage:
# visualizer = WaveformVisualizer()
# visualizer.draw_waveform(your_message_object)
