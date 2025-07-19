import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.ttk import Notebook, Frame, Treeview
from datetime import datetime, timedelta
import json
import os
from expense_tracker import ExpenseTracker, format_currency
from widgets import DateEntryWidget
from analytics import ExpenseAnalytics

class ExpenseTrackerGUI:
    """
    Modern GUI for the Expense Tracker application using Tkinter.
    Demonstrates Python GUI programming with ttk styling.
    """
    
    def __init__(self):
        """Initialize the GUI application."""
        self.root = tk.Tk()
        self.root.title("Expense Tracker - Python GUI Demo")
        self.root.geometry("1600x1000")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize the expense tracker backend
        self.tracker = ExpenseTracker()
        
        # Create category mappings for UI display
        self.category_display_to_key = {name: key for key, name in self.tracker.categories.items()}
        self.category_key_to_display = {key: name for key, name in self.tracker.categories.items()}
        
        # Configure modern styling
        self.setup_styles()
        
        # Initialize analytics
        self.analytics = ExpenseAnalytics(self)
        
        # Create the main interface
        self.create_widgets()
        
        # Refresh the display
        self.refresh_expense_table()
        self.update_summary()
    
    def setup_styles(self):
        """Configure modern styles for ttk widgets."""
        style = ttk.Style()
        
        # Configure modern color scheme
        style.theme_use('clam')
        
        # Custom styles for different components
        style.configure('Title.TLabel', font=('Helvetica', 24, 'bold'), foreground='#2c3e50')
        style.configure('Heading.TLabel', font=('Helvetica', 18, 'bold'), foreground='#34495e')
        style.configure('Success.TLabel', foreground='#27ae60', font=('Helvetica', 15, 'bold'))
        style.configure('Error.TLabel', foreground='#e74c3c', font=('Helvetica', 15, 'bold'))
        
        # Button styles
        style.configure('Action.TButton', font=('Helvetica', 15, 'bold'))
        style.configure('Reset.TButton', font=('Helvetica', 15, 'bold'), foreground='#e74c3c')
        style.configure('Primary.TButton', font=('Helvetica', 16, 'bold'))
        
        # Treeview styling
        style.configure('Treeview.Heading', font=('Helvetica', 15, 'bold'))
        style.configure('Treeview', font=('Helvetica', 14))
    
    def create_widgets(self):
        """Create all GUI widgets with modern layout."""
        # Create main notebook for tabs
        self.notebook = Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_main_tab()
        self.analytics.create_analytics_tab(self.notebook)
        self.create_settings_tab()
    
    def create_main_tab(self):
        """Create the main tab with expense management."""
        main_frame = Frame(self.notebook)
        self.notebook.add(main_frame, text="Expense Management")
        
        # Create main sections
        self.create_input_section(main_frame)
        self.create_filter_section(main_frame)
        self.create_table_section(main_frame)
        self.create_summary_section(main_frame)
    
    def create_input_section(self, parent):
        """Create the expense input section."""
        # Input frame with modern styling
        input_frame = ttk.LabelFrame(parent, text="Add New Expense", padding=15)
        input_frame.pack(fill='x', padx=10, pady=(10, 5))
        
        # Create input grid
        input_grid = Frame(input_frame)
        input_grid.pack(fill='x')
        
        # Amount input
        ttk.Label(input_grid, text="Amount ($):", font=('Helvetica', 15, 'bold')).grid(
            row=0, column=0, sticky='w', padx=(0, 10), pady=5)
        self.amount_var = tk.StringVar()
        amount_entry = ttk.Entry(input_grid, textvariable=self.amount_var, font=('Helvetica', 15))
        amount_entry.grid(row=0, column=1, sticky='ew', padx=(0, 20), pady=5)
        
        # Category dropdown
        ttk.Label(input_grid, text="Category:", font=('Helvetica', 15, 'bold')).grid(
            row=0, column=2, sticky='w', padx=(0, 10), pady=5)
        self.category_var = tk.StringVar()
        category_combo = ttk.Combobox(
            input_grid, textvariable=self.category_var, 
            values=list(self.tracker.categories.values()),
            state='readonly', font=('Helvetica', 15)
        )
        category_combo.grid(row=0, column=3, sticky='ew', padx=(0, 20), pady=5)
        category_combo.set('Food & Dining')  # Default selection
        
        # Date picker
        ttk.Label(input_grid, text="Date:", font=('Helvetica', 15, 'bold')).grid(
            row=1, column=0, sticky='w', padx=(0, 10), pady=5)
        self.date_picker = DateEntryWidget(
            input_grid, width=12, font=('Helvetica', 15)
        )
        self.date_picker.grid(row=1, column=1, sticky='ew', padx=(0, 20), pady=5)
        
        # User dropdown  
        ttk.Label(input_grid, text="User:", font=('Helvetica', 15, 'bold')).grid(
            row=1, column=2, sticky='w', padx=(0, 10), pady=5)
        self.user_var = tk.StringVar()
        user_combo = ttk.Combobox(
            input_grid, textvariable=self.user_var,
            values=self.tracker.users,
            state='readonly', font=('Helvetica', 15)
        )
        user_combo.grid(row=1, column=3, sticky='ew', padx=(0, 20), pady=5)
        user_combo.set(self.tracker.users[0])  # Default to first user
        
        # Description input
        ttk.Label(input_grid, text="Description:", font=('Helvetica', 15, 'bold')).grid(
            row=2, column=0, sticky='w', padx=(0, 10), pady=5)
        self.description_var = tk.StringVar()
        description_entry = ttk.Entry(input_grid, textvariable=self.description_var, font=('Helvetica', 15))
        description_entry.grid(row=2, column=1, columnspan=3, sticky='ew', pady=5)
        
        # Configure grid weights for responsive design
        for i in range(4):
            input_grid.columnconfigure(i, weight=1)
        
        # Action buttons
        button_frame = Frame(input_frame)
        button_frame.pack(fill='x', pady=(10, 0))
        
        add_button = ttk.Button(
            button_frame, text="Add Expense", 
            command=self.add_expense, style='Action.TButton'
        )
        add_button.pack(side='left', padx=(0, 10))
        
        clear_button = ttk.Button(
            button_frame, text="Clear Form", 
            command=self.clear_form, style='Action.TButton'
        )
        clear_button.pack(side='left')
        
        # Status label
        self.status_label = ttk.Label(button_frame, text="")
        self.status_label.pack(side='right')
    
    def create_filter_section(self, parent):
        """Create the filtering controls section."""
        filter_frame = ttk.LabelFrame(parent, text="Filter & Search", padding=10)
        filter_frame.pack(fill='x', padx=10, pady=5)
        
        # Filter controls
        controls_frame = Frame(filter_frame)
        controls_frame.pack(fill='x')
        
        # Date range filter
        ttk.Label(controls_frame, text="From:", font=('Helvetica', 14)).grid(
            row=0, column=0, sticky='w', padx=(0, 5))
        self.start_date_picker = DateEntryWidget(
            controls_frame, width=10, font=('Helvetica', 14)
        )
        self.start_date_picker.set_date(datetime.now() - timedelta(days=30))
        self.start_date_picker.grid(row=0, column=1, padx=(0, 10))
        
        ttk.Label(controls_frame, text="To:", font=('Helvetica', 14)).grid(
            row=0, column=2, sticky='w', padx=(0, 5))
        self.end_date_picker = DateEntryWidget(
            controls_frame, width=10, font=('Helvetica', 14)
        )
        self.end_date_picker.set_date(datetime.now())
        self.end_date_picker.grid(row=0, column=3, padx=(0, 15))
        
        # Category filter
        ttk.Label(controls_frame, text="Category:", font=('Helvetica', 14)).grid(
            row=0, column=4, sticky='w', padx=(0, 5))
        self.filter_category_var = tk.StringVar()
        filter_combo = ttk.Combobox(
            controls_frame, textvariable=self.filter_category_var,
            values=['All'] + list(self.tracker.categories.values()),
            state='readonly', width=12, font=('Helvetica', 14)
        )
        filter_combo.grid(row=0, column=5, padx=(0, 15))
        filter_combo.set('All')
        
        # User filter
        ttk.Label(controls_frame, text="User:", font=('Helvetica', 14)).grid(
            row=0, column=6, sticky='w', padx=(0, 5))
        self.filter_user_var = tk.StringVar()
        user_filter_combo = ttk.Combobox(
            controls_frame, textvariable=self.filter_user_var,
            values=['All'] + self.tracker.users,
            state='readonly', width=15, font=('Helvetica', 14)
        )
        user_filter_combo.grid(row=0, column=7, padx=(0, 15))
        user_filter_combo.set('All')
        
        # Search box
        ttk.Label(controls_frame, text="Search:", font=('Helvetica', 14)).grid(
            row=0, column=8, sticky='w', padx=(0, 5))
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(controls_frame, textvariable=self.search_var, width=15, font=('Helvetica', 14))
        search_entry.grid(row=0, column=9, padx=(0, 10))
        
        # Filter buttons
        filter_button = ttk.Button(
            controls_frame, text="Filter", 
            command=self.apply_filters, style='Action.TButton'
        )
        filter_button.grid(row=0, column=10, padx=5)
        
        reset_button = ttk.Button(
            controls_frame, text="Reset", 
            command=self.reset_filters, style='Reset.TButton'
        )
        reset_button.grid(row=0, column=11, padx=5)
    
    def create_table_section(self, parent):
        """Create the expenses table section."""
        table_frame = ttk.LabelFrame(parent, text="Expenses List", padding=10)
        table_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Create table with scrollbars
        table_container = Frame(table_frame)
        table_container.pack(fill='both', expand=True)
        
        # Treeview for expenses
        columns = ('ID', 'Date', 'Amount', 'Category', 'User', 'Description')
        self.expense_tree = Treeview(table_container, columns=columns, show='headings', height=15)
        
        # Define column headings and widths
        self.expense_tree.heading('ID', text='ID')
        self.expense_tree.heading('Date', text='Date')
        self.expense_tree.heading('Amount', text='Amount')
        self.expense_tree.heading('Category', text='Category')
        self.expense_tree.heading('User', text='User')
        self.expense_tree.heading('Description', text='Description')
        
        self.expense_tree.column('ID', width=80, anchor='center')
        self.expense_tree.column('Date', width=100, anchor='center')
        self.expense_tree.column('Amount', width=100, anchor='center')
        self.expense_tree.column('Category', width=120, anchor='center')
        self.expense_tree.column('User', width=150, anchor='center')
        self.expense_tree.column('Description', width=250, anchor='w')
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_container, orient='vertical', command=self.expense_tree.yview)
        h_scrollbar = ttk.Scrollbar(table_container, orient='horizontal', command=self.expense_tree.xview)
        self.expense_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack table and scrollbars
        self.expense_tree.pack(side='left', fill='both', expand=True)
        v_scrollbar.pack(side='right', fill='y')
        h_scrollbar.pack(side='bottom', fill='x')
        
        # Context menu for right-click actions
        self.create_context_menu()
        
        # Table action buttons
        action_frame = Frame(table_frame)
        action_frame.pack(fill='x', pady=(10, 0))
        
        edit_button = ttk.Button(
            action_frame, text="Edit Selected", 
            command=self.edit_selected_expense
        )
        edit_button.pack(side='left', padx=(0, 10))
        
        delete_button = ttk.Button(
            action_frame, text="Delete Selected", 
            command=self.delete_selected_expense
        )
        delete_button.pack(side='left')
        
        # Export button
        export_button = ttk.Button(
            action_frame, text="Export to JSON", 
            command=self.export_data
        )
        export_button.pack(side='right')
    
    def create_summary_section(self, parent):
        """Create the summary information section."""
        summary_frame = ttk.LabelFrame(parent, text="Quick Summary", padding=10)
        summary_frame.pack(fill='x', padx=10, pady=(5, 10))
        
        # Summary labels
        summary_grid = Frame(summary_frame)
        summary_grid.pack(fill='x')
        
        # Total expenses
        ttk.Label(summary_grid, text="Total Expenses:", font=('Helvetica', 15, 'bold')).grid(
            row=0, column=0, sticky='w', padx=(0, 20))
        self.total_label = ttk.Label(summary_grid, text="$0.00", font=('Helvetica', 18, 'bold'), foreground='#e74c3c')
        self.total_label.grid(row=0, column=1, sticky='w')
        
        # Expense count
        ttk.Label(summary_grid, text="Total Count:", font=('Helvetica', 15, 'bold')).grid(
            row=0, column=2, sticky='w', padx=(50, 20))
        self.count_label = ttk.Label(summary_grid, text="0", font=('Helvetica', 18, 'bold'), foreground='#3498db')
        self.count_label.grid(row=0, column=3, sticky='w')
        
        # Average expense
        ttk.Label(summary_grid, text="Average:", font=('Helvetica', 15, 'bold')).grid(
            row=0, column=4, sticky='w', padx=(50, 20))
        self.avg_label = ttk.Label(summary_grid, text="$0.00", font=('Helvetica', 18, 'bold'), foreground='#9b59b6')
        self.avg_label.grid(row=0, column=5, sticky='w')
    
    def create_settings_tab(self):
        """Create the settings and data management tab."""
        settings_frame = Frame(self.notebook)
        self.notebook.add(settings_frame, text="Settings")
        
        # Data management section
        data_frame = ttk.LabelFrame(settings_frame, text="Data Management", padding=15)
        data_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(data_frame, text="Load Data", 
                  command=self.load_data).pack(side='left', padx=(0, 10))
        ttk.Button(data_frame, text="Clear All Data", 
                  command=self.clear_all_data).pack(side='left')
        
        # Categories management
        categories_frame = ttk.LabelFrame(settings_frame, text="Category Management", padding=15)
        categories_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Categories list
        categories_list = Frame(categories_frame)
        categories_list.pack(fill='both', expand=True)
        
        ttk.Label(categories_list, text="Current Categories:", 
                 style='Heading.TLabel').pack(anchor='w', pady=(0, 10))
        
        # Display current categories with delete buttons
        self.categories_container = Frame(categories_list)
        self.categories_container.pack(fill='both', expand=True)
        self.refresh_categories_display()
        
        # Add new category section
        ttk.Label(categories_list, text="Add New Category:", 
                 font=('Helvetica', 15, 'bold')).pack(anchor='w', pady=(20, 10))
        
        add_category_frame = Frame(categories_list)
        add_category_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(add_category_frame, text="Display Name:", font=('Helvetica', 12)).grid(
            row=0, column=0, sticky='w', padx=(0, 10))
        self.new_category_name_var = tk.StringVar()
        ttk.Entry(add_category_frame, textvariable=self.new_category_name_var, 
                 font=('Helvetica', 12), width=20).grid(row=0, column=1, sticky='ew', padx=(0, 10))
        
        ttk.Button(add_category_frame, text="Add Category", 
                  command=self.add_new_category).grid(row=0, column=2)
        
        # Configure grid weights
        add_category_frame.columnconfigure(1, weight=1)
    
    def create_context_menu(self):
        """Create right-click context menu for the table."""
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Edit", command=self.edit_selected_expense)
        self.context_menu.add_command(label="Delete", command=self.delete_selected_expense)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Copy Details", command=self.copy_expense_details)
        
        # Bind right-click to table
        self.expense_tree.bind("<Button-3>", self.show_context_menu)
    
    def show_context_menu(self, event):
        """Show context menu on right-click."""
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()
    
    def add_expense(self):
        """Add a new expense to the tracker."""
        try:
            # Get values from form
            amount = float(self.amount_var.get().strip())
            category_display = self.category_var.get().strip()
            # Convert display name to internal key
            category = self.category_display_to_key.get(category_display, category_display.lower())
            description = self.description_var.get().strip()
            user = self.user_var.get().strip()
            
            # Get date
            date_str = self.date_picker.get()
            
            # Validate inputs
            if not description:
                raise ValueError("Description cannot be empty")
            if not user:
                raise ValueError("Please select a user")
            
            # Add expense using backend
            expense_id = self.tracker.add_expense(amount, category, description, user, date_str)
            
            # Show success message
            self.show_status(f"Expense added successfully! (ID: {expense_id})", "success")
            
            # Clear form and refresh display
            self.clear_form()
            self.refresh_expense_table()
            self.update_summary()
            
        except ValueError as e:
            self.show_status(f"Error: {str(e)}", "error")
        except Exception as e:
            self.show_status(f"Unexpected error: {str(e)}", "error")
    
    def clear_form(self):
        """Clear the expense input form."""
        self.amount_var.set("")
        self.description_var.set("")
        self.category_var.set("Food & Dining")
        self.user_var.set(self.tracker.users[0])  # Reset to first user
        self.date_picker.set_date(datetime.now().date())
    
    def show_status(self, message, status_type="info"):
        """Show status message with appropriate styling."""
        if status_type == "success":
            self.status_label.configure(text=message, style='Success.TLabel')
        elif status_type == "error":
            self.status_label.configure(text=message, style='Error.TLabel')
        else:
            self.status_label.configure(text=message)
        
        # Clear status after 5 seconds
        self.root.after(5000, lambda: self.status_label.configure(text=""))
    
    def refresh_expense_table(self, expenses=None):
        """Refresh the expenses table display."""
        # Clear existing items
        for item in self.expense_tree.get_children():
            self.expense_tree.delete(item)
        
        # Get expenses to display
        if expenses is None:
            expenses = self.tracker.view_all_expenses()
        
        # Populate table
        for expense in expenses:
            self.expense_tree.insert('', 'end', values=(
                expense['id'],
                expense['date'],
                format_currency(expense['amount']),
                expense['category'].title(),
                expense.get('user', 'N/A'),
                expense['description']
            ))
        
        # Update summary
        self.update_summary()
    
    def update_summary(self):
        """Update the summary information display."""
        expenses = self.tracker.view_all_expenses()
        total_amount = sum(expense['amount'] for expense in expenses)
        count = len(expenses)
        avg_amount = total_amount / count if count > 0 else 0
        
        self.total_label.configure(text=format_currency(total_amount))
        self.count_label.configure(text=str(count))
        self.avg_label.configure(text=format_currency(avg_amount))
    
    def apply_filters(self):
        """Apply filters to the expense display."""
        try:
            # Get filter values
            start_date = self.start_date_picker.get()
            end_date = self.end_date_picker.get()
            
            category = self.filter_category_var.get()
            user = self.filter_user_var.get()
            search_query = self.search_var.get().strip()
            
            # Start with all expenses
            expenses = self.tracker.view_all_expenses()
            
            # Apply date filter
            if start_date and end_date:
                expenses = [e for e in expenses 
                           if start_date <= e['date'] <= end_date]
            
            # Apply category filter
            if category and category != 'All':
                # Convert display name to internal key for comparison
                category_key = self.category_display_to_key.get(category, category.lower())
                expenses = [e for e in expenses 
                           if e['category'] == category_key]
            
            # Apply user filter
            if user and user != 'All':
                expenses = [e for e in expenses 
                           if e.get('user', 'N/A') == user]
            
            # Apply search filter
            if search_query:
                expenses = [e for e in expenses 
                           if search_query.lower() in e['description'].lower()]
            
            # Refresh table with filtered results
            self.refresh_expense_table(expenses)
            
            self.show_status(f"Found {len(expenses)} matching expenses")
            
        except Exception as e:
            self.show_status(f"Filter error: {str(e)}", "error")
    
    def reset_filters(self):
        """Reset all filters and show all expenses."""
        self.filter_category_var.set('All')
        self.filter_user_var.set('All')
        self.search_var.set('')
        self.start_date_picker.set_date((datetime.now() - timedelta(days=30)).date())
        self.end_date_picker.set_date(datetime.now().date())
        
        self.refresh_expense_table()
        self.show_status("Filters reset")
    
    def edit_selected_expense(self):
        """Edit the selected expense."""
        selection = self.expense_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an expense to edit")
            return
        
        # Get selected expense data
        item = self.expense_tree.item(selection[0])
        expense_id = item['values'][0]
        
        # Find expense in backend
        expense = self.tracker.expenses.get(expense_id)
        if not expense:
            messagebox.showerror("Error", "Expense not found")
            return
        
        # Create edit dialog
        self.create_edit_dialog(expense)
    
    def create_edit_dialog(self, expense):
        """Create dialog for editing an expense."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Expense")
        dialog.geometry("800x600")
        dialog.resizable(False, False)
        dialog.configure(bg='#f0f0f0')
        
        # Center the dialog
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Create form
        main_frame = ttk.Frame(dialog, padding=20)
        main_frame.pack(fill='both', expand=True)
        
        # Amount
        ttk.Label(main_frame, text="Amount ($):", font=('Helvetica', 15, 'bold')).pack(anchor='w', pady=(0, 5))
        amount_var = tk.StringVar(value=str(expense['amount']))
        amount_entry = ttk.Entry(main_frame, textvariable=amount_var, font=('Helvetica', 15))
        amount_entry.pack(fill='x', pady=(0, 15))
        
        # Category
        ttk.Label(main_frame, text="Category:", font=('Helvetica', 15, 'bold')).pack(anchor='w', pady=(0, 5))
        category_var = tk.StringVar(value=self.category_key_to_display.get(expense['category'], expense['category'].title()))
        category_combo = ttk.Combobox(
            main_frame, textvariable=category_var,
            values=list(self.tracker.categories.values()),
            state='readonly', font=('Helvetica', 15)
        )
        category_combo.pack(fill='x', pady=(0, 15))
        
        # User
        ttk.Label(main_frame, text="User:", font=('Helvetica', 15, 'bold')).pack(anchor='w', pady=(0, 5))
        user_var = tk.StringVar(value=expense.get('user', self.tracker.users[0]))
        user_combo = ttk.Combobox(
            main_frame, textvariable=user_var,
            values=self.tracker.users,
            state='readonly', font=('Helvetica', 15)
        )
        user_combo.pack(fill='x', pady=(0, 15))
        
        # Description
        ttk.Label(main_frame, text="Description:", font=('Helvetica', 15, 'bold')).pack(anchor='w', pady=(0, 5))
        description_var = tk.StringVar(value=expense['description'])
        description_entry = ttk.Entry(main_frame, textvariable=description_var, font=('Helvetica', 15))
        description_entry.pack(fill='x', pady=(0, 15))
        
        # Date
        ttk.Label(main_frame, text="Date:", font=('Helvetica', 15, 'bold')).pack(anchor='w', pady=(0, 5))
        date_var = tk.StringVar(value=expense['date'])
        date_entry = ttk.Entry(main_frame, textvariable=date_var, font=('Helvetica', 15))
        date_entry.pack(fill='x', pady=(0, 20))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x', pady=(20, 10))
        
        def save_changes():
            try:
                # Update expense data
                # Convert category display name back to key
                category_display = category_var.get()
                category_key = self.category_display_to_key.get(category_display, category_display.lower())
                
                new_expense = {
                    **expense,
                    'amount': float(amount_var.get()),
                    'category': category_key,
                    'user': user_var.get(),
                    'description': description_var.get().strip(),
                    'date': date_var.get().strip()
                }
                
                # Validate
                if not new_expense['description']:
                    raise ValueError("Description cannot be empty")
                
                # Update in tracker
                self.tracker.expenses[expense['id']] = new_expense
                self.tracker.save_data()
                
                # Refresh display
                self.refresh_expense_table()
                self.show_status(f"Expense {expense['id']} updated successfully", "success")
                dialog.destroy()
                
            except ValueError as e:
                messagebox.showerror("Error", str(e))
        
        save_btn = ttk.Button(button_frame, text="Save Changes", command=save_changes, 
                  style='Primary.TButton')
        save_btn.pack(side='left', padx=(0, 10))
        
        cancel_btn = ttk.Button(button_frame, text="Cancel", command=dialog.destroy)
        cancel_btn.pack(side='left')
    
    def delete_selected_expense(self):
        """Delete the selected expense."""
        selection = self.expense_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an expense to delete")
            return
        
        # Get selected expense ID
        item = self.expense_tree.item(selection[0])
        expense_id = item['values'][0]
        
        # Confirm deletion
        result = messagebox.askyesno(
            "Confirm Deletion", 
            f"Are you sure you want to delete expense {expense_id}?\n\nThis action cannot be undone."
        )
        
        if result:
            if self.tracker.delete_expense(expense_id):
                self.show_status(f"Expense {expense_id} deleted successfully", "success")
                self.refresh_expense_table()
            else:
                self.show_status(f"Failed to delete expense {expense_id}", "error")
    
    def copy_expense_details(self):
        """Copy selected expense details to clipboard."""
        selection = self.expense_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an expense to copy")
            return
        
        # Get expense details
        item = self.expense_tree.item(selection[0])
        details = " | ".join(str(val) for val in item['values'])
        
        # Copy to clipboard
        self.root.clipboard_clear()
        self.root.clipboard_append(details)
        self.show_status("Expense details copied to clipboard")
    
    def load_data(self):
        """Load data from file and merge with existing expenses."""
        from tkinter import filedialog
        
        # Let user select a file to load
        filename = filedialog.askopenfilename(
            title="Select Expense Data File",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            defaultextension=".json"
        )
        
        if not filename:
            # User cancelled the dialog
            return
        
        try:
            # Load data from selected file and merge with existing
            new_expenses_count = self.tracker.load_and_merge_data(filename)
            self.refresh_expense_table()
            
            if new_expenses_count > 0:
                self.show_status(f"Loaded and merged {new_expenses_count} expenses successfully", "success")
                messagebox.showinfo("Success", 
                    f"Successfully loaded and merged {new_expenses_count} expenses from {filename}\n\n"
                    f"Total expenses: {len(self.tracker.expenses)}")
            else:
                self.show_status("No new expenses found to merge", "success")
                messagebox.showinfo("Info", "No new expenses found in the selected file.")
                
        except Exception as e:
            error_msg = f"Failed to load data: {str(e)}"
            self.show_status(error_msg, "error")
            messagebox.showerror("Load Error", error_msg)
    
    def clear_all_data(self):
        """Clear all expense data."""
        result = messagebox.askyesno(
            "Confirm Clear All", 
            "Are you sure you want to delete ALL expenses?\n\nThis action cannot be undone!"
        )
        
        if result:
            self.tracker.expenses = {}
            self.tracker.save_data()
            self.refresh_expense_table()
            self.show_status("All data cleared", "success")
    
    def refresh_categories_display(self):
        """Refresh the categories display with current categories and delete buttons."""
        # Clear existing widgets
        for widget in self.categories_container.winfo_children():
            widget.destroy()
        
        # Display current categories with delete buttons
        for key, name in self.tracker.categories.items():
            category_row = Frame(self.categories_container)
            category_row.pack(fill='x', pady=2)
            
            ttk.Label(category_row, text=f"• {name}", 
                     font=('Helvetica', 15)).pack(side='left')
            
            # Only allow deletion of non-essential categories
            if key not in ['food', 'transport', 'utilities', 'other']:
                delete_btn = ttk.Button(category_row, text="Delete", width=8,
                                      command=lambda k=key: self.delete_category(k))
                delete_btn.pack(side='right', padx=(10, 0))
    
    def add_new_category(self):
        """Add a new category to the tracker."""
        category_name = self.new_category_name_var.get().strip()
        
        if not category_name:
            messagebox.showerror("Error", "Please enter a category name")
            return
        
        # Generate key from display name
        category_key = category_name.lower().replace(' ', '').replace('&', '').replace('-', '')
        
        # Check if category already exists
        if category_key in self.tracker.categories:
            messagebox.showerror("Error", "A category with this name already exists")
            return
        
        # Check if display name already exists
        if category_name in self.tracker.categories.values():
            messagebox.showerror("Error", "A category with this display name already exists")
            return
        
        try:
            # Add to tracker
            self.tracker.categories[category_key] = category_name
            
            # Update category mappings
            self.update_category_mappings()
            
            # Update all dropdowns
            self.update_category_dropdowns()
            
            # Save changes
            self.tracker.save_data()
            
            # Refresh display
            self.refresh_categories_display()
            
            # Clear input
            self.new_category_name_var.set("")
            
            self.show_status(f"Category '{category_name}' added successfully", "success")
            messagebox.showinfo("Success", f"Category '{category_name}' has been added")
            
        except Exception as e:
            self.show_status(f"Failed to add category: {str(e)}", "error")
            messagebox.showerror("Error", f"Failed to add category: {str(e)}")
    
    def delete_category(self, category_key):
        """Delete a category from the tracker."""
        category_name = self.tracker.categories.get(category_key, category_key)
        
        # Check if category is being used by any expenses
        expenses_using_category = [e for e in self.tracker.expenses.values() 
                                  if e.get('category') == category_key]
        
        if expenses_using_category:
            messagebox.showerror("Cannot Delete", 
                f"Cannot delete category '{category_name}' because it is being used by {len(expenses_using_category)} expense(s).\n\n"
                "Please reassign or delete those expenses first.")
            return
        
        # Confirm deletion
        result = messagebox.askyesno("Confirm Deletion", 
            f"Are you sure you want to delete the category '{category_name}'?\n\n"
            "This action cannot be undone.")
        
        if result:
            try:
                # Remove from tracker
                del self.tracker.categories[category_key]
                
                # Update category mappings
                self.update_category_mappings()
                
                # Update all dropdowns
                self.update_category_dropdowns()
                
                # Save changes
                self.tracker.save_data()
                
                # Refresh display
                self.refresh_categories_display()
                
                self.show_status(f"Category '{category_name}' deleted successfully", "success")
                messagebox.showinfo("Success", f"Category '{category_name}' has been deleted")
                
            except Exception as e:
                self.show_status(f"Failed to delete category: {str(e)}", "error")
                messagebox.showerror("Error", f"Failed to delete category: {str(e)}")
    
    def update_category_mappings(self):
        """Update the category mapping dictionaries."""
        self.category_display_to_key = {name: key for key, name in self.tracker.categories.items()}
        self.category_key_to_display = {key: name for key, name in self.tracker.categories.items()}
    
    def update_category_dropdowns(self):
        """Update all category dropdown values after categories change."""
        try:
            category_values = list(self.tracker.categories.values())
            
            # Update add expense category dropdown
            if hasattr(self, 'category_var'):
                current_value = self.category_var.get()
                # Find the combobox widget and update its values
                for widget in self.root.winfo_children():
                    self._update_combobox_values_recursive(widget, "category", category_values)
                
                # Reset selection if current value no longer exists
                if current_value not in category_values and category_values:
                    self.category_var.set(category_values[0])
            
            # Update filter category dropdown
            if hasattr(self, 'filter_category_var'):
                current_filter = self.filter_category_var.get()
                filter_values = ['All'] + category_values
                for widget in self.root.winfo_children():
                    self._update_combobox_values_recursive(widget, "filter_category", filter_values)
                
                if current_filter not in filter_values:
                    self.filter_category_var.set('All')
                    
        except Exception as e:
            print(f"Error updating dropdowns: {e}")
    
    def _update_combobox_values_recursive(self, widget, combo_type, values):
        """Recursively find and update combobox values."""
        try:
            if isinstance(widget, ttk.Combobox):
                current_values = list(widget['values'])
                if combo_type == "category" and len(current_values) > 0 and current_values[0] != 'All':
                    widget['values'] = values
                elif combo_type == "filter_category" and len(current_values) > 0 and 'All' in current_values:
                    widget['values'] = values
            
            for child in widget.winfo_children():
                self._update_combobox_values_recursive(child, combo_type, values)
        except:
            pass  # Ignore any widget access errors
    
    def export_data(self):
        """Export expenses to JSON file."""
        from tkinter import filedialog
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Export Expenses"
        )
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    json.dump({
                        'expenses': self.tracker.expenses,
                        'export_date': datetime.now().isoformat(),
                        'total_expenses': len(self.tracker.expenses),
                        'total_amount': self.tracker.get_total_expenses()
                    }, f, indent=2)
                
                self.show_status(f"Data exported to {filename}", "success")
            except Exception as e:
                self.show_status(f"Export failed: {str(e)}", "error")
    
    def run(self):
        """Start the GUI application."""
        self.root.mainloop()

def main():
    """Main function to run the GUI application."""
    print("Starting Expense Tracker GUI...")
    
    try:
        # Start the application
        app = ExpenseTrackerGUI()
        app.run()
        
    except Exception as e:
        print(f"Error starting application: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main() 