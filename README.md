This is a rework of 'Resistor ratio matcher.py' - the initial iteration of 'resistor_ratio_match_v2.py'. I reworked it to submit as an assignment for a class requiring proof of basic Python knowledge.
As for why I chose the initial over the (possibly) improved v2, this version:
  - Existed within one file (the code needed to be copied to a text document for submission)
  - I honestly forgot two versions existed.

So here I am, a couple hours of work later, and satisfied with the performance of the reworked v1.

Details on the usage head the .py file, but the short of it is:
  1. Voltage divider design requires for you to choose one resistor's value and calculate the other
  2. The other resistor's value likely won't lie on (or even particularly close to) a standard E Series value
  3. This program optimizes both variables (R1 and R2) to get as close to the desired Vout/Vin ratio as possible

Use to your hearts content. Don't kill anyone though. Voltage dividers are meant for good.

!! IMPORTANT !! : I'm a python beginner. Proceed with caution.
