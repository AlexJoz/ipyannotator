# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/05_image_button.ipynb (unless otherwise specified).

__all__ = ['ImageButton']

# Cell
from functools import partial

import base64
from pathlib import Path

from ipyevents import Event
from ipywidgets import Image, VBox, Layout, Output, HTML, Label
from traitlets import Bool, Unicode, HasTraits, Bytes, link, dlink, observe

# Cell

class ImageButton(VBox, HasTraits):
    debug_output = Output(layout={'border': '1px solid black'})
    active = Bool()
    image_path = Unicode()
    label_value = Unicode()

    def __init__(self, im_path=None, label=None,
                 im_name=None, im_index=None,
                 display_label=True, image_width='50px', image_height=None):

        self.display_label = display_label
        self.label = 'None'
        self.image = Image(
            layout=Layout(display='flex',
                          justify_content='center',
                          align_items='center',
                          align_content='center',
                          width=image_width,
                          height=image_height),
        )

        if self.display_label:  # both image and label
            self.label = HTML(
                value='?',
                layout=Layout(display='flex',
                              justify_content='center',
                              align_items='center',
                              align_content='center'),
            )
        else:  # no label (capture image case)
            self.im_name = im_name
            self.im_index = im_index
            self.image.layout.border = 'solid 1px gray'
            self.image.layout.object_fit = 'contain'

        super().__init__(layout=Layout(align_items='center',
                                       margin='3px',
                                       padding='2px'))
        if not im_path:
            self.clear()

        self.d = Event(source=self, watched_events=['click'])

    @observe('image_path')
    def _read_image(self, change=None):
        new_path = change['new']
        if new_path:
            self.image.value = open(new_path, "rb").read()
            if not self.children:
                self.children = (self.image,)
                if self.display_label:
                    self.children += (self.label,)
        else:
            #do not display image widget
            self.children = []


    @observe('label_value')
    def _read_label(self, change=None):
        new_label = change['new']

        if isinstance(self.label, HTML):
            self.label.value = new_label
        else:
            self.label = new_label

    def clear(self):
        if isinstance(self.label, HTML):
            self.label.value = ''
        else:
            self.label = ''
        self.image_path = ''
        self.active = False

    @observe('active')
    def mark(self, ev):
        # pad to compensate self size with border
        if self.active:
            if self.display_label:
                self.layout.border = 'solid 2px #1B8CF3'
                self.layout.padding = '0px'
            else:
                self.image.layout.border = 'solid 3px #1B8CF3'
                self.image.layout.padding = '0px'
        else:
            if self.display_label:
                self.layout.border = 'none'
                self.layout.padding = '2px'
            else:
                self.image.layout.border = 'solid 1px gray'

    @property
    def name(self):
        return Path(self.image_path).name

    @debug_output.capture(clear_output=False)
    def on_click(self, cb):
        self.d.on_dom_event(cb)

    def reset_callbacks(self):
        self.d.reset_callbacks()
