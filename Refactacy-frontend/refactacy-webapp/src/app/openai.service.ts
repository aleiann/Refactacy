import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class OpenAIService {

  private apiUrl = 'http://127.0.0.1:5000/openai';  // URL dell'API

  constructor(private http: HttpClient) { }

  // Metodo per ottenere il nome
  getName(name: string): Observable<any> {
    const params = new HttpParams().set('name', name);  // Aggiungi il parametro 'name'

    return this.http.get(this.apiUrl, { params: params });
  }
}
