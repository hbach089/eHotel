from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,SelectField,FieldList,IntegerField
from wtforms.validators import DataRequired,Length

class roomForm(FlaskForm):
  capacity=SelectField(u"Capacity",
  choices=[('single','single'),('double','double'),('triple','triple')])
  view=SelectField(u"View",
  choices=[('seaview','seaview'),('mountain view','mountain view')])
  submit=SubmitField('Submit')
  
class CustInfoForm(FlaskForm):
  ssn=StringField("SSN",render_kw={"placeholder": "SSN"},validators=[DataRequired(),Length(min=0,max=40,message="Input must be fewer than 40 characters!")])
  fname=StringField("First Name",render_kw={"placeholder": "First Name"},validators=[DataRequired(),Length(min=0,max=40,message="Input must be fewer than 40 characters!")])
  lname=StringField("Last Name",render_kw={"placeholder": "Last Name"},validators=[DataRequired(),Length(min=0,max=40,message="Input must be fewer than 40 characters!")])
  street=StringField("Street",render_kw={"placeholder": "Street"},validators=[DataRequired(),Length(min=0,max=40,message="Input must be fewer than 40 characters!")])
  city=StringField("City",render_kw={"placeholder": "City"},validators=[DataRequired(),Length(min=0,max=40,message="Input must be fewer than 40 characters!")])
  province=SelectField(u"Province",
                          choices=[("Metropolitan","Metropolitan"),("Serenity Province","Serenity Province"),("Harmony State","Harmony State"),("Celestial Region","Celestial Region")])
  #province=StringField("Province",render_kw={"placeholder": "Province"},validators=[DataRequired(),Length(min=0,max=40,message="Input must be fewer than 40 characters!")])
  postalcode=StringField("PostalCode",render_kw={"placeholder": "PostalCode"},validators=[DataRequired(),Length(min=0,max=40,message="Input must be fewer than 40 characters!")]) 
  phonenumber=StringField("Phonenumber",render_kw={"placeholder":"Phonenumber"},validators=[DataRequired(),Length(min=0,max=40,message="Input must be fewer than 40 characters!")])
  book=SubmitField('Book room')
  back=SubmitField("Go back")
  
class thankyouForm(FlaskForm):
  updatecust=SubmitField('Change Customer Info')
  deletebook=SubmitField('Cancel booking')
  
class loginForm(FlaskForm):
  cust=SubmitField('Customer')
  empl=SubmitField('Employee')
  
class empLoginForm(FlaskForm):
  empssn=IntegerField("EmpSSN",render_kw={"placeholder":"Employee SSN"},validators=[DataRequired(),])
  hid=IntegerField("HotelID",render_kw={"placeholder":"Hotel ID"},validators=[DataRequired(),])
  login=SubmitField("Login")
  
class emplRegisterForm(FlaskForm):
  empssn=StringField("Employee SSN",render_kw={"placeholder":"Employee SSN"},validators=[DataRequired(),])
  fname=StringField("First Name",render_kw={"placeholder": "First Name"},validators=[DataRequired(),Length(min=0,max=40,message="Input must be fewer than 40 characters!")])
  lname=StringField("Last Name",render_kw={"placeholder": "Last Name"},validators=[DataRequired(),Length(min=0,max=40,message="Input must be fewer than 40 characters!")])
  street=StringField("Street",render_kw={"placeholder": "Street"},validators=[DataRequired(),Length(min=0,max=40,message="Input must be fewer than 40 characters!")])
  city=StringField("City",render_kw={"placeholder": "City"},validators=[DataRequired(),Length(min=0,max=40,message="Input must be fewer than 40 characters!")])
  province=StringField("Province",render_kw={"placeholder": "Province"},validators=[DataRequired(),Length(min=0,max=40,message="Input must be fewer than 40 characters!")])
  postalcode=StringField("PostalCode",render_kw={"placeholder": "PostalCode"},validators=[DataRequired(),Length(min=0,max=40,message="Input must be fewer than 40 characters!")]) 
  position=SelectField(u"Position",
                          choices=[("Manager","Manager"),("Front Desk","Front Desk"),("Housekeeping","Housekeeping"),("Maintenance","Maintenance")])  
  phonenumber=StringField("Phonenumber",render_kw={"placeholder":"Phonenumber"},validators=[DataRequired(),Length(min=0,max=40,message="Input must be fewer than 40 characters!")])
  addEmp=SubmitField("Add employee!")
  remEmp=SubmitField("Fire employee(s)")
  backbtn=SubmitField("Go back")
  
