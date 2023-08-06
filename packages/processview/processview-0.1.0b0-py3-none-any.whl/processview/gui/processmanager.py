# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016-2017 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ###########################################################################*/


__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "03/11/2020"


from typing import Union
from silx.gui import qt
from collections import OrderedDict
from processview.core.manager import DatasetState
from processview.core.manager import ProcessManager as _ProcessManager
from processview.gui import icons as icons
from processview.utils import docstring
import fnmatch


_SCAN_STATE_BACKGROUND = {
    DatasetState.ON_GOING: qt.QColor("#839684"),  # light blue
    DatasetState.SUCCEED: qt.QColor("#068c0c"),  # green
    DatasetState.FAILED: qt.QColor("#f52718"),  # red
    DatasetState.PENDING: qt.QColor("#609ab3"),  # blue gray
    DatasetState.SKIPPED: qt.QColor("#f08e0e"),  # light orange
}


class ProcessManagerWindow(qt.QMainWindow):
    """
    Main window of the process manager
    """

    def __init__(self, parent):
        qt.QMainWindow.__init__(self, parent)
        self.setWindowFlags(qt.Qt.Widget)

        self._centralWidget = ProcessManagerWidget(parent=self)
        self.setCentralWidget(self._centralWidget)


class ProcessManagerWidget(qt.QWidget):
    def __init__(self, parent):
        qt.QWidget.__init__(self, parent)
        self.setLayout(qt.QVBoxLayout())

        self._manager = ProcessManager()

        self.filterWidget = _ToggleableFilterWidget(parent=self)
        self.layout().setContentsMargins(4, 4, 4, 4)
        self.layout().setSpacing(4)
        self.filterWidget.layout().setSpacing(4)
        self.layout().addWidget(self.filterWidget)

        self.observationTable = qt.QTableView(parent=parent)
        self.layout().addWidget(self.observationTable)
        self.observationTable.setSelectionBehavior(qt.QAbstractItemView.SelectRows)
        self.observationTable.setModel(
            _ScanProcessModel(parent=self.observationTable, header=tuple())
        )
        self.observationTable.resizeColumnsToContents()
        self.observationTable.setSortingEnabled(True)
        self.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Expanding)

        # connect signal / slot
        self._manager.sigUpdated.connect(self._updateScanStates)
        self._manager.sigNewProcessRegistered.connect(self._updateProcesses)
        self.filterWidget.filterWidget.sigScanPatternEditingFinished.connect(
            self._filterUpdated
        )
        self.filterWidget.filterWidget.sigProcessPatternEditingFinished.connect(
            self._filterUpdated
        )

    def _updateScanStates(self):
        self.observationTable.model().setScans(self._manager.get_scans())

    def _updateProcesses(self):
        self.observationTable.model().setProcesses(self._manager.get_processes())

    def _filterUpdated(self):
        self.observationTable.model().process_patterns = (
            self.filterWidget.getProcessPatterns()
        )
        self._updateProcesses()
        self.observationTable.model().scan_patterns = (
            self.filterWidget.getScanPatterns()
        )
        self._updateScanStates()


