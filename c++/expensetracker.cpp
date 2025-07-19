#include <iostream> // For input/output operations (cin, cout)
#include <vector>   // For std::vector to store expenses
#include <string>   // For std::string to handle text data
#include <iomanip>  // For std::fixed and std::setprecision for formatting output
#include <map>      // For std::map to store category summaries
#include <algorithm> // For std::remove_if to potentially remove items (though not directly used for deletion here)
#include <limits>   // For std::numeric_limits to clear input buffer

// Define a structure to represent an individual expense
// Using a struct makes all members public by default, which is suitable for a simple data container.
struct Expense {
    std::string date;        // Date of the expense (e.g., "YYYY-MM-DD")
    double amount;           // Amount of the expense
    std::string category;    // Category of the expense (e.g., "Food", "Transport")
    std::string description; // Description of the expense

    // Constructor to easily create Expense objects
    Expense(std::string d, double a, std::string c, std::string desc)
        : date(std::move(d)), amount(a), category(std::move(c)), description(std::move(desc)) {}
};

// Function to display a single expense
void displayExpense(const Expense& exp) {
    std::cout << std::fixed << std::setprecision(2); // Set precision for amount
    std::cout << "  Date: " << exp.date
              << ", Amount: $" << exp.amount
              << ", Category: " << exp.category
              << ", Description: " << exp.description << std::endl;
}

// Function to add a new expense
void addExpense(std::vector<Expense>& expenses) {
    std::string date, category, description;
    double amount;

    std::cout << "\n--- Add New Expense ---" << std::endl;
    std::cout << "Enter Date (YYYY-MM-DD): ";
    std::cin >> date;
    std::cout << "Enter Amount: $";
    // Input validation for amount
    while (!(std::cin >> amount) || amount <= 0) {
        std::cout << "Invalid amount. Please enter a positive number: $";
        std::cin.clear(); // Clear error flags
        // Ignore remaining characters in the input buffer up to the newline
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
    }
    // Clear the input buffer after reading amount to prepare for getline
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');

    std::cout << "Enter Category (e.g., Food, Transport, Utilities): ";
    std::getline(std::cin, category); // Use getline to read category with spaces
    std::cout << "Enter Description: ";
    std::getline(std::cin, description); // Use getline to read description with spaces

    expenses.emplace_back(date, amount, category, description); // Add expense to vector
    std::cout << "Expense added successfully!" << std::endl;
}

// Function to view all expenses
void viewAllExpenses(const std::vector<Expense>& expenses) {
    std::cout << "\n--- All Expenses ---" << std::endl;
    if (expenses.empty()) {
        std::cout << "No expenses recorded yet." << std::endl;
        return;
    }
    for (const auto& exp : expenses) {
        displayExpense(exp);
    }
}

// Function to filter expenses by date range
void filterExpensesByDate(const std::vector<Expense>& expenses) {
    std::string startDateStr, endDateStr;
    std::cout << "\n--- Filter Expenses by Date Range ---" << std::endl;
    std::cout << "Enter Start Date (YYYY-MM-DD): ";
    std::cin >> startDateStr;
    std::cout << "Enter End Date (YYYY-MM-DD): ";
    std::cin >> endDateStr;
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n'); // Clear buffer

    std::cout << "\nExpenses from " << startDateStr << " to " << endDateStr << ":" << std::endl;
    bool found = false;
    for (const auto& exp : expenses) {
        // Simple string comparison for dates (assumes YYYY-MM-DD format for correct lexicographical order)
        if (exp.date >= startDateStr && exp.date <= endDateStr) {
            displayExpense(exp);
            found = true;
        }
    }
    if (!found) {
        std::cout << "No expenses found in this date range." << std::endl;
    }
}

// Function to filter expenses by category
void filterExpensesByCategory(const std::vector<Expense>& expenses) {
    std::string categoryFilter;
    std::cout << "\n--- Filter Expenses by Category ---" << std::endl;
    std::cout << "Enter Category to filter by: ";
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n'); // Clear buffer before getline
    std::getline(std::cin, categoryFilter);

    std::cout << "\nExpenses in category '" << categoryFilter << "':" << std::endl;
    bool found = false;
    for (const auto& exp : expenses) {
        // Case-insensitive comparison for category
        std::string expCategoryLower = exp.category;
        std::string filterCategoryLower = categoryFilter;
        std::transform(expCategoryLower.begin(), expCategoryLower.end(), expCategoryLower.begin(), ::tolower);
        std::transform(filterCategoryLower.begin(), filterCategoryLower.end(), filterCategoryLower.begin(), ::tolower);

        if (expCategoryLower == filterCategoryLower) {
            displayExpense(exp);
            found = true;
        }
    }
    if (!found) {
        std::cout << "No expenses found for category '" << categoryFilter << "'." << std::endl;
    }
}

// Function to calculate and display summary of expenses
void showSummary(const std::vector<Expense>& expenses) {
    std::map<std::string, double> categoryTotals;
    double overallTotal = 0.0;

    for (const auto& exp : expenses) {
        categoryTotals[exp.category] += exp.amount;
        overallTotal += exp.amount;
    }

    std::cout << "\n--- Expense Summary ---" << std::endl;
    if (expenses.empty()) {
        std::cout << "No expenses recorded yet to summarize." << std::endl;
        return;
    }

    std::cout << "Total Expenses by Category:" << std::endl;
    std::cout << std::fixed << std::setprecision(2); // Set precision for amounts
    for (const auto& pair : categoryTotals) {
        std::cout << "  " << pair.first << ": $" << pair.second << std::endl;
    }

    std::cout << "\nOverall Total Expenses: $" << overallTotal << std::endl;
}

// Main function to run the application
int main() {
    std::vector<Expense> expenses; // Vector to store all expense objects
    int choice;

    do {
        std::cout << "\n--- Expense Tracker Menu ---" << std::endl;
        std::cout << "1. Add Expense" << std::endl;
        std::cout << "2. View All Expenses" << std::endl;
        std::cout << "3. Filter Expenses by Date Range" << std::endl;
        std::cout << "4. Filter Expenses by Category" << std::endl;
        std::cout << "5. Show Summary" << std::endl;
        std::cout << "6. Exit" << std::endl;
        std::cout << "Enter your choice: ";

        // Input validation for menu choice
        while (!(std::cin >> choice) || choice < 1 || choice > 6) {
            std::cout << "Invalid choice. Please enter a number between 1 and 6: ";
            std::cin.clear(); // Clear error flags
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n'); // Ignore remaining characters
        }

        switch (choice) {
            case 1:
                addExpense(expenses);
                break;
            case 2:
                viewAllExpenses(expenses);
                break;
            case 3:
                filterExpensesByDate(expenses);
                break;
            case 4:
                filterExpensesByCategory(expenses);
                break;
            case 5:
                showSummary(expenses);
                break;
            case 6:
                std::cout << "Exiting Expense Tracker. Goodbye!" << std::endl;
                break;
            default:
                // This case should ideally not be reached due to input validation
                std::cout << "An unexpected error occurred. Please try again." << std::endl;
                break;
        }
    } while (choice != 6); // Continue loop until user chooses to exit

    return 0; // Indicate successful execution
}