class managerChoices(FlaskForm):
  rooms=SubmitField("Rooms")
  hotels=SubmitField("Hotels")
  employees=SubmitField("Employees")
  backbtn=SubmitField("Go back")
  
class roomChoices(FlaskForm):
  del_upd=SubmitField('Delete or Update')
  insert=SubmitField("Add new room")
  remove=SubmitField("Delete room(s)")
  change=SubmitField("Modify room(s)")
  backbtn=SubmitField("Go back")
  
class hotelChoices(FlaskForm):
  del_upd=SubmitField('Delete or Update')
  insert=SubmitField("Add new hotel")
  remove=SubmitField("Delete room(s)")
  change=SubmitField("Modify room(s)")
  backbtn=SubmitField("Go back")

class roomsUpdate(FlaskForm):
  roomnum=IntegerField("RoomNumber",render_kw={"placeholder":"RoomNumber"},validators=[DataRequired(),])
  extendable=SelectField(u"Extendable",choices=[("Extendable","True"),("Not Extendable","False")])
  capacity=SelectField(u"single",choices=[("single","single"),("double","double"),("triple","triple")])
  seaview=SelectField(u"View",choices=[("Seaview","Seaview"),("Mountain View","Mountain View"),])
  price=StringField("Price",render_kw={"placeholder": "Price"},validators=[DataRequired(),Length(min=0,max=40,message="Input must be fewer than 40 characters!")])
  update=SubmitField("Update")
  backbtn=SubmitField("Go back")
  
class CheckIn(FlaskForm):
  checkin=SubmitField('CheckIn')
  backbtn=SubmitField("Go back")


class addHotel(FlaskForm):
  hid=IntegerField("Hotel ID",render_kw={"placeholder":"Hotel ID"},validators=[DataRequired(),])
  hname=StringField("Hotel Name",render_kw={"placeholder": "Hotel Name"},validators=[DataRequired(),Length(min=0,max=40,message="Input must be fewer than 40 characters!")])
  street=StringField("street",render_kw={"placeholder":"street"},validators=[DataRequired(),])
  city=StringField("city",render_kw={"placeholder": "city"},validators=[DataRequired(),Length(min=0,max=40,message="Input must be fewer than 40 characters!")])
  province=StringField("province",render_kw={"placeholder": "province"},validators=[DataRequired(),Length(min=0,max=40,message="Input must be fewer than 40 characters!")])
  postalcode=StringField("postalcode",render_kw={"placeholder": "postalcode"},validators=[DataRequired(),Length(min=0,max=40,message="Input must be fewer than 40 characters!")])
  email=StringField("Email",render_kw={"placeholder": "Email"},validators=[DataRequired(),Length(min=0,max=40,message="Input must be fewer than 40 characters!")])
  rating=IntegerField("rating",render_kw={"placeholder":"rating"},validators=[DataRequired(),])
  postalcode=StringField("PostalCode",render_kw={"placeholder": "PostalCode"},validators=[DataRequired(),Length(min=0,max=40,message="Input must be fewer than 40 characters!")]) 
  phonenumber=StringField("Phonenumber",render_kw={"placeholder": "Phonenumber"},validators=[DataRequired(),Length(min=0,max=40,message="Input must be fewer than 40 characters!")]) 
  insert=SubmitField("Add new hotel")
