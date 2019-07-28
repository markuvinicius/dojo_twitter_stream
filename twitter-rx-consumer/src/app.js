// from node
var util = require('util');
var stream = require('stream');               
// from npm
var _ = require('highland');
var websocket = require('websocket-stream');

var catWS = websocket('ws://localhost:5000/tweets');

var toConsole = new stream.Writable({
    objectMode: true 
  });

toConsole._write = function (data, encoding, done) {
console.log(data);
done();
};