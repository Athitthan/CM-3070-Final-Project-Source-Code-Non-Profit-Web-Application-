# CM-3070-Final-Project-Source-Code-Non-Profit-Web-Application-
The is the source code of my non profilt web application (Shine In Darkness)

## Getting Started

These instructions will help you set up a copy of the project running on your local machine for development and testing purposes. Follow these steps to get started.

### Prerequisites

Before you begin, ensure you have the following tools installed on your system:

- Python (3.8 or newer): [https://www.python.org/downloads/](https://www.python.org/downloads/)
- pip (Python package manager): Comes with Python.
- Virtualenv: Install by running `pip install virtualenv`.

### Setting Up the Development Environment


1. **Clone the repository**

   Start by cloning the project repository to your local machine:

   ```bash
   git clone https://github.com/Athitthan/CM-3070-final-project-web-app-souce-code.git
   cd CM-3070-final-project-web-app-souce-code
   ```


#### Using `virtualenv`

2.Create and activate a virtual environment:

  ```bash
   virtualenv venv
   source venv/bin/activate  # On Unix or MacOS
   .\venv\Scripts\activate  # On Windows
  ```


#### Common Steps

After setting up your virtual environment using either option:

3. Install project dependencies:

   ```bash
   pip install -r requirements.txt
   ```


4. Run database migrations:

   ```bash
   python manage.py migrate
   ```

5. Start the development server:

   ```bash
   python manage.py runserver
   ```

   Visit `http://127.0.0.1:8080/` in your browser to view the project.

## Running the Tests

Running automated tests for this project:

```bash
python manage.py test
```


