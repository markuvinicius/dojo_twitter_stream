package br.com.dojo.twitter.rx.api.service;

import br.com.dojo.twitter.rx.api.model.Tweet;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

public interface ITweetService {
	
	public Flux<Tweet> findAll();
	public Mono<Tweet> findById(String id);

}
