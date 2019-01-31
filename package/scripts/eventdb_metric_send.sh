#!/bin/sh
url=http://$1:6188/ws/v1/timeline/metrics
hostname=$2
appid='eventdb'
while [ 1 ]
do
totaltables=`curl -s "http://$2:8081/eventdb:info?op=tableList"|grep -o , | wc -l`
let "totaltables+=1"
totalevents=`curl -s "http://$2:8081/eventdb:info?op=totalEvents"`
# totalevents=`bc -l <<< "${totalevents}/1000000"`
totalfiles=`curl -s "http://$2:8081/eventdb:info?op=totalFiles"`
writespeed=`curl -s "http://$2:8081/eventdb:info?op=writeSpeedOfLast&lastSeconds=0"`
readlatency=`curl -s "http://$2:8081/eventdb:info?op=readLatencyOfLast&lastSeconds=0"`

millon_time=$(( $(date +%s%N) / 1000000 ))
json="{
 \"metrics\": [ {
 \"metricname\": \"totaltables\",
 \"appid\": \"${appid}\",
 \"hostname\": \"${hostname}\",
 \"timestamp\": ${millon_time},
 \"starttime\": ${millon_time},
 \"metrics\": {
 \"${millon_time}\": ${totaltables}
 }
 },
 {
 \"metricname\": \"totalevents\",
 \"appid\": \"${appid}\",
 \"hostname\": \"${hostname}\",
 \"timestamp\": ${millon_time},
 \"starttime\": ${millon_time},
 \"metrics\": {
 \"${millon_time}\": ${totalevents}
 }
 },
 {
 \"metricname\": \"totalfiles\",
 \"appid\": \"${appid}\",
 \"hostname\": \"${hostname}\",
 \"timestamp\": ${millon_time},
 \"starttime\": ${millon_time},
 \"metrics\": {
 \"${millon_time}\": ${totalfiles}
 }
 },
 {
 \"metricname\": \"writespeed\",
 \"appid\": \"${appid}\",
 \"hostname\": \"${hostname}\",
 \"timestamp\": ${millon_time},
 \"starttime\": ${millon_time},
 \"metrics\": {
 \"${millon_time}\": ${writespeed}
 }
 },
 {
 \"metricname\": \"readlatency\",
 \"appid\": \"${appid}\",
 \"hostname\": \"${hostname}\",
 \"timestamp\": ${millon_time},
 \"starttime\": ${millon_time},
 \"metrics\": {
 \"${millon_time}\": ${readlatency}
 }
 }
 ]
}"
 
# echo $json |tee -a /root/my_metric.log
curl -i -X POST -H "Content-Type: application/json" -d "${json}" ${url}
sleep 5
done
