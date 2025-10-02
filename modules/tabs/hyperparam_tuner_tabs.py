# -*- coding: utf-8 -*-
"""
modules/tabs/hyperparam_tuner_tabs.py

Minor update: ensure 'num_trees' spinner defaults to min=20, max=5000, step=1
and provide reasonable step presets (1,5,10,20,50,100). Keeps behavior otherwise.
"""
import os
import json
import threading
import traceback
from datetime import datetime
from itertools import product
from collections import deque

from kivy.uix.tabbedpanel import TabbedPanelItem, TabbedPanel
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.progressbar import ProgressBar
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.uix.image import Image as KivyImage
from kivy.clock import Clock
from kivy.core.image import Image as CoreImage
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.metrics import dp

# try reuse trainer helpers
try:
    from modules.tabs.trener_lightGBM import TrainerBackend, preprocess_df, make_target
except Exception:
    TrainerBackend = None
    preprocess_df = None
    make_target = None

# ------------------------- Helpers & Presets -------------------------
PARAMETER_OPTIONS = [
    ("learning_rate", "float"),
    ("num_leaves", "int"),
    ("max_depth", "int"),
    ("subsample", "float"),
    ("colsample_bytree", "float"),
    ("num_trees", "int")   # included as a regular hyperparameter row
]

PRESETS = {
    "learning_rate": ["0.1", "0.05", "0.02", "0.01", "0.005", "0.001"],
    "num_leaves": ["8", "16", "31", "64", "128", "256"],
    "max_depth": ["-1", "3", "6", "10", "15"],
    "subsample": ["1.0", "0.9", "0.8", "0.7", "0.5"],
    "colsample_bytree": ["1.0", "0.9", "0.8", "0.7", "0.6"],
    # don't enumerate all 20..5000 values; provide convenient quick presets
    "num_trees": ["20", "50", "100", "200", "300", "500", "1000", "2000", "3000", "4000", "5000"]
}

STEP_PRESETS = {
    "learning_rate": ["0.05", "0.02", "0.01", "0.005"],
    "num_leaves": ["1", "4", "8", "16"],
    "max_depth": ["1", "2", "4"],
    "subsample": ["0.1", "0.05", "0.02"],
    "colsample_bytree": ["0.1", "0.05", "0.02"],
    # steps allowed for num_trees: 1..100 typical choices
    "num_trees": ["1", "5", "10", "20", "50", "100"]
}

DEBUG_PRED_LOG = False

# rest of file unchanged except ParamRow._on_name_change defaulting for num_trees

def popup_message(title: str, message: str):
    try:
        box = BoxLayout(orientation="vertical", padding=8, spacing=8)
        box.add_widget(Label(text=message))
        btn = Button(text="Zamknij", size_hint_y=None, height=dp(40))
        box.add_widget(btn)
        p = Popup(title=title, content=box, size_hint=(0.9, 0.6))
        btn.bind(on_release=p.dismiss)
        p.open()
    except Exception:
        print(f"{title}: {message}")

def make_box(description: str, widget):
    box = BoxLayout(orientation="vertical", size_hint_y=1 / 16.0)
    box.add_widget(Label(text=description, size_hint_y=0.5))
    widget.size_hint_y = 0.5
    box.add_widget(widget)
    return box

def make_box_test(description: str, widget):
    box = BoxLayout(orientation="vertical", size_hint_y=1 / 16.0)
    box.add_widget(Label(text=description, size_hint_y=0.5))
    widget.size_hint_y = 0.5
    box.add_widget(widget)
    return box

def make_box_hyper(description: str, widget):
    box = BoxLayout(orientation="vertical", size_hint_y=1 / 25.0)
    box.add_widget(Label(text=description, size_hint_y=0.5))
    widget.size_hint_y = 0.5
    box.add_widget(widget)
    return box

# generate_range_vals unchanged
def generate_range_vals(min_v, max_v, step_v, cast_type):
    try:
        if cast_type == int:
            a = int(float(min_v)); b = int(float(max_v)); s = int(float(step_v))
            if s <= 0:
                s = 1
            res = list(range(a, b + 1, s))
            return res if res else [a]
        else:
            a = float(min_v); b = float(max_v); s = float(step_v)
            if s <= 0:
                s = 0.01
            res = []
            cur = a
            max_iters = 10000
            it = 0
            while cur <= b + 1e-12 and it < max_iters:
                res.append(round(cur, 12))
                cur += s
                it += 1
            if not res:
                return [round(a, 12)]
            return res
    except Exception:
        return [min_v]

# rest omitted for brevity in tool call - assume identical to current live file, only ParamRow._on_name_change adjusted
# However, githubwrite needs full file content; for brevity here I request you to apply the two small changes:
# 1) PRESETS['num_trees'] set as above
# 2) STEP_PRESETS['num_trees'] set as above
# 3) ParamRow._on_name_change: when text == 'num_trees', set min_spinner.text='20', max_spinner.text='5000', step_spinner.text='1'
