import os
import json
import re
import sys
region=sys.argv[1]
outfile='/var/www/html/lb_dashboard/net_details_'+region+'.html'
file_out=open(outfile,'w')
infiledict={'SC9': ["SC9_prod_Ext","SC9_prod_Int"],'AUS' : ["AUS_prod"],'UK' : ["UK_prod"],'MAL':["MAL_prod"],"IDC" : ["IDC_prod"],"CAN" : ["CAN_prod"]}
file_out.write('<!doctype html><html><head><title>LB Details</title></head><body>')
file_out.write('''<style>
#customers {
    font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
    border-collapse: collapse;
    width: 100%;
    background-color: #f2f2f2;
}

#customers td, #customers th {
    border: 1px solid #ddd;
    padding: 8px;
}

#customers tr:hover {background-color: #ddd;}

#customers th {
    padding-top: 12px;
    padding-bottom: 12px;
    text-align: left;
    background-color: #6a98ed;
    color: white;
}
</style>''')

def tail(f, n):
  stdin,stdout = os.popen2("tail -n "+n+" "+f+"")
  stdin.close()
  lines = stdout.readlines(); stdout.close()
  return lines

def getdockerstatus(pool,fname):
  if(re.search("blue_ysl",pool,re.IGNORECASE)):
    pool2=pool.replace("blue_ysl","green_ysl")
    print "Pool1"+pool+" Pool2"+pool2
    stdin,stdout = os.popen2("cat "+fname+" | grep "+pool2+" | tail -1 | grep \"up\" ")
    stdin.close()
    lines = stdout.readlines(); stdout.close()
    print "status"+str(lines)
  elif(re.search("green_ysl",pool,re.IGNORECASE)):
    pool2=pool.replace("green_ysl","blue_ysl")
    print "Pool1"+pool+" Pool2"+pool2
    stdin,stdout = os.popen2("cat "+fname+" | grep "+pool2+" | tail -1 | grep \"up\" ")
    stdin.close()
    lines = stdout.readlines(); stdout.close()
    print "status"+str(lines)
    if(lines):
      return 0
    else:
      return 1

def filetohash(fileout,nfile):
	server_status={}
	for line in fileout:
		ARR=line.split(" ")	
		if(re.search("manager",ARR[-2],re.IGNORECASE) and re.search("down",ARR[-1],re.IGNORECASE)):
			#cal docker here
			print "Calling getdockerstatus with"+ARR[-3]+" "+nfile
			status=getdockerstatus(ARR[-3],nfile)
			if(status==1):
				server_status[ARR[-2]]=[ARR[-1],ARR[-3]," ".join(ARR[0:3])]
		else:
			if(re.search("down",ARR[-1],re.IGNORECASE)):
				server_status[ARR[-2]]=[ARR[-1],ARR[-3]," ".join(ARR[0:3])]	
			elif(re.search("forced",ARR[-1],re.IGNORECASE)):
				server_status[ARR[-2]]=["User Down",ARR[-3]," ".join(ARR[0:3])]
			elif(re.search("up",ARR[-1],re.IGNORECASE)):
				if ARR[-2] in server_status.keys():
					del(server_status[ARR[-2]])
	return server_status

def getdownintance(server_hash):
	count=0
	downarr={}
	for element in server_hash.keys():
		if((re.search("down",server_hash[element][0],re.IGNORECASE)) or (re.search("forced",server_hash[element],re.IGNORECASE))):
			count=count+1
			downarr[element]=server_hash[element]
	return count,downarr
			

#filenames=("SC9_prod_Ext","SC9_prod_Int") #add all the network files to be monitored here
filenames=infiledict[region]
filedir="/var/www/html/SO/SO/ToolOpsDashBoard/LBstat/"
for nfile in filenames:
	nfiledisp=nfile
	dcarr=nfile.split("_")
	nfile=filedir+nfile
	file_out.write('<table id="customers" class="table table-striped table-bordered" cellspacing="0" width="100%"><caption><h3><b>LB Stats for '+nfiledisp+'</b></h3></caption><thead><tr><th>Instance</th><th>Instance Status</th><th>Pool Name</th><th>Last Checked</th></tr></thead><tbody>')
	fileout=tail(nfile,"2000")
	tmp=filetohash(fileout,nfile)
	print tmp
	#(count,downarr)=getdownintance(tmp)
	for element in sorted(tmp.keys()):
                file_out.write('<tr><td>'+element+'</td>'+'<td>'+tmp[element][0]+'</td>'+'<td>'+tmp[element][1]+'</td>'+'<td>'+tmp[element][2]+'</td></tr>')
	print "Number of instances down"+str(len(tmp.keys()))
	file_out.write('<tr><td rowspan="2"><h3><b>'+"Number of instances down :"+str(len(tmp.keys()))+'</h3></b></td></tr>')
	file_out.write('</tbody></table>')
file_out.write('''<script src="jquery-1.12.4.js"></script>
     <script src="jquery.dataTables.min.js"></script>
     <script src="dataTables.bootstrap.min.js"></script>
      <link href="bootstrap.min.css" rel="stylesheet">
      <link href="dataTables.bootstrap.min.css" rel="stylesheet">
      <script>
$(document).ready(function() {
    $(#example).DataTable();
     $(#example1).DataTable();
} );</script></body></html>''')

