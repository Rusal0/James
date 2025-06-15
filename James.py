import os
import shutil
import sys
from datetime import datetime

# Import PySide6 modules
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget,
    QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QListWidget, QProgressBar, QFileDialog,
    QMessageBox, QAbstractItemView, QSizePolicy
)
from PySide6.QtCore import Qt, QSize, QThread, Signal, QPoint, QRect
from PySide6.QtGui import QMouseEvent, QFont, QIcon

# --- Script 1: Folder Creation Functions (Adapted for PySide6 UI Interactions) ---
def create_directory(path):
    """Creates a directory if it doesn't exist."""
    os.makedirs(path, exist_ok=True)

def get_language_code_med_devices(language):
    """Extracts the first two lowercase and last two uppercase letters of a language."""
    if len(language) >= 4:
        return f"{language[:2].lower()}{language[-2:].upper()}"
    elif len(language) == 3:
        return f"{language[:2].lower()}{language[-1:].upper()}"
    elif len(language) == 2:
        return f"{language.lower()}{language.upper()}"
    else:
        return "xxXX" # Default if language code is too short

def get_current_date_code():
    """Returns the current date inYYYY-MM-DD format."""
    return datetime.now().strftime("%Y-%m-%d")

def browse_folder_pyside(entry_widget: QLineEdit):
    """Opens a QFileDialog for the user to select a folder and updates the QLineEdit."""
    folder_selected = QFileDialog.getExistingDirectory(None, "Select Folder", "", QFileDialog.ShowDirsOnly)
    if folder_selected:
        entry_widget.setText(folder_selected)

# --- Methodology Specific Folder Creation Functions ---
def create_base_folders(path):
    """Creates the base 'Work' folder and initial subfolders (for non-Med_Devices)."""
    try:
        work_path = os.path.join(path, "Work")
        create_directory(work_path)
        create_directory(os.path.join(work_path, "01_Source"))
        prep_path = os.path.join(work_path, "02_Prep")
        create_directory(prep_path)
        create_directory(os.path.join(prep_path, "01_toDTP-ENG"))
        create_directory(os.path.join(prep_path, "02_fromDTP-ENG"))
        create_directory(os.path.join(prep_path, "03_SegQA"))
        create_directory(os.path.join(work_path, "03_Mapping"))
        create_directory(os.path.join(work_path, "04_Mapping_Review"))
        legacy_analysis_path = os.path.join(work_path, "05_Legacy_Analysis")
        create_directory(legacy_analysis_path)
        create_directory(os.path.join(legacy_analysis_path, "01_toCleanUp"))
        create_directory(os.path.join(legacy_analysis_path, "02_CleanedUp"))
        create_directory(os.path.join(legacy_analysis_path, "03_TMX-Create"))
        target_path = os.path.join(work_path, "06_Target")
        create_directory(target_path)
        return target_path
    except Exception as e:
        raise e

def create_language_folders_adapt(languages, path, progress_callback):
    """Creates 'Adapt' methodology specific folders."""
    try:
        target_path = create_base_folders(path)
        if target_path:
            for language in languages:
                language_path = os.path.join(target_path, language)
                create_directory(language_path)
                adapt_path = os.path.join(language_path, "Adapt")
                create_directory(adapt_path)
                adapt_subfolders = ["01_Adapt", "02_LLQA", "03_Post", "04_Final_QA", "05_Final_PM", "06_TM_Update"]
                for subfolder in adapt_subfolders:
                    create_directory(os.path.join(adapt_path, subfolder))
                create_directory(os.path.join(adapt_path, "01_Adapt", "01_toLing"))
                create_directory(os.path.join(adapt_path, "01_Adapt", "02_fromLing"))
                create_directory(os.path.join(adapt_path, "03_Post", "01_toPost"))
                create_directory(os.path.join(adapt_path, "03_Post", "02_fromPost"))
                progress_callback.emit(1)
    except Exception as e:
        raise e

def create_language_folders_TEP(languages, path, progress_callback):
    """Creates 'TEP' methodology specific folders."""
    try:
        target_path = create_base_folders(path)
        if target_path:
            for language in languages:
                language_path = os.path.join(target_path, language)
                create_directory(language_path)
                tep_path = os.path.join(language_path, "TEP")
                create_directory(tep_path)
                main_folders = ["01_Trans", "02_Edit", "03_LLQA", "05_Post", "06_Final_QA", "07_Final_PM", "08_TM_Update"]
                for folder in main_folders:
                    create_directory(os.path.join(tep_path, folder))
                create_directory(os.path.join(tep_path, "01_Trans", "01_toLing"))
                create_directory(os.path.join(tep_path, "01_Trans", "02_fromLing"))
                create_directory(os.path.join(tep_path, "02_Edit", "01_toLing"))
                create_directory(os.path.join(tep_path, "02_Edit", "02_fromLing"))
                create_directory(os.path.join(tep_path, "05_Post", "01_toPost"))
                create_directory(os.path.join(tep_path, "05_Post", "02_fromPost"))
                progress_callback.emit(1)
    except Exception as e:
        raise e

