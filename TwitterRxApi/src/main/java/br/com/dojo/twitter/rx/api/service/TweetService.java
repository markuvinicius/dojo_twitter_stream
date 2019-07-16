package br.com.dojo.twitter.rx.api.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.amazonaws.services.comprehend.model.Entity;

import br.com.dojo.twitter.rx.api.model.Tweet;
import br.com.dojo.twitter.rx.api.repository.TweetRepository;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

@Service
public class TweetService implements ITweetService{
	
	private TweetRepository repo;
	private AwsComprehendService comprehendService;
	
	@Autowired
	public TweetService(TweetRepository repo, AwsComprehendService service) {
		this.repo = repo;
		this.comprehendService = service;
	}

	@Override
	public Flux<Tweet> findAll() {
		return this.repo.findAll();
	}

	@Override
	public Mono<Tweet> findById(String id) {
		return this.repo.findById(id);
	}
	
	public Flux<Tweet> upperTweet(Tweet tweet){
		return Flux.just( Tweet.builder()
							.id(tweet.getId())
							.texto(tweet.getTexto().toUpperCase())
							.usuario(tweet.getUsuario())
							.build());
	}
	
	public Mono<?> detectKeyPhrases(String text) {
		return this.comprehendService.detectKeyPhrasesRequest(text);
	}
	
	public Mono<?> detectSentiment(String text){
		return this.comprehendService.detectSentiment(text);
	}
	
	public Mono<List<Entity>> detectEntities(String text) {
		return this.comprehendService.detectEntities(text);
	}
}
