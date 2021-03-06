/***************************
*    Utils
****************************/

var obColors={
	'image' : '#40D7FF',
	'text' : '#FFDA3E',
	'sound' : '#5AED64',
	'video' : '#FF563D',
	};


// function to get multiline labels for d3 svg text elements
function insertLineBreaksD3(d) {
    var el = d3.select(this);
    el.attr("stroke", function(d) {
        return "black";
    });
    var words = d.split(/[_ ]/);
    el.text('');

    for (var i = 0; i < words.length; i++) {
        // if a word is too short (<3 chars) append it to the next element
        //if (words[i].length<3 && i< words.length-1){
        //    words[i+1]=words[i]+" "+words[i+1];
        //    continue;
        //}
        
	if (i>= words.length/2){
            var tspan = el.append('tspan').text(words[i]);
            if (i > 0)
        tspan.attr('x', 0).attr('dy', '15');
    }
    }
}

//function to unescape html entities
function htmlDecode(input){
  var e = document.createElement('div');
  var pre_cleaning = input.replace(/&amp;/g,"&").replace(/&amp;/g,"&");
  e.innerHTML = pre_cleaning;   
  var result ="";
  if (e.childNodes.length === 0)
  {
      return result;
  }
  else if (e.childNodes[0].nodeValue)
  {
      //console.log("arrunta "+e.childNodes[0].nodeValue);
      result = e.childNodes[0].nodeValue;      
      return result.replace(/http:\/\/www.http\/\//, "http://");
  }
  else
  {
      //console.log("aldaketarik ez");
      return input;
  }
}


//Maddalen: Nodoen titulutik etiketak garbitu eta Moztu 

function tituluaGarbitu (titulua,moztu){ 
        
    titulua=titulua.replace(/^\s+/,"");
    var tituluaJat=htmlDecode(titulua);
    titulua=tituluaJat;
    var titulu_es="";
    var titulu_en="";
    var titulu_eu="";
   
    //console.log(titulua);
    //espresio erregularrak erabilita hizkuntza desberdinetako tituluak atera 
    var myRegexpES = new RegExp("<div class=\"titulu_es\">(.*?)</div>");
    //var myRegexpES = /<div class=\"titulu_es\">(.*?)</div>/g;
    var match_es = myRegexpES.exec(titulua);
   
    if (match_es){      
        titulu_es=match_es[1]; //0 posizioan jatorrizkoa dago
       }
    else{
        titulu_es="";
       }
    
    var myRegexpEN = new RegExp("<div class=\"titulu_en\">(.*?)</div>");
    var match_en = myRegexpEN.exec(titulua);     
    if (match_en){
        titulu_en=match_en[1];
       }
    else{
        titulu_en="";
    }
 
    var myRegexpEU = new RegExp("<div class=\"titulu_eu\">(.*?)</div>");
    var match_eu = myRegexpEU.exec(titulua);  
    if (match_eu){
        titulu_eu=match_eu[1];
       }
    else{
        titulu_eu="";
    }
  
    //titulua= !!!erabaki defektuzkoa zein den eu,en,es
    if (titulu_eu){
        titulua=titulu_eu;
     }
    else if (titulu_es){
        titulua=titulu_es;
       }
    else{
        titulua=titulu_en;
       }
   
    //DBko tituluak hizkuntza kontrola ez baldin badu edo lg bada
    if (titulua ==""){
        titulua=tituluaJat;                
    }
    titulua=titulua.replace(/<div class=\"titulu_lg\">(.*?)<\/div>/, "$1");
    
    if (moztu==true && titulua.length>15){
        return titulua.substr(0,14)+"...";
    }
    else{
        return titulua;        
    }

}

function getBrowserInfo()
{
	var ua = navigator.userAgent, tem,
	M = ua.match(/(opera|chrome|safari|firefox|msie|trident(?=\/))\/?\s*(\d+)/i) || [];
	if(/trident/i.test(M[1]))
	{
		tem=  /\brv[ :]+(\d+)/g.exec(ua) || [];
		return 'IE '+(tem[1] || '');
	}
	if(M[1]=== 'Chrome')
	{
		tem= ua.match(/\b(OPR|Edge)\/(\d+)/);
		if(tem!= null) return tem.slice(1).join(' ').replace('OPR', 'Opera');
	}
	M = M[2]? [M[1], M[2]]: [navigator.appName, navigator.appVersion, '-?'];
	if((tem= ua.match(/version\/(\d+)/i))!= null) 
		M.splice(1, 1, tem[1]);
	return M.join(' ');
}


/***************************
*    End of Utils
****************************/



//data: Aldagai honetan daude nodo guztiak.

var data = ibilbide_data;

//zuhaitzaren arraya hasieratu
var treeData = [];

//lehen aldiz margotzea.
sortu(data);


function sortu(data){

    // Sortu mapa
    var dataMap = data.reduce(function(map, node) {
	//node.id: id-ak erabiliko ditu loturak sortzeko.
	map[node.id] = node;
	return map;
    }, {});

    // Sortu zuhaitzaren array-a
    data.forEach(function(node) {
	// Gehitu aitari
	var parent = dataMap[node.parent];
	if (parent) {
            //Sortu semeen array bat existitzen ez bada.
            (parent.children || (parent.children = []))
            // Gehitu nodoa seme array-era
		.push(node);
	} else {
            // Aita null edo ez dauka
            treeData.push(node);
	}
    });

    // ************** Sortu zuhaitz diagrama  *****************
    var margin = {top: 20, right: 120, bottom: 20, left: 120},//marginak
    width = 800 - margin.right - margin.left,//svg-aren zabalera
    height = 600 - margin.top - margin.bottom;//svg-aren altuera    
    var selectedNode = null; //Aukeratutako nodoa
    var draggingNode = null; //Mugitzen ari garen nodoa
    var panSpeed = 200; //abiadura
    var panBoundary = 20;//Muga.
    var duration = 750;//Transizioaren iraupena
    var viewerWidth =  0; //nodoak zetratzeko zabalera
    var viewerHeight = width; //nodoak zetratzeko altuera
    var radio = 30;
    var luzera = radio+10; //luzera = radio +10. Link-aren luzaera.
    var i = 0;

    //Zuhaitza sortu
    var tree = d3.layout.tree()
	.size([width,height]);
    //Diagonala sortu
    var diagonal = d3.svg.diagonal()
	.projection(function(d) { 
            return [d.y-luzera, d.x]; });

    //svg-a sortu, path_boxes div-aren barruan.
    var svg = d3.select("#path_boxes").append("svg")
	.attr("width", width + margin.right + margin.left)
	.attr("height", height + margin.top + margin.bottom)
	.attr("transform", "translate(" + margin.left + "," + margin.top + ")");
    
    //click funtzioa: klik egitean aukeratutako nodoaren zirkulua gorriz ezartzen du.
    function click() {
    	var p = d3.select(this);
    	if (p.select("circle").classed("aukeratuta") == true){
            //d3.selectAll("circle").style({stroke: 'steelblue'});
            //p.select("circle").style({stroke: 'red'});			
            p.select("circle").classed("aukeratuta",false);            
    	} else {
            //p.select("circle").style({stroke: 'steelblue'});
            p.select("circle").classed("aukeratuta",true);
    	}
    	$(this).find(".d3_button").toggle(); //.css({"visibility":"visible"});
    }
    //dblclick funtzioa: klik bikoitza egitean narrazioa gehitzeko textarea eta botoia gaitu egiten dira.
    function dblclick(d){	
	//document.getElementById("narra_textarea").value = d.narrazioa;
	var narrazio_html = htmlDecode(d.narrazioa);
    CKEDITOR.instances.narra_textarea.setData(narrazio_html);
	$("#narrazio_modal").modal('show');
	$('#narrazio_modal').on('shown', function() {
            $("#narra_textarea").focus();
	});
	document.getElementById("narra_botoia").onclick = function () { 
            //d.narrazioa = document.getElementById("narra_textarea").value;  
            d.narrazioa = CKEDITOR.instances.narra_textarea.getData();                                                       
	    $("#narrazio_modal").modal('hide');
        };
    }
    
    // geoclick funtzioa: nodo baten geo informazioa editatzean koordenatu berriak elementuarik gehitzeko.
    function geoclick(d) {
        current_node=d;
        $('#geoloc_modal').modal('show');
        setTimeout(function(){
        	global_map.invalidateSize();
        }, 1000);
        document.getElementById("geomodal_botoia").onclick = function () {            
            d.latitude = document.getElementById('latitude').value;
            d.longitude = document.getElementById('longitude').value;
            save_path_node_geolocation(d.id,d.latitude,d.longitude);
            $("#geoloc_modal").modal('hide');
        };

    }
    
    // ibilbide bateko nodoen geolokalizazioa eguneratzeko funtzioa.
    function save_path_node_geolocation(id, lat,long){
	$.ajax({
	    method : 'POST',
	    url : '/ajax_save_path_node_geolocation',
	    dataType : 'html',
	    data : {
		id : id,
		latitude: lat,
		longitude: long
	    }
	}).done(function(data) {
		var message = gettext("Geolokalizazioa ongi gorde da.");
		$('#message_div').prepend("<div class='alert alert-info' role='alert'>"+message+" <a id='alert-close-button' type='button' onclick='$(this).parent().slideUp();return False;'><i class='fa fa-times eskuma'></i></a></div>");
		$('#message_div').focus();
		//alert("Geolokalizazioa ongi gorde da.");
	});
    }


    //pan funtzioa:noaren posizioaren aldaketa
    function pan(unekoNodoa, direction) {
	var speed = panSpeed;
	if (panTimer) {
            clearTimeout(panTimer);
            translateCoords = d3.transform(svgGroup.attr("transform"));
	    if (direction == 'left' || direction == 'right') {
		translateX = direction == 'left' ? translateCoords.translate[0] + speed : translateCoords.translate[0] - speed;
		translateY = translateCoords.translate[1];
	    } else if (direction == 'up' || direction == 'down') {
		translateX = translateCoords.translate[0];
		translateY = direction == 'up' ? translateCoords.translate[1] + speed : translateCoords.translate[1] - speed;
	    }
            scaleX = translateCoords.scale[0];
            scaleY = translateCoords.scale[1];
            scale = zoomListener.scale();
            svgGroup.transition().attr("transform", "translate(" + translateX + "," + translateY + ")scale(" + scale + ")");
            d3.select(unekoNodoa).select('g.node').attr("transform", "translate(" + translateX + "," + translateY + ")");
            zoomListener.scale(zoomListener.scale());
            zoomListener.translate([translateX, translateY]);
            panTimer = setTimeout(function() {
		pan(unekoNodoa, speed, direction);
            }, 50);
	}
    }
    //zoom funtzioa:eskala haunditu edo txikitu egiten du.
    function zoom() {
	svgGroup.attr("transform", "translate(" + d3.event.translate + ")scale(" + d3.event.scale + ")");
    }
    
    // define the zoomListener which calls the zoom function on the "zoom" event constrained within the scaleExtents
    var zoomListener = d3.behavior.zoom().scaleExtent([0.1, 3]).on("zoom", zoom);
    
    //initiateDrag funtzioa: 
    function initiateDrag(d, unekoNodoa) {
	draggingNode = d;
	d3.select(unekoNodoa).attr('pointer-events', 'none');
	d3.selectAll('.node').attr('class', 'node desactiveDrag');
	d3.select(unekoNodoa).attr('class', 'node activeDrag');
	svgGroup.selectAll("g.node").sort(function(a, b) { // select the parent and sort the path's
	    if (a.id != draggingNode.id) return 1; // a is not the hovered element, send "a" to the back
            else return -1; // a is the hovered element, bring "a" to the front
	});
	// if nodes has children, remove the links and nodes
	if (nodorenzuhaitza.length > 1) {
            // remove link paths
            links = tree.links(nodorenzuhaitza);
            nodePaths = svgGroup.selectAll("path.link")
		.data(links, function(d) {
		    return d.target.id;
		}).remove();
            // remove child nodes
            nodesExit = svgGroup.selectAll("g.node")
		.data(nodorenzuhaitza, function(d) {
		    return d.id;
		}).filter(function(d, i) {
		    if (d.id == draggingNode.id) {
			return false;
		    }
                    return true;
		}).remove();
	}
	// remove parent link
	parentLink = tree.links(tree.nodes(draggingNode.parent));
	svgGroup.selectAll('path.link').filter(function(d, i) {
	    if (d.target.id == draggingNode.id) {
		return true;
	    }
            return false;
	}).remove();
	dragStarted = null;
    }

    var updateTempConnector = function() {
	var data = [];
	if (draggingNode !== null && selectedNode !== null) {
	    // have to flip the source coordinates since we did this for the existing connectors on the original tree
            data = [{
            source: {
                x: selectedNode.y0,
                y: selectedNode.x0
            },
		target: {
                    x: draggingNode.y0,
                    y: draggingNode.x0
		}
            }];
	}
	var link = svgGroup.selectAll(".templink").data(data);
	link.enter().append("path")
            .attr("class", "templink")
            .attr("d", d3.svg.diagonal())
            .attr('pointer-events', 'none');
	link.attr("d", d3.svg.diagonal());
	link.exit().remove();
    };
    
    function centerNode(source) {
	scale = zoomListener.scale();
	x = -source.y0;
	y = -source.x0;
	x = x * scale + viewerWidth / 2;
	y = y * scale + viewerHeight / 2;
	d3.select('g').transition()
            .duration(duration)
            .attr("transform", "translate(" + 0 + "," + 0 + ")scale(" + scale + ")");
	zoomListener.scale(scale);
	zoomListener.translate([x, y]);
    }
    

    function endDrag() {
	selectedNode = null;
	d3.selectAll('.node').attr('class', 'node desactiveDrag');
	d3.select(unekoNodoa).attr('class', 'node');
	// now restore the mouseover event or we won't be able to drag a 2nd time
	d3.select(unekoNodoa).attr('pointer-events', '');
	updateTempConnector();
	if (draggingNode !== null) {
            update(root);
            centerNode(draggingNode);
            draggingNode = null;
	}
    }
    
    var drag = d3.behavior.drag()
	.on("dragstart", function(d){
	    //Nodoa root bada ezin da mugitu bestela nodoa mugitzen hasiko da.
            if (d == root) {
		var p = d3.select(this);
		p.select("circle").style({stroke: 'black'});
		return;
            }
            dragHasi = true;
            //nodorenzuhaitza:Aldagai honetan svg-an dauden nodo bakoitzaren zuhaitza agertzen da. Zein den bere aita eta semeak baditu zeintzuk dira bere semeak.
            nodorenzuhaitza = tree.nodes(d);
            d3.event.sourceEvent.stopPropagation();
	}).on("drag", function(d){
            if (d == root) {
		return;
            }
            if (dragHasi) {
		//unekonodoa= aukeratuta daugan nodoa da
		unekoNodoa = this;
		initiateDrag(d, unekoNodoa);
            }
            relCoords = d3.mouse($('svg').get(0));
            if (relCoords[0] < panBoundary) {
		panTimer = true;
		pan(this, 'left');
            } else if (relCoords[0] > ($('svg').width() - panBoundary)) {
		panTimer = true;
		pan(this, 'right');
            } else if (relCoords[1] < panBoundary) {
		panTimer = true;
		pan(this, 'up');
            } else if (relCoords[1] > ($('svg').height() - panBoundary)) {
		panTimer = true;
		pan(this, 'down');
            } else {
		try {
                    clearTimeout(panTimer);
		} catch (e) {
		}
            }
            d.x0 += d3.event.dy;
            d.y0 += d3.event.dx;
            var node = d3.select(this);
            node.attr("transform", "translate(" + d.y0 + "," + d.x0 + ")");
            updateTempConnector();
	}).on("dragend", function(d) {
            if (d == root) {
		return;
            } 
            //draggingNode: Mugitzen ari garen nodoa.
            //selectedNode: Aukeratu dugun nodoa.
            //Mugitzen dugun nodoa, nodo bat ez dagoen lekuan ezartzen badugu, nodo hori zegoen lekura joango da.
            else if (draggingNode == selectedNode){
		endDrag();
            } else if (selectedNode.parent == draggingNode){
		var index = draggingNode.parent.children.indexOf(draggingNode);
		if (index > -1) {
                    draggingNode.parent.children.splice(index, 1);
		}
		var dragAita = draggingNode.parent;
		selectedNode.parent = dragAita;
		draggingNode.parent = selectedNode;
		for (var i=0;i<draggingNode.children.length;i++){
                    if (selectedNode.name == draggingNode.children[i].name){
			draggingNode.children.splice(i, 1);
                    }
		}
		if (selectedNode.children){
                    selectedNode.children.push(draggingNode);
                    selectedNode.parent.children.push(selectedNode);
                    endDrag(); 
		} else {
                    selectedNode.children = [];
                    selectedNode.children.push(draggingNode);
                    selectedNode.parent.children.push(selectedNode);
                    endDrag();
		} 
            } else if (selectedNode.parent.parent == draggingNode || selectedNode.parent.parent.parent == draggingNode){
		var index = draggingNode.parent.children.indexOf(draggingNode);
		if (index > -1) {
                    draggingNode.parent.children.splice(index, 1);
		}
		var index2 = selectedNode.parent.children.indexOf(selectedNode);
		if (index2 > -1) {
                    selectedNode.parent.children.splice(index2, 1);
		}
		var dragAita = draggingNode.parent;
		selectedNode.parent = dragAita;
		draggingNode.parent = selectedNode;
		if (selectedNode.children){
                    selectedNode.children.push(draggingNode);
                    selectedNode.parent.children.push(selectedNode);
                    endDrag(); 
		} else {
                    selectedNode.children = [];
                    selectedNode.children.push(draggingNode);
                    selectedNode.parent.children.push(selectedNode);
		    for (var c= 0;c<draggingNode.children;c++){
			var index3 = draggingNode.children[i].children.indexOf(selectedNode);
			if (index > -1) {
			    draggingNode.children[i].children.splice(index, 1);
			}
		    }
		    endDrag();
		}
            }  else {
		unekoNodoa = this;
		if (selectedNode) {
                    var index = draggingNode.parent.children.indexOf(draggingNode);
                    if (index > -1) {
			draggingNode.parent.children.splice(index, 1);
                    }
                    if (typeof selectedNode.children !== 'undefined' || typeof selectedNode._children !== 'undefined') {
			if (typeof selectedNode.children !== 'undefined') {
                            selectedNode.children.push(draggingNode);
			} else {
                            selectedNode._children.push(draggingNode);
			}
                    } else {
			selectedNode.children = [];
			selectedNode.children.push(draggingNode);
                    }
                    // Make sure that the node being added to is expanded so user can see added node is correctly moved
                    expand(selectedNode);
                    endDrag();
		}
            }
	});
    
    function expand(d) {
	if (d._children) {
            d.children = d._children;
            d.children.forEach(expand);
            d._children = null;
	}
    } 
    
    function collapse(d) {
	if (d.children) {
            d._children = d.children;
            d._children.forEach(collapse);
            d.children = null;
	}
    }
    
    var overCircle = function(d) {
	selectedNode = d;
	updateTempConnector();
    };  
    

    var svgGroup = svg.append("g");
    root = treeData[0];
    root.x0 = 0;
    root.y0 = height/2;
    update(root);
    centerNode(root);
    
    function update(source) {
	
	// kalkulatu zuhaitz layout berria: Nodoak eta link-ak.
	var nodes = tree.nodes(root).reverse(),
        links = tree.links(nodes);
        //ezabatu root nodoa
        nodes.pop();
        nodes.reverse();
	
	
        // Nodoen arteko distantzia
        nodes.forEach(function(d) { 
            d.y = d.depth * 100;});
	
    // Nodoak deklaratu
	var node = svg.selectAll("g.node")
            .data(nodes, function(d) { return d.id || (d.id = ++i); });
	
	// Nodoak sartu.
	var nodeEnter = node.enter().append("g")
            .call(drag)
            .attr("class", "node")
            .attr("transform", function(d) { 
		return "translate(" + d.y + "," + d.x + ")"; })
            .on('click', click)
            .on('dblclick',dblclick)
            .on("mouseover", function(node) {
            	overCircle(node);
            	
            });
	
        //Zakarrontzi irudia gehitu. Zakarrontzi honetan klik egiten baduzu nodoa ezabatu dezakezu.
        nodeEnter.append("text")
            .style('font-family', 'FontAwesome')
            .style('font-size', '1.5em')
            .style('cursor','pointer')
            .attr("id",function(d) {
		var z = "r"+d.id;
		return z; })
            //.attr("class","fa fa-trash")                                                                                                                                                                        
            .attr("x", function(d) { return -60;})
            .attr("y", function(d) { return -20;})
            .attr("height", 15)
            .attr("width", 15)
            .attr("class", "d3_button")
            .text(function(d) { return '\uf1f8' })
            .on('click', function(d) { 
                if (d.parent.name == "ROOT"){
                	var msg= gettext("Nodoa hau ezin da ezabatu");
                    alert(msg);
                    return;
                } else {
                	var msg=gettext(" Nodoa ezabatu nahi duzu? ");
                    var result = confirm(msg);
                    if (result) {
                        var index = d.parent.children.indexOf(d);
                        if (index>-1){
                            d.parent.children.splice(index, 1);
                        }
                        if (d.children !=undefined){
                            var index2 = d.children.length;
                            for (var i=0;i<index2;i++){
                                d.children[i].parent = d.parent;
                                d.parent.children.push(d.children[i]);
                            }  
                        }
                        update(root);
                    } else {
                    	var msg= gettext("Nodoa ez da ezabatu");
                        alert(msg);
                    }            
                }
            }); 
        
        // Mapa-puntu baten ikonoa gehitu. Gainean klik egiten baduzu nodoaren geokokapena mapan adierazteko aukera izango duzu.
        nodeEnter.append("text")
            .style('font-family', 'FontAwesome')
            .style('font-size', '1.5em')
            .style('cursor','pointer')
            .attr("id",function(d) { 
            	var z = "m"+d.id;
            	return z; })
        //.attr("class","fa fa-map-marker")
            .attr("x", function(d) { return -40;})
            .attr("y", function(d) { return -20;})
            .attr("height", 15)
            .attr("width", 15)
            .attr("class", "d3_button")
            .text(function(d) { return '\uf041' })
            .on('click', geoclick);

        
          //Nodoari motaren arabera irudi bat gehitu.
   		
   		nodeEnter.append("image")
            .attr("id",function(d) { 
                var z = "z"+d.id;
                return z; })
           	.attr("xlink:href", function(d) {return "/static/img/icons/"+d.mota.toLowerCase()+".png";})          	           	 
            .attr("x", function(d) { return 25;})
            .attr("y", function(d) { return -35;})
            .attr("height", 15)
            .attr("width", 15)  
	
	  	//Nodoen Gainean Sagua jarritakoan Nodoaren Titulu osoa erakutsiko da        
		nodeEnter.append("svg:title").text(function(d) {
                return tituluaGarbitu(d.name,false);  });
		
        //nodoari zirkulua gehitu
        nodeEnter.append("circle")
            .attr("id",function(d) {
                return 'nodo: '+tituluaGarbitu(d.name,false);  })
            .attr("class",function(d) { return "aukeratuta stroke-"+d.mota.toLowerCase();})
            .attr("r", function(d){
                if (nodes.length>=10){
                    return radio-10;
                } else {
                    return radio;
                }
            })
            .style("fill", function(d) { 
                var ir = "#"+d.id;
                return  "url("+ir+")";});
	
        //nodoari background irudia ezarri.
	
        nodeEnter.append('defs')
            .append('pattern')
            .attr('id', function(d) { return (d.id);})
            .attr('width', 1)
            .attr('height', 1)
            .attr('patternContentUnits', 'objectBoundingBox')
            .append("svg:image")
            .attr("xlink:xlink:href", function(d) { return htmlDecode(d.irudia);}) // "icon" is my image url. It comes from json too. The double xlink:xlink is a necessary hack (first "xlink:" is lost...).
            .attr("x", 0)
            .attr("y", 0)
            .attr("height", 1)
            .attr("width", 1)
            .attr("preserveAspectRatio", "xMinYMin slice"); 
          
        //Nodoari testua gehitu. 
        /*nodeEnter.append("text")
            .attr("x", function(d) { 
                return d.children || d._children ? 30 : -30; })
            .attr("dy", function(d) {
                if (nodes.length>=10){
                    return d.children || d._children ?  35 : 35;
                } else {
                    return d.children || d._children ?  45 : 45;
                }
            })
            .attr("text-anchor", function(d) { 
                return d.children || d._children ? "end" : "start"; })
            .text(function(d) { 
                //var name = d.name.substring(0,10)+"...";
                var name = tituluaGarbitu(d.name,true);
                return name; })
            .style("fill-opacity", 1);*/
	
	   nodeEnter.append("foreignObject")
      .attr("x", function(d) { 
          return -radio-luzera/3; }) // lehen 35: -35
      .attr("y", function(d) {
            return radio/1.8; //lehen 30 : 30
    })
      .attr("width",function ( d, i ) { return radio*2.1+luzera;})
      .attr("height",function ( d, i ) { return 38;})
      .attr("text-anchor", function(d) { 
          return d.children || d._children ? "end" : "start"; })
          .append("xhtml:body")
          .attr("xmlns","http://www.w3.org/1999/xhtml")
          .attr("title",function(d) { return tituluaGarbitu(d.name,false);})
          .style("background","transparent")
          .append("p")
            .text(function(d) { return tituluaGarbitu(d.name,false);}) //Maddalen
            .style("fill-opacity", 1)
                .attr("class","d3label");

	
    //Nodoaren transizioaren posizioa.
	var nodeUpdate = node.transition()
            .duration(duration)
            .attr("transform", function(d) {
		if (nodes.length>=10){
                var a = d.y-10;
                    return "translate(" + a + "," + d.x + ")";
            } else {
                return "translate(" + d.y + "," + d.x + ")";
            }
            }); 
	
        nodeUpdate.select("text")
            .style("fill-opacity", 1);
        var nodeExit = node.exit().transition()
            .duration(duration)
            .attr("transform", function(d) {
                return "translate(" + source.y + "," + source.x + ")";
            })
            .remove();
        nodeExit.select("circle")
            .attr("r", 0);
        nodeExit.select("text")
            .style("fill-opacity", 0);                      
	

	// link-ak deklaratu
	var link = svgGroup.selectAll("path.link")
            .data(links, function(d) { return d.target.id; });
        link.enter().insert("path", "g")
            .attr("class", "link")
            .style("opacity", function(link){ 
		//ROOT BADA IZKUTATUKO DU ETA BESTELA ERAKUTSIKO DU.
		if (link.source.name == "ROOT"){
                    return 0;
		} else {
                    return 1;
		} })
            .attr('stroke-width', 2)
            .attr("marker-end", "url(#arrowhead)")
            .attr("d", function(d) {
                var o = {
                    x: source.x0,
                    y: source.y0
                };
                //o= Object {x: NaN, y: NaN};
                return diagonal({
                    source: o,
                    target: o
                })
            }); 

        // Transizio linkak bere posizio berrira.
        link.transition()
            .duration(750)
            .attr("d", diagonal);

        //Transizioa existitzen diren nodoen bere aita berrien posiziora.
        link.exit().transition()
            .duration(750)
            .attr("d", function(d) {
                var o = {
                    x: source.x,
                    y: source.y
                };
                return diagonal({
                    source: o,
                    target: o
                });
            })
            .remove();            
	
        //Nodo bakoitzaren d.x posizioa d.x0 izango da.
        //Nodo bakoitzaren d.y posizioa d.y0 izango da.   
        nodes.forEach(function(d) {
            d.x0 = d.x;
            d.y0 = d.y;
        });
	
	//Gezia ezarri link-ari, hau da marker bat gehitu.
        svg.append("defs").append("marker")
            .attr("id", "arrowhead")
            .attr("refX", 0)
            .attr("refY", 0)
            .attr("markerWidth", 6)
            .attr("markerHeight", 4)
            .attr("viewBox", "0 -5 10 10")
            .attr("orient", "auto")
            .append("path")
            .attr("d", "M0,-5L10,0L0,5");
    }
    
}

