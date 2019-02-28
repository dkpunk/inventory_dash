<html>
  <head>
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script><script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
</script>
</head>
<body>
<h1> Inventory Details     <img src="inventory.png" style="width:40px; height:40px" title="Inventory"></h1>
  Server IP : <input type="text" id="ip"><br>
<button onclick="myFunction()">Submit</button>
<div id="output" width="80%" height="20%"></div>
<script type="text/javascript">
	function myFunction(){
		var ip=document.getElementById("ip").value;
		var json_var={ "ip" :ip};
		//alert(ip);
		//alert(fdt_val);
		//alert(tdt_val);		
		$.ajax({
			type: 'POST',
			url : 'getdetails.php',
			data : (json_var),
			success: function(data){
//				alert(data);
			document.getElementById("output").innerHTML=data;
			},
			error : function(jq,status,message){
			alert("unable to fetch data"+status+" Message "+message);}
		});
	}
	</script>
	<script src="jquery-1.12.4.js"></script>
     <script src="jquery.dataTables.min.js"></script>
     <script src="dataTables.bootstrap.min.js"></script>
      <link href="bootstrap.min.css" rel="stylesheet">
      <link href="dataTables.bootstrap.min.css" rel="stylesheet">
      <script>
$(document).ready(function() {
   $('#example').DataTable();
     $('#example1').DataTable();
} );
</script>
</body>
</html>