class _ScanProcessModel(qt.QAbstractTableModel):
    def __init__(self, parent, header, *args):
        qt.QAbstractTableModel.__init__(self, parent, *args)
        self.header = header
        self._processes = OrderedDict()
        self._scans = OrderedDict()
        self._processPatterns = tuple()
        # is there some process name pattern to follow ?
        self._scanPatterns = tuple()
        # is there some scan id pattern to follow ?

    def _match_scan_patterns(self, scan):
        if len(self._scanPatterns) is 0:
            return True
        for pattern in self._scanPatterns:
            if fnmatch.fnmatch(str(scan), pattern):
                return True
        return False

    def _match_process_patterns(self, process):
        if len(self.process_patterns) is 0:
            return True
        for pattern in self._processPatterns:
            if fnmatch.fnmatch(process.name, pattern):
                return True
        return False

    @property
    def process_patterns(self):
        return self._processPatterns

    @process_patterns.setter
    def process_patterns(self, patterns):
        self._processPatterns = patterns

    @property
    def scan_patterns(self):
        return self._scanPatterns

    @scan_patterns.setter
    def scan_patterns(self, patterns):
        self._scanPatterns = patterns

    def add(self, scan, status):
        self._processes[scan] = status
        self.endResetModel()

    def remove(self, scan):
        if scan in self._processes:
            del self._processes[scan]
        self.endResetModel()

    def update_scan(self, scan, status):
        self._processes[scan] = status
        self.endResetModel()

    def clear(self):
        self._processes = OrderedDict()
        self.endResetModel()

    def rowCount(self, parent=None):
        return len(self._scans)

    def columnCount(self, parent=None):
        return len(self._processes)

    def setProcesses(self, processes):
        assert isinstance(processes, (tuple, list))
        self._processes = {}
        processes = list(filter(self._match_process_patterns, processes))
        for i_process, process in enumerate(processes):
            self._processes[i_process] = process
        self.endResetModel()

    def setScans(self, scans):
        assert isinstance(scans, (tuple, list))
        self._scans = {}
        scans = list(filter(self._match_scan_patterns, scans))
        for i_scan, scan in enumerate(scans):
            self._scans[i_scan] = scan
        self.endResetModel()

    def headerData(self, col, orientation, role):
        if orientation == qt.Qt.Horizontal and role == qt.Qt.DisplayRole:
            if col < len(self._processes):
                return self._processes[col].name
        elif orientation == qt.Qt.Vertical and role == qt.Qt.DisplayRole:
            if col < len(self._scans):
                return str(self._scans[col])
        return None

    #
    # def sort(self, col, order):
    #     print('sort call')
    #     self.layoutAboutToBeChanged.emit()
    #     if self._processes is None:
    #         return
    #
    #     to_order = {}
    #     for observation in self._processes.keys():
    #         to_order[str(observation)] = observation
    #
    #     ordering = sorted(list(to_order.keys()))
    #     if order == qt.Qt.DescendingOrder:
    #         ordering = reversed(ordering)
    #     _observations = OrderedDict()
    #     for str_key in ordering:
    #         key = to_order[str_key]
    #         _observations[key] = self._processes[key]
    #
    #     self._processes = _observations
    #     self.layoutChanged.emit()

    def data(self, index, role):
        if index.isValid() is False:
            return None

        if role not in (qt.Qt.DisplayRole, qt.Qt.ToolTipRole, qt.Qt.BackgroundRole):
            return None

        scan_short_name = self._scans[index.row()]
        process_name = self._processes[index.column()]
        scan_process_state = ProcessManager().get_scan_state(
            scan=scan_short_name, process=process_name
        )
        scan_process_details = ProcessManager().get_dataset_details(
            scan=scan_short_name, process=process_name
        )
        if role == qt.Qt.BackgroundRole:
            if scan_process_state is None:
                # if "unmet"
                return qt.QColor("#ffffff")
            else:
                return _SCAN_STATE_BACKGROUND[scan_process_state]
        elif role == qt.Qt.DisplayRole:
            if scan_process_state is None:
                return ""
            else:
                return scan_process_state.value
        if role == qt.Qt.ToolTipRole:
            if scan_process_details is None:
                return ""
            else:
                return scan_process_details


class _ToggleableFilterWidget(qt.QWidget):

    _BUTTON_ICON = qt.QStyle.SP_ToolBarVerticalExtensionButton  # noqa

    def __init__(self, parent):
        qt.QWidget.__init__(self, parent)
        self.setLayout(qt.QGridLayout())
        self._toggleButton = qt.QPushButton("", self)
        self.layout().addWidget(self._toggleButton, 0, 0, 1, 1)
        self._filterWidget = _FilterWidget(parent=self)
        self.layout().addWidget(self._filterWidget, 0, 1, 4, 4)

        self._toggleButton.setSizePolicy(qt.QSizePolicy.Fixed, qt.QSizePolicy.Fixed)
        self._setButtonIcon(show=True)

        # connect signal / slot
        self._toggleButton.clicked.connect(self._toggleFilterWidget)

        # expose API
        self.getProcessPatterns = self._filterWidget.getProcessPatterns
        self.getScanPatterns = self._filterWidget.getScanPatterns

    @property
    def filterWidget(self):
        return self._filterWidget

    def _setButtonIcon(self, show):
        style = qt.QApplication.instance().style()
        # return a QIcon
        icon = style.standardIcon(self._BUTTON_ICON)
        if show is True:
            pixmap = icon.pixmap(32, 32).transformed(qt.QTransform().scale(1, -1))
            icon = qt.QIcon(pixmap)
        self._toggleButton.setIcon(icon)

    def _toggleFilterWidget(self):
        visible = not self._filterWidget.isVisible()
        self._setButtonIcon(show=visible)
        self._filterWidget.setVisible(visible)


