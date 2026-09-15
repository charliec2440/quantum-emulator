from random import random
# importing random for taking measurments of qubit systems

PI= 3.1415926535897932
E = 2.7182818284590452
ANGLES= [0.46364760900080626, 0.24497866312686423,
	0.12435499454676142, 0.062418809995957336,
	0.031239833430268274, 0.015623728620476828,
	0.007812341060101111, 0.0039062301319669713,
	0.0019531225164788185, 0.0009765621895593196,
	0.00048828121119489834, 0.0002441406201493618,
	0.00012207031189367022, 6.103515617420878e-05,
	3.05175781155261e-05, 1.5258789061315763e-05,
	7.629394531101971e-06, 3.8146972656064966e-06,
	1.9073486328101872e-06, 9.53674316405961e-07,
	4.768371582030889e-07, 2.38418579101558e-07,
	1.192092895507807e-07, 5.960464477539056e-08,
	2.9802322387695306e-08, 1.4901161193847656e-08,
	7.450580596923828e-09, 3.725290298461914e-09,
	1.862645149230957e-09, 9.313225746154785e-10,
	4.656612873077393e-10, 2.3283064365386963e-10,
	1.1641532182693481e-10, 5.820766091346741e-11,
	2.9103830456733704e-11, 1.4551915228366852e-11,
	7.275957614183426e-12, 3.637978807091713e-12,
	1.8189894035458565e-12, 9.094947017729282e-13,
	4.547473508864641e-13, 2.2737367544323206e-13,
	1.1368683772161603e-13, 5.684341886080802e-14,
	2.842170943040401e-14, 1.4210854715202004e-14,
	7.105427357601002e-15, 3.552713678800501e-15,
	1.7763568394002505e-15, 8.881784197001252e-16,
	4.440892098500626e-16, 2.220446049250313e-16,
	1.1102230246251565e-16, 5.551115123125783e-17,
	2.7755575615628914e-17, 1.3877787807814457e-17,
	6.938893903907228e-18, 3.469446951953614e-18,
	1.734723475976807e-18, 8.673617379884035e-19,
	4.336808689942018e-19, 2.168404344971009e-19,
	1.0842021724855044e-19, 5.421010862427522e-20]
# constants for use within the code

