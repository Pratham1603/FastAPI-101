from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json

class Patient(BaseModel):

    id: Annotated[str, Field(..., title="Patient ID", description="ID of the patient", example="P001")]
    name: Annotated[str, Field(..., title="Name", description="Name of the patient", example="Ananya Verma")]
    city: Annotated[str, Field(..., title="City", description="City of the patient", example="Guwahati")]
    age: Annotated[int, Field(..., gt=0, lt=120, title="Age", description="Age of the patient", example=28)]
    gender: Annotated[Literal['male', 'female', 'other'], Field(..., title="Gender", description="Gender of the patient", example="female")]
    height: Annotated[float, Field(..., gt=0, title="Height", description="Height of the patient in meters", example=1.65)]
    weight: Annotated[float, Field(..., gt=0, title="Weight", description="Weight of the patient in kilograms", example=90.0)]

    # bmi and verdict = we will calculate them based on height and weight, so we will not take them as input from the user
    @computed_field
    @property
    def bmi(self) -> float:
        bmi =  round(self.weight / (self.height ** 2), 2)
        return bmi

    @computed_field
    @property
    def verdict(self) -> str:
        bmi_value = self.bmi
        if bmi_value < 18.5:
            return "Underweight"
        elif 18.5 <= bmi_value < 24.9:
            return "Normal weight"
        elif 25 <= bmi_value < 29.9:
            return "Overweight"
        else:
            return "Obesity"

# Making new pydantic model for update patient record
# why not old pydantic model? coz, older model has required fields that are complulsory to fill, but we don't know what user wants to update, so we will make all fields optional in the new model.
class PatientUpdate(BaseModel):

    # id --> user will put the id so we will know which patient record to update.
    name: Annotated[Optional[str], Field(default=None, title="Name", description="Name of the patient", example="Ananya Verma")]
    city: Annotated[Optional[str], Field(default=None, title="City", description="City of the patient", example="Guwahati")]
    age: Annotated[Optional[int], Field(default=None, gt=0, lt=120, title="Age", description="Age of the patient", example=28)]
    gender: Annotated[Optional[Literal['male', 'female', 'other']], Field(default=None, title="Gender", description="Gender of the patient", example="female")]
    height: Annotated[Optional[float], Field(default=None, gt=0, title="Height", description="Height of the patient in meters", example=1.65)]
    weight: Annotated[Optional[float], Field(default=None, gt=0, title="Weight", description="Weight of the patient in kilograms", example=90.0)]

def load_data():
    with open('patient.json', 'r') as f:
        data = json.load(f)

    return data

def save_data(data):
    with open('patient.json', 'w') as f:
        json.dump(data, f)

app = FastAPI()

@app.get("/")
def hello():
    return {"message": "Hello, World!"}

@app.get('/about')
def about():
    return {'message': 'A fully functional API to manage your patient records'}

@app.get('/view')
def view():
    data = load_data()
    return data

@app.get('/patient/{patient_id}')
def view_patient(patient_id: str = Path(..., title="Patient ID", example="P001", description="The unique identifier for a patient")):
    # load all patient data 
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found")

@app.get('/sort')
def sort_patients(sort_by: str = Query(..., title="Sort By", description="Sort patient records by specific fields", example="height"), order: str = Query('asc', title="Order", description="ascending or descending", example="asc")):

    valid_fields = ['height', 'weight', 'bmi']
    # handle wrong inputs rather than valid_fields
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort field choose from {valid_fields}")

    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail=f"Invalid order value. Choose from 'asc' or 'desc'")

    # sort the data based on the specified field and order
    data = load_data()
    sorted_data = sorted(data.values(), key=lambda x: x[sort_by], reverse=(order == 'desc'))
    return sorted_data              


@app.post('/create')
def create_patient(patient: Patient):  

    # 1. load existing patient data
    data = load_data()

    # 2. check if patient with the same ID already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient with this ID already exists")

    # add the new patient data to the existing data

    # problem: data is a pydantic object, we need to convert it to a dictionary before adding it to the data
    # solution: serialization in pydantic : .model_dump() method to convert the patient object to a dictionary

    # 3. convert pydantic object to dictionary
    patient_data = patient.model_dump(exclude=['id']) # exclude the 'id' field since it's already used as the key
    data[patient.id] = patient_data

    # 4. save the updated data back to the JSON file ( create new function save_data() to save the data to the JSON file)
    save_data(data)

    return JSONResponse(status_code=201, content={"message": "Patient record created successfully", "patient_id": patient.id}) # in json response send 2 things: status_code and content.

# PUT - Update patient record
@app.put('/update/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate):

    # 1. load existing patient data
    data = load_data()

    # 2. check if patient with the given ID exists
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")

    # 3. update the patient record with the new data
    existing_patient_info = data[patient_id]

    # update only the fields that are provided in the request body
    updated_patient_data = patient_update.model_dump(exclude_unset=True)
    # why patient_update.model_dump()? --> coz patient_update is a pydantic object, we need to convert it to a dictionary before updating the existing patient data.
    # exclude_unset=True? ---> will only include fields that are provided in the request body and not all fields.
    # Now, existing_patient_info --> has all old data
    # updated_patient_data --> has only new data that user wants to update

    # update the existing patient data with the new data
    for key, value in updated_patient_data.items():
        existing_patient_info[key] = value            # updated 

    # New problem - what of user updates height or weight? --> we need to recalculate bmi and verdict
    # solution - make pyadantic object of existing_patient_info and then get the new bmi and verdict from it automatically
    #            then convert the pydantic object to dictionary so new data can save in the JSON file
    existing_patient_info['id'] = patient_id  # --> id was not there so pydantic object can't make!
    patient_pydantic_obj = Patient( **existing_patient_info)  
    # obj --> dict
    existing_patient_info = patient_pydantic_obj.model_dump(exclude=['id'])  # exclude id = already used as the key

    # add dict to data
    data[patient_id] = existing_patient_info
    

    # 4. save the updated data back to the JSON file
    save_data(data)

    return JSONResponse(status_code=200, content={"message": "Patient record updated successfully", "patient_id": patient_id})

# DELETE - Delete patient record
@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):
    # 1. load existing patient data
    data = load_data()

    # 2. check if patient with the given ID exists
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")

    # 3. delete the patient record
    del data[patient_id]

    # 4. save the updated data back to the JSON file
    save_data(data)

    return JSONResponse(status_code=200, content={"message": "Patient record deleted successfully", "patient_id": patient_id})