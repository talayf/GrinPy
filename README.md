# GROMACS Web GUI
A lightweight Flask-based web interface that automates a full GROMACS molecular-dynamics workflow — from structure 
preparation to production runs.

## Features
• Upload .pdb, .gro, or .g96 structure files  
• Choose force field, water model, box type, and ion type  
• Automatically runs: pdb2gmx → editconf → solvate → grompp/genion → mdrun  
• Includes example .mdp parameter files  
• Inspired by Justin A. Lemkul’s GROMACS tutorials  

## Project Structure
gromacs_gui/
├── app.py
├── input_files/
│   ├── ions.mdp
│   ├── minim.mdp
│   ├── nvt.mdp
│   ├── npt.mdp
│   └── md.mdp
├── static/
│   └── protein.png
├── templates/
│   ├── home.html
│   ├── prep.html
│   └── analyze.html
├── requirements.txt
└── README.md

##️ Requirements
Python 3.8 +  
Flask  
GROMACS 2024 +  (must be installed and in $PATH)  

Install dependencies:
pip install -r requirements.txt  
Check GROMACS:
gmx --version  

## ️ Usage
python app.py  
Then open http://127.0.0.1:5000 in your browser.  
Upload a PDB, choose parameters, and wait for completion.  
Results appear in the same directory.

## Visualization
vmd md.tpr md.trr  
pymol md.gro  

## Credits
Based on Justin Lemkul’s GROMACS tutorials (https://www.mdtutorials.com/gmx/)  

## License
MIT License — free to use and modify with attribution.

