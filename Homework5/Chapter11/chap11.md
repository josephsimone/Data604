---
output:
  pdf_document: default
  html_document: default
---
# Modeling and Simulation in Python

Chapter 11

Copyright 2017 Allen Downey

License: [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0)

Lab Author @ Joseph Simone


```python
# Configure Jupyter so figures appear in the notebook
%matplotlib inline

# Configure Jupyter to display the assigned value after an assignment
%config InteractiveShell.ast_node_interactivity='last_expr_or_assign'

# import functions from the modsim.py module
from modsim import *
```

### SIR implementation

We'll use a `State` object to represent the number (or fraction) of people in each compartment.


```python
init = State(S=89, I=1, R=0)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>values</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>S</th>
      <td>89</td>
    </tr>
    <tr>
      <th>I</th>
      <td>1</td>
    </tr>
    <tr>
      <th>R</th>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>



To convert from number of people to fractions, we divide through by the total.


```python
init /= sum(init)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>values</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>S</th>
      <td>0.988889</td>
    </tr>
    <tr>
      <th>I</th>
      <td>0.011111</td>
    </tr>
    <tr>
      <th>R</th>
      <td>0.000000</td>
    </tr>
  </tbody>
</table>
</div>



`make_system` creates a `System` object with the given parameters.


```python
def make_system(beta, gamma):
    """Make a system object for the SIR model.
    
    beta: contact rate in days
    gamma: recovery rate in days
    
    returns: System object
    """
    init = State(S=89, I=1, R=0)
    init /= sum(init)

    t0 = 0
    t_end = 7 * 14

    return System(init=init, t0=t0, t_end=t_end,
                  beta=beta, gamma=gamma)
```

Here's an example with hypothetical values for `beta` and `gamma`.


```python
tc = 3      # time between contacts in days 
tr = 4      # recovery time in days

beta = 1 / tc      # contact rate in per day
gamma = 1 / tr     # recovery rate in per day

system = make_system(beta, gamma)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>values</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>init</th>
      <td>S    0.988889
I    0.011111
R    0.000000
dtyp...</td>
    </tr>
    <tr>
      <th>t0</th>
      <td>0</td>
    </tr>
    <tr>
      <th>t_end</th>
      <td>98</td>
    </tr>
    <tr>
      <th>beta</th>
      <td>0.333333</td>
    </tr>
    <tr>
      <th>gamma</th>
      <td>0.25</td>
    </tr>
  </tbody>
</table>
</div>



The update function takes the state during the current time step and returns the state during the next time step.


```python
def update_func(state, t, system):
    """Update the SIR model.
    
    state: State with variables S, I, R
    t: time step
    system: System with beta and gamma
    
    returns: State object
    """
    s, i, r = state

    infected = system.beta * i * s    
    recovered = system.gamma * i
    
    s -= infected
    i += infected - recovered
    r += recovered
    
    return State(S=s, I=i, R=r)
```

To run a single time step, we call it like this:


```python
state = update_func(init, 0, system)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>values</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>S</th>
      <td>0.985226</td>
    </tr>
    <tr>
      <th>I</th>
      <td>0.011996</td>
    </tr>
    <tr>
      <th>R</th>
      <td>0.002778</td>
    </tr>
  </tbody>
</table>
</div>



Now we can run a simulation by calling the update function for each time step.


```python
def run_simulation(system, update_func):
    """Runs a simulation of the system.
    
    system: System object
    update_func: function that updates state
    
    returns: State object for final state
    """
    state = system.init
    
    for t in linrange(system.t0, system.t_end):
        state = update_func(state, t, system)
        
    return state
```

The result is the state of the system at `t_end`


```python
run_simulation(system, update_func)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>values</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>S</th>
      <td>0.520568</td>
    </tr>
    <tr>
      <th>I</th>
      <td>0.000666</td>
    </tr>
    <tr>
      <th>R</th>
      <td>0.478766</td>
    </tr>
  </tbody>
</table>
</div>



**Exercise**  Suppose the time between contacts is 4 days and the recovery time is 5 days.  After 14 weeks, how many students, total, have been infected?

Hint: what is the change in `S` between the beginning and the end of the simulation?


```python
def make_system(beta, gamma):
    """Make a system object for the SIR model.
    
    beta: contact rate in days
    gamma: recovery rate in days
    
    returns: System object
    """
    init = State(S=89, I=1, R=0)
    init /= sum(init)

    t0 = 0
    t_end =14

    return System(init=init, t0=t0, t_end=t_end,
                  beta=beta, gamma=gamma)

tc = 4      # time between contacts in days 
tr = 5      # recovery time in days


beta = 1 / tc      # contact rate in per day
gamma = 1 / tr     # recovery rate in per day

system = make_system(beta, gamma)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>values</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>init</th>
      <td>S    0.988889
