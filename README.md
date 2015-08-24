# music-generator

## Installation
This assumes you are using anaconda and *currently in the root directory* of this repository.

1. Create the environment (anaconda's version of virtualenv) using `conda env create`.

2. Activate the environment with `activate musicgen`. This makes the terminal start using the environment's packages when you type a command.

3. Install Theano and Lasagne. Since both are in active development and Lasagne only very recently got its first release, they will be installed in "development mode". 
  1. Theano and Lasagne are included as Git submodules. Essentially, a pointer to a particular commit in Theano's and Lasagne's repositories is stored and used to checkout a copy of their code.

     First run `git submodule init` to update the submodule list. You only need to do this once.

     Then run `git submodule update` to checkout the version of Theano and Lasagne currently being used in this project. If we ever change versions of Theano and Lasagne, just run this command to update to the right version.
  2. Finally, run `conda develop vendor/theano` and `conda develop vendor/lasagne` to install the packages in this environment.

4. You can test that the installation is working by running the vendor/lasagne/examples/mnist.py script.
