
  

# barneySA

A general-purpose library for sensitivity analysis using fractional factorial design and analysis of variance. The library conducts sensitivity analysis on a given model based on the ranges provided for the parameters. Basically, barneySA does the followings:

- Sample from the n-dimensional space of the parameters using fractional factorial design

- Create a parameter set for each of sample sets

- Run the given model for each parameter set and collect distance value

- Conduct the analysis of variance to determine the relative importance of parameters with respect to one another

  
## Getting started

### Quick start

`pip install --upgrade barneySA`

```py

# inside your script, e.g. test.py

from barneySA import tools
free_params = { # define the parameters and their range
    'P1' = [2,3],
    'P2' = [1.2,4.3]
}
settings = { # define settings
    "MPI_flag": True,
    "replica_n": 2,
    "output_path": "outputs/SA",
    "model":MODEL # this is your model  
}

obj = tools.SA(free_params = free_params,settings = settings)

obj.sample()

obj.run()

obj.postprocess()

```

```py

# in terminal

mpiexec -n 'cpu_numbers' python test.py

```

barneySA receives two inputs from users. First, the free parameters' list that is a python dictionary that contains the names and bounds (min and max) of each free parameter. Second, the settings that is another python dictionary that contains specifications of SA. Inside the specification, the model which is an object of the fomulated problem needs to be provided. The model object should have a function named 'run' that receives a parameter set (a sample of the given free parameters) and results in a distance value based on the goodness of fit considered for the problem in hand.


### Outputs

The library results in a value for each free parameters that shows the importance of that parameter with respect to the rest of the parameters.


## Authors

- Jalil Nourisa


### Acknowledgments

No one yet. Give some feedback so your name would appear here :-)
