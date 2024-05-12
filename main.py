import io
import cv2
from fastapi.responses import StreamingResponse
from fastapi import File, UploadFile
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from datetime import datetime, timedelta
from models import User
from schemas import UserCreate, UserUpdate, User as UserSchema
from crud import (
    create_user,
    get_user,
    update_user,
    delete_user, 
    search_users,
)  


from security import verify_token,create_access_token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

 

ACCESS_TOKEN_EXPIRE_MINUTES = 1
app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




def authenticate_user(username: str, password: str):
    return username == "admin" and password == "admin"
@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    if not authenticate_user(form_data.username, form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}





@app.post("/users/", response_model=UserSchema)
def create_user_api(user_data: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user_data)

@app.get("/users/{user_id}", response_model=UserSchema)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.put("/users/{user_id}", response_model=UserSchema)
def update_user_api(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    db_user = update_user(db, user_id, user_data)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.delete("/users/{user_id}", response_model=bool)
def delete_user_api(user_id: int, db: Session = Depends(get_db), username: str = Depends(verify_token)):
    deleted = delete_user(db, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return deleted

@app.get("/users/", response_model=list[UserSchema])
def search_users_api(name: str, db: Session = Depends(get_db)):
    return search_users(db, name)



from fastapi import FastAPI, File, UploadFile, HTTPException
import cv2
import mediapipe as mp
import numpy as np
from PIL import Image
import io
from fastapi.responses import JSONResponse, FileResponse
import tempfile
import matplotlib.pyplot as plt

@app.post("/process-image")
async def process_image(image: UploadFile = File(...)):
    # Read the image file as numpy array
    contents = await image.read()
    
    nparr = np.frombuffer(contents, np.uint8)
    
    # Convert numpy array to OpenCV format
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    height, width, _ = img.shape
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Initialize MediaPipe face detection and landmark models
    mp_face_detection = mp.solutions.face_detection
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh=mp_face_mesh.FaceMesh(refine_landmarks=True)

    mesh_img=img_rgb
    face_mesh_result=face_mesh.process(img_rgb)
    print(face_mesh_result)

    landmarks=[]

    ## I don't know why its not getting facelandmarks
    if(face_mesh_result.multi_face_landmarks):
        for facial_landmarks in face_mesh_result.multi_face_landmarks:
            for i in range(0, 468):
                pt1=facial_landmarks.landmark[i]
                x=int(pt1.x * width)
                y=int(pt1.y * height)
                cv2.circle(mesh_img, (x,y), 2, (100, 100, 0), -1)
                landmarks.append({"x": x, "y": y})

    annotated_image=img.copy()
    # Run MediaPipe face detection
    with mp_face_detection.FaceDetection(min_detection_confidence=0.5) as face_detection:
        # Convert the image to RGB
        results = face_detection.process(img_rgb)
        print(results.detections)    
        for i, detection in enumerate(results.detections):
            box=detection.location_data.relative_bounding_box
            x_start, y_start=int(box.xmin * img.shape[1]), int(box.ymin * img.shape[0])
            x_end, y_end=int((box.xmin+box.width)*img.shape[1]),int((box.ymin+box.height)*img.shape[0])
            annotated_image=cv2.rectangle(img,(x_start, y_start),(x_end,y_end),(0,255,255), 5)

    ## for testing
    plt.imshow(mesh_img)
    plt.axis('off')  # Turn off axis
    plt.show()

    plt.imshow(annotated_image)
    plt.axis('off')  # Turn off axis
    plt.show()


    temp_filename2 = tempfile.NamedTemporaryFile(suffix=".jpg").name
    cv2.imwrite(temp_filename2, cv2.cvtColor(mesh_img, cv2.COLOR_RGB2BGR))
    

    # Save annotated image to a temporary file
    temp_filename = tempfile.NamedTemporaryFile(suffix=".jpg").name
    cv2.imwrite(temp_filename, cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR))
    return FileResponse(temp_filename2, media_type="image/jpeg"), FileResponse(temp_filename, media_type="image/jpeg")
