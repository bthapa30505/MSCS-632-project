import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Union
import uuid

class ExpenseTracker:
    """
    A comprehensive expense tracking application that demonstrates Python features:
    - Dictionary-based data storage
    - Dynamic typing capabilities
    - Datetime manipulation
    - JSON persistence
    """
    
    def __init__(self, data_file: str = "expenses.json"):
        """
        Initialize the expense tracker with optional data persistence.
        
        Args:
            data_file: Path to JSON file for data persistence
        """
        self.data_file = data_file
        # Primary data storage using dictionary - demonstrates Python's dict capabilities
        self.expenses: Dict[str, Dict] = {}
        # Categories for expense classification - demonstrates dynamic typing
        self.categories = {
            "food": "Food & Dining",
            "transport": "Transportation", 
            "utilities": "Utilities",
            "entertainment": "Entertainment",
            "healthcare": "Healthcare",
            "shopping": "Shopping",
            "education": "Education",
            "other": "Other"
        }
        # User options for expense tracking
        self.users = [
            "Bishal Thapa",
            "Aryan Shrestha", 
            "Mahesh Gaire",
            "Sajjad-IT-35",
            "SandeRestha",
            "Tushar Limbachiya"
        ]
        self.load_data()
    
    def add_expense(self, amountIn: Union[int, float], category: str,
                    description: str, user: str, date: Optional[str] = None) -> str:
        """
        Add a new expense to the tracker.
        Demonstrates Python's dynamic typing with Union types and optional parameters.
        
        Args:
            amountIn: Expense amount (int or float)
            category: Expense category
            description: Expense description
            user: User who made the expense
            date: Optional date string (YYYY-MM-DD), defaults to today
            
        Returns:
            str: Unique expense ID
        """
        # Generate unique ID
        expense_id = str(uuid.uuid4())[:8]
        
        # Handle date - demonstrate datetime manipulation
        if date is None:
            expense_date = datetime.now()
        else:
            try:
                expense_date = datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                raise ValueError("Date must be in YYYY-MM-DD format")
        
        # Validate category
        if category not in self.categories:
            available_categories = ", ".join(self.categories.keys())
            raise ValueError(f"Category must be one of: {available_categories}")
        
        # Validate user
        if user not in self.users:
            available_users = ", ".join(self.users)
            raise ValueError(f"User must be one of: {available_users}")
        
        # Validate amount - demonstrate dynamic typing
        if isinstance(amountIn, (int, float)) and amountIn > 0:
            expense_amount = float(amountIn)
        else:
            raise ValueError("Amount must be a positive number")
        
        # Create expense dictionary - demonstrates dict usage
        expense = {
            "id": expense_id,
            "amount": expense_amount,
            "category": category,
            "description": description.strip(),
            "user": user,
            "date": expense_date.strftime("%Y-%m-%d"),
            "timestamp": expense_date.isoformat(),
            "created_at": datetime.now().isoformat()
        }
        
        # Store in main dictionary
        self.expenses[expense_id] = expense
        self.save_data()
        
        return expense_id
    
    def view_all_expenses(self) -> List[Dict]:
        """
        Return all expenses sorted by date (newest first).
        
        Returns:
            List of expense dictionaries
        """
        expenses_list = list(self.expenses.values())
        # Sort by date using datetime parsing - demonstrates datetime usage
        expenses_list.sort(
            key=lambda x: datetime.fromisoformat(x["timestamp"]), 
            reverse=True
        )
        return expenses_list
    
    def filter_expenses_by_date(self, start_date: str, end_date: str) -> List[Dict]:
        """
        Filter expenses by date range.
        Demonstrates datetime manipulation and list comprehensions.
        
        Args:
            start_date: Start date string (YYYY-MM-DD)
            end_date: End date string (YYYY-MM-DD)
            
        Returns:
            List of filtered expense dictionaries
        """
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Dates must be in YYYY-MM-DD format")
        
        if start > end:
            raise ValueError("Start date cannot be after end date")
        
        # Filter using list comprehension - demonstrates Python's concise syntax
        filtered = [
            expense for expense in self.expenses.values()
            if start <= datetime.fromisoformat(expense["timestamp"]) <= end
        ]
        
        # Sort by date
        filtered.sort(
            key=lambda x: datetime.fromisoformat(x["timestamp"]), 
            reverse=True
        )
        
        return filtered
    
    def filter_expenses_by_category(self, category: str) -> List[Dict]:
        """
        Filter expenses by category.
        
        Args:
            category: Category to filter by
            
        Returns:
            List of filtered expense dictionaries
        """
        if category not in self.categories:
            available_categories = ", ".join(self.categories.keys())
            raise ValueError(f"Category must be one of: {available_categories}")
        
        # Filter using list comprehension
        filtered = [
            expense for expense in self.expenses.values()
            if expense["category"] == category
        ]
        
        # Sort by date
        filtered.sort(
            key=lambda x: datetime.fromisoformat(x["timestamp"]), 
            reverse=True
        )
        
        return filtered
    
    def search_expenses(self, query: str) -> List[Dict]:
        """
        Search expenses by description text.
        Demonstrates string manipulation and filtering.
        
        Args:
            query: Search query string
            
        Returns:
            List of matching expense dictionaries
        """
        query_lower = query.lower().strip()
        
        # Search in descriptions using case-insensitive matching
        filtered = [
            expense for expense in self.expenses.values()
            if query_lower in expense["description"].lower()
        ]
        
        # Sort by date
        filtered.sort(
            key=lambda x: datetime.fromisoformat(x["timestamp"]), 
            reverse=True
        )
        
        return filtered
    
    def get_total_expenses(self) -> float:
        """
        Calculate total of all expenses.
        Demonstrates sum function with generator expression.
        
        Returns:
            Total amount of all expenses
        """
        return sum(expense["amount"] for expense in self.expenses.values())
    
    def get_expenses_by_category(self) -> Dict[str, Dict[str, Union[float, int]]]:
        """
        Get summary of expenses grouped by category.
        Demonstrates dictionary manipulation and aggregation.
        
        Returns:
            Dictionary with category summaries
        """
        summary = {}
        
        # Initialize all categories
        for category_key, category_name in self.categories.items():
            summary[category_key] = {
                "name": category_name,
                "total": 0.0,
                "count": 0
            }
        
        # Aggregate expenses by category
        for expense in self.expenses.values():
            category = expense["category"]
            summary[category]["total"] += expense["amount"]
            summary[category]["count"] += 1
        
        return summary
    
    def get_monthly_summary(self, year: int, month: int) -> Dict:
        """
        Get summary for a specific month.
        Demonstrates datetime manipulation and filtering.
        
        Args:
            year: Year (YYYY)
            month: Month (1-12)
            
        Returns:
            Dictionary with monthly summary
        """
        try:
            # Create start and end dates for the month
            start_date = datetime(year, month, 1)
            if month == 12:
                end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
            else:
                end_date = datetime(year, month + 1, 1) - timedelta(days=1)
        except ValueError:
            raise ValueError("Invalid year or month")
        
        # Filter expenses for the month
        monthly_expenses = [
            expense for expense in self.expenses.values()
            if start_date <= datetime.fromisoformat(expense["timestamp"]) <= end_date
        ]
        
        # Calculate summary
        total_amount = sum(expense["amount"] for expense in monthly_expenses)
        expense_count = len(monthly_expenses)
        
        # Category breakdown
        category_totals = {}
        for expense in monthly_expenses:
            category = expense["category"]
            category_totals[category] = category_totals.get(category, 0) + expense["amount"]
        
        return {
            "month": f"{year}-{month:02d}",
            "total_amount": total_amount,
            "expense_count": expense_count,
            "category_breakdown": category_totals,
            "expenses": monthly_expenses
        }
    
    def delete_expense(self, expense_id: str) -> bool:
        """
        Delete an expense by ID.
        
        Args:
            expense_id: ID of expense to delete
            
        Returns:
            True if deleted, False if not found
        """
        if expense_id in self.expenses:
            del self.expenses[expense_id]
            self.save_data()
            return True
        return False
    
    def save_data(self) -> None:
        """
        Save expenses to JSON file.
        Demonstrates JSON serialization and file I/O.
        """
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.expenses, f, indent=2, default=str)
        except Exception as e:
            raise Exception(f"Could not save data to {self.data_file}: {e}")
    
    def load_data(self) -> None:
        """
        Load expenses from JSON file.
        Demonstrates JSON deserialization and error handling.
        """
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    self.expenses = json.load(f)
            except Exception as e:
                raise Exception(f"Could not load data from {self.data_file}: {e}")
        else:
            # File doesn't exist, start with empty expenses
            self.expenses = {}
    
    def _generate_unique_id(self) -> str:
        """Generate a unique ID that doesn't conflict with existing expenses."""
        import uuid
        while True:
            new_id = str(uuid.uuid4())[:8]
            if new_id not in self.expenses:
                return new_id
    
    def load_and_merge_data(self, filename: str) -> int:
        """
        Load expenses from a JSON file and merge with existing expenses.
        Returns the number of new expenses added.
        
        Args:
            filename: Path to the JSON file to load
            
        Returns:
            Number of new expenses that were merged
        """
        if not os.path.exists(filename):
            raise Exception(f"File {filename} does not exist")
        
        try:
            with open(filename, 'r') as f:
                file_data = json.load(f)
            
            # Handle different JSON formats
            if isinstance(file_data, dict):
                if 'expenses' in file_data:
                    # Export format with metadata
                    loaded_expenses = file_data['expenses']
                else:
                    # Direct expenses dictionary
                    loaded_expenses = file_data
            else:
                raise Exception("Invalid file format: expected JSON object")
            
            # Merge expenses, handling ID conflicts
            new_count = 0
            
            for expense_id, expense_data in loaded_expenses.items():
                if expense_id not in self.expenses:
                    # ID doesn't exist, add directly
                    self.expenses[expense_id] = expense_data
                    new_count += 1
                else:
                    # ID conflict, generate new unique ID
                    new_id = self._generate_unique_id()
                    expense_data['id'] = new_id  # Update the ID in the data
                    self.expenses[new_id] = expense_data
                    new_count += 1
            
            # Auto-save the merged data
            self.save_data()
            return new_count
            
        except json.JSONDecodeError as e:
            raise Exception(f"Invalid JSON file: {e}")
        except Exception as e:
            raise Exception(f"Could not load and merge data from {filename}: {e}")

