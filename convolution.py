# coding: utf-8

# imports
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QProgressDialog, QAction
from PyQt5.QtGui import QTextCharFormat, QBrush
from PyQt5.QtCore import Qt
import sys
import math
import numpy as np
import matplotlib.pyplot as plt
from templates.MainWindowClass import Ui_MainWindow as Ui_MainWindow
from templates.SpectrumWindowClass import Ui_Dialog as Ui_SpectrumDialog
from templates.ReferenceWindowClass import Ui_Dialog as Ui_ReferenceDialog
from templates.OutputFileWindowClass import Ui_Dialog as Ui_OutputFileDialog

# GLOBALS
__version__ = 0.96
__copyright__ = "<a href='https://creativecommons.org/licenses/by/4.0/deed.fr'>CC-BY 4.0</a> (Authors attribution alone required)"
__GitHub_repos__ = "https://github.com/FlexStudia/Convolution-of-a-spectrum"
__author_mail__ = "flex.studia.dev@gmail.com"
__bug_support_mail__ = "convolution.of.a.spectrum@gmail.com"

# style
font_size = 10

# GLOBALS: deresoudre source spectrum
deresoudre_source_dict = dict()
deresoudre_source_dict.update({'deresoudre_data_set_up': ''})
deresoudre_source_dict.update({'deresoudre_source': ''})
deresoudre_source_dict.update({'deresoudre_file_name': ''})
deresoudre_source_dict.update({'fichier_a_deresoudre_unit': ''})
deresoudre_source_dict.update({'ligne_debut_deresoudre': 0})
deresoudre_source_dict.update({'long_column_number': 0})
deresoudre_source_dict.update({'refh_column_number': 0})
deresoudre_source_dict.update({'deresoudre_content_separator': '\t'})
# GLOBALS: reference source:
# attention: 'reference' in code is 'destination' on interface
reference_source_dict = dict()
reference_source_dict.update({'tabWidget_activa_tab': 0})
reference_source_dict.update({'tabWidget_2_activa_tab': 0})
reference_source_dict.update({'function_source': ''})
reference_source_dict.update({'reference_data_set_up': ''})
reference_source_dict.update({'function_type': ''})
reference_source_dict.update({'reference_source': ''})
reference_source_dict.update({'reference_source_file_name': ''})
reference_source_dict.update({'fichier_a_reference_unit': ''})
reference_source_dict.update({'ligne_debut_reference': 0})
reference_source_dict.update({'long_column_number': 0})
reference_source_dict.update({'reference_wavelength_separator': ''})
reference_source_dict.update({'wavelength_min': ''})
reference_source_dict.update({'wavelength_max': ''})
reference_source_dict.update({'wavelength_step': ''})
reference_source_dict.update({'width_const': ''})
reference_source_dict.update({'top_const': ''})
reference_source_dict.update({'width_top_source': ''})
reference_source_dict.update({'width_top_source_file_name': ''})
reference_source_dict.update({'ligne_debut_width_top': 0})
reference_source_dict.update({'width_column_number': 0})
reference_source_dict.update({'top_column_number': 0})
reference_source_dict.update({'width_top_separator': ''})
reference_source_dict.update({'width_min': ''})
reference_source_dict.update({'width_max': ''})
reference_source_dict.update({'top_min': ''})
reference_source_dict.update({'top_max': ''})
# GLOBALS: format output
format_output_dict = dict()
format_output_dict.update({'decimals_wavelength': 5})
format_output_dict.update({'decimals_intencity': 5})
format_output_dict.update({'format': 'decimal'})
format_output_dict.update({'wlth_format': 'decimal'})
format_output_dict.update({'intens_format': 'decimal'})
format_output_dict.update({'order': 1})
format_output_dict.update({'title': 'with'})
format_output_dict.update({'separator': '\t'})
# GLOBALS: data changed
data_changed_dict = dict()
data_changed_dict.update({'current_data_changed': -1})


# Other external functions
def set_yellow_text(separ_sign):
    fmt = QTextCharFormat()
    fmt.setBackground(QBrush(Qt.yellow))
    separ_sign.mergeCurrentCharFormat(fmt)
    if '\n' in separ_sign.toPlainText():
        separ_sign.setPlainText(separ_sign.toPlainText().replace('\n', ''))


def gauss(moy, ecart, x):
    pi = math.pi
    return math.exp(-((x - moy) ** 2) / (2 * ecart ** 2)) / (math.sqrt(2 * pi) * ecart)


def triangle(moy, ecart, x):
    if abs(x - moy) > 2 * ecart:
        return x * 10 ** (-20)
    elif x - moy <= 0:
        return ((x - moy) + 2 * ecart) / (4 * ecart ** 2)
    else:
        return ((moy - x) + 2 * ecart) / (4 * ecart ** 2)


def trapeze(moy, ecart, top, x):
    if abs(x - moy) > 2 * ecart - top:
        return x * 10 ** (-20)
    elif abs(x - moy) <= top:
        return 1 / (2 * ecart)
    elif x - moy <= 0:
        return ((x - moy) + 2 * ecart - top) / (4 * ecart * (ecart - top))
    else:
        return ((moy - x) + 2 * ecart - top) / (4 * ecart * (ecart - top))


def changement_units(value_to_convert, unit_from, unit_to):
    # possible units: cm-1, micron, nm, A
    if unit_from == unit_to:
        return value_to_convert
    else:
        if (unit_from == 'cm-1' and unit_to == 'micron') or (unit_from == 'micron' and unit_to == 'cm-1'):
            return 10_000 / value_to_convert
        if (unit_from == 'cm-1' and unit_to == 'nm') or (unit_from == 'nm' and unit_to == 'cm-1'):
            return 10_000_000 / value_to_convert
        if (unit_from == 'cm-1' and unit_to == 'A') or (unit_from == 'A' and unit_to == 'cm-1'):
            return 100_000_000 / value_to_convert
        if unit_from == 'micron' and unit_to == 'nm':
            return 1000 * value_to_convert
        if unit_from == 'nm' and unit_to == 'micron':
            return value_to_convert / 1000
        if unit_from == 'micron' and unit_to == 'A':
            return 10000 * value_to_convert
        if unit_from == 'A' and unit_to == 'micron':
            return value_to_convert / 10000
        if unit_from == 'nm' and unit_to == 'A':
            return 10 * value_to_convert
        if unit_from == 'A' and unit_to == 'nm':
            return value_to_convert / 10


