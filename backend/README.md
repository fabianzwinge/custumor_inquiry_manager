# Backend

To set up and run the backend application:


1.  **Setup Venv**:
    ```bash
    python -m venv venv && venv/Scripts/activate
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Start the application**:
    ```bash
    uvicorn main:app --reload
    ```

This will start the backend application in development mode.