class _FilterWidget(qt.QWidget):
    """
    Widget to define some filtering pattern on scans and / or processes
    """

    sigProcessPatternEditingFinished = qt.Signal()
    """signal emit when the process pattern editing finished"""

    sigScanPatternEditingFinished = qt.Signal()
    """signal emit when the scan pattern editing finished"""

    def __init__(self, parent=None, name="filter", font_size=12, icon_size=20):
        qt.QWidget.__init__(self, parent)
        self.setLayout(qt.QGridLayout())

        font = self.font()
        font.setPixelSize(font_size)
        self.setFont(font)

        icon = icons.getQIcon("magnifying_glass")
        self._researchLabelIcon = qt.QLabel("", parent=self)
        self._researchLabelIcon.setPixmap(icon.pixmap(icon_size, state=qt.QIcon.On))
        self.layout().addWidget(qt.QLabel(name, self), 0, 1, 1, 1)
        self.layout().addWidget(self._researchLabelIcon, 0, 2, 1, 1)

        # filter by scan id / name
        self._scanLabel = qt.QLabel("scan", self)
        self.layout().addWidget(self._scanLabel, 1, 2, 1, 2)
        self._scanPatternLE = qt.QLineEdit("", self)
        self.layout().addWidget(self._scanPatternLE, 1, 4, 1, 1)
        tooltip = (
            "Provide one or several scan name or pattern to only "
            " display those scans. Pattern should be separated by a "
            "semi colon. Handle linux wild card. Example: "
            "`pattern1; *suffix; prefix*`"
        )
        for widget in self._scanLabel, self._scanPatternLE:
            widget.setToolTip(tooltip)
        self._clearScanPatternPB = qt.QPushButton("clear", self)
        self._clearScanPatternPB.setAutoDefault(True)
        self.layout().addWidget(self._clearScanPatternPB, 1, 5, 1, 1)

        # filter by process name
        self._processLabel = qt.QLabel("process", self)
        self.layout().addWidget(self._processLabel, 2, 2, 1, 2)
        self._processPatternLE = qt.QLineEdit("", self)
        self.layout().addWidget(self._processPatternLE, 2, 4, 1, 1)
        tooltip = (
            "Provide one or several process name or pattern to only "
            " display those scans. Pattern should be separated by a "
            "semi colon. Handle linux wild card. Example: "
            "`pattern1; *suffix; prefix*`"
        )
        for widget in self._processLabel, self._processPatternLE:
            widget.setToolTip(tooltip)
        self._clearProcessPatternPB = qt.QPushButton("clear", self)
        self._clearProcessPatternPB.setAutoDefault(True)
        self.layout().addWidget(self._clearProcessPatternPB, 2, 5, 1, 1)

        # connect signal / slot
        self._clearProcessPatternPB.released.connect(self._processPatternLE.clear)
        self._clearProcessPatternPB.released.connect(
            self._processPatternEditingFinished
        )
        self._clearScanPatternPB.released.connect(self._scanPatternLE.clear)
        self._clearScanPatternPB.released.connect(self._scanPatternEditingFinished)
        self._scanPatternLE.editingFinished.connect(self._scanPatternEditingFinished)
        self._processPatternLE.editingFinished.connect(
            self._processPatternEditingFinished
        )

    def getProcessPatterns(self) -> tuple:
        if self._processPatternLE.text() == "":
            return ("*",)
        res = self._processPatternLE.text().replace(" ", "")
        return tuple(res.split(";"))

    def getScanPatterns(self) -> tuple:
        if self._scanPatternLE.text() == "":
            return ("*",)
        res = self._scanPatternLE.text().replace(" ", "")
        return tuple(res.split(";"))

    def _scanPatternEditingFinished(self, *args, **kwargs):
        self.sigScanPatternEditingFinished.emit()

    def _processPatternEditingFinished(self, *args, **kwargs):
        self.sigProcessPatternEditingFinished.emit()


class ProcessManager(qt.QObject):
    sigUpdated = qt.Signal()
    """Signal emitted when the state of some process / scan is updated
    """

    sigNewProcessRegistered = qt.Signal()
    """Signal emitted when a new process is registered"""

    def __init__(self):
        qt.QObject.__init__(self)
        self.manager = _ProcessManager()

        # monkey patch manager updated function
        # TODO: add / remove callback would be simpler
        self.manager.add_update_callback(self.updated)
        self.manager.add_new_process_callback(self.processAdded)

    def updated(self):
        self.sigUpdated.emit()

    def processAdded(self):
        self.sigNewProcessRegistered.emit()

    def processNameChanged(self, process):
        self.sigProcessNameChanged.emit(process)

    def destroyed(self, object_):
        self.manager.remove_update_callback(self.updated)
        qt.QObject.destroyed(object_)

    # expose some of the original ProcessManager API
    @docstring(_ProcessManager)
    def notify_dataset_state(self, scan, process, state) -> None:
        self.manager.notify_dataset_state(dataset=scan, process=process, state=state)

    @docstring(_ProcessManager)
    def get_scan_state(self, scan, process) -> Union[None, DatasetState]:
        return self.manager.get_dataset_state(dataset=scan, process=process)

    @docstring(_ProcessManager)
    def get_dataset_details(self, scan, process) -> Union[None, DatasetState]:
        return self.manager.get_dataset_details(dataset=scan, process=process)

    @docstring(_ProcessManager)
    def get_dataset_stream(self, scan, time_stamp=False) -> tuple:
        return self.manager.get_dataset_stream(
            self, dataset=scan, time_stamp=time_stamp
        )

    @docstring(_ProcessManager)
    def get_process_history(self, process, time_stamp=False) -> tuple:
        return self.manager.get_process_history(process=process, time_stamp=time_stamp)

    @docstring(_ProcessManager)
    def get_processes(self):
        return self.manager.get_processes()

    @docstring(_ProcessManager)
    def get_scans(self):
        return self.manager.get_datasets()


if __name__ == "__main__":
    app = qt.QApplication([])
    widget = ProcessManagerWidget(parent=None)
    widget.show()
    app.exec_()