# MAIN WINDOW class
class ConvolutionMainW(QtWidgets.QMainWindow):
    def __init__(self):
        super(ConvolutionMainW, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # class globals
        self.selected_windows = ""
        self.setWindowTitle(f"Convolution of a spectrum v{__version__}")
        self.deresoudre_content_array_long = []
        self.deresoudre_content_array_refh = []
        self.reference_content_array_longref = []
        self.FWM_array = []
        self.FWHM_array = []
        self.drefh = []
        self.reference_data_order = 1
        self.convolution_not_finished = 0
        self.answer = ''
        # GUI beauties
        # GUI beauties: buttons
        self.ui.btn_1.setStyleSheet('QPushButton{padding: 15px; background-color: #D5E4FF}')
        self.ui.btn_2.setStyleSheet('QPushButton{padding: 5px; background-color: #D5E4FF}')
        self.ui.btn_3.setStyleSheet('QPushButton{padding: 15px; background-color: #F2FFE7}')
        self.ui.btn_4.setStyleSheet('QPushButton{padding: 15px; background-color: #F2FFE7}')
        self.ui.btn_5.setStyleSheet('QPushButton{padding: 15px; background-color: #D5E4FF}')
        self.ui.btn_6.setStyleSheet('QPushButton{padding: 5px; background-color: #F2FFE7}')
        self.ui.btn_7.setStyleSheet('QPushButton{padding: 15px; background-color: #D5E4FF}')
        # Menu
        extractAction = QAction("&About", self)
        extractAction.setStatusTip('About The App')
        extractAction.triggered.connect(self.show_about)
        self.statusBar()
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&Help')
        fileMenu.addAction(extractAction)
        # Signal & Slots
        self.ui.btn_1.clicked.connect(self.spectrum_source)
        self.ui.btn_2.clicked.connect(self.reference_source)
        self.ui.btn_3.clicked.connect(self.output_param_set)
        self.ui.btn_4.clicked.connect(self.verification_data)
        self.ui.btn_5.clicked.connect(self.convolution_calc)
        self.ui.btn_6.clicked.connect(self.plot_data)
        self.ui.btn_7.clicked.connect(self.download_file)

    def show_about(self):
        self.dialog_ok(f"<b>Convolution of a Spectrum</b> v{__version__}"
                       f"<p>Copyright: {__copyright__}</p>"
                       f"<p><a href='{__GitHub_repos__}'>GitHub repository</a> (program code and more information)</p>"
                       f"<p>Created by Gorbacheva Maria ({__author_mail__})</p>"
                       "<p>Scientific base by Bernard Schmitt, IPAG (bernard.schmitt@univ-grenoble-alpes.fr)</p>"
                       f"<p>For any questions and bug reports, please, mail at {__bug_support_mail__}</p>"
                       "<p>In case of a bug, please report it and specify your operating system, "
                       "provide a detailed description of the problem with screenshots "
                       "and the files used and produced, if possible. Your contribution matters to make it better!</p>")

    def spectrum_source(self):
        try:
            SpectrumSourceW()
        except Exception as e:
            win.dialog_critical(f'Critical error while loading the spectrum for convolution window: {str(e)}')

    def reference_source(self):
        try:
            ReferenceSourceW()
        except Exception as e:
            win.dialog_critical(f'Critical error while loading the destination wavelengths window: {str(e)}')

    def output_param_set(self):
        try:
            OutputParamW()
        except Exception as e:
            win.dialog_critical(f'Critical error while loading the output file parameters window: {str(e)}')

    def dialog_critical(self, s):
        dlg = QMessageBox(self)
        dlg.setWindowTitle('Error!')
        dlg.setText(s)
        dlg.setIcon(QMessageBox.Critical)
        dlg.show()

    def dialog_ok(self, s):
        dlg = QMessageBox(self)
        dlg.setWindowTitle('Ok!')
        dlg.setText(s)
        dlg.setIcon(QMessageBox.Information)
        dlg.show()

    def dialog_progress_verif(self, text1, text2, lim1, lim2):
        dlg = QProgressDialog(text1, text2, lim1, lim2)
        dlg.setWindowModality(Qt.WindowModal)
        dlg.setMinimumDuration(100)
        dlg.setWindowTitle('At work')
        # reference wavelength & width are the same length
        verification_wavelength_width_ok = 1
        if len(self.reference_content_array_longref) != len(self.FWHM_array) and len(self.FWHM_array) != 1:
            verification_wavelength_width_ok = 0
        # reference width & top are the same length
        verification_width_top_len_ok = 1
        if reference_source_dict['function_type'] == 'Trapeze':
            if len(self.FWHM_array) != len(self.FWM_array):
                verification_width_top_len_ok = 0
        if not verification_wavelength_width_ok or not verification_width_top_len_ok:
            verification_widths_tops_ok = 1
            verification_merge_border_ok = 1
            verification_merge_spectre_ok = 1
        else:
            # test widths & tops for Trapeze
            verification_widths_tops_ok = 1
            if reference_source_dict['function_type'] == 'Trapeze':
                if len(self.FWHM_array) != 1:
                    for i in range(len(self.FWHM_array)):
                        if self.FWHM_array[i] < self.FWM_array[i]:
                            verification_widths_tops_ok = 0
            # des marges de convolution aux deux extrémités du spectre
            verification_merge_border_ok = 0
            min_side = 0
            max_side = 0
            min_limit = 0
            max_limit = 0
            width_lbd_ref_min = self.FWHM_array[0] if len(self.FWHM_array) == 1 else min(self.FWHM_array)
            width_lbd_ref_max = self.FWHM_array[0] if len(self.FWHM_array) == 1 else max(self.FWHM_array)
            if reference_source_dict['function_type'] == "Gaussienne":
                min_limit = min(self.reference_content_array_longref) - 3 * width_lbd_ref_min
                max_limit = max(self.reference_content_array_longref) + 3 * width_lbd_ref_max
                if min(self.deresoudre_content_array_long) < \
                        min(self.reference_content_array_longref) - 3 * width_lbd_ref_min:
                    verification_merge_border_ok = 1
                    min_side = 1
                if max(self.deresoudre_content_array_long) > \
                        max(self.reference_content_array_longref) + 3 * width_lbd_ref_max:
                    verification_merge_border_ok = 1
                    max_side = 1
            elif reference_source_dict['function_type'] == "Triangle":
                min_limit = min(self.reference_content_array_longref) - width_lbd_ref_min
                max_limit = max(self.reference_content_array_longref) + width_lbd_ref_max
                if min(self.deresoudre_content_array_long) < \
                        min(self.reference_content_array_longref) - width_lbd_ref_min:
                    verification_merge_border_ok = 1
                    min_side = 1
                if max(self.deresoudre_content_array_long) > \
                        max(self.reference_content_array_longref) + width_lbd_ref_max:
                    verification_merge_border_ok = 1
                    max_side = 1
            elif reference_source_dict['function_type'] == "Trapeze":
                top_width_lbd_ref_min = self.FWM_array[0] if len(self.FWM_array) == 1 else min(self.FWM_array)
                top_width_lbd_ref_max = self.FWM_array[0] if len(self.FWM_array) == 1 else max(self.FWM_array)
                min_limit = min(self.reference_content_array_longref) - top_width_lbd_ref_min - width_lbd_ref_min
                max_limit = max(self.reference_content_array_longref) + top_width_lbd_ref_max + width_lbd_ref_max
                if min(self.deresoudre_content_array_long) < \
                        min(self.reference_content_array_longref) - top_width_lbd_ref_min - width_lbd_ref_min:
                    verification_merge_border_ok = 1
                    min_side = 1
                if max(self.deresoudre_content_array_long) > \
                        max(self.reference_content_array_longref) + top_width_lbd_ref_max + width_lbd_ref_max:
                    verification_merge_border_ok = 1
                    max_side = 1
            # des marges de convolution sur tout spectre
            verification_merge_spectre_ok = 1
            if reference_source_dict['function_type'] == "Gaussienne":
                k_ref = 0.15
            elif reference_source_dict['function_type'] == "Triangle":
                k_ref = 0.5
            else:
                k_ref = 1.1
            i = 0
            for i in range(len(self.reference_content_array_longref)):
                dlg.setValue(i)
                if dlg.wasCanceled():
                    break
                for j in range(len(self.deresoudre_content_array_long) - 1):
                    if self.deresoudre_content_array_long[j] < self.reference_content_array_longref[i] < \
                            self.deresoudre_content_array_long[j + 1]:
                        if len(self.FWHM_array) == 1:
                            if reference_source_dict['function_type'] == "Gaussienne" or \
                                    reference_source_dict['function_type'] == "Triangle":
                                width_lbd_ref = self.FWHM_array[0]
                            else:
                                width_lbd_ref = self.FWHM_array[0] + self.FWM_array[0]
                        else:
                            if reference_source_dict['function_type'] == "Gaussienne" or \
                                    reference_source_dict['function_type'] == "Triangle":
                                width_lbd_ref = self.FWHM_array[i]
                            else:
                                width_lbd_ref = self.FWHM_array[i] + self.FWM_array[i]
                        if width_lbd_ref \
                                / (self.deresoudre_content_array_long[j + 1] - self.deresoudre_content_array_long[j]) \
                                <= k_ref:
                            verification_merge_spectre_ok = 0
                            break
                if verification_merge_spectre_ok == 0:
                    break
        index = 0
        self.answer = 'The following issues were found:'
        if not verification_merge_border_ok:
            if min_side:
                index = index + 1
                self.answer = self.answer + f'\n{index}. ' \
                                            f'The minimum destination wavelength is lower than the minimum ' \
                                            f'spectrum wavelength' \
                                            f'\nIt should be larger than {min_limit} ' \
                                            f'{reference_source_dict["fichier_a_reference_unit"]}'
            if max_side:
                index = index + 1
                self.answer = self.answer + f'\n{index}. ' \
                                            f'The maximum destination wavelength is larger than the maximum ' \
                                            f'spectrum wavelength' \
                                            f'\nIt should be lower than {max_limit} ' \
                                            f'{reference_source_dict["fichier_a_reference_unit"]}'
        if not verification_wavelength_width_ok:
            index = index + 1
            self.answer = self.answer + f'\n{index}. ' \
                                        f'The width set has not the same length than the destination wavelength set'
        if not verification_width_top_len_ok:
            index = index + 1
            self.answer = self.answer + f'\n{index}. ' \
                                        f'Trapeze convolution parameter issue: ' \
                                        f'width data do not have the same length as the top data'
        if not verification_merge_spectre_ok:
            index = index + 1
            self.answer = self.answer + f'\n{index}. The convolution condition on the width is not met at least once ' \
                                        f'(starting at destination wavelength ' \
                                        f'{self.reference_content_array_longref[i]})'
        if not verification_widths_tops_ok:
            index = index + 1
            self.answer = self.answer + f'\n{index}. ' \
                                        f'Trapeze convolution parameter issue: top value should be smaller than width!'
        dlg.setValue(len(self.reference_content_array_longref))
        dlg.show()

    def dialog_progress_calc(self, text1, text2, lim1, lim2):
        dlg = QProgressDialog(text1, text2, lim1, lim2)
        dlg.setWindowModality(Qt.WindowModal)
        dlg.setMinimumDuration(100)
        dlg.setWindowTitle('At work')
        self.convolution_not_finished = 0
        self.reading_data()
        # CONVOLUTION
        # set up the convolution result list
        self.drefh = []
        for i in range(len(self.reference_content_array_longref)):
            self.drefh.append(0)
        # convolution calc
        topsigma = 0
        for i in range(len(self.reference_content_array_longref)):
            dlg.setValue(i)
            if dlg.wasCanceled():
                self.convolution_not_finished = 1
                break
            # sigme & topsigma
            if len(self.FWHM_array) == 1:
                sigma = self.FWHM_array[0] / 2
                if reference_source_dict['function_type'] == "Trapeze":
                    topsigma = self.FWM_array[0] / 2
            else:
                sigma = self.FWHM_array[i] / 2
                if reference_source_dict['function_type'] == "Trapeze":
                    topsigma = self.FWM_array[i] / 2
            # min & max inside deresoudre_content_array_long
            j_min = 0
            j_max = len(self.deresoudre_content_array_long)
            if reference_source_dict['function_type'] == 'Gaussienne':
                for j in range(len(self.deresoudre_content_array_long)):
                    if (self.deresoudre_content_array_long[j] >
                        self.reference_content_array_longref[i] - 10 * sigma) and (j_min == 0):
                        j_min = j
                    if (self.deresoudre_content_array_long[j] >
                        self.reference_content_array_longref[i] + 10 * sigma) and \
                            (j_max == len(self.deresoudre_content_array_long)):
                        j_max = j
                        break
            elif reference_source_dict['function_type'] == 'Triangle':
                for j in range(len(self.deresoudre_content_array_long)):
                    if (self.deresoudre_content_array_long[j] > self.reference_content_array_longref[i]
                        - 3 * sigma) and (j_min == 0):
                        j_min = j
                    if (self.deresoudre_content_array_long[j] > self.reference_content_array_longref[i]
                        + 3 * sigma) and \
                            (j_max == len(self.deresoudre_content_array_long)):
                        j_max = j
                        break
            elif reference_source_dict['function_type'] == 'Trapeze':
                for j in range(len(self.deresoudre_content_array_long)):
                    if (self.deresoudre_content_array_long[j] > self.reference_content_array_longref[
                        i] - topsigma - 3 * sigma) and (
                            j_min == 0):
                        j_min = j
                    if (self.deresoudre_content_array_long[j] > self.reference_content_array_longref[
                        i] + topsigma + 3 * sigma) and (
                            j_max == len(self.deresoudre_content_array_long)):
                        j_max = j
                        break
            # ref function array calc
            ref_array = []
            if reference_source_dict['function_type'] == "Gaussienne":
                for j in range(j_min, j_max):
                    ref_array.append(gauss(self.reference_content_array_longref[i], sigma,
                                           self.deresoudre_content_array_long[j]))
            if reference_source_dict['function_type'] == "Triangle":
                for j in range(j_min, j_max):
                    ref_array.append(triangle(self.reference_content_array_longref[i], sigma,
                                              self.deresoudre_content_array_long[j]))
            if reference_source_dict['function_type'] == "Trapeze":
                for j in range(j_min, j_max):
                    ref_array.append(trapeze(self.reference_content_array_longref[i], sigma, topsigma,
                                             self.deresoudre_content_array_long[j]))
            # convolution
            if sum(ref_array):
                ref_array.reverse()
                self.drefh[i] = \
                    list(np.convolve(self.deresoudre_content_array_refh[j_min:j_max], ref_array, 'valid'))[
                        0] / sum(ref_array)
            else:
                j_delta = 0
                delta_value = abs(self.reference_content_array_longref[i] - self.deresoudre_content_array_long[0])
                for j in range(len(self.deresoudre_content_array_long)):
                    if delta_value < abs(self.reference_content_array_longref[i] -
                                         self.deresoudre_content_array_long[j]):
                        j_delta = j
                        delta_value = abs(self.reference_content_array_longref[i] -
                                          self.deresoudre_content_array_long[j])
                self.drefh[i] = self.deresoudre_content_array_refh[j_delta]
        dlg.setValue(len(self.reference_content_array_longref))
        dlg.show()

    def reading_data(self):
        self.deresoudre_content_array_long = []
        self.deresoudre_content_array_refh = []
        self.reference_content_array_longref = []
        self.FWM_array = []
        self.FWHM_array = []
        # READING INPUT
        # spectrum wavelength & intensities source
        l_index = 0
        for line in deresoudre_source_dict['deresoudre_source'].splitlines():
            l_index = l_index + 1
            if l_index >= deresoudre_source_dict['ligne_debut_deresoudre']:
                if float(line.split(deresoudre_source_dict['deresoudre_content_separator'])
                         [deresoudre_source_dict['long_column_number'] - 1].strip().replace(',', '.', 1)) != 0:
                    self.deresoudre_content_array_long.append(float(
                        line.split(deresoudre_source_dict['deresoudre_content_separator'])
                        [deresoudre_source_dict['long_column_number'] - 1].strip().replace(',', '.', 1)))
                    self.deresoudre_content_array_refh.append(float(
                        line.split(deresoudre_source_dict['deresoudre_content_separator'])
                        [deresoudre_source_dict['refh_column_number'] - 1].strip().replace(',', '.', 1)))
        # reference wavelength source
        if reference_source_dict['reference_source'] != '':
            l_index = 0
            if reference_source_dict['reference_wavelength_separator'] != '':
                for line in reference_source_dict['reference_source'].splitlines():
                    l_index = l_index + 1
                    if l_index >= reference_source_dict['ligne_debut_reference']:
                        self.reference_content_array_longref.append(float(
                            line.split(reference_source_dict['reference_wavelength_separator'])
                            [reference_source_dict['long_column_number'] - 1].strip().replace(',', '.', 1)))
            else:
                for line in reference_source_dict['reference_source'].splitlines():
                    l_index = l_index + 1
                    if l_index >= reference_source_dict['ligne_debut_reference']:
                        self.reference_content_array_longref.append(float(line.strip().replace(',', '.', 1)))
        else:
            for i in range(int((float(reference_source_dict['wavelength_max'].replace(',', '.', 1)) -
                                float(reference_source_dict['wavelength_min'].replace(',', '.', 1)))
                               / float(reference_source_dict['wavelength_step'].replace(',', '.', 1)))):
                self.reference_content_array_longref.append(
                    float(reference_source_dict['wavelength_min'].replace(',', '.', 1)) +
                    float(reference_source_dict['wavelength_step'].replace(',', '.', 1)) * i)
        # reference width & top source
        if reference_source_dict['width_top_source'] != '':
            l_index = 0
            if reference_source_dict['width_top_separator'] != '':
                for line in reference_source_dict['width_top_source'].splitlines():
                    l_index = l_index + 1
                    if l_index >= reference_source_dict['ligne_debut_width_top']:
                        self.FWHM_array.append(float(
                            line.split(reference_source_dict['width_top_separator'])
                            [reference_source_dict['width_column_number'] - 1].strip().replace(',', '.', 1)))
                        if reference_source_dict['function_type'] == 'Trapeze':
                            self.FWM_array.append(float(
                                line.split(reference_source_dict['width_top_separator'])
                                [reference_source_dict['top_column_number'] - 1].strip().replace(',', '.', 1)))
            else:
                for line in reference_source_dict['width_top_source'].splitlines():
                    l_index = l_index + 1
                    if l_index >= reference_source_dict['ligne_debut_width_top']:
                        self.FWHM_array.append(float(line.strip().replace(',', '.', 1)))
        elif reference_source_dict['width_const'] != '':
            self.FWHM_array.append(float(reference_source_dict['width_const'].replace(',', '.', 1)))
            if reference_source_dict['function_type'] == 'Trapeze':
                self.FWM_array.append(float(reference_source_dict['top_const'].replace(',', '.', 1)))
        else:
            for i in range(len(self.reference_content_array_longref)):
                self.FWHM_array.append(
                    float(reference_source_dict['width_min'].replace(',', '.', 1)) +
                    i * (float(reference_source_dict['width_max'].replace(',', '.', 1)) -
                         float(reference_source_dict['width_min'].replace(',', '.', 1)))
                    / len(self.reference_content_array_longref))
            if reference_source_dict['function_type'] == 'Trapeze':
                for i in range(len(self.reference_content_array_longref)):
                    self.FWM_array.append(
                        float(reference_source_dict['top_min'].replace(',', '.', 1)) +
                        i * (float(reference_source_dict['top_max'].replace(',', '.', 1)) -
                             float(reference_source_dict['top_min'].replace(',', '.', 1)))
                        / len(self.reference_content_array_longref))
        # CHANGEMENT des unités si besoin
        if deresoudre_source_dict['fichier_a_deresoudre_unit'] != reference_source_dict['fichier_a_reference_unit']:
            for i in range(len(self.deresoudre_content_array_long)):
                self.deresoudre_content_array_long[i] = changement_units(
                    self.deresoudre_content_array_long[i],
                    deresoudre_source_dict['fichier_a_deresoudre_unit'],
                    reference_source_dict['fichier_a_reference_unit'])
        # RENVERSE si besoin
        if self.reference_content_array_longref[1] - self.reference_content_array_longref[0] < 0:
            self.reference_content_array_longref.reverse()
            self.FWM_array.reverse()
            self.FWHM_array.reverse()
            self.reference_data_order = 0
        else:
            self.reference_data_order = 1
        if self.deresoudre_content_array_long[1] - self.deresoudre_content_array_long[0] < 0:
            self.deresoudre_content_array_long.reverse()
            self.deresoudre_content_array_refh.reverse()


    def verification_data(self):
        if deresoudre_source_dict['deresoudre_data_set_up'] != 'OK':
            self.dialog_critical('No data for the spectrum to convolve has been found.\nPlease specify')
            self.ui.btn_1.setFocus()
        elif reference_source_dict['reference_data_set_up'] != 'OK':
            self.dialog_critical('No convolution parameter was found\nPlease specify')
            self.ui.btn_2.setFocus()
        else:
            try:
                self.reading_data()
                self.dialog_progress_verif("Test in progress...", "Abort", 0, len(self.reference_content_array_longref))
                if self.answer != 'The following issues were found:':
                    self.dialog_critical(self.answer)
                else:
                    self.dialog_ok('The data is Ok for the convolution!')
            except Exception as e:
                win.dialog_critical(f'Critical error while testing data: {str(e)}.'
                                    f'\nPlease check the spectrum and destination sources.'
                                    f'\nPossible issues:'
                                    f'\n- incorrect unit;'
                                    f'\n- incorrect order in start, end and step values for '
                                    f'the generated destination wavelength and / or width (top).')

    def convolution_calc(self):
        if deresoudre_source_dict['deresoudre_data_set_up'] != 'OK':
            self.dialog_critical('No data for the spectrum to convolve has been found.\nPlease specify')
            self.ui.btn_1.setFocus()
        elif reference_source_dict['reference_data_set_up'] != 'OK':
            self.dialog_critical('No convolution parameter has been found\nPlease specify')
            self.ui.btn_2.setFocus()
        else:
            verification_wavelength_width_ok = 1
            if len(self.reference_content_array_longref) != len(self.FWHM_array) and len(self.FWHM_array) != 1:
                verification_wavelength_width_ok = 0
            # reference width & top are the same length
            verification_width_top_len_ok = 1
            if reference_source_dict['function_type'] == 'Trapeze':
                if len(self.FWHM_array) != len(self.FWM_array):
                    verification_width_top_len_ok = 0
            if not verification_wavelength_width_ok:
                self.dialog_critical('The width set has not the same length than the destination wavelength set')
            elif not verification_width_top_len_ok:
                self.dialog_critical('The width set has not the same length than the top set')
            else:
                try:
                    self.dialog_progress_calc("calculation in progress...", "Abort", 0,
                                              len(self.reference_content_array_longref))
                    if not self.convolution_not_finished:
                        data_changed_dict['current_data_changed'] = 3
                        if not self.reference_data_order:
                            self.drefh.reverse()
                        self.dialog_ok('The convolution calculation is successfully completed!\n'
                                       'You can save and/or plot the result')
                except Exception as e:
                    self.dialog_critical(f'Critical error while calculating the convolution: {str(e)}'
                                         f'\nPlease check the spectrum and destination sources.'
                                         f'\nPossible issues:'
                                         f'\n- incorrect unit;'
                                         f'\n- incorrect order in start, end and step values for '
                                         f'the generated destination wavelength and / or width (top).')

    def plot_data(self):
        if deresoudre_source_dict['deresoudre_data_set_up'] != 'OK':
            self.dialog_critical('No data for the spectrum to convolve has been found.\nPlease specify')
            self.ui.btn_1.setFocus()
        elif reference_source_dict['reference_data_set_up'] != 'OK':
            self.dialog_critical('No convolution parameter has been found\nPlease specify')
            self.ui.btn_2.setFocus()
        elif self.convolution_not_finished:
            self.dialog_critical('Nothing to plot!\nPlease, run convolution before plotting it')
            self.ui.btn_4.setFocus()
        else:
            if self.drefh == [] or data_changed_dict['current_data_changed'] == -1:
                self.dialog_critical('Nothing to plot!\nPlease, run convolution before plotting it')
            elif data_changed_dict['current_data_changed'] == 0:
                reply = QMessageBox.question(self, 'Message',
                                             "Some parameters of the spectrum to convolve have been modified "
                                             "but no new convolution calculation has been performed."
                                             "\nDo you want to plot the result of PREVIOUS calculation?",
                                             QMessageBox.Yes |
                                             QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    self.plot_f()
            elif data_changed_dict['current_data_changed'] == 1:
                reply = QMessageBox.question(self, 'Message',
                                             "Some parameters of the convolution function "
                                             "or the destination wavelengths have been modified "
                                             "but no new convolution calculation has been performed."
                                             "\nDo you want to plot the result of PREVIOUS calculation?",
                                             QMessageBox.Yes |
                                             QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    self.plot_f()
            else:
                self.plot_f()

    def plot_f(self):
        try:
            plot_reference_content_array_longref = self.reference_content_array_longref[:]
            plot_deresoudre_content_array_long = []
            plot_deresoudre_content_array_refh = []
            min_long = self.reference_content_array_longref[0] * (1 - 0.15)
            max_long = self.reference_content_array_longref[len(self.reference_content_array_longref) - 1] * (1 + 0.15)
            for i in range(len(self.deresoudre_content_array_long)):
                if min_long <= self.deresoudre_content_array_long[i] <= max_long:
                    plot_deresoudre_content_array_long.append(self.deresoudre_content_array_long[i])
                    plot_deresoudre_content_array_refh.append(self.deresoudre_content_array_refh[i])
                elif self.deresoudre_content_array_long[i] > max_long:
                    break
            if not self.reference_data_order:
                plot_deresoudre_content_array_long.reverse()
                plot_deresoudre_content_array_refh.reverse()
                plot_reference_content_array_longref.reverse()
            plt.figure('Convolution plot')
            plt.title(f'Convolution of {deresoudre_source_dict["deresoudre_file_name"]}')
            plt.xlabel(f'wavelength ({reference_source_dict["fichier_a_reference_unit"]})')
            plt.ylabel('intensity')
            if plot_deresoudre_content_array_long:
                if self.reference_data_order:
                    plt.xlim(0.95 * plot_deresoudre_content_array_long[0],
                             1.05 * plot_deresoudre_content_array_long[len(plot_deresoudre_content_array_long) - 1])
                else:
                    plt.xlim(1.05 * plot_deresoudre_content_array_long[0],
                             0.95 * plot_deresoudre_content_array_long[len(plot_deresoudre_content_array_long) - 1])
                plt.plot(plot_deresoudre_content_array_long, plot_deresoudre_content_array_refh, label='initial spectrum')
            plt.plot(plot_reference_content_array_longref, self.drefh, label='convolution')
            plt.legend()
            plt.show()
        except Exception as e:
            self.dialog_critical(f'Critical error while plotting: {str(e)}.')


    def download_file(self):
        if deresoudre_source_dict['deresoudre_data_set_up'] != 'OK':
            self.dialog_critical('No data for the spectrum to convolve has been found.\nPlease specify')
            self.ui.btn_1.setFocus()
        elif reference_source_dict['reference_data_set_up'] != 'OK':
            self.dialog_critical('No convolution parameter has been found\nPlease specify')
            self.ui.btn_2.setFocus()
        elif self.convolution_not_finished:
            self.dialog_critical('Nothing to save!\nPlease, run the convolution before to save it')
            self.ui.btn_4.setFocus()
        else:
            if self.drefh == [] or data_changed_dict['current_data_changed'] == -1:
                self.dialog_critical('Nothing to save!\nPlease, run convolution before saving it')
            elif data_changed_dict['current_data_changed'] == 0:
                reply = QMessageBox.question(self, 'Message',
                                             "Some parameters of the spectrum to convolve have been modified "
                                             "but no new convolution calculation has been performed."
                                             "\nDo you want to save the result of PREVIOUS calculation?",
                                             QMessageBox.Yes |
                                             QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    self.file_save_f()
            elif data_changed_dict['current_data_changed'] == 1:
                reply = QMessageBox.question(self, 'Message',
                                             "Some parameters of the convolution function "
                                             "or the destination wavelengths have been modified "
                                             "but no new convolution calculation has been performed."
                                             "\nDo you want to save the result of PREVIOUS calculation?",
                                             QMessageBox.Yes |
                                             QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    self.file_save_f()
            else:
                self.file_save_f()

    def file_save_f(self):
        options = QFileDialog.Options()
        end_value = deresoudre_source_dict['deresoudre_file_name'].rfind('.')
        conv_file_name = deresoudre_source_dict['deresoudre_file_name'][0:end_value] + "_conv.txt"
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", conv_file_name,
                                                   "Text Files (*.txt)", options=options)
        if file_name:
            if format_output_dict['title'] == 'with':
                str_result = f'wavelength({reference_source_dict["fichier_a_reference_unit"]})' + \
                             format_output_dict['separator'] + 'intensity\n'
            else:
                str_result = ''
            reference_content_array_longref_copy = self.reference_content_array_longref[:]
            drefh_copy = self.drefh[:]
            if format_output_dict['order'] == 0:
                reference_content_array_longref_copy.reverse()
                if self.reference_data_order == 1:
                    drefh_copy.reverse()
            elif self.reference_data_order == 0:
                drefh_copy.reverse()
            for i in range(len(drefh_copy)):
                if format_output_dict['wlth_format'] == 'exponential':
                    wavelength_str = self.f_string_generator_e(reference_content_array_longref_copy[i],
                                                               format_output_dict['decimals_wavelength'])
                else:
                    wavelength_str = self.f_string_generator_d(reference_content_array_longref_copy[i],
                                                               format_output_dict['decimals_wavelength'])
                if format_output_dict['intens_format'] == 'exponential':
                    intensity_str = self.f_string_generator_e(drefh_copy[i],
                                                              format_output_dict['decimals_intencity'])
                else:
                    intensity_str = self.f_string_generator_d(drefh_copy[i],
                                                              format_output_dict['decimals_intencity'])
                str_result = str_result + wavelength_str + format_output_dict['separator'] + intensity_str + '\n'
            with open(file_name, 'w+') as file_output:
                file_output.write(str_result)

    def f_string_generator_e(self, value_format, qqty_digits):
        if qqty_digits == 0:
            return f'{value_format:.0e}'
        elif qqty_digits == 1:
            return f'{value_format:.1e}'
        elif qqty_digits == 2:
            return f'{value_format:.2e}'
        elif qqty_digits == 3:
            return f'{value_format:.3e}'
        elif qqty_digits == 4:
            return f'{value_format:.4e}'
        elif qqty_digits == 5:
            return f'{value_format:.5e}'
        elif qqty_digits == 6:
            return f'{value_format:.6e}'
        elif qqty_digits == 7:
            return f'{value_format:.7e}'
        elif qqty_digits == 8:
            return f'{value_format:.8e}'
        elif qqty_digits == 9:
            return f'{value_format:.9e}'
        elif qqty_digits == 10:
            return f'{value_format:.10e}'
        elif qqty_digits == 11:
            return f'{value_format:.11e}'
        elif qqty_digits == 12:
            return f'{value_format:.12e}'
        elif qqty_digits == 13:
            return f'{value_format:.13e}'
        elif qqty_digits == 14:
            return f'{value_format:.14e}'
        elif qqty_digits == 15:
            return f'{value_format:.15e}'
        else:
            return f'{value_format:.16e}'

    def f_string_generator_d(self, value_format, qqty_digits):
        if qqty_digits == 0:
            return f'{value_format:.0f}'
        elif qqty_digits == 1:
            return f'{value_format:.1f}'
        elif qqty_digits == 2:
            return f'{value_format:.2f}'
        elif qqty_digits == 3:
            return f'{value_format:.3f}'
        elif qqty_digits == 4:
            return f'{value_format:.4f}'
        elif qqty_digits == 5:
            return f'{value_format:.5f}'
        elif qqty_digits == 6:
            return f'{value_format:.6f}'
        elif qqty_digits == 7:
            return f'{value_format:.7f}'
        elif qqty_digits == 8:
            return f'{value_format:.8f}'
        elif qqty_digits == 9:
            return f'{value_format:.9f}'
        elif qqty_digits == 10:
            return f'{value_format:.10f}'
        elif qqty_digits == 11:
            return f'{value_format:.11f}'
        elif qqty_digits == 12:
            return f'{value_format:.12f}'
        elif qqty_digits == 13:
            return f'{value_format:.13f}'
        elif qqty_digits == 14:
            return f'{value_format:.14f}'
        elif qqty_digits == 15:
            return f'{value_format:.15f}'
        else:
            return f'{value_format:.16f}'


class ReferenceSourceW(QtWidgets.QDialog):
    def __init__(self):
        super(ReferenceSourceW, self).__init__()
        self.ui = Ui_ReferenceDialog()
        self.ui.setupUi(self)
        # class globals
        self.close_source = ''
        self.reference_source = reference_source_dict['reference_source']
        self.reference_source_file_name = reference_source_dict['reference_source_file_name']
        self.width_top_source = reference_source_dict['width_top_source']
        self.width_top_source_file_name = reference_source_dict['width_top_source_file_name']
        # GUI beauties
        # GUI beauties: no border for GroupBox
        self.ui.groupBox_2.setStyleSheet("border:0;")
        self.ui.groupBox_c.setStyleSheet("border:0;")
        # GUI beauties: convolution function
        if reference_source_dict['function_source'] == '':
            if reference_source_dict['function_type'] == 'Trapeze':
                self.ui.rbtn_Trapeze.setChecked(True)
            elif reference_source_dict['function_type'] == 'Triangle':
                self.ui.rbtn_Triangle.setChecked(True)
            else:
                self.ui.rbtn_Gaussian.setChecked(True)
        else:
            self.ui.rbtn_Gaussian.setAutoExclusive(False)
            self.ui.rbtn_Gaussian.setChecked(False)
            self.ui.rbtn_Gaussian.setAutoExclusive(True)
            self.ui.rbtn_Triangle.setAutoExclusive(False)
            self.ui.rbtn_Triangle.setChecked(False)
            self.ui.rbtn_Triangle.setAutoExclusive(True)
            self.ui.rbtn_Trapeze.setAutoExclusive(False)
            self.ui.rbtn_Trapeze.setChecked(False)
            self.ui.rbtn_Trapeze.setAutoExclusive(True)
        # GUI beauties: reference wavelength
        fmt = QTextCharFormat()
        fmt.setBackground(QBrush(Qt.yellow))
        self.ui.tabWidget.setCurrentIndex(reference_source_dict['tabWidget_activa_tab'])
        self.ui.wl_separator.mergeCurrentCharFormat(fmt)
        if reference_source_dict['reference_source'] != '':
            self.ui.label_wl_file.setText(reference_source_dict['reference_source_file_name'])
            self.ui.wl_min.setText('')
            self.ui.wl_max.setText('')
            self.ui.wl_step.setText('')
            self.ui.wl_start.setValue(reference_source_dict['ligne_debut_reference'])
            self.ui.wl_column.setValue(reference_source_dict['long_column_number'])
            self.ui.wl_separator.setPlainText(reference_source_dict['reference_wavelength_separator'])
        else:
            self.ui.label_wl_file.setText('no file selected')
            self.ui.wl_min.setText(reference_source_dict['wavelength_min'])
            self.ui.wl_max.setText(reference_source_dict['wavelength_max'])
            self.ui.wl_step.setText(reference_source_dict['wavelength_step'])
            self.ui.wl_start.setValue(1)
            self.ui.wl_column.setValue(1)
            self.ui.wl_separator.setPlainText('\t')
        # GUI beauties: units
        self.ui.cm_label.setText('cm<sup>-1</sup>')
        self.ui.cm_label.setStyleSheet('QLabel{padding-left: -1px;}')
        self.ui.btn_cm.setStyleSheet('QRadioButton{margin-right: -6px;}')
        if reference_source_dict['fichier_a_reference_unit'] == 'A':
            self.ui.rbtn_A.setChecked(True)
        elif reference_source_dict['fichier_a_reference_unit'] == 'micron':
            self.ui.rbtn_micron.setChecked(True)
        elif reference_source_dict['fichier_a_reference_unit'] == 'nm':
            self.ui.rbtn_nm.setChecked(True)
        else:
            self.ui.btn_cm.setChecked(True)
        # GUI beauties: width
        fmt = QTextCharFormat()
        fmt.setBackground(QBrush(Qt.yellow))
        self.ui.tabWidget_2.setCurrentIndex(reference_source_dict['tabWidget_2_activa_tab'])
        self.ui.wth_separator.mergeCurrentCharFormat(fmt)
        if reference_source_dict['width_top_source'] != '':
            self.ui.label_wth_file.setText(reference_source_dict['width_top_source_file_name'])
            self.ui.wth_constant.setText('')
            self.ui.top_const.setText('')
            self.ui.top_min.setText('')
            self.ui.top_max.setText('')
            self.ui.wth_min.setText('')
            self.ui.wth_max.setText('')
            self.ui.wth_start.setValue(reference_source_dict['ligne_debut_width_top'])
            self.ui.wth_column.setValue(reference_source_dict['width_column_number'])
            self.ui.top_column.setValue(reference_source_dict['top_column_number'])
            self.ui.wth_separator.setPlainText(reference_source_dict['width_top_separator'])
        elif reference_source_dict['width_const'] != '':
            self.ui.label_wth_file.setText('no file selected')
            self.ui.wth_constant.setText(reference_source_dict['width_const'])
            self.ui.top_const.setText(reference_source_dict['top_const'])
            self.ui.top_min.setText('')
            self.ui.top_max.setText('')
            self.ui.wth_min.setText('')
            self.ui.wth_max.setText('')
            self.ui.wth_start.setValue(1)
            self.ui.wth_column.setValue(2)
            self.ui.top_column.setValue(3)
            self.ui.wth_separator.setPlainText('\t')
        else:
            self.ui.label_wth_file.setText('no file selected')
            self.ui.wth_constant.setText('')
            self.ui.top_const.setText('')
            self.ui.top_min.setText(reference_source_dict['top_min'])
            self.ui.top_max.setText(reference_source_dict['top_max'])
            self.ui.wth_min.setText(reference_source_dict['width_min'])
            self.ui.wth_max.setText(reference_source_dict['width_max'])
            self.ui.wth_start.setValue(1)
            self.ui.wth_column.setValue(2)
            self.ui.top_column.setValue(3)
            self.ui.wth_separator.setPlainText('\t')
        # GUI beauties: hide/show top
        if reference_source_dict['function_type'] == 'Trapeze':
            self.ui.top_const.setVisible(True)
            self.ui.label_20.setVisible(True)
            self.ui.top_column.setVisible(True)
            self.ui.label_22.setVisible(True)
            self.ui.top_min.setVisible(True)
            self.ui.label_23.setVisible(True)
            self.ui.top_max.setVisible(True)
            self.ui.label_24.setVisible(True)
        else:
            self.ui.top_const.setVisible(False)
            self.ui.label_20.setVisible(False)
            self.ui.top_column.setVisible(False)
            self.ui.label_22.setVisible(False)
            self.ui.top_min.setVisible(False)
            self.ui.label_23.setVisible(False)
            self.ui.top_max.setVisible(False)
            self.ui.label_24.setVisible(False)
        # GYI beauties: buttons
        self.ui.btn_upload_wl.setStyleSheet('QPushButton{padding: 15px;}')
        self.ui.btn_upload_wth.setStyleSheet('QPushButton{padding: 15px;}')
        self.ui.btn_save.setStyleSheet('QPushButton{padding: 15px;}')
        self.ui.btn_clear.setStyleSheet('QPushButton{padding: 15px;}')
        self.ui.btn_close.setStyleSheet('QPushButton{padding: 15px;}')
        # SIGNALS & SLOTS
        self.ui.cm_label.mousePressEvent = self.cm_enable
        self.ui.rbtn_Gaussian.toggled.connect(self.clear_selected_function_file)
        self.ui.rbtn_Triangle.toggled.connect(self.clear_selected_function_file)
        self.ui.rbtn_Trapeze.toggled.connect(self.clear_selected_function_file)
        self.ui.btn_upload_wl.clicked.connect(self.wl_from_file)
        self.ui.del_wl_file.clicked.connect(self.clear_selected_wl_file)
        self.ui.btn_upload_wth.clicked.connect(self.wth_from_file)
        self.ui.del_wth_file.clicked.connect(self.clear_selected_wth_file)
        self.ui.btn_save.clicked.connect(self.save_data_function)
        self.ui.btn_clear.clicked.connect(self.clear_form_function)
        self.ui.btn_close.clicked.connect(self.close_form_function)
        self.ui.wl_separator.textChanged.connect(self.set_yellow_text_wl_separator)
        self.ui.wth_separator.textChanged.connect(self.set_yellow_text_wth_separator)
        # WINDOW SHOW
        if __name__ == '__main__':
            self.setWindowModality(Qt.ApplicationModal)
            self.show()
            self.exec_()

    def closeEvent(self, event):
        if self.close_source == 'save':
            self.close()
        else:
            reply = QMessageBox.question(self, 'Message',
                                         "Are you sure you want to close this window?\nAny change will be lost",
                                         QMessageBox.Yes |
                                         QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.close()
            else:
                event.ignore()

    def cm_enable(self, event):
        self.ui.btn_cm.setChecked(True)

    def set_yellow_text_wl_separator(self):
        set_yellow_text(self.ui.wl_separator)

    def set_yellow_text_wth_separator(self):
        set_yellow_text(self.ui.wth_separator)

    def clear_selected_function_file(self):
        if self.ui.rbtn_Gaussian.isChecked() or self.ui.rbtn_Triangle.isChecked() or self.ui.rbtn_Trapeze.isChecked():
            reference_source_dict['function_source'] = ''
            reference_source_dict['function_source_file_name'] = ''
        if self.ui.rbtn_Trapeze.isChecked():
            self.ui.top_const.setVisible(True)
            self.ui.label_20.setVisible(True)
            self.ui.top_column.setVisible(True)
            self.ui.label_22.setVisible(True)
            self.ui.top_min.setVisible(True)
            self.ui.label_23.setVisible(True)
            self.ui.top_max.setVisible(True)
            self.ui.label_24.setVisible(True)
        else:
            self.ui.top_const.setVisible(False)
            self.ui.label_20.setVisible(False)
            self.ui.top_column.setVisible(False)
            self.ui.label_22.setVisible(False)
            self.ui.top_min.setVisible(False)
            self.ui.label_23.setVisible(False)
            self.ui.top_max.setVisible(False)
            self.ui.label_24.setVisible(False)

    def wl_from_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Choose file with destination data", "",
                                              "Text documents (*.txt *.csv *tsv);;All files (*.*)")
        if path:
            try:
                with open(path, 'r') as f:
                    self.reference_source = f.read()
                    if path.rfind("/") != -1:
                        self.reference_source_file_name = path[path.rfind("/") + 1:]
                    else:
                        self.reference_source_file_name = path[path.rfind("\\") + 1:]
                    self.ui.label_wl_file.setText(self.reference_source_file_name)
            except Exception as e:
                self.dialog_critical(f'Critical error while opening file: {str(e)}.'
                                     f'\nThis file is corrupted or it is not a text document')

    def clear_selected_wl_file(self):
        if self.reference_source != '':
            reply = QMessageBox.question(self, 'Message',
                                         "Are you sure you want to remove the selected file?",
                                         QMessageBox.Yes |
                                         QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.reference_source = ""
                self.reference_source_file_name = ""
                self.ui.label_wl_file.setText('no file selected')

    def wth_from_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Choose file with destination data", "",
                                              "Text documents (*.txt *.csv *tsv);;All files (*.*)")
        if path:
            try:
                with open(path, 'r') as f:
                    self.width_top_source = f.read()
                    if path.rfind("/") != -1:
                        self.width_top_source_file_name = path[path.rfind("/") + 1:]
                    else:
                        self.width_top_source_file_name = path[path.rfind("\\") + 1:]
                    self.ui.label_wth_file.setText(self.width_top_source_file_name)
            except Exception as e:
                self.dialog_critical(f'Critical error while opening file: {str(e)}.'
                                     f'\nThis file is corrupted or it is not a text document')

    def clear_selected_wth_file(self):
        if self.width_top_source != '':
            reply = QMessageBox.question(self, 'Message',
                                         "Are you sure you want to remove the selected file?",
                                         QMessageBox.Yes |
                                         QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.width_top_source = ""
                self.width_top_source_file_name = ""
                self.ui.label_wth_file.setText('no file selected')

    def save_data_function(self):
        verification_ok = 0
        # verifications: wavelenth
        if self.reference_source == '' and self.ui.wl_min.text() == '':
            self.ui.tabWidget.setCurrentIndex(0)
            self.ui.btn_upload_wl.setFocus()
            self.dialog_critical(
                'Data for the destination wavelengths is mandatory!\n'
                'Please, either choose a non-empty file or specify min, max and step values to generate it')
        elif self.reference_source != '' and (self.ui.wl_min.text() != '' or self.ui.wl_max.text() != ''
                                                                  or self.ui.wl_step.text() != ''):
            self.ui.tabWidget.setCurrentIndex(0)
            self.ui.btn_upload_wl.setFocus()
            self.dialog_critical(
                'You have to choose only one source between "Upload from file" or "Generate"!\n'
                'Please, delete the unnecessary data source')
        elif self.reference_source == '' and not self.ui.wl_min.text().strip().replace(',', '.', 1)\
                .replace('.', '', 1).isdecimal():
            self.ui.tabWidget.setCurrentIndex(1)
            self.ui.wl_min.setFocus()
            self.dialog_critical(
                'The minimum wavelength value must be a positive number!\nPlease, enter an appropriate numerical value')
        elif self.reference_source == '' and not self.ui.wl_max.text().strip().replace(',', '.', 1)\
                .replace('.', '', 1).isdecimal():
            self.ui.tabWidget.setCurrentIndex(1)
            self.ui.wl_max.setFocus()
            self.dialog_critical(
                'The maximum wavelength value must be a positive number!\nPlease, enter an appropriate numerical value')
        elif self.reference_source == '' and (not self.ui.wl_step.text().strip().replace(',', '.', 1).\
                replace('.', '', 1).replace('-', '', 1).isdecimal() or self.ui.wl_step.text().strip() == "0"):
            self.ui.tabWidget.setCurrentIndex(1)
            self.ui.wl_step.setFocus()
            self.dialog_critical(
                'The step wavelength value must be a non-zero number!\nPlease, enter an appropriate numerical value')
        elif self.reference_source != '' and self.ui.wl_separator.toPlainText() not in \
                self.reference_source:
            self.ui.tabWidget.setCurrentIndex(0)
            self.ui.wl_separator.setFocus()
            self.dialog_critical(
                'Cannot find this separator in the destination wavelength file!\nPlease, enter an appropriate value')
        elif self.reference_source != '' and self.ui.wl_separator.toPlainText() == '' \
                and self.ui.wl_column.value() != 1:
            self.ui.tabWidget.setCurrentIndex(0)
            self.ui.wl_separator.setFocus()
            self.dialog_critical(
                'For a file with several columns a separator is mandatory!\nPlease, enter an appropriate value')
        # verifications: width
        elif self.width_top_source == '' and self.ui.wth_constant.text() == '' \
                and self.ui.wth_min.text() == '' and self.ui.wth_max.text() == '':
            self.ui.tabWidget_2.setCurrentIndex(0)
            self.ui.btn_upload_wth.setFocus()
            self.dialog_critical(
                'Data for the destination width is mandatory!\n'
                'Please, choose either a constant value, or a non-empty file providing it, '
                'or specify min and max values to generate it')
        elif (self.width_top_source != '' and self.ui.wth_constant.text() != '') \
                or (self.width_top_source != '' and
                    (self.ui.wth_min.text() != '' or self.ui.wth_max.text() != '')) \
                or (self.ui.wth_constant.text() != '' and (self.ui.wth_min.text() != '' or self.ui.wth_max.text() != '')):
            self.ui.tabWidget_2.setCurrentIndex(0)
            self.ui.btn_upload_wth.setFocus()
            self.dialog_critical(
                'You have to choose only one source of width among "Upload from file", "Generate" or "Constant"!\n'
                'Please, delete all unnecessary data sources')
        elif self.width_top_source == '' and self.ui.wth_constant.text() != '' \
                and (not self.ui.wth_constant.text().strip().replace(',', '.', 1).replace('.', '', 1).isdecimal() or
                     self.ui.wth_constant.text().strip() == "0"):
            self.ui.tabWidget_2.setCurrentIndex(2)
            self.ui.wth_constant.setFocus()
            self.dialog_critical(
                'The width value must be a positive number!\nPlease, enter an appropriate numerical value')
        elif self.width_top_source == '' and self.ui.wth_constant.text() == ''\
                and self.ui.wth_max.text() != '' and self.ui.wth_min.text() == '':
            self.ui.tabWidget_2.setCurrentIndex(1)
            self.ui.wth_min.setFocus()
            self.dialog_critical(
                'The minimum width value is mandatory!\nPlease, enter an appropriate value')
        elif self.width_top_source == '' and self.ui.wth_constant.text() == ''\
                and self.ui.wth_max.text() == '' and self.ui.wth_min.text() != '':
            self.ui.tabWidget_2.setCurrentIndex(1)
            self.ui.wth_min.setFocus()
            self.dialog_critical(
                'The maximum width value is mandatory!\nPlease, enter an appropriate value')
        elif reference_source_dict[
            'width_top_source'] == '' and self.ui.wth_min.text() != '' and not self.ui.wth_min.text().strip()\
                .replace(',', '.', 1).replace('.', '', 1).isdecimal():
            self.ui.tabWidget_2.setCurrentIndex(1)
            self.ui.wth_min.setFocus()
            self.dialog_critical(
                'The minimum width value must be a positive number!\nPlease, enter an appropriate numerical value')
        elif reference_source_dict[
            'width_top_source'] == '' and self.ui.wth_max.text() != '' and not self.ui.wth_max.text().strip()\
                .replace(',', '.', 1).replace('.', '', 1).isdecimal():
            self.ui.tabWidget_2.setCurrentIndex(1)
            self.ui.wth_max.setFocus()
            self.dialog_critical(
                'The maximum width value must be a positive number!\nPlease, enter an appropriate numerical value')
        elif self.width_top_source != '' and self.ui.wth_separator.toPlainText() not in \
                self.width_top_source:
            self.ui.tabWidget_2.setCurrentIndex(0)
            self.ui.wth_separator.setFocus()
            self.dialog_critical(
                'Cannot find this separator in the destination width file!\nPlease, enter an appropriate value')
        elif self.width_top_source != '' and self.ui.wth_separator.toPlainText() == '' \
                and self.ui.wth_column.value() != 1:
            self.ui.tabWidget_2.setCurrentIndex(0)
            self.ui.wth_separator.setFocus()
            self.dialog_critical(
                'For a file with several columns a separator is mandatory!\nPlease, enter an appropriate value')
        # verifications: top
        elif self.ui.rbtn_Trapeze.isChecked():
            if self.width_top_source == '' and self.ui.top_const.text() == '' \
                    and self.ui.top_min.text() == '' and self.ui.top_max.text() == '':
                self.ui.tabWidget_2.setCurrentIndex(0)
                self.ui.btn_upload_wth.setFocus()
                self.dialog_critical(
                    'Data for the top base is mandatory in case of Trapeze function!\n'
                    'Please, choose either a constant value, or a non-empty file providing it, '
                    'or specify min and max values to generate it')
            elif (self.width_top_source != '' and self.ui.top_const.text() != '') \
                    or (self.width_top_source != '' and
                        (self.ui.top_min.text() != '' or self.ui.top_max.text() != '')) \
                    or (self.ui.top_const.text() != '' and (self.ui.top_min.text() != '' or self.ui.top_max.text() != '')):
                self.ui.tabWidget_2.setCurrentIndex(0)
                self.ui.btn_upload_wth.setFocus()
                self.dialog_critical(
                    'You have to choose only one source of top among "Constant", "Upload from a file" or "Generate"!'
                    '\nPlease, delete all unnecessary data sources')
            elif self.width_top_source == '' and self.ui.top_const.text() == '' \
                    and self.ui.top_min.text() != '' and self.ui.top_max.text() == '':
                self.ui.tabWidget_2.setCurrentIndex(1)
                self.ui.top_const.setFocus()
                self.dialog_critical('The max top value is mandatory!\nPlease, enter an appropriate value')
            elif self.width_top_source == '' and self.ui.top_const.text() == '' \
                    and self.ui.top_min.text() == '' and self.ui.top_max.text() != '':
                self.ui.tabWidget_2.setCurrentIndex(1)
                self.ui.top_const.setFocus()
                self.dialog_critical('The min top value is mandatory!\nPlease, enter an appropriate value')
            elif self.width_top_source == '' and self.ui.top_const.text() != '' \
                    and (not self.ui.top_const.text().strip().replace(',', '.', 1).replace('.', '', 1).isdecimal() or
                         self.ui.top_const.text().strip() == "0"):
                self.ui.tabWidget_2.setCurrentIndex(2)
                self.ui.top_const.setFocus()
                self.dialog_critical('The top value must be a positive number!\nPlease, enter an appropriate numerical value')
            elif self.width_top_source == '' and self.ui.top_min.text() != '' \
                    and not self.ui.top_min.text().strip().replace(',', '.', 1).replace('.', '', 1).isdecimal():
                self.ui.tabWidget_2.setCurrentIndex(1)
                self.ui.top_min.setFocus()
                self.dialog_critical(
                    'The minimum top value must be a positive number!\nPlease, enter an appropriate numerical value')
            elif self.width_top_source == '' and self.ui.top_max.text() != '' \
                    and not self.ui.top_max.text().strip().replace(',', '.', 1).replace('.', '', 1).isdecimal():
                self.ui.tabWidget_2.setCurrentIndex(1)
                self.ui.top_max.setFocus()
                self.dialog_critical(
                    'The maximum top value must be a positive number!\nPlease, enter an appropriate numerical value')
            elif self.ui.wth_constant.text() != '' and self.ui.top_const.text() != '' \
                    and float(self.ui.wth_constant.text().strip().replace(',', '.', 1)) < \
                    float(self.ui.top_const.text().strip().replace(',', '.', 1)):
                self.ui.tabWidget_2.setCurrentIndex(2)
                self.ui.wth_constant.setFocus()
                self.dialog_critical(
                    'The top value must be smaller than the width value!\nPlease, enter an appropriate value')
            elif self.ui.top_min.text() != '' and self.ui.wth_min.text() != '' \
                    and float(self.ui.top_min.text().strip().replace(',', '.', 1)) > \
                    float(self.ui.wth_min.text().strip().replace(',', '.', 1)):
                self.ui.tabWidget_2.setCurrentIndex(1)
                self.ui.top_min.setFocus()
                self.dialog_critical(
                    'The min top value must be smaller than the min width value!'
                    '\nPlease, enter an appropriate value')
            elif self.ui.top_max.text() != '' and self.ui.wth_max.text() != '' \
                    and float(self.ui.top_max.text().strip().replace(',', '.', 1)) > \
                    float(self.ui.wth_max.text().strip().replace(',', '.', 1)):
                self.ui.tabWidget_2.setCurrentIndex(1)
                self.ui.top_max.setFocus()
                self.dialog_critical(
                    'The max top value must be smaller than the max width value!'
                    '\nPlease, enter an appropriate value')
            elif self.width_top_source != '' and self.ui.wth_separator.toPlainText() == '':
                self.ui.tabWidget_2.setCurrentIndex(0)
                self.ui.wth_separator.setFocus()
                self.dialog_critical(
                    'For a file with several columns a separator is mandatory!\nPlease, enter an appropriate value')
            else:
                verification_wl = 0
                try:
                    if self.reference_source != '':
                        l_index = 0
                        if self.ui.wl_separator.toPlainText() != '':
                            for line in self.reference_source.splitlines():
                                l_index = l_index + 1
                                if l_index >= self.ui.wl_start.value():
                                    x = float(line.split(self.ui.wl_separator.toPlainText())
                                              [self.ui.wl_column.value() - 1].strip().replace(',', '.', 1))
                        else:
                            for line in self.reference_source.splitlines():
                                l_index = l_index + 1
                                if l_index >= self.ui.wl_start.value():
                                    x = float(line.strip().replace(',', '.', 1))
                    verification_wl = 1
                except Exception as e:
                    self.dialog_critical(
                        f'Critical error while reading the file with destination wavelength data: {str(e)}.'
                        f'\nPlease, verify the starting line and the number of the column'
                        f'\nin which each parameter is stored in the file.'
                        f'\nOther possible issue: there is text or other non-numerical type in the file,'
                        f'or separator info is missing.')
                verification_wdth_top = 0
                try:
                    # reference width & top source
                    if self.width_top_source != '':
                        l_index = 0
                        if self.ui.wth_separator.toPlainText() != '':
                            for line in self.width_top_source.splitlines():
                                l_index = l_index + 1
                                if l_index >= self.ui.wth_start.value():
                                    x = float(line.split(self.ui.wth_separator.toPlainText())
                                              [self.ui.wth_column.value() - 1].strip().replace(',', '.', 1))
                                    if self.ui.rbtn_Trapeze.isChecked():
                                        y = float(line.split(self.ui.wth_separator.toPlainText())
                                                  [self.ui.top_column.value() - 1].strip().replace(',', '.', 1))
                        else:
                            for line in self.width_top_source.splitlines():
                                l_index = l_index + 1
                                if l_index >= self.ui.wth_start.value():
                                    x = float(line.strip().replace(',', '.', 1))
                    verification_wdth_top = 1
                except Exception as e:
                    self.dialog_critical(f'Critical error while reading the file with width & top data: {str(e)}.'
                                         f'\nPlease, verify the starting line and the number of the column'
                                         f'\nin which each parameter is stored in the file.'
                                         f'\nOther possible issue: there is text or other non-numerical type in the file,'
                                         f'or separator info is missing.')
                if verification_wl and verification_wdth_top:
                    verification_ok = 1
        else:
            verification_wl = 0
            try:
                if self.reference_source != '':
                    l_index = 0
                    if self.ui.wl_separator.toPlainText() != '':
                        for line in self.reference_source.splitlines():
                            l_index = l_index + 1
                            if l_index >= self.ui.wl_start.value():
                                x = float(line.split(self.ui.wl_separator.toPlainText())
                                    [self.ui.wl_column.value() - 1].strip().replace(',', '.', 1))
                    else:
                        for line in self.reference_source.splitlines():
                            l_index = l_index + 1
                            if l_index >= self.ui.wl_start.value():
                                x = float(line.strip().replace(',', '.', 1))
                verification_wl = 1
            except Exception as e:
                self.dialog_critical(f'Critical error while reading the file with destination wavelength data: {str(e)}.'
                                     f'\nPlease, verify the starting line and the number of the column'
                                     f'\nin which each parameter is stored in the file.'
                                     f'\nOther possible issue: there is text or other non-numerical type in the file,'
                                     f'or separator info is missing.')
            verification_wdth_top = 0
            try:
                # reference width & top source
                if self.width_top_source != '':
                    l_index = 0
                    if self.ui.wth_separator.toPlainText() != '':
                        for line in self.width_top_source.splitlines():
                            l_index = l_index + 1
                            if l_index >= self.ui.wth_start.value():
                                x = float(line.split(self.ui.wth_separator.toPlainText())
                                    [self.ui.wth_column.value() - 1].strip().replace(',', '.', 1))
                    else:
                        for line in self.width_top_source.splitlines():
                            l_index = l_index + 1
                            if l_index >= self.ui.wth_start.value():
                                x = float(line.strip().replace(',', '.', 1))
                verification_wdth_top = 1
            except Exception as e:
                self.dialog_critical(f'Critical error while reading the file with width data: {str(e)}.'
                                     f'\nPlease, verify the starting line and the number of the column'
                                     f'\nin which each parameter is stored in the file.'
                                     f'\nOther possible issue: there is text or other non-numerical type in the file,'
                                     f'or separator info is missing.')
            if verification_wl and verification_wdth_top:
                verification_ok = 1
        # saving the data
        if verification_ok:
            reference_source_dict['reference_source'] = self.reference_source
            reference_source_dict['reference_source_file_name'] = self.reference_source_file_name
            reference_source_dict['width_top_source'] = self.width_top_source
            reference_source_dict['width_top_source_file_name'] = self.width_top_source_file_name
            reference_source_dict['tabWidget_activa_tab'] = self.ui.tabWidget.currentIndex()
            reference_source_dict['tabWidget_2_activa_tab'] = self.ui.tabWidget_2.currentIndex()
            reference_source_dict['reference_data_set_up'] = 'OK'
            data_changed_dict['current_data_changed'] = 1
            # convolution function type
            if self.ui.rbtn_Gaussian.isChecked():
                reference_source_dict['function_type'] = 'Gaussienne'
            elif self.ui.rbtn_Triangle.isChecked():
                reference_source_dict['function_type'] = 'Triangle'
            elif self.ui.rbtn_Trapeze.isChecked():
                reference_source_dict['function_type'] = 'Trapeze'
            # reference file: units
            if self.ui.btn_cm.isChecked():
                reference_source_dict['fichier_a_reference_unit'] = 'cm-1'
            elif self.ui.rbtn_micron.isChecked():
                reference_source_dict['fichier_a_reference_unit'] = 'micron'
            elif self.ui.rbtn_nm.isChecked():
                reference_source_dict['fichier_a_reference_unit'] = 'nm'
            else:
                reference_source_dict['fichier_a_reference_unit'] = 'A'
            # reference file: placement
            reference_source_dict['ligne_debut_reference'] = self.ui.wl_start.value()
            reference_source_dict['long_column_number'] = self.ui.wl_column.value()
            reference_source_dict['reference_wavelength_separator'] = self.ui.wl_separator.toPlainText()
            # reference wavelenth generate
            reference_source_dict['wavelength_min'] = self.ui.wl_min.text()
            reference_source_dict['wavelength_max'] = self.ui.wl_max.text()
            reference_source_dict['wavelength_step'] = self.ui.wl_step.text()
            # reference width & top: constant
            reference_source_dict['width_const'] = self.ui.wth_constant.text()
            reference_source_dict['top_const'] = self.ui.top_const.text()
            # reference width & top: placement
            reference_source_dict['ligne_debut_width_top'] = self.ui.wth_start.value()
            reference_source_dict['width_column_number'] = self.ui.wth_column.value()
            reference_source_dict['top_column_number'] = self.ui.top_column.value()
            reference_source_dict['width_top_separator'] = self.ui.wth_separator.toPlainText()
            # reference width & top: generate
            reference_source_dict['width_min'] = self.ui.wth_min.text()
            reference_source_dict['width_max'] = self.ui.wth_max.text()
            reference_source_dict['top_min'] = self.ui.top_min.text()
            reference_source_dict['top_max'] = self.ui.top_max.text()
            self.close_source = 'save'
            self.close()

    def clear_form_function(self):
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to clear this form?\nAll its data will be deleted",
                                     QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.reference_source = ''
            self.reference_source_file_name = ''
            self.width_top_source = ''
            self.width_top_source_file_name = ''
            # reset: convolution function
            self.ui.rbtn_Gaussian.setAutoExclusive(False)
            self.ui.rbtn_Gaussian.setChecked(True)
            self.ui.rbtn_Gaussian.setAutoExclusive(True)
            self.ui.rbtn_Triangle.setAutoExclusive(False)
            self.ui.rbtn_Triangle.setChecked(False)
            self.ui.rbtn_Triangle.setAutoExclusive(True)
            self.ui.rbtn_Trapeze.setAutoExclusive(False)
            self.ui.rbtn_Trapeze.setChecked(False)
            self.ui.rbtn_Trapeze.setAutoExclusive(True)
            # reset: wavelength
            self.ui.label_wl_file.setText('no file selected')
            self.ui.wl_start.setValue(1)
            self.ui.wl_column.setValue(1)
            self.ui.wl_separator.setPlainText('\t')
            self.ui.wl_min.setText('')
            self.ui.wl_max.setText('')
            self.ui.wl_step.setText('')
            self.ui.tabWidget.setCurrentIndex(0)
            # reset: units
            self.ui.btn_cm.setChecked(True)
            # reset: width & top
            self.ui.label_wth_file.setText('no file selected')
            self.ui.wth_start.setValue(1)
            self.ui.wth_column.setValue(2)
            self.ui.top_column.setValue(3)
            self.ui.wth_separator.setPlainText('\t')
            self.ui.wth_constant.setText('')
            self.ui.top_const.setText('')
            self.ui.top_min.setText('')
            self.ui.top_max.setText('')
            self.ui.wth_min.setText('')
            self.ui.wth_max.setText('')
            self.ui.tabWidget_2.setCurrentIndex(0)
            # reset: clear Trapeze
            self.ui.top_const.setVisible(False)
            self.ui.label_20.setVisible(False)
            self.ui.top_column.setVisible(False)
            self.ui.label_22.setVisible(False)
            self.ui.top_min.setVisible(False)
            self.ui.label_23.setVisible(False)
            self.ui.top_max.setVisible(False)
            self.ui.label_24.setVisible(False)
            self.ui.tabWidget_2.setCurrentIndex(0)

    def close_form_function(self):
        self.close()

    def dialog_critical(self, s):
        dlg = QMessageBox(self)
        dlg.setWindowTitle('Error!')
        dlg.setText(s)
        dlg.setIcon(QMessageBox.Critical)
        dlg.show()


class SpectrumSourceW(QtWidgets.QDialog):
    def __init__(self):
        super(SpectrumSourceW, self).__init__()
        # Ui_SpectrumDialog
        self.ui = Ui_SpectrumDialog()
        self.ui.setupUi(self)
        # class' globals
        self.close_source = ''
        self.deresoudre_source = deresoudre_source_dict["deresoudre_source"]
        self.deresoudre_file_name = deresoudre_source_dict["deresoudre_file_name"]
        # GUI beauties
        # GUI beauties: no border for GroupBox
        self.ui.groupBox_3.setStyleSheet("border:0;")
        # GUI beauties: selected file
        if deresoudre_source_dict['deresoudre_file_name']:
            self.ui.label_file_selected.setText(deresoudre_source_dict['deresoudre_file_name'])
        else:
            self.ui.label_file_selected.setText('no file selected')
        # GUI beauties: buttons
        self.ui.btn_filechoose.setStyleSheet('QPushButton{padding: 15px;}')
        self.ui.btn_save.setStyleSheet('QPushButton{padding: 15px;}')
        self.ui.btn_clear.setStyleSheet('QPushButton{padding: 15px;}')
        self.ui.btn_close.setStyleSheet('QPushButton{padding: 15px;}')
        # GUI beauties: radio
        self.ui.cm_label.setText('cm<sup>-1</sup>')
        self.ui.cm_label.setStyleSheet('QLabel{padding-left: -1px;}')
        self.ui.rbtn_cm.setStyleSheet('QRadioButton{margin-right: -8px;}')
        if deresoudre_source_dict['fichier_a_deresoudre_unit'] != '':
            if deresoudre_source_dict['fichier_a_deresoudre_unit'] == 'cm-1':
                self.ui.rbtn_cm.setChecked(True)
            elif deresoudre_source_dict['fichier_a_deresoudre_unit'] == 'micron':
                self.ui.rbtn_micron.setChecked(True)
            elif deresoudre_source_dict['fichier_a_deresoudre_unit'] == 'nm':
                self.ui.rbtn_nm.setChecked(True)
            else:
                self.ui.rbtn_A.setChecked(True)
        else:
            self.ui.rbtn_cm.setChecked(True)
        # GUI beauties: spin box
        if deresoudre_source_dict['ligne_debut_deresoudre'] != 0:
            self.ui.file_start.setValue(deresoudre_source_dict['ligne_debut_deresoudre'])
            self.ui.wlth_column.setValue(deresoudre_source_dict['long_column_number'])
            self.ui.ints_column.setValue(deresoudre_source_dict['refh_column_number'])
        # GUI beauties: text edit
        fmt = QTextCharFormat()
        fmt.setBackground(QBrush(Qt.yellow))
        self.ui.separ_sign.mergeCurrentCharFormat(fmt)
        if deresoudre_source_dict['deresoudre_content_separator'] != '':
            self.ui.separ_sign.setPlainText(deresoudre_source_dict['deresoudre_content_separator'])
        # SIGNAL & SLOTS
        self.ui.cm_label.mousePressEvent = self.cm_enable
        self.ui.btn_filechoose.clicked.connect(self.choose_file_function)
        self.ui.del_selected_file.clicked.connect(self.clear_selected_file)
        self.ui.btn_save.clicked.connect(self.save_data_function)
        self.ui.btn_clear.clicked.connect(self.clear_form_function)
        self.ui.btn_close.clicked.connect(self.close_form_function)
        self.ui.separ_sign.textChanged.connect(self.set_yellow_text)
        # WINDOW SHOW
        if __name__ == '__main__':
            self.setWindowModality(Qt.ApplicationModal)
            self.show()
            self.exec_()

    def closeEvent(self, event):
        if self.close_source == 'save':
            self.close()
        else:
            reply = QMessageBox.question(self, 'Message',
                                         "Are you sure you want to close this window?\nAny change will be lost",
                                         QMessageBox.Yes |
                                         QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.close()
            else:
                event.ignore()

    def cm_enable(self, event):
        self.ui.rbtn_cm.setChecked(True)

    def set_yellow_text(self):
        fmt = QTextCharFormat()
        fmt.setBackground(QBrush(Qt.yellow))
        self.ui.separ_sign.mergeCurrentCharFormat(fmt)
        if '\n' in self.ui.separ_sign.toPlainText():
            self.ui.separ_sign.setPlainText(self.ui.separ_sign.toPlainText().replace('\n', ''))

    def choose_file_function(self):
        path, _ = QFileDialog.getOpenFileName(self, "Choose file", "", "Text documents (*.txt *.csv *tsv);;All files (*.*)")
        if path:
            try:
                with open(path, 'r') as f:
                    self.deresoudre_source = f.read()
                    if path.rfind("/") != -1:
                        self.deresoudre_file_name = path[path.rfind("/") + 1:]
                    else:
                        self.deresoudre_file_name = path[path.rfind("\\") + 1:]
                    self.ui.label_file_selected.setText(self.deresoudre_file_name)
            except Exception as e:
                self.dialog_critical(f'Critical error while opening file: {str(e)}.'
                                     f'\nThis file is corrupted or it is not a text document')

    def clear_selected_file(self):
        if self.deresoudre_file_name != '':
            reply = QMessageBox.question(self, 'Message',
                                         "Are you sure you want to remove the selected file?",
                                         QMessageBox.Yes |
                                         QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.deresoudre_file_name = ""
                self.deresoudre_source = ""
                self.ui.label_file_selected.setText('no file selected')

    def save_data_function(self):
        # verifications: file for spectrum source is not selected
        verification_ok = 0
        if self.deresoudre_source == '':
            self.ui.btn_filechoose.setFocus()
            self.dialog_critical('File for spectrum source must not be empty')
        elif self.ui.separ_sign.toPlainText() == '':
            self.ui.separ_sign.setFocus()
            self.dialog_critical('For a file with several columns a separator is mandatory!'
                                 '\nPlease, enter an appropriate value')
        else:
            try:
                l_index = 0
                for line in self.deresoudre_source.splitlines():
                    l_index = l_index + 1
                    if l_index >= int(self.ui.file_start.text()):
                        if float(line.split(self.ui.separ_sign.toPlainText())
                                 [int(self.ui.wlth_column.text()) - 1].strip().replace(',', '.', 1)) != 0:
                            x = float(line.split(self.ui.separ_sign.toPlainText())
                                [int(self.ui.wlth_column.text()) - 1].strip().replace(',', '.', 1))
                            y = float(line.split(self.ui.separ_sign.toPlainText())
                                [int(self.ui.ints_column.text()) - 1].strip().replace(',', '.', 1))
                verification_ok = 1
                deresoudre_source_dict['deresoudre_source'] = self.deresoudre_source
                deresoudre_source_dict['deresoudre_file_name'] = self.deresoudre_file_name
            except Exception as e:
                self.dialog_critical(f'Critical error while reading the file with spectral data: {str(e)}.'
                                     f'\nPlease, verify the starting line and the number of the column'
                                     f'\nin which each parameter is stored in the file.'
                                     f'\nOther possible issue: there is text or other non-numerical type in the file,'
                                     f'or separator info is missing.')
        if verification_ok:
            # units
            if self.ui.rbtn_cm.isChecked():
                deresoudre_source_dict['fichier_a_deresoudre_unit'] = 'cm-1'
            elif self.ui.rbtn_micron.isChecked():
                deresoudre_source_dict['fichier_a_deresoudre_unit'] = 'micron'
            elif self.ui.rbtn_nm.isChecked():
                deresoudre_source_dict['fichier_a_deresoudre_unit'] = 'nm'
            else:
                deresoudre_source_dict['fichier_a_deresoudre_unit'] = 'A'
            # placement
            deresoudre_source_dict['ligne_debut_deresoudre'] = int(self.ui.file_start.text())
            deresoudre_source_dict['long_column_number'] = int(self.ui.wlth_column.text())
            deresoudre_source_dict['refh_column_number'] = int(self.ui.ints_column.text())
            deresoudre_source_dict['deresoudre_content_separator'] = self.ui.separ_sign.toPlainText()
            deresoudre_source_dict['deresoudre_data_set_up'] = 'OK'
            data_changed_dict['current_data_changed'] = 0
            self.close_source = 'save'
            self.close()

    def clear_form_function(self):
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to clear the form?\nAll its data will be reset", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.deresoudre_file_name = ""
            self.deresoudre_source = ""
            self.ui.label_file_selected.setText('no file selected')
            self.ui.rbtn_cm.setChecked(True)
            self.ui.file_start.setValue(1)
            self.ui.wlth_column.setValue(1)
            self.ui.ints_column.setValue(2)
            self.ui.separ_sign.setPlainText('\t')

    def close_form_function(self):
        self.close()

    def dialog_critical(self, s):
        dlg = QMessageBox(self)
        dlg.setWindowTitle('Error!')
        dlg.setText(s)
        dlg.setIcon(QMessageBox.Critical)
        dlg.show()


class OutputParamW(QtWidgets.QDialog):
    def __init__(self):
        super(OutputParamW, self).__init__()
        self.ui = Ui_OutputFileDialog()
        self.ui.setupUi(self)
        # class globals
        self.close_source = ''
        # GUI beauties
        # GUI beauties: no borders in GroupBox
        self.ui.groupBox_2.setStyleSheet("border:0;")
        self.ui.groupBox_3.setStyleSheet("border:0;")
        self.ui.groupBox_4.setStyleSheet("border:0;")
        self.ui.groupBox_5.setStyleSheet("border:0;")
        # GUI beauties: decimal signs
        self.ui.d_s_wl.setValue(format_output_dict['decimals_wavelength'])
        self.ui.d_s_int.setValue(format_output_dict['decimals_intencity'])
        # GUI beauties: formal
        if format_output_dict['wlth_format'] == 'exponential':
            self.ui.w_f_exp.setChecked(True)
        else:
            self.ui.w_f_dec.setChecked(True)
        if format_output_dict['intens_format'] == 'exponential':
            self.ui.i_f_exp.setChecked(True)
        else:
            self.ui.i_f_dec.setChecked(True)
        # GUI beauties: order
        if format_output_dict['order'] == 1:
            self.ui.w_o_a.setChecked(True)
        else:
            self.ui.w_o_d.setChecked(True)
        # GUI beauties: title
        if format_output_dict['title'] == 'without':
            self.ui.t_n.setChecked(True)
        else:
            self.ui.t_w.setChecked(True)
        # GUI beauties: separator
        fmt = QTextCharFormat()
        fmt.setBackground(QBrush(Qt.yellow))
        self.ui.separ_sign.mergeCurrentCharFormat(fmt)
        self.ui.separ_sign.setPlainText(format_output_dict['separator'])
        # GUI beauties: buttons
        self.ui.btn_save.setStyleSheet('QPushButton{padding: 15px;}')
        self.ui.btn_clear.setStyleSheet('QPushButton{padding: 15px;}')
        self.ui.btn_close.setStyleSheet('QPushButton{padding: 15px;}')
        # SIGNAL & SLOTS
        self.ui.separ_sign.textChanged.connect(self.set_yellow_text)
        self.ui.btn_save.clicked.connect(self.save_data_function)
        self.ui.btn_clear.clicked.connect(self.clear_form_function)
        self.ui.btn_close.clicked.connect(self.close_form_function)
        # WINDOW SHOW
        if __name__ == '__main__':
            self.setWindowModality(Qt.ApplicationModal)
            self.show()
            self.exec_()

    def closeEvent(self, event):
        if self.close_source == 'save':
            self.close()
        else:
            reply = QMessageBox.question(self, 'Message',
                                         "Are you sure you want to close this window?\nAny change will be lost",
                                         QMessageBox.Yes |
                                         QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.close()
            else:
                event.ignore()

    def set_yellow_text(self):
        fmt = QTextCharFormat()
        fmt.setBackground(QBrush(Qt.yellow))
        self.ui.separ_sign.mergeCurrentCharFormat(fmt)
        if '\n' in self.ui.separ_sign.toPlainText():
            self.ui.separ_sign.setPlainText(self.ui.separ_sign.toPlainText().replace('\n', ''))

    def save_data_function(self):
        format_output_dict['decimals_wavelength'] = self.ui.d_s_wl.value()
        format_output_dict['decimals_intencity'] = self.ui.d_s_int.value()
        if self.ui.w_f_dec.isChecked():
            format_output_dict['wlth_format'] = 'decimal'
        else:
            format_output_dict['wlth_format'] = 'exponential'
        if self.ui.i_f_dec.isChecked():
            format_output_dict['intens_format'] = 'decimal'
        else:
            format_output_dict['intens_format'] = 'exponential'
        if self.ui.w_o_a.isChecked():
            format_output_dict['order'] = 1
        else:
            format_output_dict['order'] = 0
        if self.ui.t_w.isChecked():
            format_output_dict['title'] = 'with'
        else:
            format_output_dict['title'] = 'without'
        format_output_dict['separator'] = self.ui.separ_sign.toPlainText()
        self.close_source = 'save'
        self.close()

    def clear_form_function(self):
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to clear the form?\nAll its data will be reset", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            format_output_dict['decimals_wavelength'] = 5
            format_output_dict['decimals_intencity'] = 5
            format_output_dict['wlth_format'] = ''
            format_output_dict['intens_format'] = ''
            format_output_dict['title'] = ''
            format_output_dict['separator'] = '\t'
            self.ui.d_s_wl.setValue(5)
            self.ui.d_s_int.setValue(5)
            self.ui.w_f_dec.setChecked(True)
            self.ui.i_f_dec.setChecked(True)
            self.ui.t_w.setChecked(True)
            self.ui.separ_sign.setPlainText('\t')

    def close_form_function(self):
        self.close()

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    win = ConvolutionMainW()
    win.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
    win.show()
    sys.exit(app.exec())