def create_language_folders_lv(languages, path, progress_callback):
    """Creates 'LV' methodology specific folders."""
    try:
        target_path = create_base_folders(path)
        if target_path:
            subfolders_with_nested_structure = {
                "01a_FT1", "01b_FT2", "02_Rec1", "03_BT", "04_CR",
                "05_Rec2", "06_SME_Review", "07_Rec3", "09_LSO", "10_CogDeb", "11_Rec4"
            }
            for i, language in enumerate(languages):
                language_path = os.path.join(target_path, language)
                create_directory(language_path)
                lv_path = os.path.join(language_path, "LV")
                create_directory(lv_path)
                lv_subfolders = [
                    "01a_FT1", "01b_FT2", "02_Rec1", "03_BT", "04_CR",
                    "05_Rec2", "06_SME_Review", "07_Rec3", "08_Post", "09_LSO",
                    "10_CogDeb", "11_Rec4", "12_Final_QA", "13_Final_PM", "14_TM_Update"
                ]
                for subfolder in lv_subfolders:
                    subfolder_path = os.path.join(lv_path, subfolder)
                    create_directory(subfolder_path)
                    if subfolder in subfolders_with_nested_structure:
                        create_directory(os.path.join(subfolder_path, "01_toLing"))
                        create_directory(os.path.join(subfolder_path, "02_fromLing"))
                        create_directory(os.path.join(subfolder_path, "03_LLQA"))
                progress_callback.emit(1)
    except Exception as e:
        raise e

def create_language_folders_ftbt(languages, path, progress_callback):
    """Creates 'FTBT' methodology specific folders."""
    try:
        target_path = create_base_folders(path)
        if target_path:
            for language in languages:
                language_path = os.path.join(target_path, language)
                create_directory(language_path)
                ftbt_path = os.path.join(language_path, "FTBT")
                create_directory(ftbt_path)
                ftbt_subfolders = ["01_FT", "02_BT", "03_CR", "04_CRI", "05_Post", "06_LSO", "07_Final_QA", "08_Final_PM", "09_TM_Update"]
                target_inner_subfolders = ["01_FT", "02_BT", "03_CR", "04_CRI", "06_LSO"]
                for subfolder in ftbt_subfolders:
                    subfolder_path = os.path.join(ftbt_path, subfolder)
                    create_directory(subfolder_path)
                    if subfolder in target_inner_subfolders:
                        create_directory(os.path.join(subfolder_path, "01_toLing"))
                        create_directory(os.path.join(subfolder_path, "02_fromLing"))
                        create_directory(os.path.join(subfolder_path, "03_LLQA"))
                progress_callback.emit(1)
    except Exception as e:
        raise e

def create_language_folders_migration(languages, path, progress_callback):
    """Creates 'Migration' methodology specific folders."""
    try:
        target_path = create_base_folders(path)
        if target_path:
            for language in languages:
                language_path = os.path.join(target_path, language)
                create_directory(language_path)
                migration_path = os.path.join(language_path, "Migration")
                create_directory(migration_path)
                migration_subfolders = ["01_Mig", "02_MigQA", "03_Post", "04_SSR1", "05_SSR2", "06_SSR3", "x_Approved"]
                for subfolder in migration_subfolders:
                    subfolder_path = os.path.join(migration_path, subfolder)
                    create_directory(subfolder_path)
                    if subfolder in ["01_Mig", "02_MigQA", "04_SSR1", "05_SSR2", "06_SSR3"]:
                        create_directory(os.path.join(subfolder_path, "01_toLing"))
                        create_directory(os.path.join(subfolder_path, "02_fromLing"))
                        create_directory(os.path.join(subfolder_path, "03_LLQA"))
                progress_callback.emit(1)
    except Exception as e:
        raise e

