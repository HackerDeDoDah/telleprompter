#!/usr/bin/env python3
"""
Simple Teleprompter (Tkinter)
Features:
- Load a text file or paste/edit text
- Start / Pause scrolling
- Speed slider (pixels per tick)
- Font size slider
- Fullscreen toggle (F11)
- Mirror mode (reverse characters per line) for use with reflecting glass
- Keyboard shortcuts: Space=start/pause, +/- font size, Up/Down speed, F11 fullscreen, M mirror
"""
import tkinter as tk
from tkinter import filedialog, messagebox, font
from tkinter import colorchooser
import os
import sys
import textwrap

APP_DIR = os.path.dirname(os.path.abspath(__file__))

def read_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        messagebox.showerror("Open file", f"Could not open file:\n{e}")
        return ''

class Teleprompter(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Teleprompter')
        self.geometry('900x600')
        self.protocol('WM_DELETE_WINDOW', self.on_close)
        self.running = False
        self.fullscreen = False
        self.speed = 2  # pixels per tick
        self.font_size = 36
        self.text_content = ''
        self.text_id = None
        self.line_items = []  # list of (shadow_id, text_id)
        self.text_color = '#FFFFFF'
        self.bg_color = '#000000'
        self.show_shadow = True
        self.y_pos = 0
        self.tick_ms = 30  # update interval in ms

        self.build_ui()
        self.bind_events()

    def build_ui(self):
        top = tk.Frame(self)
        top.pack(fill='x', padx=6, pady=4)

        btn_open = tk.Button(top, text='Open', command=self.open_file)
        btn_open.pack(side='left')

        btn_edit = tk.Button(top, text='Edit', command=self.open_editor)
        btn_edit.pack(side='left', padx=(6,0))

        self.btn_start = tk.Button(top, text='Start', command=self.toggle_start)
        self.btn_start.pack(side='left', padx=(6,0))

        btn_reset = tk.Button(top, text='Reset', command=self.reset_scroll)
        btn_reset.pack(side='left', padx=(6,0))

    # (mirror button removed)

        btn_full = tk.Button(top, text='Fullscreen', command=self.toggle_fullscreen)
        btn_full.pack(side='left', padx=(6,0))
        
        # Style controls
        btn_text_color = tk.Button(top, text='Text Color', command=self.choose_text_color)
        btn_text_color.pack(side='left', padx=(8,0))
        
        btn_bg_color = tk.Button(top, text='BG Color', command=self.choose_bg_color)
        btn_bg_color.pack(side='left', padx=(6,0))
        
        self.shadow_var = tk.IntVar(value=1)
        chk_shadow = tk.Checkbutton(top, text='Shadow', variable=self.shadow_var, command=self.toggle_shadow)
        chk_shadow.pack(side='left', padx=(6,0))

        # Speed
        tk.Label(top, text='Speed').pack(side='left', padx=(16,2))
        self.speed_scale = tk.Scale(top, from_=1, to=20, orient='horizontal', command=self.on_speed_change)
        self.speed_scale.set(self.speed)
        self.speed_scale.pack(side='left')

        # Font size
        tk.Label(top, text='Font').pack(side='left', padx=(16,2))
        self.font_scale = tk.Scale(top, from_=18, to=120, orient='horizontal', command=self.on_font_change)
        self.font_scale.set(self.font_size)
        self.font_scale.pack(side='left')

        # Canvas for display
        self.canvas = tk.Canvas(self, bg='black')
        self.canvas.pack(fill='both', expand=True)

        # Default font
        self.display_font = font.Font(family='Courier', size=self.font_size)

        # Status bar
        self.status = tk.Label(self, text='Ready', anchor='w')
        self.status.pack(fill='x')

        # Load sample text by default if present
        sample = os.path.join(APP_DIR, 'sample_script.txt')
        if os.path.exists(sample):
            self.load_text(read_file(sample))
        else:
            self.load_text('Welcome to the Teleprompter. Click Open or Edit to load text.')
        
        # Progress bar (at bottom)
        self.progress_id = self.canvas.create_rectangle(0, 0, 0, 4, fill='#4caf50', width=0)

    def bind_events(self):
        self.bind('<space>', lambda e: self.toggle_start())
        self.bind('<F11>', lambda e: self.toggle_fullscreen())
        self.bind('<Up>', lambda e: self.adjust_speed(1))
        self.bind('<Down>', lambda e: self.adjust_speed(-1))
        self.bind('<plus>', lambda e: self.adjust_font(2))
        self.bind('<minus>', lambda e: self.adjust_font(-2))
    # mirror bindings removed

    def open_file(self):
        path = filedialog.askopenfilename(filetypes=[('Text files','*.txt;*.md;*.py;*.rtf'), ('All files','*.*')])
        if path:
            txt = read_file(path)
            if txt is not None:
                self.load_text(txt)

    def open_editor(self):
        editor = tk.Toplevel(self)
        editor.title('Edit Text')
        editor.geometry('700x500')
        txt = tk.Text(editor, wrap='word')
        txt.pack(fill='both', expand=True)
        txt.insert('1.0', self.text_content)
        def save_and_close():
            self.load_text(txt.get('1.0', 'end').rstrip('\n'))
            editor.destroy()
        btn = tk.Button(editor, text='Save', command=save_and_close)
        btn.pack()

    def choose_text_color(self):
        col = colorchooser.askcolor(title='Choose text color', initialcolor=self.text_color)
        if col and col[1]:
            self.text_color = col[1]
            self.render_text_on_canvas()

    def choose_bg_color(self):
        col = colorchooser.askcolor(title='Choose background color', initialcolor=self.bg_color)
        if col and col[1]:
            self.bg_color = col[1]
            self.canvas.config(bg=self.bg_color)
            self.render_text_on_canvas()

    def toggle_shadow(self):
        self.show_shadow = bool(self.shadow_var.get())
        self.render_text_on_canvas()
        

    def toggle_start(self):
        self.running = not self.running
        self.btn_start.config(text='Pause' if self.running else 'Start')
        self.status.config(text='Running' if self.running else 'Paused')
        if self.running:
            self.after(self.tick_ms, self.tick)

    def reset_scroll(self):
        # put text below the bottom so it scrolls up
        self.y_pos = self.canvas.winfo_height()
        # reposition all line items to start at y_pos
        if self.line_items:
            w = self.canvas.winfo_width()
            y = self.y_pos
            for shadow_id, text_id in self.line_items:
                # get text height from bbox
                bbox = self.canvas.bbox(text_id)
                th = (bbox[3] - bbox[1]) if bbox else int(self.font_size * 1.2)
                # place current line at y
                if shadow_id:
                    self.canvas.coords(shadow_id, w//2 + 2, y + 2)
                self.canvas.coords(text_id, w//2, y)
                y += th
        elif self.text_id:
            self.canvas.coords(self.text_id, self.canvas.winfo_width()//2, self.y_pos)
        self.status.config(text='Reset')

    # mirror removed

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        self.attributes('-fullscreen', self.fullscreen)
        self.status.config(text='Fullscreen On' if self.fullscreen else 'Fullscreen Off')

    def on_speed_change(self, val):
        try:
            self.speed = int(val)
        except Exception:
            pass

    def on_font_change(self, val):
        try:
            self.font_size = int(val)
            self.display_font.configure(size=self.font_size)
            # re-render
            self.render_text_on_canvas()
        except Exception:
            pass

    def adjust_speed(self, delta):
        self.speed = max(1, min(40, self.speed + delta))
        self.speed_scale.set(self.speed)

    def adjust_font(self, delta):
        self.font_size = max(8, min(200, self.font_size + delta))
        self.font_scale.set(self.font_size)
        self.display_font.configure(size=self.font_size)
        self.render_text_on_canvas()

    def load_text(self, txt):
        self.text_content = txt
        # simple load: render provided text
        self.render_text_on_canvas(text=txt)
        self.reset_scroll()

    def render_text_on_canvas(self, text=None):
        if text is None:
            text = self.text_content

        # clear canvas but keep progress bar id if present
        keep = getattr(self, 'progress_id', None)
        for iid in self.canvas.find_all():
            if iid != keep:
                self.canvas.delete(iid)

        w = self.canvas.winfo_width() or 800
        h = self.canvas.winfo_height() or 600

        # per-line canvas rendering for styling (shadow, per-line control)
        avg_char_w = self.display_font.measure('x') or 8
        wrap_width = int(w * 0.9)
        max_chars = max(20, wrap_width // max(1, avg_char_w))
        wrapped = []
        for paragraph in text.split('\n'):
            wrapped.extend(textwrap.wrap(paragraph, width=max_chars) or [''])

        self.line_items = []
        y = h
        spacing = max(2, int(self.font_size * 0.1))
        for line in wrapped:
            sid = None
            if self.show_shadow:
                sid = self.canvas.create_text(w//2 + 2, y + 2, text=line, font=self.display_font, fill='#000000', width=int(w*0.9), anchor='n')
            tid = self.canvas.create_text(w//2, y, text=line, font=self.display_font, fill=self.text_color, width=int(w*0.9), anchor='n')
            self.line_items.append((sid, tid))
            bbox = self.canvas.bbox(tid)
            th = (bbox[3] - bbox[1]) if bbox else int(self.font_size * 1.2)
            y += th + spacing
        self.y_pos = h
        self.total_text_height = max(0, y - h)
        self.total_scroll_distance = h + self.total_text_height

        # ensure progress bar exists and is on top
        if getattr(self, 'progress_id', None):
            ph = self.canvas.winfo_height()
            self.canvas.coords(self.progress_id, 0, ph-6, 0, ph)
        else:
            self.progress_id = self.canvas.create_rectangle(0, h-6, 0, h, fill='#4caf50', width=0)

    def tick(self):
        if not self.running:
            return

        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()

        if self.line_items:
            # move all line items
            for sid, tid in self.line_items:
                if sid:
                    self.canvas.move(sid, 0, -self.speed)
                self.canvas.move(tid, 0, -self.speed)
            self.y_pos -= self.speed

            # compute bottom-most y of text items
            max_bottom = -9999
            for sid, tid in self.line_items:
                bbox = self.canvas.bbox(tid)
                if bbox:
                    max_bottom = max(max_bottom, bbox[3])
            if max_bottom < 0:
                self.running = False
                self.btn_start.config(text='Start')
                self.status.config(text='Finished')
                return

            # update progress bar
            total = getattr(self, 'total_scroll_distance', None) or 1
            progress = min(1.0, max(0.0, (h - self.y_pos) / total))
            self.canvas.coords(self.progress_id, 0, h-6, int(progress * w), h)
            self.status.config(text=f'Running — {int(progress*100)}%')

        elif self.text_id:
            # image or single text
            self.y_pos -= self.speed
            self.canvas.coords(self.text_id, w//2, self.y_pos)
            bbox = self.canvas.bbox(self.text_id)
            if bbox and bbox[3] < 0:
                self.running = False
                self.btn_start.config(text='Start')
                self.status.config(text='Finished')
                return

            total = getattr(self, 'total_scroll_distance', None) or 1
            progress = min(1.0, max(0.0, (h - self.y_pos) / total))
            self.canvas.coords(self.progress_id, 0, h-6, int(progress * w), h)
            self.status.config(text=f'Running — {int(progress*100)}%')

        self.after(self.tick_ms, self.tick)

    def on_close(self):
        self.destroy()

if __name__ == '__main__':
    app = Teleprompter()
    # ensure canvas resizes update text
    def on_resize(event):
        app.render_text_on_canvas()
    app.canvas.bind('<Configure>', on_resize)
    app.mainloop()
