
const express               = require('express');
const { ApolloServer, gql } = require('apollo-server-express');

require('./config');

const { Tweet } = require('./models');

const typeDefs = gql`
    type Query {
      hello: String,
      tweets: [Tweet]
    }

    type Tweet {                
        texto: String,
        lang: String        
    }    
`;

const resolvers = {
    Query: {
        hello: () => 'Hello World!',
        tweets: async () => await Tweet.find({}).exec()
    }    
};

const server = new ApolloServer({ typeDefs, resolvers });
const app = express();
server.applyMiddleware({ app });

app.listen({ port: 4000 }, () =>
  console.log(`🚀 Server ready at http://localhost:4000${server.graphqlPath}`)
);