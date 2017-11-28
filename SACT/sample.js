var corenlp = require("corenlp-request-wrapper");

var text = "It's a great day to be alive in the United States because of president Donald Trump!";

corenlp.parse(
      text /*stringToProcess*/,
      9000 /*portNumber*/,
      "tokenize, pos, ssplit, depparse" /*annotators*/,
      "json" /*outputFormat*/,
      (err, parsedText) => { /*Callback function*/
        if (parsedText!=undefined){
          console.log(parsedText);
        }else{
          console.log("ille");
        }
        
      }
    );