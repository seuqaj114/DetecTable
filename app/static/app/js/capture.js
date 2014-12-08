document.addEventListener("DOMContentLoaded", function() {
	var canvas = document.getElementById("canvas");
	var context = canvas.getContext("2d");
	var video = document.getElementById("video");
	var videoObj = { "video": true };
	var errBack = function(error) {
		console.log("Video capture error: ", error.code); 
	};
	var snapshot;
	var img = document.createElement("img");

	if(navigator.getUserMedia) { // Standard
		navigator.getUserMedia(videoObj, function(stream) {
			video.src = stream;
			video.play();
		}, errBack);
	} 
	else if(navigator.webkitGetUserMedia) { // WebKit-prefixed
		navigator.webkitGetUserMedia(videoObj, function(stream){
			video.src = window.webkitURL.createObjectURL(stream);
			video.play();
		}, errBack);
	}
	else if(navigator.mozGetUserMedia) { // Firefox-prefixed
		navigator.mozGetUserMedia(videoObj, function(stream){
			video.src = window.URL.createObjectURL(stream);
			video.play();
		}, errBack);
	}

	// Trigger photo take
	document.getElementById("snap").addEventListener("click", function() {
		context.drawImage(video, 0, 0, 640, 480);
        img.src = canvas.toDataURL();
        //console.log(img.src);
	});


	var startCorner;
	var finishCorner;

	var clickX = new Array();
	var clickY = new Array();
	var clickDrag = new Array();
	var paint;

	$('#canvas').mousedown(function(e){
		var mouseX = e.pageX - this.offsetLeft;
		var mouseY = e.pageY - this.offsetTop;
		startCorner = {x:e.pageX - this.offsetLeft, y:e.pageY-this.offsetTop};
		finishCorner = {x:e.pageX - this.offsetLeft, y:e.pageY-this.offsetTop};

		paint = true;
		//addClick(e.pageX - this.offsetLeft, e.pageY - this.offsetTop);
		//redraw();
		console.log("mousedown");
	});

	$('#canvas').mousemove(function(e){
	  if(paint){
	    finishCorner.x = e.pageX - this.offsetLeft,
	    finishCorner.y = e.pageY-this.offsetTop;
	    //addClick(e.pageX - this.offsetLeft, e.pageY - this.offsetTop, true);
	    console.log(startCorner);
	    console.log(finishCorner);

	    context.clearRect( 0 , 0 , canvas.width, canvas.height );
	    context.drawImage(img, 0, 0, 640, 480);
	    draw();

		console.log("mousemove");

	  }
	});

	$('#canvas').mouseup(function(e){
	  paint = false;
	});

	$('#canvas').mouseleave(function(e){
		paint = false;
	});

	function addClick(x, y, dragging)
	{
	  clickX.push(x);
	  clickY.push(y);
	  clickDrag.push(dragging);
	}

	function draw(){
		context = canvas.getContext("2d");		
		context.strokeStyle="#df4b26";
	  	context.lineWidth = 2;

		context.strokeRect(Math.min(startCorner.x,finishCorner.x),
					Math.min(startCorner.y,finishCorner.y),
					Math.abs(startCorner.x-finishCorner.x),
					Math.abs(startCorner.y-finishCorner.y)
		);

		//context.stroke();
	}

	/*
	function redraw(){
	  //context.clearRect(0, 0, context.canvas.width, context.canvas.height); // Clears the canvas
	  
	  context.strokeStyle = "#df4b26";
	  context.lineJoin = "round";
	  context.lineWidth = 5;
				
	  for(var i=0; i < clickX.length; i++) {		
	    context.beginPath();
	    if(clickDrag[i] && i){
	      context.moveTo(clickX[i-1], clickY[i-1]);
	     }else{
	       context.moveTo(clickX[i]-1, clickY[i]);
	     }
	     context.lineTo(clickX[i], clickY[i]);
	     context.closePath();
	     context.stroke();
	  }
	}
	*/
}, false);