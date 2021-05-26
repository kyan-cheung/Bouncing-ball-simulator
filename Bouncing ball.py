import numpy as np
import matplotlib.pyplot as plt

gravity = 9.81 #m/s^2
initialVelocity = 0 # m/s
initialHeight = 10 # m
COR = 0.9 # Coefficient of restitution
end = 20 # Right end of graph, in seconds

# Returns a quadratic function
def quadratic(x):
    return - (gravity * (x ** 2)) + initialVelocity * x + initialHeight

# Largest root of quadratic function
def findLargestRoot():
    return np.amax(np.roots([- gravity, initialVelocity, initialHeight]))

xAdjustment = 0 
x = []
y = []
loops = 0

def graphParabola(margin = -1):
    global x, y, firstRoot, secondRoot
    if margin < 0:
        margin = findLargestRoot()

    spacing = int(np.ceil(margin * 100000)) + 1 # Spaced such that there are at least 10000 points per second
    localx = np.linspace(0, margin, spacing, endpoint=True) # x starts at zero for every quadratic equation generated
    x.extend([i + xAdjustment for i in localx]) # Adjusts x to account for starting at origin
    y.extend([quadratic(i) for i in localx])

    # Log where the ball lands the first and second time
    if loops == 0:
        firstRoot = findLargestRoot()
    elif loops == 1:
        secondRoot = findLargestRoot()

while findLargestRoot() + xAdjustment < end: # While the next time the ball hits the ground is before the end of the graph
    graphParabola()
    
    rootDerivative = initialVelocity - 2 * findLargestRoot() * gravity # Derivative at root

    xAdjustment += findLargestRoot()
    initialVelocity = -rootDerivative * COR
    initialHeight = 0

    if findLargestRoot() < 10 ** -5: # Ball bounces too low
        x.append(end)
        y.append(0)
        break
    
    loops += 1

if len(x) > 0:
    if x[-1] != end:
        graphParabola(end - xAdjustment)
else:
    graphParabola(end - xAdjustment)

if COR >= 1:
    print("The ball never stops jumping.")
else:
    try:
        timeToStopBouncing = firstRoot + (secondRoot / (1 - COR))
    except NameError: # Ball never reaches ground
        rootDerivative = initialVelocity - 2 * findLargestRoot() * gravity
        initialVelocity = -rootDerivative * COR
        initialHeight = 0

        secondRoot = findLargestRoot()
        timeToStopBouncing = firstRoot + (secondRoot / (1 - COR))
    finally:
        print(f"Time for the ball to stop bouncing: {timeToStopBouncing} seconds")

fig = plt.figure()
plt.suptitle("Position-time graph of bouncing ball", fontweight = "bold")
ax = fig.add_subplot(111)

#Add titles and grid, set scientific notation
ax.set_xlabel("Time (s)")
ax.set_ylabel("Height (m)")
ax.grid(True)

ax.plot(x, y)
plt.show()