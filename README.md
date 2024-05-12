
**FastAPI Image Processing API**
This API provides endpoints for user management and image processing using FastAPI.

**Installation**
Ensure you have Python 3.12 installed.

**Clone this repository:**
git clone https://github.com/your-username/your-repo.git

**Navigate into the project directory:**
cd "BLEED AI"

**Install dependencies using pip:**
pip install -r requirements.txt

**Running the app**
uvicorn main:app --reload



**API Endpoints**
POST /token: Get an access token by providing username and password.

POST /users/: Create a new user.

GET /users/{user_id}: Get user details by ID.

PUT /users/{user_id}: Update user details by ID.

DELETE /users/{user_id}: Delete user by ID.

GET /users/: Search for users by name.

POST /process-image: Process an image file uploaded by the user. Returns the processed image with facial landmarks annotated.