def create_language_folders_flv(languages, path, progress_callback):
    """Creates 'FLV' methodology specific folders."""
    try:
        target_path = create_base_folders(path)
        if target_path:
            for language in languages:
                language_path = os.path.join(target_path, language)
                create_directory(language_path)
                flv_path = os.path.join(language_path, "FLV")
                create_directory(flv_path)
                flv_subfolders = ["01a_FT1", "01b_FT2", "02_Rec1", "03_BT", "04_CR", "05_Rec2", "06_Expert_Review", "07_Rec3", "08_SME_Review", "09_Rec4", "10_Post"]
                for subfolder in flv_subfolders:
                    subfolder_path = os.path.join(flv_path, subfolder)
                    create_directory(subfolder_path)
                    if subfolder in ["01a_FT1", "01b_FT2", "02_Rec1", "03_BT", "04_CR", "05_Rec2", "06_Expert_Review", "07_Rec3", "08_SME_Review", "09_Rec4"]:
                        create_directory(os.path.join(subfolder_path, "01_toLing"))
                        create_directory(os.path.join(subfolder_path, "02_fromLing"))
                        create_directory(os.path.join(subfolder_path, "03_LLQA"))
                progress_callback.emit(1)
    except Exception as e:
        raise e

def create_language_folders_med_devices(languages, path, progress_callback):
    """Creates 'Med_Devices' methodology specific folders."""
    try:
        work_path = os.path.join(path, "Work")
        create_directory(work_path)

        for language in languages:
            lang_code = get_language_code_med_devices(language)
            date_code = get_current_date_code()

            create_directory(os.path.join(work_path, "01_Source",f"{date_code}_{lang_code}", language))
            create_directory(os.path.join(work_path, "02_Prep", f"{date_code}_{lang_code}", language))
            create_directory(os.path.join(work_path, "03_Trans", f"{date_code}_{lang_code}", language))
            create_directory(os.path.join(work_path, "04_Revision", f"{date_code}_{lang_code}", language))
            create_directory(os.path.join(work_path, "05_Post", f"{date_code}_{lang_code}", language))
            create_directory(os.path.join(work_path, "06_Final_QA", f"{date_code}_{lang_code}", language))
            create_directory(os.path.join(work_path, "07_Final_PM", f"{date_code}_{lang_code}", language))
            create_directory(os.path.join(work_path, "xx_ICR", f"{date_code}_{lang_code}", language))
            create_directory(os.path.join(work_path, "xx_ICR_imp", f"{date_code}_{lang_code}", language))

            progress_callback.emit(1)
    except Exception as e:
        raise e

def create_language_folders_cogdeb(languages, path, progress_callback):
    """Creates 'CogDeb' methodology specific folders."""
    try:
        target_path = create_base_folders(path)
        if target_path:
            for language in languages:
                language_path = os.path.join(target_path, language)
                create_directory(language_path)
                cogdeb_path = os.path.join(language_path, "CogDeb")
                create_directory(cogdeb_path)
                cogdeb_subfolders = ["01a_FT1", "01b_FT2", "02_Rec1", "03_BT", "04_CR", "05_Rec2", "06_Post", "07_LSO", "08_CogDeb", "09_Rec4", "10_Final_QA", "11_Final_PM", "12_TM_Update"]
                target_inner_cogdeb_subfolders = ["01a_FT1", "01b_FT2", "02_Rec1", "03_BT", "04_CR", "05_Rec2", "07_LSO", "08_CogDeb", "09_Rec4"]
                for subfolder in cogdeb_subfolders:
                    subfolder_path = os.path.join(cogdeb_path, subfolder)
                    create_directory(subfolder_path)
                    if subfolder in target_inner_cogdeb_subfolders:
                        create_directory(os.path.join(subfolder_path, "01_toLing"))
                        create_directory(os.path.join(subfolder_path, "02_fromLing"))
                        create_directory(os.path.join(subfolder_path, "03_LLQA"))
                progress_callback.emit(1)
    except Exception as e:
        raise e


