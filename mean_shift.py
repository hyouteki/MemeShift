import numpy
from ml_classes import Point
from termcolor import colored

class MeanShift:
    blocked: bool = True

    def __init__(this, bandwidth: int):
        this.debug = False

        this.dim = -1
        """dimension / number of features"""

        this.bandwidth = bandwidth
        """bandwidth / radius of neighbourhood"""

        this.data: list[Point] = []
        """sample data"""

        this.rawData: list[list[float]] = []
        """raw data"""

        this.__iterationNumber = 0
        """current iteration number / current centroid number"""

        this.__centroid: Point = None
        """centroid of current cluster"""

        this.__members: list[int] = []
        """list of indices of members"""

    def __normalize(this) -> None:
        max: list[float] = [1 for i in range(this.dim)]
        for point in this.rawData:
            for i in range(this.dim):
                if (point[i] > max[i]):
                    max[i] = point[i]
        dup: list[list[float]] = this.rawData.copy()
        for point in dup:
            point = [point[i]/max[i] for i in range(this.dim)]
        return dup

    def initRawData(this, dump: list[list[int]]) -> None:
        this.dim = len(dump[0])
        this.rawData = dump

    def initSampleData(this, dump: list[Point]) -> None:
        this.dim = dump[0].dim
        this.data = dump
        len: int = len(dump)

    def __getUnlabeledDataPoint(this) -> Point:
        for point in this.data:
            if point.label != MeanShift.blocked:
                return point
        return None

    def __assignMembership(this) -> None:
        for member in this.__members:
            point: Point = this.data[member]
            this.data[member].setLabel(MeanShift.blocked)
            point.setPoint(this.__centroid.point)
        this.__iterationNumber += 1

    def __shiftCentroid(this) -> None:
        junk: list = numpy.zeros(this.dim)
        for member in this.__members:
            trash: Point = this.data[member]
            junk = [junk[i]+trash.point[i] for i in range(this.dim)]
        junk = [junk[i]/len(this.__members) for i in range(this.dim)]
        this.__centroid = Point(this.dim)
        this.__centroid.setPoint(junk)

    def __preprocess(this, dump: list[list[float]]) -> None:
        this.data.clear()
        for junk in dump:
            point: Point = Point(this.dim)
            point.setPoint(junk)
            this.data.append(point)

    def __makeMember(this) -> None:
        this.__members.clear()
        for i in range(len(this.data)):
            point: Point = this.data[i]
            if point.label != MeanShift.blocked:
                if Point.distance(this.__centroid, point) < this.bandwidth:
                    this.__members.append(i)

    def doTheJob(this) -> None:
        if (this.dim == -1):
            print(colored("First initialize data", "red"))
            exit(1)
        normalizedData: list[list[float]] = this.__normalize()
        this.__preprocess(normalizedData)
        while True:
            this.__centroid = this.__getUnlabeledDataPoint()
            if (this.__centroid == None):
                break
            while True:
                this.__makeMember()
                centroidPre: list[float] = this.__centroid.point
                this.__shiftCentroid()
                centroidPost: list[float] = this.__centroid.point
                if (numpy.allclose(centroidPre, centroidPost)):
                    this.__assignMembership()
                    if (this.debug):
                        print(colored(f"[debug] itr number :: {this.__iterationNumber}", "yellow"))
                    break
