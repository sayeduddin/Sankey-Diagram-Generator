#!/usr/bin/env python3
##############
#  19010865  #
#SAYED  UDDIN#
##############
"""Draw a sankey diagram using data from a given input file.
"""
import sys
from ezgraphics import GraphicsWindow
from math import *


WIDTH = 1000
HEIGHT = 700
COLOURS = [(230, 25, 75), (60, 180, 75), (255, 225, 25), (0, 130, 200),
(245, 130, 48), (145, 30, 180), (70, 240, 240), (240, 50, 230),
(210, 245, 60), (250, 190, 212), (0, 128, 128), (220, 190, 255),
(170, 110, 40), (255, 250, 200), (128, 0, 0), (170, 255, 195),
(128, 128, 0), (255, 215, 180), (0, 0, 128), (128, 128, 128),
(255, 255, 255), (0, 0, 0)]


def read_file(file_name):
    """Opens and reads the file. Returns the title, left-hand axis label and 
    the data values in the file.


    Parameters
    ----------
        file_name : str
            Name of file containing the data.

    Raises
    ------
        FileNotFoundError:
            If file not found or is not readable, this exception is raised

    Returns
    -------
        contents[0] : str
            Diagram title
        contents[1] : str
            Left-hand axis label 
        contents[2:] : list
            Each element contains one line of data from the file
    """
    try:
        file = open(file_name, "r+")
    except FileNotFoundError:
        raise
    contents = file.readlines()
    file.close()
    return contents[0], contents[1], contents[2:]


def set_up_graph(title, left_axis_label):
    """
    Creates a window and canvas. Displays the title, left-hand axis label.
    Returns a reference to the window. 


    Parameters
    ----------
        title : str
            Title for the window
        left_axis_label : str
            Left-hand axis label

    Returns
    -------
        GraphicsWindow : GraphicsWindow
            Reference to the window
    """
    win = GraphicsWindow(WIDTH, HEIGHT)
    canvas = win.canvas()
    win.setTitle(title)
    canvas.setTextAnchor("w")
    #Allows text to be drawn from the left-middle of the text
    canvas.drawText(7, HEIGHT / 2, left_axis_label.split(",")[0])
    #Splits the line in left_axis_label and uses first item
    return win


def process_data(data_list):
    """
    Returns a dictionary produced by processing the data in the list. 


    Parameters
    ----------
        data_list : list
            List containing the data read from the file

    Raises
    ------
        ValueError:
            Raised if there are errors in the data values in the file

    Returns
    -------
        dictionary : dictionary
            Data about the value and name of each bar 
    """
    data_dict={}
    for x in range(len(data_list)):
        split_data = [item.strip() for item in data_list[x].split(",")]
        #Splits the line from the file and strips each item
        if "" in split_data:
            print(f"Error on line {x+3}: data is missing")
            raise ValueError
        try:
            if float(split_data[1]) < 0:
                raise ValueError
            #Raises error if value is negative
            data_dict[split_data[0]] = float(split_data[1])
        except ValueError:
            print(f"Error on line {x+3}: {split_data[1]} is not a valid number")
            raise ValueError
    return data_dict         


def get_colours(data_list):
    """Gets colour data from files 


    Parameters
    ----------
        data_list: list
            List of data from text file

    Returns
    -------
        colours : list
            Contains colour data for each bar 
    """
    colours = []
    for item in range(len(data_list)):
        try:
            split_item = [x.strip() for x in data_list[item].split(",")]
            colour = (int(split_item[-3]), int(split_item[-2]), int(split_item[-1]))
            for value in colour:
                if value / 255 > 1 or value / 255 < 0:
                    print(f"Colour {colour} on line {item + 3} is invalid.")
                    raise
            colours.append((int(split_item[-3]),
                            int(split_item[-2]),
                            int(split_item[-1])))
            #Check to see if there is a valid string of numbers at the end of
            #the line to use as a colour
        except:
            colours.append(COLOURS[item%len(COLOURS)])
            #%len(colours) allows the default colour option to loop back around
            #there are no more different colours to choose from
    return colours


