package br.tec.zello.boladecristal;

import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.EnableAutoConfiguration;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.domain.EntityScan;
import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.context.ApplicationContext;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.data.mongodb.repository.config.EnableMongoRepositories;
import org.springframework.web.client.RestTemplate;

@SpringBootApplication
@EnableAutoConfiguration
@ComponentScan(basePackages = BolaDeCristalApplication.BASE_PACK)
@EntityScan(basePackages = BolaDeCristalApplication.BASE_PACK + ".entity")
@EnableMongoRepositories(basePackages = BolaDeCristalApplication.BASE_PACK + ".repository")
public class BolaDeCristalApplication {

	static final String BASE_PACK = "br.tec.zello.boladecristal";

	public static void main(String[] args) {
		SpringApplication.run(BolaDeCristalApplication.class, args);
	}

	@Bean
	public RestTemplate restTemplate(RestTemplateBuilder builder) {
		return builder.build();
	}

	@Bean
	public CommandLineRunner commandLineRunner(ApplicationContext ctx) {
		return args -> {
		};
	}

}