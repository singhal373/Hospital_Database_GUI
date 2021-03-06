import seaborn as sns 
import tkinter as tk
from tkinter import filedialog, Text, font
import os
from PIL import ImageTk, Image
import sql_connector as sq
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd

def showPatients():
	toplevel=tk.Toplevel( bg="white", height=900, width=900, ) #opens a new window
	toplevel.title("Patient Data")


	figure1, ax = plt.subplots(2,2, squeeze=False, gridspec_kw={'wspace':0.3, 'hspace':0.5})
	figure1.set_figheight(20)
	figure1.set_figwidth(20)
	canvas = FigureCanvasTkAgg(figure1, toplevel)
	canvas.get_tk_widget().pack()

	
	#	Cat plot  patient blood group
	query1="select Blood_gp, count(Blood_gp) from Patient group by Blood_gp;" 
	table=sq.Query(query1)
	label=[]
	size=[]
	for i in table[1]:
		label.append(i[0])
		size.append(i[1])

	data={}
	data["Blood Groups"]=label
	data["Number of Patients"]=size
	df=pd.DataFrame(data, columns=["Blood Groups", "Number of Patients"])
	plot=sns.stripplot(x="Blood Groups", y="Number of Patients",data=df, ax=ax[0][0] )
	ax[0][0].set_title("Distribution of patients according to Blood Groups",fontdict={'fontsize':12})

	# Lollipop graph of patients with different diseases
	sq.doQuery("create table t select Disease_ID from Treatment inner join Patient on Patient.Treatment_ID= Treatment.Treatment_ID;")
	table=sq.Query("select Name, count(*) from t inner join Disease on t.Disease_ID=Disease.Disease_ID group by Name;")
	sq.doQuery("Drop table t;")
	label=[]
	size=[]
	for i in table[1]:
		label.append(i[0])
		size.append(i[1])

	ax[0][1].vlines(x=label, ymin=0, ymax=size, color='firebrick', alpha=0.7, linewidth=2)
	ax[0][1].scatter(x=label, y=size, color='firebrick', alpha=0.7)
	ax[0][1].set_title('Lollipop Chart for Disease wise Patient Distribution', fontdict={'fontsize':12})
	ax[0][1].set_ylabel('Number of Patients')
	ax[0][1].set_xticks(label)
	ax[0][1].set_xticklabels(label, rotation=60, fontdict={'horizontalalignment': 'right', 'fontsize':9})


	#Counts plot for patient age and disease type
	table=sq.Query("select Name as Disease, Age from Patient as pp, Treatment as t, Disease as d, Person as p where p.U_ID=pp.U_ID and pp.Treatment_ID=t.Treatment_ID and t.Disease_ID=d.Disease_ID;")
	label=[]
	size=[]
	for i in table[1]:
		label.append(i[0])
		size.append(i[1])
	data={}
	data[table[0][0]]=label
	data[table[0][1]]=size
	df=pd.DataFrame(data, columns=table[0])
	
	plot=sns.stripplot(y="Age", x="Disease", data=df, ax=ax[1][1])
	sns.set(style="ticks", color_codes=True)
	plot.set_xticklabels(plot.get_xticklabels(), rotation=60, fontdict={'horizontalalignment': 'right', 'fontsize':9})
	ax[1][1].set_title("Counts Plot - Patient's Age and Disease",fontdict={'fontsize':12})

	#Pie Chart for Gender wise Patient Distribution
	table=sq.Query("select Gender, count(Gender) from Person inner join Patient on Patient.U_ID = Person.U_ID group by Gender;")
	label=[]
	size=[]
	explode=[]
	for i in table[1]:
		label.append(i[0])
		size.append(i[1])
		explode.append(i[1]*0.001)

	ax[1][0].pie(size, labels=label, shadow=True,  autopct='%1.1f%%', explode=explode)
	ax[1][0].set_title("Pie Chart: Patient Composition by Gender",fontdict={'fontsize':12})

	
