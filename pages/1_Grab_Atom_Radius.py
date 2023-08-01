import streamlit as st
import subprocess
import os
import time
import sys
import tempfile

sys.path.append(os.path.join(os.path.dirname(__file__), "GrabAtomRadius"))

from grab_atom_radius import grab_radius

st.markdown("## Grab Atom Radius")
st.divider()

# File uploader
pdb_file = st.file_uploader(
    "Upload",
    type="pdb",
    help="**Input:** Protein PDB \n\n**Output:** Atom Radius"
)

# Optional arguments
st.write("Optional")
radius = st.number_input("Radius (Angstrom)", min_value=0.0, value=10.0, step=0.1, help="Radius in Angstrom for atoms to extract (Default 10.0)")
coordinates_str = st.text_input("Coordinates (X,Y,Z)", "0,0,0", help="Input: Center for extracting atoms (Default '0,0,0')")

# Convert input strings to required types
if coordinates_str:
    coordinates = tuple(map(float, coordinates_str.split(',')))
else:
    coordinates = (0.0, 0.0, 0.0)

# Check if a PDB file is uploaded
if pdb_file is not None:
    # Show the "Run" button
    if st.button("Run", help="Grabbing Atom Radius"):
        with st.spinner("Running..."):
            time.sleep(2)
            # Save the PDB file to a temporary location
            temp_pdb_file_path = os.path.join(tempfile.gettempdir(), pdb_file.name)
            with open(temp_pdb_file_path, "wb") as f:
                f.write(pdb_file.getvalue())

            # Call the grab_radius function with the uploaded PDB file and optional arguments
            residues = grab_radius(temp_pdb_file_path, radius, coordinates)

            # Display the FASTA output in the Streamlit app
            st.divider()
            st.subheader("Output")
            st.code('\n'.join(residues))

            # Save the FASTA output to a temporary file
            temp_fasta_file_path = os.path.join(tempfile.gettempdir(), "output.fasta")
            with open(temp_fasta_file_path, "w") as f:
                f.write('\n'.join(residues))

            # Download the FASTA file using st.download
            st.divider()
            st.subheader("Download")
            st.download_button(label="Download Atom Radius FASTA", data='\n'.join(residues), file_name="output.fasta")

            # Remove the temporary PDB and FASTA files
            os.remove(temp_pdb_file_path)
            os.remove(temp_fasta_file_path)
