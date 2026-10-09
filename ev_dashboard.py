import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.linear_model import LinearRegression
import os

# Professional executive light theme settings
sns.set_theme(style="whitegrid")
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Segoe UI', 'Arial', 'Helvetica']
})

# --- AUTOMATED DATASET ROBUSTNESS & FALLBACK CHECK ---
try:
    df_raw = pd.read_csv('EV_vs_Fuel_Engines_and_Customer_Insights.csv')
    df_global = pd.read_csv('Global_EV_Market_Dataset_2020_2026.csv')
    
    if os.path.exists('master_ev_vs_ice_timeline_2030.csv'):
        df_timeline = pd.read_csv('master_ev_vs_ice_timeline_2030.csv')
    else:
        df_timeline = df_global.groupby(['Year', 'Vehicle_Type'])['Sales_Volume'].sum().reset_index()
        df_timeline['Data_Type'] = 'Actual'
        df_timeline.to_csv('master_ev_vs_ice_timeline_2030.csv', index=False)
except Exception as e:
    print(f"Dataset Loading Error: {e}")
    exit()

class RoundedButton(tk.Canvas):
    """Custom Modern Pill-Shaped Button inspired by Figma UI Kit styles"""
    def __init__(self, parent, text, command, bg_color="#1e293b", fg_color="#ffffff", 
                 accent_color="#38bdf8", height=48, font_style=("Segoe UI", 10, "bold")):
        super().__init__(parent, bg="#0f172a", highlightthickness=0, cursor="hand2", height=height)
        self.command = command
        self.text = text
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.accent_color = accent_color
        self.font_style = font_style
        self.button_height = height
        
        self.bind("<Configure>", self.redraw)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)
        self.is_hovered = False

    def redraw(self, event=None):
        self.delete("all")
        w = self.winfo_width()
        h = self.button_height
        if w < 10:
            w = 380
        r = h / 2
        
        current_bg = self.accent_color if self.is_hovered else self.bg_color
        border_color = self.accent_color if self.is_hovered else "#334155"
        
        if self.is_hovered:
            self.create_oval(1, 1, h-1, h-1, outline=self.accent_color, width=2)
            self.create_rectangle(r, 1, w-r, h-1, outline="", fill=self.accent_color)
            self.create_oval(w-h+1, 1, w-1, h-1, outline=self.accent_color, width=2)

        self.create_oval(4, 4, h-4, h-4, outline="", fill=current_bg)
        self.create_rectangle(r, 4, w-r, h-4, outline="", fill=current_bg)
        self.create_oval(w-h+4, 4, w-4, h-4, outline="", fill=current_bg)

        self.create_oval(4, 4, h-4, h-4, outline=border_color, width=1.5)
        self.create_rectangle(r, 4, w-r, h-4, outline="", fill=current_bg) 
        self.create_line(r, 4, w-r, 4, fill=border_color, width=1.5)
        self.create_line(r, h-4, w-r, h-4, fill=border_color, width=1.5)
        self.create_oval(w-h+4, 4, w-4, h-4, outline=border_color, width=1.5)

        self.create_text(w/2, h/2, text=self.text, fill=self.fg_color, font=self.font_style)

    def on_enter(self, event):
        self.is_hovered = True
        self.redraw()

    def on_leave(self, event):
        self.is_hovered = False
        self.redraw()

    def on_click(self, event):
        if self.command:
            self.command()


class ExecutiveDashboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Automotive Market Intelligence & Forecasting | Executive Suite")
        self.root.state('zoomed')
        self.root.configure(bg="#f1f5f9")

        self.current_view = "home"
        self.drilldown_filter = None
        self.anim_job = None

        self.sidebar_frame = tk.Frame(root, bg="#0f172a", width=420)
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar_frame.pack_propagate(False)

        self.main_workspace = tk.Frame(root, bg="#f1f5f9")
        self.main_workspace.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

        self.create_kpi_banner()

        self.content_container = tk.Frame(self.main_workspace, bg="#f1f5f9")
        self.content_container.pack(expand=True, fill=tk.BOTH, padx=20, pady=(0, 20))

        self.content_frame = tk.Frame(self.content_container, bg="#ffffff", bd=1, relief=tk.SOLID)
        self.content_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.fig, self.ax = plt.subplots(figsize=(9, 4.8))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.content_frame)
        self.canvas.get_tk_widget().pack(expand=True, fill=tk.BOTH, padx=15, pady=15)

        self.car_anim_label = tk.Label(self.content_frame, bg="#ffffff")
        self.load_car_animation_frames()

        self.annot = self.ax.annotate("", xy=(0,0), xytext=(-20,20),
                            textcoords="offset points",
                            bbox=dict(boxstyle="round,pad=0.5", fc="#1e293b", ec="#38bdf8", alpha=0.9),
                            arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0", color="#38bdf8"))
        self.annot.set_visible(False)

        self.canvas.mpl_connect('motion_notify_event', self.on_hover)
        self.canvas.mpl_connect('pick_event', self.on_pick)

        self.show_executive_overview()

    def load_car_animation_frames(self):
        self.car_frames = []
        anim_path = 'car_animation.gif'
        if os.path.exists(anim_path):
            try:
                im = Image.open(anim_path)
                for frame in range(im.n_frames):
                    im.seek(frame)
                    resized = im.copy().resize((140, 70), Image.Resampling.LANCZOS)
                    self.car_frames.append(ImageTk.PhotoImage(resized))
                self.anim_idx = 0
                self.play_car_animation()
            except Exception:
                pass

    def play_car_animation(self):
        if self.car_frames:
            self.car_anim_label.configure(image=self.car_frames[self.anim_idx])
            self.anim_idx = (self.anim_idx + 1) % len(self.car_frames)
            self.root.after(100, self.play_car_animation)

    def animate_transition(self, render_callback):
        if self.anim_job:
            self.root.after_cancel(self.anim_job)
            self.anim_job = None

        def step(progress=0.0):
            if progress < 1.0:
                eased = 1 - pow(1 - progress, 3)
                offset = (1 - eased) * 0.08
                self.content_frame.place(relx=offset, rely=0, relwidth=1.0, relheight=1.0)
                self.root.after(12, lambda: step(progress + 0.12))
            else:
                self.content_frame.place(relx=0, rely=0, relwidth=1.0, relheight=1.0)

        render_callback()
        step(0.0)

    def create_kpi_banner(self):
        kpi_frame = tk.Frame(self.main_workspace, bg="#f1f5f9", height=90)
        kpi_frame.pack(fill=tk.X, padx=20, pady=20)
        kpi_frame.pack_propagate(False)

        total_vol = f"{df_timeline['Sales_Volume'].sum():,.0f}"
        avg_price_usd = df_raw['Average_Price_USD'].mean()
        avg_price_inr = avg_price_usd * 95.85
        avg_price_str = f"₹{avg_price_inr:,.0f}"
        avg_satisfaction = f"{df_raw['Customer_Satisfaction_Rating'].mean():.2f} / 5.0"
        market_leaders = "EV & Hybrid Adoption"

        cards = [
            ("TOTAL MARKET VOLUME", total_vol, "#0284c7"),
            ("AVG VEHICLE PRICE (INR)", avg_price_str, "#d97706"),
            ("CUSTOMER SATISFACTION", avg_satisfaction, "#059669"),
            ("PRIMARY DRIVER", market_leaders, "#7c3aed")
        ]

        for title, val, color in cards:
            card = tk.Frame(kpi_frame, bg="#ffffff", bd=1, relief=tk.RAISED)
            card.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5)
            
            tk.Label(card, text=title, bg="#ffffff", fg="#64748b", font=("Segoe UI", 9, "bold")).pack(anchor='w', padx=12, pady=(10, 0))
            tk.Label(card, text=val, bg="#ffffff", fg=color, font=("Segoe UI", 14, "bold")).pack(anchor='w', padx=12, pady=(5, 10))

    def clear_sidebar(self):
        for widget in self.sidebar_frame.winfo_children():
            widget.destroy()

    def style_axes(self):
        self.fig.patch.set_facecolor('#ffffff')
        self.ax.set_facecolor('#ffffff')
        self.ax.tick_params(axis='x', colors='#334155', labelsize=10)
        self.ax.tick_params(axis='y', colors='#334155', labelsize=10)
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['left'].set_color('#cbd5e1')
        self.ax.spines['bottom'].set_color('#cbd5e1')
        self.ax.grid(True, color='#e2e8f0', linestyle='--', alpha=0.7)

    def on_hover(self, event):
        if event.inaxes == self.ax:
            vis = self.annot.get_visible()
            hit = False
            for child in self.ax.get_children():
                if hasattr(child, "contains") and not isinstance(child, plt.Axes):
                    contains, attr = child.contains(event)
                    if contains:
                        hit = True
                        pos = event.xdata, event.ydata
                        if pos[0] is not None and pos[1] is not None:
                            self.annot.xy = (pos[0], pos[1])
                            text = f"Year: {round(pos[0])}\nVolume: {pos[1]:,.0f}"
                            self.annot.set_text(text)
                            self.annot.set_visible(True)
                            self.canvas.draw_idle()
                            break
            if not hit and vis:
                self.annot.set_visible(False)
                self.canvas.draw_idle()

    def on_pick(self, event):
        if self.current_view == "sales_trend" and hasattr(event, 'ind'):
            ind = event.ind[0]
            plot_df = df_timeline.copy()
            clicked_year = int(plot_df.iloc[ind]['Year'])
            self.drilldown_filter = clicked_year
            self.animate_transition(lambda: self.show_drilldown_view(f"Granular Powertrain Breakdown for Year: {clicked_year}"))

    # --- NAVIGATION & VIEWS ---
    def show_executive_overview(self):
        self.current_view = "home"
        self.clear_sidebar()
        self.car_anim_label.place(relx=0.78, rely=0.78)
        
        if self.anim_job:
            self.root.after_cancel(self.anim_job)
            self.anim_job = None

        def render_stylish_home():
            self.fig.patch.set_facecolor('#ffffff')
            self.fig.clf()
            self.ax = self.fig.add_subplot(111)
            self.ax.set_facecolor('#ffffff')
            self.ax.axis('off')

            self.ax.text(0.5, 0.78, "AUTOMOTIVE MARKET INTELLIGENCE", fontsize=22, fontweight='extra bold', color='#0f172a', ha='center', va='center')
            self.ax.text(0.5, 0.61, "Global EV vs. ICE Forecasting & Customer Analytics Suite (2020–2030)", fontsize=15, fontweight='bold', color='#0284c7', ha='center', va='center')
            self.ax.text(0.5, 0.43, "✦   End-to-End Data Architecture (Excel, Python, SQL, Power BI Framework)", fontsize=11, fontweight='bold', color='#1e293b', ha='center', va='center')
            self.ax.text(0.5, 0.31, "✦   Real-Time KPI Tracking, Pricing Analysis in INR, & Interactive Drill-Downs", fontsize=11, fontweight='bold', color='#1e293b', ha='center', va='center')

            self.canvas.draw()

        self.animate_transition(render_stylish_home)

        tk.Label(self.sidebar_frame, text="EXECUTIVE CONTROLS", bg="#0f172a", fg="#38bdf8", font=("Segoe UI", 13, "bold")).pack(pady=(15, 8))
        
        btn_configs = [
            ("📊  Sales & Market Trends", self.show_sales_menu, "#0284c7"),
            ("👥  Customer Insights", self.show_customer_menu, "#0d9488"),
            ("🚗  Vehicle Specs & Analytics", self.show_specs_menu, "#7c3aed"),
            ("🌍  Geographic Region Analysis", self.show_region_menu, "#2563eb"),
            ("🏢  Manufacturer Competitiveness", self.show_manufacturer_menu, "#d97706"),
            ("💰  Pricing & Incentives", self.show_pricing_menu, "#059669"),
            ("⚡  Battery & Range Technology", self.show_tech_menu, "#4f46e5"),
            ("🍃  Environmental & CO2 Impact", self.show_environmental_menu, "#16a34a"),
            ("🔮  Market Forecasting & Predictions", lambda: self.animate_transition(self.plot_ml_predictions), "#d946ef")
        ]

        for text, cmd, accent in btn_configs:
            RoundedButton(self.sidebar_frame, text, cmd, bg_color="#1e293b", accent_color=accent, height=48).pack(fill=tk.X, expand=True, padx=15, pady=3)

    def show_sales_menu(self):
        if self.anim_job:
            self.root.after_cancel(self.anim_job)
            self.anim_job = None
        self.clear_sidebar()
        self.car_anim_label.place_forget()
        
        tk.Label(self.sidebar_frame, text="Sales & Forecasting", bg="#0f172a", fg="#38bdf8", font=("Segoe UI", 13, "bold")).pack(pady=(20, 10))
        
        sub_configs = [
            ("Sales Trend Line (2020-2030)", lambda: self.animate_transition(self.plot_sales_trend), "#0284c7"),
            ("Annual Volume Breakdown", lambda: self.animate_transition(self.plot_sales_bar), "#ea580c"),
            ("EV Growth Trajectory", lambda: self.animate_transition(self.plot_ev_growth), "#0891b2"),
            ("ICE Fuel Stability", lambda: self.animate_transition(self.plot_ice_stability), "#c2410c"),
            ("🏠 Executive Home", self.show_executive_overview, "#64748b")
        ]

        for text, cmd, accent in sub_configs:
            RoundedButton(self.sidebar_frame, text, cmd, bg_color="#1e293b", accent_color=accent, height=58).pack(fill=tk.X, expand=True, padx=15, pady=5)
        
        self.animate_transition(self.plot_sales_trend)

    def show_customer_menu(self):
        if self.anim_job:
            self.root.after_cancel(self.anim_job)
            self.anim_job = None
        self.clear_sidebar()
        self.car_anim_label.place_forget()
        
        tk.Label(self.sidebar_frame, text="Customer Insights", bg="#0f172a", fg="#2dd4bf", font=("Segoe UI", 13, "bold")).pack(pady=(20, 10))
        
        sub_configs = [
            ("Customer Preferences", lambda: self.animate_transition(self.plot_customer_pref), "#0d9488"),
            ("Satisfaction Ratings", lambda: self.animate_transition(self.plot_satisfaction), "#db2777"),
            ("Market Share Impact", lambda: self.animate_transition(self.plot_market_share), "#7c3aed"),
            ("🏠 Executive Home", self.show_executive_overview, "#64748b")
        ]

        for text, cmd, accent in sub_configs:
            RoundedButton(self.sidebar_frame, text, cmd, bg_color="#1e293b", accent_color=accent, height=58).pack(fill=tk.X, expand=True, padx=15, pady=5)
        
        self.animate_transition(self.plot_customer_pref)

    def show_specs_menu(self):
        if self.anim_job:
            self.root.after_cancel(self.anim_job)
            self.anim_job = None
        self.clear_sidebar()
        self.car_anim_label.place_forget()
        
        tk.Label(self.sidebar_frame, text="Vehicle Specs & Stats", bg="#0f172a", fg="#a78bfa", font=("Segoe UI", 13, "bold")).pack(pady=(20, 10))
        
        sub_configs = [
            ("Feature Correlation Matrix", lambda: self.animate_transition(self.plot_heatmap), "#7c3aed"),
            ("Price vs Range Analysis", lambda: self.animate_transition(self.plot_price_range), "#d97706"),
            ("Fuel Efficiency Dist.", lambda: self.animate_transition(self.plot_efficiency), "#16a34a"),
            ("🏠 Executive Home", self.show_executive_overview, "#64748b")
        ]

        for text, cmd, accent in sub_configs:
            RoundedButton(self.sidebar_frame, text, cmd, bg_color="#1e293b", accent_color=accent, height=58).pack(fill=tk.X, expand=True, padx=15, pady=5)
        
        self.animate_transition(self.plot_heatmap)

    def show_region_menu(self):
        if self.anim_job:
            self.root.after_cancel(self.anim_job)
            self.anim_job = None
        self.clear_sidebar()
        self.car_anim_label.place_forget()
        
        tk.Label(self.sidebar_frame, text="Geographic Distribution", bg="#0f172a", fg="#60a5fa", font=("Segoe UI", 13, "bold")).pack(pady=(20, 10))
        
        sub_configs = [
            ("Sales Volume by Region", lambda: self.animate_transition(self.plot_region_sales), "#2563eb"),
            ("Global Charging Infrastructure", lambda: self.animate_transition(self.plot_charging_stations), "#0284c7"),
            ("🏠 Executive Home", self.show_executive_overview, "#64748b")
        ]

        for text, cmd, accent in sub_configs:
            RoundedButton(self.sidebar_frame, text, cmd, bg_color="#1e293b", accent_color=accent, height=68).pack(fill=tk.X, expand=True, padx=15, pady=6)
        
        self.animate_transition(self.plot_region_sales)

    def show_manufacturer_menu(self):
        if self.anim_job:
            self.root.after_cancel(self.anim_job)
            self.anim_job = None
        self.clear_sidebar()
        self.car_anim_label.place_forget()
        
        tk.Label(self.sidebar_frame, text="Manufacturer Competitiveness", bg="#0f172a", fg="#fbbf24", font=("Segoe UI", 13, "bold")).pack(pady=(20, 10))
        
        sub_configs = [
            ("Top Manufacturers Comparison", lambda: self.animate_transition(self.plot_manufacturer_share), "#d97706"),
            ("🏠 Executive Home", self.show_executive_overview, "#64748b")
        ]

        for text, cmd, accent in sub_configs:
            RoundedButton(self.sidebar_frame, text, cmd, bg_color="#1e293b", accent_color=accent, height=78).pack(fill=tk.X, expand=True, padx=15, pady=8)
        
        self.animate_transition(self.plot_manufacturer_share)

    def show_pricing_menu(self):
        if self.anim_job:
            self.root.after_cancel(self.anim_job)
            self.anim_job = None
        self.clear_sidebar()
        self.car_anim_label.place_forget()
        
        tk.Label(self.sidebar_frame, text="Pricing & Incentives", bg="#0f172a", fg="#34d399", font=("Segoe UI", 13, "bold")).pack(pady=(20, 10))
        
        sub_configs = [
            ("Government Incentives Impact", lambda: self.animate_transition(self.plot_incentives), "#059669"),
            ("🏠 Executive Home", self.show_executive_overview, "#64748b")
        ]

        for text, cmd, accent in sub_configs:
            RoundedButton(self.sidebar_frame, text, cmd, bg_color="#1e293b", accent_color=accent, height=78).pack(fill=tk.X, expand=True, padx=15, pady=8)
        
        self.animate_transition(self.plot_incentives)

    def show_tech_menu(self):
        if self.anim_job:
            self.root.after_cancel(self.anim_job)
            self.anim_job = None
        self.clear_sidebar()
        self.car_anim_label.place_forget()
        
        tk.Label(self.sidebar_frame, text="Battery & Range Technology", bg="#0f172a", fg="#818cf8", font=("Segoe UI", 13, "bold")).pack(pady=(20, 10))
        
        sub_configs = [
            ("Average Range by Powertrain", lambda: self.animate_transition(self.plot_tech_range), "#4f46e5"),
            ("Running Cost Efficiency", lambda: self.animate_transition(self.plot_running_cost), "#6366f1"),
            ("🏠 Executive Home", self.show_executive_overview, "#64748b")
        ]

        for text, cmd, accent in sub_configs:
            RoundedButton(self.sidebar_frame, text, cmd, bg_color="#1e293b", accent_color=accent, height=68).pack(fill=tk.X, expand=True, padx=15, pady=6)
        
        self.animate_transition(self.plot_tech_range)

    def show_environmental_menu(self):
        if self.anim_job:
            self.root.after_cancel(self.anim_job)
            self.anim_job = None
        self.clear_sidebar()
        self.car_anim_label.place_forget()
        
        tk.Label(self.sidebar_frame, text="Environmental Impact", bg="#0f172a", fg="#4ade80", font=("Segoe UI", 13, "bold")).pack(pady=(20, 10))
        
        sub_configs = [
            ("CO2 Emissions Saved (Tons)", lambda: self.animate_transition(self.plot_co2_savings), "#16a34a"),
            ("🏠 Executive Home", self.show_executive_overview, "#64748b")
        ]

        for text, cmd, accent in sub_configs:
            RoundedButton(self.sidebar_frame, text, cmd, bg_color="#1e293b", accent_color=accent, height=78).pack(fill=tk.X, expand=True, padx=15, pady=8)
        
        self.animate_transition(self.plot_co2_savings)

    # --- PLOTTING & PREDICTION ENGINE WITH EXPLICIT VEHICLE TYPE LABELS ---
    def prepare_ax(self):
        self.fig.clf()
        self.ax = self.fig.add_subplot(111)

    def plot_sales_trend(self):
        self.current_view = "sales_trend"
        self.prepare_ax()
        self.style_axes()
        plot_df = df_timeline.copy()
        plot_df['Vehicle_Type'] = plot_df['Vehicle_Type'].str.replace('_', ' ')
        
        sns.lineplot(data=plot_df, x='Year', y='Sales_Volume', hue='Vehicle_Type', style='Data_Type', marker='o', linewidth=3, ax=self.ax, palette=['#0284c7', '#ea580c'])
        for line in self.ax.get_lines():
            line.set_picker(8)

        self.ax.set_title('Global EV (Blue) vs ICE (Orange) Sales Trend & Forecast (2020-2030)', fontsize=12, fontweight='bold', color='#0f172a', pad=15)
        self.ax.set_ylabel('Total Sales Volume (Units)', fontsize=11, fontweight='bold', color='#334155', labelpad=8)
        self.ax.set_xlabel('Timeline Year (Click marker point for drill-down)', fontsize=11, fontweight='bold', color='#334155', labelpad=8)
        self.ax.legend(title='Vehicle & Data Type', loc='upper left', frameon=True, facecolor='#ffffff', labelcolor='#334155', fontsize='9')
        self.canvas.draw()

    def show_drilldown_view(self, title_text):
        self.current_view = "drilldown"
        self.prepare_ax()
        self.style_axes()
        
        filtered_df = df_timeline[df_timeline['Year'] == self.drilldown_filter]
        bars = sns.barplot(data=filtered_df, x='Vehicle_Type', y='Sales_Volume', hue='Data_Type', ax=self.ax, palette='Set2')
        
        for p in self.ax.patches:
            height = p.get_height()
            if height > 0:
                self.ax.annotate(f"{height:,.0f}",
                                (p.get_x() + p.get_width() / 2., height),
                                ha='center', va='bottom', fontsize=9, fontweight='bold', color='#0f172a', xytext=(0, 3), textcoords='offset points')

        self.ax.set_title(title_text, fontsize=12, fontweight='bold', color='#0f172a', pad=15)
        self.ax.set_ylabel('Sales Volume (Units)', fontsize=11, fontweight='bold', color='#334155', labelpad=8)
        self.ax.set_xlabel('Vehicle Powertrain Type (EV vs ICE)', fontsize=11, fontweight='bold', color='#334155', labelpad=8)
        self.ax.legend(loc='upper right', frameon=True, facecolor='#ffffff', labelcolor='#334155', fontsize='9')
        self.canvas.draw()

    def plot_sales_bar(self):
        self.current_view = "other"
        self.prepare_ax()
        self.style_axes()
        pivot_df = df_timeline.pivot_table(index='Year', columns='Vehicle_Type', values='Sales_Volume', aggfunc='sum')
        pivot_df.columns = pivot_df.columns.str.replace('_', ' ')
        ax = pivot_df.plot(kind='bar', ax=self.ax, width=0.65, edgecolor='#ffffff', alpha=0.95, color=['#0284c7', '#ea580c'])
        
        for p in ax.patches:
            height = p.get_height()
            if height > 0:
                ax.annotate(f"{height:,.0f}", (p.get_x() + p.get_width() / 2., height),
                            ha='center', va='bottom', fontsize=8, fontweight='bold', color='#0f172a', rotation=45)

        self.ax.set_title('Annual Sales Breakdown: Blue = Electric Vehicle (EV) | Orange = ICE Fuel', fontsize=12, fontweight='bold', color='#0f172a', pad=15)
        self.ax.set_ylabel('Total Sales Volume (Units)', fontsize=11, fontweight='bold', color='#334155', labelpad=8)
        self.ax.set_xlabel('Timeline Year', fontsize=11, fontweight='bold', color='#334155', labelpad=8)
        self.ax.set_xticklabels(pivot_df.index, rotation=0)
        self.ax.legend(title='Vehicle Type (EV / ICE)', title_fontsize='9', fontsize='9', facecolor='#ffffff', labelcolor='#334155')
        self.canvas.draw()

    def plot_ev_growth(self):
        self.current_view = "other"
        self.prepare_ax()
        self.style_axes()
        ev_df = df_timeline[df_timeline['Vehicle_Type'] == 'EV']
        ax = sns.barplot(data=ev_df, x='Year', y='Sales_Volume', hue='Data_Type', ax=self.ax, palette='Blues_r')
        
        for p in ax.patches:
            height = p.get_height()
            if height > 0:
                ax.annotate(f"{height:,.0f}", (p.get_x() + p.get_width() / 2., height),
                            ha='center', va='bottom', fontsize=8, fontweight='bold', color='#0f172a', rotation=45)

        self.ax.set_title('Electric Vehicle (EV) Growth Trajectory (Historical vs Forecast)', fontsize=12, fontweight='bold', color='#0f172a', pad=15)
        self.ax.set_ylabel('EV Sales Volume (Units)', fontsize=11, fontweight='bold', color='#334155', labelpad=8)
        self.ax.set_xlabel('Timeline Year', fontsize=11, fontweight='bold', color='#334155', labelpad=8)
        self.ax.legend(title='EV Data Type', title_fontsize='9', fontsize='9', facecolor='#ffffff', labelcolor='#334155')
        self.canvas.draw()

    def plot_ice_stability(self):
        self.current_view = "other"
        self.prepare_ax()
        self.style_axes()
        ice_df = df_timeline[df_timeline['Vehicle_Type'] == 'ICE_Fuel']
        ax = sns.barplot(data=ice_df, x='Year', y='Sales_Volume', hue='Data_Type', ax=self.ax, palette='Oranges_r')
        
        for p in ax.patches:
            height = p.get_height()
            if height > 0:
                ax.annotate(f"{height:,.0f}", (p.get_x() + p.get_width() / 2., height),
                            ha='center', va='bottom', fontsize=8, fontweight='bold', color='#0f172a', rotation=45)

        self.ax.set_title('Traditional ICE Fuel Engines Trend Analysis (Historical vs Forecast)', fontsize=12, fontweight='bold', color='#0f172a', pad=15)
        self.ax.set_ylabel('ICE Sales Volume (Units)', fontsize=11, fontweight='bold', color='#334155', labelpad=8)
        self.ax.set_xlabel('Timeline Year', fontsize=11, fontweight='bold', color='#334155', labelpad=8)
        self.ax.legend(title='ICE Data Type', title_fontsize='9', fontsize='9', facecolor='#ffffff', labelcolor='#334155')
        self.canvas.draw()

    def plot_customer_pref(self):
        self.current_view = "other"
        self.prepare_ax()
        self.style_axes()
        pref_counts = df_raw.groupby(['Powertrain_Type', 'Customer_Primary_Preference'])['Sales_Volume'].sum().reset_index()
        pref_counts['Customer_Primary_Preference'] = pref_counts['Customer_Primary_Preference'].str.replace('_', ' ')
        sns.barplot(data=pref_counts, x='Customer_Primary_Preference', y='Sales_Volume', hue='Powertrain_Type', ax=self.ax, palette='muted')
        self.ax.set_title('Customer Primary Preferences Grouped by Powertrain Type (EV / Hybrid / ICE)', fontsize=12, fontweight='bold', color='#0f172a', pad=15)
        self.ax.set_xlabel('Primary Preference Factor', fontsize=11, fontweight='bold', color='#334155', labelpad=8)
        self.ax.set_ylabel('Total Sales Volume (Units)', fontsize=11, fontweight='bold', color='#334155', labelpad=8)
        self.ax.tick_params(axis='x', rotation=15)
        self.ax.legend(title='Vehicle Powertrain', title_fontsize='9', fontsize='9', facecolor='#ffffff', labelcolor='#334155')
        self.canvas.draw()

    def plot_satisfaction(self):
        self.current_view = "other"
        self.prepare_ax()
        self.style_axes()
        sat_data = df_raw.groupby('Powertrain_Type')['Customer_Satisfaction_Rating'].mean().reset_index()
        sat_data['Powertrain_Type'] = sat_data['Powertrain_Type'].str.replace('_', ' ')
        ax = sns.barplot(data=sat_data, x='Powertrain_Type', y='Customer_Satisfaction_Rating', hue='Powertrain_Type', palette='crest', ax=self.ax, legend=False)
        
        for p in ax.patches:
            height = p.get_height()
            ax.annotate(f"{height:.2f}", (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='bottom', fontsize=9, fontweight='bold', color='#0f172a', xytext=(0, 3), textcoords='offset points')

        self.ax.set_title('Average Customer Satisfaction Rating by Powertrain Type', fontsize=12, fontweight='bold', color='#0f172a', pad=15)
        self.ax.set_ylabel('Satisfaction Rating (0 - 5 Scale)', fontsize=11, fontweight='bold', color='#334155', labelpad=8)
        self.ax.set_xlabel('Powertrain Category', fontsize=11, fontweight='bold', color='#334155', labelpad=8)
        self.ax.set_ylim(0, 5.5)
        self.canvas.draw()

    def plot_market_share(self):
        self.current_view = "other"
        self.prepare_ax()
        self.style_axes()
        pref_share = df_raw.groupby('Customer_Primary_Preference')['Sales_Volume'].sum().reset_index()
        pref_share['Customer_Primary_Preference'] = pref_share['Customer_Primary_Preference'].str.replace('_', ' ')
        sns.lineplot(data=pref_share, x='Customer_Primary_Preference', y='Sales_Volume', marker='s', color='#7c3aed', linewidth=3, ax=self.ax)
        self.ax.set_title('Overall Market Share Impact per Preference Factor', fontsize=12, fontweight='bold', color='#0f172a', pad=15)
        self.ax.set_xlabel('Primary Preference Factor', fontsize=11, fontweight='bold', color='#334155', labelpad=8)
        self.ax.set_ylabel('Total Sales Volume (Units)', fontsize=11, fontweight='bold', color='#334155', labelpad=8)
        self.ax.tick_params(axis='x', rotation=15)
        self.canvas.draw()

    def plot_heatmap(self):
        self.current_view = "other"
        self.prepare_ax()
        self.style_axes()
        numeric_cols = ['Sales_Volume', 'Average_Price_USD', 'Fuel_Efficiency_Km_Per_Litre', 'Vehicle_Range_Km', 'Customer_Satisfaction_Rating']
        corr = df_raw[numeric_cols].corr()
        clean_labels = ['Sales Vol', 'Avg Price', 'Efficiency', 'Range', 'Satisfaction']
        sns.heatmap(corr, annot=True, cmap='Blues', fmt=".2f", linewidths=0.6, xticklabels=clean_labels, yticklabels=clean_labels, ax=self.ax, annot_kws={"size": 9, "weight": "bold"})
        self.ax.set_title('Feature Correlation Matrix Deep Dive', fontsize=12, fontweight='bold', color='#0f172a', pad=15)
        self.canvas.draw()

    def plot_price_range(self):
        self.current_view = "other"
        self.prepare_ax()
        self.style_axes()
        plot_data = df_raw.copy()
        plot_data['Average_Price_INR'] = plot_data['Average_Price_USD'] * 95.85
        sns.scatterplot(data=plot_data, x='Vehicle_Range_Km', y='Average_Price_INR', hue='Powertrain_Type', alpha=0.85, s=60, ax=self.ax, palette='tab10')
        self.ax.set_title('Vehicle Range vs. Average Price (INR) by Vehicle Powertrain', fontsize=12, fontweight='bold', color='#0f172a', pad=15)
        self.ax.set_xlabel('Vehicle Range (km)', fontsize=11, fontweight='bold', color='#334155', labelpad=8)
        self.ax.set_ylabel('Average Price (₹)', fontsize=11, fontweight='bold', color='#334155', labelpad=8)
        self.ax.legend(title='Vehicle Powertrain Type', title_fontsize='9', fontsize='9', facecolor='#ffffff', labelcolor='#334155')
        self.canvas.draw()

    def plot_efficiency(self):
        self.current_view = "other"
        self.prepare_ax()
        self.style_axes()
        sns.histplot(data=df_raw, x='Fuel_Efficiency_Km_Per_Litre', hue='Powertrain_Type', kde=True, bins=15, ax=self.ax, palette='Set2')
        self.ax.set_title('Fuel Efficiency & Energy Consumption Distribution by Powertrain', fontsize=12, fontweight='bold', color='#0f172a', pad=15)
        self.ax.set_xlabel('Fuel Efficiency (km/L)', fontsize=11, fontweight='bold', color='#334155', labelpad=8)
        self.ax.set_ylabel('Frequency Count', fontsize=11, fontweight='bold', color='#334155', labelpad=8)
        self.ax.legend(title='Powertrain Type', title_fontsize='9', fontsize='9', facecolor='#ffffff', labelcolor='#334155')
        self.canvas.draw()

    def plot_region_sales(self):
        self.current_view = "other"
        self.prepare_ax()
        self.style_axes()
        region_df = df_raw.groupby('Region')['Sales_Volume'].sum().reset_index()
        ax = sns.barplot(data=region_df, x='Region', y='Sales_Volume', palette='Blues_r', ax=self.ax)
        
        for p in ax.patches:
            height = p.get_height()
            ax.annotate(f"{height:,.0f}", (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='bottom', fontsize=9, fontweight='bold', color='#0f172a', xytext=(0, 3), textcoords='offset points')

        self.ax.set_title('Geographic Distribution: Total Sales Volume by Region', fontsize=12, fontweight='bold', color='#0f172a', pad=15)
        self.ax.set_xlabel('Geographic Region', fontsize=11, fontweight='bold', color='#334155', labelpad=8)
        self.ax.set_ylabel('Total Sales Volume (Units)', fontsize=11, fontweight='bold', color='#334155', labelpad=8)
        self.canvas.draw()

    def plot_charging_stations(self):
        self.current_view = "other"
        self.prepare_ax()
        self.style_axes()
        infra_df = df_global.groupby('Country')['Charging_Stations'].sum().reset_index().sort_values(by='Charging_Stations', ascending=False).head(8)
        ax = sns.barplot(data=infra_df, x='Country', y='Charging_Stations', palette='magma', ax=self.ax)
        
        for p in ax.patches:
            height = p.get_height()
            ax.annotate(f"{height:,.0f}", (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='bottom', fontsize=8, fontweight='bold', color='#0f172a', rotation=30, xytext=(0, 3), textcoords='offset points')

        self.ax.set_title('Top Countries by EV Charging Infrastructure Expansion', fontsize=12, fontweight='bold', color='#0f172a', pad=15)
        self.ax.set_xlabel('Country', fontsize=11, fontweight='bold', color='#334155', labelpad=8)
        self.ax.set_ylabel('Charging Stations Count', fontsize=11, fontweight='bold', color='#334155', labelpad=8)
        self.canvas.draw()

    def plot_manufacturer_share(self):
        self.current_view = "other"
        self.prepare_ax()
        self.style_axes()
        mfg_df = df_raw.groupby('Manufacturer')['Sales_Volume'].sum().reset_index().sort_values(by='Sales_Volume', ascending=False).head(8)
        ax = sns.barplot(data=mfg_df, x='Sales_Volume', y='Manufacturer', palette='Spectral', ax=self.ax)
        
        for p in ax.patches:
            width = p.get_width()
            ax.annotate(f"{width:,.0f}", (width, p.get_y() + p.get_height() / 2.),
                        ha='left', va='center', fontsize=8, fontweight='bold', color='#0f172a', xytext=(3, 0), textcoords='offset points')

        self.ax.set_title('Top Manufacturer Competitiveness & Sales Volume', fontsize=12, fontweight='bold', color='#0f172a', pad=15)
        self.ax.set_xlabel('Total Sales Volume (Units)', fontsize=11, fontweight='bold', color='#334155', labelpad=8)
        self.ax.set_ylabel('Manufacturer', fontsize=11, fontweight='bold', color='#334155', labelpad=8)
        self.canvas.draw()

    def plot_incentives(self):
        self.current_view = "other"
        self.prepare_ax()
        self.style_axes()
        plot_global = df_global.copy()
        plot_global['Incentive_INR'] = plot_global['Government_Incentive_USD'] * 95.85
        sns.scatterplot(data=plot_global, x='Incentive_INR', y='Sales_Volume', hue='Vehicle_Type', s=70, ax=self.ax, palette='deep')
        self.ax.set_title('Government Incentives (INR) vs. Vehicle Type Sales Volume Impact', fontsize=12, fontweight='bold', color='#0f172a', pad=15)
        self.ax.set_xlabel('Government Incentive (₹)', fontsize=11, fontweight='bold', color='#334155', labelpad=8)
        self.ax.set_ylabel('Sales Volume (Units)', fontsize=11, fontweight='bold', color='#334155', labelpad=8)
        self.ax.legend(title='Vehicle Type', title_fontsize='9', fontsize='9', facecolor='#ffffff', labelcolor='#334155')
        self.canvas.draw()

    def plot_tech_range(self):
        self.current_view = "other"
        self.prepare_ax()
        self.style_axes()
        range_df = df_raw.groupby('Powertrain_Type')['Vehicle_Range_Km'].mean().reset_index()
        ax = sns.barplot(data=range_df, x='Powertrain_Type', y='Vehicle_Range_Km', palette='Purples_r', ax=self.ax)
        
        for p in ax.patches:
            height = p.get_height()
            ax.annotate(f"{height:.1f} km", (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='bottom', fontsize=9, fontweight='bold', color='#0f172a', xytext=(0, 3), textcoords='offset points')

        self.ax.set_title('Average Vehicle Range (km) by Powertrain Technology', fontsize=12, fontweight='bold', color='#0f172a', pad=15)
        self.ax.set_xlabel('Powertrain Type', fontsize=11, fontweight='bold', color='#334155', labelpad=8)
        self.ax.set_ylabel('Average Range (km)', fontsize=11, fontweight='bold', color='#334155', labelpad=8)
        self.canvas.draw()

    def plot_running_cost(self):
        self.current_view = "other"
        self.prepare_ax()
        self.style_axes()
        cost_df = df_raw.groupby('Powertrain_Type')['Running_Cost_Per_Km_USD'].mean().reset_index()
        cost_df['Running_Cost_INR'] = cost_df['Running_Cost_Per_Km_USD'] * 95.85
        ax = sns.barplot(data=cost_df, x='Powertrain_Type', y='Running_Cost_INR', palette='mako', ax=self.ax)
        
        for p in ax.patches:
            height = p.get_height()
            ax.annotate(f"₹{height:.2f}", (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='bottom', fontsize=9, fontweight='bold', color='#0f172a', xytext=(0, 3), textcoords='offset points')

        self.ax.set_title('Average Running Cost per Kilometer (₹) by Powertrain', fontsize=12, fontweight='bold', color='#0f172a', pad=15)
        self.ax.set_xlabel('Powertrain Type', fontsize=11, fontweight='bold', color='#334155', labelpad=8)
        self.ax.set_ylabel('Running Cost per Km (₹)', fontsize=11, fontweight='bold', color='#334155', labelpad=8)
        self.canvas.draw()

    def plot_co2_savings(self):
        self.current_view = "other"
        self.prepare_ax()
        self.style_axes()
        co2_df = df_global.groupby('Year')['CO2_Saved_Tons'].sum().reset_index()
        sns.lineplot(data=co2_df, x='Year', y='CO2_Saved_Tons', marker='o', color='#16a34a', linewidth=3, ax=self.ax)
        
        for yr, val in zip(co2_df['Year'], co2_df['CO2_Saved_Tons']):
            self.ax.annotate(f"{val:,.0f}", (yr, val), textcoords="offset points", xytext=(0,8), ha='center', fontsize=8, fontweight='bold', color='#15803d')

        self.ax.set_title('Cumulative CO₂ Emissions Saved (Tons) Over Time', fontsize=12, fontweight='bold', color='#0f172a', pad=15)
        self.ax.set_xlabel('Timeline Year', fontsize=11, fontweight='bold', color='#334155', labelpad=8)
        self.ax.set_ylabel('CO₂ Saved (Tons)', fontsize=11, fontweight='bold', color='#334155', labelpad=8)
        self.canvas.draw()

    def plot_ml_predictions(self):
        self.current_view = "other"
        self.prepare_ax()
        self.style_axes()

        yearly_sales = df_global.groupby('Year')['Sales_Volume'].sum().reset_index()
        
        X = yearly_sales[['Year']]
        y = yearly_sales['Sales_Volume']
        model = LinearRegression()
        model.fit(X, y)

        future_years_df = pd.DataFrame({'Year': np.arange(2020, 2031)})
        predicted_sales = model.predict(future_years_df)

        self.ax.plot(future_years_df['Year'], predicted_sales, marker='o', color='#d946ef', linewidth=3, markersize=7, label='ML Forecast Trend (2020-2030)')
        
        for yr, val in zip(future_years_df['Year'], predicted_sales):
            self.ax.annotate(f"{val:,.0f}", (yr, val), textcoords="offset points", xytext=(0,8), ha='center', fontsize=8, fontweight='bold', color='#701a75')

        self.ax.set_title('AI / ML Market Sales Volume Forecasting & Projections (2020–2030)', fontsize=12, fontweight='bold', color='#0f172a', pad=15)
        self.ax.set_xlabel('Calendar Year', fontsize=11, fontweight='bold', color='#334155', labelpad=8)
        self.ax.set_ylabel('Projected Sales Volume (Units)', fontsize=11, fontweight='bold', color='#334155', labelpad=8)
        self.ax.legend(facecolor='#ffffff', labelcolor='#334155', fontsize='9')
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = ExecutiveDashboardApp(root)
    root.mainloop()