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
import seaborn as sns
import pandas as pd

def showPatients():
	toplevel=tk.Toplevel( bg="white", height=900, width=900, ) #opens a new window
	toplevel.title("Patient Data")
	
	#	Cat plot  patient blood group
	query1="select Blood_gp, count(Blood_gp) from Patient group by Blood_gp;" 
	table=sq.Query(query1)
	label=[]
	size=[]
	for i in table[1]:
		label.append(i[0])
		size.append(i[1])

	figure1, ax = plt.subplots(2,2, squeeze=False, gridspec_kw={'wspace':0.3, 'hspace':0.5})
	figure1.set_figheight(20)
	figure1.set_figwidth(20)
	canvas = FigureCanvasTkAgg(figure1, toplevel)
	canvas.get_tk_widget().pack()


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
		explode.append(i[1]*0.02)

	ax[1][0].pie(size, labels=label, shadow=True,  autopct='%1.1f%%', explode=explode)
	ax[1][0].set_title("Pie Chart: Patient Composition by Gender",fontdict={'fontsize':12})

def showDoctors():

	"""
	Grouping patients per doctor
	Distribution plot : doctors per department

	"""
	print("yay")
def showAdmin():
	print("Admin")


	"""
	Number of ongoing treatment per Department
	Resources stocks
	Dead patients per Disease
	Time series plot of patients getting admitted

	"""
	toplevel=tk.Toplevel( bg="white", height=900, width=900, )
	toplevel.title("Department Data")
	
	#	pie chart for the diff departments of the doctors
	query1="select type, count(type) from Doctors, Departments where Departments.Dept_ID=Doctors.Dept_ID group by type;" 
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
	ax1.set_title("Distribution of Doctors according to Departments")

def show3rdParty():

	"""
	Organ Donation according to type of organ
	Distribution Graph: No of new insurance and their amount
	
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
admin_button= tk.Button(stake_holder_frame, bg="white", fg="grey", text="   Admin    " , font=("Helvetica", 20, tk.font.BOLD), command=showAdmin)
admin_button.pack() 
thirdparty_button= tk.Button(stake_holder_frame, bg="white", fg="grey", text=" 3rd Party " , font=("Helvetica", 20, tk.font.BOLD), command=show3rdParty)
thirdparty_button.pack()
root.mainloop() # to run the app



"""
todo
auto-update in real time
"""