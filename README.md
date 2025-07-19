# 🧑‍💼 Employee Management System

A Django-based Employee Management System that helps manage employee data, roles, and departments. The system includes a secure admin panel for managing records and a login system for employees to view their own details.

---

## 🚀 Features

- 🔐 **Admin Panel**: 
  - Add, update, delete employees
  - Assign departments and roles
  - Search and filter employees by department

- 👥 **Employee Login**:
  - View personal details
  - View assigned department and role

- 🗂️ **Models**:
  - `Employee`: Contains employee info (name, email, department, role, etc.)
  - `Department`: Lists available departments
  - `Role`: Lists available roles

---

## 🛠️ Tech Stack

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS (Bootstrap for styling)
- **Database**: SQLite (default Django DB)
- **Authentication**: Django built-in auth system

---

## 🔧 Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Prakhar-Maitreya/Employee-Portal-Cipherschools.git
   cd Employee-Portal-Cipherschools
   ## Or if the local folder becomes cipherSchoolproject, use that instead of cd into anything
2. **Setup SMTP**
- In [settings.py](employeeportal%2Femployeeportal%2Fsettings.py)
- edit line 52 and 53, add your email address and app password