class Matrix:
	### Matrix parent class to be inherited from for qubits and quantum gates ###

	def __init__(self, size, raw_data):
		### Initialises an instance of a matrix when being created ###
		# size in a [x, y] form to be accessed
		# data in just one list to be fed in to be put into the matrix
		self.collumns = size[0]
		self.rows = size[1]
		self.data = raw_data
		self.initialise()

	def initialise(self):
		### Creates two two dimensional lists from the raw data ###
		self.matrix = [[self.data[j + i * self.collumns] for j in range(self.collumns)] for i in range(self.rows)]
		self.transposed = [[self.data[i + j * self.collumns] for j in range(self.rows)] for i in range(self.collumns)]

	def redefine(self):
		### If you make changes to your matrix list you can use this to change the raw data and transposed list to match ###
		self.data = []
		for i in self.matrix:
			for j in i:
				self.data.append(j)
		self.transposed= [[self.data[i + j*self.collumns] for j in range(self.rows)] for i in range(self.collumns)]

	def __repr__(self):
		### Overwriting the repr function for a string representation of the matrix ###
		return f"A matrix of size {[self.collumns,self.rows]} with data {self.data}."

	def __str__(self):
		### Overwriting the string function for a nicely formatted version of the matrix ###
		matrix_list =[[] for i in range(self.rows)]
		for i in range(self.collumns):
			longest = 0
			for j in self.transposed[i]:
				if len(str(j)) > longest:
					longest = len(str(j))
			for j in range(len(self.transposed[i])):
				extra = longest - len(str(self.transposed[i][j]))
				extra_string = "".join([" " for k in range(extra//2)])
				matrix_list[j].append(extra_string + str(self.transposed[i][j]) + extra_string + "".join([" " for k in range(extra % 2)]))
		matrix_string = "r "
		for i in range(len(matrix_list)):
			for j in range(len(matrix_list[i])):
				matrix_string += matrix_list[i][j]
				if j != self.collumns - 1:
					matrix_string += "\t"
			if i == 0:
				matrix_string += " l\n"
			elif i == self.rows - 1:
				matrix_string += " J"
			else:
				matrix_string += " |\n"
			if i == self.rows - 2:
				matrix_string += "L "
			elif i == self.rows - 1:
				pass
			else:
				matrix_string += "| "
		return matrix_string
 
	def __add__(self, x):
	### Overwriting addition for addition between matricies ###
		if self.rows== x.rows and self.collumns == x.collumns:
			raw_data = []
			size = [self.collumns, self.rows]
			for i in range(self.rows):
				for j in range(self.collumns):
					raw_data.append(self.matrix[i][j] + x.matrix[i][j])
			return type(self)(size, raw_data)
		else:
			raise(Exception("These matricies are not compatable to add like this."))

	def __sub__(self, x):
		### Overwriting subtraction for subtraction between matricies ###
		if self.rows == x.rows and self.collumns == x.collumns:
			raw_data = []
			size = [self.collumns, self.rows]
			for i in range(self.rows):
				for j in range(self.collumns):
					raw_data.append(self.matrix[i][j] - x.matrix[i][j])
			return type(self)(size, raw_data)
		else:
			raise(Exception("These matricies are not compatable to subtract like this."))

	def __mul__(self, x):
		### Overwriting multiplication for matrix multiplication, and multiplication with other types ###
		if isinstance(x, Matrix):
			# when working with another matrix
			if self.collumns == x.rows:
				size= [x.collumns, self.rows]
				raw_data = []
				for i in range(self.rows):
					for j in range(x.collumns):
						t = 0
						for k in range(self.collumns):
							t += self.matrix[i][k] * x.transposed[j][k]
						raw_data.append(t)
				return type(x)(size, raw_data)
			else:
				raise(Exception("These matricies are not compatable to multiply together like this"))
		elif isinstance(x, int) or isinstance(x, float) or isinstance(x, IrrationalNumber) or isinstance(x, ComplexNumber):
			# when working with a float, integer, irrational or complex number
			new_data = [i * x for i in self.data]
			new_size = [self.collumns, self.rows]
			return type(self)(new_size, new_data)
		else:
			raise(Exception("That was not a valid datatype for this operation."))

	def __rmul__(self, x):
		### Overwriting multiplication but if is called with the matrix on the other side of the other piece of data ###
		if isinstance(x, int) or isinstance(x, float) or isinstance(x, IrrationalNumber) or isinstance(x, ComplexNumber):
			# in case of a float, integer, irrational or complex number
			new_data = [i * x for i in self.data]
			new_size = [self.collumns, self.rows]
			return type(self)(new_size, new_data)
		else:
			raise(Exception("That was not a valid datatype for this operation."))

	def dot(self, x):
		### Allowing for you to take a dot product between two vectors ###
		if self.rows== x.rows and self.collumns == 1 and x.collumns == 1:
			total = 0
			for i in range(self.rows):
				for j in range(self.collumns):
					total+= self.matrix[i][j] * x.matrix[i][j]
			return total
		else:
			raise(Exception("These matricies are not able to be dot producted together like this"))

	def inverse(self):
		### Calculates the inverse and the determinant of the matrix ###
		if self.rows == self.collumns:
			# a matrix must be square in order to be inverted
			if self.rows == 2:
				det = self.matrix[0][0] * self.matrix[1][1] - self.matrix[0][1] * self.matrix[1][0]
				if det == 0:
					return -1
			elif self.rows == 3:
				det = self.matrix[0][0] * self.matrix[1][1] * self.matrix[2][2] + self.matrix[0][1] * self.matrix[1][2] * self.matrix[2][0] + self.matrix[0][2] * self.matrix[1][0] * self.matrix[2][1] - self.matrix[0][2] * self.matrix[1][1] * self.matrix[2][0] - self.matrix[0][1] * self.matrix[1][0] * self.matrix[2][2] - self.matrix[0][0] * self.matrix[1][2] * self.matrix[2][1]
				if	det == 0:
					return -1

			id = identity(self.rows)
			# creates a blank identity to be transformed onto the inverse
			if self.matrix[0][0] == 0:
				# ensures that there is a value in the top left position so that the algorithm can start
				for i in range(self.rows):
					if self.matrix[i][0] != 0:
						self.row_addition(0, i)
						id.row_addition(0, i)
						break
			if self.matrix[0][0] == 0:
				# if it is impossible to move a value into the top left position with the process above then that means that the first collumn must be all zeros, so the matrix is non-invertable
				return -1
			for i in range(self.rows):
				# run through and eliminate all of the lower entries in the matrix to leave it in an upper triangularised form, while also doing the same operations to the prospective inverse to keep it at the same place
				for j in range(i):
					if self.matrix[i][j] != 0:
						if self.matrix[j][j] != 0:
							x = - 1 * (self.matrix[i][j] / self.matrix[j][j])
							self.row_addition(i, j, x)
							id.row_addition(i, j, x)
						else:
							# if you create a zero at this stage you do not necesarily know if the matrix is invertable for sure, but you can move the row down by one because then it's already got a zero in the right place and try again with the row below
							self.row_swap(i, j)
							id.row_swap(i, j)
							j = 0
					for k in range(self.collumns):
						if isinstance(self.matrix[i][k], float):
							# fixes errors thrown by numbers being negligebly close to zero, but not actually zero
							self.matrix[i][k] = round(self.matrix[i][k], 10)
			for i in range(self.rows):
				# run through and eliminate all of the upper entries in the matrix to leave it in a diagonalised form, while also doing the same operations to the prospective inverse to keep it at the same place
				for j in range(i):
					t = self.rows - i - 1
					u = self.rows - j - 1
					if self.matrix[t][u] != 0:
						x = - 1 * (self.matrix[t][u] / self.matrix[u][u])
						self.row_addition(t, u, x)
						id.row_addition(t, u, x)
					if self.matrix[t][t] == 0:
						# if you manage to eliminate a whole row (so it is all zeros after this point) then the matrix must be non-invertable
						return -1
					for k in range(self.collumns):
						# fixes errors thrown by numbers being negligebly close to zero, but not actually zero
						if isinstance(self.matrix[i][k], float):
							self.matrix[i][k] = round(self.matrix[i][k], 10)
			dets = []
			for i in range(self.rows):
				# pulls the remaining factor from each row to leave the original matrix as the identity and then multiplies in to the inverse with the relevant factor
				dets.append(self.matrix[i][i])
				id.row_multiplication(i, (1/dets[-1]))
			det = 1
			for i in dets:
				# constructs the determinant form the factors that were pulled from the matrix above
				det = det * i
			# saves the data so that it can be referenced again if the user wishes to and cleans up the matricies so that all data stored for them is the same data
			self.det = det
			self.inv = id
			self.initialise()
			id.redefine()
			return [det, id]
		else:
			# if the matrix is not square then it cannot be inverted
			return -1

	def row_addition(self, target, operator, multiple=1):
		### Elementary row operation to add a multiple of one row to another ###
		for i in range(self.collumns):
			self.matrix[target][i] += self.matrix[operator][i] * multiple

	def row_multiplication(self, target, operator):
		### Elementary row operation to multiply a whole row by a value ###
		for i in range(self.collumns):
			self.matrix[target][i] = self.matrix[target][i] * operator
 
	def row_swap(self, row_one, row_two):
		### Elementary row operation to swap the positions of two different rows ###
		t = self.matrix[row_one]
		self.matrix[row_one] = self.matrix[row_two]
		self.matrix[row_two] = t


class QubitSystem(Matrix):
	### Subclass for a system of qubits, extending of the Matrix class ###

	def __init__(self, size, raw_data):
		### Initialises an instance of a matrix when being created ###
		# size in a [x, y] form to be accessed
		# data in just one list to be fed in to be put into the matrix
		self.collumns = size[0]
		self.rows = size[1]
		condition_one = is_power_of_two(self.collumns)
		condition_two = self.is_unitary(raw_data)
		condition_three = self.collumns == 1
		# checks if it is a possible qubit
		if condition_one and condition_two and condition_three:
			self.data = raw_data
			self.initialise()
			self.number_of_qubits = power_of_two(self.rows)
		else:
			# stops the class being made
			raise(Exception("That was not a possible qubit to be created."))

	def __repr__(self):
		### Overwriting the repr function for a string representation of the Qubit System ###
		return f"A Qubit System of {power_of_two(self.rows)} qubits with probabilities {self.data}."

	def is_unitary(self, data):
		### Checks that the totals of the probabilites of a qubit system sums to 1 ###
		total = 0
		for i in data:
			total += probability(i)
		if round(total, 3) == 1:
			return True
		else:
			return False

	def measurement(self):
		### To take a random measurement of the system ###
		result= random()
		for i in range(self.rows):
			result-= probability(self.matrix[i][0])
			if result< 0:
				return binary(i, self.number_of_qubits)
		return binary(self.rows - 1, self.number_of_qubits)

	def specific_measurement(self, target_qubit):
		### To measure one specific qubit in the system ###
		# numbering with one as the rightmost qubit in the string
		target = 2 ** (target_qubit - 1)
		probability_of_zero = 0
		probability_of_one = 0
		for i in range(self.rows):
			# generate the probabilities that the target qubit would be a zero or a one on measurement
			parity= (i //target)% 2
			if parity == 0:
				probability_of_zero += probability(self.matrix[i][0])
			elif parity == 1:
				probability_of_one += probability(self.matrix[i][0])
		result = random()
		# take the measurement of the qubit
		if result < probability_of_zero:
			output = "0"
			divisor = probability_of_zero ** 0.5
		else:
			output = "1"
			divisor = probability_of_one ** 0.5
		new_system_data = []
		for i in range(self.rows):
			# breakdown the system according to the measurement just taken
			parity = (i //target)% 2
			if parity== int(output):
				new_probability = self.matrix[i][0] / divisor
				new_system_data.append(new_probability)
		new_system_size = [1, self.rows // 2]
		new_system = QubitSystem(new_system_size, new_system_data)
		return output, new_system

	def controlled_measurement(self, target_qubit, value):
		### To see what would happen if a qubit were to be measured to have a specific value ###
		# again with numbering starting from the rightmost qubit
		target = power_of_two(target_qubit) - 1
		first_probability = 0
		for i in range(self.rows):
			# generate the probability of the desired outcome
			parity = (i // target) % 2
			if parity == value:
				first_probability += probability(self.matrix[i][0])
		divisor = first_probability ** 0.5
		new_system_data = []
		for i in range(self.rows):
			# breakdown the system according to the desired measurement
			parity = (i // target) % 2
			if parity == value:
				second_probability = self.matrix[i][0] / divisor
				new_system_data.append(second_probability)
		new_system_size = [1, self.rows // 2]
		new_system = QubitSystem(new_system_size, new_system_data)
		return new_system

	def large_specific_measurement(self, length, direction):
		### Measures more than one specific qubit, but not the whole system ###
		# direction should be a boolean value, True going in from the right, False for going in from the left
		system = self
		output = ""
		for i in range(length):
			# runs through each qubit that needs to be measured
			if direction:
				t = 1
			else:
				t = power_of_two(system.rows)
			# measures each qubit in turn and then updates the current output with the result, and updates the system that it's working with to one that has collapsed under the measurement
			value, system = system.specific_measurement(t)
			if direction:
				output= value+ output
			else:
				output= output+ value
		return output, system

	def large_controlled_measurement(self, length, direction, target_string):
		### Measures multiple qubits from the left or the right to a specific value ###
		# again direction is boolean with True in from the Right and False in from the Left
		system = self
		for i in range(length):
			#Runs through all of the qubits in the wanting to be seeded
			if direction:
				t = system.rows - 1
				target= int(target_string[i])
			else:
				t = 1
				target= int(target_string[-1-i])
			# "measures" each qubit to the specified value
			system= system.controlled_measurement(t, target)
		return system
 
	def entanglement(self, second_qubit):
		### Entangle this qubit with another ###
		# entangles with qubits from this system on the left, and qubits from the other system on the right
		output_probabilites = []
		for i in self.data:
			for j in second_qubit.data:
				output_probabilites.append(i * j)
		output_size = [1, self.rows* second_qubit.rows]
		return QubitSystem(output_size, output_probabilites)


class QuantumGate(Matrix):
	### Subclass for quantum gates, extending off the Matrix class ###

	def __init__(self, size, raw_data):
		### Initialises an instance of a matrix when being created ###
		# size in a [x, y] form to be accessed
		# data in just one list to be fed in to be put into the matrix
		self.collumns = size[0]
		self.rows = size[1]
		condition_one = is_power_of_two(self.rows)
		condition_two = self.rows == self.collumns
		# checks that it is a valid quantum gate to be made
		if condition_one and condition_two:
			self.data = raw_data
			self.initialise()
			condition_three = self.is_unitary()
			if condition_three:
				pass
			else:
				# stops the class being made
				raise(Exception("That was not a valid quantum gate that could be made."))
		else:
			# stops the class being made
			raise(Exception("That was not a valid quantum gate that could be made."))

	def _repr_(self):
		### Overwriting the repr function for a string representation of the Qubit gate ###
		return f"A Quantum Gate of size {self.collumns} with etries {self.data}."

	def is_unitary(self):
		### Calculates the hermitian adjoint and the inverse and compares them, if they are the same then the gate is unitary ###
		hermitian_data = []
		for i in self.transposed:
			# constructs the hermitian adjoint
			for j in i:
				c = con(j)
				hermitian_data.append(c)
		self.inverse()
		# gets the data of the inverse of the gate
		inverse_data = self.inv.data
		for i in range(len(hermitian_data)):
			# compares the two sets of data to see if they're the same
			if round(hermitian_data[i], 3) == round(inverse_data[i], 3):
				pass
			else:
				return False
		return True


class IrrationalNumber:
	### Class for Irrational Numbers ###

	def __init__(self, coefficient, radicand):
		### Initialsies a irational number, storing the coefficient, radicand and if it is imaginary ###
		self.coefficient = coefficient
		self.radicand = radicand
		if self.radicand < 0:
			self.imaginary = True
		else:
			self.imaginary = False

	def __repr__(self):
		### Overwriting the repr function so that you can get an idea of what is going on with the number more easily ###
		return f"an irrational number of magnitude {self.absoulute_value()}"

	def _str_(self):
		### Creates a string representation for the irrational number taking into account all of the different kinds of irrational it could be ###
		if self.coefficient== 0 or self.radicand == 0:
			return "0"
		elif self.coefficient== 1:
			if self.radicand == 1:
				coefficient = "1"
			else:
				coefficient = ""
		elif self.coefficient == - 1:
			if self.radicand == 1:
				coefficient= "-1"
			else:
				coefficient = "-"
		else:
			coefficient= self.coefficient
		if self.imaginary:
			if self.radicand == - 1:
				return f"{coefficient}i"
			else:
				return f"{coefficient}i√{ - self.radicand}"
		else:
			if self.radicand == 1:
				return f"{coefficient}"
			else:
				return f"{coefficient}v{self.radicand}"

	def __mul__(self, x):
		### Overwrites multiplication between these irrational numbers and other possible datatypes ###
		if isinstance(x, IrrationalNumber):
			# for with other irrational numbers
			if self.radicand == x.radicand:
				# if they have the same base combine it
				c = self.coefficient * x.coefficient * self.radicand
				return IrrationalNumber(c, 1)
			else:
				# otherwise just perform a "naive" multiplication
				c = self.coefficient * x.coefficient
				r = self.radicand * x.radicand
				return IrrationalNumber(c, r)
		elif isinstance(x, ComplexNumber):
			# for with complex numbers
			return ComplexNumber([self * i for i in x.values])
		elif isinstance(x, int) or isinstance(x, float):
			# with intgers or floats
			c = self.coefficient * x
			return IrrationalNumber(c, self.radicand)
		else:
			raise(Exception("That was not a valid datatype for this operation."))

	def __rmul__(self, x):
		### Incase multiplication is tried with an integer or float on the other side ###
		if isinstance(x, int) or isinstance(x, float):
			c = self.coefficient * x
			return IrrationalNumber(c, self.radicand)
		else:
			raise(Exception("That was not a valid datatype for this operation."))

	def __truediv__(self, x):
		### Overwrites division between these irrational numbers and other datatypes ###
		if isinstance(x, IrrationalNumber):
			# for with other irrational numbers
			if self.radicand == x.radicand:
				# if they have the same base remove it
				c = self.coefficient/ x.coefficient
				return IrrationalNumber(c, 1)
			else:
				# otherwise just perform "naive" division
				c = self.coefficient/ x.coefficient
				r = self.radicand / x.radicand
				return IrrationalNumber(c, r)
		elif isinstance(x, ComplexNumber):
			multiplyer = x.conjugate()
			bottom = IrrationalNumber((x * multiplyer).abs(), 1)
			c = self / bottom
			return c * multiplyer
		elif isinstance(x, int) or isinstance(x, float):
			# for with an integer or float
			c =self.coefficient/ x
			return IrrationalNumber(c, self.radicand)
		else:
			raise(Exception("That was not a valid datatype for this operation."))

	def __rtruediv__(self, x):
		### In case it is wanted to divide by an irrational number instead ###
		if isinstance(x, int) or isinstance(x, float):
			c = x /(self.coefficient* self.radicand)
			return IrrationalNumber(c, self.radicand)
		else:
			raise(Exception("That was not a valid datatype for this operation."))

	def __add__(self, x):
		### Overwrites addition between irrational and other types of number ###
		if isinstance(x, IrrationalNumber):
			# when adding two irrational numbers
			if self.radicand == x.radicand:
				# if they have the same base then they can be added
				c =self.coefficient+ x.coefficient
				return IrrationalNumber(c, self.radicand)
			else:
				# otherwise they form a complex number
				return ComplexNumber([self, x])
		elif isinstance(x, ComplexNumber):
			# for adding compex numbers
			v = x.values
			v.append(self)
			return ComplexNumber(v)
		elif isinstance(x, int) or isinstance(x, float):
			# for adding integers / floats
			if self.radicand == 1:
				c =self.coefficient + x
				return IrrationalNumber(c, 1)
			else:
				return ComplexNumber([self, IrrationalNumber(x,1)])
		else:
			raise(Exception("That was not a valid datatype for this operation."))

	def __radd__(self, x):
		### In case an integer or float is tried to be added on the other side of the irrational number ###
		if isinstance(x, int) or isinstance(x, float):
			if self.radicand == 1:
				c = self.coefficient+ x
				return IrrationalNumber(c, 1)
			else:
				return ComplexNumber([self, IrrationalNumber(x,1)])
		else:
			raise(Exception("That was not a valid datatype for this operation."))

	def __sub__(self, x):
		### Overwrites subtraction between irrational numbers ###
		if isinstance(x, IrrationalNumber):
			if self.radicand == x.radicand:
				# if they have the same base then they can be subtraced as normal
				c = self.coefficient - x.coefficient
				return IrrationalNumber(c, self.radicand)
			else:
				# otherwise they form a complex number
				return ComplexNumber([self, IrrationalNumber( - x.coefficient, x.radicand)])
		elif isinstance(x, ComplexNumber):
			# for subtracting a complex number
			v = [self]
			for i in x.values:
				v.append(IrrationalNumber( - i.coefficient, i.radicand))
			return ComplexNumber(v)
		elif isinstance(x, int) or isinstance(x, float):
			# when subtracting an intger or a float
			if self.radicand == 1:
				c = self.coefficient - x
				return IrrationalNumber(c, 1)
			else:
				return ComplexNumber([self, IrrationalNumber( -x, 1)])
		else:
			raise(Exception("That was not a valid datatype for this operation"))

	def __rsub__(self, x):
		### Incase an integer or float is to be subtracted from ###
		if isinstance(x, int) or isinstance(x, float):
			if self.radicand == 1:
				c = x - self.radicand
				return IrrationalNumber(c, 1)
			else:
				return ComplexNumber(IrrationalNumber(x, 1), IrrationalNumber( - self.coefficient, self.radicand))
		else:
			raise(Exception("That was not a valid datatype for this operation."))

	def __round__(self, n):
		### Allows rounding of irrational numbers to get an approximate value ###
		if self.imaginary:
			a = round((abs(self.absoulute_value())) ** 0.5, n)
			if self.coefficient < 0:
				a = -a
			return IrrationalNumber(a, -1)
		else:
			a = round((self.absoulute_value()) ** 0.5, n)
			if self.coefficient< 0:
				a= -a
			return a

	def __pow__(self, n):
		### Allows you to raise irrational number to powers ###
		if isinstance(n, int):
			if n % 2 == 1:
				c = IrrationalNumber((self.coefficient ** n) * (self.radicand ** (n//2)), self.radicand)
			else:
				c = (self.coefficient** n) * (self.radicand ** (n//2))
			return c
		elif isinstance(n, float):
			if not self.imaginary:
				return (self.absoulute_value() ** 0.5) ** n
			else:
				raise(Exception("That was not a valid datatype for this operation."))
		else:
			raise(Exception("That was not a valid datatype for this operation."))

	def __eq__(self, n):
		### Overwrites equality for Irrational Numbers ###
		if isinstance(n, IrrationalNumber):
			# with other irrational numbers
			if self.coefficient== 0 and n.coefficient == 0:
				return True
			else:
				x = round(self, 10)
				y = round(n, 10)
				if isinstance(x, IrrationalNumber):
					if isinstance(y, IrrationalNumber):
						return x.coefficient == y.coefficient and x.radicand == y.radicand
					else:
						return False
				else:
					if isinstance(y, IrrationalNumber):
						return False
					else:
						return x == y
		elif isinstance(n, ComplexNumber):
			# with complex numbers
			x = round(n, 10)
			if isinstance(x, ComplexNumber):
				return False
			else:
				return x[0] == self
		elif isinstance(n, int) or isinstance(n, float):
			# with integers and floats
			if self.coefficient== 0 and n == 0:
				return True
			else:
				if self.imaginary:
					return False
				else:
					return self.absoulute_value() == n
		else:
			return False

	def __gt__(self, n):
		### Overwrites the greater than operator ###
		if isinstance(n ,IrrationalNumber):
			if self.absoulute_value() > n.absoulute_value():
				return True
			else:
				return False
		elif isinstance(n, ComplexNumber):
			if self.absoulute_value() > (n.abs() ** 2):
				return True
			else:
				return False
		elif isinstance(n, int) or isinstance(n, float):
			if self.absoulute_value() > n * n:
				return True
			else:
				return False
		else:
			raise(Exception("Those were not valid datatypes for this operator."))

	def __lt__(self, n):
		### Overwrites the less than operator ###
		if isinstance(n ,IrrationalNumber):
			if self.absoulute_value() < n.absoulute_value():
				return True
			else:
				return False
		elif isinstance(n, ComplexNumber):
			if self.absoulute_value() < (n.abs() ** 2):
				return True
			else:
				return False
		elif isinstance(n, int) or isinstance(n, float):
			if self.absoulute_value() < n * n:
				return True
			else:
				return False
		else:
			raise(Exception("Those were not valid datatypes for this operator."))

	def absoulute_value(self):
		### Aids in calculating the absolute value of complex numbers ###
		if self.imaginary:
			return self.coefficient* self.coefficient* self.radicand * - 1
		else:
			return self.coefficient* self.coefficient* self.radicand


class ComplexNumber:
	### A class for Complex Numbers (or just numbers that are sums of multiple different irrational numbers) ###

	def __init__(self, values, sorted=False):
		### Initialises the complex number with the list of irrational numbers that are being summed together ###
		if not sorted:
			# values are ordered on radicand descending if they're not inputted in order
			values = self.sort(values)
			if values==[]:
				values= [IrrationalNumber(0, 1)]
		self.values= values
		self.radicands = []
		for i in self.values:
			self.radicands.append(i.radicand)
		
	def __repr__(self):
		### Overwriting the repr function to make things more obvious when used ###
		return f"a complex number adding {len(self.values)} irrational numbers"

	def __str__(self):
		### Overwrites the string function to allow for nice representations of your complex numbers ###
		string = ""
		for i in self.values:
			s = str(i)
			if string == "":
				string += s
			elif i.coefficient > 0:
				string += f" + {s}"
			elif i.coefficient < 0:
				string += f" {s}"
		return string
		
	def __mul__(self, x):
		### Multiplies a complex number with other numnbers ###
		if isinstance(x, ComplexNumber):
			# with other complex numbers
			output = []
			for i in self.values:
				# cycles through each number in the first list
				to_add = []
				for j in x.values:
					# multiplies each number in the second list by a number in the first and then adds that to the current output 
					to_add.append(i * j)
				if output == []:
					output = ComplexNumber(to_add)
				else:
					output = output + ComplexNumber(to_add)
			return output
		elif isinstance(x, IrrationalNumber) or isinstance(x, int) or isinstance(x, float):
			# if multiplication with an irrational number or integer or float is wanted
			return ComplexNumber([i * x for i in self.values])
		else:
			raise(Exception("That was not a valid datatype for this operation."))

	def __rmul__(self, x):
		### To allow for multiplication with integers from the other side ###
		if isinstance(x, int) or isinstance(x, float):
			return ComplexNumber([i * x for i in self.values])
		else:
			raise(Exception("That was not a valid datatype for this operation."))

	def __truediv__(self, x):
		### For division between complex numbers ###
		if isinstance(x, ComplexNumber):
			# considers it like a fraction, and multiplys the bottom and top by the conjugate of what is on the bottom
			# this turns the bottom into a real number that can be easily divided by
			# and so you calculate the multiplication for the top of the fraction and then divide in to each value by what is left on the bottom
			multiplyer = x.conjugate()
			top = self * multiplyer
			bottom = x * multiplyer
			divisor = IrrationalNumber(bottom.abs(), 1)
			output = ComplexNumber([i / divisor for i in top.values])
			return output
		elif isinstance(x, IrrationalNumber) or isinstance(x, int) or isinstance(x, float):
			# for dividing by an irration, integer or float
			return ComplexNumber([i / x for i in self.values])
		else:
			raise(Exception("That was not a valid datatype for this operation."))
	
	def __rtruediv__(self, x):
		### To allow for truedivision by a complex number ###
		if isinstance(x, int) or isinstance(x, float):
			multiplyer = self.conjugate()
			bottom= IrrationalNumber((self * multiplyer).abs(), 1)
			c = x / bottom
			return c * multiplyer
		else:
			raise(Exception("That was not a valid datatype for this operation."))
	
	def __add__(self, x):
		### Adds a complex number to another number ###
		if isinstance(x, ComplexNumber):
			# functions similar to a merge sort
			# in that since the numbers in both lists are already sorted you add the larger of the two at the front of the lists
			# then move along to the next one in that list and work your way through
			# and if you come across two of the same radicand then they will be added properly along the way
			pointer_one = 0
			pointer_two = 0
			output = []
			while pointer_one < len(self.values) and pointer_two < len(x.values):
				if self.radicands[pointer_one] > x.radicands[pointer_two]:
					# if the current values in the first complex number is larger add that next
					output.append(self.values[pointer_one])
					pointer_one += 1
				elif self.radicands[pointer_one] < x.radicands[pointer_two]:
					# otherwise if the value from the second list is larger, add that
					output.append(x.values[pointer_two])
					pointer_two += 1
				elif self.radicands[pointer_one] == x.radicands[pointer_two]:
					# if they're the same add them, and then add them to the list
					output.append(self.values[pointer_one] +
					x.values[pointer_two])
					pointer_one += 1
					pointer_two += 1
			if pointer_one == len(self.values):
				while pointer_two < len(x.values):
					# if there are still values left in the second list
					output.append(x.values[pointer_two])
					pointer_two += 1
			elif pointer_two == len(x.values):
				while pointer_one < len(self.values):
					# if there are still values left in the first list
					output.append(self.values[pointer_one])
					pointer_one += 1
			return ComplexNumber(output)
		elif isinstance(x, IrrationalNumber):
			# to add an irrational number to your complex number
			v = self.values
			v.append(x)
			return ComplexNumber(v)
		elif isinstance(x, int) or isinstance(x, float):
			# to add a float or intger to your complex number
			v = self.values
			v.append(IrrationalNumber(x, 1))
			return ComplexNumber(v)
		else:
			raise(Exception("That was not a valid datatype for this operation."))
	
	def __radd__(self, x):
		### In case an integer or float is added from the left instead of the right ###
		if isinstance(x, int) or isinstance(x, float):
			v = self.values
			v.append(IrrationalNumber(x, 1))
			return ComplexNumber(v)
		else:
			raise(Exception("That was not a valid datatype for this operation."))
	
	def __sub__(self, x):
		### Allows for subtraction from complex numbers ###
		if isinstance(x, ComplexNumber):
			# for subtraction between complex numbers, using the add method, but reversing the sign for the coefficients of each number that is being subtracted
			to_subtract = []
			for i in x.values:
				to_subtract.append(IrrationalNumber( - i.coefficient, i.radicand))
			return self+ ComplexNumber(to_subtract)
		elif isinstance(x, IrrationalNumber):
			# for subtraction of an irrational number from a complex number
			v = self.values
			v.append(IrrationalNumber( - x.coefficient, x.radicand))
			return ComplexNumber(v)
		elif isinstance(x, int) or isinstance(x, float):
			# for subtraction of a float or integer from a complex number
			v = self.values
			v.append(IrrationalNumber( - x, 1))
			return ComplexNumber(v)
		else:
			raise(Exception("That was not a valid datatype for this operation."))
	
	def __rsub__(self, x):
		### To allow for subtraction by a complex number ###
		if isinstance(x, int) or isinstance(x, float):
			v = [IrrationalNumber(x, 1)]
			for i in self.values:
				v.append(IrrationalNumber( - i.coefficient, i.radicand))
			return ComplexNumber(v)
		else:
			raise(Exception("That was not a valid datatype for this operation."))
	
	def __pow__(self, x):
		### To allow you to raise complex numebrs to powers ###
		if isinstance(x, int):
			C = 1
			for i in range(x):
				c = c * self
			return c
		else:
			raise(Exception("That was not a valid datatype for this operation."))

	def __round__(self, n):
		### To round complex numbers to get approximate values for them ###
		r = 0
		c = IrrationalNumber(0, -1)
		for i in self.values:
			if i.radicand > 0:
				r = r + round(i, n)
			else:
				c = c + round(i, n)
		if r == 0 and c.coefficient == 0:
			return 0
		elif r == 0:
			return c
		elif c.coefficient == 0:
			return r
		else:
			return ComplexNumber([IrrationalNumber(r, 1), c])
	
	def __eq__(self, n):
		### Overwrites the euqality operator for Complex Numbers ###
			if isinstance(n, ComplexNumber):
				# with other complex numbers
				x = round(self, 10)
				y = round(n, 10)
				if isinstance(x, ComplexNumber):
					if isinstance(y, ComplexNumber):
						return x.values[0] == y.values[0] and x. values[1] == y.values[1]
					else:
						return False
				elif isinstance(x, IrrationalNumber):
					if isinstance(y, IrrationalNumber):
						return x == y
					else:
						return False
				else:
					return x == y
			elif isinstance(n, IrrationalNumber):
				# with irrational numbers
				x = round(self, 10)
				y = round(n, 10)
				if isinstance(x, ComplexNumber):
					return False
				else:
					return x == y
			elif isinstance(n, int) or isinstance(n, float):
				# with intgers and floats
				x = round(self, 10)
				y = round(n, 10)
				if isinstance(x, ComplexNumber) or isinstance(x, IrrationalNumber):
					return False
				else:
					return x == y
			else:
				return False
		
	def __gt__(self, n):
		### Overwrites the greater than operator ###
		if isinstance(n ,ComplexNumber):
			# with other complex numbers
			if self.abs()> n.abs():
				return True
			else:
				return False
		elif isinstance(n, IrrationalNumber):
			# with irrational numbers
			if (self.abs()** 2) > n.absoulute_value():
				return True
			else:
				return False
		elif isinstance(n, int) or isinstance(n, float):
			# with integers and floats
			if self.abs()> n:
				return True
			else:
				return False
		else:
			raise(Exception("Those were not valid datatypes for this operator."))
		
	def __lt__(self, n):
		### Overwrites the less than operator ###
		if isinstance(n ,ComplexNumber):
			# with other complex numebrs
			if self.abs()< n.abs():
				return True
			else:
				return False
		elif isinstance(n, IrrationalNumber):
			# with irrational numbers
			if (self.abs()** 2) < n.absoulute_value():
				return True
			else:
				return False
		elif isinstance(n, int) or isinstance(n, float):
			# with intgers and floats
			if self.abs()< n:
				return True
			else:
				return False
		else:
			raise(Exception("Those were not valid datatypes for this operator."))
		
	def abs(self):
		### Calculated the absolute value of a complex number ###
		# allowing you to get an exact value if working with a non-imaginary number
		# or to get the magnitude of one that is imaginary
		square = 0
		for i in self.values:
			square += i.absoulute_value()
		absoulute_value = square** 0.5
		return absoulute_value
			
	def conjugate(self):
		### Returns the complex conjugate for the complex number ###
		# just returns itself if it has no imaginary parts
		conjugate_values = []
		for i in self.values:
			if i.imaginary:
				conjugate_values.append(IrrationalNumber( -i.coefficient, i.radicand))
			else:
				conjugate_values.append(i) 
		return ComplexNumber(conjugate_values)

	def sort(self, list):
		### A merge sort to make sure that the irrational numbers coming in are in order for proper use in the program ###
		if len(list) == 1:
			# base step
			if isinstance(list[0], IrrationalNumber):
				return list
			else:
				return [IrrationalNumber(list[0], 1)]
		else:
			# recursive step
			mid = len(list) // 2
			# break it down to two smaller lists
			list_one = list[:mid]
			list_two = list[mid:]
			# sort those
			list_one = self.sort(list_one)
			list_two = self.sort(list_two)
			output_list = []
			while len(list_one) > 0 and len(list_two) > 0:
				# add them back together
				if list_one[0].radicand == 0 or list_one[0].coefficient == 0:
					list_one.pop(0)
				elif list_two[0].radicand == 0 or list_two[0].coefficient == 0:
					list_two.pop(0)
				elif list_one[0].radicand >= list_two[0].radicand:
					# if the larger is in the first list
					output_list.append(list_one.pop(0))
				elif list_one[0].radicand < list_two[0].radicand:
					# if the larger is in the second list
					output_list.append(list_two.pop(0))
				elif list_one.radicand == list_two.radicand:
					x = list_one.pop(0) + list_two.pop(0)
					output_list.append(x)
			if len(list_one) == 0:
				# if there were more in list two
				for i in list_two:
					output_list.append(i)
			elif len(list_two) == 0:
				# if there were more in list one
				for i in list_one:
					output_list.append(i)
			return output_list


def identity(size):
	### A function to generate an identity matrix of any size ###

	id = [1]
	for i in range(size):
		for j in range(size):
			id.append(0)
		id.append(1)
	return Matrix([size, size], id)
 
def is_power_of_two(x):
	### Checks if a number is a power of two (for use checking if qubits and quantum gates can be created) ###
	if x == 1:
		return True
	elif x < 1:
		return False
	else:
		y = x / 2
	return is_power_of_two(y)
 
def power_of_two(x, n=0):
	### Gives the power that two is raised to to get x ###
	if x == 1:
		return n
	else:
		n += 1
		y = x // 2
	return power_of_two(y, n)
 
def binary(x, size):
	### Takes a number in base 10 and the binary length that it needs to be and then returns that number in binary as a string of the required length ###
	binary_output = ""
	for i in range(1, size + 1):
		if x - (2 ** (size - i)) >= 0:
			binary_output += "1"
			x -= (2 ** (size - i))
		else:
			binary_output += "0"
	return binary_output

def con(z):
	### Allows for conjugate to be called on a number without knowing if it is complex, irrational or not ###
	try:
		c = z.conjugate()
	except:
		try:
			is_imaginary = z.imaginary
			if is_imaginary:
				c = IrrationalNumber( - z.coefficient, z.radicand)
			else:
				c = z
		except:
			c = z
	return c
	
def probability(n):
	### Returns the probability a value from a vector in a qubit system represents ###
	if isinstance(n, ComplexNumber):
		return (n.abs()) ** 2
	elif isinstance(n, IrrationalNumber):
		return n.absoulute_value()
	else:
		return n ** 2
 
def arctan(z):
	### For calculating values of arctan using Euler's infinite series ### 
	'''
	This produced the ANGLES list in this program along with this little bit of code:

	angles=[]
	for i in range(1, 65):
		z = (2 ** (-i))
		angles.append(arctan(z))
	print(angles)
	'''
	multiplyer = z / (1 + z * z)
	sum = 0
	for n in range(100):
		product = 1
		for k in range(1, n + 1):
			product = product* ((2 * k * z) / (2 * k + 1)) * multiplyer
		sum += product
	return multiplyer * sum
	
def cordic(theta):
	### The algorithm that actually does the trigonometric legwork to calculate sine, cosine and tan ###
	# initialises at π/4 with coordinates (1, 1)
	coordinates = [1, 1]
	current_angle = 0.78539816339744831
	for i in range(len(ANGLES)):
		if theta > current_angle:
			# if you need to add to get to the desired angle
			new_coordinates = [coordinates[0] - (coordinates[1]*(0.5**(i+1))), coordinates[1] + (coordinates[0]*(0.5**(i+1)))]
			current_angle += ANGLES[i]
		elif theta < current_angle:
			# if you need to subtract to get to the desired angle
			new_coordinates = [coordinates[0] + (coordinates[1]*(0.5**(i+1))), coordinates[1] - (coordinates[0]*(0.5**(i+1)))]
			current_angle -= ANGLES[i]
		else:
			# if you make it to the desired angle early
			break
		coordinates = new_coordinates
	hypotenuse = (coordinates[0]**2 + coordinates[1]**2)**0.5
	return coordinates[0], coordinates[1], hypotenuse, current_angle

def sine(theta):
	### For sin of an angle ###
	if theta < 0:
		a = -theta
		negative = True
	else:
		a = theta
		negative = False
	while a > 2 * PI:
		a = a - (2 * PI)
	if a <= (PI / 2):
		dimensions = cordic(a)
		if negative:
			return - dimensions[1] / dimensions[2]
		else:
			return dimensions[1] / dimensions[2]
	elif a <= PI:
		a = PI - a
		dimensions = cordic(a)
		if negative:
			return - dimensions[1] / dimensions[2]
		else:
			return dimensions[1] / dimensions[2]
	elif a <= ((3 * PI)/ 2):
		a = a - PI
		dimensions = cordic(a)
		if negative:
			return dimensions[1] / dimensions[2]
		else:
			return - dimensions[1] / dimensions[2]
	else:
		a = 2 * PI - a
		dimensions = cordic(a)
		if negative:
			return dimensions[1] / dimensions[2]
		else:
			return - dimensions[1] / dimensions[2]
	
def cosine(theta):
	### For cos of an angle ###
	if theta < 0:
		a = -theta
	else:
		a = theta
	while a > 2 * PI:
		a = a - (2 * PI)
	if a <= (PI / 2):
		dimensions = cordic(a)
		return dimensions[0] / dimensions[2]
	elif a <= PI:
		a = PI - a
		dimensions = cordic(a)
		return - dimensions[0] / dimensions[2]
	elif a <= ((3 * PI)/ 2):
		a = a - PI
		dimensions = cordic(a)
		return - dimensions[0] / dimensions[2]
	else:
		a = 2 * PI - a
		dimensions = cordic(a)
		return dimensions[0] / dimensions[2]

def tangent(theta):
	### For tan of an angle ###
	if theta < 0:
		a = -theta
		negative = True
	else:
		a = theta
		negative = False
	while a > 2 * PI:
		a = a - (2 * PI)
	if a <= (PI / 2):
		dimensions = cordic(a)
		if negative:
			return - dimensions[1] / dimensions[0]
		else:
			return dimensions[1] / dimensions[0]
	elif a <= PI:
		a = PI - a
		dimensions = cordic(a)
		if negative:
			return dimensions[1] / dimensions[0]
		else:
			return - dimensions[1] / dimensions[0]
	elif a <= ((3 * PI)/ 2):
		a = a - PI
		dimensions = cordic(a)
		if negative:
			return - dimensions[1] / dimensions[0]
		else:
			return dimensions[1] / dimensions[0]
	else:
		a = 2 * PI - a
		dimensions = cordic(a)
		if negative:
			return dimensions[1] / dimensions[0]
		else:
			return - dimensions[1] / dimensions[0]
		
def pauli_x():
	### Creates a pauli x gate ###
	return QuantumGate([2, 2], [0, 1, 1, 0])
		
def pauli_y():
	### Creates a pauli y gate ###
	return QuantumGate([2, 2], [0, IrrationalNumber(-1, -1), IrrationalNumber(1, -1), 0])

def pauli_z():
	### Creates a pauli z gate ###
	return QuantumGate([2, 2], [1, 0, 0, -1])
 
def hadamard():
	### Creates a hadamard gate ###
	return QuantumGate([2, 2], [IrrationalNumber(1, 0.5), IrrationalNumber(1, 0.5), IrrationalNumber(1, 0.5), IrrationalNumber(-1, 0.5)])
 
def phase():
	### Creates a phase shift gate ###
	return QuantumGate([2, 2], [1, 0, 0, IrrationalNumber(1, -1)])
 
def pi_by_eight():
	### Creates a π/8 gate ###
	return QuantumGate([2, 2], [1, 0, 0, ComplexNumber([IrrationalNumber(cosine(PI / 4), 1), IrrationalNumber(sine(PI / 4), -1)])])

def x_rotation(theta):
	### Creates a gate for rotation about the x axis about angle theta ###
	angle = theta / 2
	return QuantumGate([2, 2], [cosine(angle), IrrationalNumber(-sine(angle), -1), IrrationalNumber(-sine(angle), -1), cosine(angle)])

def y_rotation(theta):
	### Creates a gate for rotation about they axis about angle theta ###
	angle = theta / 2
	return QuantumGate([2, 2], [cosine(angle), -sine(angle), sine(angle), cosine(angle)])

def z_rotation(theta):
	### Creates a gate for rotation about the z axis about angle theta ###
	angle = theta / 2
	return QuantumGate([2, 2], [ComplexNumber([IrrationalNumber(cosine(angle), 1), IrrationalNumber( - sine(angle), -1)]), 0, 0, ComplexNumber([IrrationalNumber(cosine(angle), 1), IrrationalNumber(sine(angle), -1)])])

def swap():
	### Creates a swap gate ###
	return QuantumGate([4, 4], [1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1])

def control(control_bits, gate):
	### Creates a control gate of the inputted gate on a given number of control bits ###
	i = identity(2 ** control_bits)
	length= (2 ** control_bits) + gate.rows
	extra_one = [0 for j in range(gate.rows)]
	extra_two = [0 for j in range(2 ** control_bits)]
	data = []
	for j in i.matrix:
		row = j + extra_one
		data += row
	for j in gate.matrix:
		row = extra_two + j
		data += row
	return QuantumGate([length, length], data)

