package br.com.dojo.twitter.rx.api.repository;

import org.springframework.data.mongodb.repository.ReactiveMongoRepository;
import org.springframework.stereotype.Repository;

import br.com.dojo.twitter.rx.api.model.Tweet;

@Repository
public interface TweetRepository extends ReactiveMongoRepository<Tweet, String>{

}
