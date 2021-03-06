import json
import logging
from typing import Callable

from PySide2 import QtCore, QtUiTools, QtWidgets

from pie.core import IndexDB
from pie.util.misc_utils import MiscUtils


class PreferencesWindow:
    __logger = logging.getLogger('PreferencesWindow')
    __UI_FILE = "assets/mainwindow.ui"
    __QLINEEDIT_VALID_VALUE_STYLESHEET = "QLineEdit { background: rgba(0, 255, 0, 0.2); }"
    __QLINEEDIT_INVALID_VALUE_STYLESHEET = "QLineEdit { background: rgba(255, 0, 0, 0.2); }"

    def __init__(self, apply_process_changed_setting: Callable[[], None]):
        self.apply_process_changed_setting = apply_process_changed_setting
        self.__indexDB = IndexDB()
        self.settings = self.__indexDB.get_settings()

        ui_file = QtCore.QFile(MiscUtils.get_abs_resource_path(PreferencesWindow.__UI_FILE))
        ui_file.open(QtCore.QFile.ReadOnly)
        loader = QtUiTools.QUiLoader()
        self.window: QtWidgets.QMainWindow = loader.load(ui_file)
        ui_file.close()

        self.window.setWindowTitle("Edit Preferences")
        self.window.setFixedSize(self.window.size())  # TODO: Disable maximize button on OSX

        self.txtMonitoredDir: QtWidgets.QLineEdit = self.window.findChild(QtWidgets.QLineEdit, 'txtMonitoredDir')
        self.btnPickMonitoredDir: QtWidgets.QPushButton = self.window.findChild(QtWidgets.QPushButton, 'btnPickMonitoredDir')
        self.lwDirsToExclude: QtWidgets.QListWidget = self.window.findChild(QtWidgets.QListWidget, 'lwDirsToExclude')
        self.btnAddDirToExclude: QtWidgets.QPushButton = self.window.findChild(QtWidgets.QPushButton, 'btnAddDirToExclude')
        self.btnDelDirToExclude: QtWidgets.QPushButton = self.window.findChild(QtWidgets.QPushButton, 'btnDelDirToExclude')

        self.txtOutputDir: QtWidgets.QLineEdit = self.window.findChild(QtWidgets.QLineEdit, 'txtOutputDir')
        self.btnPickOutputDir: QtWidgets.QPushButton = self.window.findChild(QtWidgets.QPushButton, 'btnPickOutputDir')
        self.txtUnknownOutputDir: QtWidgets.QLineEdit = self.window.findChild(QtWidgets.QLineEdit, 'txtUnknownOutputDir')
        self.btnPickUnknownOutputDir: QtWidgets.QPushButton = self.window.findChild(QtWidgets.QPushButton, 'btnPickUnknownOutputDir')

        self.btnRestoreDefaults: QtWidgets.QPushButton = self.window.findChild(QtWidgets.QPushButton, 'btnRestoreDefaults')
        self.lblTaskStatus: QtWidgets.QLabel = self.window.findChild(QtWidgets.QLabel, 'lblTaskStatus')
        self.pbTaskProgress: QtWidgets.QProgressBar = self.window.findChild(QtWidgets.QProgressBar, 'pbTaskProgress')
        self.chkSkipSameNameVideo: QtWidgets.QCheckBox = self.window.findChild(QtWidgets.QCheckBox, 'chkSkipSameNameVideo')
        self.chkSkipSameNameRaw: QtWidgets.QCheckBox = self.window.findChild(QtWidgets.QCheckBox, 'chkSkipSameNameRaw')
        self.chkConvertUnknown: QtWidgets.QCheckBox = self.window.findChild(QtWidgets.QCheckBox, 'chkConvertUnknown')
        self.chkOverwriteFiles: QtWidgets.QCheckBox = self.window.findChild(QtWidgets.QCheckBox, 'chkOverwriteFiles')
        self.chkAutoUpdateCheck: QtWidgets.QCheckBox = self.window.findChild(QtWidgets.QCheckBox, 'chkAutoUpdateCheck')
        self.chkAutoShowLogWindow: QtWidgets.QCheckBox = self.window.findChild(QtWidgets.QCheckBox, 'chkAutoShowLogWindow')
        self.spinImageQuality: QtWidgets.QSpinBox = self.window.findChild(QtWidgets.QSpinBox, 'spinImageQuality')
        self.spinImageMaxDimension: QtWidgets.QSpinBox = self.window.findChild(QtWidgets.QSpinBox, 'spinImageMaxDimension')
        self.spinVideoMaxDimension: QtWidgets.QSpinBox = self.window.findChild(QtWidgets.QSpinBox, 'spinVideoMaxDimension')
        self.spinVideoCrf: QtWidgets.QSpinBox = self.window.findChild(QtWidgets.QSpinBox, 'spinVideoCrf')
        self.cbVideoNvencPreset: QtWidgets.QComboBox = self.window.findChild(QtWidgets.QComboBox, 'cbVideoNvencPreset')
        self.spinVideoAudioBitrate: QtWidgets.QSpinBox = self.window.findChild(QtWidgets.QSpinBox, 'spinVideoAudioBitrate')
        self.spinIndexingWorkers: QtWidgets.QSpinBox = self.window.findChild(QtWidgets.QSpinBox, 'spinIndexingWorkers')
        self.spinConversionWorkers: QtWidgets.QSpinBox = self.window.findChild(QtWidgets.QSpinBox, 'spinConversionWorkers')
        self.spinGpuWorkers: QtWidgets.QSpinBox = self.window.findChild(QtWidgets.QSpinBox, 'spinGpuWorkers')
        self.spinGpuCount: QtWidgets.QSpinBox = self.window.findChild(QtWidgets.QSpinBox, 'spinGpuCount')

        self.txtPathFfmpeg: QtWidgets.QLineEdit = self.window.findChild(QtWidgets.QLineEdit, 'txtPathFfmpeg')
        self.txtPathMagick: QtWidgets.QLineEdit = self.window.findChild(QtWidgets.QLineEdit, 'txtPathMagick')
        self.txtPathExiftool: QtWidgets.QLineEdit = self.window.findChild(QtWidgets.QLineEdit, 'txtPathExiftool')

        self.txtImageExt: QtWidgets.QLineEdit = self.window.findChild(QtWidgets.QLineEdit, 'txtImageExt')
        self.txtImageRawExt: QtWidgets.QLineEdit = self.window.findChild(QtWidgets.QLineEdit, 'txtImageRawExt')
        self.txtVideoExt: QtWidgets.QLineEdit = self.window.findChild(QtWidgets.QLineEdit, 'txtVideoExt')
        self.txtVideoRawExt: QtWidgets.QLineEdit = self.window.findChild(QtWidgets.QLineEdit, 'txtVideoRawExt')

        self.btnPickMonitoredDir.clicked.connect(self.btnPickMonitoredDir_click)
        self.lwDirsToExclude.itemSelectionChanged.connect(self.lwDirsToExclude_itemSelectionChanged)
        self.btnAddDirToExclude.clicked.connect(self.btnAddDirToExclude_click)
        self.btnDelDirToExclude.clicked.connect(self.btnDelDirToExclude_click)
        self.btnPickOutputDir.clicked.connect(self.btnPickOutputDir_click)
        self.btnPickUnknownOutputDir.clicked.connect(self.btnPickUnknownOutputDir_click)
        self.chkSkipSameNameVideo.stateChanged.connect(self.chkSkipSameNameVideo_stateChanged)
        self.chkSkipSameNameRaw.stateChanged.connect(self.chkSkipSameNameRaw_stateChanged)
        self.chkConvertUnknown.stateChanged.connect(self.chkConvertUnknown_stateChanged)
        self.chkOverwriteFiles.stateChanged.connect(self.chkOverwriteFiles_stateChanged)
        self.chkAutoUpdateCheck.stateChanged.connect(self.chkAutoUpdateCheck_stateChanged)
        self.chkAutoShowLogWindow.stateChanged.connect(self.chkAutoShowLogWindow_stateChanged)

        self.btnRestoreDefaults.clicked.connect(self.btnRestoreDefaults_click)

        self.spinImageQuality.valueChanged.connect(self.spinImageQuality_valueChanged)
        self.spinImageMaxDimension.valueChanged.connect(self.spinImageMaxDimension_valueChanged)
        self.spinVideoMaxDimension.valueChanged.connect(self.spinVideoMaxDimension_valueChanged)
        self.spinVideoCrf.valueChanged.connect(self.spinVideoCrf_valueChanged)
        self.cbVideoNvencPreset.currentTextChanged.connect(self.cbVideoNvencPreset_currentTextChanged)
        self.spinVideoAudioBitrate.valueChanged.connect(self.spinVideoAudioBitrate_valueChanged)
        self.spinIndexingWorkers.valueChanged.connect(self.spinIndexingWorkers_valueChanged)
        self.spinConversionWorkers.valueChanged.connect(self.spinConversionWorkers_valueChanged)
        self.spinGpuWorkers.valueChanged.connect(self.spinGpuWorkers_valueChanged)
        self.spinGpuCount.valueChanged.connect(self.spinGpuCount_valueChanged)

        self.txtPathFfmpeg.textChanged.connect(self.txtPathFfmpeg_textChanged)
        self.txtPathMagick.textChanged.connect(self.txtPathMagick_textChanged)
        self.txtPathExiftool.textChanged.connect(self.txtPathExiftool_textChanged)

        self.txtImageExt.textChanged.connect(self.txtImageExt_textChanged)
        self.txtImageRawExt.textChanged.connect(self.txtImageRawExt_textChanged)
        self.txtVideoExt.textChanged.connect(self.txtVideoExt_textChanged)
        self.txtVideoRawExt.textChanged.connect(self.txtVideoRawExt_textChanged)

        self.cbVideoNvencPreset: QtWidgets.QComboBox = self.window.findChild(QtWidgets.QComboBox, 'cbVideoNvencPreset')

        self.__indexDB.save_settings(self.settings)

    def show(self):
        self.apply_settings()
        self.window.show()
        self.window.raise_()
        self.window.activateWindow()

    def hide(self):
        self.window.hide()

    def btnPickMonitoredDir_click(self):
        selected_directory = QtCore.QDir.toNativeSeparators(QtWidgets.QFileDialog.getExistingDirectory(self.window, "Pick directory to monitor"))
        if selected_directory:
            self.settings.monitored_dir = selected_directory
            self.__indexDB.save_settings(self.settings)
            self.txtMonitoredDir.setText(self.settings.monitored_dir)

    def lwDirsToExclude_itemSelectionChanged(self):
        selected_items = self.lwDirsToExclude.selectedItems()
        self.btnDelDirToExclude.setEnabled(len(selected_items) > 0)

    def btnAddDirToExclude_click(self):
        selected_directory = QtCore.QDir.toNativeSeparators(QtWidgets.QFileDialog.getExistingDirectory(self.window, "Pick a directory to exclude"))
        current_dirs_to_exclude = json.loads(self.settings.dirs_to_exclude)
        if (selected_directory and not selected_directory in current_dirs_to_exclude):
            current_dirs_to_exclude.append(selected_directory)
            self.settings.dirs_to_exclude = json.dumps(current_dirs_to_exclude)
            self.lwDirsToExclude.addItem(selected_directory)
            self.__indexDB.save_settings(self.settings)

    def btnDelDirToExclude_click(self):
        selected_items = self.lwDirsToExclude.selectedItems()
        for selected_item in selected_items:
            selected_item: QtWidgets.QListWidgetItem = selected_item
            current_dirs_to_exclude = json.loads(self.settings.dirs_to_exclude)
            current_dirs_to_exclude.remove(selected_item.text())
            self.settings.dirs_to_exclude = json.dumps(current_dirs_to_exclude)
            self.lwDirsToExclude.takeItem(self.lwDirsToExclude.row(selected_item))
        self.__indexDB.save_settings(self.settings)

    def btnPickOutputDir_click(self):
        selected_directory = QtCore.QDir.toNativeSeparators(QtWidgets.QFileDialog.getExistingDirectory(self.window, "Pick output directory"))
        if selected_directory:
            self.settings.output_dir = selected_directory
            self.__indexDB.save_settings(self.settings)
            self.txtOutputDir.setText(self.settings.output_dir)

    def btnPickUnknownOutputDir_click(self):
        selected_directory = QtCore.QDir.toNativeSeparators(QtWidgets.QFileDialog.getExistingDirectory(self.window, "Pick output directory"))
        if selected_directory:
            self.settings.unknown_output_dir = selected_directory
            self.__indexDB.save_settings(self.settings)
            self.txtUnknownOutputDir.setText(self.settings.unknown_output_dir)

    def btnRestoreDefaults_click(self):
        response: QtWidgets.QMessageBox.StandardButton = QtWidgets.QMessageBox.question(
            self.window, "Confirm Action", "Clear all settings and restore defaults?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if QtWidgets.QMessageBox.Yes == response:
            self.__indexDB.clear_settings()
            self.settings = self.__indexDB.get_settings()
            self.apply_settings()

    def apply_settings(self):
        self.txtMonitoredDir.setText(self.settings.monitored_dir)
        self.lwDirsToExclude.clear()
        self.lwDirsToExclude.addItems(json.loads(self.settings.dirs_to_exclude))
        self.txtUnknownOutputDir.setText(self.settings.unknown_output_dir)
        self.txtOutputDir.setText(self.settings.output_dir)
        self.chkSkipSameNameVideo.setChecked(self.settings.skip_same_name_video)
        self.chkSkipSameNameRaw.setChecked(self.settings.skip_same_name_raw)
        self.chkConvertUnknown.setChecked(self.settings.convert_unknown)
        self.chkOverwriteFiles.setChecked(self.settings.overwrite_output_files)
        self.chkAutoUpdateCheck.setChecked(self.settings.auto_update_check)
        self.chkAutoShowLogWindow.setChecked(self.settings.auto_show_log_window)
        self.spinImageQuality.setValue(self.settings.image_compression_quality)
        self.spinImageMaxDimension.setValue(self.settings.image_max_dimension)
        self.spinVideoMaxDimension.setValue(self.settings.video_max_dimension)
        self.spinVideoCrf.setValue(self.settings.video_crf)
        self.cbVideoNvencPreset.setCurrentIndex(self.cbVideoNvencPreset.findText(self.settings.video_nvenc_preset))
        self.spinVideoAudioBitrate.setValue(self.settings.video_audio_bitrate)
        self.spinIndexingWorkers.setValue(self.settings.indexing_workers)
        self.spinConversionWorkers.setValue(self.settings.conversion_workers)
        self.spinGpuWorkers.setValue(self.settings.gpu_workers)
        self.spinGpuCount.setValue(self.settings.gpu_count)
        self.txtPathFfmpeg.setText(self.settings.path_ffmpeg)
        self.txtPathMagick.setText(self.settings.path_magick)
        self.txtPathExiftool.setText(self.settings.path_exiftool)
        self.txtImageExt.setText(self.settings.image_extensions)
        self.txtImageRawExt.setText(self.settings.image_raw_extensions)
        self.txtVideoExt.setText(self.settings.video_extensions)
        self.txtVideoRawExt.setText(self.settings.video_raw_extensions)

    def cleanup(self):
        self.__logger.info("Performing cleanup")
        self.window.hide()
        self.__indexDB.disconnect_db()
        self.__logger.info("Cleanup completed")

    def chkSkipSameNameVideo_stateChanged(self):
        self.settings.skip_same_name_video = self.chkSkipSameNameVideo.isChecked()
        self.__indexDB.save_settings(self.settings)

    def chkSkipSameNameRaw_stateChanged(self):
        self.settings.skip_same_name_raw = self.chkSkipSameNameRaw.isChecked()
        self.__indexDB.save_settings(self.settings)

    def chkConvertUnknown_stateChanged(self):
        self.settings.convert_unknown = self.chkConvertUnknown.isChecked()
        self.__indexDB.save_settings(self.settings)

    def chkOverwriteFiles_stateChanged(self):
        self.settings.overwrite_output_files = self.chkOverwriteFiles.isChecked()
        self.__indexDB.save_settings(self.settings)

    def chkAutoUpdateCheck_stateChanged(self):
        self.settings.auto_update_check = self.chkAutoUpdateCheck.isChecked()
        self.__indexDB.save_settings(self.settings)

    def chkAutoShowLogWindow_stateChanged(self):
        self.settings.auto_show_log_window = self.chkAutoShowLogWindow.isChecked()
        self.__indexDB.save_settings(self.settings)

    def spinImageQuality_valueChanged(self, new_value: int):
        self.settings.image_compression_quality = new_value
        self.__indexDB.save_settings(self.settings)

    def spinImageMaxDimension_valueChanged(self, new_value: int):
        self.settings.image_max_dimension = new_value
        self.__indexDB.save_settings(self.settings)

    def spinVideoMaxDimension_valueChanged(self, new_value: int):
        self.settings.video_max_dimension = new_value
        self.__indexDB.save_settings(self.settings)

    def spinVideoCrf_valueChanged(self, new_value: int):
        self.settings.video_crf = new_value
        self.__indexDB.save_settings(self.settings)

    def cbVideoNvencPreset_currentTextChanged(self, new_text: str):
        self.settings.video_nvenc_preset = new_text
        self.__indexDB.save_settings(self.settings)

    def spinVideoAudioBitrate_valueChanged(self, new_value: int):
        self.settings.video_audio_bitrate = new_value
        self.__indexDB.save_settings(self.settings)

    def spinIndexingWorkers_valueChanged(self, new_value: int):
        self.settings.indexing_workers = new_value
        self.__indexDB.save_settings(self.settings)

    def spinConversionWorkers_valueChanged(self, new_value: int):
        self.settings.conversion_workers = new_value
        self.__indexDB.save_settings(self.settings)

    def spinGpuWorkers_valueChanged(self, new_value: int):
        self.settings.gpu_workers = new_value
        self.__indexDB.save_settings(self.settings)

    def spinGpuCount_valueChanged(self, new_value: int):
        self.settings.gpu_count = new_value
        self.__indexDB.save_settings(self.settings)

    def txtPathFfmpeg_textChanged(self, new_text: str):
        try:
            MiscUtils.exec_subprocess([new_text, "-h"], "Wrong path")
            self.txtPathFfmpeg.setStyleSheet(PreferencesWindow.__QLINEEDIT_VALID_VALUE_STYLESHEET)
            self.settings.path_ffmpeg = new_text
            self.__indexDB.save_settings(self.settings)
        except:
            self.txtPathFfmpeg.setStyleSheet(PreferencesWindow.__QLINEEDIT_INVALID_VALUE_STYLESHEET)

    def txtPathMagick_textChanged(self, new_text: str):
        try:
            MiscUtils.exec_subprocess([new_text, "-help"], "Wrong path")
            self.txtPathMagick.setStyleSheet(PreferencesWindow.__QLINEEDIT_VALID_VALUE_STYLESHEET)
            self.settings.path_magick = new_text
            self.__indexDB.save_settings(self.settings)
        except:
            self.txtPathMagick.setStyleSheet(PreferencesWindow.__QLINEEDIT_INVALID_VALUE_STYLESHEET)

    def txtPathExiftool_textChanged(self, new_text: str):
        try:
            MiscUtils.exec_subprocess([new_text, "-ver"], "Wrong path")
            self.txtPathExiftool.setStyleSheet(PreferencesWindow.__QLINEEDIT_VALID_VALUE_STYLESHEET)
            self.settings.path_exiftool = new_text
            self.__indexDB.save_settings(self.settings)
        except:
            self.txtPathExiftool.setStyleSheet(PreferencesWindow.__QLINEEDIT_INVALID_VALUE_STYLESHEET)

    def txtImageExt_textChanged(self, new_text: str):
        self.settings.image_extensions = new_text
        self.__indexDB.save_settings(self.settings)

    def txtImageRawExt_textChanged(self, new_text: str):
        self.settings.image_raw_extensions = new_text
        self.__indexDB.save_settings(self.settings)

    def txtVideoExt_textChanged(self, new_text: str):
        self.settings.video_extensions = new_text
        self.__indexDB.save_settings(self.settings)

    def txtVideoRawExt_textChanged(self, new_text: str):
        self.settings.video_raw_extensions = new_text
        self.__indexDB.save_settings(self.settings)
