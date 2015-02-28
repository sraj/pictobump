(function() {
  var PB_App = {};
  PB_App.init = function() {

    PB_App.canvas = document.getElementById("js-canvas-draw");
    PB_App.canvas.height = (PB_App.canvas.parentNode.offsetWidth/2);
    PB_App.canvas.width = PB_App.canvas.parentNode.offsetWidth;
    PB_App.ctx = PB_App.canvas.getContext("2d");
    PB_App.canvasInit();

    PB_App.socket = io.connect('http://localhost:4000');
    
    PB_App.socket.emit('pictoinit', {
        id:PBData.PICTOID
    });

    PB_App.socket.on('turnfriend', function(data) {
      PBData.IS_OWNER = false;
      $('canvas').die();
      $("#js-guess-result").html("");
      $("#js-submit").live('click', PB_App._bindGuess);
      PB_App.canvas.width = PB_App.canvas.width;
      PB_App.canvasInit();
    });

    PB_App.socket.on('yourturn', function(data) {
      PBData.IS_OWNER = true;
      $("#js-submit").die();
      $("#js-guess-result").html("");
      $('canvas').live('mousedown mouseup mousemove', PB_App._bindDraw);
      PB_App.socket.emit('makefriend', {
        id:PBData.PICTOID
      });
      PB_App.canvas.width = PB_App.canvas.width;
      PB_App.canvasInit();
    });

    PB_App.socket.on('draw', function(data) {
      return PB_App.draw((data.x * PB_App.canvas.width), (data.y * PB_App.canvas.height), data.type);
    });
    
    PB_App.socket.on('guessed', function(data) {
      var divHTML = '<div style="overflow: hidden; margin-bottom: 5px; border-bottom: 1px dotted #e5e5e5;">';
      divHTML += '<span class="text-success"><strong>'+data.text+'</strong></span>';
      if (PBData.IS_OWNER) {
        divHTML += '<a class="btn btn-small pull-right" href="#"><i class="icon-ok"></i></a>';
      }
      divHTML += '</div>';
      jQuery(divHTML).appendTo('#js-guess-result');
    });

    $("#js-guess-result a").live('click', function(e) {
      PB_App.socket.emit('frndturn', {
        id:PBData.PICTOID
      });
    });
  };
  
  PB_App.canvasInit = function() {
    PB_App.ctx.fillStyle = "solid";
    PB_App.ctx.strokeStyle = "#999999";
    PB_App.ctx.lineWidth = 2;
    PB_App.ctx.lineCap = "round";
    PB_App.ctx.setTransform(1,0,0,1,0,0);
  }

  PB_App.draw = function(x, y, type) {
    if (type === "mousedown" || type === "touchstart") {
      PB_App.ctx.beginPath();
      return PB_App.ctx.moveTo(x, y);
    } else if (type === "mousemove" || type === "touchmove") {
      PB_App.ctx.lineTo(x, y);
      return PB_App.ctx.stroke();
    } else {
      return PB_App.ctx.closePath();
    }
  };

  PB_App._bindGuess = function(e) {
    var guess_a = $("#js-guess-form").serializeArray();
    if (!PBData.IS_OWNER) {
      PB_App.socket.emit('guess', {
        id:PBData.PICTOID,
        text: guess_a[0].value
      });
    }
    $(this).closest('form').find("input[type=text]").val("");
    return false;
  };

  PB_App._bindDraw = function(e) {
      var offset, type, x, y;
      type = e.handleObj.type;
      if (type === "mousemove") { 
        if (e.which != 1) { return; }
      }
      offset = $(this).offset();
      e.offsetX = e.originalEvent.pageX - offset.left;
      e.offsetY = e.originalEvent.pageY - offset.top;
      x = e.offsetX;
      y = e.offsetY;
      PB_App.draw(x, y, type);
      PB_App.socket.emit('pictodraw', {
        id:PBData.PICTOID,
        x: x/PB_App.canvas.width,
        y: y/PB_App.canvas.height,
        type: type
      });
      e.preventDefault();
  };

  $(window).resize(function() {
    var c = $(PB_App.canvas);
    c.attr('width', c.parent().width());
    c.attr('height', (c.parent().width()/2));
    PB_App.canvasInit();
  });

  if (PBData.IS_OWNER) {
    $('canvas').live('mousedown mouseup mousemove', PB_App._bindDraw);
  } else {
    $("#js-submit").live('click', PB_App._bindGuess);
  }

  $(function() {
    return PB_App.init();
  });
}).call(this);
