#import all the required packages
from flask import Flask, flash, render_template, url_for, request, redirect 
import os
import subprocess
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/' #used in case the application is hosted online

#Route to home page
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

#Route to input prepation page
@app.route("/prep")
def prep ():
	#rc = subprocess.Popen(['. /usr/local/gromacs/bin/GMXRC.bash'], shell=True)
	return render_template('prep.html')

#These functions will run when POST method is used (after submitting)
@app.route('/prep', methods = ["POST"])
def main():
	uploaded_file = request.files['pdbfile'] #get uploaded file from html form, accepted file forms are: pdb, gro, gro96
	#check if file is selected
	if uploaded_file.filename != '':
		filename = secure_filename(uploaded_file.filename) #check if input is safe
		uploaded_file.save(filename) #access the file by saving it to the same folder as the app
		################# PDB2GMX #################
		chosenforcefield = str(request.form.get('forcefield')) #get chosen forcefield
		chosenwatermodel = str(request.form.get('water')) #get chosen water model
		#create a command with the chosen arguments
		pdb2gmx = 'gmx pdb2gmx -f ' +  uploaded_file.filename + ' -o conf.gro -p topol.top -i posre.itp -ff ' + chosenforcefield + ' -water ' + chosenwatermodel
		stream1 = os.popen(pdb2gmx) #run it 
		status = os.wait() #wait for the operation to finish before starting the next one
		################# EDITCONF #################
		chosenboxtype = str(request.form.get('boxtype')) #get chosen box type
		chosendistance = str(request.form.get('dist')) #get input distance
		#create a command with the chosen arguments
		editconf = 'gmx editconf -f conf.gro -o newbox.gro -c -d ' + chosendistance + ' -bt ' + chosenboxtype
		stream2 = os.popen(editconf) #run it 
		status = os.wait() #wait for the operation to finish before starting the next one
		################# SOLVATE #################
		solvate = 'gmx solvate -cp newbox.gro -cs spc216.gro -o solv.gro -p topol.top' #create command
		stream3 = os.popen(solvate) #run it
		status = os.wait() #wait for the operation to finish before starting the next one
		################# ADD IONS #################
		grompp1 = 'gmx grompp -f input_files/ions.mdp -c solv.gro -p topol.top -o ions.tpr -po mdout.mdp' #create grompp command >> .tpr
		stream4 = os.popen(grompp1) #run it
		status = os.wait() #wait for the operation to finish before starting the next one
		chosenions = str(request.form.get('ions')) #get chosen types of ions
		#create GENION command based on chosen ions
		if chosenions == 'nacl':
			genion = 'echo SOL | gmx genion -s ions.tpr -o solv_ions.gro -p topol.top -pname NA -nname CL -neutral' #choses SOL automatically
			stream4 = os.popen(genion) #run it
			os.wait() #wait for the operation to finish before starting the next one
		else: 
			genion = 'echo SOL | gmx genion -s ions.tpr -o solv_ions.gro -p topol.top -pname K -nname CL -neutral' #choses SOL automatically
			stream4 = os.popen(genion) #run it
			os.wait() #wait for the operation to finish before starting the next one
		################# ENERGY MINIMIZATION #################
		grompp2 = 'gmx grompp -f input_files/minim.mdp -c solv_ions.gro -p topol.top -o em.tpr' #create command
		stream5 = os.popen(grompp2) #run it
		status = os.wait() #wait for the operation to finish before starting the next one
		mdrun1 = 'gmx mdrun -v -deffnm em' #create command
		stream6 = os.popen(mdrun1) #run it
		status = os.wait() #wait for the operation to finish before starting the next one
		################# EQUILIBRATION PHASE 1 #################
		grompp3 = 'gmx grompp -f input_files/nvt.mdp -c em.gro -r em.gro -p topol.top -o nvt.tpr' #create command
		stream7 = os.popen(grompp3) #run it
		status = os.wait() #wait for the operation to finish before starting the next one
		mdrun2 = 'gmx mdrun -deffnm nvt' #create command
		stream8 = os.popen(mdrun2) #run it
		status = os.wait() #wait for the operation to finish before starting the next one
		################# EQUILIBRATION PHASE 2 #################
		grompp4 = 'gmx grompp -f input_files/npt.mdp -c nvt.gro -r nvt.gro -t nvt.cpt -p topol.top -o npt.tpr' #create command
		stream9 = os.popen(grompp4) #run it
		status = os.wait() #wait for the operation to finish before starting the next one
		mdrun3 = 'gmx mdrun -deffnm npt' #create command
		stream10 = os.popen(mdrun3) #run it
		status = os.wait() #wait for the operation to finish before starting the next one
		################# Produce .tpr file #################
		grompp5 = 'gmx grompp -f input_files/md.mdp -c npt.gro -t npt.cpt -p topol.top -o md.tpr' #create command
		stream11 = os.popen(grompp5) #run it
		status = os.wait() #wait for the operation to finish before starting the next one
		################# RUN SIMULATION #################
		mdrun = 'gmx mdrun -deffnm md' #create command
		stream12 = os.popen(mdrun) #run it
		status = os.wait() #wait for the operation to finish
	return redirect(url_for('prep')) #resets prep page 
#Run the previous function
def runmain(): 
	return main()

#Route to trajectory analysis page
@app.route("/analyze")
def analyze():
	return render_template('analyze.html')

if __name__ == '__main__':
	app.run(debug=True) #allow debugging 