# --- QThread for Folder Creation ---
class FolderCreationWorker(QThread):
    progress_updated = Signal(int)
    finished = Signal()
    error_occurred = Signal(str)

    def __init__(self, languages_str: str, methodologies_list: list, path: str):
        super().__init__()
        self.languages_str = languages_str
        self.methodologies_list = methodologies_list
        self.path = path

    def run(self):
        try:
            parsed_languages = [lang.strip() for lang in self.languages_str.split(',') if lang.strip()]
            if not parsed_languages:
                self.error_occurred.emit("Languages input is invalid.")
                return

            for method in self.methodologies_list:
                method_lower = method.lower()
                if method_lower == "adapt":
                    create_language_folders_adapt(parsed_languages, self.path, self.progress_updated)
                elif method_lower == "tep":
                    create_language_folders_TEP(parsed_languages, self.path, self.progress_updated)
                elif method_lower == "lv":
                    create_language_folders_lv(parsed_languages, self.path, self.progress_updated)
                elif method_lower == "ftbt":
                    create_language_folders_ftbt(parsed_languages, self.path, self.progress_updated)
                elif method_lower == "migration":
                    create_language_folders_migration(parsed_languages, self.path, self.progress_updated)
                elif method_lower == "flv":
                    create_language_folders_flv(parsed_languages, self.path, self.progress_updated)
                elif method_lower == "med_devices":
                    create_language_folders_med_devices(parsed_languages, self.path, self.progress_updated)
                elif method_lower == "cogdeb":
                    create_language_folders_cogdeb(parsed_languages, self.path, self.progress_updated)
                else:
                    self.error_occurred.emit(f"Unknown methodology: {method}")
                    return

            self.finished.emit()
        except Exception as e:
            self.error_occurred.emit(f"An unexpected error occurred: {e}")


# --- Script 2: Empty Folder Deletion Functions (Adapted for PySide6 UI Interactions) ---
def is_dir_empty(dirpath):
    for _, dirnames, files in os.walk(dirpath):
        if files or dirnames:
            return False
    return True

def identify_empty_dirs(path):
    empty_folders = []
    for dirpath, dirnames, files in os.walk(path, topdown=False):
        if "_Obsolete" not in dirpath:
            if is_dir_empty(dirpath):
                empty_folders.append(dirpath)
    return empty_folders

def move_empty_dirs(empty_folders, obsolete_dir):
    moved_folders_info = []
    for folder in empty_folders:
        try:
            common_base = os.path.commonpath([folder, obsolete_dir])
            relative_path = os.path.relpath(folder, common_base)
           
            dest_folder = os.path.join(obsolete_dir, relative_path)
            os.makedirs(os.path.dirname(dest_folder), exist_ok=True)
            shutil.move(folder, dest_folder)
            moved_folders_info.append(f"Moved: {folder} to {dest_folder}")
        except Exception as e:
            moved_folders_info.append(f"Failed to move {folder}: {e}")
    return moved_folders_info

def process_empty_folder_deletion_logic(path_to_clean: str):
    if not path_to_clean or not os.path.isdir(path_to_clean):
        QMessageBox.warning(None, "Input Error", "Please enter a valid path to clean.")
        return

    obsolete_dir = os.path.join(path_to_clean, "_Obsolete")
    os.makedirs(obsolete_dir, exist_ok=True)

    empty_folders_report = []
    moved_folders_report = []

    try:
        while True:
            current_empty_folders = identify_empty_dirs(path_to_clean)
            if not current_empty_folders:
                break

            moved_info = move_empty_dirs(current_empty_folders, obsolete_dir)
            empty_folders_report.extend(current_empty_folders)
            moved_folders_report.extend(moved_info)
           
            if not moved_info and current_empty_folders:
                break

        if empty_folders_report:
            report_file_path = os.path.join(path_to_clean, 'empty_folders_report.txt')
            moved_report_file_path = os.path.join(path_to_clean, 'moved_folders_report.txt')

            with open(report_file_path, 'w') as f:
                f.write("Identified Empty Folders:\n" + '\n'.join(empty_folders_report) + '\n')

            with open(moved_report_file_path, 'w') as f:
                f.write("Moved Folders Details:\n" + '\n'.join(moved_folders_report) + '\n')

            final_message = f"The script has finished execution. Reports created:\n- {report_file_path}\n- {moved_report_file_path}"
        else:
            final_message = "No empty folders are present in the specified directory."

        QMessageBox.information(None, "Empty Folder Deletion", final_message)

    except Exception as e:
        QMessageBox.critical(None, "Error", f"An error occurred during empty folder deletion: {e}")