def showDoctors():

	print("showDoctors")
	toplevel=tk.Toplevel( bg="white", height=900, width=900, ) #opens a new window
	toplevel.title("Grouping Patients Data")

	# Distribution of Patients among Doctors
	query1="select A.Doctor_ID, COUNT(B.Patient_ID) from Treatment as A, Patient as B where A.Treatment_ID = B.Treatment_ID group by A.Doctor_ID;" 
	table=sq.Query(query1)
	# print(table)
	label=[]
	size=[]
	for i in table[1]:
		label.append(i[0])
		size.append(i[1])

	figure1 = plt.Figure(figsize=(8,5), dpi=100)
	ax1 = figure1.add_subplot(211)
	canvas = FigureCanvasTkAgg(figure1, toplevel)
	canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
	ax1.plot(label,size, 'r')
	ax1.set_title("Distribution of Patients among Doctors")
	ax1.set_xticklabels(label, rotation=30, fontdict={'horizontalalignment': 'right'})

	# Distribution of Doctors according to Departments
	query1="select A.type, COUNT(B.Doctor_ID) from Departments as A, Doctors as B where A.Dept_ID = B.Dept_ID group by A.type;" 
	table=sq.Query(query1)
	# print(table)
	label=[]
	size=[]
	explode=[]
	for i in table[1]:
		label.append(i[0])
		size.append(i[1])
		explode.append(i[1]*0.02)

	figure1 = plt.Figure(figsize=(8,8), dpi=100)
	ax1 = figure1.add_subplot(212)
	canvas = FigureCanvasTkAgg(figure1, toplevel)
	canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
	ax1.pie(size, labels=label, shadow=True,  autopct='%1.1f%%', explode=explode)
	ax1.set_title("Distribution of Doctors according to Departments")

	"""
	Grouping patients per doctor
	Distribution plot : doctors per department

	"""
	print("yay")
def showAdmin():
	print("Admin")


	"""
	1. Number of ongoing treatment per Department
	2. Dead patients per Disease
	3. NO of doctors avl in diff departments
	4. stock of resources available
	# Time series plot of patients getting admitted

	"""
	#1.	Cat plot  for Busiest Department (ongoing treatments per departments)
	toplevel=tk.Toplevel( bg="white", height=900, width=900, )
	toplevel.title("Department Data")
	
	q1="drop table if exists temp, d_count;"
	q2="create table temp select Doctor_ID from Treatment where End_time is NULL;"
	q3="create table d_count select Dept_ID,count(Dept_ID) as dept_count from temp inner join Doctors on Doctors.Doctor_ID =temp.Doctor_ID group by Dept_ID;"
	q4="select type as Department_Name, dept_count from d_count as c, Departments as d where d.Dept_ID = c.Dept_ID order by dept_count desc;"
	sq.doQuery(q1)
	sq.doQuery(q2)
	sq.doQuery(q3)
	table=sq.Query(q4)
	sq.doQuery(q1)
	print(table)
	label=[]
	size=[]
	for i in table[1]:
		label.append(i[0])
		size.append(i[1])
	print(label)
	print(size)
	figure1, ax = plt.subplots(2,2, squeeze=False, gridspec_kw={'wspace':0.4, 'hspace':0.8})
	figure1.set_figheight(20)
	figure1.set_figwidth(20)
	canvas = FigureCanvasTkAgg(figure1, toplevel)
	canvas.get_tk_widget().pack()


	data={}
	data["Department"]=label
	data["Number of Patients"]=size
	df=pd.DataFrame(data, columns=["Department", "Number of Patients"])
	plot=sns.stripplot(x="Department", y="Number of Patients",data=df, ax=ax[0][0] )
	
	ax[0][0].set_title("Department wise Number of Active patient Distribution ",fontdict={'fontsize':12})
	ax[0][0].set_xticklabels(label, rotation=30, fontdict={'horizontalalignment': 'right'})

	#2. Dead patients per Disease
	query1="create table t select Disease_ID from Treatment inner join Patient on Patient.Treatment_ID= Treatment.Treatment_ID;"
	query2="select Name, count(*) from t inner join Disease on t.Disease_ID=Disease.Disease_ID group by Name;"
	query3="Drop table IF EXISTS t;" 
	table3=sq.doQuery(query3)
	table1=sq.doQuery(query1)
	table2=sq.Query(query2)
	table3=sq.doQuery(query3)
	# print(table1)
	# print(table2)
	# print(table3)
	label=[]
	size=[]
	for i in table2[1]:
		label.append(i[0])
		size.append(i[1])
	ax[0][1].vlines(x=label, ymin=0, ymax=size, color='firebrick', alpha=0.7, linewidth=2)
	ax[0][1].scatter(x=label, y=size, color='firebrick', alpha=0.7)
	ax[0][1].set_title('Lollipop Chart for Disease wise Dead Patient Distribution', fontdict={'fontsize':12})
	ax[0][1].set_ylabel('Number of dead Patients')
	ax[0][1].set_xticks(label)
	ax[0][1].set_xticklabels(label, rotation=45, fontdict={'horizontalalignment': 'right'})


	#	3. pie chart for no of doc avl in diff departments
	query1="select type, count(type) from Doctors, Departments where Departments.Dept_ID=Doctors.Dept_ID group by type;" 
	table=sq.Query(query1)
	label=[]
	size=[]
	explode=[]
	print(table)
	print(table[1])

	for i in table[1]:
		label.append(i[0])
		size.append(i[1])
		explode.append(i[1]*0.02)
	print(explode)
	ax[1][0].pie(size, labels=label, shadow=True,  autopct='%1.1f%%', explode=explode)
	ax[1][0].set_title("Department wise percentage of available doctors ")

	#4. bar graph of stock of supplies available
	query1="select Name, Quantity_available from Stock_of_supplies;" 
	table=sq.Query(query1)
	label=[]
	size=[]
	for i in table[1]:
		label.append(i[0])
		size.append((float)(i[1]))

	ax[1][1].bar(label,size, label=label, color=('#6600ff','#00ff00','#ff3300','#33FFFF'))
	ax[1][1].set_title("Stock of Supplies available")
	ax[1][1].set_xticklabels(label, rotation=25, fontdict={'horizontalalignment': 'right'})
	ax[1][1].set_ylabel('Available quantity')
	
