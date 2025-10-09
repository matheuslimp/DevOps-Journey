package br.tec.zello.boladecristal.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import br.tec.zello.boladecristal.entity.Cor;
import br.tec.zello.boladecristal.repository.CorRepository;

@Service
public class CorService {

	@Autowired
	private CorRepository corRepository;

	public List<Cor> listar() {
		List<Cor> resultado = corRepository.findAll();
		if (resultado.isEmpty()) {
			corRepository.save(Cor.builder().nome("Vermelho").codigo("red").build());
			corRepository.save(Cor.builder().nome("Azul").codigo("blue").build());
			corRepository.save(Cor.builder().nome("Preto").codigo("black").build());
			corRepository.save(Cor.builder().nome("Cinza").codigo("grey").build());
			corRepository.save(Cor.builder().nome("Verde").codigo("green").build());
			resultado = corRepository.findAll();
		}
		return resultado;
	}

}