I    0.011111
R    0.000000
dtyp...</td>
    </tr>
    <tr>
      <th>t0</th>
      <td>0</td>
    </tr>
    <tr>
      <th>t_end</th>
      <td>14</td>
    </tr>
    <tr>
      <th>beta</th>
      <td>0.25</td>
    </tr>
    <tr>
      <th>gamma</th>
      <td>0.2</td>
    </tr>
  </tbody>
</table>
</div>




```python
run_simulation(system, update_func)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>values</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>S</th>
      <td>0.938488</td>
    </tr>
    <tr>
      <th>I</th>
      <td>0.019743</td>
    </tr>
    <tr>
      <th>R</th>
      <td>0.041770</td>
    </tr>
  </tbody>
</table>
</div>



### Using TimeSeries objects

If we want to store the state of the system at each time step, we can use one `TimeSeries` object for each state variable.


```python
def run_simulation(system, update_func):
    """Runs a simulation of the system.
    
    Add three Series objects to the System: S, I, R
    
    system: System object
    update_func: function that updates state
    """
    S = TimeSeries()
    I = TimeSeries()
    R = TimeSeries()

    state = system.init
    t0 = system.t0
    S[t0], I[t0], R[t0] = state
    
    for t in linrange(system.t0, system.t_end):
        state = update_func(state, t, system)
        S[t+1], I[t+1], R[t+1] = state
    
    return S, I, R
```

Here's how we call it.


```python
def make_system(beta, gamma):
    """Make a system object for the SIR model.
    
    beta: contact rate in days
    gamma: recovery rate in days
    
    returns: System object
    """
    init = State(S=89, I=1, R=0)
    init /= sum(init)

    t0 = 0
    t_end = 7 * 14

    return System(init=init, t0=t0, t_end=t_end,
                  beta=beta, gamma=gamma)


tc = 3      # time between contacts in days 
tr = 4      # recovery time in days

beta = 1 / tc      # contact rate in per day
gamma = 1 / tr     # recovery rate in per day

system = make_system(beta, gamma)
S, I, R = run_simulation(system, update_func)
```

And then we can plot the results.


```python
def plot_results(S, I, R):
    """Plot the results of a SIR model.
    
    S: TimeSeries
    I: TimeSeries
    R: TimeSeries
    """
    plot(S, '--', label='Susceptible')
    plot(I, '-', label='Infected')
    plot(R, ':', label='Recovered')
    decorate(xlabel='Time (days)',
             ylabel='Fraction of population')
```

Here's what they look like.


```python
plot_results(S, I, R)
savefig('figs/chap11-fig01.pdf')
```


![png](output_29_0.png)


### Using a DataFrame

Instead of making three `TimeSeries` objects, we can use one `DataFrame`.

We have to use `row` to selects rows, rather than columns.  But then Pandas does the right thing, matching up the state variables with the columns of the `DataFrame`.


```python
def run_simulation(system, update_func):
    """Runs a simulation of the system.
        
    system: System object
    update_func: function that updates state
    
    returns: TimeFrame
    """
    frame = TimeFrame(columns=system.init.index)
    frame.row[system.t0] = system.init
    
    for t in linrange(system.t0, system.t_end):
        frame.row[t+1] = update_func(frame.row[t], t, system)
    
    return frame
```

Here's how we run it, and what the result looks like.


```python
tc = 3      # time between contacts in days 
tr = 4      # recovery time in days

beta = 1 / tc      # contact rate in per day
gamma = 1 / tr     # recovery rate in per day

system = make_system(beta, gamma)
results = run_simulation(system, update_func)
results.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>S</th>
      <th>I</th>
      <th>R</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0.988889</td>
      <td>0.011111</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>1</th>
      <td>0.985226</td>
      <td>0.011996</td>
      <td>0.002778</td>
    </tr>
    <tr>
      <th>2</th>
      <td>0.981287</td>
      <td>0.012936</td>
      <td>0.005777</td>
    </tr>
    <tr>
      <th>3</th>
      <td>0.977055</td>
      <td>0.013934</td>
      <td>0.009011</td>
    </tr>
    <tr>
      <th>4</th>
      <td>0.972517</td>
      <td>0.014988</td>
      <td>0.012494</td>
    </tr>
  </tbody>
</table>
</div>



We can extract the results and plot them.


```python
plot_results(results.S, results.I, results.R)
```


![png](output_36_0.png)


## Exercises

**Exercise**  Suppose the time between contacts is 4 days and the recovery time is 5 days.  Simulate this scenario for 14 weeks and plot the results.


```python
# Solution

tc = 4      # time between contacts in days 
tr = 5      # recovery time in days

beta = 1 / tc      # contact rate in per day
gamma = 1 / tr     # recovery rate in per day

system = make_system(beta, gamma)
results = run_simulation(system, update_func)

plot_results(results.S, results.I, results.R)
```


![png](output_38_0.png)

