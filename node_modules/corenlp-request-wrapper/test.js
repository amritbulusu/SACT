'use strict';
const corenlp = require("./index");

// CoreNLP Server was started with french props file on port 9000
corenlp.parse(
  "Bonjour le monde.", /*stringToProcess*/
  9000, /*portNumber*/
  "pos,lemma", /*annotators*/
  "json", /*outputFormat*/
  (err, parsedText) => { /*Callback function*/
    let parsed = JSON.parse(parsedText); // we expect a JSON output string
    console.log(JSON.stringify(parsed, null, 2));
  }
);
