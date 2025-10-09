package br.tec.zello.boladecristal.repository;

import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

import br.tec.zello.boladecristal.entity.Cor;

@Repository
public interface CorRepository extends MongoRepository<Cor, String> {

}