def format_currency(amount: float) -> str:
    """Utility function to format currency."""
    return f"${amount:.2f}"

def format_expense_display(expense: Dict) -> str:
    """
    Format expense for display.
    Demonstrates string formatting and dictionary access.
    """
    return (
        f"ID: {expense['id']} | "
        f"Date: {expense['date']} | "
        f"Amount: {format_currency(expense['amount'])} | "
        f"Category: {expense['category'].title()} | "
        f"User: {expense.get('user', 'N/A')} | "
        f"Description: {expense['description']}"
    )

def display_expenses_table(expenses: List[Dict]) -> None:
    """
    Display expenses in a formatted table.
    Demonstrates string formatting and iteration.
    """
    if not expenses:
        print("No expenses found.")
        return
    
    print(f"\n{'='*130}")
    print(f"{'ID':<10} {'Date':<12} {'Amount':<12} {'Category':<15} {'User':<20} {'Description':<35}")
    print(f"{'='*130}")
    
    for expense in expenses:
        print(f"{expense['id']:<10} "
              f"{expense['date']:<12} "
              f"{format_currency(expense['amount']):<12} "
              f"{expense['category'].title():<15} "
              f"{expense.get('user', 'N/A'):<20} "
              f"{expense['description'][:33]:<35}")
    
    print(f"{'='*130}")
    total = sum(expense['amount'] for expense in expenses)
    print(f"Total: {format_currency(total)} ({len(expenses)} expenses)")

