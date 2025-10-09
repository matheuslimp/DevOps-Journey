package br.tec.zello.boladecristal.controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;

import br.tec.zello.boladecristal.entity.Cor;
import br.tec.zello.boladecristal.service.CorService;

@Controller
@RequestMapping(value = "/cor", produces = "application/json")
public class CorController {

	@Autowired
	private CorService corService;

	@GetMapping
	public ResponseEntity<List<Cor>> listar() {
		return ResponseEntity.ok(corService.listar());
	}
}
