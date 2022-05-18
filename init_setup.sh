echo [$(date)]: "START"
echo [$(date)]: "creating environment"
conda create --prefix ./env python=3.7 -y   #creating the enviornment in the same project directory
echo [$(date)]: "activate environment"
source activate ./env                       #activating the environment
echo [$(date)]: "install requirements"
pip install -r requirements.txt             #installing the requirements