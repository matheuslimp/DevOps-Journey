package br.tec.zello.boladecristal.entity;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;

@Document
@EqualsAndHashCode
@Data
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class Cor {

	@Id
	private String id;
	private String nome;
	private String codigo;
}