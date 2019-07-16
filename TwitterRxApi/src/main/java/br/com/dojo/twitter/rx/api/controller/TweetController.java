package br.com.dojo.twitter.rx.api.controller;


import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

import com.amazonaws.services.comprehend.model.Entity;

import br.com.dojo.twitter.rx.api.model.Tweet;
import br.com.dojo.twitter.rx.api.service.TweetService;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

@RestController
@RequestMapping("/tweets")
public class TweetController {
		
	private TweetService service;
	
	@Autowired
	public TweetController(TweetService service) {
		this.service = service;	
	}
	
	@GetMapping(produces="application/json")
	@ResponseStatus(HttpStatus.OK)
	public Flux<Tweet> findAll(){
		return this.service.findAll();
	}
	
	@GetMapping(value="/upper", produces="application/json")
	public Flux<Tweet> UpperAll(){
		return this.service.findAll()
					.flatMap( tweet -> service.upperTweet(tweet) );
	}
	
	@GetMapping(value="/{id}", produces="application/json")
	public Mono<Tweet> findById(@PathVariable String id){
		return this.service.findById(id);
	}
	
	@GetMapping(value="/{id}/comprehend-entities", produces="application/json")
	public Mono<List<Entity>> comprehendEntities(@PathVariable String id) {
		return this.service.findById(id)												
						.flatMap( tweet -> this.service.detectEntities(tweet.getTexto()));						
	}
	
	@GetMapping(value="/{id}/comprehend-keyphrases", produces="application/json")
	public Mono<?> comprehendKeyPhrases(@PathVariable String id) {
		return this.service.findById(id)
					.flatMap( tweet -> this.service.detectKeyPhrases(tweet.getTexto()));		
	}
	
	@GetMapping(value="/{id}/comprehend-sentiment", produces="application/json")
	public Mono<?> comprehendSentiment(@PathVariable String id) {
		return this.service.findById(id)
					.flatMap( tweet -> this.service.detectSentiment(tweet.getTexto()));		
	}	
}
