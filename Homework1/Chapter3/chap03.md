---
output:
  pdf_document: default
  html_document: default
---
# Modeling and Simulation in Python

Chapter 3

Copyright 2017 Allen Downey

License: [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0)

Lab Author: Joseph Simone


```python
# Configure Jupyter so figures appear in the notebook
%matplotlib inline

# Configure Jupyter to display the assigned value after an assignment
%config InteractiveShell.ast_node_interactivity='last_expr_or_assign'

# import functions from the modsim library
from modsim import *

# set the random number generator
np.random.seed(7)
```

## More than one State object

Here's the code from the previous chapter, with two changes:

1. I've added DocStrings that explain what each function does, and what parameters it takes.

2. I've added a parameter named `state` to the functions so they work with whatever `State` object we give them, instead of always using `bikeshare`.  That makes it possible to work with more than one `State` object.


```python
def step(state, p1, p2):
    """Simulate one minute of time.
    
    state: bikeshare State object
    p1: probability of an Olin->Wellesley customer arrival
    p2: probability of a Wellesley->Olin customer arrival
    """
    if flip(p1):
        bike_to_wellesley(state)
    
    if flip(p2):
        bike_to_olin(state)
        
def bike_to_wellesley(state):
    """Move one bike from Olin to Wellesley.
    
    state: bikeshare State object
    """
    state.olin -= 1
    state.wellesley += 1
    
def bike_to_olin(state):
    """Move one bike from Wellesley to Olin.
    
    state: bikeshare State object
    """
    state.wellesley -= 1
    state.olin += 1
    
def decorate_bikeshare():
    """Add a title and label the axes."""
    decorate(title='Olin-Wellesley Bikeshare',
             xlabel='Time step (min)', 
             ylabel='Number of bikes')
```

And here's `run_simulation`, which is a solution to the exercise at the end of the previous notebook.


```python
def run_simulation(state, p1, p2, num_steps):
    """Simulate the given number of time steps.
    
    state: State object
    p1: probability of an Olin->Wellesley customer arrival
    p2: probability of a Wellesley->Olin customer arrival
    num_steps: number of time steps
    """
    results = TimeSeries()    
    for i in range(num_steps):
        step(state, p1, p2)
        results[i] = state.olin
        
    plot(results, label='Olin')
```

Now we can create more than one `State` object:


```python
bikeshare1 = State(olin=10, wellesley=2)
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
      <th>olin</th>
      <td>10</td>
    </tr>
    <tr>
      <th>wellesley</th>
      <td>2</td>
    </tr>
  </tbody>
</table>
</div>




```python
bikeshare2 = State(olin=2, wellesley=10)
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
      <th>olin</th>
      <td>2</td>
    </tr>
    <tr>
      <th>wellesley</th>
      <td>10</td>
    </tr>
  </tbody>
</table>
</div>



Whenever we call a function, we indicate which `State` object to work with:


```python
bike_to_olin(bikeshare1)
```


```python
bike_to_wellesley(bikeshare2)
```

And you can confirm that the different objects are getting updated independently:


```python
bikeshare1
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
      <th>olin</th>
      <td>11</td>
    </tr>
    <tr>
      <th>wellesley</th>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>




```python
bikeshare2
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
      <th>olin</th>
      <td>1</td>
    </tr>
    <tr>
      <th>wellesley</th>
      <td>11</td>
    </tr>
  </tbody>
</table>
</div>



## Negative bikes

In the code we have so far, the number of bikes at one of the locations can go negative, and the number of bikes at the other location can exceed the actual number of bikes in the system.

If you run this simulation a few times, it happens often.


```python
bikeshare = State(olin=10, wellesley=2)
run_simulation(bikeshare, 0.4, 0.2, 60)
decorate_bikeshare()
```


![png](output_17_0.png)


We can fix this problem using the `return` statement to exit the function early if an update would cause negative bikes.


```python
def bike_to_wellesley(state):
    """Move one bike from Olin to Wellesley.
    
    state: bikeshare State object
    """
    if state.olin == 0:
        return
    state.olin -= 1
    state.wellesley += 1
    
def bike_to_olin(state):
    """Move one bike from Wellesley to Olin.
    
    state: bikeshare State object
    """
    if state.wellesley == 0:
        return
    state.wellesley -= 1
    state.olin += 1
```

Now if you run the simulation again, it should behave.


```python
bikeshare = State(olin=10, wellesley=2)
run_simulation(bikeshare, 0.4, 0.2, 60)
decorate_bikeshare()
```


![png](output_21_0.png)


## Comparison operators

The `if` statements in the previous section used the comparison operator `==`.  The other comparison operators are listed in the book.

It is easy to confuse the comparison operator `==` with the assignment operator `=`.

Remember that `=` creates a variable or gives an existing variable a new value.


```python
x = 5
```




    5



Whereas `==` compares two values and returns `True` if they are equal.


```python
x == 5
```




    True



You can use `==` in an `if` statement.


```python
if x == 5:
    print('yes, x is 5')
```

    yes, x is 5
    

But if you use `=` in an `if` statement, you get an error.


```python
# If you remove the # from the if statement and run it, you'll get
# SyntaxError: invalid syntax

#if x = 5:
#    print('yes, x is 5')
```

**Exercise:** Add an `else` clause to the `if` statement above, and print an appropriate message.

Replace the `==` operator with one or two of the other comparison operators, and confirm they do what you expect.

## Metrics

