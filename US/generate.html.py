from os import walk

def generateHTML(filename):
	f = open(str(filename.split('.')[:-1][0])+'.html','w')
	print filename
	HTML = """
	<!DOCTYPE html>
	<meta charset="utf-8">
	<style>

	svg {
	  background-color: #fff;
	}

	.counties {
	  fill: none;
	  ;
	}

	.states {
	  fill: none;
	  stroke: #fff;
	  stroke-linejoin: round;
	}

	</style>
	<body>
	<script src="http://d3js.org/d3.v3.min.js"></script>
	<script src="http://d3js.org/queue.v1.min.js"></script>
	<script src="http://d3js.org/topojson.v1.min.js"></script>
	<script>

	var width = 960,
	    height = 500;

	var color = d3.scale.threshold()
	    .domain([1,100,200,300,400,500,600,700,800,900,1000,2000,3000,4000,5000,6000,7000,8000,9000,10000,125000,150000,20000,100000])
	    .range(['#ebf1fb','#dde8f8','#cfdef6','#c1d4f3','#b2caf0','#a4c0ee','#96b6eb','#88ace8','#79a3e5','#6b99e3','#5d8fe0','#4f85dd','#407bda','#3271d8','#2868d1','#2561c2','#235ab4','#2053a6','#1d4c98','#1a4589','#183e7b','#15366d','#122f5f','#0f2850','#0d2142']);

	var path = d3.geo.path();

	var svg = d3.select("body").append("svg")
	    .attr("width", width)
	    .attr("height", height);

	queue()
	    .defer(d3.json, "US-STATES.topojson")
	    .defer(d3.tsv, "%s")
	    .await(ready);

	function ready(error, us, unemployment) {
	  var rateById = {};

	  unemployment.forEach(function(d) { rateById[d.id] = +d.rate; });

	  svg.append("g")
	      .attr("class", "counties")
	    .selectAll("path")
	      .data(topojson.feature(us, us.objects.states).features)
	    .enter().append("path")
	      .attr("d", path)
	      .style("fill", function(d) { return color(rateById[d.properties.STATE]); });
	      
	  svg.append("path")
	      .datum(topojson.mesh(us, us.objects.states, function(a, b) { return a.id !== b.id; }))
	      .attr("class", "states")
	      .attr("d", path);
	}

	</script>
	""" % filename
	f.write(HTML)
	f.close

f = []
for (dirpath, dirnames, filenames) in walk('.'):
	f.extend(filenames)
	break
for file in f:
	try:
		if file.split('.')[-1] == 'tsv' and int(file.split('.')[0]):
			generateHTML(file)
	except Exception, exc:
		pass