import tkinter as tk
from tkinter import ttk

# Ultra Modern Renk Paleti
COLORS = {
    # Primary - Modern Blue Gradient
    'primary': '#6366f1',  # Indigo
    'primary_dark': '#4f46e5',
    'primary_light': '#818cf8',
    'primary_gradient': ['#6366f1', '#8b5cf6'],  # Indigo to Purple
    
    # Accent Colors
    'accent_cyan': '#06b6d4',
    'accent_pink': '#ec4899',
    'accent_orange': '#f97316',
    'accent_emerald': '#10b981',
    
    # Status Colors
    'success': '#10b981',
    'success_light': '#34d399',
    'danger': '#ef4444',
    'danger_light': '#f87171',
    'warning': '#f59e0b',
    'warning_light': '#fbbf24',
    'info': '#3b82f6',
    'info_light': '#60a5fa',
    
    # Neutral Colors
    'dark': '#0f172a',  # Slate 900
    'dark_secondary': '#1e293b',  # Slate 800
    'dark_tertiary': '#334155',  # Slate 700
    'light': '#f8fafc',  # Slate 50
    'light_secondary': '#e2e8f0',  # Slate 200
    'light_tertiary': '#cbd5e1',  # Slate 300
    
    # Background
    'bg_primary': '#ffffff',
    'bg_secondary': '#f8fafc',
    'bg_dark': '#0f172a',
    'bg_dark_secondary': '#1e293b',
    
    # Text
    'text_primary': '#0f172a',
    'text_secondary': '#475569',
    'text_light': '#64748b',
    'text_white': '#ffffff',
    
    # Borders
    'border_light': '#e2e8f0',
    'border_medium': '#cbd5e1',
    'border_dark': '#94a3b8',
}

# Modern Fonts
FONTS = {
    'heading': ('Inter', 16, 'bold'),
    'subheading': ('Inter', 12, 'bold'),
    'body': ('Inter', 10, 'normal'),
    'body_bold': ('Inter', 10, 'bold'),
    'small': ('Inter', 9, 'normal'),
    'tiny': ('Inter', 8, 'normal'),
}

