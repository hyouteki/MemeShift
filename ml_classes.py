import random


class Point:
    """Data point class"""
    def __init__(this, dim: int):
        """dim :: dimension of the point"""
        this.dim = dim
        this.label = None
        this.junk = None  # can be used to assign any value you like
        this.point: list = [0 for i in range(dim)]

    def setPoint(this, point: list):
        this.point = point

    def distanceTo(this, other) -> float:
        """Euclidean distance between two points"""
        sum = 0
        for i in range(this.dim):
            sum += (this.point[i] - other.point[i])**2
        return sum**(0.5)

    def setLabel(this, label: any):
        this.label = label

    def manhattanDistanceTo(this, other) -> float:
        """Manhattan distance between two points"""
        return sum([abs(this.point[i] - other.point[i]) for i in range(this.dim)])

    @classmethod
    def distance(this, point1, point2) -> float:
        """Euclidean distance between two points"""
        sum = 0
        for i in range(point1.dim):
            sum += (point1.point[i] - point2.point[i])**2
        return sum**(0.5)

    @classmethod
    def manhattanDistance(this, point1, point2) -> float:
        """Manhattan distance between two points"""
        return sum([abs(point1.point[i] - point2.point[i]) for i in range(point1.dim)])

    @classmethod
    def toMatrix(this, object) -> list[list[float]]:
        ret: list[list[float]] = []
        for point in object:
            ret.append(point.point)
        return ret

    @classmethod
    def toPointArray(this, points, matrix):
        ret: list = []
        dim: int = len(matrix[0])
        for i in range(len(points)):
            points[i].dim = dim
            points[i].setPoint(matrix[i])

    def __str__(this):
        return "{ Point: "+f"{this.point}, Label: {this.label}"+"}"

    def __repr__(this):
        return "{ Point: "+f"{this.point}, Label: {this.label}"+"}"


class Cluster:
    """Cluster class"""
    def __init__(this, id: int, dim: int):
        """
         id :: cluster id
        dim :: dimension of point
        """
        this.id = id
        this.dim = dim
        this.centroid: Point = Point(dim)
        this.members: list[Point] = []

    def randomizeCentroid(this):
        center: list = []
        for i in range(this.dim):
            center.append(random.randint(0, 1))
        this.centroid.setPoint(center)

    def addMember(this, member):
        this.members.append(member)

    def recomputeCentroid(this):
        this.centroid = Point(this.dim)
        for point in this.members:
            for i in range(this.dim):
                this.centroid.point[i] += point.point[i]
        for i in range(this.dim):
            this.centroid.point[i] /= this.dim

    def averagePoint(this) -> Point:
        point: list[float] = [0 for i in range(this.dim)]
        for trash in this.members:
            for i in range(this.dim):
                point[i] += trash.point[i]
        for i in range(this.dim):
            point[i] /= this.dim
        new: Point = Point(this.dim)
        new.setPoint(point)
        return new

    def doomsDay(this):
        this.members: list[Point] = []

    def __str__(this):
        return "{centroid: "+f"{this.centroid.point}"+", members: "+f"{this.members}"+"}"

    def __repr__(this):
        return "{centroid: "+f"{this.centroid.point}"+", members: "+f"{this.members}"+"}"


if (__name__ == "__main__"):
    cluster = Cluster(0, 2)
    print(f"Cluster centroid :: {cluster.centroid.point}")
    cluster.randomizeCentroid()
    this = Point(2)
    this.setPoint([0, 0])
    other = Point(2)
    other.setPoint([3, 4])
    cluster.addMember(this)
    cluster.addMember(other)
    print(f"Cluster centroid :: {cluster.centroid.point}")
    cluster.recomputeCentroid()
    print(f"Recomputed centroid :: {cluster.centroid.point}")
    print(f"Distance of point1 from point2 :: {this.distanceTo(other)}")
    print(
        f"Distance of point1 from point2[@classmethod] :: {Point.distance(this, other)}")
