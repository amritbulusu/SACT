
var express = require('express');
var path = require('path');
var app = express();
var fs = require('fs');
var corenlp = require("corenlp-request-wrapper");
var bodyParser = require('body-parser')
app.use( bodyParser.json());       // to support JSON-encoded bodies
app.use(bodyParser.urlencoded({     // to support URL-encoded bodies
  extended: true
})); 


app.set('port',3000);

app.use(express.static(path.join(__dirname, 'public')));

app.post('/parseNLU', function(req, res) {

    var text = req.body.text;
    console.log("text"+text);
    // CoreNLP Server was lunched here with the french props file on port 9000 
    corenlp.parse(
      ""+text /*stringToProcess*/,
      9000 /*portNumber*/,
      "tokenize, pos, ssplit, depparse" /*annotators*/,
      "json" /*outputFormat*/,
      (err, parsedText) => { /*Callback function*/
        if (parsedText!=undefined){
          var json = JSON.parse(parsedText);
          res.send(json);  
        }
        
      }
    );
});

var server = app.listen(app.get('port'), function() {
  var port = server.address().port;
  console.log('Magic happens on port ' + port);
});

const { spawn } = require('child_process');
const bat = spawn('cmd.exe', ['/c', 'run_sc.bat']);

bat.stdout.on('data', (data) => {
  console.log(data.toString());
});



