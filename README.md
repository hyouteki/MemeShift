# MemeShift
**A image segmenting program built on Python using mean shift algorithm. [Image segmentation](https://en.wikipedia.org/wiki/Image_segmentation) is the process of partitioning a digital image into multiple image segments, also known as image regions or image objects**

### Sample images (original vs segmented)

<kbd> 
<img src="https://github.com/Hyouteki/MemeShift/blob/main/dump/original.png" width="512" height="384"> 
</kbd> <kbd> 
<img src="https://github.com/Hyouteki/MemeShift/blob/main/dump/segmented.jpg" width="512" height="384">
</kbd>

### Contents
- [Code explanation](#code-explanation)
- [Mean shift class overview](#mean-shift-class-overview)
- [How to use](#how-to-use)
- [License](#license)

## Code explanation
Mean shift algorithm works in the infinite cycle of 6 steps, until all the data points has been labeled.

### Step-1 :: Initialize the centroid with a random unlabel data point
``` Python
this.__centroid = this.__getUnlabeledDataPoint()

def __getUnlabeledDataPoint(this) -> Point:
    for point in this.data:
        if point.label != MeanShift.blocked:
            return point
     return None
```

### Step-2 :: Mark all the points as members that are within the bandwidth amount of distance from the cluster centroid which are not blocked from the computation. And clear the old members(if any).
``` Python
this.__makeMember()

def __makeMember(this) -> None:
    this.__members.clear()
    for i in range(len(this.data)):
        point: Point = this.data[i]
        if point.label != MeanShift.blocked:
            if Point.distance(this.__centroid, point) < this.bandwidth:
                this.__members.append(i)
```

### Step-3 :: Shift the centroid to the mean of all the members of that cluster.
``` Python
this.__shiftCentroid()

def __shiftCentroid(this) -> None:
    junk: list = numpy.zeros(this.dim)
    for member in this.__members:
        trash: Point = this.data[member]
        junk = [junk[i]+trash.point[i] for i in range(this.dim)]
    junk = [junk[i]/len(this.__members) for i in range(this.dim)]
    this.__centroid = Point(this.dim)
    this.__centroid.setPoint(junk)
```

### Step-4 :: Check for convergence. That is if the old centroid is almost same as the new centroid.
``` Python

if (numpy.allclose(centroidPre, centroidPost)):
    this.__assignMembership()
    if (this.debug):
        print(colored(f"[debug] itr number :: {this.__iterationNumber}", "yellow"))
    break
```

### Step-5 :: If convergence has been reached. Block all the final members of the clusters and assign them the value of the centroid. And increament the iteration number.
``` Python
this.__assignMembership()

def __assignMembership(this) -> None:
    for member in this.__members:
        point: Point = this.data[member]
        this.data[member].setLabel(MeanShift.blocked)
        point.setPoint(this.__centroid.point)
    this.__iterationNumber += 1
```

### Step-6 :: If convergence has not been reached. Then redo the steps from Step-1 to Step-4.

Break from the code when all the data points has been labeled or the max number of iterations has been reached. And return the new segmented data points.

## Mean shift class overview

### Variables
``` Python
# Public variables

this.debug = False
"""contains the debug instance"""

this.dim = -1
"""dimension / number of features"""

this.bandwidth = bandwidth
"""bandwidth / radius of neighbourhood"""

this.data: list[Point] = []
"""sample data in custom Point format"""

this.rawData: list[list[float]] = []
"""raw data in the matrix form"""

# Private variables

this.__iterationNumber = 0
"""current iteration number / current centroid number"""

this.__centroid: Point = None
"""centroid of current cluster"""

this.__members: list[int] = []
"""list of indices of members"""
```

### Methods
``` Python
# Public methods

initRawData(this, dump: list[list[int]]) -> None
"""Initializes the data in the matrix form"""

initSampleData(this, dump: list[Point]) -> None
"""Initializes the data in the custom Point format"""

doTheJob(this) -> None
"""Main  function; does the job"""

# Private methods

__normalize(this) -> None
"""Normalizes the data by dividing every feature vector by their max value"""

__getUnlabeledDataPoint(this) -> Point
"""Returns a random unlabeled data point"""

__assignMembership(this) -> None
"""Assign membership of the current cluster to all the members"""

__shiftCentroid(this) -> None
"""Shifts centroid to the mean of all the members"""

__preprocess(this, dump: list[list[float]]) -> None
"""Preprocesses the data"""

__makeMember(this) -> None
"""Make all the non blocked data points; members that are within the bandwidth amount of distance"""
```

## How to use
- Clone the git file `git clone https://github.com/Hyouteki/MemeShift.git` or download the latest release.
- Type the following command `make install` to install all the necessary imports.
- Run the sample driver code by `make doTheJob` [case-sensitive].
- To segment a custom image replace the following path with your custom image path in driver.py file; line number 8
``` Python
image = cv2.imread("dump/original.png")
```
- **P.S. It will take around 10-15 minutes to finish segmenting**.

## License
``` Markdown
MIT License

Copyright (c) 2023 Lakshay

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation 
files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, 
modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software 
is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES 
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE 
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR 
IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```