Now that we have a working simulation, we'll use it to evaluate alternative designs and see how good or bad they are.  The metric we'll use is the number of customers who arrive and find no bikes available, which might indicate a design problem.

First we'll make a new `State` object that creates and initializes additional state variables to keep track of the metrics.


```python
bikeshare = State(olin=10, wellesley=2, 
                  olin_empty=0, wellesley_empty=0)
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
      <th>olin</th>
      <td>10</td>
    </tr>
    <tr>
      <th>wellesley</th>
      <td>2</td>
    </tr>
    <tr>
      <th>olin_empty</th>
      <td>0</td>
    </tr>
    <tr>
      <th>wellesley_empty</th>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>



Next we need versions of `bike_to_wellesley` and `bike_to_olin` that update the metrics.


```python
def bike_to_wellesley(state):
    """Move one bike from Olin to Wellesley.
    
    state: bikeshare State object
    """
    if state.olin == 0:
        state.olin_empty += 1
        return
    state.olin -= 1
    state.wellesley += 1
    
def bike_to_olin(state):
    """Move one bike from Wellesley to Olin.
    
    state: bikeshare State object
    """
    if state.wellesley == 0:
        state.wellesley_empty += 1
        return
    state.wellesley -= 1
    state.olin += 1
```

Now when we run a simulation, it keeps track of unhappy customers.


```python
run_simulation(bikeshare, 0.4, 0.2, 60)
decorate_bikeshare()
```


![png](output_39_0.png)


After the simulation, we can print the number of unhappy customers at each location.


```python
bikeshare.olin_empty
```




    6




```python
bikeshare.wellesley_empty
```




    0



## Exercises

**Exercise:** As another metric, we might be interested in the time until the first customer arrives and doesn't find a bike.  To make that work, we have to add a "clock" to keep track of how many time steps have elapsed:

1. Create a new `State` object with an additional state variable, `clock`, initialized to 0. 

2. Write a modified version of `step` that adds one to the clock each time it is invoked.

Test your code by running the simulation and check the value of `clock` at the end.


```python
bikeshare = State(olin=10, wellesley=2, 
                  olin_empty=0, wellesley_empty=0,
                  clock=0)
```


```python
def bike_to_wellesley(state):
    """Move one bike from Olin to Wellesley.
    
    state: bikeshare State object
    """
    if state.olin == 0:
        state.olin_empty += 1
        return
    state.olin -= 1
    state.wellesley += 1
    state.clock += 1
    
def bike_to_olin(state):
    """Move one bike from Wellesley to Olin.
    
    state: bikeshare State object
    """
    if state.wellesley == 0:
        state.wellesley_empty += 1
        return
    state.wellesley -= 1
    state.olin += 1
    state.clock += 1
```


```python
run_simulation(bikeshare, 0.4, 0.2, 60)
decorate_bikeshare()
```


![png](output_46_0.png)



```python
bikeshare.count
```




    <bound method Series.count of olin                1
    wellesley          11
    olin_empty         18
    wellesley_empty     0
    dtype: int64>



**Exercise:** Continuing the previous exercise, let's record the time when the first customer arrives and doesn't find a bike.

1. Create a new `State` object with an additional state variable, `t_first_empty`, initialized to -1 as a special value to indicate that it has not been set. 

2. Write a modified version of `step` that checks whether`olin_empty` and `wellesley_empty` are 0.  If not, it should set `t_first_empty` to `clock` (but only if `t_first_empty` has not already been set).

Test your code by running the simulation and printing the values of `olin_empty`, `wellesley_empty`, and `t_first_empty` at the end.


```python
bikeshare = State(olin=10, wellesley=2, 
                  olin_empty=0, wellesley_empty=0,
                  clock=0, t_first_empty = -1)
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
      <th>olin</th>
      <td>10</td>
    </tr>
    <tr>
      <th>wellesley</th>
      <td>2</td>
    </tr>
    <tr>
      <th>olin_empty</th>
      <td>0</td>
    </tr>
    <tr>
      <th>wellesley_empty</th>
      <td>0</td>
    </tr>
    <tr>
      <th>clock</th>
      <td>0</td>
    </tr>
    <tr>
      <th>t_first_empty</th>
      <td>-1</td>
    </tr>
  </tbody>
</table>
</div>




```python
def bike_to_wellesley(state):
    """Move one bike from Olin to Wellesley.
    
    state: bikeshare State object
    """
    if state.olin == 0:
        state.olin_empty += 1
        return
    state.olin -= 1
    state.wellesley += 1
    state.clock += 1
    
    if state.olin_empty !=0:
        return
        state.t_first_empty = state.clock 
        
def bike_to_olin(state):
    """Move one bike from Wellesley to Olin.
    
    state: bikeshare State object
    """
    if state.wellesley == 0:
        state.wellesley_empty += 1
        return
    state.wellesley -= 1
    state.olin += 1
    state.clock += 1
    
    if state.wellesley_empty != 0:
        return
    state.t_first_empty = state.clock
    
```


```python
run_simulation(bikeshare, 0.4, 0.2, 60)
decorate_bikeshare()
```


![png](output_51_0.png)



```python
bikeshare.olin_empty
```




    1




```python
bikeshare.wellesley_empty
```




    0




```python
bikeshare.t_first_empty
```




    38




```python
bikeshare.count
```




    <bound method Series.count of olin                1
    wellesley          11
    olin_empty          1
    wellesley_empty     0
    clock              39
    t_first_empty      38
    dtype: int64>


