# Expense Management System

This project is an expense management system that consists of a Streamlit Frontend application and a FastAPI backend server.

## Project Structure

**frontend/**: Contains the Streamlit application code.
**backend/**: Contains the FastAPI backend server code.
**tests/**: Contains the test cases for both frontend and backend.
**requirement.txt/**: Lists the required python packages.
**README.md/**: Provides an overview and instructions for the project.


## Setup Instructions

1. **clone the repository**:
```bash
git clone https://github.com/shivududeshi/expense-management-system.git
cd expense-management-system
```
2. **Install dependencies:**:
```commandline
pip install -r requirements.txt
```
3. **Run the FastAPI server:**:
```commandline
uvicorn server.server:app --reload
```
4. **Run the Streamlit app:**:
```commandline
streamlit run frontend/app.py
```
