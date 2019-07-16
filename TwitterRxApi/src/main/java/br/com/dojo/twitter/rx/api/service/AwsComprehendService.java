package br.com.dojo.twitter.rx.api.service;

import java.util.List;

import org.springframework.stereotype.Service;

import com.amazonaws.auth.AWSCredentialsProvider;
import com.amazonaws.auth.DefaultAWSCredentialsProviderChain;
import com.amazonaws.regions.Regions;
import com.amazonaws.services.comprehend.AmazonComprehend;
import com.amazonaws.services.comprehend.AmazonComprehendClientBuilder;
import com.amazonaws.services.comprehend.model.DetectEntitiesRequest;
import com.amazonaws.services.comprehend.model.DetectEntitiesResult;
import com.amazonaws.services.comprehend.model.DetectKeyPhrasesRequest;
import com.amazonaws.services.comprehend.model.DetectKeyPhrasesResult;
import com.amazonaws.services.comprehend.model.DetectSentimentRequest;
import com.amazonaws.services.comprehend.model.DetectSentimentResult;
import com.amazonaws.services.comprehend.model.Entity;

import lombok.Value;
import reactor.core.publisher.Mono;

@Service
public class AwsComprehendService {
	
	private AmazonComprehend comprehendClient;
	
	public AwsComprehendService() {					
		AWSCredentialsProvider awsCreds = DefaultAWSCredentialsProviderChain.getInstance();		
   	 
		comprehendClient = AmazonComprehendClientBuilder.standard()
	   	                                         .withCredentials(awsCreds)
	   	                                         .withRegion(Regions.US_EAST_1)
	   	                                         .build();    	
	}
	
	public void detectEntitiesRequest(String text) {		
	    DetectEntitiesRequest detectEntitiesRequest = new DetectEntitiesRequest().withText(text)
	                                                                             .withLanguageCode("pt");
	    DetectEntitiesResult detectEntitiesResult  = comprehendClient.detectEntities(detectEntitiesRequest);	    	    
	    detectEntitiesResult.getEntities().forEach(System.out::println);		    
	}
	
	public Mono<?> detectKeyPhrasesRequest(String text) {		
		DetectKeyPhrasesRequest detectKeyPhrasesRequest = new DetectKeyPhrasesRequest().withText(text)
																					   .withLanguageCode("pt");
		DetectKeyPhrasesResult detectKeyPhrasesResult = comprehendClient.detectKeyPhrases(detectKeyPhrasesRequest);
		return Mono.just(detectKeyPhrasesResult.getKeyPhrases());		
	}
	
	public Mono<?> detectSentiment(String text) {
		DetectSentimentRequest detectSentimentRequest = new DetectSentimentRequest().withText(text)
																					.withLanguageCode("pt");
		DetectSentimentResult detectSentimentResult = comprehendClient.detectSentiment(detectSentimentRequest);
		return Mono.just(detectSentimentResult.getSentimentScore());		
	}
	
	public Mono<List<Entity>> detectEntities(String text) {		
	    DetectEntitiesRequest detectEntitiesRequest = new DetectEntitiesRequest().withText(text)
	                                                                             .withLanguageCode("pt");
	    DetectEntitiesResult detectEntitiesResult  = comprehendClient.detectEntities(detectEntitiesRequest);
	    return Mono.just(detectEntitiesResult.getEntities());	    
	}

}