# --- PySide6 UI Classes ---
class FolderCreationTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.worker_thread = None
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(15, 15, 15, 15) # Reduced padding slightly
        self.layout.setSpacing(10) # Default spacing between elements

        tab_title_label = QLabel("Folder Automation Tool")
        tab_title_label.setObjectName("TitleLabel")
        self.layout.addWidget(tab_title_label)
        self.layout.addSpacing(10) # Reduced spacing after title

        # Languages Input
        self.layout.addWidget(QLabel("Enter Languages (comma separated):"))
        self.languages_entry = QLineEdit()
        self.languages_entry.setPlaceholderText("e.g., enIN, French(France), de-DE")
        # Let QLineEdit expand horizontally. Set a sensible minimum.
        self.languages_entry.setMinimumWidth(300)
        self.layout.addWidget(self.languages_entry)
        # No extra spacing here, relying on layout.setSpacing(10)

        # Methodologies Selection
        self.layout.addWidget(QLabel("Select Methodologies:"))
        self.methodology_listbox = QListWidget()
        self.methodology_listbox.setSelectionMode(QAbstractItemView.MultiSelection)
        methodologies = ["Adapt", "TEP", "LV", "FTBT", "Migration", "FLV", "Med_Devices", "CogDeb"]
        self.methodology_listbox.addItems(methodologies)
        # Use QSizePolicy to allow vertical expansion, but set a fixed width for alignment
        self.methodology_listbox.setFixedWidth(380) # Keep fixed width to match other elements
        self.methodology_listbox.setMinimumHeight(len(methodologies) * 25) # Estimate height
        self.methodology_listbox.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.layout.addWidget(self.methodology_listbox)
        # No extra spacing here

        # Folder Selection
        self.folder_selection_h_layout = QHBoxLayout()
        self.folder_entry = QLineEdit()
        self.folder_entry.setPlaceholderText("Browse for a directory to create structures in...")
        self.folder_entry.setReadOnly(True)
        self.folder_entry.setFixedWidth(300) # Match the width with progress bar if needed, otherwise rely on stretch
       
        self.browse_button = QPushButton("Browse")
        self.browse_button.setFixedSize(70, 28) # Slightly smaller button
        self.browse_button.clicked.connect(lambda: browse_folder_pyside(self.folder_entry))
       
        self.folder_selection_h_layout.addWidget(self.folder_entry)
        self.folder_selection_h_layout.addWidget(self.browse_button)
        self.layout.addLayout(self.folder_selection_h_layout)
        # No extra spacing here

        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setValue(0)
        self.progress_bar.setFixedWidth(380) # Explicitly set width to align with listbox
        self.layout.addWidget(self.progress_bar)
        # No extra spacing here

        # Create Folders Button (centered horizontally, smaller)
        self.create_button = QPushButton("Create Folders")
        self.create_button.setFixedSize(110, 32) # Smaller button
        self.create_button.clicked.connect(self.on_create_folders_clicked)
       
        button_layout = QHBoxLayout() # Use a sub-layout to center the button
        button_layout.addStretch(1)
        button_layout.addWidget(self.create_button)
        button_layout.addStretch(1)
        self.layout.addLayout(button_layout)

        self.layout.addStretch(1) # Push content to the top

    def on_create_folders_clicked(self):
        languages = self.languages_entry.text()
        selected_methodologies = [item.text() for item in self.methodology_listbox.selectedItems()]
        path = self.folder_entry.text()
       
        if not path:
            QMessageBox.warning(self, "Input Error", "Please select a folder to create structures in.")
            return
        if not languages:
            QMessageBox.warning(self, "Input Error", "Please enter at least one language.")
            return
        if not selected_methodologies:
            QMessageBox.warning(self, "Input Error", "Please select at least one methodology.")
            return

        parsed_languages = [lang.strip() for lang in languages.split(',') if lang.strip()]
        if not parsed_languages:
            QMessageBox.warning(self, "Input Error", "Languages input is invalid.")
            return

        self.create_button.setEnabled(False)
        self.languages_entry.setEnabled(False)
        self.methodology_listbox.setEnabled(False)
        self.folder_entry.setEnabled(False)
        self.browse_button.setEnabled(False) # Disable browse button during operation

        total_languages_iterations = len(parsed_languages) * len(selected_methodologies)
        self.progress_bar.setMaximum(total_languages_iterations)
        self.progress_bar.setValue(0)

        self.worker_thread = FolderCreationWorker(languages, selected_methodologies, path)
        self.worker_thread.progress_updated.connect(self.update_progress)
        self.worker_thread.finished.connect(self.on_creation_finished)
        self.worker_thread.error_occurred.connect(self.on_creation_error)
        self.worker_thread.start()

    def update_progress(self, increment):
        current_value = self.progress_bar.value()
        self.progress_bar.setValue(current_value + increment)

    def on_creation_finished(self):
        self.progress_bar.setValue(self.progress_bar.maximum())
        QMessageBox.information(self, "Success", "Folder structure created successfully!")
        self.progress_bar.setValue(0)
        self.enable_ui_elements()

    def on_creation_error(self, message):
        QMessageBox.critical(self, "Error", message)
        self.progress_bar.setValue(0)
        self.enable_ui_elements()

    def enable_ui_elements(self):
        self.create_button.setEnabled(True)
        self.languages_entry.setEnabled(True)
        self.methodology_listbox.setEnabled(True)
        self.folder_entry.setEnabled(True)
        self.browse_button.setEnabled(True) # Re-enable browse button

class EmptyFolderDeletionTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15) # Consistent padding
        layout.setSpacing(10) # Consistent spacing

        tab_title_label = QLabel("Empty Folder Deletion Tool")
        tab_title_label.setObjectName("TitleLabel")
        layout.addWidget(tab_title_label)
        layout.addSpacing(10)

        # Path to Clean
        layout.addWidget(QLabel("Enter Path to Clean:"))
        folder_selection_h_layout = QHBoxLayout()
        self.path_entry_efd = QLineEdit()
        self.path_entry_efd.setPlaceholderText("Browse for a directory to clean...")
        self.path_entry_efd.setReadOnly(True)
        self.path_entry_efd.setMinimumWidth(300) # Maintain consistent minimum width
       
        browse_button = QPushButton("Browse")
        browse_button.setFixedSize(70, 28) # Consistent with FolderCreationTab's browse button
        browse_button.clicked.connect(lambda: browse_folder_pyside(self.path_entry_efd))
       
        folder_selection_h_layout.addWidget(self.path_entry_efd)
        folder_selection_h_layout.addWidget(browse_button)
        layout.addLayout(folder_selection_h_layout)
        # No extra spacing here

        # Delete Button (centered horizontally, smaller)
        delete_button = QPushButton("Delete Empty Folders")
        delete_button.setFixedSize(180, 32) # Smaller button
        delete_button.clicked.connect(self.on_delete_empty_folders_clicked)
       
        button_layout_efd = QHBoxLayout()
        button_layout_efd.addStretch(1)
        button_layout_efd.addWidget(delete_button)
        button_layout_efd.addStretch(1)
        layout.addLayout(button_layout_efd)

        layout.addStretch(1) # Keep stretch here if this tab is shorter and you want content to stick to top

    def on_delete_empty_folders_clicked(self):
        path = self.path_entry_efd.text()
        process_empty_folder_deletion_logic(path)

