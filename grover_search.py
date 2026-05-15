from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
 
TARGET = '000'
SHOTS  = 1024
 
# create 3 qubits and 3 classical bits
qc = QuantumCircuit(3, 3)
 
# all qubits into superposition
qc.h([0, 1, 2])
qc.barrier()
 
# amount of iterations = pi/4 * sqrt(N))
for _ in range(2):
	# oracle
     # find the target state 
     qc.x([0, 1, 2]) # flip all bits to make |111> the target state
	qc.h(2)
	qc.ccx(0, 1, 2)  # troffi gate to flip the target state only will flip when |111> 
	qc.h(2)
     qc.x([0, 1, 2]) # flip all bits to make |111> the target state
 
	# diffuser 
     # amplify the target state
	qc.h([0, 1, 2]) # put all qubits into superposition
	qc.x([0, 1, 2]) # flip all bits to make |000> the target state
	qc.h(2)
	qc.ccx(0, 1, 2) # troffi gate to flip the |000> state only will flip when |000>
	qc.h(2)
	qc.x([0, 1, 2]) # reverse flip of all bits to restore original states
	qc.h([0, 1, 2]) # reverse superposition to amplify the target state
	qc.barrier()

#collapse the state to the target state
qc.measure([0, 1, 2], [0, 1, 2])
 


counts = AerSimulator().run(qc, shots=SHOTS).result().get_counts()
 
#print
print(f"\nSearching for: |{TARGET}> = decimal {int(TARGET, 2)}")
print("")
print(f"{'State':<8} {'Shots':>6}  {'Probability':>12}")
print("-" * 32)
for state, count in sorted(counts.items(), key=lambda x: -x[1]):
    marker = " <-- TARGET" if state == TARGET[::-1] else ""
    print(f"|{state}>  {count:>6}   {count/SHOTS:>10.1%}{marker}")