def main():
    """
    Main application loop with command-line interface.
    Demonstrates user interaction and menu system.
    """
    global amount
    tracker = ExpenseTracker()
    
    print("🏦 Welcome to the Expense Tracker Application!")
    print("This application demonstrates Python's dynamic typing, dictionary usage, and datetime manipulation.")
    
    while True:
        print(f"\n{'='*60}")
        print("EXPENSE TRACKER MENU")
        print(f"{'='*60}")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Filter by Date Range")
        print("4. Filter by Category")
        print("5. Search by Description")
        print("6. View Summary by Category")
        print("7. View Monthly Summary")
        print("8. Delete Expense")
        print("9. Exit")
        print(f"{'='*60}")
        
        try:
            choice = input("Select an option (1-9): ").strip()
            
            if choice == '1':
                # Add expense - demonstrates input validation and dynamic typing
                print("\n--- Add New Expense ---")
                amount_input = input("Enter amount: $").strip()
                try:
                    # Demonstrate dynamic typing - accept both int and float
                    amount = float(amount_input)
                except ValueError:
                    print("Invalid amount. Please enter a number.")
                    continue
                
                print("\nAvailable categories:")
                for key, name in tracker.categories.items():
                    print(f"  {key}: {name}")
                
                category = input("\nEnter category: ").strip().lower()
                description = input("Enter description: ").strip()
                
                print("\nAvailable users:")
                for i, user in enumerate(tracker.users, 1):
                    print(f"  {i}. {user}")
                
                user_input = input("\nEnter user number or name: ").strip()
                # Handle numeric input
                try:
                    user_index = int(user_input) - 1
                    if 0 <= user_index < len(tracker.users):
                        user = tracker.users[user_index]
                    else:
                        raise ValueError("Invalid user number")
                except ValueError:
                    # Try to match by name
                    user = user_input
                
                date_input = input("Enter date (YYYY-MM-DD) or press Enter for today: ").strip()
                date_value = date_input if date_input else None
                
                try:
                    expense_id = tracker.add_expense(amount, category, description, user, date_value)
                    print(f"Expense added successfully! ID: {expense_id}")
                except ValueError as e:
                    print(f"Error: {e}")
            
            elif choice == '2':
                # View all expenses
                print("\n--- All Expenses ---")
                expenses = tracker.view_all_expenses()
                display_expenses_table(expenses)
            
            elif choice == '3':
                # Filter by date range - demonstrates datetime manipulation
                print("\n--- Filter by Date Range ---")
                start_date = input("Enter start date (YYYY-MM-DD): ").strip()
                end_date = input("Enter end date (YYYY-MM-DD): ").strip()
                
                try:
                    expenses = tracker.filter_expenses_by_date(start_date, end_date)
                    print(f"\nExpenses from {start_date} to {end_date}:")
                    display_expenses_table(expenses)
                except ValueError as e:
                    print(f"Error: {e}")
            
            elif choice == '4':
                # Filter by category
                print("\n--- Filter by Category ---")
                print("Available categories:")
                for key, name in tracker.categories.items():
                    print(f"  {key}: {name}")
                
                category = input("\nEnter category: ").strip().lower()
                
                try:
                    expenses = tracker.filter_expenses_by_category(category)
                    print(f"\nExpenses in category '{category}':")
                    display_expenses_table(expenses)
                except ValueError as e:
                    print(f"Error: {e}")
            
            elif choice == '5':
                # Search by description
                print("\n--- Search by Description ---")
                query = input("Enter search query: ").strip()
                
                if query:
                    expenses = tracker.search_expenses(query)
                    print(f"\nExpenses containing '{query}':")
                    display_expenses_table(expenses)
                else:
                    print("Please enter a search query.")
            
            elif choice == '6':
                # View summary by category - demonstrates dictionary manipulation
                print("\n--- Expenses Summary by Category ---")
                summary = tracker.get_expenses_by_category()
                total_all = tracker.get_total_expenses()
                
                print(f"\n{'Category':<20} {'Total Amount':<15} {'Count':<8} {'Percentage':<12}")
                print(f"{'='*60}")
                
                for category_key, data in summary.items():
                    if data['count'] > 0:  # Only show categories with expenses
                        percentage = (data['total'] / total_all * 100) if total_all > 0 else 0
                        print(f"{data['name']:<20} "
                              f"{format_currency(data['total']):<15} "
                              f"{data['count']:<8} "
                              f"{percentage:.1f}%")
                
                print(f"{'='*60}")
                print(f"{'TOTAL':<20} {format_currency(total_all):<15} "
                      f"{sum(data['count'] for data in summary.values()):<8}")
            
            elif choice == '7':
                # Monthly summary - demonstrates datetime manipulation
                print("\n--- Monthly Summary ---")
                try:
                    year = int(input("Enter year (YYYY): ").strip())
                    month = int(input("Enter month (1-12): ").strip())
                    
                    summary = tracker.get_monthly_summary(year, month)
                    
                    print(f"\n--- Summary for {summary['month']} ---")
                    print(f"Total Amount: {format_currency(summary['total_amount'])}")
                    print(f"Number of Expenses: {summary['expense_count']}")
                    
                    if summary['category_breakdown']:
                        print(f"\nCategory Breakdown:")
                        for category, amount in summary['category_breakdown'].items():
                            category_name = tracker.categories.get(category, category)
                            print(f"  {category_name}: {format_currency(amount)}")
                    
                except ValueError as e:
                    print(f"Error: {e}")
            
            elif choice == '8':
                # Delete expense
                print("\n--- Delete Expense ---")
                expense_id = input("Enter expense ID to delete: ").strip()
                
                if tracker.delete_expense(expense_id):
                    print("Expense deleted successfully!")
                else:
                    print("Expense not found.")
            
            elif choice == '9':
                print("Thank you for using the Expense Tracker! ")
                break
            
            else:
                print("Invalid option. Please select 1-9.")
        
        except KeyboardInterrupt:
            print("\n\nGoodbye! ")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main() 