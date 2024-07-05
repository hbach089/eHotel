from flask import Flask,request,render_template,redirect,url_for,flash
from room_forms import *
import psycopg2,os,ast,uuid,atexit
from datetime import datetime, time
from createtables import *

app=Flask(__name__)


user=os.getenv('DB_USERNAME')
pswd=os.getenv('DB_PASSWORD')

app.config['SECRET_KEY']='IHOPEWEGETAGOODGRADEONTHISPOS'

atexit.register(droptables)
'''conn=psycopg2.connect(database='eHotels',user='postgres',
                      password='postgres',host='localhost',port='5433')
 
cur=conn.cursor()

cur.execute('SELECT * FROM hotel NATURAL JOIN hotel_phonenumber ORDER BY rating DESC;')
all_hotel_IDs=cur.fetchall()



#cur.execute('SELECT chainID FROM hotelchain_officeaddress')
cur.execute('SELECT * FROM hotelchains NATURAL JOIN hotelchain_officeaddress NATURAL JOIN hotelchains_phonenumber')
all_hotelchain_IDs=cur.fetchall()

hotel_dict={}
hotelchains_dict={}
hotel_names=['Dolomiti', 'Tranquiluxe', 'Serenstay', 'Crestview', 'Grandeur', 'Radiance', 'Blissful', 'Solitude', 'Lumina', 'Celestial', 'Oasis', 'Elysium', 'Mirage', 'Summit', 'Enclave', 'Azure', 'HarmonyInn', 'EclipseLodge', 'MajesticView', 'WhisperingPines', 'GoldenSands', 'MoonlightManor', 'RoyalRetreat', 'SilverSprings', 'ParadisePalms', 'EmeraldHaven', 'CrystalWaters', 'StarlightSuites', 'SunriseVilla', 'TranquilityBay', 'RainbowResort', 'PeacefulHaven', 'OceanBreeze', 'MountainMajesty', 'GoldenGateHotel', 'SapphireShores', 'EvergreenLodge', 'WhimsicalWoods', 'BlueHorizonInn', 'SunsetSerenity', 'GardenGroveHotel', 'PinnaclePeaks', 'IslandOasis']

#hotel_names=['Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti']
hotelchain_names=['LuxhotelsTranquilHaven','SerenitySapphireSands','HarmonyHavenSuites','CelestialLuxLodgings','BlissVilleResorts']


j=0
for i in all_hotel_IDs:
  hotel_dict[i]=hotel_names[j]
  j+=1

j=0
for i in all_hotelchain_IDs:
  hotelchains_dict[i]=hotelchain_names[j]
  #hotelchains_dict[i[0]]=hotelchain_names[j]
  j+=1

cur.close()
conn.close()'''


@app.route('/hotelchains',methods=['POST','GET'])
def hotelchains():
  conn=psycopg2.connect(database='eHotels',user='postgres',password='postgres',
                        host='localhost',port='5433')
  
  cur=conn.cursor()
  cur.execute('SELECT * FROM hotelchain_officeaddress')
  hotelchains_db=cur.fetchall()
  cur.close()
  conn.close()
  return render_template('hotelchains.html',hotelchains_db=hotelchains_db,hotelchains_dict=hotelchains_dict)


@app.route('/hotels',methods=['POST','GET'])
def hotels():
  #verifie si on vient du NAV bar ou d'un hotel chain specifique
  chosen_hotelchain=request.args.get('hotelchain')
  if chosen_hotelchain=='nav':
    chosen_hotelchain_ID=request.args.get('cid')
  else:
    chosen_hotelchain_ID=int(request.args.get('cid'))
    
  conn=psycopg2.connect(database='eHotels',user='postgres',password='postgres',host='localhost',port='5433')
  cur=conn.cursor()
  
  if chosen_hotelchain=='nav':
    cur.execute(f'SELECT * FROM hotel ORDER BY rating DESC')
  else:
    cur.execute(f'SELECT * FROM hotel WHERE chainid={chosen_hotelchain_ID} ORDER BY rating DESC')
  all_hotels_db=cur.fetchall()
  
  cur.close()
  conn.close()
  context={
    'chosen_hotelchain_ID':chosen_hotelchain_ID,
    'chosen_hotelchain':chosen_hotelchain,
    'all_hotels_db':all_hotels_db, 
    'hotel_dict':hotel_dict,
    'hotelchains_dict':hotelchains_dict
  }   
  return render_template('hotels.html',**context)
  
