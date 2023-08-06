# fileloghelper

A simple helper for logging content to files (and displaying it)

## Installation

```bash
pip3 install fileloghelper
```

## class Logger

Used to log content to file and print output to the console

### **init**(filename='log.txt', context='', verbose=True)

Logger will be configured to be saved to 'filename' if self.save() is called. 'context' is used to configure the behavior of logging/printing (see set_context()). If 'verbose', it will write extra information about the statement in the log file. If an error/warning is handled via show_error()/show_warning()/handle_exception(), it will write it's type in the same place.

```python
verbose = False
>>> [context] [12:34:56] Hello World!
verbose = True
>>> [DEBUG] [context] [12:34:56] Hello World!
>>> [NotImplementedError] [context] [12:34:56] Hello World!
```

### set_context(context)

Specifies context which will be added to all outputs (file & terminal) in front

|  parameter   | description                                     |
| :----------: | ----------------------------------------------- |
| context: str | string to be added to output of other functions |

### set_verbose(verbose)

Sets verbose mode for whole logger. If true, a info whether the text is success/debug/warning/error information will be added to the file

|   parameter   | description                   |
| :-----------: | ----------------------------- |
| verbose: bool | value to set for verbose mode |

### save()

Saves the file under default/at declaration specified filename

### clear()

Clear the log. **Note**: You have to save again to make changes to the actual file

### success(text, display=True)

Writes log to file. If verbose mode active, '[SUCCESS]' will be written in addition.

|   parameter   | description           |
| :-----------: | --------------------- |
| display: bool | print text on console |

### debug(text, display=True)

Writes log to file. If verbose mode active, '[DEBUG]' will be written in addition.

|   parameter   | description           |
| :-----------: | --------------------- |
| display: bool | print text on console |

### warning(text, display=True, extra_context="")

Writes log to file. If verbose mode active, [{extra_context}] will be written in addition. extra_context can be used to give extra information about the warning.

|   parameter   | description           |
| :-----------: | --------------------- |
| display: bool | print text on console |

### error(text, display=True, extra_context="")

Writes log to file. If verbose mode active, [{extra_context}] will be written in addition. extra_context can be used to give extra information about the error.

|   parameter   | description           |
| :-----------: | --------------------- |
| display: bool | print text on console |

### plain(text, display=False, extra_long=False, very_plain=False)

Writes log without any colors to file. If display==True, the text will be displayed. If extra_long==True, milliseconds will be added to the timestamp. If very_plain==True, the timestamp will be omitted.

### show_warning(warning: Warning, display=True)

Extracts class from warning and uses it to invoke warning() with extra_context

### show_error(error: Exception, display=True)

Extracts class from error and uses it to invoke error() with extra_context

### handle_exception(exception: Exception)

Automatically categorizes exception to invoke show_warning() or show_error()

### header(sys_stat=False, date=False, description="", display=0)

Use plain() to output certain information:

|  parameter  | description                                                       |
| :---------: | ----------------------------------------------------------------- |
|  sys_stat   | write system information to the log                               |
|    date     | write date information to the log                                 |
| description | write the specified description to the log                        |
|   display   | also display certain information in the console (see table below) |

**Modes for display:**

| mode number  | information printed              |
| :----------: | -------------------------------- |
| 0 (standard) | none                             |
|      1       | description only                 |
|      2       | date only                        |
|      3       | system information only          |
|      4       | description & date               |
|      5       | description & system information |
|      6       | date & system information        |
|      7       | all above                        |

### progress(x=0, description='', startx=0, maxx=100, mode='=', scale=10)

Easily create a progress bar. Startx is the minimal x value, maxx the maximum possible. 'mode' specifies the style ('=' / '#'). 'scale' indicates the length of the progress bar in characters. To update the progress bar, simply run the same method again and specify x to visualize the progress.

```python
from fileloghelper import Logger

logger = Logger(filename='log.txt', context='MyContext')

logger.progress(description="Running 'Self-Destruction'")
```

```none
Running 'Self-Destruction': 0.0% [>        ]
```

<br />

```python
logger.progress(80)
```

```none
Running 'Self-Destruction': 80.0% [=======> ]
```

### Logger - Example

```python
from fileloghelper import Logger

logger = Logger(filename='log.txt', context='MyLogger')

logger.header(sys_stat=True, date=True, description='A short description', display=7)

logger.debug('Hello World!', display=False)
logger.success('Successfull!', display=True)
logger.handle_exception(NotImplementedError("off to work!"))

logger.save()
```

## class VariableObserver

Wrapper for variable with functions pre/post changing the variables's value and (for int and float) a history (a list, e.g. to plot with matplotlib)

### **init**(value, pre_chance_func=lambda x: x, post_change_func=lambda x: x)

|    parameter     | description                                    |
| :--------------: | ---------------------------------------------- |
|      value       | starting value of the variable                 |
| pre_change_func  | function called before the variable is changed |
| post_change_func | function called after the variable is changed  |

**Note:** pre/post-change functions will be called with the value of the (main) variable. They will have to accept 1 positional argument.

### set_value(new_value)

If new_value is different from the previous variable, it will trigger pre/post-change functions and change the value of the variable.

### get_history()

If the type of the (main) variable is int or float, it has created a list of past values which can be get by calling this method

### VariableObserver - Example

```python
from fileloghelper import VariableObserver

def print_value(x):
    print("Current value:", x)

vo = VariableObserver(0, print_value, print_value)
for i in range(3):
    vo.set_value(i)
```

```none
Current value: 0 [pre-change]
Current value: 1 [post-change]
Current value: 1 [pre]
Current value: 2 [post]
```

```python
vo.get_history()
```

```none
[0, 1, 2]
```

## class VarSet

A set/collection of VariableObserver to make it easer to print larger streams of data to the console.

### **init**(variables: dict[str, value])

### print_variables()

Prints values of all variables in set to the console while overwriting old ones

### VarSet - Example

```python
from fileloghelper import VarSet
from time import sleep

myvars = {
    "x": 0,
    "y": 0
}
vs = VarSet(myvars)
for i in range(11):
    vs.variables.get("x").set_value(i)
    vs.variables.get("y").set_value(i * 2)
    vs.print_variables()
    sleep(0.5)
```

final output:

```none
10, 20
```
