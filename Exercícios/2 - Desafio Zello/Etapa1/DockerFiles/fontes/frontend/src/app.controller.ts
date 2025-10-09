import { Get, Controller, Res, Render } from '@nestjs/common';
import { Response } from 'express';
import { AppService } from './app.service';

@Controller()
export class AppController {
  constructor(private readonly appService: AppService) { }

  @Get()
  @Render('index')
  root() {
    return {};
  }

  @Get('resposta')
  async resposta(@Res() res: Response) {
    let cor = await this.appService.adivinhar();
    return res.render("resposta", cor);
  }

}