# Custom Title Bar Widget
class CustomTitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.setFixedHeight(30)
        self.setObjectName("CustomTitleBar")

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.title_label = QLabel("COA - Automation Tool")
        self.title_label.setObjectName("TitleBarLabel")
        self.title_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.layout.addWidget(self.title_label)
        self.layout.addStretch(1)

        self.minimize_button = QPushButton("—")
        self.minimize_button.setObjectName("MinimizeButton")
        self.minimize_button.setFixedSize(40, 30)
        self.minimize_button.clicked.connect(self.parent_window.showMinimized)
        self.layout.addWidget(self.minimize_button)

        self.maximize_button = QPushButton("□")
        self.maximize_button.setObjectName("MaximizeButton")
        self.maximize_button.setFixedSize(40, 30)
        self.maximize_button.clicked.connect(self.toggle_maximize_restore)
        self.layout.addWidget(self.maximize_button)

        self.close_button = QPushButton("✕")
        self.close_button.setObjectName("CloseButton")
        self.close_button.setFixedSize(40, 30)
        self.close_button.clicked.connect(self.parent_window.close)
        self.layout.addWidget(self.close_button)

        self.start_pos = None
        self.pressing = False

    def toggle_maximize_restore(self):
        if self.parent_window.isMaximized():
            self.parent_window.showNormal()
            self.maximize_button.setText("□")
        else:
            self.parent_window.old_pos = self.parent_window.pos()
            self.parent_window.showMaximized()
            self.maximize_button.setText("❐")

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.pressing = True
            self.start_pos = event.globalPosition().toPoint() - self.parent_window.pos()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.pressing and self.start_pos is not None:
            self.parent_window.move(event.globalPosition().toPoint() - self.start_pos)
            event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent):
        self.pressing = False
        self.start_pos = None
        event.accept()
   
    def mouseDoubleClickEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.toggle_maximize_restore()
            event.accept()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.old_pos = self.pos()
        self.init_ui()
        self.set_calculated_size()

    def set_calculated_size(self):
        # Create a dummy instance of FolderCreationTab to get its preferred size
        temp_tab = FolderCreationTab()
        # It's crucial to put it in a temporary layout to allow its internal layouts to calculate sizes
        dummy_container = QWidget()
        dummy_container_layout = QVBoxLayout(dummy_container)
        dummy_container_layout.addWidget(temp_tab)
        dummy_container.setLayout(dummy_container_layout)
        dummy_container_layout.activate() # Force layout recalculation
       
        # Get the size hint after layouts have been calculated
        content_size_hint = temp_tab.sizeHint()

        # Calculate width: Max of fixed widths (380 for listbox/progress bar) + padding + border
        # Max input widget width (listbox, progress bar) is 380px.
        # Tab content area padding (FolderCreationTab.setContentsMargins(15, 15, 15, 15)) = 15px left/right
        # QTabWidget::pane border = 1px left/right
        content_pane_width = 380 + (15 * 2) + (1 * 2) # = 412
       
        # QTabBar width (from stylesheet padding + icon/text width, usually about 100-120px for West position)
        tab_bar_width = 120 # Estimate for vertical tab bar
       
        # Main window border
        main_window_border = 1 * 2 # 1px on left and right for QMainWindow

        calculated_width = content_pane_width + tab_bar_width + main_window_border # 412 + 120 + 2 = 534

        # Calculate height:
        # Title bar height
        title_bar_height = self.title_bar.height() # 30px

        # Tab pane vertical padding and border
        # QTabWidget::pane padding (15px top/bottom) + border (1px top/bottom)
        tab_pane_vertical_extras = (15 * 2) + (1 * 2) # = 32px
       
        # Sum of heights of widgets in FolderCreationTab + vertical spacing
        # Let's sum based on the `init_ui` layout and estimated widget heights/spacing
        # (Assuming default label height ~18px, lineedit/button height ~28-35px, progress bar ~20px, listbox ~200px)
       
        # A more dynamic way to sum heights would be `temp_tab.sizeHint().height()`, but it often returns
        # less accurate values without a full `show()` and `adjustSize()` cycle.
        # Manual sum for now based on common widget heights and specified spacings:
        content_height_sum = (
            30 +  # TitleLabel (generous est based on font size)
            10 +  # Spacing after title
            18 +  # Language Label
            30 +  # Language Entry (with padding from stylesheet)
            10 +  # Spacing
            18 +  # Methodologies Label
            200 + # Methodology Listbox (approx. 8 items * 25px)
            10 +  # Spacing
            30 +  # Folder Entry/Browse row (QLineEdit/QPushButton heights 28-30)
            10 +  # Spacing
            20 +  # Progress Bar
            10 +  # Spacing
            35    # Create Button (with padding from stylesheet)
        ) # Sum of typical heights + 10px spacing = ~421px

        # Add the tab pane extras and title bar height
        calculated_height = title_bar_height + tab_pane_vertical_extras + content_height_sum + 10 # 10 for bottom stretch/buffer
        # 30 (title bar) + 32 (tab pane padding/border) + 421 (content) + 10 (buffer) = 493

        # Set final calculated size
        self.setFixedSize(QSize(534, 495)) # Adjusted to fit slightly better based on my run

        # Clean up dummy widget and tab
        dummy_container.deleteLater()
        temp_tab.deleteLater()


    def get_stylesheet(self):
        stylesheet = """
            QMessageBox {
                background-color: #1a1a1a;
                color: #ffffff;
                border: 1px solid #ff6600;
                border-radius: 8px;
            }
            QMessageBox QLabel {
                color: #ffffff;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 13px;
            }
            QMessageBox QPushButton {
                background-color: #ff6600;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 12px;
                font-weight: bold;
                min-width: 70px;
            }
            QMessageBox QPushButton:hover {
                background-color: #ff8533;
            }
            QMessageBox QPushButton:pressed {
                background-color: #cc5200;
            }
            QMessageBox QPushButton:focus {
                outline: none;
            }
           
            QMainWindow {
                background-color: #1a1a1a;
                border: 1px solid #333333;
                border-radius: 10px;
            }

            QWidget#CustomTitleBar {
                background-color: #0d0d0d;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
            }
            QLabel#TitleBarLabel {
                color: #ffffff;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
                font-weight: bold;
                padding-left: 10px;
            }
            QPushButton#MinimizeButton,
            QPushButton#MaximizeButton,
            QPushButton#CloseButton {
                background-color: transparent;
                border: none;
                color: #ffffff;
                font-size: 16px;
                font-weight: bold;
                padding: 0px;
                margin: 0px;
                min-width: 40px;
                max-width: 40px;
                height: 30px;
                border-radius: 0px;
            }
            QPushButton#MinimizeButton:hover,
            QPushButton#MaximizeButton:hover {
                background-color: #333333;
            }
            QPushButton#CloseButton:hover {
                background-color: #e81123;
            }
            QPushButton#MinimizeButton:pressed,
            QPushButton#MaximizeButton:pressed {
                background-color: #555555;
            }
            QPushButton#CloseButton:pressed {
                background-color: #8c0a17;
            }

            QTabWidget::pane {
                border: 1px solid #ff6600;
                background-color: #1a1a1a;
                border-bottom-left-radius: 10px;
                border-bottom-right-radius: 10px;
                border-top-right-radius: 10px;
                margin-left: 3px;
            }
            QTabWidget::tab-bar {
                alignment: left;
            }
            QTabBar::tab {
                background: #333333;
                color: white;
                padding: 8px 15px; /* Smaller padding for tabs */
                border-top-left-radius: 6px;
                border-bottom-left-radius: 6px;
                margin-bottom: 3px;
                min-height: 35px; /* Slightly shorter tab height */
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 12px; /* Slightly smaller font */
                font-weight: bold;
                border: 1px solid #444444;
                border-right: none;
            }
            QTabBar::tab:selected {
                background: #ff6600;
                color: white;
                border: 1px solid #ff6600;
                border-right: none;
            }
            QTabBar::tab:hover:!selected {
                background: #555555;
            }
            QLabel {
                color: #ffffff;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 11px; /* Slightly smaller general label font */
            }
            QLabel#TitleLabel {
                color: #ff6600;
                font-size: 18px; /* Slightly smaller tab title */
                font-weight: bold;
                padding-bottom: 5px; /* Reduced padding */
            }
            QLineEdit {
                background-color: #333333;
                color: #ffffff;
                border: 1px solid #555555;
                border-radius: 5px; /* Slightly smaller radius */
                padding: 6px; /* Reduced padding */
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 11px; /* Consistent with labels */
                min-height: 20px; /* Ensure a minimum height */
            }
            QLineEdit:read-only {
                background-color: #2a2a2a;
                color: #aaaaaa;
            }
            QPushButton {
                background-color: #ff6600;
                color: white;
                border: none;
                border-radius: 5px; /* Consistent with line edit */
                padding: 6px 15px; /* Reduced padding for smaller buttons */
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 12px; /* Consistent with smaller buttons */
                font-weight: bold;
                min-width: 80px; /* Adjusted minimum width */
            }
            QPushButton:hover {
                background-color: #ff8533;
            }
            QPushButton:pressed {
                background-color: #cc5200;
            }
            QPushButton:disabled {
                background-color: #4a4a4a;
                color: #888888;
            }
            QListWidget {
                background-color: #333333;
                color: white;
                border: 1px solid #555555;
                border-radius: 5px;
                padding: 2px; /* Reduced padding */
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 11px; /* Consistent with labels */
            }
            QListWidget::item {
                padding: 4px; /* Reduced item padding */
            }
            QListWidget::item:selected {
                background-color: #ff6600;
                color: white;
                border-radius: 3px;
            }
            QListWidget::item:hover:!selected {
                background-color: #444444;
            }
            QProgressBar {
                border: 1px solid #555555;
                border-radius: 5px; /* Consistent with other elements */
                text-align: center;
                color: white;
                background-color: #333333;
                height: 18px; /* Slightly smaller progress bar */
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 11px;
            }
            QProgressBar::chunk {
                background-color: #ff6600;
                border-radius: 5px;
            }
        """
        return stylesheet


    def init_ui(self):
        main_vertical_layout = QVBoxLayout()
        main_vertical_layout.setContentsMargins(0, 0, 0, 0)
        main_vertical_layout.setSpacing(0)

        self.title_bar = CustomTitleBar(self)
        main_vertical_layout.addWidget(self.title_bar)

        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)

        self.tab_widget = QTabWidget()
        self.tab_widget.setTabPosition(QTabWidget.West)

        self.folder_creation_tab = FolderCreationTab()
        self.empty_folder_deletion_tab = EmptyFolderDeletionTab()

        self.tab_widget.addTab(self.folder_creation_tab, "Folder Creation")
        self.tab_widget.addTab(self.empty_folder_deletion_tab, "Empty Folder Deletion")

        content_layout.addWidget(self.tab_widget)
        main_vertical_layout.addWidget(content_widget)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setLayout(main_vertical_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
   
    main_window = MainWindow()
    app.setStyleSheet(main_window.get_stylesheet())

    main_window.show()
    sys.exit(app.exec())
