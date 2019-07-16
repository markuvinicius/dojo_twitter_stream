const mongoose = require('mongoose');
mongoose.Promise = global.Promise;

const url = 'mongodb://dev-mongo-db:27017/twitter_rx';

mongoose.connect(url, { useNewUrlParser: true });
mongoose.connection.once('open', () => console.log(`Connected to mongo at ${url}`));