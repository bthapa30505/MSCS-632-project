import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from expense_tracker import format_currency

# Optional imports for charts - will be handled in try/except blocks
plt = None
FigureCanvasTkAgg = None

class ExpenseAnalytics:
    """Handles analytics and chart functionality for the expense tracker."""
    
    def __init__(self, gui_instance):
        """Initialize with reference to main GUI instance."""
        self.gui = gui_instance
        self.tracker = gui_instance.tracker
        self.root = gui_instance.root
    
    def create_analytics_tab(self, notebook):
        """Create the analytics tab with charts and detailed summaries."""
        analytics_frame = ttk.Frame(notebook)
        notebook.add(analytics_frame, text="Analytics")
        
        # Create chart section
        chart_frame = ttk.LabelFrame(analytics_frame, text="Expense Charts", padding=10)
        chart_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Chart controls
        control_frame = ttk.Frame(chart_frame)
        control_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Button(control_frame, text="Category Pie Chart", 
                  command=self.show_category_chart).pack(side='left', padx=(0, 10))
        ttk.Button(control_frame, text="Monthly Trend", 
                  command=self.show_trend_chart).pack(side='left', padx=(0, 10))
        ttk.Button(control_frame, text="Category Summary", 
                  command=self.show_category_summary).pack(side='left')
        
        # Chart canvas placeholder
        self.chart_frame = ttk.Frame(chart_frame)
        self.chart_frame.pack(fill='both', expand=True)
        
        # Initial welcome message
        welcome_label = ttk.Label(
            self.chart_frame, 
            text="Click a button above to view analytics charts",
            font=('Helvetica', 21), 
            foreground='#7f8c8d'
        )
        welcome_label.pack(expand=True)
    
    def show_category_chart(self):
        """Show pie chart of expenses by category."""
        try:
            # Clear chart frame
            for widget in self.chart_frame.winfo_children():
                widget.destroy()
            
            # Get category summary
            summary = self.tracker.get_expenses_by_category()
            categories = []
            amounts = []
            colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', 
                     '#DDA0DD', '#98D8C8', '#F7DC6F']
            
            for i, (key, data) in enumerate(summary.items()):
                if data['total'] > 0:
                    categories.append(data['name'])
                    amounts.append(data['total'])
            
            if not amounts:
                ttk.Label(self.chart_frame, text="No data to display", 
                         font=('Helvetica', 21)).pack(expand=True)
                return
            
            # Try to create matplotlib figure
            try:
                import matplotlib.pyplot as plt
                from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
                
                fig, ax = plt.subplots(figsize=(10, 6))
                wedges, texts, autotexts = ax.pie(amounts, labels=categories, autopct='%1.1f%%', 
                                                colors=colors[:len(categories)])
                ax.set_title('Expenses by Category', fontsize=24, fontweight='bold')
                
                # Embed in tkinter
                canvas = FigureCanvasTkAgg(fig, self.chart_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(fill='both', expand=True)
                
            except ImportError:
                # Fallback to text-based display if matplotlib not available
                self._show_text_category_summary(summary)
            
        except Exception as e:
            messagebox.showerror("Chart Error", f"Could not generate chart: {str(e)}")
    
    def show_trend_chart(self):
        """Show monthly trend chart."""
        try:
            # Clear chart frame
            for widget in self.chart_frame.winfo_children():
                widget.destroy()
            
            expenses = self.tracker.view_all_expenses()
            if not expenses:
                ttk.Label(self.chart_frame, text="No data to display", 
                         font=('Helvetica', 21)).pack(expand=True)
                return
            
            # Group by month
            monthly_data = {}
            for expense in expenses:
                month_key = expense['date'][:7]  # YYYY-MM
                monthly_data[month_key] = monthly_data.get(month_key, 0) + expense['amount']
            
            # Sort by date
            sorted_months = sorted(monthly_data.items())
            months = [item[0] for item in sorted_months]
            amounts = [item[1] for item in sorted_months]
            
            try:
                import matplotlib.pyplot as plt
                from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
                
                # Create matplotlib figure
                fig, ax = plt.subplots(figsize=(12, 6))
                ax.plot(months, amounts, marker='o', linewidth=2, markersize=8)
                ax.set_title('Monthly Expense Trend', fontsize=24, fontweight='bold')
                ax.set_xlabel('Month')
                ax.set_ylabel('Amount ($)')
                ax.grid(True, alpha=0.3)
                plt.xticks(rotation=45)
                plt.tight_layout()
                
                # Embed in tkinter
                canvas = FigureCanvasTkAgg(fig, self.chart_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(fill='both', expand=True)
                
            except ImportError:
                # Fallback to text-based display if matplotlib not available
                self._show_text_trend_summary(monthly_data)
            
        except Exception as e:
            messagebox.showerror("Chart Error", f"Could not generate chart: {str(e)}")
    
    def show_category_summary(self):
        """Show detailed category summary in a new window."""
        summary = self.tracker.get_expenses_by_category()
        total_all = self.tracker.get_total_expenses()
        
        # Create summary window
        summary_window = tk.Toplevel(self.root)
        summary_window.title("Category Summary")
        summary_window.geometry("800x600")
        summary_window.configure(bg='#f0f0f0')
        
        # Create table
        frame = ttk.Frame(summary_window, padding=20)
        frame.pack(fill='both', expand=True)
        
        ttk.Label(frame, text="Expense Summary by Category", 
                 style='Title.TLabel').pack(pady=(0, 20))
        
        # Summary table
        columns = ('Category', 'Total Amount', 'Count', 'Percentage', 'Average')
        tree = ttk.Treeview(frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor='center')
        
        # Populate data
        for category_key, data in summary.items():
            if data['count'] > 0:
                percentage = (data['total'] / total_all * 100) if total_all > 0 else 0
                average = data['total'] / data['count']
                tree.insert('', 'end', values=(
                    data['name'],
                    format_currency(data['total']),
                    data['count'],
                    f"{percentage:.1f}%",
                    format_currency(average)
                ))
        
        tree.pack(fill='both', expand=True, pady=(0, 20))
        
        # Total row
        total_frame = ttk.Frame(frame)
        total_frame.pack(fill='x')
        ttk.Label(total_frame, text=f"Total: {format_currency(total_all)}", 
                 font=('Helvetica', 18, 'bold')).pack(side='left')
        ttk.Label(total_frame, text=f"Count: {sum(data['count'] for data in summary.values())}", 
                 font=('Helvetica', 18, 'bold')).pack(side='right')
    
    def _show_text_category_summary(self, summary):
        """Show category summary in text format when matplotlib is not available."""
        # Create scrollable text widget
        text_frame = ttk.Frame(self.chart_frame)
        text_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title_label = ttk.Label(text_frame, text="Category Summary (Text View)", 
                               font=('Helvetica', 18, 'bold'))
        title_label.pack(pady=(0, 10))
        
        # Create text widget with scrollbar
        text_widget = tk.Text(text_frame, wrap=tk.WORD, font=('Courier', 12))
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        # Display category data
        text_content = "Category Breakdown:\n" + "="*50 + "\n\n"
        
        for key, data in summary.items():
            if data['total'] > 0:
                text_content += f"{data['name']:<20} {format_currency(data['total']):>12} ({data['count']} items)\n"
        
        text_content += "\n" + "="*50 + "\n"
        text_content += f"{'Total':<20} {format_currency(self.tracker.get_total_expenses()):>12}\n"
        
        text_widget.insert(tk.END, text_content)
        text_widget.configure(state='disabled')  # Make read-only
        
        # Pack widgets
        text_widget.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def _show_text_trend_summary(self, monthly_data):
        """Show trend summary in text format when matplotlib is not available."""
        # Create scrollable text widget
        text_frame = ttk.Frame(self.chart_frame)
        text_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title_label = ttk.Label(text_frame, text="Monthly Trend (Text View)", 
                               font=('Helvetica', 18, 'bold'))
        title_label.pack(pady=(0, 10))
        
        # Create text widget with scrollbar
        text_widget = tk.Text(text_frame, wrap=tk.WORD, font=('Courier', 12))
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        # Display monthly data
        text_content = "Monthly Expense Trend:\n" + "="*50 + "\n\n"
        
        sorted_months = sorted(monthly_data.items())
        for month, amount in sorted_months:
            # Create simple bar chart using text characters
            bar_length = int((amount / max(monthly_data.values())) * 30) if monthly_data.values() else 0
            bar = "█" * bar_length
            text_content += f"{month}  {format_currency(amount):>10} {bar}\n"
        
        text_widget.insert(tk.END, text_content)
        text_widget.configure(state='disabled')  # Make read-only
        
        # Pack widgets
        text_widget.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y') 