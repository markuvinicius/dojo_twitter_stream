const mongoose = require('mongoose');
const { Schema } = mongoose;

const tweetSchema = new Schema({
    texto: String,
    lang:String    
  });

const Tweet = mongoose.model('tweets', tweetSchema); 

module.exports = {
  Tweet
};