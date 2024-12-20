# Web Scraping API with FastAPI

Welcome to the Web Scraping API! This FastAPI application scrapes a given URL's homepage content and extracts key information such as the industry, company size, and location. It's designed to be simple, efficient, and secure, with built-in authentication and robust error handling.

## Features

- **Homepage Scraping:** Scrapes only the homepage (no deep links).
- **Industry Extraction:** Identifies the industry (e.g., Technology, Healthcare, etc.) from the text.
- **Company Size Detection:** Determines whether the company is small, medium, or large based on the content.
- **Location Extraction:** Extracts the location (city or country) from the content.
- **Authentication:** Secure access via a secret key, ensuring only authorized requests can access the service.
- **Error Handling:** Graceful error responses for invalid URLs, unauthorized requests, or scraping failures.

## Setup & Installation

Follow these steps to get the application running on your local machine or in a Docker container.

### Prerequisites

1. **Python 3.7+**
2. **pip** (Python package installer)
3. **Docker** (optional, but recommended for containerization)
4. **Virtual Environment** (recommended to keep dependencies isolated)

### Steps to Run Locally

1. **Clone the repository:**

    ```bash
    git clone https://github.com/praful-vats/firmable_scraper.git
    cd your-repo-name
    ```

2. **Set up a virtual environment:**

   - **For Windows:**

     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```

   - **For Linux/macOS:**

     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Create a `.env` file** in the root directory and add the `SECRET_KEY` for authentication:

    ```bash
    SECRET_KEY=your_secret_key_here
    ```

    > **Important:** Replace `your_secret_key_here` with a secure, unique key that you’ll use to authenticate requests.

5. **Run the FastAPI application:**

    ```bash
    uvicorn main:app --reload
    ```

    The app will be available at `http://127.0.0.1:8000`.

---

## Testing the API on Render

You can test the deployed API live at:  
**[https://firmable-scraper.onrender.com/scrape](https://firmable-scraper.onrender.com/scrape)**  

Make sure to include the required `Authorization` header with your `SECRET_KEY` while making requests.

---

## API Endpoints

### POST `/scrape`

This endpoint scrapes the homepage of a given URL and extracts key details like the industry, company size, and location.

**Request:**

- **Headers:**
  - `Authorization`: Your `SECRET_KEY` (set in the `.env` file).
  
- **Body:**

  ```json
  {
    "url": "http://example.com"
  }
