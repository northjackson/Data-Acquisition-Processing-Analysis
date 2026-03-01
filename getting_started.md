# Introduction to Seasonal Snow Observations, Models, and Analysis

# Getting Started: 
Please fork this repo to your GitHub account.
Next, identify a folder location where you would like to work in a development environment.
Using the command prompt, change your working directory to this folder and git clone https://github.com/USERID/Data-Acquisition-Processing-Analysis

    git clone https://github.com/USERID/Data-Acquisition-Processing-Analysis


## Virtual Environment
It is a best practice to create a virtual environment when starting a new project, as a virtual environment essentially creates an isolated working copy of Python for a particular project. 
I.e., each environment can have its own dependencies or even its own Python versions.
Creating a Python virtual environment is useful if you need different versions of Python or packages for different projects.
Lastly, a virtual environment keeps things tidy, makes sure your main Python installation stays healthy and supports reproducible and open science.

### Creating your HyRiver Virtual Environment on UU HPC
Since we will be using Jupyter Notebooks for this exercise, we will use the Anaconda command prompt to create our virtual environment. 
We suggest using Mamba rather than conda for installs, conda may be used but will take longer. First, we need to initiate mamba. This is similar to miniconda3 but it is caled miniforge3. A good habit is to know how to find modules:

    module avail miniforge

This should return two versions of miniforge3:   miniforge3/24.9.0    miniforge3/25.11.0. Lets go ahead and load the latest version:

    ml miniforge3/25.11.0

Now that we have mamba loaded, we can make our environment.In the command line type: 


    mamba env create -f hyriver.yml 

    conda activate hyriver

    python -m ipykernel install --user --name=hyriver

Sign all notbooks to **Trust**

    jupyter trust *.ipynb

