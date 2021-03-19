Extending the functionality
===========================
The software is structured to help extension of the code be really simple.
To extend any part of the software you need to do two things:

1. Add a function to the user_methods.py file in the top level of the particletracker project.
2. Add an appropriate entry to a .param file

To illustrate how to extend the software we use an example which is pretty 
much the same regardless of which part of the software you wish to extend.
Lets say we have a new postprocessing method which we want to implement.

1. Add a function to user_methods.py
------------------------------------
In the top level of the particletracker module is the user_methods.py. This contains template functions 
for the different sections. There are a lot of comments explaining details contained in these templates,
however we have stripped out all the comments here to save space. The Docstrings in these examples explain 
what inputs and outputs your function needs to work. You then write whatever code is required.

.. code-block:: python
    
    def postprocessor_method_name(data, f_index=None, parameters=None, call_num=None):
        try:
            method_key = get_method_key('postprocessor_method_name', call_num=call_num)
            params = parameters['postprocess'][method_key]
            """
            Write the body of your code
            """
            return df
        except Exception as e:
            raise PPMethodNameError(e)
    

There is also a matching exception which you need to also copy. Make this exception name unique
and match the raised Exception above:

.. code-block:: python
   
   class PPMethodNameError(PostprocessorError):
        """Implement this custom exception."""
        def __init__(self,e):
            super().__init__(e)
            self.error_msg = 'specific error message to show user in status bar'
            self.e=e


2. Add an entry to the dictionary
---------------------------------
Open the file particletracker.general.param_file_creator. Inside this file there
is a multiply nested dictionary that controls the behaviour of the particletracker.

Expand the "postprocess" dictionary. Add a new key to this dictionary with the same
name as given to the function above and a value that is also a dictionary containing
all the parameters needed.

.. code-block:: python
   
   postprocess = {postprocess_method:(smooth,),
                'smooth':{'column_name':'y',
                          'output_name':'y_smooth',
                          'span':[5,1,50,1],
                          'method':'default'
                         },
                'postprocessor_method_name':{'param1' : [startval, minval, maxval, step],
                                             'param2' : [value, ('value', 'value2')],
                                             'param3' : (0,255,0)
                                            }
                    }


The parameters are automatically assessed to decide what gui element to create. Here param 1
will result in a slider with initial value startval and min, max and increment ("step") values as shown.
If step is an integer eg 1 the slider will return integers. If step is a decimal eg 0.01 then the slider
As a result if your value happens to be something like 1.0 you should write 1.0 and not 1.
param 2 results in a dropdown options box with the values value, value2, value3 to choose between. Within
the brackets all these should be strings. However value at the first position should be of the correct datatype.
Param3 produces a text box which can take any value.

To regenerate the settings file you can now call create_param_file(filename.param) to create a new file 
which can be read into the gui. 

.. code-block:: python

   from particletracker.general.param_file_creator import create_param_file
   
   settings_filename = 'path/to/new/settings_file.param'
   create_param_file(settings_filename)

To access the variables in your new dictionary entry inside the new method you need to write

.. code-block:: python

   param1 = get_param_val(params['param1'])
   param2 = get_param_val(params['param2'])
   


