# -*- coding: utf-8 -*-
import datetime
import logging
from traceback import format_exc

import numpy as np
import numpy.core.defchararray as npchar
import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets

from ...blocks.utils import (
    csv_bytearray2hex,
    csv_int2bin,
    csv_int2hex,
    pandas_query_compatible,
)

from ..utils import run_thread_with_progress
from .tabular_base import TabularTreeItem, TabularBase
from .tabular_filter import TabularFilter

logger = logging.getLogger("asammdf.gui")
LOCAL_TIMEZONE = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo


class Tabular(TabularBase):
    add_channels_request = QtCore.pyqtSignal(list)

    def __init__(self, signals=None, start=0, format="phys", *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.signals_descr = {}
        self.start = start
        self.pattern = {}
        self.format = format
        self.format_selection.setCurrentText(format)

        if signals is None:
            self.signals = pd.DataFrame()
        else:
            index = pd.Series(np.arange(len(signals), dtype="u8"), index=signals.index)
            signals["Index"] = index

            signals["timestamps"] = signals.index
            signals.set_index(index, inplace=True)
            dropped = {}

            for name_ in signals.columns:
                col = signals[name_]
                if col.dtype.kind == "O":
                    if name_.endswith("DataBytes"):
                        try:
                            sizes = signals[name_.replace("DataBytes", "DataLength")]
                        except:
                            sizes = None
                        dropped[name_] = pd.Series(
                            csv_bytearray2hex(
                                col,
                                sizes,
                            ),
                            index=signals.index,
                        )

                    elif name_.endswith("Data Bytes"):
                        try:
                            sizes = signals[name_.replace("Data Bytes", "Data Length")]
                        except:
                            sizes = None
                        dropped[name_] = pd.Series(
                            csv_bytearray2hex(
                                col,
                                sizes,
                            ),
                            index=signals.index,
                        )

                    elif col.dtype.name != 'category':
                        try:
                            dropped[name_] = pd.Series(
                                csv_bytearray2hex(col), index=signals.index
                            )
                        except:
                            pass

                    self.signals_descr[name_] = 0

                elif col.dtype.kind == "S":
                    try:
                        dropped[name_] = pd.Series(
                            npchar.decode(col, "utf-8"), index=signals.index
                        )
                    except:
                        dropped[name_] = pd.Series(
                            npchar.decode(col, "latin-1"), index=signals.index
                        )
                    self.signals_descr[name_] = 0
                else:
                    self.signals_descr[name_] = 0

            signals = signals.drop(columns=["Index", *list(dropped)])
            for name, s in dropped.items():
                signals[name] = s

            names = list(signals.columns)
            names = [
                "timestamps",
                *[name for name in names if name.endswith((".ID", ".DataBytes"))],
                *[
                    name
                    for name in names
                    if name != "timestamps" and not name.endswith((".ID", ".DataBytes"))
                ],
            ]
            self.signals = signals[names]

        self._original_timestamps = signals["timestamps"]

        self.build(self.signals, True)

        prefixes = set()
        for name in self.signals.columns:
            while "." in name:
                name = name.rsplit(".", 1)[0]
                prefixes.add(f"{name}.")

        self.filters.minimal_menu = True

        self.prefix.insertItems(0, sorted(prefixes, key=lambda x: (-len(x), x)))
        self.prefix.setEnabled(False)

        self.prefix.currentIndexChanged.connect(self.prefix_changed)

        if prefixes:
            self.remove_prefix.setCheckState(QtCore.Qt.Checked)

        self._settings = QtCore.QSettings()
        integer_mode = self._settings.value("tabular_format", "phys")

        self.format_selection.setCurrentText(integer_mode)
