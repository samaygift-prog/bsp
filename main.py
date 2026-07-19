from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, FileResponse
from sqlalchemy import create_engine, text
from openpyxl import Workbook


app = FastAPI()

app.mount("/static", StaticFiles(directory="photos"), name="static")

templates = Jinja2Templates(directory="templates")


# Database
DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)



# Home - Login Page

@app.get("/")
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="login.html"
    )



# Create Database Tables

@app.get("/create-table")
def create_table():

    with engine.connect() as conn:

        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS admin_users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
        """))


        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS entries(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            mobile TEXT,
            problem TEXT,
            medical_history TEXT,
            talent TEXT,
            profession TEXT,
            second_hand_product TEXT
        )
        """))

        conn.commit()


    return {
        "message": "Tables Created"
    }




# Add Admin User

@app.get("/add-user")
def add_user():

    with engine.connect() as conn:

        conn.execute(text("""
        INSERT INTO admin_users(username,password)
        VALUES('admin','1234')
        """))

        conn.commit()


    return {
        "message":"Admin Added"
    }




# Login

@app.post("/login-page")
def login_page(

    username: str = Form(...),
    password: str = Form(...)

):

    with engine.connect() as conn:

        result = conn.execute(
            text("""
            SELECT * FROM admin_users
            WHERE username=:username
            AND password=:password
            """),
            {
                "username":username,
                "password":password
            }
        )


        user = result.fetchone()



    if user:

        return RedirectResponse(
            "/entry",
            status_code=303
        )


    return {
        "message":"Invalid Login"
    }





# Entry Page

@app.get("/entry")
def entry(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="entry.html"
    )
    # Save User Entry

@app.post("/save-entry")
def save_entry(

    name: str = Form(...),
    mobile: str = Form(...),
    problem: str = Form(...),
    medical_history: str = Form(...),
    talent: str = Form(...),
    profession: str = Form(...),
    second_hand_product: str = Form(...)

):


    # Mobile Number Validation

    if not mobile.isdigit():

        return {
            "message": "Mobile number should contain only numbers"
        }


    if len(mobile) != 10:

        return {
            "message": "Mobile number must be 10 digits"
        }



    query = text("""
    INSERT INTO entries
    (
        name,
        mobile,
        problem,
        medical_history,
        talent,
        profession,
        second_hand_product
    )

    VALUES
    (
        :name,
        :mobile,
        :problem,
        :medical_history,
        :talent,
        :profession,
        :second_hand_product
    )
    """)



    with engine.connect() as conn:

        conn.execute(
            query,
            {
                "name": name,
                "mobile": mobile,
                "problem": problem,
                "medical_history": medical_history,
                "talent": talent,
                "profession": profession,
                "second_hand_product": second_hand_product
            }
        )

        conn.commit()



    # Submit ke baad blank form

    return RedirectResponse(
        "/entry",
        status_code=303
    )





# Show All Data

@app.get("/data")
def data_page(request: Request):


    with engine.connect() as conn:

        result = conn.execute(
            text("SELECT * FROM entries")
        )

        rows = result.fetchall()



    return templates.TemplateResponse(
        request=request,
        name="data.html",
        context={
            "data": rows
        }
    )





# Download Excel

@app.get("/download-excel")
def download_excel():


    with engine.connect() as conn:

        result = conn.execute(
            text("SELECT * FROM entries")
        )

        rows = result.fetchall()



    filename = "User_Data.xlsx"


    wb = Workbook()

    ws = wb.active

    ws.title = "User Data"



    ws.append(
        [
            "ID",
            "Name",
            "Mobile",
            "Problem",
            "Medical History",
            "Talent",
            "Profession",
            "Second Hand Product"
        ]
    )



    for row in rows:

        ws.append(list(row))



    wb.save(filename)



    return FileResponse(
        filename,
        filename="User_Data.xlsx"
    )

    @app.get("/clear-data")
def clear_data():

    with engine.connect() as conn:
        conn.execute(text("DELETE FROM entries"))
        conn.commit()

    return {
        "message": "All data deleted successfully"
    }