@app.route('/roomInfo',methods=['POST','GET'])
def roominfo():
  #hotel id
  chosen_hotel_id=request.args.get('hid')
  
  #hotel name
  chosen_hotel=request.args['hotel']
  
  #WTFform for Room
  form=roomForm()
  

  # si la chambre est booked, met ca dans une liste de tuple (hotelID,RoomNumber)
  #fait in dict pour cela avec le choix comme key
  
  conn=psycopg2.connect(database='eHotels',user='postgres',password='postgres',host='localhost',port='5433')
  curr=conn.cursor()
  curr.execute(f"SELECT hotelID,phonenumber,street,city,Province,PostalCode FROM hotel NATURAL JOIN Hotel_PhoneNumber")
  hotel_desc=curr.fetchall()
    
  for i in hotel_desc:
    if chosen_hotel_id is None:
      pass
    else:
      if int(i[0])==int(chosen_hotel_id):
        hotel_desc=i[1:]
        break
        
    
  for i in hotel_dict:
    if int(chosen_hotel_id)==int(i[0]):
      chosen_chain_id=i[1]
    
  for key,i in hotelchains_dict.items():
    if int(key[0])==int(chosen_chain_id):
      chosen_chain=i

  cur.close()
  conn.close()
 
  if (request.method=='POST'):
    form=roomForm()
    view=request.form.getlist('view')
    conn=psycopg2.connect(database='eHotels',user='postgres',password='postgres',host='localhost',port='5433')
    curr=conn.cursor()
    extendable=request.form.get('Extra Bed')    
    if(extendable==None):
      extendable=False
    else:extendable=True
    if(form.view.data=='seaview'): view=True
    else: view=False
    
 
    curr.execute(f"SELECT * FROM room WHERE hotelid={chosen_hotel_id} AND capacity='{form.capacity.data}' AND extendable={extendable} AND seaview={view}")
    all_room_db=curr.fetchall()
    cur.close()
    conn.close()
    
    context={
      'chosen_hotel_id':chosen_hotel_id,
      'chosen_hotel':chosen_hotel,
      'chosen_chain':chosen_chain,
      'form':form,
      'hotel_desc':hotel_desc,
      'all_room_db':all_room_db
    }
    return redirect(url_for('pickroom',**context))
  else:
    context={
      'chosen_hotel_id':chosen_hotel_id,
      'chosen_hotel':chosen_hotel,
      'chosen_chain':chosen_chain,
      'form':form,
      'hotel_desc':hotel_desc,
    }
    return render_template('RoomInfo.html',**context)
  

#Ajoute un if get: retourne la page ci-dessous et si chosen_hotel est vide redirect a hotels, si post=cree un forms avec wtfforms
@app.route('/pickRoom',methods=['POST','GET'])
def pickroom():
  chosen_hotel_id=request.args.get('chosen_hotel_id')

  chosen_hotel=request.args['chosen_hotel']
  all_room_db=request.args.getlist('all_room_db')
  all_room_db_tuple=[]
  for s in all_room_db:
    # Use ast.literal_eval() to safely evaluate the string and convert it into a tuple
    tuple_val = ast.literal_eval(s)
    # Append the tuple to the tuple_list
    all_room_db_tuple.append(tuple_val)
  
  conn=psycopg2.connect(database='eHotels',user='postgres',password='postgres',
                        host='localhost',port='5433')
  
  cur=conn.cursor()
  cur.execute(f'SELECT * FROM room WHERE hotelid={chosen_hotel_id}')
  rooms=cur.fetchall()
  cur.execute(f'SELECT * FROM roomamenities WHERE hotelid={chosen_hotel_id}')
  amenities=cur.fetchall()
    
  cur.execute(f"SELECT hotelID,phonenumber,street,city,Province,PostalCode FROM hotel NATURAL JOIN Hotel_PhoneNumber")
  hotel_desc=cur.fetchall()
    
  for i in hotel_desc:
    if chosen_hotel_id is None:
      pass
    else:
      if int(i[0])==int(chosen_hotel_id):
        hotel_desc=i[1:]
        break
        
    
  for i in hotel_dict:
    if int(chosen_hotel_id)==int(i[0]):
      chosen_chain_id=i[1]
    
  for key,i in hotelchains_dict.items():
    if int(key[0])==int(chosen_chain_id):
      chosen_chain=i
  
  cur.close()
  conn.close()
  
  context={
    'chosen_hotel_id':chosen_hotel_id,
    'chosen_hotel':chosen_hotel,
    'rooms':rooms,
    'amenities':amenities,
    'chosen_chain':chosen_chain,
    'hotel_desc':hotel_desc,
    'all_room_db_tuple':all_room_db_tuple
  }
  return render_template('PickRoom.html',**context)