def show3rdParty():
	
	print("3rdParty")
	toplevel=tk.Toplevel( bg="white", height=900, width=900, ) #opens a new window
	toplevel.title("Organ Donation Data")

	# Organ Donation
	query1="select Organ , count(Organ ) from Organ_Donations group by Organ ;" 
	table=sq.Query(query1)
	label=[]
	size=[]
	explode=[]
	for i in table[1]:
		label.append(i[0])
		size.append(i[1])
		explode.append(i[1]*0.02)

	figure1 = plt.Figure(figsize=(6,5), dpi=100)
	ax1 = figure1.add_subplot(111)
	canvas = FigureCanvasTkAgg(figure1, toplevel)
	canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
	ax1.pie(size, labels=label, shadow=True,  autopct='%1.1f%%', explode=explode)
	ax1.set_title("Number of Organs Donated by Type")



	# toplevel=tk.Toplevel( bg="white", height=900, width=900, ) #opens a new window
	# toplevel.title("Insurance Distribution Data")

	#	Insurance
	query1="select EXTRACT(YEAR FROM Date_of_expiry),AVG(Amount) from insurance_record group by EXTRACT(YEAR FROM Date_of_expiry);" 
	table=sq.Query(query1)
	label=[]
	size=[]
	for i in table[1]:
		label.append(i[0])
		size.append((float)(i[1]))

	figure1 = plt.Figure(figsize=(16,5), dpi=100)
	# ax1 = figure1.add_subplot(111)
	ax1 = figure1.add_axes([0.2,0.2,0.7,0.7])
	canvas = FigureCanvasTkAgg(figure1, toplevel)
	canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
	ax1.bar(label,size, label=label, color=('#6600ff','#00ff00','#ff3300','#33FFFF'))
	ax1.set_title("Cost Distribution Over the Years")
	
	"""
	Organ Donation according to type of organ
	Distribution Graph: Average Cost Year Wise Distribution during Expiry

	"""
	print("yay")

root = tk.Tk()
root.title("MediQL Data Analytics")
root.resizable(width=True, height=True)


canvas = tk.Canvas(root, height=900, width = 900, bg="white")
canvas.pack()

img=ImageTk.PhotoImage(Image.open("./talend.png").resize((900, 900), Image.ANTIALIAS))

canvas.create_image(450, 400, image=img, anchor=tk.CENTER)

stake_holder_frame=tk.Frame(root)
stake_holder_frame.pack()
stake_holder_frame.place(relx=0.75, rely=0.37)


patient_button= tk.Button(stake_holder_frame, bg="white", fg="grey", text="  Patients  " , font=("Helvetica", 20, tk.font.BOLD), command=showPatients)
patient_button.pack()
doctor_button= tk.Button(stake_holder_frame, bg="white", fg="grey", text="  Doctors  " , font=("Helvetica", 20, tk.font.BOLD), command=showDoctors)
doctor_button.pack()
admin_button= tk.Button(stake_holder_frame, bg="white", fg="grey", text="   Admin   " , font=("Helvetica", 20, tk.font.BOLD), command=showAdmin)
admin_button.pack() 
thirdparty_button= tk.Button(stake_holder_frame, bg="white", fg="grey", text=" 3rd Party " , font=("Helvetica", 20, tk.font.BOLD), command=show3rdParty)
thirdparty_button.pack()
root.mainloop() # to run the app



"""
todo
auto-update in real time
"""
