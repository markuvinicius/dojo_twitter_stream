package br.com.dojo.twitter.rx.api.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.BodyInserters;
import org.springframework.web.reactive.function.server.ServerRequest;
import org.springframework.web.reactive.function.server.ServerResponse;

import br.com.dojo.twitter.rx.api.model.Tweet;
import br.com.dojo.twitter.rx.api.service.ITweetService;
import reactor.core.publisher.Mono;

@Component
public class TweetWebFluxHandler {
	
	private ITweetService service;
	
	@Autowired
	public TweetWebFluxHandler(ITweetService service) {
		this.service = service;
	}
	
	public Mono<ServerResponse> getAllTweets(ServerRequest request){
		return ServerResponse.ok()
				.contentType(MediaType.TEXT_EVENT_STREAM)
				.body(BodyInserters.fromPublisher( service.findAll(), Tweet.class));
	}
}
