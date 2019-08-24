package br.com.dojo.twitter.rx.api.router;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.reactive.function.server.RequestPredicates;
import org.springframework.web.reactive.function.server.RouterFunction;
import org.springframework.web.reactive.function.server.RouterFunctions;
import org.springframework.web.reactive.function.server.ServerResponse;

import br.com.dojo.twitter.rx.api.controller.TweetWebFluxHandler;

@Configuration
public class TweetRouter {
	
	@Bean
	public RouterFunction<ServerResponse> route(TweetWebFluxHandler handler){
		return RouterFunctions
				.route(RequestPredicates.GET("/rx/tweets"), handler::getAllTweets);
	}

}
