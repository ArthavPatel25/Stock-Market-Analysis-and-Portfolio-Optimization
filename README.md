Stock Market Analysis and Portfolio Optimization
------------------------------------------------

This project analyzes stock market trends and optimizes investment portfolios using Modern Portfolio Theory (MPT). It utilizes Python for data processing and visualization, PostgreSQL for data storage, and visualization libraries like Matplotlib and Seaborn.

Features:
- Fetch historical stock data using Python and the yFinance library.
- Apply Modern Portfolio Theory (MPT) for portfolio optimization.
- Analyze performance metrics like Sharpe Ratio, Volatility, and Expected Returns.
- Visualize data and results using Matplotlib and Seaborn.
- Store and manage data in PostgreSQL.

Installation Steps:
1. Clone the repository:
   git clone https://github.com/ArthavPatel25/stock-market-portfolio-optimization.git
   cd stock-market-portfolio-optimization

2. Create and activate a virtual environment (optional but recommended):
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies:
   pip install -r requirements.txt

4. Setup Environment Variables:
   - Create a `.env` file based on `.env.example`.
   - Fill in your PostgreSQL database credentials.

5. Set up the PostgreSQL database:
   - Create the database and tables using the provided SQL files in the `database/` directory.

6. Run the main Python script:
   python scripts/portfolio_optimization.py

Project Structure:
- data/                : Contains raw and processed stock data in CSV format.
- database/            : SQL files for database schema and table creation.
- scripts/             : Python scripts for data processing and optimization.
- dashboard/           : Visualization assets and exported charts.
- requirements.txt     : Python dependencies list.
- README.txt           : Project documentation and instructions.
- .gitignore           : Lists files and directories to be ignored by Git.

Notes:
- Ensure that PostgreSQL is installed and running on your machine.
- Update the `.env` file with the correct database credentials.
- The `.env` file is excluded from version control for security reasons.

License:
This project is licensed under the MIT License.

Author:
Arthav Patel (https://github.com/ArthavPatel25)