def draw_sankey(window, data_dic, colours):
    """Draw the sankey diagram

    Args:
        window (GraphicsWindow): contains the graph
        data_dic (dictionary): contains the data for the graph
        colours (list): contains colours data for each bar
    """
    total_heights = 500 - 10 * (len(data_dic) - 1)
    #Calculates the total flow of the bars 
    canvas = window.canvas()
    end_y = 100
    source_y = (700 - total_heights) / 2
    
    canvas.setFill(colours[0][0], colours[0][1], colours[0][2])
    canvas.drawRect(100, (700 - total_heights) / 2, 20, total_heights)
    canvas.setTextAnchor("w")
    #Draws and labels source bar on the left

    bar_heights=[data_dic[value] * total_heights / sum(data_dic.values())
                 for value in data_dic]
    #Uses total heights to calculate the proportional height of each bar
    colour_sankey(canvas, data_dic, end_y, bar_heights, colours, source_y)


def colour_sankey(canvas, data_dic, end_y, bar_heights, colours, source_y):
    """
    Draws coloured and curved bars by drawing vertical strips of gradually
    changing colour.

    Parameters
    ----------
    canvas : canvas
        Contains the canvas object for drawing shapes on
    data_dic : dictionary
        Contains the data from the text files such as titles and values 
    end_y : int
        Y-coordinate at at the end of the bar
    bar_heights : list
        Contains the list of bar heights
    colours : list
        Contains the list of colour data as tuples
    source_y : integer
        Y-coordinate at the start of the bar   
    """
    for a, name in enumerate(data_dic):
    #Iterates through each item in data_dic
        canvas.setColor(0, 0, 0)
        canvas.drawText(885, end_y + bar_heights[a] / 2, name)
        canvas.setFill(colours[a + 1][0], colours[a + 1][1], colours[a + 1][2])
        canvas.drawRect(860, end_y, 20, bar_heights[a])
        
        for x in range(120, 861):
            delta_x, delta_y = (861-120), end_y - source_y
            increment = [(colours[a + 1][b] - colours[0][b]) / 740
                         for b in range(3)]
            #Calculates increments needed to change each colour by
            gap = source_y + delta_y / 2
            #Padding for curve to draw curve at correct position
            y = gap + (delta_y / 2) * sin((-pi / 2) + (pi / delta_x) * (x-119))
            #Function for transformed sine wave to connect source_y and end_y
            canvas.setColor(0, 0, 0)
            canvas.drawLine(x, y , x, y + bar_heights[a] + 1)
            #Draws longer black line behind the coloured line to make an outline
            canvas.setColor(int(colours[0][0] + (x - 119) * increment[0]),
                            int(colours[0][1] + (x - 119) * increment[1]),
                            int(colours[0][2] + (x - 119) * increment[2]))
            canvas.drawLine(x, y + 1, x, y + bar_heights[a])
            #Draws coloured line
        
        end_y += bar_heights[a] + 10
        source_y += bar_heights[a]
        #Moves y coordinates to the position of the next bar 
        

def main():
    # DO NOT EDIT THIS CODE
    input_file = ""
    args = sys.argv[1:]  
    if len(args) == 0:
        input_file = input("Please enter the name of the file: ")                    
    elif len(args) > 1:
        print('\n\nUsage\n\tTo visualise data using a sankey diagram type:\
            \n\n\tpython sankey.py infile\n\n\twhere infile is the name of \
            the file containing the data.\n')
        return         
    else:
        input_file = args[0]

    # Section 1: Read the file contents
    try:
        title, left_axis_label, data_list = read_file(input_file)
    except FileNotFoundError:
        print(f"File {input_file} not found or is not readable.")
        return 
    
    # Section 2: Create a window and canvas
    win = set_up_graph(title, left_axis_label)

    # Section 3: Process the data
    try:
        data_dic = process_data(data_list)
    except:
        print("Content of file is invalid")
        #win.close()
        return

    # Section 4: Draw the graph
    draw_sankey(win, data_dic, get_colours([left_axis_label] + data_list))
    #get_colours() has been passed in as a parameter to pass in the colour data
    #from the files

    win.wait()


if __name__ == "__main__":
    main()
