# SPDX-License-Identifier: MIT
# Copyright (c) 2025 connyTheOne

import sys
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QLineEdit, 
    QSpinBox, QHBoxLayout, QFileDialog, QCheckBox, QMessageBox, QComboBox, QListWidget, 
    QRadioButton, QSplitter
    )
from PySide6.QtGui import QPixmap, QPainter, QColor, QFont, QFontMetrics, QImage, QIcon
from PySide6.QtCore import Qt

VERSION = "0.0.0.1"
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".gif"}
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ICON_PATH = os.path.join(BASE_DIR, "dualImgView.ico")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowIcon(QIcon(ICON_PATH))
        self.setWindowTitle(f"Dual-Image Viewer v{VERSION}")

        self.setGeometry(100, 100, 1000, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Root-Layout + Splitter
        self.layout = QHBoxLayout(self.central_widget)
        self.splitter = QSplitter(Qt.Horizontal)
        self.layout.addWidget(self.splitter)

        # Linke Seite: beide ImagePanels in eigenem Container
        left_container = QWidget()
        left_hbox = QHBoxLayout(left_container)

        self.image_panels = [ImagePanel(self), ImagePanel(self)]
        for panel in self.image_panels:
            left_hbox.addWidget(panel)

        self.splitter.addWidget(left_container)

        # Rechte Seite: Save-Panel mit Optionen
        self.save_layout = QVBoxLayout()

        # Schriftgröße (gemeinsam für Previews & Speichern)
        size_row = QHBoxLayout()
        size_row.addWidget(QLabel("Schriftgröße:"))
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(6, 72)
        self.font_size_spin.setValue(16)
        
        size_row.addWidget(self.font_size_spin)
        size_row.addStretch(1)
        self.save_layout.addLayout(size_row)

        self.labels_img1 = self.create_labels("Labels Bild 1 (oben rechts):", prefix="L", count=3)
        self.labels_img2 = self.create_labels("Labels Bild 2 (oben rechts):", prefix="R", count=3)

        self.radiobtn_horizontal = QRadioButton("Horizontal")
        self.radiobtn_vertical = QRadioButton("Vertical")
        self.radiobtn_horizontal.setChecked(True)
        self.save_layout.addWidget(self.radiobtn_horizontal)
        self.save_layout.addWidget(self.radiobtn_vertical)

        self.save_combined_button = QPushButton("Save Combined")
        self.save_combined_button.clicked.connect(self.save_combined_images)
        self.save_layout.addWidget(self.save_combined_button)

        self.embed_checkbox = QCheckBox("Embed Filenames")
        self.save_layout.addWidget(self.embed_checkbox)

        # nach oben drücken
        self.save_layout.addStretch(1)

        self.save_panel = QWidget()
        self.save_panel.setLayout(self.save_layout)
        self.splitter.addWidget(self.save_panel)

        # Splitter-Startgrößen/Verhalten
        self.save_panel.setMinimumWidth(240)
        self.splitter.setStretchFactor(0, 1)  # left grows
        self.splitter.setStretchFactor(1, 0)  # right fixed
        self.splitter.setCollapsible(0, False)
        self.splitter.setCollapsible(1, True)
        self.splitter.setSizes([self.width() - 320, 320])

        # Live-Update der Previews bei Änderungen
        self.embed_checkbox.toggled.connect(self.update_previews)
        for cb, edit in self.labels_img1 + self.labels_img2:
            cb.toggled.connect(self.update_previews)
            edit.textChanged.connect(self.update_previews)
        self.radiobtn_horizontal.toggled.connect(self.update_previews)
        self.radiobtn_vertical.toggled.connect(self.update_previews)
        self.font_size_spin.valueChanged.connect(self.update_previews)

    def create_labels(self, title: str, prefix: str, count: int):
        """
        Fügt im save_layout eine Überschrift und count Zeilen (Checkbox + LineEdit) hinzu.
        Rückgabe: Liste [(QCheckBox, QLineEdit), ...]
        """
        lbls = []
        self.save_layout.addWidget(QLabel(title))
        for i in range(1, count + 1):
            row = QHBoxLayout()
            cb = QCheckBox(f"{prefix}{i}")
            edit = QLineEdit()
            edit.setPlaceholderText(f"Text {i}")
            row.addWidget(cb)
            row.addWidget(edit)
            self.save_layout.addLayout(row)
            lbls.append((cb, edit))
        return lbls
    
    def get_overlay_for_preview(self, panel) -> tuple[bool, list[str]]:
        show_filename = self.embed_checkbox.isChecked()
        # Panel-Index ermitteln (0 links, 1 rechts)
        idx = 0 if panel is self.image_panels[0] else 1
        pairs = self.labels_img1 if idx == 0 else self.labels_img2
        texts = [e.text().strip() for cb, e in pairs if cb.isChecked() and e.text().strip()]
        return show_filename, texts
    
    def update_previews(self):
        for p in self.image_panels:
            p.display_image()
    
    def draw_bottom_left(self, painter, fm, base, text):
        if not text:
            return
        bx, by, bw, bh = base
        margin, pad = 6, 6
        tw, th = fm.horizontalAdvance(text), fm.height()
        bg_w, bg_h = tw + 2 * pad, th + 2 * pad
        bg_x = bx + margin
        bg_y = by + bh - margin - bg_h
        painter.fillRect(bg_x, bg_y, bg_w, bg_h, QColor(0, 0, 0, 160))
        painter.setPen(QColor(255, 255, 255))
        painter.drawText(bg_x + pad, bg_y + pad + fm.ascent(), text)

    def draw_top_right_stack(self, painter, fm, base, texts):
        bx, by, bw, bh = base
        margin, pad, gap = 6, 6, 2
        y = by + margin
        for t in texts:
            if not t:
                continue
            tw, th = fm.horizontalAdvance(t), fm.height()
            bg_w, bg_h = tw + 2 * pad, th + 2 * pad
            bg_x = bx + bw - margin - bg_w
            bg_y = y
            painter.fillRect(bg_x, bg_y, bg_w, bg_h, QColor(0, 0, 0, 160))
            painter.setPen(QColor(255, 255, 255))
            painter.drawText(bg_x + pad, bg_y + pad + fm.ascent(), t)
            y += bg_h + gap

    def save_combined_images(self):
        # Pfade der aktuell sichtbaren Bilder holen
        p1 = self.image_panels[0].get_current_image_path()
        p2 = self.image_panels[1].get_current_image_path()
        if not p1 or not p2:
            QMessageBox.information(self, "Info", "Beide Seiten müssen ein aktuelles Bild anzeigen.")
            return

        img1 = QImage(p1)
        img2 = QImage(p2)
        if img1.isNull() or img2.isNull():
            QMessageBox.warning(self, "Fehler", "Ein Bild konnte nicht geladen werden.")
            return
        
        if self.radiobtn_horizontal.isChecked():
            target_h = min(img1.height(), img2.height())
            s1 = img1.scaledToHeight(target_h, Qt.SmoothTransformation)
            s2 = img2.scaledToHeight(target_h, Qt.SmoothTransformation)
            out_w, out_h = s1.width() + s2.width(), target_h
            out_img = QImage(out_w, out_h, QImage.Format_ARGB32)
            out_img.fill(Qt.white)
            painter = QPainter(out_img)
            painter.drawImage(0, 0, s1)
            painter.drawImage(s1.width(), 0, s2)
            base1 = (0, 0, s1.width(), s1.height())
            base2 = (s1.width(), 0, s2.width(), s2.height())
        else:
            target_w = min(img1.width(), img2.width())
            s1 = img1.scaledToWidth(target_w, Qt.SmoothTransformation)
            s2 = img2.scaledToWidth(target_w, Qt.SmoothTransformation)
            out_w, out_h = target_w, s1.height() + s2.height()
            out_img = QImage(out_w, out_h, QImage.Format_ARGB32)
            out_img.fill(Qt.white)
            painter = QPainter(out_img)
            painter.drawImage(0, 0, s1)
            painter.drawImage(0, s1.height(), s2)
            base1 = (0, 0, s1.width(), s1.height())
            base2 = (0, s1.height(), s2.width(), s2.height())

        # Helper zum Zeichnen
        painter.setRenderHint(QPainter.Antialiasing, True)
        font = QFont()
        font.setPointSize(self.font_size_spin.value())
        painter.setFont(font)
        fm = QFontMetrics(font)

        # Optional: Dateinamen einbrennen (unten links je Teilbild)
        if self.embed_checkbox.isChecked():
            self.draw_bottom_left(painter, fm, base1, os.path.basename(self.image_panels[0].get_current_image_path() or ""))
            self.draw_bottom_left(painter, fm, base2, os.path.basename(self.image_panels[1].get_current_image_path() or ""))

        # Neue: Benutzer-Labels oben rechts pro Teilbild
        texts1 = [e.text().strip() for cb, e in self.labels_img1 if cb.isChecked() and e.text().strip()]
        texts2 = [e.text().strip() for cb, e in self.labels_img2 if cb.isChecked() and e.text().strip()]
        if texts1:
            self.draw_top_right_stack(painter, fm, base1, texts1)
        if texts2:
            self.draw_top_right_stack(painter, fm, base2, texts2)

        painter.end()

        # Sicherer Default-Dateiname (ohne Extension)
        base_name = os.path.splitext(self.image_panels[0].get_current_filename() or "combined")[0]
        save_path, _ = QFileDialog.getSaveFileName(self, "Save combined image", base_name, "JPEG (*.jpg *.jpeg)")
        if not save_path:
            return
        if not save_path.lower().endswith((".jpg", ".jpeg")):
            save_path += ".jpg"
        if not out_img.save(save_path, "JPEG", 100):
            QMessageBox.warning(self, "Fehler", "Speichern fehlgeschlagen.")

class ImagePanel(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)

        self.load_button = QPushButton("Load Images")
        self.load_button.clicked.connect(self.load_images)
        self.layout.addWidget(self.load_button)

        self.image_label = QLabel("No Image Loaded")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.image_label)

        self.filename_label = QLabel("")
        self.layout.addWidget(self.filename_label)

        self.nav_layout = QHBoxLayout()
        self.prev_button = QPushButton("Previous")
        self.prev_button.clicked.connect(self.show_previous_image)
        self.nav_layout.addWidget(self.prev_button)
        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.show_next_image)
        self.nav_layout.addWidget(self.next_button)
        self.layout.addLayout(self.nav_layout)

        # Sortier-ComboBox
        sort_row = QHBoxLayout()
        sort_row.addWidget(QLabel("Sortieren nach:"))
        self.sort_combo = QComboBox()
        self.sort_combo.addItems([
            "Name (A–Z)",
            "Name (Z–A)",
            "Geändert (neu→alt)",
            "Geändert (alt→neu)",
            "Erstellt (neu→alt)",
            "Erstellt (alt→neu)",
        ])
        self.sort_combo.currentIndexChanged.connect(self.on_sort_changed)
        sort_row.addWidget(self.sort_combo)
        sort_row.addStretch(1)
        self.layout.addLayout(sort_row)

        self.list_widget = QListWidget()
        self.list_widget.setAlternatingRowColors(True)
        self.list_widget.setSelectionMode(QListWidget.SingleSelection)
        self.list_widget.currentRowChanged.connect(self.on_list_row_changed)
        self.list_widget.setMaximumHeight(400)  # bei Bedarf anpassen
        self.layout.addWidget(self.list_widget)

        self.images = []
        self.current_index = -1

    def load_images(self):
        folder = QFileDialog.getExistingDirectory(self, "Ordner mit Bildern wählen")
        if not folder:
            return
        files = [os.path.join(folder, f)
            for f in sorted(os.listdir(folder))
            if os.path.splitext(f)[1].lower() in IMAGE_EXTENSIONS]
        if not files:
            QMessageBox.information(self, "Hinweis", "Im gewählten Ordner wurden keine Bilder gefunden.")
            return
        self.images = files
        self.sort_images(keep_selection=False)
    
    def on_sort_changed(self, _idx: int):
        # Live neu sortieren, aktuelle Auswahl beibehalten
        self.sort_images(keep_selection=True)

    def display_image(self):
        if self.images:
            base_path = self.images[self.current_index]
            pixmap = QPixmap(base_path).scaled(700, 450, Qt.KeepAspectRatio, Qt.SmoothTransformation)

            # Overlays vom MainWindow holen und auf die Vorschau malen
            owner = self.window()  # statt self.parent()
            if hasattr(owner, "get_overlay_for_preview"):
                show_filename, top_right_texts = owner.get_overlay_for_preview(self)

                pm = pixmap.copy()
                painter = QPainter(pm)
                painter.setRenderHint(QPainter.Antialiasing, True)

                font = QFont()
                font.setPointSize(owner.font_size_spin.value())
                painter.setFont(font)
                fm = QFontMetrics(font)
                margin, pad, gap = 6, 6, 2
                w, h = pm.width(), pm.height()

                # unten links: Dateiname
                if show_filename:
                    text = os.path.basename(base_path)
                    tw, th = fm.horizontalAdvance(text), fm.height()
                    bg_w, bg_h = tw + 2 * pad, th + 2 * pad
                    bg_x = margin
                    bg_y = h - margin - bg_h
                    painter.fillRect(bg_x, bg_y, bg_w, bg_h, QColor(0, 0, 0, 160))
                    painter.setPen(QColor(255, 255, 255))
                    painter.drawText(bg_x + pad, bg_y + pad + fm.ascent(), text)

                # oben rechts: gestapelte Labels
                y = margin
                for t in top_right_texts:
                    tw, th = fm.horizontalAdvance(t), fm.height()
                    bg_w, bg_h = tw + 2 * pad, th + 2 * pad
                    bg_x = w - margin - bg_w
                    bg_y = y
                    painter.fillRect(bg_x, bg_y, bg_w, bg_h, QColor(0, 0, 0, 160))
                    painter.setPen(QColor(255, 255, 255))
                    painter.drawText(bg_x + pad, bg_y + pad + fm.ascent(), t)
                    y += bg_h + gap

                painter.end()
                self.image_label.setPixmap(pm)
            else:
                self.image_label.setPixmap(pixmap)

            self.filename_label.setText(os.path.basename(base_path))
            # Liste auf aktuellen Index setzen (Signale blocken)
            self.list_widget.blockSignals(True)
            self.list_widget.setCurrentRow(self.current_index)
            self.list_widget.scrollToItem(self.list_widget.item(self.current_index))
            self.list_widget.blockSignals(False)
        else:
            self.image_label.setText("No Image Loaded")
            self.filename_label.setText("")
            self.list_widget.clear()

    def show_previous_image(self):
        if self.images and self.current_index > 0:
            self.current_index -= 1
            self.display_image()

    def show_next_image(self):
        if self.images and self.current_index < len(self.images) - 1:
            self.current_index += 1
            self.display_image()
    
    def get_current_image_path(self):
        if self.images and 0 <= self.current_index < len(self.images):
            return self.images[self.current_index]
        return None
    
    def get_current_filename(self):
        path = self.get_current_image_path()
        return os.path.basename(path) if path else None
    
    def refresh_list(self):
        self.list_widget.blockSignals(True)
        self.list_widget.clear()
        for p in self.images:
            self.list_widget.addItem(os.path.basename(p))
        if 0 <= self.current_index < len(self.images):
            self.list_widget.setCurrentRow(self.current_index)
            self.list_widget.scrollToItem(self.list_widget.item(self.current_index))
        self.list_widget.blockSignals(False)

    def on_list_row_changed(self, row: int):
        if 0 <= row < len(self.images) and row != self.current_index:
            self.current_index = row
            self.display_image()
    
    def sort_images(self, keep_selection: bool):
        if not self.images:
            self.refresh_list()
            self.display_image()
            return

        prev_path = self.get_current_image_path() if keep_selection else None

        mode = self.sort_combo.currentText()
        reverse = False

        def safe_mtime(p):
            try:
                return os.path.getmtime(p)
            except Exception:
                return 0.0

        def safe_ctime(p):
            try:
                return os.path.getctime(p)
            except Exception:
                return 0.0

        if mode.startswith("Name"):
            keyfunc = lambda p: os.path.basename(p).lower()
            reverse = "Z–A" in mode
        elif mode.startswith("Geändert"):
            keyfunc = safe_mtime
            reverse = "neu→alt" in mode  # neu->alt = absteigend
        elif mode.startswith("Erstellt"):
            keyfunc = safe_ctime
            reverse = "neu→alt" in mode
        else:
            keyfunc = lambda p: os.path.basename(p).lower()

        self.images.sort(key=keyfunc, reverse=reverse)

        if prev_path in self.images:
            self.current_index = self.images.index(prev_path)
        else:
            self.current_index = 0

        self.refresh_list()
        self.display_image()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())