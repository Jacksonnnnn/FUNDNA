[UK Logo]: https://i.gyazo.com/962a0a13ee9d910deacdea456f514f85.png "University of Kentucky College of Engineering Logo"

![alt-text][UK Logo]
# Function to Chemical Reaction Network
This project uses DNA as logic gates to create a Chemical Reaction Network (CRN) that allows us to compute values of different mathematical functions.

## Important Information
#### Background
Read the scholarly article here: https://www.nature.com/articles/s41598-018-26709-6

### About the Project
#### Project Lead
> Dr. Sayed Ahmad Salehi \
> Assistant Professor \
> Department of Electrical and Computer Engineering \
> Director of Computing with Unconventional Technologies (CUT) Lab \
> University of Kentucky | http://salehi.engr.uky.edu/

#### Descrption
When we hear about computation and information processing the first thing that comes to our minds is man-made electronic processing systems. However, computation is not a man-made phenomenon and, in fact, the most powerful information processing systems have been provided by nature. For example, complex circuits within cells

- can have over 30,000 distinct states;

- their computational efficiency per operation is 4 to 5 orders of magnitude more efficient than nano-scale GHz electronic processors regarding energy and size;

- they are massively parallel such that more than 10,000,000 biochemical reactions fire in a human cell each second.

Our research is about the exploration of computational power in bio-molecular systems. Since the chemical reaction network (CRN) theory is the fundamental model in the study of molecular reactions, we try to understand and discover the information processing abilities of CRNs and accordingly design new molecular systems for particular applications. One part of this research is the design of digital signal processing algorithms by CRNs. Another part is the computation of mathematical functions by CRNs using a new encoding of information so called fractional representation. In order to address practical issues for biological implementation of these designs, we map the CRNs to DNA reactions using DNA strand-displacement mechanism. Applications for our research are drug delivery and monitoring, smart and personalized drugs.

Further, we work on encoding and storing information by DNA molecules as they have the potential to be used as future memories with longer retention, higher density  and lower power consumption compared to semiconductor memories. Also we are interested in the interface of biological circuits (e.g., DNA and RNA molecules) with semiconductor circuits and sensors.

## The Software
In this GitHub Repository, there are several python files that are able to be executed to assist in generating Chemical Reaction Networks for a given function. Though functions are limited at the program's current state, it is a very useful tool for cross-checking any calculations.

#### Installation
1. Download, fork, or clone the repository.
2. Make sure the latest version of Python (Anaconda recommended) is installed along with Pathlib, Tkinter, NumPy, SciPy, NetworkX, and PIL.
3. Run the GUI file (~/build/gui.py).

#### Use and Important Notes
At the moment, this program can only calculate functions whose taylor series representation is alternating as positive and negative. This is because it only has support for Horner's Rearrangement Rule, as presented in the scholarly article provided above. For example:
> e^(-x) \
> sin(x) \
> cos(x) \
> log(x+1)

* When utilizing the GUI, it is strongly recommended using `x` as a variable, however it has support as long as you indicate which variable will be used.
  * ***The GUI has support for single-variable functions, not multi-variable.***

* Point estimations should be 0 or 1 only, otherwise the results will be inaccurate or will throw and exception.
* The degree field will indicate what power (n-1) the generated taylor function will go to.
* The traced value at point will return what the function's actual value is at the point estimation given. Example: sin(x) around point 0 will equal 0, but cos(x) around point 1 will equal 1.

#### Contributing to the Project
If you would like to contribute to this project, please reach out to Dr. Salehi with information provided in the link to his website above. Feel free to contribute by creating pull requests describing your changes and why and the GitHub Repo Admin will handle all requests!

Thank you and good luck!