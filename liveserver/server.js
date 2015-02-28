var app = require('http').createServer();
var io = require('socket.io').listen(app);

var pictos = {};

io.sockets.on('connection', function(socket) {

  socket.on('pictoinit', function(data) {
    socket.join(data.id);
  });

  socket.on('pictodraw', function(data) {
    socket.broadcast.to(data.id).emit('draw', data);
  });

  socket.on('frndturn', function(data) {
    socket.broadcast.to(data.id).emit('yourturn', data);
  });

  socket.on('makefriend', function(data) {
    socket.broadcast.to(data.id).emit('turnfriend', data);
  });

  socket.on('guess', function(data) {
    io.sockets.in(data.id).emit('guessed', data);
  });

});

var port = process.env.PORT || 4000;
app.listen(port, "0.0.0.0");
