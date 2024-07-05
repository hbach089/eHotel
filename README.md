# eHotel Project Documentation
## Overview
The eHotel project is a comprehensive hotel management system developed using the Flask framework. It supports managing multiple hotel chains, each consisting of several hotels, and provides features for handling rooms and employee assignments. The system ensures efficient hotel operations, from room reservations to employee management.

## Introduction
The eHotel project aims to streamline hotel management tasks by offering an intuitive web-based interface. Built with Python and Flask, it utilizes Jinja2 for templating and Bootstrap for responsive design, ensuring a seamless user experience across devices. The backend is powered by PostgreSQL, which efficiently handles data storage and retrieval for the numerous entities involved, such as hotel chains, hotels, employees, and rooms.
## Technologies Used
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;•	Flask  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;•	Jinja2  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;•	HTML/CSS  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;•	Bootstrap  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;•	PostgreSQL  

## Database Design
The database design is central to the eHotel project, ensuring that data is well-organized and easily accessible. The project uses PostgreSQL to manage a relational database that includes the following key entities:    

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;•	Hotel Chains: Each hotel chain has a unique identifier and name.    
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;•	Hotels: Each hotel belongs to a hotel chain and has attributes such as name, address, and contact information.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;•	Rooms: Each room is associated with a specific hotel and has attributes like room number, type, and status.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;•	Employees: Employees are linked to specific hotels and have details such as name, position, and contact information.  

## Setup and Installation
To set up the eHotel project, you will need to have Python and PostgreSQL installed on your machine. After cloning the repository, you can set up a virtual environment, install the necessary dependencies from the requirements.txt file, and configure the PostgreSQL database. Detailed setup instructions and database configuration scripts are provided in the project repository.

## ER Diagram
![image](https://github.com/hbach089/eHotel/assets/146272622/68e2ea87-40c5-42c9-a512-6bdb557e1495)

## Screenshots
## The customer view: 
### Home page:  
![image](https://github.com/hbach089/eHotel/assets/146272622/cd2cca29-488c-4241-aa00-5342f6e6b863)  

### Choosing a hotelchain:
![image](https://github.com/hbach089/eHotel/assets/146272622/2f823fed-955a-4869-af23-ae3dc34feedc)  

### Choosing a hotel:    
![image](https://github.com/hbach089/eHotel/assets/146272622/009c01f3-4daf-43d6-a5fa-a9e31d850524)  

### Picking room amenities:  
![image](https://github.com/hbach089/eHotel/assets/146272622/07cfc5b9-3493-4429-b0a8-138acf4604ae)  

### Rooms matching the chosen amenities in database: 
![image](https://github.com/hbach089/eHotel/assets/146272622/c36b0dfa-d068-4038-90b4-c57aca4510dc)  

### Customer books a room
![image](https://github.com/hbach089/eHotel/assets/146272622/941900ea-bab2-4479-ba74-ec48379017a8)  

## The employee view:   
### Edit choices available to employee
![image](https://github.com/hbach089/eHotel/assets/146272622/0f48b254-2295-4db3-839d-5b8f007e99b5)  

## Next steps
&nbsp;&nbsp;&nbsp;&nbsp;•	Create a Docker container for the Flask application to ensure consistent performance across environments.  
&nbsp;&nbsp;&nbsp;&nbsp;•	Set up a Docker container for the PostgreSQL database for easier management and deployment.   
&nbsp;&nbsp;&nbsp;&nbsp;•	Configure Docker to link the Flask application container with the PostgreSQL database container.  
&nbsp;&nbsp;&nbsp;&nbsp;•	Deploy the Dockerized application.  

