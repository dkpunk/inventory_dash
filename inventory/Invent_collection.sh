#!/bin/sh

script_home=/home/jsudarsan/KERNAL_AUTO
dum_int=$script_home/dumbleoutput.txt
sot_int=$script_home/sot_prod.csv

#echo "Provide the server IP:"
#read ip
ip=$1
echo -e "<html><head><title>Inventory Details</title></head><body>"
echo -e "<h3> DUMBLEDOOR DATA <h3>\n"

tot_dm=`grep -i "$ip" $dum_int | sort | uniq | wc -l`
inst_cat=`grep -i "$ip"  $dum_int | awk -F":" '{print $4"<br>"}' | sort | uniq -c`

echo "<table class=\"table table-striped table-bordered\" cellspacing=\"0\" width=\"50%\"><tr><td>Total Number Instances: $tot_dm</td></tr>"

echo -e "<tr><td><b>Instances By category:</b><br>\n"

echo "$inst_cat</td></tr>"

echo -e "<tr><td><b>Complete Instance Details:</b><br>\n"
echo "<table id=\"example\" class=\"table table-striped table-bordered\" cellspacing=\"0\" width=\"50%\"><tr><th>IP</th><th>Port</th><th>Instance</th><th>Component</th><th>User</th><th>Date</th></tr>"
grep -i "$ip" $dum_int | awk -F":" '{print "<tr><td>"$1"</td><td>"$2"</td><td>"$3"</td><td>"$4"</td><td>"$5"</td><td>"$6"</td></tr>"}'
echo "</table>"
dif_dum=`grep -i "$ip" $dum_int | awk -F":" '{print $1":"$2}' | sort`

echo "$dif_dum" >$script_home/com_dum.txt

echo "</td></tr></table>"

echo -e "<h3>SOT DATA</h3>"

tot_sot=`grep -i "$ip" $sot_int | sed 's/"//g'| awk -F, '{print $1":"$2":"$3}' | sort | uniq | wc -l`
inst_cat_sot=`grep -i "$ip"  $sot_int | sed 's/"//g' | awk -F, '{print $1":"$2":"$3}' |sort | uniq | awk -F":" '{print $3"<br>"}' | sort | uniq -c`

echo "<table class=\"table table-striped table-bordered\" cellspacing=\"0\" width=\"50%\"><tr><td><b>Total Number Instances:</b> <br>$tot_sot</td></tr>"

echo -e "<tr><td><b>Instances By category:</b><br>"
echo "$inst_cat_sot</td>"

echo -e "<tr><td><b>Complete Instance Details:</b><br>"
echo "<table id=\"example\" class=\"table table-striped table-bordered\" cellspacing=\"0\" width=\"50%\"><tr><th>IP</th><th>Port</th><th>Component</th></tr>"
grep -i "$ip" $sot_int |sed 's/"//g' | awk -F, '{print "<tr><td>"$1"</td><td>"$2"</td><td>"$3"</td></tr>"}' | sort | uniq

dif_sot=`grep -i "$ip" $sot_int | sed 's/"//g' | awk -F, '{print $1":"$2":"$3}' | sort | uniq | awk -F":" '{print $1":"$2}'| sort`


echo "</td></tr></table>"

echo -e "<h3>COMPARISON BETWEEN SOT and DUMBLEDOOR</h3><table class=\"table table-striped table-bordered\" cellspacing=\"0\" width=\"50%\"><tr><td>"

echo "$dif_sot" >$script_home/com_sot.txt

echo "<br>"
diff_data=`diff $script_home/com_dum.txt $script_home/com_sot.txt`

echo "$diff_data" | grep -E "<|>" | sed 's/<//g' | sed 's/>//g'| sed 's/ /<br>/g'
echo "<br>"

##### Current data #####


ssh otc@${ip} 'ps -ef | grep -E "java|ytask|server_upgrade.js|server.js"' >$script_home/livedata.txt

tot_app_inst=`cat $script_home/livedata.txt | grep -aE -o 'jvm_CORE..........|jvm_YTASK.........' | awk '{print $1}'|sort | uniq | wc -l`
tot_node_inst=`cat $script_home/livedata.txt | grep -E "server_upgrade.js|server.js" | grep node | awk '{print $NF}' | sort | uniq|wc -l`

tot_live=`expr $tot_app_inst + $tot_node_inst`

echo "</td></tr></table><br>"
echo -e "<h3>SUMMARY:</h3>"
#echo -e "*********\n"


echo "<table class=\"table table-striped table-bordered\" cellspacing=\"0\" width=\"50%\"><tr><td><tr><td>Total Instances in Dumbledoor : $tot_dm</td></tr>"
echo "<tr><td>Total Instances in SOT : $tot_sot</td></tr>"
echo "<tr><td>Total Instances in Live : $tot_live </td></tr></table>"

