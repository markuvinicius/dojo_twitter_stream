package br.com.dojo.twitter.rx.api.model;

import java.util.List;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@EqualsAndHashCode 
@NoArgsConstructor
@AllArgsConstructor
@Document(collection="tweets")
@Getter
@Setter
@Builder
public class Tweet {
	
	@Id
	private String id;
	
	@Field(value="texto")
	private String texto;
	
	@Field(value="usuario")
	private Object usuario;
	@Field(value="data")
	private String dataPostagem;
	@Field(value="hashtags")	
	private List<?> hashtags;
	@Field(value="user_mentions")
	private List<?> userMentions;
	@Field(value="retweeted")
	private boolean isRetweeted;
	@Field(value="quoted")
	private boolean isQuoted;
	@Field(value="quote_count")
	private Long quoteCount;
	@Field(value="reply_count")
	private Long replyCount;
	@Field(value="retweet_count")
	private Long retweetCount;
	@Field(value="favorite_count")
	private Long favoriteCount;
}
