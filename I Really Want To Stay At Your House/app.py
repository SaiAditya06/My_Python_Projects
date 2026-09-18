import sys
import os
import re
from bisect import bisect_right

from PySide6.QtCore import (
    Qt,
    QUrl,
    Signal,
    QRect,
    QPropertyAnimation,
    QParallelAnimationGroup,
    QEasingCurve,
    QAbstractAnimation,
)

from PySide6.QtGui import (
    QPixmap,
    QFont,
    QFontMetrics,
    QPainter,
    QColor,
)

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QHBoxLayout,
    QGraphicsDropShadowEffect,
    QGraphicsOpacityEffect,
    QFrame,
)

from PySide6.QtMultimedia import (
    QMediaPlayer,
    QAudioOutput,
)


# =========================================================
# FILES
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SONG_FILE = os.path.join(BASE_DIR, "assets", "song.mp3")
BACKGROUND_FILE = os.path.join(BASE_DIR, "assets", "background.png")
LYRICS_FILE = os.path.join(BASE_DIR, "assets", "lyrics.lrc")


# =========================================================
# CLICKABLE SLIDER
# =========================================================

class ClickableSlider(QSlider):

    sliderClicked = Signal(int)

    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:

            value = self.minimum() + (
                (self.maximum() - self.minimum())
                * event.position().x()
                / self.width()
            )

            value = int(value)

            self.setValue(value)
            self.sliderClicked.emit(value)

        super().mousePressEvent(event)


# =========================================================
# BACKGROUND OVERLAY
# =========================================================

