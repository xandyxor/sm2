var app = require('http').createServer(null);
var io = require('socket.io')(app);

app.listen(81);

io.on('connection', function (socket) {
    socket.on('handshake1', function (data) {
        console.log(data);
        socket.emit('handshake2','002');
    });
    socket.on('chatroom', function(data) {
        console.log("chatroom:  " + data);
    });
    socket.on('speak', function(data) {
        socket.broadcast.emit('speak',data);
        console.log("speak:  " + data);
    });
    
    socket.on('face_identification', function(data) {
        socket.broadcast.emit('face_identification',data);
        console.log('face_identification'+data);
    });
    socket.on('speaker_ecognition', function(data) {
        socket.broadcast.emit('speaker_ecognition',data);
        console.log('speaker_ecognition'+data);
    });
    socket.on('crawler', function(data) {
        socket.broadcast.emit('crawler',data);
        console.log('crawler'+data);
    });

    socket.on('801', function(data) {
        console.log("getkeywords:  " + data);
    });
    socket.on('802', function(data) {
        console.log("Crawler:  " + data);
    });
    socket.on('803', function(data) {
        console.log("showfilename:  " + data);
    });
    socket.on('804', function(data) {
        console.log("CrawlerFlag:  " + data);
    });
    socket.on('805', function(data) {
        console.log("get_news:  " + data);
    });
    socket.on('806', function(data) {
        console.log("google:  " + data);
    });

    socket.on('service', function(data) {
        //用來傳代碼
        socket.broadcast.emit('service',data);

        console.log(data);
        if(data =="test"){
            socket.emit('events','asdasdasdas');
        }
        if(data =="801"){
            // socket.emit('getkeywords','10');
            socket.emit('801','10');

        }
        if(data =="802"){
            // socket.emit('Crawler','1');
            socket.emit('802','2');

        }
        if(data =="803"){
            // socket.emit('showfilename','showfilename');
            socket.emit('803','showfilename');

        }
        if(data =="804"){
            // socket.emit('CrawlerFlag','CrawlerFlag');
            socket.emit('804','CrawlerFlag');

        }
        if(data =="805"){
            // socket.emit('get_news','美國');
            socket.emit('805','美國');

        }
        if(data =="806"){
            // socket.emit('get_news','美國');
            socket.emit('806','美國是審麼');

        }
    });

});