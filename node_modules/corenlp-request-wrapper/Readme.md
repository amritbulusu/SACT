# corenlp-request-wrapper

Make simple requests to Stanford CoreNLP with javascript.

## Stanford CoreNLP
Download and extract Stanford CoreNLP from http://stanfordnlp.github.io/CoreNLP/#download

Run `java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer` in the extracted folder to start the CoreNLP server at http://localhost:9000/.

## corenlp-request-wrapper
`npm install corenlp-request-wrapper` or `yarn add corenlp-request-wrapper`

This wrapper provides a single method `parse` which interacts with Stanford CoreNLP server. 

### Test & Example

To test run `npm test` or `yarn run test`

```js
const corenlp = require("corenlp-request-wrapper");

// CoreNLP Server was lunched here with the french props file on port 9000
corenlp.parse(
  "Bonjour le monde." /*stringToProcess*/,
  9000 /*portNumber*/,
  "pos,lemma" /*annotators*/,
  "json" /*outputFormat*/,
  (err, parsedText) => { /*Callback function*/
    console.log(JSON.stringify(JSON.parse(parsedText), null, 2));
  }
);
```

### Read More
For full Stanford CoreNLP usage information see http://stanfordnlp.github.io/CoreNLP/index.html