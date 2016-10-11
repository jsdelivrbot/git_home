# hdfs dfs -copyFromLocal $input /user/
hadoop jar $HADOOP_STREAMING/hadoop-streaming-2.7.2.jar\
    -file $mapper\
    -mapper $mapper\
    -file $reducer\
    -reducer $reducer\
    -input $input\
    -output $output
