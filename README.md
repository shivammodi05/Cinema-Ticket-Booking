# Cinema Ticket Booking System

This project is a simple cinema ticket booking system implemented in Python. It allows users to buy tickets for a cinema seat using a valid card. The system checks if the seat is available and if the card has sufficient balance before processing the purchase. A PDF ticket is generated upon successful purchase.

## Features

- Check seat availability
- Validate card details and balance
- Purchase a ticket
- Generate a PDF ticket

## Requirements

- Python 3.x
- `fpdf` library
- `sqlite3` library

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/shivammodi05/Cinema-Ticket-Booking.git
    ```
2. Navigate to the project directory:
    ```sh
    cd Cinema-Ticket-Booking
    ```
3. Install the required libraries:
    ```sh
    pip install fpdf
    ```

## Usage

1. Run the `main.py` script:
    ```sh
    python main.py
    ```
2. Follow the prompts to enter your name, seat number, and card details.

## Project Structure

- `main.py`: The main script to run the ticket booking system.
- `.venv/Lib/site-packages/fpdf/fpdf.py`: The `fpdf` library used for generating PDF tickets.
- `.gitignore`: Git ignore file to exclude unnecessary files from version control.

## Database

- `cinema.db`: SQLite database containing seat information.
- `banking.db`: SQLite database containing card information.

## License

This project is licensed under the MIT License.
