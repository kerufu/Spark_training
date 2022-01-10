from pyspark import SparkContext, SparkConf, AccumulatorParam
import os
import glob

conf = SparkConf()
conf = conf.setAppName("sparkYarn")
conf = conf.setMdaster("yarn")
conf = conf.set("spark.submit.deployMode", "client")
sc = SparkContext(conf=conf)

rdd = sc.parallelize(range(1, 4)).map(lambda x: (x, "a" * x))

# if os.path.exists("file"):
#     for f in glob.glob("file/*") + glob.glob("file/.*"):
#         try:
#             os.remove(f)
#         except OSError as e:
#             print("Error: %s : %s" % (f, e.strerror))
#     os.rmdir("file")

# rdd.saveAsSequenceFile("file")
# print(sc.sequenceFile("file").collect())

lines = sc.parallelize(range(1, 4)).map(lambda x: "a" * x)
lineLengths = lines.map(lambda s: len(s))
lineLengths.persist()
totalLength = lineLengths.reduce(lambda a, b: a + b)
print(totalLength)

lines.foreach(print)
print(lines.map(len).collect())

class VectorAccumulatorParam(AccumulatorParam):
        def zero(self, value):
            return [0.0] * len(value)
        def addInPlace(self, val1, val2):
            for i in range(len(val1)):
                val1[i] += val2[i]
            return val1
va = sc.accumulator([1.0, 2.0, 3.0], VectorAccumulatorParam())
def g(x):
    va.add([x] * 3)
rdd = sc.parallelize([1,2,3])
rdd.foreach(g)
print(va.value)

accum = sc.accumulator(0)
def g(x):
    accum.add(x)
    return x^2
rdd = rdd.map(g)
print(accum.value)
print(rdd.collect())
print(accum.value)

# from pyspark.sql import SparkSession
# spark = SparkSession.builder.getOrCreate()
# from datetime import datetime, date
# import pandas as pd
# from pyspark.sql import Row

# df = spark.createDataFrame([
#     (1, 2., 'string1', date(2000, 1, 1), datetime(2000, 1, 1, 12, 0)),
#     (2, 3., 'string2', date(2000, 2, 1), datetime(2000, 1, 2, 12, 0)),
#     (3, 4., 'string3', date(2000, 3, 1), datetime(2000, 1, 3, 12, 0))
# ], schema='a long, b double, c string, d date, e timestamp')
# print(df.collect())

# pandas_df = pd.DataFrame({
#     'a': [1, 2, 3],
#     'b': [2., 3., 4.],
#     'c': ['string1', 'string2', 'string3'],
#     'd': [date(2000, 1, 1), date(2000, 2, 1), date(2000, 3, 1)],
#     'e': [datetime(2000, 1, 1, 12, 0), datetime(2000, 1, 2, 12, 0), datetime(2000, 1, 3, 12, 0)]
# })
# df = spark.createDataFrame(pandas_df)
# print(df.collect())

# rdd = spark.sparkContext.parallelize([
#     (1, 2., 'string1', date(2000, 1, 1), datetime(2000, 1, 1, 12, 0)),
#     (2, 3., 'string2', date(2000, 2, 1), datetime(2000, 1, 2, 12, 0)),
#     (3, 4., 'string3', date(2000, 3, 1), datetime(2000, 1, 3, 12, 0))
# ])
# df = spark.createDataFrame(rdd, schema=['a', 'b', 'c', 'd', 'e'])
# print(df.collect())

# df.show()
# df.printSchema()
# df.select("a", "b", "c").describe().show()
# from pyspark.sql import Column
# from pyspark.sql.functions import upper
# df.withColumn('upper_c', upper(df.c)).show()
# df.toPandas()

# df = spark.createDataFrame([
#     ['red', 'banana', 1, 10], ['blue', 'banana', 2, 20], ['red', 'carrot', 3, 30],
#     ['blue', 'grape', 4, 40], ['red', 'carrot', 5, 50], ['black', 'carrot', 6, 60],
#     ['red', 'banana', 7, 70], ['red', 'grape', 8, 80]], schema=['color', 'fruit', 'v1', 'v2'])
# df.show()

# df.groupby('color').avg().show()

# def plus_mean(pandas_df):
#     return pandas_df.assign(v1=pandas_df.v1 - pandas_df.v1.mean())

# df.groupby('fruit').applyInPandas(plus_mean, schema=df.schema).show()


# df1 = spark.createDataFrame(
#     [(20000101, 1, 1.0), (20000101, 2, 2.0), (20000102, 1, 3.0), (20000102, 2, 4.0)],
#     ('time', 'id', 'v1'))

# df2 = spark.createDataFrame(
#     [(20000101, 1, 'x'), (20000102, 1, 'z'), (20000101, 2, 'y')],
#     ('time', 'id', 'v2'))

# df1.show()
# df2.show()

# def asof_join(l, r):
#     return pd.merge_asof(l, r, on='time', by='id')

# df1.groupby('id').cogroup(df2.groupby('id')).applyInPandas(
#     asof_join, schema='time int, id int, v1 double, v2 string').show()