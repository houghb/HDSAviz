"""
Tools for reading and processing the sensitivity analysis data files.
Some of the files are specific to our project (`input_parameters.csv' and
`results.csv`), but the results of sensitivity analyses are formatted
as any SALib analysis results will be.

Our data files are stored outside this repository because they are too large,
so it may be necessary for future users to update the relative paths below
(our data directory is located at ../../HDSAviz_data/
"""
import os

import pandas as pd


def read_file(path, numrows=None, drop=False, sep=','):
    """
    Function reads a file of input parameters or model results
    and returns a pandas dataframe with its contents.
    The first line of the input should contain headers
    corresponding to the column names.

    Parameters:
    ----------
    path      : String with the complete filename, including
                absolute or relative path.
    numrows   : Integer number of rows of the file to read.
                If you don't specify this parameter all rows
                will be read.
    drop      : A list of strings indicating which (if any)
                of the named columns you do not want to include
                in the resulting dataframe. (ex. ['cats', 'dogs'],
                default is not to drop any rows)
    sep       : String indicating the column separator in the
                file (optional, default = ',').

    Returns:
    --------
    df : A pandas dataframe with the contents of the file,
         limited to the number of rows specified and without the
         columns named in "drop".
    """
    df = pd.read_csv(path, sep=sep, nrows=numrows)
    if not drop:
        df.drop(drop, axis=1, inplace=True)

    return df


def get_params(path='../../HDSAviz_data/input_parameters.csv',
               numrows=None, drop=['End_time', 'Oxygen']):
    """
    NOTE: This function is specific to our lignin modeling dataset

    Returns a pandas dataframe with all the parameters analyzed in
    the sensitivity analysis, but not additional parameters like
    end time and oxygen content.  If you would like all of the
    parameters (even those not analyzed for sensitivity) then pass
    drop=False.

    Parameters:
    ----------
    path    : string containing the path to the parameters csv
    numrows : the number of rows of the input_parameters file to read
              (default is to read all rows).
    drop    : a list of strings for which parameters you do not want to
              include in the returned dataframe.  If you want all params
              then pass drop=False.

    Returns:
    -------
    A pandas dataframe

    """
    return read_file(path, numrows=numrows, drop=drop)


def get_results(path='../../HDSAviz_data/results.csv',
                numrows=None, drop=['light_aromatic_C-C',
                                    'light_aromatic_methoxyl']):
    """
    NOTE: This function is specific to our lignin modeling dataset

    Returns a pandas dataframe with the results of running all of the
    simulations for the parameters sets in `input_parameters.csv`. This
    function drops two unused functional groups from the results file.

    Parameters:
    ----------
    path    : string containing the path to the results csv file
    numrows : the number of rows of the input_parameters file to read
              (default is to read all rows).
    drop    : a list of strings for which output measures to drop from
              the returned dataframe.  If you want all outputs use
              drop=False.
    """
    return read_file(path, numrows=numrows, drop=drop)


def get_sa(path='../../HDSAviz_data/'):
    """
    This function reads and processes all the sensitivity analysis results
    in a specified folder, and returns a dictionary with the corresponding
    dataframes.  Sensitivity analysis results should be in the default SALib
    format and must start with the letter 'a'.

    NOTE: there are two lines of code at the beginning of this function
    (the filenames.remove lines) that are specific to our lignin modeling
    dataset.  Future users will want to remove or modify these lines to use
    with other datasets.

    Parameters:
    -----------
    path : String containing the relative or absolute path of the directory
           where analysis_*.txt files are stored.  There cannot be any
           files or folders within this directory that start with 'a'
           except those generated by the SALib sensitivity analysis.

    Returns:
    --------
    sens : Dictionary where keys are the names of the various output measures
           (one output measure per analysis file in the folder specified by
           path).  Dictionary values are a list of pandas dataframes.  If
           only first and total order indices were calculated in the
           sensitivity analysis then this list will contain just one pandas
           dataframe (sens[key][0]) and the second item in the list will be
           False.  If second order indices are present they are in a second
           dataframe (sens[key][1]).
    """
    filenames = [filename for filename in os.listdir(
                path) if filename.startswith('a')]
    # These two functional groups are not present in the light oil fraction
    filenames.remove('analysis_light_aromatic-C-C.txt')
    filenames.remove('analysis_light_aromatic-methoxyl.txt')

    # Make a dictionary where keys are the different output measures
    # (one for each analysis file) and values are lists of dataframes
    # with the first/total analysis results, and the second order results.
    sens = {}
    for i, filename in enumerate(filenames):
        name = filename[9:].replace('.txt', '')

        with open(path + filename) as result:
            contents = []
            contents.append(result.readlines())
            # find the line number in the file where 2nd order results appear
            for i, line in enumerate(contents[0]):
                # End this loop when you reach the line that separates
                # the first/total indices from the second order indices
                if line.startswith('\n'):
                    break
                # If no second order indices in file
                else:
                    i = False
            # If there are second order indices in the file
            if i:
                sens[name] = [pd.read_csv(path + filename, sep=' ',
                                          nrows=(i - 1)),
                              pd.read_csv(path + filename, sep=' ',
                                          skiprows=i)
                              ]
            else:
                sens[name] = [pd.read_csv(path + filename, sep=' '),
                              False]

        # Convert negative values to 0 (all negative values are close to
        # zero already, negative values are the result of machine precision
        # issues or setting n too low when generating the parameter sets)
        sens[name][0].ix[sens[name][0]['S1'] < 0, 'S1'] = 0
        if isinstance(sens[name][1], pd.DataFrame):
            sens[name][1].ix[sens[name][1]['S2'] < 0, 'S2'] = 0

        # Change 'rxn' to 'k' for consistency with inputs file
        sens[name][0].Parameter = (sens[name][0].Parameter
                                   .str.replace('rxn', 'k', case=False))

    return sens


def combine_sens(order):
    """
    STILL WORKING ON WRITING THIS FUNCTION

    This function creates a pandas dataframe that has all the sensitivity
    indices and confidence values of a specified order (first, total) from
    every output measure.

    Parameters:
    -----------
    order : String indicating which order indices to combine (first, total)

    Returns:
    --------

    """
#     temp = np.ones((len(filenames),len(SA['CO'].Parameter)+1))
#     column_names = np.concatenate((np.array(['Output_Measure'],dtype=object),
#                                    SA['CO'].Parameter.values),axis=0)
#     row_names = [x[9:].replace('.txt','') for x in filenames]

#     for i,name in enumerate(row_names):
#         temp[i,1:] = SA[name].ST.values

#     STdata = pd.DataFrame(temp,columns=column_names)
#     STdata['Output_Measure'] = row_names


def id_unnecessary():
    """
    STILL WORKING ON WRITING THIS FUNCTION

    Identify candidate reactions which may not be necessary at all
    in the kinetic scheme.  Such reactions have no influence on the
    output measures of interest, so we suspect they may be acceptible
    to prune from the kinetic scheme.
    """
#     for col in STdata.columns:
#         if col != 'Output_Measure':
#             if STdata[col].max() == 0.0:
#                 print col