class OverlayWidget(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setAttribute(
            Qt.WA_TransparentForMouseEvents
        )

        self.setAttribute(
            Qt.WA_TranslucentBackground
        )

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.fillRect(
            self.rect(),
            QColor(0, 0, 0, 18)
        )

        painter.fillRect(
            0,
            int(self.height() * 0.26),
            self.width(),
            int(self.height() * 0.54),
            QColor(0, 0, 0, 22)
        )


# =========================================================
# LYRICS STAGE
# =========================================================

class LyricsStage(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setMinimumHeight(290)

        self.lyrics = []
        self.current_index = -1
        self.animation_group = None


        # =================================================
        # MAIN PANEL
        # =================================================

        self.panel = QFrame(self)

        self.panel.setStyleSheet("""
            QFrame {

                background-color:
                    rgba(5, 15, 20, 115);

                border-top:
                    1px solid rgba(0,234,255,95);

                border-bottom:
                    1px solid rgba(0,234,255,95);

                border-left:
                    none;

                border-right:
                    none;

                border-radius:
                    10px;
            }
        """)


        self.panel_opacity = QGraphicsOpacityEffect(
            self.panel
        )

        self.panel.setGraphicsEffect(
            self.panel_opacity
        )

        self.panel_opacity.setOpacity(
            0.0
        )


        # =================================================
        # LABELS
        # =================================================

        self.previous_label = self.create_previous_label()

        self.current_label = self.create_current_label()

        self.next_label = self.create_next_label()


        # NOTHING visible on startup
        self.panel.hide()

        self.previous_label.hide()

        self.current_label.hide()

        self.next_label.hide()


    # =====================================================
    # CREATE LABELS
    # =====================================================

    def create_previous_label(self):

        label = QLabel("", self)

        label.setAlignment(
            Qt.AlignCenter
        )

        label.setWordWrap(False)

        self.apply_previous_style(
            label
        )

        return label


    def create_current_label(self):

        label = QLabel("", self)

        label.setAlignment(
            Qt.AlignCenter
        )

        # IMPORTANT
        # Don't wrap current lyrics
        label.setWordWrap(False)

        self.apply_current_style(
            label
        )

        return label


    def create_next_label(self):

        label = QLabel("", self)

        label.setAlignment(
            Qt.AlignCenter
        )

        label.setWordWrap(False)

        self.apply_next_style(
            label
        )

        return label


    # =====================================================
    # STYLES
    # =====================================================

    def apply_previous_style(self, label):

        label.setGraphicsEffect(None)

        label.setWordWrap(False)

        font = QFont("Arial")

        font.setPointSize(
            17
        )

        font.setBold(
            True
        )

        label.setFont(
            font
        )

        label.setStyleSheet("""
            QLabel {

                color:
                    rgba(255,255,255,100);

                background:
                    transparent;

                border:
                    none;
            }
        """)


    def apply_next_style(self, label):

        label.setGraphicsEffect(None)

        label.setWordWrap(False)

        font = QFont("Arial")

        font.setPointSize(
            17
        )

        font.setBold(
            True
        )

        label.setFont(
            font
        )

        label.setStyleSheet("""
            QLabel {

                color:
                    rgba(255,255,255,100);

                background:
                    transparent;

                border:
                    none;
            }
        """)


    def apply_current_style(self, label):

        label.setWordWrap(False)

        font = QFont("Arial")

        font.setPointSize(
            28
        )

        font.setBold(
            True
        )

        label.setFont(
            font
        )

        label.setStyleSheet("""
            QLabel {

                color:
                    white;

                background:
                    transparent;

                border:
                    none;
            }
        """)


        glow = QGraphicsDropShadowEffect(
            label
        )

        glow.setBlurRadius(
            28
        )

        glow.setOffset(
            0,
            0
        )

        glow.setColor(
            QColor(
                0,
                235,
                255,
                210
            )
        )

        label.setGraphicsEffect(
            glow
        )


    # =====================================================
    # AUTO FIT TEXT
    # =====================================================

    def fit_current_text(self, label, rect):

        if not label.text():

            return


        # Leave room so glow/text doesn't touch edges
        available_width = (
            rect.width() - 70
        )


        # Start big
        font_size = 28


        while font_size >= 16:

            font = QFont(
                "Arial"
            )

            font.setPointSize(
                font_size
            )

            font.setBold(
                True
            )


            metrics = QFontMetrics(
                font
            )


            text_width = metrics.horizontalAdvance(
                label.text()
            )


            if text_width <= available_width:

                label.setFont(
                    font
                )

                return


            font_size -= 1


        # Absolute minimum
        font = QFont(
            "Arial"
        )

        font.setPointSize(
            16
        )

        font.setBold(
            True
        )

        label.setFont(
            font
        )


    # =====================================================
    # FIT SMALL PREVIOUS/NEXT LYRICS
    # =====================================================

    def fit_secondary_text(self, label, rect):

        if not label.text():

            return


        available_width = (
            rect.width() - 60
        )


        font_size = 17


        while font_size >= 12:

            font = QFont(
                "Arial"
            )

            font.setPointSize(
                font_size
            )

            font.setBold(
                True
            )


            metrics = QFontMetrics(
                font
            )


            width = metrics.horizontalAdvance(
                label.text()
            )


            if width <= available_width:

                label.setFont(
                    font
                )

                return


            font_size -= 1


    # =====================================================
    # POSITIONS
    # =====================================================

    def get_positions(self):

        width = self.width()

        center_y = (
            self.height() // 2
        )


        # Wider than before
        side_margin = max(
            20,
            int(width * 0.025)
        )


        available_width = (
            width
            -
            side_margin * 2
        )


        previous_rect = QRect(
            side_margin,
            center_y - 108,
            available_width,
            42
        )


        panel_rect = QRect(
            side_margin,
            center_y - 50,
            available_width,
            100
        )


        # Almost full panel width
        current_rect = QRect(
            side_margin + 10,
            center_y - 50,
            available_width - 20,
            100
        )


        next_rect = QRect(
            side_margin,
            center_y + 65,
            available_width,
            42
        )


        above_rect = QRect(
            side_margin,
            center_y - 165,
            available_width,
            42
        )


        below_rect = QRect(
            side_margin,
            center_y + 125,
            available_width,
            42
        )


        first_start_rect = QRect(
            side_margin + 10,
            center_y + 100,
            available_width - 20,
            100
        )


        panel_start_rect = QRect(
            side_margin,
            center_y - 3,
            available_width,
            6
        )


        return (
            previous_rect,
            panel_rect,
            current_rect,
            next_rect,
            above_rect,
            below_rect,
            first_start_rect,
            panel_start_rect,
        )


    # =====================================================
    # RESIZE
    # =====================================================

    def resizeEvent(self, event):

        (
            previous_rect,
            panel_rect,
            current_rect,
            next_rect,
            above_rect,
            below_rect,
            first_start_rect,
            panel_start_rect,
        ) = self.get_positions()


        if (
            self.animation_group is None
            or
            self.animation_group.state()
            != QAbstractAnimation.Running
        ):

            if self.panel.isVisible():

                self.panel.setGeometry(
                    panel_rect
                )


            if self.previous_label.isVisible():

                self.previous_label.setGeometry(
                    previous_rect
                )

                self.fit_secondary_text(
                    self.previous_label,
                    previous_rect
                )


            if self.current_label.isVisible():

                self.current_label.setGeometry(
                    current_rect
                )

                self.fit_current_text(
                    self.current_label,
                    current_rect
                )


            if self.next_label.isVisible():

                self.next_label.setGeometry(
                    next_rect
                )

                self.fit_secondary_text(
                    self.next_label,
                    next_rect
                )


        super().resizeEvent(
            event
        )


    # =====================================================
    # SET LYRICS
    # =====================================================

    def set_lyrics(self, lyrics):

        self.lyrics = lyrics


    # =====================================================
    # HIDE EVERYTHING
    # =====================================================

    def hide_all(self):

        if self.animation_group is not None:

            self.animation_group.stop()


        self.current_index = -1


        self.previous_label.setText("")
        self.current_label.setText("")
        self.next_label.setText("")


        self.previous_label.hide()
        self.current_label.hide()
        self.next_label.hide()


        self.panel_opacity.setOpacity(
            0
        )

        self.panel.hide()


    # =====================================================
    # FIRST LYRIC
    # =====================================================

    def animate_first_lyric(self, index):

        if not self.lyrics:

            return


        if self.animation_group is not None:

            self.animation_group.stop()


        self.current_index = index


        (
            previous_rect,
            panel_rect,
            current_rect,
            next_rect,
            above_rect,
            below_rect,
            first_start_rect,
            panel_start_rect,
        ) = self.get_positions()


        # =================================================
        # PANEL
        # =================================================

        self.panel.setGeometry(
            panel_start_rect
        )

        self.panel_opacity.setOpacity(
            0.0
        )

        self.panel.show()

        self.panel.lower()


        # =================================================
        # FIRST CURRENT LYRIC
        # =================================================

        self.current_label.setText(
            self.lyrics[index][1]
        )


        self.apply_current_style(
            self.current_label
        )


        self.fit_current_text(
            self.current_label,
            current_rect
        )


        self.current_label.setGeometry(
            first_start_rect
        )

        self.current_label.show()

        self.current_label.raise_()


        # No previous yet
        self.previous_label.hide()


        # Prepare next
        if index + 1 < len(self.lyrics):

            self.next_label.setText(
                self.lyrics[
                    index + 1
                ][1]
            )

        else:

            self.next_label.setText("")


        self.apply_next_style(
            self.next_label
        )


        self.fit_secondary_text(
            self.next_label,
            next_rect
        )


        self.next_label.hide()


        # =================================================
        # PANEL EXPAND
        # =================================================

        panel_geometry_animation = QPropertyAnimation(
            self.panel,
            b"geometry"
        )

        panel_geometry_animation.setDuration(
            380
        )

        panel_geometry_animation.setStartValue(
            panel_start_rect
        )

        panel_geometry_animation.setEndValue(
            panel_rect
        )

        panel_geometry_animation.setEasingCurve(
            QEasingCurve.OutCubic
        )


        # =================================================
        # PANEL FADE
        # =================================================

        panel_opacity_animation = QPropertyAnimation(
            self.panel_opacity,
            b"opacity"
        )

        panel_opacity_animation.setDuration(
            320
        )

        panel_opacity_animation.setStartValue(
            0.0
        )

        panel_opacity_animation.setEndValue(
            1.0
        )

        panel_opacity_animation.setEasingCurve(
            QEasingCurve.OutCubic
        )


        # =================================================
        # FIRST LYRIC SLIDES UP
        # =================================================

        lyric_animation = QPropertyAnimation(
            self.current_label,
            b"geometry"
        )

        lyric_animation.setDuration(
            460
        )

        lyric_animation.setStartValue(
            first_start_rect
        )

        lyric_animation.setEndValue(
            current_rect
        )

        lyric_animation.setEasingCurve(
            QEasingCurve.OutCubic
        )


        # =================================================
        # START
        # =================================================

        self.animation_group = QParallelAnimationGroup(
            self
        )


        self.animation_group.addAnimation(
            panel_geometry_animation
        )

        self.animation_group.addAnimation(
            panel_opacity_animation
        )

        self.animation_group.addAnimation(
            lyric_animation
        )


        def finished():

            self.panel.setGeometry(
                panel_rect
            )


            self.panel_opacity.setOpacity(
                1.0
            )


            self.current_label.setGeometry(
                current_rect
            )


            self.fit_current_text(
                self.current_label,
                current_rect
            )


            if self.next_label.text():

                self.next_label.setGeometry(
                    next_rect
                )

                self.fit_secondary_text(
                    self.next_label,
                    next_rect
                )

                self.next_label.show()

                self.next_label.raise_()


        self.animation_group.finished.connect(
            finished
        )


        self.animation_group.start()


    # =====================================================
    # NORMAL TRANSITION
    # =====================================================

    def animate_to_index(self, new_index):

        if not self.lyrics:

            return


        if self.current_index == -1:

            self.animate_first_lyric(
                new_index
            )

            return


        if new_index != self.current_index + 1:

            self.set_index_immediately(
                new_index
            )

            return


        if (
            self.animation_group is not None
            and
            self.animation_group.state()
            ==
            QAbstractAnimation.Running
        ):

            self.animation_group.stop()

            self.set_index_immediately(
                new_index
            )

            return


        (
            previous_rect,
            panel_rect,
            current_rect,
            next_rect,
            above_rect,
            below_rect,
            first_start_rect,
            panel_start_rect,
        ) = self.get_positions()


        self.current_index = new_index


        # =================================================
        # OLD PREVIOUS
        # =================================================

        old_previous = self.previous_label


        previous_animation = QPropertyAnimation(
            old_previous,
            b"geometry"
        )


        previous_animation.setDuration(
            380
        )


        previous_animation.setStartValue(
            previous_rect
        )


        previous_animation.setEndValue(
            above_rect
        )


        previous_animation.setEasingCurve(
            QEasingCurve.OutCubic
        )


        # =================================================
        # CURRENT -> PREVIOUS
        # =================================================

        old_current = self.current_label


        self.apply_previous_style(
            old_current
        )


        self.fit_secondary_text(
            old_current,
            previous_rect
        )


        current_animation = QPropertyAnimation(
            old_current,
            b"geometry"
        )


        current_animation.setDuration(
            420
        )


        current_animation.setStartValue(
            current_rect
        )


        current_animation.setEndValue(
            previous_rect
        )


        current_animation.setEasingCurve(
            QEasingCurve.OutCubic
        )


        # =================================================
        # NEXT -> CURRENT
        # =================================================

        old_next = self.next_label


        self.apply_current_style(
            old_next
        )


        self.fit_current_text(
            old_next,
            current_rect
        )


        old_next.show()


        next_animation = QPropertyAnimation(
            old_next,
            b"geometry"
        )


        next_animation.setDuration(
            420
        )


        next_animation.setStartValue(
            next_rect
        )


        next_animation.setEndValue(
            current_rect
        )


        next_animation.setEasingCurve(
            QEasingCurve.OutCubic
        )


        # =================================================
        # NEW NEXT
        # =================================================

        new_next = self.create_next_label()


        future_index = (
            new_index + 1
        )


        if future_index < len(self.lyrics):

            new_next.setText(
                self.lyrics[
                    future_index
                ][1]
            )

        else:

            new_next.setText("")


        self.fit_secondary_text(
            new_next,
            next_rect
        )


        new_next.setGeometry(
            below_rect
        )


        new_next.show()

        new_next.raise_()


        incoming_animation = QPropertyAnimation(
            new_next,
            b"geometry"
        )


        incoming_animation.setDuration(
            420
        )


        incoming_animation.setStartValue(
            below_rect
        )


        incoming_animation.setEndValue(
            next_rect
        )


        incoming_animation.setEasingCurve(
            QEasingCurve.OutCubic
        )


        # =================================================
        # RUN
        # =================================================

        self.animation_group = QParallelAnimationGroup(
            self
        )


        self.animation_group.addAnimation(
            previous_animation
        )


        self.animation_group.addAnimation(
            current_animation
        )


        self.animation_group.addAnimation(
            next_animation
        )


        self.animation_group.addAnimation(
            incoming_animation
        )


        def finished():

            old_previous.deleteLater()


            self.previous_label = old_current

            self.current_label = old_next

            self.next_label = new_next


            self.apply_previous_style(
                self.previous_label
            )


            self.apply_current_style(
                self.current_label
            )


            self.apply_next_style(
                self.next_label
            )


            self.fit_secondary_text(
                self.previous_label,
                previous_rect
            )


            self.fit_current_text(
                self.current_label,
                current_rect
            )


            self.fit_secondary_text(
                self.next_label,
                next_rect
            )


            self.previous_label.setGeometry(
                previous_rect
            )


            self.current_label.setGeometry(
                current_rect
            )


            self.next_label.setGeometry(
                next_rect
            )


            self.previous_label.show()

            self.current_label.show()


            if self.next_label.text():

                self.next_label.show()

            else:

                self.next_label.hide()


            self.previous_label.raise_()

            self.current_label.raise_()

            self.next_label.raise_()


        self.animation_group.finished.connect(
            finished
        )


        self.animation_group.start()


    # =====================================================
    # IMMEDIATE UPDATE
    # =====================================================

    def set_index_immediately(self, index):

        if not self.lyrics:

            return


        if index < 0:

            self.hide_all()

            return


        if self.animation_group is not None:

            self.animation_group.stop()


        self.current_index = index


        (
            previous_rect,
            panel_rect,
            current_rect,
            next_rect,
            above_rect,
            below_rect,
            first_start_rect,
            panel_start_rect,
        ) = self.get_positions()


        self.panel.setGeometry(
            panel_rect
        )


        self.panel_opacity.setOpacity(
            1.0
        )


        self.panel.show()

        self.panel.lower()


        # Previous
        if index > 0:

            self.previous_label.setText(
                self.lyrics[
                    index - 1
                ][1]
            )

            self.previous_label.show()

        else:

            self.previous_label.setText("")

            self.previous_label.hide()


        # Current
        self.current_label.setText(
            self.lyrics[
                index
            ][1]
        )

        self.current_label.show()


        # Next
        if index + 1 < len(self.lyrics):

            self.next_label.setText(
                self.lyrics[
                    index + 1
                ][1]
            )

            self.next_label.show()

        else:

            self.next_label.setText("")

            self.next_label.hide()


        self.apply_previous_style(
            self.previous_label
        )


        self.apply_current_style(
            self.current_label
        )


        self.apply_next_style(
            self.next_label
        )


        self.fit_secondary_text(
            self.previous_label,
            previous_rect
        )


        self.fit_current_text(
            self.current_label,
            current_rect
        )


        self.fit_secondary_text(
            self.next_label,
            next_rect
        )


        self.previous_label.setGeometry(
            previous_rect
        )


        self.current_label.setGeometry(
            current_rect
        )


        self.next_label.setGeometry(
            next_rect
        )


        self.previous_label.raise_()

        self.current_label.raise_()

        self.next_label.raise_()


# =========================================================
# MAIN PLAYER
# =========================================================

class MusicPlayer(QWidget):

    def __init__(self):

        super().__init__()


        self.setWindowTitle(
            "I Really Want to Stay at Your House"
        )


        self.resize(
            1280,
            720
        )


        self.setMinimumSize(
            900,
            550
        )


        self.original_background = None

        self.lyrics = []

        self.lyric_times = []

        self.current_lyric_index = -1

        self.dragging_slider = False


        self.setup_audio()

        self.setup_ui()

        self.load_files()


    # =====================================================
    # AUDIO
    # =====================================================

    def setup_audio(self):

        self.audio_output = QAudioOutput()

        self.audio_output.setVolume(
            0.8
        )


        self.player = QMediaPlayer()

        self.player.setAudioOutput(
            self.audio_output
        )


        self.player.positionChanged.connect(
            self.position_changed
        )


        self.player.durationChanged.connect(
            self.duration_changed
        )


        self.player.playbackStateChanged.connect(
            self.state_changed
        )


    # =====================================================
    # UI
    # =====================================================

    def setup_ui(self):

        self.setStyleSheet("""
            QWidget {

                background-color:
                    black;

                color:
                    white;

                font-family:
                    Arial;
            }


            QSlider::groove:horizontal {

                background:
                    rgba(255,255,255,55);

                height:
                    5px;

                border-radius:
                    2px;
            }


            QSlider::sub-page:horizontal {

                background:
                    #00eaff;

                height:
                    5px;

                border-radius:
                    2px;
            }


            QSlider::handle:horizontal {

                background:
                    white;

                width:
                    15px;

                height:
                    15px;

                margin:
                    -5px 0;

                border-radius:
                    7px;
            }
        """)


        # =================================================
        # BACKGROUND
        # =================================================

        self.background = QLabel(
            self
        )


        self.background.setAlignment(
            Qt.AlignCenter
        )


        self.background.lower()


        # =================================================
        # OVERLAY
        # =================================================

        self.overlay = OverlayWidget(
            self
        )


        self.overlay.lower()


        # =================================================
        # MAIN LAYOUT
        # =================================================

        layout = QVBoxLayout(
            self
        )


        layout.setContentsMargins(
            25,
            25,
            25,
            25
        )


        layout.setSpacing(
            5
        )


        layout.addStretch(
            3
        )


        # =================================================
        # LYRICS
        # =================================================

        self.lyric_stage = LyricsStage(
            self
        )


        layout.addWidget(
            self.lyric_stage
        )


        layout.addStretch(
            3
        )


        # =================================================
        # PROGRESS
        # =================================================

        progress_layout = QHBoxLayout()


        progress_layout.setSpacing(
            12
        )


        self.current_time_label = QLabel(
            "00:00"
        )


        self.total_time_label = QLabel(
            "00:00"
        )


        time_style = """
            QLabel {

                background:
                    transparent;

                color:
                    white;

                font-size:
                    12px;

                font-weight:
                    bold;
            }
        """


        self.current_time_label.setStyleSheet(
            time_style
        )


        self.total_time_label.setStyleSheet(
            time_style
        )


        self.progress_slider = ClickableSlider(
            Qt.Horizontal
        )


        self.progress_slider.setRange(
            0,
            1000
        )


        self.progress_slider.sliderPressed.connect(
            self.slider_pressed
        )


        self.progress_slider.sliderReleased.connect(
            self.slider_released
        )


        self.progress_slider.sliderClicked.connect(
            self.seek
        )


        progress_layout.addWidget(
            self.current_time_label
        )


        progress_layout.addWidget(
            self.progress_slider
        )


        progress_layout.addWidget(
            self.total_time_label
        )


        layout.addLayout(
            progress_layout
        )


        # =================================================
        # PLAY
        # =================================================

        controls = QHBoxLayout()


        controls.addStretch()


        self.play_button = QPushButton(
            "▶"
        )


        self.play_button.setCursor(
            Qt.PointingHandCursor
        )


        self.play_button.setFixedSize(
            62,
            48
        )


        self.play_button.setStyleSheet("""
            QPushButton {

                font-size:
                    20px;

                font-weight:
                    bold;

                color:
                    white;

                background-color:
                    rgba(0,0,0,110);

                border:
                    2px solid rgba(0,234,255,200);

                border-radius:
                    23px;
            }

            QPushButton:hover {

                background-color:
                    rgba(0,234,255,75);

                border:
                    2px solid white;
            }
        """)


        self.play_button.clicked.connect(
            self.toggle_play
        )


        controls.addWidget(
            self.play_button
        )


        controls.addStretch()


        layout.addLayout(
            controls
        )


    # =====================================================
    # FILE LOADING
    # =====================================================

    def load_files(self):

        if os.path.exists(
            BACKGROUND_FILE
        ):

            self.load_background(
                BACKGROUND_FILE
            )


        if os.path.exists(
            SONG_FILE
        ):

            self.player.setSource(
                QUrl.fromLocalFile(
                    SONG_FILE
                )
            )


        if os.path.exists(
            LYRICS_FILE
        ):

            self.load_lyrics(
                LYRICS_FILE
            )


    # =====================================================
    # BACKGROUND
    # =====================================================

    def load_background(self, path):

        pixmap = QPixmap(
            path
        )


        if pixmap.isNull():

            return


        self.original_background = pixmap

        self.update_background()


    def update_background(self):

        if self.original_background is None:

            return


        pixmap = self.original_background.scaled(
            self.size(),
            Qt.KeepAspectRatioByExpanding,
            Qt.SmoothTransformation
        )


        self.background.setPixmap(
            pixmap
        )


    # =====================================================
    # LYRICS
    # =====================================================

    def load_lyrics(self, path):

        self.lyrics = []


        pattern = re.compile(
            r"\[(\d{1,2}):(\d{1,2}(?:\.\d+)?)\](.*)"
        )


        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:


            for line in file:

                matches = pattern.findall(
                    line
                )


                for minutes, seconds, text in matches:

                    timestamp = (
                        int(minutes) * 60
                        +
                        float(seconds)
                    )


                    text = text.strip()


                    if text:

                        self.lyrics.append(
                            (
                                timestamp,
                                text
                            )
                        )


        self.lyrics.sort(
            key=lambda x: x[0]
        )


        self.lyric_times = [
            lyric[0]
            for lyric in self.lyrics
        ]


        self.lyric_stage.set_lyrics(
            self.lyrics
        )


        self.lyric_stage.hide_all()


    # =====================================================
    # UPDATE LYRICS
    # =====================================================

    def update_lyrics(self, position_ms):

        if not self.lyrics:

            return


        seconds = (
            position_ms
            /
            1000
        )


        index = bisect_right(
            self.lyric_times,
            seconds
        ) - 1


        # BEFORE FIRST LYRIC
        if index < 0:

            if self.current_lyric_index != -1:

                self.current_lyric_index = -1

                self.lyric_stage.hide_all()

            return


        if index == self.current_lyric_index:

            return


        old_index = (
            self.current_lyric_index
        )


        self.current_lyric_index = index


        # FIRST LYRIC
        if old_index == -1 and index == 0:

            self.lyric_stage.animate_first_lyric(
                index
            )

            return


        # NORMAL FORWARD
        if index == old_index + 1:

            self.lyric_stage.animate_to_index(
                index
            )

            return


        # SEEK
        self.lyric_stage.set_index_immediately(
            index
        )


    # =====================================================
    # PLAY / PAUSE
    # =====================================================

    def toggle_play(self):

        if (
            self.player.playbackState()
            ==
            QMediaPlayer.PlayingState
        ):

            self.player.pause()

        else:

            self.player.play()


    def state_changed(self, state):

        if state == QMediaPlayer.PlayingState:

            self.play_button.setText(
                "❚❚"
            )

        else:

            self.play_button.setText(
                "▶"
            )


    # =====================================================
    # POSITION
    # =====================================================

    def position_changed(self, position):

        self.update_lyrics(
            position
        )


        duration = self.player.duration()


        if (
            duration > 0
            and
            not self.dragging_slider
        ):

            value = int(
                position
                /
                duration
                *
                1000
            )


            self.progress_slider.setValue(
                value
            )


        self.current_time_label.setText(
            self.format_time(
                position
            )
        )


    def duration_changed(self, duration):

        self.total_time_label.setText(
            self.format_time(
                duration
            )
        )


    # =====================================================
    # SEEK
    # =====================================================

    def slider_pressed(self):

        self.dragging_slider = True


    def slider_released(self):

        self.dragging_slider = False


        self.seek(
            self.progress_slider.value()
        )


    def seek(self, value):

        duration = self.player.duration()


        if duration <= 0:

            return


        position = int(
            duration
            *
            value
            /
            1000
        )


        self.current_lyric_index = -999


        self.player.setPosition(
            position
        )


    # =====================================================
    # TIME
    # =====================================================

    @staticmethod
    def format_time(milliseconds):

        seconds = int(
            milliseconds / 1000
        )


        minutes = (
            seconds // 60
        )


        seconds = (
            seconds % 60
        )


        return (
            f"{minutes:02}:{seconds:02}"
        )


    # =====================================================
    # KEYS
    # =====================================================

    def keyPressEvent(self, event):

        if event.key() == Qt.Key_Space:

            self.toggle_play()


        elif event.key() == Qt.Key_F11:

            if self.isFullScreen():

                self.showNormal()

            else:

                self.showFullScreen()


        elif event.key() == Qt.Key_Escape:

            if self.isFullScreen():

                self.showNormal()


        elif event.key() == Qt.Key_Right:

            self.current_lyric_index = -999


            self.player.setPosition(
                min(
                    self.player.duration(),
                    self.player.position()
                    +
                    5000
                )
            )


        elif event.key() == Qt.Key_Left:

            self.current_lyric_index = -999


            self.player.setPosition(
                max(
                    0,
                    self.player.position()
                    -
                    5000
                )
            )


    # =====================================================
    # RESIZE
    # =====================================================

    def resizeEvent(self, event):

        self.background.setGeometry(
            self.rect()
        )


        self.overlay.setGeometry(
            self.rect()
        )


        self.update_background()


        super().resizeEvent(
            event
        )


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":

    app = QApplication(
        sys.argv
    )


    window = MusicPlayer()


    window.show()


    sys.exit(
        app.exec()
    )