@app.route('/secondroomInfo',methods=['POST','GET'])
def secondroominfo():
  #chosen_hotel_id=request.args['chosen_hotel_id']
  chosen_hotel=request.args['chosen_hotel']
  room_number=request.args.get('room_number')
  hid=request.args['hid']
  room_info=request.args.getlist('room_info')
  update=request.args.get('update')
  #chosen_chain=request.args['chosen_chain']
  #hotel_desc=request.args['hotel_desc']
  ssn=None
  fname=None
  lname=None
  street=None
  city=None
  province=None
  postalcode=None
  phonenumber=None
  book=None
  from_date=None
  
  form=CustInfoForm()
  context={
    #'chosen_chain':chosen_chain,
    'form':form,
    'chosen_hotel':chosen_hotel,
    'room_number':room_number,
    'hid':hid
    #'hotel_desc':hotel_desc
  }
  unique_id = int(str(uuid.uuid4().int)[:5])
  bookid=int(unique_id)
  if request.method=='POST':
    #if form.validate_on_submit():
    ssn=form.ssn.data
    fname=form.fname.data
    lname=form.lname.data
    street=form.street.data
    city=form.city.data
    province=form.province.data
    postalcode=form.postalcode.data
    phonenumber=form.phonenumber.data
    cust_info=[str(ssn),fname,lname,street,city,province,postalcode,phonenumber]
    from_date = request.form['trip-start']
    to_date = request.form['trip-end']
    from_date = datetime.strptime(from_date, '%Y-%m-%d')
    to_date = datetime.strptime(to_date, '%Y-%m-%d')

    # Calculate the difference
    date_diff = to_date - from_date
    date_diff=date_diff.days
    try:
      conn=psycopg2.connect(database='eHotels',user='postgres',password='postgres',host='localhost',port='5433')
      cur=conn.cursor()
      
      #unique_id = int(str(uuid.uuid4().int)[:5])
      cust_info_str = str(cust_info).replace("'", "''")  # Escape single quotes in the string
       

      cur.execute(f"SELECT * FROM Customer NATURAL JOIN customer_phonenumber")
      cust_data = cur.fetchall()
      

      in_db = False
      for i in cust_data:
          if i[0] == int(ssn):
              print("DEJA DANS LA DB")
              in_db = True
              print("in_db inside loop:", in_db)  # Add this line to check in_db inside the loop
              break

      if(update is None):
        print("ON INSERT!!!!!!")
        if(in_db==False):
          cur.execute(f"INSERT INTO Customer(customerssn,firstname,lastname,street,city,province) VALUES({int(ssn)},'{fname}','{lname}','{street}','{city}','{province}')")
          cur.execute(f"INSERT INTO customer_phonenumber VALUES({int(ssn)},'{phonenumber}')")
        cur.execute("INSERT INTO book (booking_id, customerssn, hotelid, roomnumber, stayduration, bookingdate, roominfo, customerinfo) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (int(unique_id), int(ssn), int(hid), int(room_number), date_diff, from_date, str(room_info), cust_info_str))
        cur.execute("INSERT INTO Booking_Archives (booking_id, customerssn, hotelid, roomnumber, stayduration, bookingdate, roominfo, customerinfo) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (int(unique_id), int(ssn), int(hid), int(room_number), date_diff, from_date, str(room_info), cust_info_str))
        conn.commit()
        context={
            #'chosen_chain':chosen_chain,
            'form':form,
            'chosen_hotel':chosen_hotel,
            'room_number':room_number,
            'room_info':room_info,
            'from_date':from_date,
            'hid':hid,
            'fname':fname,
            'bookid':bookid
            #'hotel_desc':hotel_desc
          }
        return redirect(url_for('thankyou',**context))
      elif(update is not None):
        cur.execute(f"SELECT * FROM customer WHERE customerssn={int(ssn)}")
        is_cust_here=cur.fetchall()
        if(len(is_cust_here)==0):
          flash("WRONG SSN, ENTER YOUR OLD SSN")
          
          return redirect(url_for('secondroominfo',**context))
        else:
          ## delete le book avec le bookid et lecustssn et update les valeurs de customer avec ce ssn et juste cree un nouveau bookid
          
          cur.execute(f"UPDATE Customer SET firstname='{fname}', lastname='{lname}', street='{street}',city='{city}', province='{province}' WHERE customerssn={int(ssn)}")
          cur.execute(f"UPDATE customer_phonenumber SET phonenumber='{phonenumber}' WHERE customerssn={int(ssn)}")
          cur.execute(f"UPDATE Book SET customerinfo='{cust_info_str}' WHERE customerssn={int(ssn)}")
          conn.commit()        
          return redirect(url_for('thankyou',**context))

      cur.execute(f"SELECT * FROM Book WHERE booking_id={int(unique_id)}")
      data = cur.fetchall()
    except psycopg2.Error as e:
      print("Error: ",e)
    finally:
      cur.close() 
      conn.close()
      
    
  context={
      #'chosen_chain':chosen_chain,
      'form':form,
      'chosen_hotel':chosen_hotel,
      'room_number':room_number,
      'room_info':room_info,
      'from_date':from_date,
      'hid':hid,
      'fname':fname,
      'bookid':bookid
      #'hotel_desc':hotel_desc
    }
  return render_template('secondroomInfo.html',**context)

@app.route('/thankyou',methods=['POST','GET'])
def thankyou():
  hid=request.args.get('hid')
  fname=request.args.get('fname')
  bookid=request.args.get('bookid')
  chosen_hotel=request.args.get('chosen_hotel')
  room_info=request.args.get('room_info')
  room_number=request.args.get('room_number')
  update=None
  form=thankyouForm()
  
  if request.method=='POST':
    if form.updatecust.data:
      update=1
      context={
        'hid':hid,
        'fname':fname,
        'bookid':bookid,
        'chosen_hotel':chosen_hotel,
        'room_info':room_info,
        'room_number':room_number,
        'update':update  
      }
      
      return redirect(url_for('secondroominfo',**context))
    elif form.deletebook.data:
      update=None
      context={
        'hid':hid,
        'fname':fname,
        'bookid':bookid,
        'chosen_hotel':chosen_hotel,
        'room_info':room_info,
        'room_number':room_number,
        'update':update  
      }
      try:
        conn=psycopg2.connect(database='eHotels',user='postgres',password='postgres',
                        host='localhost',port='5433')
  
        cur=conn.cursor()
        cur.execute(f'DELETE FROM Book WHERE booking_id={int(bookid)}')
        conn.commit()
      except psycopg2.Error as e:
        print("Error: ",e)
      finally:
        cur.close() 
        conn.close()
      #redirect a la page d'accueil et flash un message de tristess
      flash("We're very sorry that you had to cancel the booking :(")
      return redirect(url_for("hotelchains"))
    return redirect(url_for('thankyou',**context))
  context={
    'form':form,
    'fname':fname,
    'chosen_hotel':chosen_hotel
  }
  return render_template('thankyou.html',**context)


@app.route('/',methods=['POST','GET'])
def home():
  form=loginForm()
  if(request.method=='POST'):
    if(form.cust.data):
      return redirect(url_for('hotelchains'))
    
    elif(form.empl.data):
      return redirect(url_for('emplogin'))
  context={
    'form':form
  }
  return render_template('base.html',**context)

####L'employee entre son information et doit login avec son ssn et hid
####chaque hotel a un manager et des sous employees
####le manager peut insert/update/delete des employees

####le manager peut insert/update/delete des chambres et des hotels
####Il va y avoir une route pour les hotels et une autre pour une liste des employees
####l'employee peut check in un cust dans le book (ce qui delete le booking)

@app.route('/emplogin',methods=['POST','GET'])
def emplogin():
  conn=psycopg2.connect(database='eHotels',user='postgres',password='postgres',
                        host='localhost',port='5433')
  
  cur=conn.cursor()
  form=empLoginForm()
  if request.method=='POST':
    empssn=None
    hid=None
    
    empssn=form.empssn.data
    hid=form.hid.data
    cur.execute(f'SELECT * FROM EMPLOYEE')
    
    flag=False
    for i in cur.fetchall():
      if((empssn,hid)==(i[0],i[1])):
        emp_cred=(i[0],i[1])
        empdesc=i
        context={
          'empdesc':empdesc
        }
        flag=True
        break
    
    if(flag==True): 
      if(empdesc[-1]=='Manager'):
        return redirect(url_for('managerchoices',**context))#return redirect(url_for('emprole',**context))#redirect
      elif(empdesc[-1]=='Front Desk'):
        return redirect(url_for('frontdesk',**context))
      elif(empdesc[-1]=='Housekeeping' or empdesc[-1]=='Maintenance'):
        return render_template('useless.html')
    else: flash("Wrong credentials, try again!") 
    
    #print(cur.fetchall())
  cur.close() 
  conn.close()

  context={
    'form':form
  }
  return render_template('emplogin.html',**context)

@app.route('/managerchoices',methods=['POST','GET'])
def managerchoices():
  empdesc=request.args.getlist('empdesc')
  form=managerChoices()
  context={
    'empdesc':empdesc,
    'form':form
  }
  if request.method=='POST':
    if form.employees.data:
      return redirect(url_for('emprole',empdesc=empdesc))
    elif form.rooms.data:
      return redirect(url_for('roomschoices',empdesc=empdesc))
    elif form.hotels.data:
      return redirect (url_for('hotelrole',empdesc=empdesc))
  return render_template("managerchoices.html",**context)


@app.route('/roomschoices',methods=['POST','GET'])
def roomschoices():
  empdesc=request.args.getlist('empdesc')
  form=roomChoices()
  context={
    'empdesc':empdesc,
    'form':form
  }
  if request.method=='POST':
    if form.del_upd.data:
      return redirect(url_for('roomsDeleteUpdate',**context))
    elif form.backbtn.data:
      return redirect(url_for('managerchoices',**context))
    elif form.insert.data:
      return redirect(url_for('roomInsert',**context))
  return render_template('roomschoices.html',**context)

@app.route('/roomInsert',methods=['POST','GET'])
def roomInsert():
  empdesc=request.args.getlist('empdesc')
  form=roomsUpdate()
  context={
    'form':form,
    'empdesc':empdesc
  }
  if request.method=='POST':
    if form.update.data:
      try:
        conn=psycopg2.connect(database='eHotels',user='postgres',password='postgres',
                        host='localhost',port='5433')
  
        cur=conn.cursor()
        if form.extendable.data=='Extendable':extendable=True
        else: extendable=False
        
        if form.seaview.data=='Seaview':view=True
        else:view=False
        
        cur.execute(f"INSERT INTO Room(roomnumber,hotelid, extendable, capacity, seaview, price) VALUES (%s, %s, %s, %s, %s, %s)",
            (int(form.roomnum.data),int(empdesc[1]), extendable, form.capacity.data, view, int(form.price.data)))


        if request.form.get('TV')==True:TV='TV'
        else: TV='No TV'
        
        if request.form.get('AC')==True:AC='AC'
        else: AC='No AC'
        
        if request.form.get('Fridge')==True:Fridge='Fridge'
        else: Fridge='No Fridge'
        
        if request.form.get('Balcony')==True:TV='Balcony'
        else: Balcony='No Balcony'

        cur.execute(f'INSERT INTO roomamenities(roomnumber,hotelid,amenities) VALUES (%s,%s,%s)',
                    (int(form.roomnum.data),int(empdesc[1]),TV))
        cur.execute(f'INSERT INTO roomamenities(roomnumber,hotelid,amenities) VALUES (%s,%s,%s)',
                    (int(form.roomnum.data),int(empdesc[1]),AC))
        cur.execute(f'INSERT INTO roomamenities(roomnumber,hotelid,amenities) VALUES (%s,%s,%s)',
                    (int(form.roomnum.data),int(empdesc[1]),Fridge))
        cur.execute(f'INSERT INTO roomamenities(roomnumber,hotelid,amenities) VALUES (%s,%s,%s)',
                    (int(form.roomnum.data),int(empdesc[1]),Balcony))
        conn.commit()

      except psycopg2.Error as e:
        print("Error: ",e)
      finally:
        cur.close() 
        conn.close()
      return redirect(url_for('roomschoices',**context))
  return render_template('roomInsert.html',**context)

@app.route('/roomsDeleteUpdate',methods=['POST','GET'])
def roomsDeleteUpdate():
  empdesc=request.args.getlist('empdesc')
  form=roomChoices()
  try:
    conn=psycopg2.connect(database='eHotels',user='postgres',password='postgres',
                        host='localhost',port='5433')
    
    cur=conn.cursor()
    cur.execute(f"SELECT * FROM room WHERE hotelid={int(empdesc[1])}")
    for key,i in hotel_dict.items():
      if(key[0]==int(empdesc[1])):
        hotel_name=i
        break
    all_rooms=cur.fetchall()
    if request.method=='POST':
      if form.remove.data:
        selected_room_nums=request.form.getlist('selectedRooms')
        for i in selected_room_nums:
          cur.execute(f'DELETE FROM Book WHERE roomnumber={int(i)} and hotelid={int(empdesc[1])} and customerssn={int(empdesc[0])}')
          cur.execute(f'DELETE FROM RoomAmenities WHERE roomnumber={int(i)} and hotelid={int(empdesc[1])}')
          cur.execute(f'DELETE FROM Room WHERE roomnumber={int(i)} and hotelid={int(empdesc[1])}')
          conn.commit()
        return redirect(url_for('roomsDeleteUpdate',empdesc=empdesc))
      
      elif form.change.data:
        selected_room_nums=request.form.getlist('selectedRooms')
        context={
          'selected_room_nums':selected_room_nums,
          'empdesc':empdesc
        }
        return redirect(url_for('roomsChange',**context))
      elif form.backbtn.data:
        return redirect(url_for('roomschoices',empdesc=empdesc))
  except psycopg2.Error as e:
      print("Error: ",e)
  finally:
    cur.close() 
    conn.close()
  context={
    'empdesc':empdesc,
    'all_rooms':all_rooms,
    'hotel_name':hotel_name,
    'form':form
  }
  return render_template('listed_rooms.html',**context)  

@app.route('/roomsChange',methods=['POST','GET'])
def roomsChange():
  form=roomsUpdate()
  empdesc=request.args.getlist('empdesc')
  selected_room_nums=request.args.getlist('selected_room_nums')
  try:
    conn=psycopg2.connect(database='eHotels',user='postgres',password='postgres',
                        host='localhost',port='5433')
    
    cur=conn.cursor()
    if request.method=='POST':
      if form.update.data:
        if form.extendable.data=='True':extendable=True
        else: extendable=False
        
        if form.seaview.data=='Seaview':seaview=True
        else: seaview=False
        
        if request.form.get('TV')==True:TV='TV'
        else:TV="No TV"
        if request.form.get('AC')==True:AC='AC'
        else:AC="No AC"
        if request.form.get('Fridge')==True:Fridge='Fridge'
        else:Fridge="No Fridge"
        if request.form.get('Balcony')==True:Balcony='Balcony'
        else:Balcony="No Balcony"
        for i in selected_room_nums:
          print(i)
          try:
            cur.execute("UPDATE Room SET extendable=%s, capacity=%s, seaview=%s, price=%s WHERE roomnumber=%s AND hotelid=%s", (extendable, form.capacity.data, seaview, form.price.data, int(i), int(empdesc[1])))
            #cur.execute("UPDATE Roomamenities SET amenities=%s WHERE roomnumber=%s AND hotelid=%s", (TV, int(i), int(empdesc[1])))
            #cur.execute("UPDATE Roomamenities SET amenities=%s WHERE roomnumber=%s AND hotelid=%s", (AC, int(i), int(empdesc[1])))
            #cur.execute("UPDATE Roomamenities SET amenities=%s WHERE roomnumber=%s AND hotelid=%s", (Fridge, int(i), int(empdesc[1])))
            #cur.execute("UPDATE Roomamenities SET amenities=%s WHERE roomnumber=%s AND hotelid=%s", (Balcony, int(i), int(empdesc[1])))
            cur.execute(f"DELETE FROM Book WHERE hotelid={int(empdesc[1])} and roomnumber={int(i)}")
          except :
            # Handle the duplicate key error, such as logging or skipping this update
            print("WTFFFFFF")
            conn.rollback()  # Rollback the transaction to avoid partial updates

        conn.commit()
        #return form.data
        return redirect(url_for('roomsDeleteUpdate',empdesc=empdesc,form=form))    
  except psycopg2.Error as e:
      print("Error: ",e)
  finally:
    cur.close() 
    conn.close()
  context={
    'form':form,
    'empdesc':empdesc,
    'selected_room_nums':selected_room_nums
  }
  return render_template('roomsChange.html',**context)


@app.route('/emprole',methods=['POST','GET'])
def emprole():
  
  empdesc=request.args.getlist('empdesc')
  form=emplRegisterForm()
  for key,i in hotel_dict.items():
    if(key[0]==int(empdesc[1])):
      hotel_name=i
      break
  try:
    conn=psycopg2.connect(database='eHotels',user='postgres',password='postgres',
                        host='localhost',port='5433')
    
    cur=conn.cursor()
    if(empdesc[-1]=='Manager'):
      cur.execute(f'SELECT * FROM employee WHERE hotelid={empdesc[1]}')
      emplist=cur.fetchall()

      context={
        'emplist':emplist,
        'hotel_name':hotel_name,
        'empdesc':empdesc,
        'form':form
      }
      if request.method=='POST':
        if form.remEmp.data:
          selected_employee_ids = request.form.getlist('selectedEmployees')
    
          for i in emplist:
            for j in selected_employee_ids:
              if(i[0]==int(j)):
                flash(f'Employee {i[2]} {i[3]} has been fired')
                cur.execute(f'DELETE FROM Employee_phonenumber WHERE employeessn={int(j)}')
                cur.execute(f'DELETE FROM Employee WHERE employeessn={int(j)}')
                conn.commit()

    
          return redirect(url_for('emprole',empdesc=empdesc))
        
        elif form.addEmp.data:
          empssn=form.empssn.data
          fname=form.fname.data
          lname=form.lname.data
          street=form.street.data
          city=form.city.data
          province=form.province.data
          postalcode=form.postalcode.data
          phonenumber=form.phonenumber.data
          position=form.position.data
          
          cur.execute(f'SELECT employeessn FROM employee WHERE employeessn={int(empssn)}')
          #print(cur.fetchall()," LOOOOOL",cur.fetchall())
          for i in cur.fetchall():
            if int(empssn)==int(i[0]):
              print(i,"   ",type(i))
              flash("SSN IS TAKEN")
              return redirect(url_for('emprole',empdesc=empdesc))
        
          cur.execute("INSERT INTO employee(employeessn, hotelid, firstname, lastname, street, city, province, postalcode, position) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (empssn, int(empdesc[1]), fname, lname, street, city, province, postalcode, position))

          cur.execute("INSERT INTO employee_phonenumber VALUES (%s, %s)",
            (empssn, phonenumber))

          conn.commit()
          return redirect(url_for('emprole',empdesc=empdesc))
        
        elif form.backbtn.data:
          return redirect(url_for('managerchoices',empdesc=empdesc))
      return render_template('manager.html',**context)
  except psycopg2.Error as e:
    print("Error: ",e)
  finally:
    cur.close() 
    conn.close()
  
  return "nothing"
 
  

@app.route('/frontdesk',methods=['POST','GET'])
def frontdesk():
  empdesc=request.args.getlist('empdesc')
  form=CheckIn()
  context={
    'empdesc':empdesc,
    'form':form
  }
  try:
    conn=psycopg2.connect(database='eHotels',user='postgres',password='postgres',
                        host='localhost',port='5433')
    
    cur=conn.cursor()
    cur.execute(f"SELECT * FROM BOOK WHERE hotelid={int(empdesc[1])}")
    all_bookings=cur.fetchall()
    for i in cur.fetchall():
      print(i)
    if request.method=='POST':
      if form.backbtn.data:
        context={
          'empdesc':empdesc,
          'all_bookings':all_bookings,
          'form':form
        }
        return redirect(url_for('emplogin',**context))
      elif form.checkin.data:
        
        selected_bookings_ids = request.form.getlist('selectedBookings')
        # Process the selected bookings and associated data

        for i in selected_bookings_ids:
          cur.execute(f"SELECT * FROM BOOK WHERE booking_id={int(i)}")
          books=cur.fetchall()
          if books:
            unique_chk_id = int(str(uuid.uuid4().int)[:5])
            cur.execute(
                "INSERT INTO Check_IN(check_in_id, hotelid, customerssn, employeessn, roomnumber, roominfo, customerinfo) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            , (unique_chk_id, int(books[0][2]), int(books[0][1]), int(empdesc[0]), int(books[0][3]), books[0][-2], books[0][-1]))
            for i in selected_bookings_ids:
              cur.execute(f"DELETE FROM BOOK WHERE booking_id={int(i)}")
            conn.commit()
        return redirect(url_for('frontdesk',**context))
  except psycopg2.Error as e:
      print("Error: ",e)
  finally:
    cur.close() 
    conn.close()
  for key,i in hotel_dict.items():
    if int(empdesc[1]) in key:
      hotel_name=i
  context={
    'empdesc':empdesc,
    'all_bookings':all_bookings,
    'hotel_name':hotel_name,
    'form':form
  }
  #et puis on appuie sur le checkbox ce qui insert dans le checkin
  return render_template('frontdesk.html',**context)

@app.route('/hotelrole',methods=['POST','GET'])
def hotelrole():
  empdesc=request.args.getlist('empdesc')
  
  form=hotelChoices()
  context={
    'empdesc':empdesc,
    'form':form
  }
  #juste change les redirects.....
  if request.method=='POST':
    if form.del_upd.data:
      return redirect(url_for('roomsDeleteUpdate',**context))
    elif form.backbtn.data:
      return redirect(url_for('managerchoices',**context))
    elif form.insert.data:
      return redirect(url_for('hotelInsert',**context))
  
  return render_template('hotelrole.html',**context)

@app.route('/hotelInsert',methods=['POST','GET'])
def hotelInsert():
  empdesc=request.args.getlist('empdesc')
  form1=addHotel()
  context={
    'form1':form1,
    'empdesc':empdesc
  }
  if request.method=='POST':
      try:
        conn=psycopg2.connect(database='eHotels',user='postgres',password='postgres',
                          host='localhost',port='5433')
    
        cur=conn.cursor()
        if form1.insert.data:
          
          cur.execute(f"SELECT hotelid FROM hotel")
          for i in cur.fetchall():
            if form1.hid.data==int(i[0]):
              flash(f"Hotel ID {int(i[0])} already exits!")
              return redirect(url_for('hotelInsert',**context))
          cur.execute("INSERT INTO hotel(hotelid, chainid, street, city, province, postalcode, email, rating) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                      ,(form1.hid.data, int(empdesc[1]), form1.street.data, form1.city.data, form1.province.data, form1.postalcode.data, form1.email.data, form1.rating.data))

          cur.execute("INSERT INTO hotel_phonenumber(hotelid, phonenumber) VALUES (%s, %s)"
                      ,(form1.hid.data, form1.phonenumber.data))

          conn.commit()
          hotel_names.append(form1.hname.data)
          
          cur.execute('SELECT * FROM hotel NATURAL JOIN hotel_phonenumber ORDER BY rating DESC;')
          all_hotel_IDs=cur.fetchall()



          #cur.execute('SELECT chainID FROM hotelchain_officeaddress')
          cur.execute('SELECT * FROM hotelchains NATURAL JOIN hotelchain_officeaddress NATURAL JOIN hotelchains_phonenumber')
          all_hotelchain_IDs=cur.fetchall()

          j=0
          for i in all_hotel_IDs:
            hotel_dict[i]=hotel_names[j]
            j+=1         
          
          flash(f"{form1.hname.data} is a new hotel!")
      except psycopg2.Error as e:
        print("Error: ",e)
      finally:
        cur.close() 
        conn.close()
      return redirect(url_for('hotelrole',**context))
  return render_template('hotelInsert.html',**context)


@app.route('/star',methods=['POST','GET'])
def star():
  return render_template('star.html')

if __name__=='__main__':
  tables()
  conn=psycopg2.connect(database='eHotels',user='postgres',
                      password='postgres',host='localhost',port='5433')
 
  cur=conn.cursor()

  cur.execute('SELECT * FROM hotel NATURAL JOIN hotel_phonenumber ORDER BY rating DESC;')
  all_hotel_IDs=cur.fetchall()



  #cur.execute('SELECT chainID FROM hotelchain_officeaddress')
  cur.execute('SELECT * FROM hotelchains NATURAL JOIN hotelchain_officeaddress NATURAL JOIN hotelchains_phonenumber')
  all_hotelchain_IDs=cur.fetchall()

  hotel_dict={}
  hotelchains_dict={}
  hotel_names=['Dolomiti', 'Tranquiluxe', 'Serenstay', 'Crestview', 'Grandeur', 'Radiance', 'Blissful', 'Solitude', 'Lumina', 'Celestial', 'Oasis', 'Elysium', 'Mirage', 'Summit', 'Enclave', 'Azure', 'HarmonyInn', 'EclipseLodge', 'MajesticView', 'WhisperingPines', 'GoldenSands', 'MoonlightManor', 'RoyalRetreat', 'SilverSprings', 'ParadisePalms', 'EmeraldHaven', 'CrystalWaters', 'StarlightSuites', 'SunriseVilla', 'TranquilityBay', 'RainbowResort', 'PeacefulHaven', 'OceanBreeze', 'MountainMajesty', 'GoldenGateHotel', 'SapphireShores', 'EvergreenLodge', 'WhimsicalWoods', 'BlueHorizonInn', 'SunsetSerenity', 'GardenGroveHotel', 'PinnaclePeaks', 'IslandOasis']

  #hotel_names=['Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti','Dolomiti']
  hotelchain_names=['LuxhotelsTranquilHaven','SerenitySapphireSands','HarmonyHavenSuites','CelestialLuxLodgings','BlissVilleResorts']


  j=0
  for i in all_hotel_IDs:
    hotel_dict[i]=hotel_names[j]
    j+=1

  j=0
  for i in all_hotelchain_IDs:
    hotelchains_dict[i]=hotelchain_names[j]
    #hotelchains_dict[i[0]]=hotelchain_names[j]
    j+=1

  cur.close()
  conn.close()
  app.run(host='0.0.0.0',port=7007,debug=True)
