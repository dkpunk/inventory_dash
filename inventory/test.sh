

cat test.txt | while read line
do

    user=`echo "$line" | awk '{print $1}'`
    inst=`echo "$line" | grep -aE -o 'jvm_CORE..........|jvm_YTASK.........' | awk '{print $1}'|sort | uniq`
    comp=`echo "$line" | grep -a -o 'Dotc.component.name=....................' | awk '{print $1}'|sort| uniq`


    echo "$user : $inst : $comp"


done
