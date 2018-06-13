# Senate-Bus-Python-Example

This is an example solution in Pythonfor the Senate Bus threading problem proposed by Allen B. Downey in his
book "Little Book of Semaphores" under the "Not Remotely Classical Problems" section. 

The problem goes as follows:

This problem was originally based on the Senate bus at Wellesley College. Riders come to a bus stop and wait
for a bus. When the bus arrives, all the waitingriders invoke boardBus, but anyone who arrives while the bus
is boarding has to wait for the next bus. The capacity of the bus is 50 people; if there are morethan 50
people waiting, some will have to wait for the next bus. When all the waiting riders have boarded, the bus
can invoke depart. If the bus arrives when there are no riders, it should depart immediately.

Puzzle: Write synchronization code that enforces all of these constraints.
