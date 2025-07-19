#include <iostream> // For input/output operations (cin, cout)
#include <vector>   // For std::vector to store expenses
#include <string>   // For std::string to handle text data
#include <iomanip>  // For std::fixed and std::setprecision for formatting output
#include <map>      // For std::map to store category summaries
#include <algorithm> // For std::transform for case-insensitive comparison
#include <limits>   // For std::numeric_limits to clear input buffer
#include <cctype>    // For ::isdigit
#include <ctime>    // For tm struct, strptime, mktime

// Define a structure to represent an individual expense
// Using a struct makes all members public by default, which is suitable for a simple data container.
struct Expense {
    std::string date;        // Date of the expense (e.g., "MM-DD-YYYY")
    double amount;           // Amount of the expense
    std::string category;    // Category of the expense (e.g., "Food", "Transport")
    std::string description; // Description of the expense

    // Constructor to easily create Expense objects
    Expense(std::string d, double a, std::string c, std::string desc)
        : date(std::move(d)), amount(a), category(std::move(c)), description(std::move(desc)) {}
};

// Helper function to parse MM-DD-YYYY string to an integer YYYYMMDD for comparison.
// Returns -1 if the format is invalid or the date itself is invalid (e.g., Feb 30th).
long parseDateToInteger(const std::string& dateStr) {
    // Basic length check for "MM-DD-YYYY" format
    if (dateStr.length() != 10) {
        return -1;
    }

    struct tm tm_struct = {0}; // Initialize tm struct to all zeros

    // Use strptime to parse the date string into the tm struct.
    // %m: month as decimal number (01-12)
    // %d: day of month as decimal number (01-31)
    // %Y: year with century as decimal number
    // strptime returns a pointer to the character after the last character parsed, or NULL on error.
    char* parse_result = strptime(dateStr.c_str(), "%m-%d-%Y", &tm_struct);

    // Check if parsing was successful and the entire string was consumed (no extra characters)
    if (parse_result == NULL || *parse_result != '\0') {
        return -1; // Parsing failed or extra characters found in the string
    }

    // Convert tm struct to time_t to normalize values and validate the date.
    // mktime will adjust tm_mday, tm_mon, tm_year if they are out of range (e.g., if you pass Feb 30).
    // It returns (time_t)-1 on failure (e.g., completely invalid date that cannot be normalized).
    time_t time_val = mktime(&tm_struct);

    if (time_val == (time_t)-1) {
        // mktime failed, indicating an invalid date (e.g., non-existent date like Feb 30)
        return -1;
    }

    // After mktime, tm_struct contains normalized and valid date components.
    // We can now safely extract year, month, day and format to YYYYMMDD for comparison.
    // tm_year is years since 1900, tm_mon is 0-11
    int year = tm_struct.tm_year + 1900;
    int month = tm_struct.tm_mon + 1;
    int day = tm_struct.tm_mday;

    // Optional: Add a reasonable year range check if desired, though mktime handles much of the validation.
    if (year < 1900 || year > 2100) {
        return -1; // Date outside a reasonable application range
    }

    // Combine into a single long integer in YYYYMMDD format for easy chronological comparison
    return (long)year * 10000 + (long)month * 100 + day;
}


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
    std::cout << "Enter Date (MM-DD-YYYY): "; // Updated prompt
    // Input validation loop for date format
    while (true) {
        std::cin >> date;
        // Clear the input buffer after reading date string (important before getline)
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        if (parseDateToInteger(date) != -1) {
            break; // Date format is valid, exit loop
        } else {
            std::cout << "Invalid date format or invalid date. Please use MM-DD-YYYY: "; // Updated error message
        }
    }

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
    long startDateInt, endDateInt;

    std::cout << "\n--- Filter Expenses by Date Range ---" << std::endl;
    std::cout << "Enter Start Date (MM-DD-YYYY): "; // Updated prompt
    // Input validation loop for start date format
    while (true) {
        std::cin >> startDateStr;
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n'); // Clear buffer
        startDateInt = parseDateToInteger(startDateStr);
        if (startDateInt != -1) {
            break;
        } else {
            std::cout << "Invalid date format or invalid date. Please use MM-DD-YYYY: "; // Updated error message
        }
    }

    std::cout << "Enter End Date (MM-DD-YYYY): "; // Updated prompt
    // Input validation loop for end date format
    while (true) {
        std::cin >> endDateStr;
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n'); // Clear buffer
        endDateInt = parseDateToInteger(endDateStr);
        if (endDateInt != -1) {
            break;
        } else {
            std::cout << "Invalid date format or invalid date. Please use MM-DD-YYYY: "; // Updated error message
        }
    }

    std::cout << "\nExpenses from " << startDateStr << " to " << endDateStr << ":" << std::endl;
    bool found = false;
    for (const auto& exp : expenses) {
        long expDateInt = parseDateToInteger(exp.date); // Convert expense date to integer

        // Compare using the integer representation of dates
        if (expDateInt != -1 && expDateInt >= startDateInt && expDateInt <= endDateInt) {
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
        // Convert both strings to lowercase for comparison
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