def apply_style(root):
    """Ultra modern, profesyonel stil uygula"""
    style = ttk.Style(root)
    
    # Modern tema seç
    try:
        style.theme_use('clam')
    except Exception:
        try:
            style.theme_use('alt')
        except Exception:
            pass
    
    # ========== NOTEBOOK (TABS) ==========
    style.configure('TNotebook', 
                   background=COLORS['bg_secondary'],
                   borderwidth=0,
                   tabmargins=[0, 0, 0, 0])
    
    style.configure('TNotebook.Tab',
                   padding=[24, 12],
                   font=FONTS['body_bold'],
                   background=COLORS['light_secondary'],
                   foreground=COLORS['text_secondary'],
                   borderwidth=0,
                   focuscolor='none')
    
    style.map('TNotebook.Tab',
             background=[('selected', COLORS['primary']),
                        ('active', COLORS['primary_light'])],
             foreground=[('selected', COLORS['text_white']),
                        ('active', COLORS['text_white']),
                        ('!selected', COLORS['text_secondary'])],
             expand=[('selected', [1, 1, 1, 0])])
    
    # ========== TREEVIEW (TABLES) ==========
    style.configure('Treeview',
                   rowheight=32,
                   font=FONTS['body'],
                   background=COLORS['bg_primary'],
                   foreground=COLORS['text_primary'],
                   fieldbackground=COLORS['bg_primary'],
                   borderwidth=0,
                   relief='flat')
    
    style.configure('Treeview.Heading',
                   font=FONTS['body_bold'],
                   background=COLORS['primary'],
                   foreground=COLORS['text_white'],
                   relief='flat',
                   borderwidth=0,
                   padding=[10, 8])
    
    style.map('Treeview',
             background=[('selected', COLORS['primary_light']),
                        ('focus', COLORS['primary_light'])],
             foreground=[('selected', COLORS['text_white']),
                        ('focus', COLORS['text_white'])])
    
    # Alternating row colors
    style.map('Treeview',
             background=[('!selected', COLORS['bg_primary'])],
             foreground=[('!selected', COLORS['text_primary'])])
    
    # ========== BUTTONS ==========
    style.configure('TButton',
                   padding=[16, 10],
                   font=FONTS['body_bold'],
                   relief='flat',
                   borderwidth=0,
                   background=COLORS['primary'],
                   foreground=COLORS['text_white'],
                   focuscolor='none',
                   cursor='hand2')
    
    style.map('TButton',
             background=[('active', COLORS['primary_dark']),
                        ('pressed', COLORS['primary_dark']),
                        ('!active', COLORS['primary'])],
             foreground=[('active', COLORS['text_white']),
                        ('pressed', COLORS['text_white']),
                        ('!active', COLORS['text_white'])],
             relief=[('pressed', 'flat'),
                    ('!pressed', 'flat')])
    
    # Success Button
    style.configure('Success.TButton',
                   background=COLORS['success'],
                   foreground=COLORS['text_white'])
    style.map('Success.TButton',
             background=[('active', COLORS['success_light']),
                        ('!active', COLORS['success'])])
    
    # Danger Button
    style.configure('Danger.TButton',
                   background=COLORS['danger'],
                   foreground=COLORS['text_white'])
    style.map('Danger.TButton',
             background=[('active', COLORS['danger_light']),
                        ('!active', COLORS['danger'])])
    
    # Warning Button
    style.configure('Warning.TButton',
                   background=COLORS['warning'],
                   foreground=COLORS['text_white'])
    style.map('Warning.TButton',
             background=[('active', COLORS['warning_light']),
                        ('!active', COLORS['warning'])])
    
    # ========== ENTRY FIELDS ==========
    style.configure('TEntry',
                   fieldbackground=COLORS['bg_primary'],
                   foreground=COLORS['text_primary'],
                   borderwidth=1,
                   relief='solid',
                   padding=[10, 8],
                   font=FONTS['body'],
                   bordercolor=COLORS['border_light'],
                   lightcolor=COLORS['border_light'],
                   darkcolor=COLORS['border_light'])
    
    style.map('TEntry',
             bordercolor=[('focus', COLORS['primary']),
                         ('!focus', COLORS['border_light'])],
             lightcolor=[('focus', COLORS['primary']),
                        ('!focus', COLORS['border_light'])],
             darkcolor=[('focus', COLORS['primary']),
                       ('!focus', COLORS['border_light'])])
    
    # ========== COMBOBOX ==========
    style.configure('TCombobox',
                   fieldbackground=COLORS['bg_primary'],
                   foreground=COLORS['text_primary'],
                   borderwidth=1,
                   relief='solid',
                   padding=[10, 8],
                   font=FONTS['body'],
                   bordercolor=COLORS['border_light'],
                   arrowcolor=COLORS['text_secondary'],
                   background=COLORS['bg_primary'])
    
    style.map('TCombobox',
             bordercolor=[('focus', COLORS['primary']),
                         ('!focus', COLORS['border_light'])],
             arrowcolor=[('active', COLORS['primary']),
                        ('!active', COLORS['text_secondary'])])
    
    # ========== LABELFRAME ==========
    style.configure('TLabelframe',
                   background=COLORS['bg_secondary'],
                   borderwidth=0,
                   relief='flat',
                   padding=16)
    
    style.configure('TLabelframe.Label',
                   font=FONTS['subheading'],
                   foreground=COLORS['text_primary'],
                   background=COLORS['bg_secondary'])
    
    # ========== SCROLLBAR ==========
    style.configure('TScrollbar',
                   background=COLORS['light_tertiary'],
                   troughcolor=COLORS['bg_secondary'],
                   borderwidth=0,
                   arrowcolor=COLORS['text_secondary'],
                   darkcolor=COLORS['light_tertiary'],
                   lightcolor=COLORS['light_tertiary'],
                   width=12,
                   gripcount=0)
    
    style.map('TScrollbar',
             background=[('active', COLORS['primary']),
                        ('!active', COLORS['light_tertiary'])],
             arrowcolor=[('active', COLORS['primary']),
                        ('!active', COLORS['text_secondary'])])
    
    # ========== FRAME ==========
    style.configure('TFrame',
                   background=COLORS['bg_secondary'],
                   relief='flat',
                   borderwidth=0)
    
    # ========== PANEDWINDOW ==========
    style.configure('TPanedwindow',
                   background=COLORS['bg_secondary'],
                   borderwidth=0)
    
    # ========== LABEL ==========
    style.configure('TLabel',
                   background=COLORS['bg_secondary'],
                   foreground=COLORS['text_primary'],
                   font=FONTS['body'])
    
    style.configure('Heading.TLabel',
                   font=FONTS['heading'],
                   foreground=COLORS['text_primary'])
    
    style.configure('Subheading.TLabel',
                   font=FONTS['subheading'],
                   foreground=COLORS['text_secondary'])
    
    # ========== TEXT WIDGET ==========
    root.option_add('*Text.background', COLORS['bg_primary'])
    root.option_add('*Text.foreground', COLORS['text_primary'])
    root.option_add('*Text.font', FONTS['body'])
    root.option_add('*Text.borderWidth', 1)
    root.option_add('*Text.relief', 'solid')
    root.option_add('*Text.highlightThickness', 0)
    root.option_add('*Text.insertBackground', COLORS['primary'])
    root.option_add('*Text.selectBackground', COLORS['primary_light'])
    root.option_add('*Text.selectForeground', COLORS['text_white'])
    
    # ========== ROOT WINDOW ==========
    root.configure(bg=COLORS['bg_secondary'])
    
    # Modern window styling
    try:
        root.attributes('-alpha', 0.98)  # Slight transparency for modern look
    except:
        pass

def get_risk_color(risk_score):
    """Risk skoruna göre renk döndür"""
    if risk_score >= 0.8:
        return COLORS['danger']
    elif risk_score >= 0.5:
        return COLORS['warning']
    elif risk_score >= 0.2:
        return COLORS['info']
    else:
        return COLORS['success']

def get_risk_bg_color(risk_score):
    """Risk skoruna göre arka plan rengi döndür"""
    if risk_score >= 0.8:
        return '#fee2e2'  # Red 100
    elif risk_score >= 0.5:
        return '#fef3c7'  # Yellow 100
    elif risk_score >= 0.2:
        return '#dbeafe'  # Blue 100
    else:
        return '#d1fae5'  # Green 100
