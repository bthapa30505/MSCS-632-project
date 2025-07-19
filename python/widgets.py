import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta

class DateEntryWidget:
    """Custom date entry widget using standard tkinter components."""
    
    def __init__(self, parent, **kwargs):
        self.parent = parent
        self.date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        
        # Create frame to hold date components
        self.frame = ttk.Frame(parent)
        
        # Extract width from kwargs to avoid conflict, default to 12
        width = kwargs.pop('width', 12)
        
        # Create entry with validation
        self.entry = ttk.Entry(self.frame, textvariable=self.date_var, width=width, **kwargs)
        self.entry.pack(side='left', fill='x', expand=True)
        
        # Add calendar button
        self.calendar_btn = ttk.Button(self.frame, text="...", width=3, command=self.show_calendar)
        self.calendar_btn.pack(side='right', padx=(2, 0))
        
        # Bind validation
        self.entry.bind('<FocusOut>', self.validate_date)
        self.entry.bind('<KeyRelease>', self.on_key_release)
    
    def get_date(self):
        """Get the date value as a datetime object."""
        try:
            return datetime.strptime(self.date_var.get(), "%Y-%m-%d")
        except:
            return datetime.now()
    
    def get(self):
        """Get the date as a string."""
        return self.date_var.get()
    
    def set_date(self, date):
        """Set the date value."""
        if isinstance(date, datetime):
            self.date_var.set(date.strftime("%Y-%m-%d"))
        elif isinstance(date, str):
            self.date_var.set(date)
        else:
            self.date_var.set(str(date))
    
    def grid(self, **kwargs):
        """Grid the widget frame."""
        self.frame.grid(**kwargs)
    
    def pack(self, **kwargs):
        """Pack the widget frame."""
        self.frame.pack(**kwargs)
    
    def validate_date(self, event=None):
        """Validate the entered date."""
        try:
            date_str = self.date_var.get()
            if date_str:
                datetime.strptime(date_str, "%Y-%m-%d")
                self.entry.configure(style="")  # Remove error styling
        except ValueError:
            # Try to auto-correct common formats
            self.auto_correct_date()
    
    def auto_correct_date(self):
        """Try to auto-correct common date formats."""
        date_str = self.date_var.get().replace("/", "-").replace(".", "-")
        
        # Try different formats
        formats = ["%Y-%m-%d", "%m-%d-%Y", "%d-%m-%Y", "%Y%m%d"]
        for fmt in formats:
            try:
                date_obj = datetime.strptime(date_str, fmt)
                self.date_var.set(date_obj.strftime("%Y-%m-%d"))
                self.entry.configure(style="")
                return
            except ValueError:
                continue
        
        # If all fails, set to today
        self.date_var.set(datetime.now().strftime("%Y-%m-%d"))
    
    def on_key_release(self, event=None):
        """Handle key release for real-time formatting."""
        current = self.date_var.get()
        # Auto-add dashes
        if len(current) == 4 and current.isdigit():
            self.date_var.set(current + "-")
        elif len(current) == 7 and current[4] == "-" and current[5:].isdigit():
            self.date_var.set(current + "-")
    
    def show_calendar(self):
        """Show a simple calendar popup."""
        self.create_calendar_popup()
    
    def create_calendar_popup(self):
        """Create a simple calendar popup using standard tkinter."""
        popup = tk.Toplevel(self.parent)
        popup.title("Select Date")
        popup.geometry("300x250")
        popup.resizable(False, False)
        popup.configure(bg='white')
        
        # Center the popup
        popup.transient(self.parent.winfo_toplevel())
        popup.grab_set()
        
        # Get current date
        try:
            current_date = datetime.strptime(self.date_var.get(), "%Y-%m-%d")
        except:
            current_date = datetime.now()
        
        # Create calendar frame
        cal_frame = tk.Frame(popup, bg='white')
        cal_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Month/Year navigation
        nav_frame = tk.Frame(cal_frame, bg='white')
        nav_frame.pack(fill='x', pady=(0, 10))
        
        self.cal_month = current_date.month
        self.cal_year = current_date.year
        
        ttk.Button(nav_frame, text="<", width=3, 
                  command=lambda: self.prev_month(popup, cal_frame, nav_frame)).pack(side='left')
        
        self.month_label = ttk.Label(nav_frame, 
                                   text=f"{current_date.strftime('%B %Y')}", 
                                   font=('Helvetica', 18, 'bold'))
        self.month_label.pack(side='left', expand=True)
        
        ttk.Button(nav_frame, text=">", width=3,
                  command=lambda: self.next_month(popup, cal_frame, nav_frame)).pack(side='right')
        
        # Create calendar grid
        self.create_calendar_grid(popup, cal_frame)
    
    def create_calendar_grid(self, popup, cal_frame):
        """Create the calendar day grid."""
        # Clear existing calendar if any
        for widget in cal_frame.winfo_children():
            if isinstance(widget, tk.Frame) and widget != cal_frame.winfo_children()[0]:
                widget.destroy()
        
        # Days grid
        days_frame = tk.Frame(cal_frame, bg='white')
        days_frame.pack(fill='both', expand=True)
        
        # Day headers
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        for i, day in enumerate(days):
            ttk.Label(days_frame, text=day, font=('Helvetica', 14, 'bold')).grid(
                row=0, column=i, padx=2, pady=2, sticky='nsew')
        
        # Get first day of month and days in month
        first_day = datetime(self.cal_year, self.cal_month, 1)
        if self.cal_month == 12:
            last_day = datetime(self.cal_year + 1, 1, 1) - timedelta(days=1)
        else:
            last_day = datetime(self.cal_year, self.cal_month + 1, 1) - timedelta(days=1)
        
        # Calculate starting position (Monday = 0)
        start_pos = first_day.weekday()
        
        # Fill calendar
        row = 1
        col = start_pos
        
        for day in range(1, last_day.day + 1):
            btn = ttk.Button(days_frame, text=str(day), width=4,
                           command=lambda d=day: self.select_date(popup, d))
            btn.grid(row=row, column=col, padx=1, pady=1, sticky='nsew')
            
            col += 1
            if col > 6:  # Sunday
                col = 0
                row += 1
        
        # Configure grid weights
        for i in range(7):
            days_frame.columnconfigure(i, weight=1)
    
    def prev_month(self, popup, cal_frame, nav_frame):
        """Navigate to previous month."""
        if self.cal_month == 1:
            self.cal_month = 12
            self.cal_year -= 1
        else:
            self.cal_month -= 1
        
        self.month_label.configure(text=datetime(self.cal_year, self.cal_month, 1).strftime('%B %Y'))
        self.create_calendar_grid(popup, cal_frame)
    
    def next_month(self, popup, cal_frame, nav_frame):
        """Navigate to next month."""
        if self.cal_month == 12:
            self.cal_month = 1
            self.cal_year += 1
        else:
            self.cal_month += 1
        
        self.month_label.configure(text=datetime(self.cal_year, self.cal_month, 1).strftime('%B %Y'))
        self.create_calendar_grid(popup, cal_frame)
    
    def select_date(self, popup, day):
        """Select a date from the calendar."""
        selected_date = datetime(self.cal_year, self.cal_month, day)
        self.date_var.set(selected_date.strftime("%Y-%m-%d"))
        popup.destroy() 