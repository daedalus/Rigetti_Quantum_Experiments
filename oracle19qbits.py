#!/usr/bin/env python
# Author Dario Clavijo 2018

from pyquil.quilatom import QubitPlaceholder
from pyquil.quil import Program,address_qubits
from pyquil.api import QVMConnection 
from pyquil.gates import CNOT, H,X,Z,MEASURE
from pyquil.api import get_devices, QPUConnection

for device in get_devices():
        if device.is_online():
                    print('Device {} is online'.format(device.name))

# this is the secret
s = int(b'001100110011001100',2) # 1110

class_readouts = [17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0]

qregs = QubitPlaceholder().register(18)
tmp = QubitPlaceholder().register(1)

prog = Program(X(tmp[0]))

prog += Program(H(tmp[0]))
for i in range(0,len(qregs)):
    prog += Program(H(qregs[i]))

# this is the oracle, think of it as a blackbo
for i in range(0,len(qregs)):
    if s & (1 << i):
        prog += Program(CNOT(qregs[i],tmp[0]))

prog += Program(H(tmp[0]))
for i in range(0,len(qregs)):
    prog += Program(H(qregs[i]))

for i in range(0,len(qregs)):
    prog += Program(MEASURE(qregs[i],i))

prog = address_qubits(prog)

print(prog)

print("Executing in the QVM")

qvm = QVMConnection() 

wf = qvm.wavefunction(prog)
print(wf)
print(wf.amplitudes)

results = qvm.run(prog, classical_addresses=class_readouts, trials=10)

for r in results:
    print r

print("Executing in the QPU")

acorn = get_devices(as_dict=True)['19Q-Acorn']

qpu = QPUConnection(acorn)
# The device name as a string is also acceptable
# qpu = QPUConnection('19Q-Acorn')

results = qpu.run(prog, classical_addresses=class_readouts, trials=10)

for r in results:
    print r

