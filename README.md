# FavQs API Automation Testing Project

This repository contains an automated testing suite for the [FavQs API](https://favqs.com/api/), built as part of a technical assessment
The project focuses on user management workflows, including account creation, profile updates, and validation error handling.

## 🛠 Technologies & Tools

**Language:** Python 3.14+ 
**Testing Framework:** pytest 
**API Interaction:** requests 
**Environment Management:** python-dotenv 
**Logging:** Configured via `pytest.ini` for real-time console output.

## 🚀 Getting Started

### Prerequisites

1. **API Key:** You must register at [FavQs API Keys](https://favqs.com/api_keys) to obtain an API Key.
2.  **Python:** Ensure Python is installed on your system.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd FavQs_API_Test
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv .venv
    # Windows:
    .venv\Scripts\activate
    # macOS/Linux:
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Configuration

Create a `.env` file in the root directory and add your FavQs API Key:

```env
FAVQS_API_KEY=your_api_key_here
