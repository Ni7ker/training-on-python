import sys
import psutil
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QSpinBox, QHBoxLayout)
from PyQt5.QtCore import QTimer, QTime
from PyQt5.QtCore import QTimer, QTime

class ResourceMonitor(QWidget):
    def __init__(self):
        super().__init__()

        # Основной интерфейс
        self.setWindowTitle("Мониторинг ресурсов")
        self.layout = QVBoxLayout()

        # Фиксированный размер окна
        self.setFixedSize(150, 200)

        self.cpu_label = QLabel("CPU: 0%")
        self.ram_label = QLabel("RAM: 0%")
        self.disk_label = QLabel("Disk: 0%")
        self.layout.addWidget(self.cpu_label)
        self.layout.addWidget(self.ram_label)
        self.layout.addWidget(self.disk_label)

        self.update_interval_label = QLabel("Update Interval (s):")
        self.layout.addWidget(self.update_interval_label)

        self.interval_input = QSpinBox()
        self.interval_input.setRange(1, 60)
        self.interval_input.setValue(1)
        self.layout.addWidget(self.interval_input)

        self.record_button = QPushButton("Начать запись")
        self.record_button.clicked.connect(self.start_recording)
        self.layout.addWidget(self.record_button)

        self.stop_button = QPushButton("Остановить")
        self.stop_button.clicked.connect(self.stop_recording)
        self.stop_button.setVisible(False)
        self.layout.addWidget(self.stop_button)

        self.timer_label = QLabel("Время записи: 00:00:00")
        self.timer_label.setVisible(False)
        self.layout.addWidget(self.timer_label)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_resources)

        self.recording_timer = QTimer()
        self.recording_timer.timeout.connect(self.update_timer)

        self.recording_time = QTime(0, 0, 0)
        self.recording = False

        self.setLayout(self.layout)

        # Подключение к базе данных
        self.db_connection = sqlite3.connect("resources.db")
        self.cursor = self.db_connection.cursor()
        self.create_table()

        self.start_monitoring()

    def create_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS resource_usage (
                timestamp TEXT,
                cpu_usage REAL,
                ram_usage REAL,
                disk_usage REAL
            )
            """
        )
        self.db_connection.commit()

    def start_monitoring(self):
        interval = self.interval_input.value() * 1000
        self.timer.start(interval)

    def update_resources(self):
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent

        self.cpu_label.setText(f"CPU: {cpu}%")
        self.ram_label.setText(f"RAM: {ram}%")
        self.disk_label.setText(f"Disk: {disk}%")

        if self.recording:
            self.save_to_db(cpu, ram, disk)

    def save_to_db(self, cpu, ram, disk):
        self.cursor.execute(
            "INSERT INTO resource_usage (timestamp, cpu_usage, ram_usage, disk_usage) VALUES (datetime('now'), ?, ?, ?)",
            (cpu, ram, disk)
        )
        self.db_connection.commit()

    def start_recording(self):
        self.recording = True
        self.recording_time = QTime(0, 0, 0)
        self.recording_timer.start(1000)

        self.record_button.setVisible(False)
        self.stop_button.setVisible(True)
        self.timer_label.setVisible(True)

    def stop_recording(self):
        self.recording = False
        self.recording_timer.stop()
        self.record_button.setVisible(True)
        self.stop_button.setVisible(False)
        self.timer_label.setVisible(False)

    def update_timer(self):
        self.recording_time = self.recording_time.addSecs(1)
        self.timer_label.setText(f"Время записи: {self.recording_time.toString('hh:mm:ss')}")

    def closeEvent(self, event):
        self.timer.stop()
        self.recording_timer.stop()
        self.db_connection.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ResourceMonitor()
    window.show()
    sys.exit(app.exec_())
