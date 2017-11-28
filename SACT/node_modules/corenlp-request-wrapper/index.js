const request = require('request');

function parse(stringToProcess, portNumber, annotators, outputFormat, cb) {
  request.post(`http://localhost:${portNumber}/`,{
    body: stringToProcess,
    qs: {properties: JSON.stringify({annotators, outputFormat}) }
  },function(err, response, body) {
    cb(err, body, response);
  });
};

module.exports = { parse };
