

curl -H "Content-Type: application/json" -X POST -d '{"environments":"stage","mailTo":"jsudarsan@yodlee.com"}' -k https://dumbledore.yodlee.com/process/getAllProcess | jq . > dumbleinvent

#grep -iwE "ip|instance|component|environment|userStartingProcess|}," dumbleinvent | grep -iv "command" | paste -s | tr "}" "\n" | awk -F'"' '{print $4":"$15":"$8":"$12":"$18}' |sed -e 's/:: /:/g' -e 's/,//g'| tr -d ' \t' >dumbleoutput.txt

grep -iwE "ip|instance|port|processStartDate|component|environment|userStartingProcess|}," dumbleinvent | grep -iv "command" | paste -s | tr "}" "\n" | awk -F'"' '{print $12":"$5":"$3":"$8":"$16":"$20":"$24}' | sed -e 's/:: /:/g' -e 's/,//g'| tr -d ' \t' | sed 's/^://g' >dumbleoutput.txt
