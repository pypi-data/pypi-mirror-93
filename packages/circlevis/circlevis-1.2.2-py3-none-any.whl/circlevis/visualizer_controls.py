from PyQt5.QtWidgets import QFrame, QPushButton, QSlider, QGridLayout, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from circlevis.utils import resource_path

class VisualizerControls(QFrame):
    def __init__(self, speed):
        super().__init__()
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setValue(0)
        self.slider.setFixedHeight(20)
        self.slider.setStyleSheet("outline: none;")

        self.play_reverse_button = QPushButton()
        self.play_reverse_button.setIcon(QIcon(resource_path("play_reverse.png")))
        self.play_reverse_button.setFixedSize(20, 20)
        self.play_reverse_button.setToolTip("Plays visualization in reverse")

        self.play_normal_button = QPushButton()
        self.play_normal_button.setIcon(QIcon(resource_path("play_normal.png")))
        self.play_normal_button.setFixedSize(20, 20)
        self.play_normal_button.setToolTip("Plays visualization in normally")

        self.next_frame_button = QPushButton()
        self.next_frame_button.setIcon(QIcon(resource_path("frame_next.png")))
        self.next_frame_button.setFixedSize(20, 20)
        self.next_frame_button.setToolTip("Displays next frame")

        self.previous_frame_button = QPushButton()
        self.previous_frame_button.setIcon(QIcon(resource_path("frame_back.png")))
        self.previous_frame_button.setFixedSize(20, 20)
        self.previous_frame_button.setToolTip("Displays previous frame")

        self.pause_button = QPushButton()
        self.pause_button.setIcon(QIcon(resource_path("pause.png")))
        self.pause_button.setFixedSize(20, 20)
        self.pause_button.setToolTip("Pause visualization")

        self.copy_to_clipboard_button = QPushButton()
        self.copy_to_clipboard_button.setIcon(QIcon(resource_path("clipboard.svg")))
        self.copy_to_clipboard_button.setFixedSize(20, 20)
        self.copy_to_clipboard_button.setToolTip("Copy timestamped url to clipboard")

        self.speed_up_button = QPushButton()
        self.speed_up_button.setIcon(QIcon(resource_path("speed_up.png")))
        self.speed_up_button.setFixedSize(20, 20)
        self.speed_up_button.setToolTip("Speed up")

        self.speed_down_button = QPushButton()
        self.speed_down_button.setIcon(QIcon(resource_path("speed_down.png")))
        self.speed_down_button.setFixedSize(20, 20)
        self.speed_down_button.setToolTip("Speed down")

        self.speed_label = QLabel(f"{speed}x")
        self.speed_label.setFixedSize(40, 20)
        self.speed_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        self.layout = QGridLayout()
        self.layout.addWidget(self.play_reverse_button, 16, 0, 1, 1)
        self.layout.addWidget(self.previous_frame_button, 16, 1, 1, 1)
        self.layout.addWidget(self.pause_button, 16, 2, 1, 1)
        self.layout.addWidget(self.next_frame_button, 16, 3, 1, 1)
        self.layout.addWidget(self.play_normal_button, 16, 4, 1, 1)
        self.layout.addWidget(self.copy_to_clipboard_button, 16, 5, 1, 1)
        self.layout.addWidget(self.slider, 16, 6, 1, 9)
        self.layout.addWidget(self.speed_label, 16, 15, 1, 1)
        self.layout.addWidget(self.speed_down_button, 16, 16, 1, 1)
        self.layout.addWidget(self.speed_up_button, 16, 17, 1, 1)
        self.layout.setContentsMargins(5, 0, 5, 5)
        self.setLayout(self.layout)
        self.setFixedHeight(25)

    def set_paused_state(self, paused):
        if paused:
            self.pause_button.setIcon(QIcon(resource_path("play.png")))
        else:
            self.pause_button.setIcon(QIcon(resource_path("pause.png")))
