import { HttpException, HttpStatus, Injectable, Logger } from '@nestjs/common';
import { HttpService } from '@nestjs/axios';

@Injectable()
export class AppService {

  constructor(
    private httpService: HttpService
  ) { }

  obterIndiceAleatorio(min, max) {
    return parseInt(Math.random() * (max - min) + min);
  }

  async adivinhar(): Promise<any> {
    return new Promise((res, rej) => {
      this.httpService.get(`${process.env.URL_BACKEND}/boladecristal/api/cor`).toPromise()
        .then((r) => {
          const cores = r.data;
          let indice = this.obterIndiceAleatorio(0, cores.length);
          res(cores[indice]);
        }).catch(e => {
          Logger.error("Falha ao acessar backend", e);
          rej(new HttpException("Falha ao acessar backend", HttpStatus.BAD_REQUEST))
        })
    })
  }
}
